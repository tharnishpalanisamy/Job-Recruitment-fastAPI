from app.core import hash_password
from app.models import User
from app.repositories.protocols import (
    RefreshTokenRepositoryProtocol,
    UserRepositoryProtocol,
)
from app.schemas import UserCreate


class AuthService:
    def __init__(
        self,
        db,
        repository: UserRepositoryProtocol,
        refresh_token_repository: RefreshTokenRepositoryProtocol,
    ):
        self.db = db
        self.user_repository = repository
        self.refresh_token_repository = refresh_token_repository

    async def authenticate_user(self, user_data: UserCreate):
        pass

    async def create_user(self, user_data: UserCreate) -> User:
        password_hash = hash_password(user_data.password)

        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=password_hash,
        )

        created_user = await self.user_repository.create(user)
        await self.db.commit()

        return created_user
