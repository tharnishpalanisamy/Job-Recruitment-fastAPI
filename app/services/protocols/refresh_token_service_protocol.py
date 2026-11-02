from typing import Protocol


class RefreshTokenServiceProtocol(Protocol):
    async def issue_refresh_token(self, user_id: int) -> str: ...

    async def rotate_refresh_token(self, raw_token: str) -> tuple[int, str]: ...
