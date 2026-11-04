from typing import Protocol


class HealthRepositoryProtocol(Protocol):
    async def check_db(self) -> bool: ...
