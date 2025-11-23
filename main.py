from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path
import os
import shutil
import mimetypes
import fitz # PyMuPDF: Biblioteca para manipulación de PDFs.
from docx import Document # python-docx: Biblioteca para trabajar con archivos .docx.
from PIL import Image # Pillow: Biblioteca para procesamiento de imágenes.
import pytesseract # Wrapper de Python para el motor Tesseract OCR.
from pydantic import BaseModel # Para definir modelos de datos y validación.
import re # Módulo para usar expresiones regulares.

# Inicialización de la aplicación FastAPI.
app = FastAPI()

# Directorio temporal donde se almacenarán los archivos de CV subidos.
# Es crucial para manejar archivos de forma segura y temporal.
TEMP_CV_DIR = Path("temp")
TEMP_CV_DIR.mkdir(exist_ok=True) # Crea el directorio si no existe, evita errores si ya está.

# Modelo Pydantic para estructurar la información extraída del CV.
# Esto asegura una salida JSON consistente y validada.
class CVInfo(BaseModel):
    name: str | None = None  # Nombre del candidato, puede ser None si no se extrae.
    email: str | None = None # Email del candidato, puede ser None.
    phone: str | None = None # Número de teléfono del candidato, puede ser None.
    full_text: str | None = None # El texto completo extraído del CV, útil para depuración o análisis posterior.
    # Se pueden añadir más campos aquí para una extracción más detallada (ej. experiencia, educación, habilidades).

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

def extract_info_from_text(text: str) -> CVInfo:
    """
    Extrae información clave (email, teléfono, nombre) del texto plano de un CV
    utilizando expresiones regulares.
    """
    name = None
    email = None
    phone = None

    # Expresión regular para email. Es un patrón común para correos electrónicos.
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    if email_match:
        email = email_match.group(0)

    # Expresión regular para teléfono. Intenta capturar varios formatos de números de teléfono,
    # incluyendo códigos de país y separadores comunes. Podría necesitar refinamiento.
    phone_match = re.search(r"(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?(\d{3}[-.\s]?\d{4}|\d{7})", text)
    if phone_match:
        phone = phone_match.group(0)
    
    # *** A MEJORAR ***
    # La extracción del nombre es un punto débil actual.
    # Se necesitaría una lógica más sofisticada (ej. buscar la primera línea prominente,
    # o usar técnicas de PNL) para extraer el nombre de forma fiable.
    # Actualmente, 'name' siempre será None.

    return CVInfo(name=name, email=email, phone=phone, full_text=text)


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
            return {"filename": filename, "status": "Uploaded, MIME type not detected. Proceed with caution.", "detected_mime_type": None}
        
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
            return {"filename": filename, "detected_mime_type": detected_mime_type, "message": "Tipo de archivo no soportado aún para extracción de texto."}

        # *** IMPORTANTE ***
        # Elimina el archivo temporal del disco después de que ha sido procesado.
        # Esto es crucial por seguridad, privacidad y gestión del espacio en disco.
        os.remove(file_path)
        
        if extracted_text:
            # Extrae la información estructurada del texto plano.
            cv_info = extract_info_from_text(extracted_text)
            return cv_info # FastAPI serializa automáticamente el objeto CVInfo a JSON.
        else:
            # Si por alguna razón no se extrajo texto (ej. archivo vacío o error silencioso).
            return {"filename": filename, "detected_mime_type": detected_mime_type, "message": "No se pudo extraer texto del archivo o el archivo está vacío."}

    except HTTPException:
        # Si ya hemos levantado una HTTPException específica, la relanzamos.
        raise
    except Exception as e:
        # Captura cualquier otra excepción inesperada durante el proceso.
        # Asegura que el archivo temporal se elimine incluso si hay un error.
        if file_path and file_path.exists():
            os.remove(file_path)
        # Registra el error y lo propaga como una excepción HTTP 500 para el cliente.
        print(f"Error general al subir o procesar el archivo: {e}")
        raise HTTPException(status_code=500, detail=f"Error al subir o procesar el archivo: {e}")
