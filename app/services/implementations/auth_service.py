from app.core import create_access_token, hash_password, verify_password
from app.exceptions import (
    EmailAlreadyExists,
    InvalidCredentialsException,
    InvalidRefreshTokenException,
)
from app.models import User
from app.repositories.protocols import (
    UserRepositoryProtocol,
)
from app.schemas import UserCreate
from app.services.protocols import EmailServiceProtocol, RefreshTokenServiceProtocol


class AuthService:
    def __init__(
        self,
        db,
        repository: UserRepositoryProtocol,
        refresh_token_service: RefreshTokenServiceProtocol,
        email_service: EmailServiceProtocol,
    ):
        self.db = db
        self.user_repository = repository
        self.refresh_token_service = refresh_token_service
        self.email_service = email_service

    async def authenticate_user(self, user_data: UserCreate) -> dict[str, str | User]:
        user = await self.user_repository.get_by_email(user_data.email)

        if not user:
            raise InvalidCredentialsException("Invalid username or password ")

        authenticated = verify_password(user_data.password, user.password_hash)

        if not authenticated:
            raise InvalidCredentialsException("Invalid username or password ")

        access_token = create_access_token(user.id, user.role)

        refresh_token = await self.refresh_token_service.issue_refresh_token(user.id)

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
        existing_user = await self.user_repository.get_by_email(user.email)

        if existing_user is not None:
            raise EmailAlreadyExists("Account Already exists please try to login")

        created_user = await self.user_repository.create(user)
        await self.db.commit()

        await self.email_service.send_welcome_email(
            recipient=created_user.email, username=created_user.username
        )
        return created_user

    async def refresh_tokens(self, token: str) -> dict[str, str]:
        (
            user_id,
            new_refresh_token,
        ) = await self.refresh_token_service.rotate_refresh_token(token)

        user = await self.user_repository.get_by_id(user_id)

        if user is None:
            raise InvalidRefreshTokenException(
                "This refresh token is no longer valid. Please sign in again."
            )

        access_token = create_access_token(user.id, user.role)

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }
