from app.models import Application


class ApplicationRepository:
    def __init__(self, db):
        self.db = db

    async def create(self, application) -> Application:
        self.db.add(application)
        await self.db.flush()
        await self.db.refresh(application)
        return application

    async def get_all(Self, filters, limit, offset): ...

    async def get_all_by_recruiter(self, filters, limit, offset, recruiter): ...

    async def update_status(self, id, status): ...

    async def delete_by_id(self, id): ...
