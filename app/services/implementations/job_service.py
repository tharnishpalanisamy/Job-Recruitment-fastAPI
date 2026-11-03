from app.models import Job


class JobService:
    def __init__(self, db, repository):
        self.db = db
        self.job_repository = repository

    async def create_job(self, user, job_data):
        job = Job(**job_data.model_dump(), created_by=user.id)

        result = await self.job_repository.create(job)
        await self.db.commit()
        return result

    async def get_all_jobs(self, filters, limit, offset): ...

    async def get_job_by_id(self, job_id): ...

    async def delete_job_by_id(self, job_id): ...

    async def update_job(self, job_data): ...
