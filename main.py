import logging
from fastapi import (
    FastAPI,
    File,
    UploadFile,
    HTTPException,
    BackgroundTasks,
    Body,
    Depends,
    Security,
)
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Dict
from pathlib import Path
from openai import AsyncOpenAI
from dotenv import load_dotenv
from uuid import UUID, uuid4
import os
import shutil
import mimetypes
import fitz  # PyMuPDF
from docx import Document  # python-docx
from PIL import Image  # Pillow
import pytesseract  # Tesseract OCR
import json
import httpx  # Para realizar peticiones asíncronas a la URL de callback.
import hashlib
import hmac


# --- Configuración Inicial ---
load_dotenv()

# Configuración básica del logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Instancia de OpenAI
try:
    client = AsyncOpenAI()
except Exception as e:
    logger.error(f"Error al inicializar el cliente de OpenAI: {e}")
    # Podrías querer que la aplicación falle al iniciar si OpenAI es crítico.
    # exit(1)

# Inicialización de Supabase
try:
    from supabase import create_client, Client

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.error("Error: Supabase URL o Key no configurados en .env")
        # Considerar elevar una excepción o salir en entornos de producción.
        # exit(1)

    supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except ImportError:
    logger.error(
        "Error: La librería 'supabase' no está instalada. Por favor, ejecuta 'pip install supabase'"
    )
    # exit(1)
except Exception as e:
    logger.error(f"Error al inicializar el cliente de Supabase: {e}")
    # exit(1)

# Inicialización de la aplicación FastAPI.
app = FastAPI(
    title="API de Procesamiento de CVs",
    description="Una API para extraer información de currículums de forma asíncrona usando IA.",
    version="2.0.0",
)

# Directorio temporal para los CVs.
TEMP_CV_DIR = Path("temp")
TEMP_CV_DIR.mkdir(exist_ok=True)


# --- Modelos Pydantic ---


class Experiencia(BaseModel):
    puesto: str | None = Field(None, description="Puesto o cargo ocupado.")
    empresa: str | None = Field(None, description="Empresa donde se trabajó.")
    periodo: str | None = Field(
        None, description="Período de tiempo en el puesto (ej. '2018 - 2022')."
    )
    descripcion: str | None = Field(
        None, description="Descripción de las responsabilidades y logros."
    )


class Educacion(BaseModel):
    titulo: str | None = Field(None, description="Título o grado obtenido.")
    institucion: str | None = Field(None, description="Institución educativa.")
    periodo: str | None = Field(
        None, description="Período de tiempo de estudio (ej. '2014 - 2018')."
    )


class CVInfo(BaseModel):
    name: str | None = Field(None, description="Nombre completo del candidato.")
    email: str | None = Field(None, description="Correo electrónico de contacto.")
    phone: str | None = Field(None, description="Número de teléfono de contacto.")
    resumen: str | None = Field(
        None, description="Resumen profesional o perfil del candidato."
    )
    experiencia: List[Experiencia] | None = Field(
        [], description="Lista de experiencias laborales."
    )
    educacion: List[Educacion] | None = Field(
        [], description="Lista de formaciones académicas."
    )
    habilidades: List[str] | None = Field(
        [], description="Lista de habilidades técnicas o 'hard skills'."
    )
    soft_skills: List[str] | None = Field(
        [], description="Lista de habilidades blandas o 'soft skills'."
    )
    full_text: str | None = Field(
        None, description="El texto completo extraído del CV."
    )


class CallbackBody(BaseModel):
    callback_url: HttpUrl = Field(
        ..., description="URL a la que se enviará el resultado del procesamiento."
    )


# --- Seguridad y Autenticación ---

api_key_header_scheme = APIKeyHeader(name="Authorization", auto_error=False)


class AuthActor(BaseModel):
    user_id: str
    key_id: UUID


async def verify_api_key(
    api_key_header: str = Security(api_key_header_scheme),
) -> AuthActor:
    """
    Verifica la API Key y devuelve un objeto con el id de usuario y el id de la clave.
    """
    if not api_key_header or not api_key_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="No se proporcionó una API Key válida en el formato 'Bearer <key>'.",
        )

    provided_key = api_key_header.split(" ")[1]

    if len(provided_key) < 8:
        raise HTTPException(status_code=401, detail="API Key con formato inválido.")

    prefix = provided_key[:8]

    try:
        response = (
            supabase_client.from_("api_keys")
            .select("id_key, key_hash, id_user")
            .eq("pre", prefix)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=401, detail="API Key inválida.")

        provided_key_hash = hashlib.sha256(provided_key.encode()).hexdigest()

        for key_data in response.data:
            stored_hash = key_data.get("key_hash")
            if stored_hash and hmac.compare_digest(provided_key_hash, stored_hash):
                user_id = key_data.get("id_user")
                key_id = key_data.get("id_key")
                if user_id and key_id:
                    return AuthActor(user_id=user_id, key_id=key_id)

        raise HTTPException(status_code=401, detail="API Key inválida.")

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error durante la verificación de la API Key: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al validar la API Key.",
        )


# --- Funciones de Extracción de Texto ---


def get_mime_type(file_path: Path) -> str | None:
    mime_type, _ = mimetypes.guess_type(file_path.name)
    return mime_type


def extract_text_from_pdf(pdf_path: Path) -> str:
    text = ""
    try:
        document = fitz.open(pdf_path)
        for page in document:
            text += page.get_text()
        document.close()
    except Exception as e:
        logger.error(f"Error al extraer texto de PDF {pdf_path.name}: {e}")
    return text


def extract_text_from_docx(docx_path: Path) -> str:
    text = ""
    try:
        document = Document(docx_path)
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        logger.error(f"Error al extraer texto de DOCX {docx_path.name}: {e}")
    return text


def extract_text_from_image(image_path: Path) -> str:
    text = ""
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
    except pytesseract.TesseractNotFoundError:
        logger.error(
            "Error: Tesseract OCR no está instalado o no se encuentra en el PATH."
        )
    except Exception as e:
        logger.error(f"Error al extraer texto de imagen {image_path.name}: {e}")
    return text


async def extract_info_with_openai(text: str) -> CVInfo | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY":
        logger.error("Error: La clave de API de OpenAI no está configurada.")
        return None

    system_prompt = """
    Eres un asistente experto en reclutamiento y análisis de currículums.
    Tu tarea es analizar el texto de un CV que te proporcionaré y extraer la información clave.
    Debes devolver la información únicamente en formato JSON, siguiendo esta estructura:
    {
        "name": "string", "email": "string", "phone": "string", "resumen": "string",
        "experiencia": [{"puesto": "string", "empresa": "string", "periodo": "string", "descripcion": "string"}],
        "educacion": [{"titulo": "string", "institucion": "string", "periodo": "string"}],
        "habilidades": ["string"], "soft_skills": ["string"]
    }
    Si no encuentras información para un campo, usa `null`. El JSON debe ser completo y válido.
    """
    user_prompt = f"Analiza el siguiente texto de CV y extráelo en el formato JSON especificado:\n---\n{text}\n---"

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
        response_content = response.choices[0].message.content
        extracted_data = json.loads(response_content)
        extracted_data["full_text"] = text
        return CVInfo(**extracted_data)
    except Exception as e:
        logger.exception(f"Error en la API de OpenAI: {e}")
        return None


# --- BackgroundTasks ---


async def process_cv_and_callback(id_request: UUID, file_path: Path):
    """
    Tarea que se ejecuta en segundo plano.
    1. Recupera la información de la petición desde la BBDD.
    2. Procesa el CV (extracción de texto + OpenAI).
    3. Actualiza el estado de la petición en la tabla `requests`.
    4. Guarda el resultado detallado en la tabla `request_logs`.
    5. Envía el resultado final a la URL de callback.
    """
    # Inicializar variables para el bloque finally
    endpoint_info = None
    payload_out = None
    error_message = None

    try:
        logger.info(f"Iniciando procesamiento de CV para la petición: {id_request}")
        # 1. Obtener datos de la petición y del endpoint asociado
        req_response = (
            supabase_client.from_("requests")
            .select("*, endpoints(info)")
            .eq("id_request", str(id_request))
            .single()
            .execute()
        )
        if not req_response.data:
            raise ValueError(f"No se encontró la petición con id {id_request}")

        request_data = req_response.data
        endpoint_info = request_data.get("endpoints", {}).get("info", {})
        callback_url = endpoint_info.get("callbackURL")

        if not callback_url:
            raise ValueError(
                f"No se encontró callbackURL en la configuración del endpoint para la petición {id_request}"
            )
        logger.info(
            f"Petición {id_request} y endpoint {request_data.get('endpoint_id')} encontrados. Callback URL: {callback_url}"
        )

        # 2. Procesar el archivo
        mime_type = get_mime_type(file_path)
        logger.info(f"Procesando archivo {file_path.name} con tipo MIME: {mime_type}")
        extracted_text = ""
        if mime_type == "application/pdf":
            extracted_text = extract_text_from_pdf(file_path)
        elif (
            mime_type
            == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            extracted_text = extract_text_from_docx(file_path)
        elif mime_type and mime_type.startswith("image/"):
            extracted_text = extract_text_from_image(file_path)
        else:
            raise ValueError(f"Tipo de archivo no soportado: {mime_type}")

        if not extracted_text:
            raise ValueError("No se pudo extraer texto del archivo o está vacío.")
        logger.info(
            f"Texto extraído del CV para la petición {id_request}. Longitud: {len(extracted_text)}"
        )

        cv_info = await extract_info_with_openai(extracted_text)
        if not cv_info:
            raise ValueError("Fallo en la extracción de información con OpenAI.")
        logger.info(
            f"Información de CV extraída con éxito para la petición {id_request}."
        )

        # 3. Preparar resultados
        status = "completed"
        payload_out = {"status": status, "data": cv_info.model_dump()}

    except Exception as e:
        status = "failed"
        error_message = str(e)
        payload_out = {"status": status, "error": error_message, "data": None}
        logger.exception(
            f"Fallo en el procesamiento para la petición {id_request}: {e}"
        )

    finally:
        # 4. Actualizar estado en la tabla 'requests'
        try:
            await supabase_client.from_("requests").update({"status": status}).eq(
                "id_request", str(id_request)
            ).execute()
            logger.info(f"Estado de la petición {id_request} actualizado a '{status}'.")
        except Exception as e:
            logger.exception(
                f"Error al actualizar el estado de la petición {id_request}: {e}"
            )

        # 5. Insertar log en la tabla 'request_logs'
        try:
            log_entry = {
                "id_request": str(id_request),
                "payload_out": payload_out,
                "error": error_message,
            }
            await supabase_client.from_("request_logs").insert(log_entry).execute()
            logger.info(f"Log insertado para la petición {id_request}.")
        except Exception as e:
            logger.exception(
                f"Error al insertar el log para la petición {id_request}: {e}"
            )

        # 6. Enviar notificación al callback
        if endpoint_info and (callback_url := endpoint_info.get("callbackURL")):
            async with httpx.AsyncClient() as async_client:
                try:
                    await async_client.post(
                        callback_url, json=payload_out, timeout=30.0
                    )
                    logger.info(
                        f"Resultado enviado al callback {callback_url} para la petición {id_request}."
                    )
                except httpx.RequestError as e:
                    logger.exception(
                        f"Error al enviar el resultado al callback para la petición {id_request} a {callback_url}: {e}"
                    )
        else:
            logger.warning(
                f"No se pudo enviar el callback para la petición {id_request}: No se encontró callbackURL."
            )

        # 7. Limpiar archivo temporal
        if file_path.exists():
            try:
                os.remove(file_path)
                logger.info(f"Archivo temporal {file_path.name} eliminado.")
            except Exception as e:
                logger.exception(
                    f"Error al eliminar el archivo temporal {file_path.name}: {e}"
                )


# --- Endpoints de la API ---


@app.get("/", summary="Endpoint de Bienvenida")
async def read_root():
    """Devuelve un mensaje de bienvenida para verificar que la API está activa."""
    logger.info("Solicitud recibida en el endpoint de bienvenida.")
    return {"message": "Bienvenido a la API de Procesamiento de CVs"}


@app.post("/cv/{endpoint_id}", status_code=202, summary="Subir CV")
async def upload_cv(
    endpoint_id: UUID,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    actor: AuthActor = Depends(verify_api_key),
):
    """
    Acepta un archivo de CV para procesamiento asíncrono.
    - Requiere una API Key válida en el header `Authorization: Bearer <key>`.
    - El `endpoint_id` debe corresponder a una configuración creada por el usuario.
    - La API responde inmediatamente y envía el resultado al webhook configurado.
    """
    try:
        logger.info(
            f"Solicitud de subida de CV recibida para el endpoint {endpoint_id} por el usuario {actor.user_id}."
        )
        # 1. Validar que el endpoint existe y pertenece al usuario autenticado
        endpoint_response = (
            await supabase_client.from_("endpoints")
            .select("id_user, info")
            .eq("id", str(endpoint_id))
            .single()
            .execute()
        )

        if not endpoint_response.data:
            logger.warning(
                f"Endpoint con id '{endpoint_id}' no encontrado para el usuario {actor.user_id}."
            )
            raise HTTPException(
                status_code=404,
                detail=f"Endpoint con id '{endpoint_id}' no encontrado.",
            )

        endpoint_data = endpoint_response.data
        if endpoint_data.get("id_user") != actor.user_id:
            logger.warning(
                f"Usuario {actor.user_id} intentó usar endpoint {endpoint_id} que pertenece a {endpoint_data.get('id_user')}."
            )
            raise HTTPException(
                status_code=403, detail="No tienes permiso para usar este endpoint."
            )

        # 2. Crear un registro de la petición en la base de datos
        request_payload = {
            "id_user": actor.user_id,
            "id_key": str(actor.key_id),
            "endpoint_id": str(endpoint_id),
            "status": "processing",  # Estado inicial mientras se guarda el archivo
        }
        request_response = (
            await supabase_client.from_("requests").insert(request_payload).execute()
        )
        id_request = request_response.data[0]["id_request"]
        logger.info(f"Petición {id_request} registrada en la base de datos.")

        # 3. Guardar el archivo en disco
        filename = Path(file.filename).name.strip()
        unique_filename = f"{uuid4()}_{filename}"
        file_path = TEMP_CV_DIR / unique_filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(
            f"Archivo '{filename}' guardado temporalmente como '{unique_filename}' para la petición {id_request}."
        )

        # 4. Añadir la tarea de procesamiento al segundo plano
        background_tasks.add_task(process_cv_and_callback, id_request, file_path)
        logger.info(
            f"Tarea de procesamiento para la petición {id_request} añadida a BackgroundTasks."
        )

        return {
            "message": "Archivo recibido. El procesamiento ha comenzado.",
            "request_id": id_request,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(
            f"Error durante el manejo inicial del archivo o la petición para el endpoint {endpoint_id} por el usuario {actor.user_id}: {e}"
        )
        raise HTTPException(
            status_code=500, detail=f"Error al guardar el archivo para procesar: {e}"
        )
