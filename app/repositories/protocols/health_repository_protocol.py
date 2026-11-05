from typing import Protocol


class HealthRepositoryProtocol(Protocol):
    async def check_database(self) -> bool: ...
