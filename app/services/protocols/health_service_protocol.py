from typing import Protocol


class HealthServiceProtocol(Protocol):
    async def check_readiness(self) -> dict[str, str]: ...
