from typing import Protocol

from app.models import JobSeeker, User
from app.schemas import JobSeekerCreate, JobSeekerFilterParams, JobSeekerUpdate


class JobSeekerServiceProtocol(Protocol):
    async def create_job_seeker(
        self, user: User, job_seeker_data: JobSeekerCreate
    ) -> JobSeeker: ...

    async def get_all_job_seekers(
        self, filters: JobSeekerFilterParams, limit: int, offset: int
    ) -> list[JobSeeker]: ...

    async def get_job_seeker_by_id(self, job_seeker_id: int) -> JobSeeker: ...

    async def get_current_job_seeker(self, user: User) -> JobSeeker: ...

    async def update_current_job_seeker(
        self, user: User, job_seeker_data: JobSeekerUpdate
    ) -> JobSeeker: ...

    async def delete_current_job_seeker(self, user_id: int) -> None: ...
