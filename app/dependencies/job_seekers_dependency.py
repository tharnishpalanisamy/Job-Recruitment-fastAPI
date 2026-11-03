from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies.email_dependency import get_email_service
from app.repositories.implementations import JobSeekersRepository, UserRepository
from app.repositories.protocols import (
    JobSeekersRepositoryProtocol,
    UserRepositoryProtocol,
)
from app.services.implementations import JobSeekerService
from app.services.protocols import EmailServiceProtocol, JobSeekerServiceProtocol


def get_job_seeker_repository(db: Annotated[AsyncSession, Depends(get_db)]):
    return JobSeekersRepository(db)


def get_user_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserRepositoryProtocol:
    return UserRepository(db)


def get_job_seeker_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    repository: Annotated[
        JobSeekersRepositoryProtocol, Depends(get_job_seeker_repository)
    ],
    user_repository: Annotated[UserRepositoryProtocol, Depends(get_user_repository)],
    email_service: Annotated[EmailServiceProtocol, Depends(get_email_service)],
) -> JobSeekerServiceProtocol:
    return JobSeekerService(db, repository, user_repository, email_service)
