from typing import Protocol

from app.schemas import UserCreate


class AuthServiceProtocol(Protocol):
    async def authenticate_user(self , user_data: UserCreate): ...

    async def create_user(self , user_data: UserCreate): ...
