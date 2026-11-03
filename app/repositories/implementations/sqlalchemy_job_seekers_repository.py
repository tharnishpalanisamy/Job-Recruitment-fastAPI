from sqlalchemy import delete, select
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

    async def get_all(self, filters, limit, offset) -> list[JobSeeker]:
        query = select(JobSeeker)

        conditions = []
        if filters.qualification is not None:
            conditions.append(
                JobSeeker.qualification.ilike(f"%{filters.qualification}%")
            )

        if filters.specialization is not None:
            conditions.append(
                JobSeeker.specialization.ilike(f"%{filters.specialization}%")
            )

        if filters.designation is not None:
            conditions.append(
                JobSeeker.current_designation.ilike(f"%{filters.designation}%")
            )

        if filters.min_experience is not None:
            conditions.append(JobSeeker.experience_years >= filters.min_experience)

        if filters.max_experience is not None:
            conditions.append(JobSeeker.experience_years <= filters.max_experience)

        for condition in conditions:
            query = query.where(condition)

        query = query.order_by(JobSeeker.id.asc())
        query = query.limit(limit).offset(offset)

        result = await self.db.scalars(query)

        return result.all()

    async def get_by_id(self, job_seeker_id) -> JobSeeker:
        query = select(JobSeeker).where(JobSeeker.id == job_seeker_id)
        return await self.db.scalar(query)

    async def get_by_user_id(self, user_id) -> JobSeeker:
        query = select(JobSeeker).where(JobSeeker.user_id == user_id)
        return await self.db.scalar(query)

    async def update_by_user_id(self, job_seeker, fields) -> JobSeeker:

        for field, value in fields.items():
            setattr(job_seeker, field, value)

        await self.db.flush()
        await self.db.refresh(job_seeker)

        return job_seeker

    async def delete_by_user_id(self, user_id: int) -> None:
        query = delete(JobSeeker).where(JobSeeker.user_id == user_id)

        await self.db.execute(query)
        await self.db.flush()
