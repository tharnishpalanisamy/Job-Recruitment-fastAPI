from sqlalchemy import delete, select

from app.models import Application, Job


class ApplicationRepository:
    def __init__(self, db):
        self.db = db

    async def create(self, application) -> Application:
        self.db.add(application)
        await self.db.flush()
        await self.db.refresh(application)
        return application

    async def get_all_by_job_seeker_id(self, id):
        query = select(Application).where(Application.job_seeker_id == id)
        result = await self.db.scalars(query)
        return result.all()

    async def get_existing_application(
        self, job_seeker_id, job_id
    ) -> Application | None:
        query = select(Application).where(
            Application.job_seeker_id == job_seeker_id, Application.job_id == job_id
        )

        return await self.db.scalar(query)

    async def get_by_application_id(self, id) -> Application | None:
        query = select(Application).where(Application.id == id)
        return await self.db.scalar(query)

    async def get_all(self, recruiter_id, job_id, limit, offset):
        query = select(Application).join(Job, Application.job_id == Job.id)

        if recruiter_id is not None:
            query = query.where(Job.created_by == recruiter_id)

        if job_id is not None:
            query = query.where(Application.job_id == job_id)
        query = query.order_by(Application.applied_at.asc()).limit(limit).offset(offset)
        result = await self.db.scalars(query)
        return result.all()


    async def update_status(self, id, status): ...

    async def delete_by_id(self, id):
        query = delete(Application).where(Application.id == id)

        result = await self.db.execute(query)
        await self.db.flush()
        return result
