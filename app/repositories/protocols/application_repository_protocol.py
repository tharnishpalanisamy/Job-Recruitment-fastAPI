from typing import Protocol

from app.core import ApplicationStatus
from app.models import Application


class ApplicationRepositoryProtocol(Protocol):
    async def create(self, application: Application) -> Application: ...

    async def get_all_by_job_seeker_id(self, id: int) -> list[Application]: ...

    async def get_existing_application(
        self, job_seeker_id: int, job_id: int
    ) -> Application | None: ...

    async def get_all(
        self, recruiter_id: int | None, job_id: int | None, limit: int, offset: int
    ) -> list[Application]: ...

    async def get_by_application_id(self, id: int) -> Application | None: ...

    async def update_status(
        self, application: Application, status: ApplicationStatus
    ) -> Application: ...

    async def delete_by_id(self, id: int) -> None: ...

    async def update_resume(
        self, application: Application, filename: str, file_path: str
    ) -> Application: ...
