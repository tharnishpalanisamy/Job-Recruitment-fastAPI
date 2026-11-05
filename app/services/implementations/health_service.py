from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.protocols import HealthRepositoryProtocol


class HealthService:
    def __init__(self, db: AsyncSession, repository: HealthRepositoryProtocol) -> None:
        self.db = db
        self.health_repository = repository

    async def check_readiness(self) -> dict[str, str]:
        await self.health_repository.check_database()

        return {
            "status": "healthy",
            "message": "Application is ready",
            "database": "connected",
        }
