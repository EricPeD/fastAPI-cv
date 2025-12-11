from fastapi import APIRouter, Depends, HTTPException
from src.auth import verify_api_key
from src.users.service import get_user_credits
from src.models import AuthActor

router = APIRouter()

@router.get("/me/credits", summary="Get User Credits", tags=["User"])
async def get_my_credits(actor: AuthActor = Depends(verify_api_key)):
    """
    Retrieves the current credit balance for the authenticated user.
    """
    credits = await get_user_credits(actor.user_id)
    if credits is None:
        raise HTTPException(status_code=404, detail="User credits not found.")
    
    return {"user_id": actor.user_id, "credits": credits}
