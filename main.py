from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path
import os
import shutil
import mimetypes
import fitz # PyMuPDF: Biblioteca para manipulación de PDFs.
from docx import Document # python-docx: Biblioteca para trabajar con archivos .docx.
from PIL import Image # Pillow: Biblioteca para procesamiento de imágenes.
import pytesseract # Wrapper de Python para el motor Tesseract OCR.
from pydantic import BaseModel, Field
from typing import List
from openai import AsyncOpenAI
import json
import re
from dotenv import load_dotenv

load_dotenv()

# instancia OpenAI
client = AsyncOpenAI()

# Inicialización de la aplicación FastAPI.
app = FastAPI()

# Directorio temporal donde se almacenarán los archivos de CV subidos.
# Es crucial para manejar archivos de forma segura y temporal.
TEMP_CV_DIR = Path("temp")
TEMP_CV_DIR.mkdir(exist_ok=True) # Crea el directorio si no existe, evita errores si ya está.

# Modelos Pydantic para estructurar la información extraída del CV.
# Esto asegura una salida JSON consistente y validada, con campos anidados.

class Experiencia(BaseModel):
    puesto: str | None = Field(None, description="Puesto o cargo ocupado.")
    empresa: str | None = Field(None, description="Empresa donde se trabajó.")
    periodo: str | None = Field(None, description="Período de tiempo en el puesto (ej. '2018 - 2022').")
    descripcion: str | None = Field(None, description="Descripción de las responsabilidades y logros.")

class Educacion(BaseModel):
    titulo: str | None = Field(None, description="Título o grado obtenido.")
    institucion: str | None = Field(None, description="Institución educativa.")
    periodo: str | None = Field(None, description="Período de tiempo de estudio (ej. '2014 - 2018').")

class CVInfo(BaseModel):
    name: str | None = Field(None, description="Nombre completo del candidato.")
    email: str | None = Field(None, description="Correo electrónico de contacto.")
    phone: str | None = Field(None, description="Número de teléfono de contacto.")
    resumen: str | None = Field(None, description="Resumen profesional o perfil del candidato.")
    experiencia: List[Experiencia] | None = Field([], description="Lista de experiencias laborales.")
    educacion: List[Educacion] | None = Field([], description="Lista de formaciones académicas.")
    habilidades: List[str] | None = Field([], description="Lista de habilidades técnicas o 'hard skills'.")
    soft_skills: List[str] | None = Field([], description="Lista de habilidades blandas o 'soft skills'.")
    full_text: str | None = Field(None, description="El texto completo extraído del CV.")

async def extract_info_with_openai(text: str) -> CVInfo:
    """
    Utiliza la API de OpenAI para extraer información estructurada del texto de un CV.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY":
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key not found or not configured. Please set the OPENAI_API_KEY environment variable."
        )

    system_prompt = """
    Eres un asistente experto en reclutamiento y análisis de currículums.
    Tu tarea es analizar el texto de un CV que te proporcionaré y extraer la información clave.
    Debes devolver la información únicamente en formato JSON, siguiendo esta estructura:
    {
        "name": "string",
        "email": "string",
        "phone": "string",
        "resumen": "string",
        "experiencia": [{"puesto": "string", "empresa": "string", "periodo": "string", "descripcion": "string"}],
        "educacion": [{"titulo": "string", "institucion": "string", "periodo": "string"}],
        "habilidades": ["string"],
        "soft_skills": ["string"]
    }
    El JSON debe ser completo y válido. Si no encuentras información para un campo, usa `null`.
    """

    # cv a analizar.
    user_prompt = f"""
    Aquí está el texto del CV. Por favor, extráelo en el formato JSON especificado.
    Texto del CV:
    ---
    {text}
    ---
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )

        # Extrae y parsea el contenido JSON de la respuesta.
        response_content = response.choices[0].message.content
        extracted_data = json.loads(response_content)

        # Añade el texto completo original a los datos extraídos
        extracted_data['full_text'] = text

        # Valida y crea una instancia del modelo CVInfo con los datos extraídos.
        cv_info = CVInfo(**extracted_data)
        return cv_info

    except json.JSONDecodeError:
        print("Error: La respuesta de OpenAI no fue un JSON válido.")
        raise HTTPException(status_code=500, detail="OpenAI returned invalid JSON.")
    except Exception as e:
        print(f"An error occurred with OpenAI API: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred with OpenAI API: {str(e)}")


# def extract_info_from_text(text: str) -> CVInfo:
#     """
#     Extrae información clave (email, teléfono, nombre) del texto plano de un CV
#     utilizando expresiones regulares.
#     """
#     name = None
#     email = None
#     phone = None

#     # Expresión regular para email. Es un patrón común para correos electrónicos.
#     email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
#     if email_match:
#         email = email_match.group(0)

#     # Expresión regular para teléfono. Intenta capturar varios formatos de números de teléfono,
#     # incluyendo códigos de país y separadores comunes. Podría necesitar refinamiento.
#     phone_match = re.search(r"(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?(\d{3}[-.\s]?\d{4}|\d{7})", text)
#     if phone_match:
#         phone = phone_match.group(0)
    
#     # Estos campos no se extraían con regex. Se inicializan como None para el modelo.
#     resumen = None
#     experiencia = []
#     educacion = []
#     habilidades = []
#     soft_skills = []

#     return CVInfo(
#         name=name,
#         email=email,
#         phone=phone,
#         full_text=text,
#         resumen=resumen,
#         experiencia=experiencia,
#         educacion=educacion,
#         habilidades=habilidades,
#         soft_skills=soft_skills
#     )


def get_mime_type(file_path: Path) -> str | None:
    """
    Intenta obtener el tipo MIME (ej. 'application/pdf', 'image/jpeg') de un archivo
    basándose en su extensión. Es un paso fundamental para despachar el archivo
    al procesador correcto.
    """
    mime_type, _ = mimetypes.guess_type(file_path.name)
    return mime_type

def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extrae todo el texto de un archivo PDF utilizando PyMuPDF.
    PyMuPDF es muy eficiente ya que los PDFs a menudo contienen el texto como datos incrustados.
    """
    text = ""
    try:
        document = fitz.open(pdf_path) # Abre el documento PDF.
        for page_num in range(len(document)): # Itera sobre cada página.
            page = document.load_page(page_num)
            text += page.get_text() # Extrae el texto de la página y lo concatena.
        document.close() # Cierra el documento para liberar recursos.
    except Exception as e:
        # Registra el error y lo propaga como una excepción HTTP 500 para el cliente.
        print(f"Error al extraer texto de PDF {pdf_path}: {e}")
        raise HTTPException(status_code=500, detail=f"Error al procesar el PDF: {e}")
    return text

def extract_text_from_docx(docx_path: Path) -> str:
    """
    Extrae todo el texto de un archivo DOCX utilizando la librería python-docx.
    Recorre los párrafos del documento para obtener su contenido textual.
    """
    text = ""
    try:
        document = Document(docx_path) # Abre el documento DOCX.
        for paragraph in document.paragraphs: # Itera sobre cada párrafo.
            text += paragraph.text + "\n" # Concatena el texto del párrafo con un salto de línea.
    except Exception as e:
        # Registra el error y lo propaga como una excepción HTTP 500.
        print(f"Error al extraer texto de DOCX {docx_path}: {e}")
        raise HTTPException(status_code=500, detail=f"Error al procesar el DOCX: {e}")
    return text

def extract_text_from_image(image_path: Path) -> str:
    """
    Extrae texto de un archivo de imagen (JPG, PNG, etc.) utilizando Tesseract OCR.
    La precisión depende en gran medida de la calidad de la imagen y la configuración de Tesseract.
    """
    text = ""
    try:
        img = Image.open(image_path) # Abre la imagen con Pillow.
        # Aplica OCR a la imagen. Se podría mejorar la precisión especificando el idioma, ej: pytesseract.image_to_string(img, lang='spa').
        text = pytesseract.image_to_string(img) 
    except pytesseract.TesseractNotFoundError:
        # Excepción específica si Tesseract OCR no está instalado o su ruta no está configurada correctamente.
        raise HTTPException(status_code=500, detail="Tesseract OCR no está instalado o no se encuentra en el PATH. Por favor, instálalo.")
    except Exception as e:
        # Registra otros errores durante el procesamiento de la imagen con OCR.
        print(f"Error al extraer texto de imagen {image_path}: {e}")
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen con OCR: {e}")
    return text

@app.get("/")
async def read_root():
    """
    Endpoint de prueba básico para verificar que la API está funcionando.
    """
    return {"message": "Hello World!"}

@app.post("/cv")
async def upload_cv(file: UploadFile = File(...)):
    """
    Endpoint principal para subir un archivo de CV, procesarlo y extraer información.
    Soporta PDF, DOCX y varios formatos de imagen.
    """
    file_path = None # Inicializa file_path fuera del try para asegurar que esté disponible en el finally/except.
    try:
        # Sanitiza el nombre del archivo para prevenir ataques de 'path traversal',
        # asegurando que solo se use el nombre base del archivo.
        filename = Path(file.filename).name
        file_path = TEMP_CV_DIR / filename

        # Guarda el archivo subido en el directorio temporal.
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Detecta el tipo MIME del archivo para decidir cómo procesarlo.
        detected_mime_type = get_mime_type(file_path)

        if not detected_mime_type:
            # Si el tipo MIME no se puede detectar (ej. extensión inusual), se informa al cliente.
            raise HTTPException(status_code=400, detail="Could not determine file MIME type.")
        
        extracted_text = None
        # Despacha el procesamiento del archivo según el tipo MIME detectado.
        if detected_mime_type == "application/pdf":
            extracted_text = extract_text_from_pdf(file_path)
        elif detected_mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            extracted_text = extract_text_from_docx(file_path)
        elif detected_mime_type.startswith("image/"): # Procesa cualquier tipo de imagen (jpeg, png, etc.).
            extracted_text = extract_text_from_image(file_path)
        else:
            # Maneja tipos de archivo no soportados.
            raise HTTPException(status_code=415, detail=f"Unsupported file type: {detected_mime_type}")
        
        if not extracted_text:
            # Si por alguna razón no se extrajo texto (ej. archivo vacío o error silencioso).
            raise HTTPException(status_code=422, detail="Could not extract text from the file or the file is empty.")

        # Extrae la información estructurada del texto plano usando OpenAI.
        cv_info = await extract_info_with_openai(extracted_text)
        return cv_info # FastAPI serializa automáticamente el objeto CVInfo a JSON.

    except HTTPException:
        # Si ya hemos levantado una HTTPException específica, la relanzamos.
        raise
    except Exception as e:
        # Captura cualquier otra excepción inesperada durante el proceso.
        # Registra el error y lo propaga como una excepción HTTP 500 para el cliente.
        print(f"General error during file upload or processing: {e}")
        raise HTTPException(status_code=500, detail=f"Error uploading or processing file: {e}")
    finally:
        # Este bloque se ejecuta siempre, garantizando la limpieza del archivo temporal.
        # Es crucial por seguridad, privacidad y gestión del espacio en disco.
        if file_path and file_path.exists():
            os.remove(file_path)
