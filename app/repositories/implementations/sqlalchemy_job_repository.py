from datetime import datetime, time, timedelta, timezone

from sqlalchemy import select

from app.models import Job


class JobRepository:
    def __init__(self, db):
        self.db = db

    async def create(self, job) -> Job:
        self.db.add(job)
        await self.db.flush()
        await self.db.refresh(job)

        return job

    async def get_all(self, filters, limit, offset):
        query = select(Job)

        conditions = []
        if filters.title is not None:
            conditions.append(Job.title.ilike(f"%{filters.title}%"))
        if filters.requirements is not None:
            conditions.append(Job.requirements.ilike(f"%{filters.requirements}%"))

        if filters.qualification is not None:
            conditions.append(Job.qualification.ilike(f"%{filters.qualification}%"))

        if filters.experience_min is not None:
            conditions.append(Job.experience_min >= filters.experience_min)

        if filters.experience_max is not None:
            conditions.append(Job.experience_max <= filters.experience_max)

        if filters.salary_min is not None:
            conditions.append(Job.salary_min >= filters.salary_min)

        if filters.salary_max is not None:
            conditions.append(Job.salary_max <= filters.salary_max)

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

    async def get_by_id(self, id): ...

    async def delete_by_id(self, job_id): ...

    async def update_by_id(self, id, job_data): ...
