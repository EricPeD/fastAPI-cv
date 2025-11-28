import asyncio
import os
import mimetypes
import json
import httpx
import fitz
from docx import Document
from PIL import Image
import pytesseract
from pathlib import Path
from uuid import UUID

from src.config import logger, openai_client, supabase_client
from src.models import CVInfo


# Directorio temporal para los CVs.
TEMP_CV_DIR = Path("temp")
TEMP_CV_DIR.mkdir(exist_ok=True)


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
    Si no encuentras información para un campo principal (ej. name, email), usa `null`. Para elementos dentro de listas (ej. habilidades, soft_skills), omite el elemento de la lista si no se encuentra un valor válido, en lugar de usar `null`. El JSON debe ser completo y válido.
    """
    user_prompt = f"Analiza el siguiente texto de CV y extráelo en el formato JSON especificado:\n---\n{text}\n---"

    try:
        response = await openai_client.chat.completions.create(
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
    status = "failed"  # Default status in case of immediate failure

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
            loop = asyncio.get_running_loop()
            extracted_text = await loop.run_in_executor(
                None,  # Usa el executor por defecto (ThreadPoolExecutor)
                extract_text_from_image,
                file_path,
            )
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
            # Need to re-fetch request_data if status was 'pending' and we defaulted it to 'failed'
            # Or ensure request_data is available
            (
                supabase_client.from_("requests")
                .update({"status": status})
                .eq("id_request", str(id_request))
                .execute()
            )
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
            (supabase_client.from_("request_logs").insert(log_entry).execute())
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
