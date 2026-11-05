import logging
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import UserRole
from app.exceptions import JobNotFoundException, NotAuthorizedException
from app.models import Application, Job, User
from app.repositories.protocols import JobRepositoryProtocol
from app.schemas import JobCreate, JobFilterParams, JobUpdate

logger = logging.getLogger(__name__)


class JobService:
    def __init__(self, db: AsyncSession, repository: JobRepositoryProtocol) -> None:
        self.db = db
        self.job_repository = repository

    async def create_job(self, user: User, job_data: JobCreate) -> Job:
        job = Job(**job_data.model_dump(), created_by=user.id)

        result = await self.job_repository.create(job)
        await self.db.commit()
        return result

    async def get_all_jobs(
        self, filters: JobFilterParams, limit: int, offset: int
    ) -> list[Job]:
        result = await self.job_repository.get_all(filters, limit, offset)

        return result

    async def get_job_by_id(self, job_id: int) -> Job:
        job = await self.job_repository.get_by_id(job_id)
        if job is None:
            raise JobNotFoundException(f"Job posting with id {job_id} not found!")
        return job

    async def update_job(self, user: User, job_id: int, job_data: JobUpdate) -> Job:
        existing_job = await self.job_repository.get_by_id(job_id)
        if existing_job is None:
            raise JobNotFoundException(f"Job with id {job_id} not found !")
        if user.role == UserRole.RECRUITER and user.id != existing_job.created_by:
            raise NotAuthorizedException("You are not allowed to edit this resouce")

        if existing_job is None:
            raise JobNotFoundException(f"Job posting with id {job_id} not found!")

        fields = job_data.model_dump(exclude_unset=True)

        result = await self.job_repository.update(existing_job, fields)
        await self.db.commit()

        return result

    async def delete_job_by_id(self, user: User, job_id: int) -> None:
        if user.role == UserRole.RECRUITER:
            job = await self.job_repository.get_by_id(job_id)

            if job is None:
                raise JobNotFoundException(f"Job with id {job_id} not found")
            if user.id != job.created_by:
                raise NotAuthorizedException(
                    "You are not authorized to delete this job posting"
                )
        existing_job = await self.job_repository.get_by_id(job_id)
        if existing_job is None:
            raise JobNotFoundException(f"Job posting with id {job_id} not found!")

        # Capture resume paths before the application's rows are removed by
        # the job foreign-key cascade.
        result = await self.db.scalars(
            select(Application.resume_path).where(Application.job_id == job_id)
        )
        resume_paths = result.all()

        await self.job_repository.delete_by_id(job_id)
        await self.db.commit()

        for resume_path in resume_paths:
            try:
                path = Path(resume_path)
                if path.exists():
                    path.unlink()
            except OSError:
                logger.exception("Failed to delete resume file: %s", resume_path)
