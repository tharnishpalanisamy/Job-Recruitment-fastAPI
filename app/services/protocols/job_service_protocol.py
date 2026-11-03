from typing import Protocol

from app.models import Job, User
from app.schemas import JobCreate, JobFilterParams, JobUpdate


class JobServiceProtocol(Protocol):
    async def create_job(self, user: User, job_data: JobCreate) -> Job: ...

    async def get_all_jobs(
        self, filters: JobFilterParams, limit: int, offset: int
    ) -> list[Job]: ...

    async def get_job_by_id(self, job_id: int) -> Job: ...

    async def delete_job_by_id(self, user: User, job_id: int) -> None: ...

    async def update_job(self, job_id: int, job_data: JobUpdate) -> Job: ...
