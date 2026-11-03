from typing import Protocol

from app.models import User
from app.schemas import UserCreate


class AuthServiceProtocol(Protocol):
    async def authenticate_user(
        self, user_data: UserCreate
    ) -> dict[str, str | User]: ...

    async def create_user(self, user_data: UserCreate) -> User: ...

    async def refresh_tokens(self, token: str) -> dict[str, str]: ...
