from typing import Protocol

from app.models import JobSeeker
from app.schemas import JobSeekerFilterParams


class JobSeekersRepositoryProtocol(Protocol):
    async def create(self, job_seeker: JobSeeker) -> JobSeeker: ...

    async def get_all(
        self, filters: JobSeekerFilterParams, limit: int, offset: int
    ) -> list[JobSeeker]: ...

    async def get_by_id(self, job_seeker_id: int) -> JobSeeker | None: ...

    async def get_by_user_id(self, user_id: int) -> JobSeeker | None: ...

    async def update_by_user_id(
        self, job_seeker: JobSeeker, fields: dict[str, object]
    ) -> JobSeeker: ...

    async def delete_by_user_id(self, user_id: int) -> None: ...
