from src.config import logger, get_supabase_client
from src.exceptions import InsufficientCreditsError, DatabaseError

async def get_user_credits(user_id: str) -> int | None:
    """
    Fetches the credit balance for a given user.
    Returns None if the user is not found.
    """
    try:
        response = await get_supabase_client().from_("users").select("credits").eq("id_user", user_id).single().execute()
        if response.data:
            return response.data.get("credits")
        return None
    except Exception as e:
        logger.error(f"Error fetching user credits for {user_id}: {e}")
        raise DatabaseError("Error al obtener los créditos del usuario.")

async def deduct_credits_atomic(user_id: str, amount: int) -> bool:
    """
    Deducts credits from a user's account via application-layer logic.
    WARNING: This operation is NOT truly atomic and may be subject to race conditions
    under high concurrency from the same user.
    """
    logger.warning(f"Executing non-atomic credit deduction for user {user_id}. A race condition is possible.")
    
    supabase = get_supabase_client()
    try:
        # 1. Fetch current credits
        user_response = await supabase.from_("users").select("credits").eq("id_user", user_id).single().execute()
        
        if not user_response.data:
            logger.error(f"Deduction failed: User '{user_id}' not found.")
            return False
            
        current_credits = user_response.data.get("credits", 0)

        # 2. Check for sufficient credits
        if current_credits < amount:
            logger.warning(f"User {user_id} has insufficient credits ({current_credits}) to deduct {amount}.")
            raise InsufficientCreditsError(required=amount)

        # 3. Perform deduction and update
        new_credits = current_credits - amount
        update_response = await supabase.from_("users").update({"credits": new_credits}).eq("id_user", user_id).execute()

        # Post-update check could be added here if needed, but we'll trust the response for now
        if update_response.data:
            logger.info(f"Successfully deducted {amount} credits from user {user_id}. New balance: {new_credits}")
            return True
        
        logger.error(f"Failed to update credits for user {user_id} after deduction check. Response: {update_response.data}")
        return False

    except InsufficientCreditsError:
        # Re-raise the specific error to be caught by the calling service
        raise
    except Exception as e:
        logger.error(f"Error during credit deduction for user {user_id}: {e}")
        # Raising a general DatabaseError for other unexpected issues
        raise DatabaseError("Error al procesar el débito de créditos.")

