from fastapi import APIRouter, HTTPException, BackgroundTasks, File, UploadFile, Depends
from uuid import UUID, uuid4
from pathlib import Path
import shutil
from postgrest.exceptions import APIError

from src.config import logger, supabase_client
from src.auth import verify_api_key
from src.models import AuthActor
from src.cv_processing.service import process_cv_and_callback, TEMP_CV_DIR

router = APIRouter(
    # prefix="/cv",
    tags=["FILE Processing"],
)

@router.post("/{endpoint_id}", status_code=202, summary="Subir achivo")
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
        try:
            endpoint_response = (
                supabase_client.from_("endpoints")
                .select("id_user, info")
                .eq("id", str(endpoint_id))
                .single()
                .execute()
            )
        except APIError as e:
            if (
                e.code == "PGRST116" and "0 rows" in e.details
            ):  # 'PGRST116' indicates "no rows found"
                logger.warning(
                    f"Endpoint con id '{endpoint_id}' no encontrado para el usuario {actor.user_id}."
                )
                raise HTTPException(
                    status_code=404,
                    detail=f"Endpoint con id '{endpoint_id}' no encontrado.",
                )
            # Re-raise other API errors
            raise

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
            supabase_client.from_("requests").insert(request_payload).execute()
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
