from typing import Protocol


class EmailServiceProtocol(Protocol):
    async def send_welcome_email(self, recipient: str, username: str) -> None: ...

    async def send_job_seeker_account_creation_email(
        self, recipient: str, username: str
    ) -> None: ...

    async def send_application_confirmation(
        self, recipient: str, username: str, job_title: str
    ) -> None: ...

    async def send_new_application_notification(
        self,
        recipient: str,
        recruiter_name: str,
        applicant_name: str,
        job_title: str,
    ) -> None: ...

    async def send_application_status_update(
        self,
        recipient: str,
        username: str,
        job_title: str,
        status: str,
    ) -> None: ...
