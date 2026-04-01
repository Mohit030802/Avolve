from fastapi import APIRouter, Depends
from typing import Any
from app.core.security import get_current_user

router = APIRouter()

@router.get("/test", response_model=dict)
def test_endpoint(current_user: dict = Depends(get_current_user)) -> Any:
    """
    Test endpoint requiring authentication.
    """
    return {
        "msg": "Success! You are authenticated.",
        "user": current_user
    }

@router.get("/public")
def public_endpoint():
    """
    Public endpoint.
    """
    return {"msg": "This is public."}
