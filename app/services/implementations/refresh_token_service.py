import hashlib
import secrets
from datetime import UTC, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import setting
from app.exceptions import InvalidRefreshTokenException
from app.models import RefreshToken
from app.repositories.protocols import RefreshTokenRepositoryProtocol


class RefreshTokenService:
    def __init__(
        self, db: AsyncSession, repository: RefreshTokenRepositoryProtocol
    ) -> None:
        self.db = db
        self.repository = repository

    @staticmethod
    def generate_refresh_token() -> str:
        return secrets.token_urlsafe(64)

    @staticmethod
    def hash_refresh_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def _build_refresh_token(self, user_id: int) -> tuple[str, RefreshToken]:
        raw_token = self.generate_refresh_token()

        hashed_token = self.hash_refresh_token(raw_token)

        token_record = RefreshToken(
            user_id=user_id,
            token_hash=hashed_token,
            expires_at=datetime.now(UTC)
            + timedelta(days=setting.REFRESH_TOKEN_EXPIRE_DAYS),
        )

        return raw_token, token_record

    async def issue_refresh_token(self, user_id: int) -> str:

        token, refresh_token = self._build_refresh_token(user_id)

        try:
            await self.repository.create(refresh_token)
            await self.db.commit()

        except Exception:
            await self.db.rollback()
            raise

        return token

    async def rotate_refresh_token(self, raw_token: str) -> tuple[int, str]:
        token_hash = self.hash_refresh_token(raw_token)

        try:
            old_record = await self.repository.get_token_by_hash_for_update(token_hash)

            if old_record is None:
                raise InvalidRefreshTokenException("This refresh token is not valid.")

            now = datetime.now(UTC)

            if old_record.revoked_at is not None:
                await self.repository.revoke_all(
                    old_record.user_id,
                    now,
                )
                await self.db.commit()
                raise InvalidRefreshTokenException(
                    "This refresh token has already been used. Please sign in again."
                )

            expires_at = old_record.expires_at

            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=UTC)

            if expires_at <= now:
                old_record.revoked_at = now
                await self.db.commit()
                raise InvalidRefreshTokenException(
                    "This refresh token has expired. Please sign in again."
                )

            user_id = old_record.user_id

            new_raw_token, new_record = self._build_refresh_token(user_id)

            self.db.add(new_record)
            await self.db.flush()

            old_record.revoked_at = now
            old_record.replaced_by_id = new_record.id

            await self.db.flush()
            await self.db.commit()

            return user_id, new_raw_token

        except InvalidRefreshTokenException:
            raise
        except Exception:
            await self.db.rollback()
            raise

    async def revoke_refresh_token(self, raw_token: str) -> None:
        token_hash = self.hash_refresh_token(raw_token)

        try:
            token_record = await self.repository.get_token_by_hash_for_update(
                token_hash
            )

            if token_record is None:
                raise InvalidRefreshTokenException("This refresh token is not valid.")

            if token_record.revoked_at is None:
                await self.repository.revoke(token_record, datetime.now(UTC))
                await self.db.commit()
        except InvalidRefreshTokenException:
            raise
        except Exception:
            await self.db.rollback()
            raise
