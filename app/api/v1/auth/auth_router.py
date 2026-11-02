from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies import get_auth_service
from app.schemas import UserCreate, UserResponse
from app.services.protocols import AuthServiceProtocol

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def login_user():
    pass


@router.post(
    "/signup",
    summary="Create Account",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def signup_user(
    user_data: UserCreate,
    service: Annotated[AuthServiceProtocol, Depends(get_auth_service)],
):
    return await service.create_user(user_data)
