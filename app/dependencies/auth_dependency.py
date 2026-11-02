from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories.implementations import RefreshTokenRepository, UserRepository
from app.repositories.protocols import (
    RefreshTokenRepositoryProtocol,
    UserRepositoryProtocol,
)
from app.services.implementations import AuthService, RefreshTokenService
from app.services.protocols import AuthServiceProtocol, RefreshTokenServiceProtocol


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

#authentication dependencies
def get_auth_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserRepositoryProtocol:
    return UserRepository(db)


def get_auth_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    repository: Annotated[UserRepositoryProtocol, Depends(get_auth_repository)],
    refresh_token_service: Annotated[
        RefreshTokenService, Depends(get_refresh_token_service)
    ]
) -> AuthServiceProtocol:
    return AuthService(db, repository, refresh_token_service)
