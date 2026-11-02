from app.core import create_access_token, hash_password, verify_password
from app.exceptions import InvalidCredentialsException
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
        user = await self.user_repository.get_by_email(user_data.email)

        if not user:
            raise InvalidCredentialsException("Invalid username or password ")

        authenticated = verify_password(user_data.password, user.password_hash)

        if not authenticated:
            raise InvalidCredentialsException("Invalid username or password ")

        access_token = create_access_token(user.id, user.role)

        refresh_token = await self.refresh_token_repository.issue_refresh_token(user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user,
        }

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
