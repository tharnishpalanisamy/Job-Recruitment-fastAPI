from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import ApplicationStatus
from app.models import Application, Job


class ApplicationRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, application: Application) -> Application:
        self.db.add(application)
        await self.db.flush()
        await self.db.refresh(application)
        return application

    async def get_all_by_job_seeker_id(self, id: int) -> list[Application]:
        query = select(Application).where(Application.job_seeker_id == id)
        result = await self.db.scalars(query)
        return result.all()

    async def get_existing_application(
        self, job_seeker_id: int, job_id: int
    ) -> Application | None:
        query = select(Application).where(
            Application.job_seeker_id == job_seeker_id, Application.job_id == job_id
        )

        return await self.db.scalar(query)

    async def get_by_application_id(self, id: int) -> Application | None:
        query = select(Application).where(Application.id == id)
        return await self.db.scalar(query)

    async def get_all(
        self, recruiter_id: int | None, job_id: int | None, limit: int, offset: int
    ) -> list[Application]:
        query = select(Application).join(Job, Application.job_id == Job.id)

        if recruiter_id is not None:
            query = query.where(Job.created_by == recruiter_id)

        if job_id is not None:
            query = query.where(Application.job_id == job_id)
        query = query.order_by(Application.applied_at.asc()).limit(limit).offset(offset)
        result = await self.db.scalars(query)
        return result.all()

    async def update_status(
        self, application: Application, status: ApplicationStatus
    ) -> Application:
        application.status = status
        await self.db.flush()
        await self.db.refresh(application)

        return application

    async def delete_by_id(self, id: int) -> None:
        query = delete(Application).where(Application.id == id)

        await self.db.execute(query)
        await self.db.flush()

    async def update_resume(
        self, application: Application, filename: str, file_path: str
    ) -> Application:
        application.resume_filename = filename
        application.resume_path = file_path

        await self.db.flush()
        await self.db.refresh(application)

        return application
