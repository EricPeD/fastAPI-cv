from fastapi import APIRouter, Depends
from src.auth import verify_api_key
from src.users.service import get_user_credits
from src.models import AuthActor
from src.exceptions import EndpointNotFoundError

router = APIRouter()

@router.get("/me/credits", summary="Get User Credits", tags=["User"])
async def get_my_credits(actor: AuthActor = Depends(verify_api_key)):
    """
    Retrieves the current credit balance for the authenticated user.
    """
    credits = await get_user_credits(actor.user_id)
    if credits is None:
        # This case should ideally not happen if a user is created with default credits.
        raise EndpointNotFoundError(f"Usuario con id '{actor.user_id}' no encontrado.")
    
    return {"user_id": actor.user_id, "credits": credits}

