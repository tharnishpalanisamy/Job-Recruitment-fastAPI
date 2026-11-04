from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories.implementations import HealthRepository
from app.repositories.protocols import HealthRepositoryProtocol
from app.services.implementations import HealthService
from app.services.protocols import HealthServiceProtocol


def get_health_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> HealthRepositoryProtocol:
    return HealthRepository(db)


def get_health_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    repository: Annotated[HealthRepositoryProtocol, Depends(get_health_repository)],
) -> HealthServiceProtocol:
    return HealthService(db, repository)
