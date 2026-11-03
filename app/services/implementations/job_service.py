from app.core import UserRole
from app.exceptions import JobNotFoundException, NotAuthorizedException
from app.models import Job, User
from app.schemas import JobCreate, JobFilterParams, JobUpdate


class JobService:
    def __init__(self, db, repository):
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

    async def update_job(self, job_id: int, job_data: JobUpdate) -> Job:
        existing_job = await self.job_repository.get_by_id(job_id)

        if existing_job is None:
            raise JobNotFoundException(f"Job posting with id {job_id} not found!")

        fields = job_data.model_dump(exclude_unset=True)

        result = await self.job_repository.update(existing_job, fields)
        await self.db.commit()

        return result

    async def delete_job_by_id(self, user: User, job_id: int) -> None:
        if user.role == UserRole.RECRUITER:
            job = await self.job_repository.get_by_id(job_id)

            if user.id != job.created_by:
                raise NotAuthorizedException(
                    "You are not authorized to delete this job posting"
                )
        existing_job = await self.job_repository.get_by_id(job_id)
        if existing_job is None:
            raise JobNotFoundException(f"Job posting with id {job_id} not found!")
        await self.job_repository.delete_by_id(job_id)
        await self.db.commit()
