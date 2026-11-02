from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import JobSeeker


class JobSeekersRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, job_seeker: JobSeeker) -> JobSeeker:
        self.db.add(job_seeker)
        await self.db.flush()
        await self.db.refresh(job_seeker)

        return job_seeker

    async def get_all(self) -> list[JobSeeker]:
        pass

    async def get_by_user_id(self, user_id) -> JobSeeker:
        query = select(JobSeeker).where(JobSeeker.user_id == user_id)
        return await self.db.scalar(query)
