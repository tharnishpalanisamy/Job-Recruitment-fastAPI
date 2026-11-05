from datetime import datetime, time, timedelta, timezone

from sqlalchemy import delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import JobStatus
from app.models import Job
from app.schemas import JobFilterParams


class JobRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, job: Job) -> Job:
        self.db.add(job)
        await self.db.flush()
        await self.db.refresh(job)

        return job

    async def get_all(
        self, filters: JobFilterParams, limit: int, offset: int
    ) -> list[Job]:
        query = select(Job)

        conditions = []
        if filters.title is not None:
            conditions.append(Job.title.ilike(f"%{filters.title}%"))
        if filters.requirements is not None:
            conditions.append(Job.requirements.ilike(f"%{filters.requirements}%"))

        if filters.qualification is not None:
            conditions.append(Job.qualification.ilike(f"%{filters.qualification}%"))

        if filters.experience_min is not None:
            # The requested range and posting range must overlap. A missing
            # posting maximum represents no upper limit.
            conditions.append(
                or_(
                    Job.experience_max.is_(None),
                    Job.experience_max >= filters.experience_min,
                )
            )

        if filters.experience_max is not None:
            conditions.append(Job.experience_min <= filters.experience_max)

        if filters.salary_min is not None:
            conditions.append(
                or_(Job.salary_max.is_(None), Job.salary_max >= filters.salary_min)
            )

        if filters.salary_max is not None:
            conditions.append(
                or_(Job.salary_min.is_(None), Job.salary_min <= filters.salary_max)
            )

        if filters.employment_type is not None:
            conditions.append(Job.employment_type == filters.employment_type)

        if filters.location is not None:
            conditions.append(Job.location.ilike(f"%{filters.location}%"))

        if filters.created_at is not None:
            start_datetime = datetime.combine(
                filters.created_at,
                time.min,
                tzinfo=timezone(timedelta(hours=5, minutes=30)),
            )

            conditions.append(Job.created_at >= start_datetime)
        if conditions:
            query = query.where(*conditions)

        query = query.order_by(Job.id.asc()).limit(limit).offset(offset)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, id: int) -> Job | None:
        query = select(Job).where(Job.id == id)
        return await self.db.scalar(query)

    async def get_by_id_for_update(self, job_id: int) -> Job | None:
        query = (
            select(Job)
            .where(Job.id == job_id)
            .with_for_update()
            .execution_options(populate_existing=True)
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def delete_by_id(self, job_id: int) -> None:
        query = delete(Job).where(Job.id == job_id)
        await self.db.execute(query)
        await self.db.flush()

    async def update(self, job: Job, fields: dict[str, object]) -> Job:
        for field, value in fields.items():
            setattr(job, field, value)
        await self.db.flush()
        await self.db.refresh(job)
        return job

    async def reduce_vacancy(self, job: Job) -> None:
        job.vacancies = job.vacancies - 1
        if job.vacancies == 0:
            job.status = JobStatus.CLOSED

        await self.db.flush()
