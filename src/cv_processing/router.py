from fastapi import APIRouter, BackgroundTasks, File, UploadFile, Depends
from uuid import UUID, uuid4
from pathlib import Path
import shutil

from src.config import logger, supabase_client
from src.auth import verify_api_key
from src.models import AuthActor
from src.cv_processing.service import process_cv_and_callback, TEMP_CV_DIR
from src.exceptions import EndpointNotFoundError, ForbiddenAccessError, DatabaseError

router = APIRouter(
    tags=["File Processing"],
)

async def verify_endpoint_access(endpoint_id: UUID, actor: AuthActor = Depends(verify_api_key)) -> dict:
    """
    Dependency that verifies if an endpoint exists and if the user has permission to use it.
    Returns the endpoint data if successful.
    """
    try:
        response = await (
            supabase_client.from_("endpoints")
            .select("id_user, info, secret_webhook")
            .eq("id", str(endpoint_id))
            .single()
            .execute()
        )
    except Exception as e:
        # Catches potential Postgrest errors (e.g., no rows found)
        logger.warning(f"Error al buscar endpoint '{endpoint_id}': {e}")
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
    endpoint_data: dict = Depends(verify_endpoint_access),
    actor: AuthActor = Depends(verify_api_key), # We still need the actor here for logging and request creation
):
    """
    Acepta un archivo de CV para procesamiento asíncrono.
    """
    try:
        # 1. Crear un registro de la petición en la base de datos
        request_payload = {
            "id_user": actor.user_id,
            "id_key": str(actor.key_id),
            "endpoint_id": str(endpoint_id),
            "status": "processing",
        }
        request_response = await supabase_client.from_("requests").insert(request_payload).execute()
        id_request = request_response.data[0]["id_request"]

        # 2. Guardar el archivo en disco de forma segura
        filename = Path(file.filename).name.strip()
        unique_filename = f"{uuid4()}_{filename}"
        file_path = TEMP_CV_DIR / unique_filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 3. Añadir la tarea de procesamiento al segundo plano
        background_tasks.add_task(process_cv_and_callback, id_request, file_path)

        return {"message": "Archivo recibido. El procesamiento ha comenzado.", "request_id": id_request}

    except Exception as e:
        logger.exception(f"Error en la subida de archivo para el usuario {actor.user_id}: {e}")
        raise DatabaseError("Error al registrar la petición o guardar el archivo.")

