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
    Verifica la API Key proporcionada por el usuario.
    La clave es un UUID completo. Su hash se compara con el almacenado en la BBDD.
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

    try:
        # 1. Buscar claves candidatas usando el prefijo para optimizar la búsqueda
        response = (
            supabase_client.from_("api_keys")
            .select("id_key, key_hash, id_user")
            .eq("pre", prefix)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=401, detail="API Key inválida.")

        # 2. Hashear la clave completa proporcionada por el usuario
        provided_key_hash = hashlib.sha256(provided_key.encode()).hexdigest()

        # 3. Comparar el hash calculado con los hashes de los candidatos de la BBDD
        for key_data in response.data:
            stored_hash = key_data.get("key_hash")
            
            # Comparación segura para prevenir ataques de temporización
            if stored_hash and hmac.compare_digest(provided_key_hash, stored_hash):
                user_id = key_data.get("id_user")
                key_id = key_data.get("id_key")
                if user_id and key_id:
                    # Éxito: la clave es válida
                    return AuthActor(user_id=user_id, key_id=key_id)

        # Si el bucle termina y no hay coincidencia, la clave es inválida
        raise HTTPException(status_code=401, detail="API Key inválida.")

    except HTTPException:
        # Re-lanzar las excepciones HTTP que ya hemos definido
        raise
    except Exception as e:
        # Capturar cualquier otro error inesperado (ej. fallo de conexión con BBDD)
        logger.exception(f"Error durante la verificación de la API Key: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al validar la API Key.",
        )
