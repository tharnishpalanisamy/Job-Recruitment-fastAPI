from typing import Protocol

from app.core import UserRole
from app.models import User


class UserRepositoryProtocol(Protocol):
    async def create(self, user: User) -> User: ...

    async def get_by_email(self, email: str) -> User | None: ...

    async def get_by_id(self, id: int) -> User | None: ...

    async def update_role(self, id: int, role: UserRole) -> User | None: ...
