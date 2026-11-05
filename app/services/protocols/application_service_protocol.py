from typing import Protocol

from fastapi import UploadFile

from app.core import ApplicationStatus
from app.models import Application, User
from app.core import ApplicationResult

class ApplicationServiceProtocol(Protocol):
    async def create_application(
        self, job_id: int, resume: UploadFile, user: User
    ) -> Application: ...

    async def get_current_user_applications(
        self, user: User
    ) -> list[Application]: ...

    async def get_all_applications(
        self, user: User, job_id: int | None, limit: int, offset: int
    ) -> list[Application]: ...

    async def update_application_status_by_id(
        self, user: User, application_id: int, status: ApplicationStatus
    ) -> Application: ...

    async def delete_application_by_id(self, user: User, id: int) -> None: ... 

    async def update_resume_by_id(self, user ,application_id , resume ) : ... 

    async def get_application_by_id(self , user:User, application_id:int ) -> Application : ... 