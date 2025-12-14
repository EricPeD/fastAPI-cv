import hashlib
import hmac
from fastapi import Security
from fastapi.security import APIKeyHeader
from src.models import AuthActor
from src.config import logger, supabase_client
from src.exceptions import InvalidAPIKeyError, DatabaseError

api_key_header_scheme = APIKeyHeader(name="Authorization", auto_error=False)

async def verify_api_key(
    api_key_header: str = Security(api_key_header_scheme),
) -> AuthActor:
    """
    Verifica la API Key proporcionada por el usuario.
    La clave es un UUID completo. Su hash se compara con el almacenado en la BBDD.
    """
    if not api_key_header or not api_key_header.startswith("Bearer "):
        raise InvalidAPIKeyError("No se proporcionó una API Key válida en el formato 'Bearer <key>'.")

    provided_key = api_key_header.split(" ")[1]

    if len(provided_key) < 8:
        raise InvalidAPIKeyError("API Key con formato inválido.")

    prefix = provided_key[:8]

    try:
        # 1. Buscar claves candidatas usando el prefijo
        response = await (
            supabase_client.from_("api_keys")
            .select("id_key, key_hash, id_user")
            .eq("pre", prefix)
            .execute()
        )

        if not response.data:
            raise InvalidAPIKeyError()

        # 2. Hashear la clave proporcionada
        provided_key_hash = hashlib.sha256(provided_key.encode()).hexdigest()

        # 3. Comparar hashes
        for key_data in response.data:
            stored_hash = key_data.get("key_hash")
            if stored_hash and hmac.compare_digest(provided_key_hash, stored_hash):
                user_id = key_data.get("id_user")
                key_id = key_data.get("id_key")
                if user_id and key_id:
                    return AuthActor(user_id=user_id, key_id=key_id)

        raise InvalidAPIKeyError()

    except Exception as e:
        logger.exception(f"Error durante la verificación de la API Key: {e}")
        raise DatabaseError("Error interno del servidor al validar la API Key.")

