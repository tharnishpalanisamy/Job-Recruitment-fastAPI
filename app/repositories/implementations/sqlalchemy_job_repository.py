from app.models import Job


class JobRepository:
    def __init__(self, db):
        self.db = db

    async def create(self, job) -> Job:
        self.db.add(job)
        await self.db.flush()
        await self.db.refresh(job)

        return job

    async def get_all(self, filters, limit, offset): ...

    async def get_by_id(self, id): ...

    async def delete_by_id(self, job_id): ...

    async def update_by_id(self, id, job_data): ...
