from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories.implementations import JobRepository
from app.repositories.protocols import (
    JobRepositoryProtocol,
)
from app.services.implementations import JobService
from app.services.protocols import JobServiceProtocol


def get_job_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> JobRepositoryProtocol:
    return JobRepository(db)


def get_job_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    repository: Annotated[JobRepositoryProtocol, Depends(get_job_repository)],
) -> JobServiceProtocol:
    return JobService(db, repository)
