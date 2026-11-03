from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies.job_dependency import get_job_repository
from app.dependencies.job_seekers_dependency import get_job_seeker_repository
from app.repositories.implementations import ApplicationRepository
from app.repositories.protocols import (
    ApplicationRepositoryProtocol,
    JobRepositoryProtocol,
    JobSeekersRepositoryProtocol,
)
from app.services.implementations import ApplicationService
from app.services.protocols import ApplicationServiceProtocol


def get_application_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApplicationRepositoryProtocol:
    return ApplicationRepository(db)


def get_application_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    repository: Annotated[
        ApplicationRepositoryProtocol, Depends(get_application_repository)
    ],
    job_seeker_repository: Annotated[
        JobSeekersRepositoryProtocol,
        Depends(get_job_seeker_repository),
    ],
    job_repository: Annotated[JobRepositoryProtocol, Depends(get_job_repository)],
) -> ApplicationServiceProtocol:
    return ApplicationService(db, repository, job_seeker_repository , job_repository)
