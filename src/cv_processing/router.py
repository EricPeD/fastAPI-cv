from fastapi import APIRouter, BackgroundTasks, File, UploadFile, Depends, Form, HTTPException
from uuid import UUID, uuid4
from pathlib import Path
import shutil
import json
from typing import Optional, Dict, Any

from src.config import logger, get_supabase_client
from src.auth import verify_api_key
from src.models import AuthActor
from src.cv_processing.service import process_cv_and_callback, TEMP_CV_DIR
from src.exceptions import EndpointNotFoundError, ForbiddenAccessError, DatabaseError

router = APIRouter(
    tags=["File Processing"],
)

async def verify_endpoint_access(
    endpoint_id: UUID,
    actor: AuthActor = Depends(verify_api_key)
) -> dict:
    try:
        client = get_supabase_client()
        response = await (
            client.from_("endpoints")
            .select("id_user, info, secret_webhook")
            .eq("id", str(endpoint_id))
            .single()
            .execute()
        )
    except Exception as e:
        logger.exception(f"[ERROR] Fallo al consultar Supabase para endpoint '{endpoint_id}': {e}")
        raise EndpointNotFoundError(str(endpoint_id))

    if not response.data:
        raise EndpointNotFoundError(str(endpoint_id))

    endpoint_data = response.data
    if endpoint_data.get("id_user") != actor.user_id:
        raise ForbiddenAccessError("No tienes permiso para usar este endpoint.")

    return endpoint_data


@router.post("/{endpoint_id}", status_code=202, summary="Subir archivo para procesar")
async def upload_cv(
    endpoint_id: UUID,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    metadata: Optional[str] = Form(None),              # <-- 1. recibir como string del form
    endpoint_data: dict = Depends(verify_endpoint_access),
    actor: AuthActor = Depends(verify_api_key),
):
    try:
        # 2. Parsear metadata
        parsed_metadata: Optional[Dict[str, Any]] = None
        if metadata:
            try:
                parsed_metadata = json.loads(metadata)
                if not isinstance(parsed_metadata, dict):
                    raise HTTPException(status_code=400, detail="metadata debe ser un objeto JSON (dict)")
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="metadata debe ser un JSON válido")

        request_payload = {
            "id_user": actor.user_id,
            "id_key": str(actor.key_id),
            "endpoint_id": str(endpoint_id),
            "status": "processing",
        }

        request_response = await (
            get_supabase_client()
            .from_("requests")
            .insert(request_payload)
            .execute()
        )

        if not request_response.data:
            raise DatabaseError("No se pudo crear la request")

        id_request = request_response.data[0]["id_request"]

        filename = Path(file.filename).name.strip()
        unique_filename = f"{uuid4()}_{filename}"
        file_path = TEMP_CV_DIR / unique_filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 3. Pasar parsed_metadata al background task
        background_tasks.add_task(process_cv_and_callback, id_request, file_path, parsed_metadata)

        return {
            "message": "Archivo recibido. El procesamiento ha comenzado.",
            "request_id": id_request,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"[ERROR] Error en upload_cv para usuario {actor.user_id}: {e}")
        raise DatabaseError("Error al registrar la petición o guardar el archivo.")