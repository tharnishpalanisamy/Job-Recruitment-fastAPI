from typing import Protocol

from app.models import User


class UserRepositoryProtocol(Protocol):
    async def create(self, user) -> User: ...

    async def get_by_email(self, email) -> User | None: ...

    async def get_by_id(self, id) -> User | None: ...
