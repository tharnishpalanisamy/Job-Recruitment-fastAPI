from sqlalchemy import select

from app.models import User


class UserRepository:
    def __init__(self, db):
        self.db = db

    async def create(self, user) -> User:
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)

        return user

    async def get_by_email(self, email) -> User | None:
        query = select(User).where(User.email == email)
        user = await self.db.scalar(query)
        return user

    async def get_by_id(self, id) -> User | None: 
        query = select(User).where(User.id == id)
        user = await self.db.scalar(query)
        return user 