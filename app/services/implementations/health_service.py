class HealthService:
    def __init__(self, db, repository):
        self.db = db
        self.health_repository = repository

    async def check_readiness(self):
        await self.health_repository.check_database()

        return {
            "status": "healthy",
            "message": "Application is ready",
            "database": "connected",
        }
