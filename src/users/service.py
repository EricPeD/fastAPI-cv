from src.config import logger, supabase_client
from src.exceptions import InsufficientCreditsError, DatabaseError

async def get_user_credits(user_id: str) -> int | None:
    """
    Fetches the credit balance for a given user.
    Returns None if the user is not found.
    """
    try:
        response = await supabase_client.from_("users").select("credits").eq("id_user", user_id).single().execute()
        if response.data:
            return response.data.get("credits")
        return None
    except Exception as e:
        logger.error(f"Error fetching user credits for {user_id}: {e}")
        raise DatabaseError("Error al obtener los créditos del usuario.")

async def deduct_credits_atomic(user_id: str, amount: int) -> bool:
    """
    Deducts credits from a user's account atomically using an RPC call.
    Assumes a `deduct_user_credits` function exists in the database.
    """
    try:
        # Assumes a DB function: `deduct_user_credits(p_user_id TEXT, p_amount INT)`
        # that returns `true` on success and `false` on failure (e.g., insufficient funds).
        response = await supabase_client.rpc(
            'deduct_user_credits',
            {'p_user_id': user_id, 'p_amount': amount}
        ).execute()
        
        if response.data:
            return True
        return False
    except Exception as e:
        logger.error(f"Error atómico al deducir créditos para {user_id}: {e}")
        raise DatabaseError("Error al procesar el débito de créditos.")

