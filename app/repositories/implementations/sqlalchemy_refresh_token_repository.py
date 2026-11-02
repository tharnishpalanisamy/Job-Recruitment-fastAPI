from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import RefreshToken


class RefreshTokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, token: RefreshToken) -> RefreshToken:
        self.db.add(token)
        await self.db.flush()
        await self.db.refresh(token)
        return token

    async def get_token_by_hash(self, token_hash: str) -> RefreshToken | None:
        query = select(RefreshToken).where(RefreshToken.token_hash == token_hash)

        result = await self.db.execute(query)
        token = result.scalar_one_or_none()

        return token

    async def get_token_by_hash_for_update(
        self, token_hash: str
    ) -> RefreshToken | None:
        query = (
            select(RefreshToken)
            .where(RefreshToken.token_hash == token_hash)
            .with_for_update()
            .execution_options(populate_existing=True)
        )

        result = await self.db.execute(query)
        token = result.scalar_one_or_none()

        return token

    async def revoke(self, token: RefreshToken, revoked_at: datetime) -> RefreshToken:
        token.revoked_at = revoked_at
        await self.db.flush()
        await self.db.refresh(token)

        return token

    async def revoke_all(self, user_id: int, revoked_at: datetime) -> None:
        query = (
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id, RefreshToken.revoked_at.is_(None))
            .values(revoked_at=revoked_at)
        )

        await self.db.execute(query)
        await self.db.flush()
