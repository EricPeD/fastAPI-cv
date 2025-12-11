from src.config import supabase_client
import logging

async def get_user_credits(user_id: str) -> int:
    """
    Fetches the credit balance for a given user.

    Args:
        user_id: The ID of the user.

    Returns:
        The user's credit balance, or 0 if not found or an error occurs.
    """
    try:
        response = supabase_client.from_("users").select("credits").eq("id_user", user_id).execute()
        if response.data:
            return response.data[0].get("credits", 0)
        return 0
    except Exception as e:
        logging.error(f"Error fetching user credits for {user_id}: {e}")
        return 0

async def check_credits(user_id: str, amount_to_deduct: int) -> bool:
    """
    Checks if a user has enough credits.

    Args:
        user_id: The ID of the user.
        amount_to_deduct: The amount of credits to check for.

    Returns:
        True if the user has enough credits, False otherwise.
    """
    current_credits = await get_user_credits(user_id)
    return current_credits >= amount_to_deduct

async def deduct_credits(user_id: str, amount: int) -> bool:
    """
    Deducts credits from a user's account.

    Args:
        user_id: The ID of the user.
        amount: The number of credits to deduct.

    Returns:
        True if deduction was successful, False otherwise.
    """
    try:
        current_credits = await get_user_credits(user_id)
        if current_credits < amount:
            return False
        
        new_credits = current_credits - amount
        response = supabase_client.from_("users").update({"credits": new_credits}).eq("id_user", user_id).execute()
        
        if response.data:
            return True
        return False
    except Exception as e:
        logging.error(f"Error deducting credits for {user_id}: {e}")
        return False
