from fastapi import APIRouter, BackgroundTasks, File, UploadFile, Depends
from uuid import UUID, uuid4
from pathlib import Path
import shutil

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
    """
    Dependency that verifies if an endpoint exists and if the user has permission to use it.
    Returns the endpoint data if successful.
    """

    logger.info(f"[DEBUG] verify_endpoint_access called with endpoint_id={endpoint_id}")
    logger.info(f"[DEBUG] Actor recibido: {actor}")

    try:
        client = get_supabase_client()
        logger.info(f"[DEBUG] Supabase client creado: {client}")

        query = (
            client.from_("endpoints")
            .select("id_user, info, secret_webhook")
            .eq("id", str(endpoint_id))
            .single()
        )

        logger.info(f"[DEBUG] Query construida: {query}")

        response = await query.execute()

        logger.info(f"[DEBUG] Respuesta de Supabase: {response}")
        logger.info(f"[DEBUG] Response data: {getattr(response, 'data', None)}")

    except Exception as e:
        logger.exception(f"[ERROR] Fallo al consultar Supabase para endpoint '{endpoint_id}': {e}")
        raise EndpointNotFoundError(str(endpoint_id))

    if not response.data:
        logger.warning(f"[DEBUG] Endpoint no encontrado en DB: {endpoint_id}")
        raise EndpointNotFoundError(str(endpoint_id))

    endpoint_data = response.data

    logger.info(f"[DEBUG] Endpoint data obtenido: {endpoint_data}")
    logger.info(f"[DEBUG] Comparando users -> DB: {endpoint_data.get('id_user')} vs Actor: {actor.user_id}")

    if endpoint_data.get("id_user") != actor.user_id:
        logger.warning("[DEBUG] Usuario no autorizado para este endpoint")
        raise ForbiddenAccessError("No tienes permiso para usar este endpoint.")
    
    return endpoint_data


@router.post("/{endpoint_id}", status_code=202, summary="Subir archivo para procesar")
async def upload_cv(
    endpoint_id: UUID,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    endpoint_data: dict = Depends(verify_endpoint_access),
    actor: AuthActor = Depends(verify_api_key),
):
    """
    Acepta un archivo de CV para procesamiento asíncrono.
    """

    logger.info(f"[DEBUG] upload_cv iniciado para endpoint_id={endpoint_id}")
    logger.info(f"[DEBUG] Actor en endpoint principal: {actor}")

    try:
        # 1. Crear un registro de la petición en la base de datos
        request_payload = {
            "id_user": actor.user_id,
            "id_key": str(actor.key_id),
            "endpoint_id": str(endpoint_id),
            "status": "processing",
        }

        logger.info(f"[DEBUG] Payload para insertar request: {request_payload}")

        request_response = await (
            get_supabase_client()
            .from_("requests")
            .insert(request_payload)
            .execute()
        )

        logger.info(f"[DEBUG] Respuesta insert request: {request_response}")

        if not request_response.data:
            logger.error("[ERROR] No se devolvió data al insertar request")
            raise DatabaseError("No se pudo crear la request")

        id_request = request_response.data[0]["id_request"]

        logger.info(f"[DEBUG] id_request generado: {id_request}")

        # 2. Guardar el archivo en disco de forma segura
        filename = Path(file.filename).name.strip()
        unique_filename = f"{uuid4()}_{filename}"
        file_path = TEMP_CV_DIR / unique_filename

        logger.info(f"[DEBUG] Guardando archivo en: {file_path}")

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info("[DEBUG] Archivo guardado correctamente")

        # 3. Añadir la tarea de procesamiento al segundo plano
        background_tasks.add_task(process_cv_and_callback, id_request, file_path)

        logger.info("[DEBUG] Background task añadida correctamente")

        return {
            "message": "Archivo recibido. El procesamiento ha comenzado.",
            "request_id": id_request
        }

    except Exception as e:
        logger.exception(f"[ERROR] Error en upload_cv para usuario {actor.user_id}: {e}")
        raise DatabaseError("Error al registrar la petición o guardar el archivo.")