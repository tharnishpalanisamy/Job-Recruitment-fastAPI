from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import UserRole
from app.models import User


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)

        return user

    async def get_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        user = await self.db.scalar(query)
        return user

    async def get_by_id(self, id: int) -> User | None:
        query = select(User).where(User.id == id)
        user = await self.db.scalar(query)
        return user

    async def update_role(self, id: int, role: UserRole) -> User | None:
        query = update(User).where(User.id == id).values(role=role).returning(User)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
