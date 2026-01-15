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

# -------------------------------
# Dependencia para verificar endpoint y permisos
# -------------------------------
async def verify_endpoint_access(endpoint_id: UUID, actor: AuthActor = Depends(verify_api_key)) -> dict:
    try:
        response = await (
            get_supabase_client().from_("endpoints")
            .select("id_user, info, secret_webhook")
            .eq("id", str(endpoint_id))
            .single()
            .execute()
        )
    except Exception as e:
        logger.warning(f"Error al buscar endpoint '{endpoint_id}': {e}")
        raise EndpointNotFoundError(str(endpoint_id))

    if not response.data:
        raise EndpointNotFoundError(str(endpoint_id))

    endpoint_data = response.data
    if endpoint_data.get("id_user") != actor.user_id:
        raise ForbiddenAccessError("No tienes permiso para usar este endpoint.")
    
    return endpoint_data

# -------------------------------
# Endpoint para subir CV
# -------------------------------
@router.post("/{endpoint_id}", status_code=202, summary="Subir archivo para procesar")
async def upload_cv(
    endpoint_id: UUID,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    metadata: Optional[str] = Form(None),  # metadata opcional
    endpoint_data: dict = Depends(verify_endpoint_access),
    actor: AuthActor = Depends(verify_api_key),
):
    """
    Acepta un archivo de CV para procesamiento asíncrono con metadata opcional.
    """
    try:
        # -------------------------------
        # Parsear metadata JSON si existe
        # -------------------------------
        parsed_metadata: Optional[Dict[str, Any]] = None
        if metadata:
            try:
                parsed_metadata = json.loads(metadata)
            except json.JSONDecodeError:
                raise HTTPException(
                    status_code=400,
                    detail="metadata debe ser un JSON válido"
                )

        # -------------------------------
        # Crear registro en la DB
        # -------------------------------
        request_payload = {
            "id_user": actor.user_id,
            "id_key": str(actor.key_id),
            "endpoint_id": str(endpoint_id),
            "status": "processing",
        }

        request_response = await get_supabase_client().from_("requests").insert(request_payload).execute()
        if not request_response.data or len(request_response.data) == 0:
            raise DatabaseError("No se pudo crear el registro en la base de datos")

        id_request = request_response.data[0]["id_request"]

        # -------------------------------
        # Guardar archivo en disco
        # -------------------------------
        filename = Path(file.filename).name.strip()
        unique_filename = f"{uuid4()}_{filename}"
        file_path = TEMP_CV_DIR / unique_filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # -------------------------------
        # Agregar tarea de procesamiento en background
        # -------------------------------
        background_tasks.add_task(
            process_cv_and_callback,
            id_request,
            file_path,  # dict para procesar si se necesita
        )

        return {
            "message": "Archivo recibido. El procesamiento ha comenzado.",
            "request_id": id_request,
        }

    except Exception as e:
        logger.exception(f"Error en la subida de archivo para el usuario {actor.user_id}: {e}")
        raise DatabaseError("Error al registrar la petición o guardar el archivo.")
