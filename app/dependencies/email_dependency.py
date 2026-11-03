from typing import Annotated

from fastapi import Depends

from app.client import EmailClient
from app.services.implementations import EmailService
from app.services.protocols import EmailServiceProtocol


def get_email_client() -> EmailClient:
    return EmailClient()


def get_email_service(
    email_client: Annotated[EmailClient, Depends(get_email_client)],
) -> EmailServiceProtocol:
    return EmailService(email_client)
