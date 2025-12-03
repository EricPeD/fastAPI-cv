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
import io
import base64

from src.config import logger, openai_client, supabase_client
from src.models import CVInfo


# Directorio temporal para los CVs.
TEMP_CV_DIR = Path("temp")
TEMP_CV_DIR.mkdir(exist_ok=True)


def get_mime_type(file_path: Path) -> str | None:
    mime_type, _ = mimetypes.guess_type(file_path.name)
    return mime_type

async def extract_info_with_openai_vision(file_path: Path, output_schema: dict | None = None) -> dict | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY":
        logger.error("Error: La clave de API de OpenAI no está configurada.")
        return None

    if not file_path.exists():
        logger.error(f"Archivo no encontrado para OpenAI Vision: {file_path}")
        return None

    messages_content = [{"type": "text", "text": "Extrae toda la información de este archivo en formato JSON exacto."}]
    
    mime_type = get_mime_type(file_path)
    
    if mime_type == "application/pdf":
        try:
            document = fitz.open(file_path)
            for page_num, page in enumerate(document):
                if page_num >= 10: # Limitar a las primeras 10 páginas
                    logger.warning(f"CV {file_path.name} tiene más de 10 páginas. Solo se procesarán las primeras 10.")
                    break
                pix = page.get_pixmap()
                img_bytes = io.BytesIO()
                # Guardar el pixmap como PNG en memoria
                Image.frombytes("RGB", [pix.width, pix.height], pix.samples).save(img_bytes, format="PNG")
                base64_image = base64.b64encode(img_bytes.getvalue()).decode("utf-8")
                messages_content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}", "detail": "high"}
                })
            document.close()
            if len(messages_content) == 1: # Check if any images were added
                logger.error(f"No se pudo extraer ninguna imagen de las páginas del PDF {file_path.name}.")
                return None
        except Exception as e:
            logger.exception(f"Error al procesar PDF para OpenAI Vision {file_path.name}: {e}")
            return None
    elif mime_type and mime_type.startswith("image/"):
        try:
            with open(file_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")
            messages_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:{mime_type};base64,{base64_image}", "detail": "high"}
            })
        except Exception as e:
            logger.exception(f"Error al procesar imagen para OpenAI Vision {file_path.name}: {e}")
            return None
    else:
        logger.error(f"Tipo de archivo no soportado para OpenAI Vision: {mime_type} en {file_path.name}")
        return None
    
    if not output_schema:
        raise ValueError("El esquema de salida (output_schema) es obligatorio para el análisis.")

    schema_string = json.dumps(output_schema, indent=2, ensure_ascii=False)
    system_prompt = f"""
    Eres un agente de IA autónomo especializado en el análisis de documentos. Tu objetivo es procesar el siguiente documento (proporcionado como imagen) y extraer la información solicitada en un formato JSON estricto.

    OBJETIVO ACTUAL: Analizar un documento.
    ESQUEMA DE SALIDA REQUERIDO (DEBES SEGUIRLO ESTRICTAMENTE):
    {schema_string}

    REGLAS ADICIONALES:
    - Tu respuesta debe ser ÚNICAMENTE el objeto JSON puro y válido. No incluyas texto introductorio, comentarios, ni bloques de código como ```json.
    - No inventes información que no esté explícitamente en el documento.
    """
    
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": messages_content},
            ],
            response_format={"type": "json_object"},
            # temperature=0.1,
            max_completion_tokens=10000 # Parámetro corregido
        )

        json_text = response.choices[0].message.content.strip()
        logger.debug(f"Raw JSON response from OpenAI Vision: {json_text}")
        
        # Limpieza adicional de la respuesta de la IA
        if json_text.startswith("```json"):
            json_text = json_text[7:-3].strip()
        elif json_text.startswith("```"):
            json_text = json_text[3:-3].strip()

        extracted_data = json.loads(json_text)
        
        return extracted_data

    except json.JSONDecodeError as e:
        logger.error(f"Error: La IA devolvió JSON inválido en OpenAI Vision:\n{json_text}\nError: {e}")
        return None
    except Exception as e:
        logger.exception(f"Error al procesar el CV con OpenAI Vision: {e}")
        return None

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


async def extract_info_from_text_with_openai(text: str, output_schema: dict | None = None) -> dict | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY":
        logger.error("Error: La clave de API de OpenAI no está configurada.")
        return None

    if not output_schema:
        raise ValueError("El esquema de salida (output_schema) es obligatorio para el análisis.")

    schema_string = json.dumps(output_schema, indent=2, ensure_ascii=False)
    system_prompt = f"""
    Eres un agente de IA autónomo especializado en el análisis de documentos. Tu objetivo es procesar el siguiente documento (proporcionado como texto) y extraer la información solicitada en un formato JSON estricto.

    OBJETIVO ACTUAL: Analizar un documento de texto.
    ESQUEMA DE SALIDA REQUERIDO (DEBES SEGUIRLO ESTRICTAMENTE):
    {schema_string}

    REGLAS ADICIONALES:
    - Tu respuesta debe ser ÚNICAMENTE el objeto JSON puro y válido. No incluyas texto introductorio, comentarios, ni bloques de código como ```json.
    - No inventes información que no esté explícitamente en el documento.
    """
    user_prompt = f"Analiza el siguiente texto y extrae la información destacable en el formato JSON especificado:\n---\n{text}\n---"

    try:
        response = await openai_client.chat.completions.create(
            model="gpt-5-nano",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        response_content = response.choices[0].message.content
        logger.debug(f"Raw JSON response from OpenAI Text: {response_content}")
        extracted_data = json.loads(response_content)

        # Siempre se devuelve un diccionario porque el esquema es dinámico
        return extracted_data
            
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

        # Parche para manejar el caso en que 'info' se almacena como un string de JSON
        if isinstance(endpoint_info, str):
            try:
                endpoint_info = json.loads(endpoint_info)
            except json.JSONDecodeError:
                raise ValueError(f"El campo 'info' del endpoint para la petición {id_request} no es un JSON válido.")

        callback_url = endpoint_info.get("callbackURL")
        output_schema = endpoint_info.get("schema") # Extraer el esquema personalizado

        if not callback_url:
            raise ValueError(
                f"No se encontró callbackURL en la configuración del endpoint para la petición {id_request}"
            )
        logger.info(
            f"Petición {id_request} y endpoint {request_data.get('endpoint_id')} encontrados. Callback URL: {callback_url}"
        )

        # 2. Procesar el archivo con la nueva lógica y fallback
        cv_info: dict | None = None # Cambiado a dict
        mode = endpoint_info.get("analysis_mode", "vision_first")  # Default a vision_first

        # --- Intento con OpenAI Vision ---
        if mode in ["vision_first", "vision_only"]:
            try:
                logger.info(f"Intentando análisis con 'openai_vision' para petición {id_request}")
                cv_info = await extract_info_with_openai_vision(file_path, output_schema) # Pasar el schema
                if cv_info:
                    logger.info(f"Análisis 'openai_vision' exitoso para petición {id_request}.")
            except Exception as e:
                logger.warning(f"Análisis 'openai_vision' falló para petición {id_request}: {e}")
                if mode == "vision_only":
                    raise  # Si el modo es solo visión, no hacemos fallback, la excepción se relanza.

        # --- Fallback o Intento Directo con Manual Text ---
        if cv_info is None:
            if mode == "vision_first":
                logger.info(f"Haciendo fallback a análisis 'manual_text' para petición {id_request}.")
            elif mode == "manual_only":
                logger.info(f"Iniciando análisis con 'manual_text' según configuración para petición {id_request}.")
            
            # Lógica de extracción de texto local
            mime_type = get_mime_type(file_path)
            logger.info(f"Procesando archivo {file_path.name} para texto manual con tipo MIME: {mime_type}")
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
            # No se soportan otros tipos para el modo manual
            elif mime_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"] and not (mime_type and mime_type.startswith("image/")):
                 raise ValueError(f"Tipo de archivo no soportado para análisis manual: {mime_type}")


            if not extracted_text:
                raise ValueError("No se pudo extraer texto del archivo para el análisis manual o está vacío.")
            logger.info(f"Texto extraído del CV para petición {id_request}. Longitud: {len(extracted_text)}")

            cv_info = await extract_info_from_text_with_openai(extracted_text, output_schema) # Pasar el schema
        
        if not cv_info:
            raise ValueError("Todos los métodos de análisis fallaron para extraer información del CV.")
        
        logger.info(
            f"Información de CV extraída con éxito para la petición {id_request}."
        )

        # 3. Preparar resultados
        status = "completed"
        payload_out = {"status": status, "data": cv_info}

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

        # 6. Enviar notificación al callback con lógica de reintentos
        if endpoint_info and (callback_url := endpoint_info.get("callbackURL")):
            retries = 3
            delay = 2.0  # en segundos
            for i in range(retries):
                try:
                    async with httpx.AsyncClient() as async_client:
                        response = await async_client.post(
                            callback_url, json=payload_out, timeout=30.0
                        )
                        response.raise_for_status()  # Lanza excepción para respuestas 4xx/5xx
                        logger.info(
                            f"Resultado enviado al callback {callback_url} para la petición {id_request} (intento {i+1})."
                        )
                        break  # Salir del bucle si tiene éxito
                except (httpx.RequestError, httpx.HTTPStatusError) as e:
                    logger.warning(
                        f"Fallo al enviar callback para {id_request} (intento {i+1}/{retries}): {e}"
                    )
                    if i < retries - 1:
                        await asyncio.sleep(delay)
                        delay *= 2  # Backoff exponencial
                    else:
                        logger.error(
                            f"Fallo final al enviar callback para {id_request} tras {retries} intentos."
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
                