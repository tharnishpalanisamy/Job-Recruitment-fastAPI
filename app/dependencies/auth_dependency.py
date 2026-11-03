from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import UserRole
from app.core.config import setting
from app.database import get_db
from app.dependencies.email_dependency import get_email_service
from app.exceptions import NotAuthorizedException
from app.models import User
from app.repositories.implementations import RefreshTokenRepository, UserRepository
from app.repositories.protocols import (
    RefreshTokenRepositoryProtocol,
    UserRepositoryProtocol,
)
from app.services.implementations import AuthService, RefreshTokenService
from app.services.protocols import (
    AuthServiceProtocol,
    EmailServiceProtocol,
    RefreshTokenServiceProtocol,
)


# Refresh token dependencies
def get_refresh_token_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> RefreshTokenRepositoryProtocol:
    return RefreshTokenRepository(db)


def get_refresh_token_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    repository: Annotated[
        RefreshTokenRepositoryProtocol, Depends(get_refresh_token_repository)
    ],
) -> RefreshTokenServiceProtocol:
    return RefreshTokenService(db, repository)


# authentication dependencies
def get_auth_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserRepositoryProtocol:
    return UserRepository(db)


def get_auth_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    repository: Annotated[UserRepositoryProtocol, Depends(get_auth_repository)],
    refresh_token_service: Annotated[
        RefreshTokenService, Depends(get_refresh_token_service)
    ],
    email_service: Annotated[EmailServiceProtocol, Depends(get_email_service)],
) -> AuthServiceProtocol:
    return AuthService(db, repository, refresh_token_service , email_service)


bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token, setting.JWT_SECRET_KEY, algorithms=[setting.JWT_ALGORITHM]
        )

        user_id = int(payload.get("sub"))

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    statement = select(User).where(User.id == user_id)

    user = await db.scalar(statement)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def require_roles(*allowed_roles: UserRole):

    def role_checker(
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        if current_user.role not in allowed_roles:
            raise NotAuthorizedException("You are not allowed to access this resource")

        return current_user

    return role_checker
