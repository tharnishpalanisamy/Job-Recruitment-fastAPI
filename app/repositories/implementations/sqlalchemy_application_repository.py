from sqlalchemy import select , delete

from app.models import Application


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

    async def get_existing_application(self , job_seeker_id , job_id) -> Application | None  :
        query = select(Application).where(
            Application.job_seeker_id == job_seeker_id , 
            Application.job_id == job_id 
        )

        return await self.db.scalar(query) 

    async def get_by_application_id(self, id ) -> Application | None  :
        query = select(Application).where(
            Application.id == id 
        )
        return await self.db.scalar(query) 
    
    async def get_all(Self, filters, limit, offset): ...

    async def get_all_by_recruiter(self, filters, limit, offset, recruiter): ...

    async def update_status(self, id, status): ...

    async def delete_by_id(self, id): 
        query = delete(
            Application
        ).where(
            Application.id == id 
        )

        result = await self.db.execute(query) 
        await self.db.flush() 
        return result 
