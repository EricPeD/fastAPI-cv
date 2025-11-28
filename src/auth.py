import hashlib
import hmac
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from src.models import AuthActor
from src.config import logger, supabase_client

api_key_header_scheme = APIKeyHeader(name="Authorization", auto_error=False)


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

    # Dividir la API Key en ID y hash
    try:
        api_key_id = provided_key.split(".")[0]
        api_key_hash = provided_key.split(".")[1]
    except IndexError:
        raise HTTPException(
            status_code=401, detail="Formato de API Key inválido. Debe ser 'id.hash'."
        )

    try:
        response = (
            supabase_client.from_("api_keys")
            .select("id_key, key_hash, id_user")
            .eq("id_key", api_key_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=401, detail="API Key inválida.")

        provided_key_hash = api_key_hash

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
