from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies import get_auth_service
from app.schemas import (
    LoginResponse,
    RefreshTokenRequest,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.protocols import AuthServiceProtocol

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/login",
    summary="Login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse,
)
async def login_user(
    login_data: UserLogin,
    service: Annotated[AuthServiceProtocol, Depends(get_auth_service)],
):
    return await service.authenticate_user(login_data)


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


@router.post("/refresh")
async def refresh_token(
    payload: RefreshTokenRequest,
    service: Annotated[AuthServiceProtocol, Depends(get_auth_service)],
):
    return await service.refresh_tokens(payload.refresh_token)
