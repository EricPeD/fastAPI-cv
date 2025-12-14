import asyncio
import os
import mimetypes
import json
import httpx
from pathlib import Path
from uuid import UUID
from typing import Tuple

from src.config import logger, supabase_client
from src.users.service import deduct_credits_atomic
from src.exceptions import DatabaseError, FileProcessingError, OpenAIError, InsufficientCreditsError
from src.models import Usage
from . import analysis, extraction

# Directorio temporal para los CVs.
TEMP_CV_DIR = Path("temp")
TEMP_CV_DIR.mkdir(exist_ok=True)

async def _get_request_details(id_request: UUID) -> dict:
    """Helper to fetch request and endpoint data."""
    try:
        response = await (
            supabase_client.from_("requests")
            .select("*, endpoints(info)")
            .eq("id_request", str(id_request))
            .single()
            .execute()
        )
        if not response.data:
            raise DatabaseError(f"No se encontró la petición con id {id_request}")
        return response.data
    except Exception as e:
        logger.error(f"Error fetching request details for {id_request}: {e}")
        raise DatabaseError("Error al obtener los detalles de la petición.")

def _get_text_extractor(mime_type: str | None):
    """Returns the appropriate text extraction function based on MIME type."""
    if mime_type == "application/pdf":
        return extraction.extract_text_from_pdf
    if mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extraction.extract_text_from_docx
    if mime_type and mime_type.startswith("image/"):
        return extraction.extract_text_from_image
    return None

async def _run_analysis(mode: str, file_path: Path, output_schema: dict) -> Tuple[dict, Usage]:
    """Orchestrates the analysis process and aggregates token usage."""
    cv_info: dict | None = None
    total_usage: Usage | None = None

    if mode in ["vision_first", "vision_only"]:
        try:
            cv_info, vision_usage = await analysis.extract_info_with_openai_vision(file_path, output_schema)
            total_usage = vision_usage
            logger.info(f"Análisis 'openai_vision' exitoso para {file_path.name}.")
        except OpenAIError as e:
            if mode == "vision_only":
                raise
            logger.warning(f"Análisis 'openai_vision' falló, intentando fallback a texto: {e}")

    if cv_info is None:
        mime_type, _ = mimetypes.guess_type(file_path.name)
        extractor = _get_text_extractor(mime_type)
        if not extractor:
            raise FileProcessingError(f"Tipo de archivo no soportado para análisis manual: {mime_type}")

        loop = asyncio.get_running_loop()
        extracted_text = await loop.run_in_executor(None, extractor, file_path)
        
        if not extracted_text:
            raise FileProcessingError("No se pudo extraer texto del archivo para el análisis manual.")
        
        cv_info, text_usage = await analysis.extract_info_from_text_with_openai(extracted_text, output_schema)
        if total_usage:
            total_usage += text_usage
        else:
            total_usage = text_usage

    if not cv_info or not total_usage:
        raise OpenAIError("Todos los métodos de análisis fallaron para extraer información o uso de tokens del CV.")
    
    return cv_info, total_usage

async def process_cv_and_callback(id_request: UUID, file_path: Path):
    """
    Tarea en segundo plano que orquesta el procesamiento de un CV.
    """
    status = "failed"
    error_message = None
    user_id = None
    endpoint_info = {}
    usage_data: Usage | None = None

    try:
        request_data = await _get_request_details(id_request)
        user_id = request_data.get("id_user")
        endpoint_info = request_data.get("endpoints", {}).get("info", {})
        
        if isinstance(endpoint_info, str):
            endpoint_info = json.loads(endpoint_info)
        
        # 1. Procesar el CV
        output_schema = endpoint_info.get("schema")
        if not output_schema:
            raise ValueError("El esquema de salida (output_schema) es obligatorio.")
        
        mode = endpoint_info.get("analysis_mode", "vision_first")
        cv_info, usage_data = await _run_analysis(mode, file_path, output_schema)
        
        # 2. Deducir créditos (operación atómica)
        if user_id:
            cost = usage_data.total_tokens
            success = await deduct_credits_atomic(user_id, cost)
            if not success:
                # This can happen if the user runs out of credits between the initial check and now.
                logger.warning(f"No se pudieron deducir {cost} créditos al usuario {user_id} para la petición {id_request} (créditos insuficientes).")
                raise InsufficientCreditsError(required=cost)

        status = "completed"
        payload_out = {"status": status, "data": cv_info, "usage": usage_data.model_dump()}
        logger.info(f"Procesamiento para la petición {id_request} completado con éxito.")

    except (DatabaseError, FileProcessingError, OpenAIError, ValueError, InsufficientCreditsError) as e:
        error_message = str(e)
        payload_out = {"status": status, "error": error_message, "data": None}
        logger.exception(f"Fallo en el procesamiento para la petición {id_request}: {e}")
    except Exception as e:
        error_message = str(e)
        payload_out = {"status": status, "error": error_message, "data": None}
        logger.critical(f"Error inesperado y no controlado en la petición {id_request}: {e}", exc_info=True)

    finally:
        # 4. Actualizar estado y registrar log
        try:
            credit_use = usage_data.total_tokens if usage_data and status == "completed" else 0
            await supabase_client.from_("requests").update({"status": status, "tokens_used": credit_use}).eq("id_request", str(id_request)).execute()
            
            log_entry = {
                "id_request": str(id_request),
                "payload_out": payload_out,
                "error": error_message,
                "credit_use": credit_use,
            }
            await supabase_client.from_("request_logs").insert(log_entry).execute()
        except Exception as e:
            logger.exception(f"Error crítico al actualizar el estado o registrar el log para la petición {id_request}: {e}")

        # 5. Enviar notificación al callback
        if callback_url := endpoint_info.get("callbackURL"):
            await _send_callback(callback_url, payload_out, id_request)
        
        # 6. Limpiar archivo temporal
        if file_path.exists():
            os.remove(file_path)

async def _send_callback(url: str, payload: dict, request_id: UUID):
    """Envia el resultado a la URL de callback con reintentos."""
    for i in range(3):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=30.0)
                response.raise_for_status()
                logger.info(f"Resultado enviado al callback {url} para la petición {request_id} (intento {i+1}).")
                return
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            logger.warning(f"Fallo al enviar callback para {request_id} (intento {i+1}/3): {e}")
            if i < 2:
                await asyncio.sleep(2.0 * (i + 1)) # Backoff lineal
    logger.error(f"Fallo final al enviar callback para {id_request} tras 3 intentos.")
