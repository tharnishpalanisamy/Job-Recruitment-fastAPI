import logging
from pathlib import Path

from fastapi_mail import MessageType
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.client import EmailClient

logger = logging.getLogger(__name__)

TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "templates"

template_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml"]),
)


class EmailService:
    def __init__(self, email_client: EmailClient) -> None:
        self.email_client = email_client

    async def _send_template(
        self,
        recipient: str | None,
        subject: str,
        template_name: str,
        context: dict[str, str],
    ) -> None:
        if not recipient:
            logger.info(
                "Skipping email %r because no recipient address is available",
                subject,
            )
            return

        try:
            template = template_env.get_template(template_name)
            body = template.render(**context)

            await self.email_client.send_email(
                recipient=recipient,
                subject=subject,
                body=body,
                subtype=MessageType.html,
            )
        except Exception:
            logger.exception("Failed to send email %r to %s", subject, recipient)

    async def send_welcome_email(
        self,
        recipient: str,
        username: str,
    ) -> None:
        await self._send_template(
            recipient=recipient,
            subject="Welcome to Job Portal!",
            template_name="welcome.html",
            context={"username": username},
        )

    async def send_application_confirmation(
        self,
        recipient: str,
        username: str,
        job_title: str,
    ) -> None:
        await self._send_template(
            recipient=recipient,
            subject="Application Submitted Successfully",
            template_name="application_confirmation.html",
            context={
                "username": username,
                "job_title": job_title,
            },
        )

    async def send_job_seeker_account_creation_email(
        self, recipient: str, username: str
    ) -> None:
        await self._send_template(
            recipient=recipient,
            subject="Your Job Seeker Profile Has Been Successfully Created – Job Portal", 
            template_name='job_seeker.html',
            context={
                'username':username
            }
        )
    async def send_new_application_notification(
        self,
        recipient: str,
        recruiter_name: str,
        applicant_name: str,
        job_title: str,
    ) -> None:
        await self._send_template(
            recipient=recipient,
            subject="New Job Application Received",
            template_name="new_application_notification.html",
            context={
                "recruiter_name": recruiter_name,
                "applicant_name": applicant_name,
                "job_title": job_title,
            },
        )

    async def send_application_status_update(
        self,
        recipient: str,
        username: str,
        job_title: str,
        status: str,
    ) -> None:
        await self._send_template(
            recipient=recipient,
            subject="Application Status Updated",
            template_name="application_status_update.html",
            context={
                "username": username,
                "job_title": job_title,
                "status": status,
            },
        )
