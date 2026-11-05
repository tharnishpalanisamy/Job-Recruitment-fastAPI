from unittest.mock import AsyncMock

import pytest

from app.services.implementations import ApplicationService, AuthService, JobService


@pytest.fixture
def mock_db():
    return AsyncMock()


@pytest.fixture
def mock_user_repository():
    return AsyncMock()


@pytest.fixture
def mock_refresh_token_service():
    return AsyncMock()


@pytest.fixture
def mock_email_service():
    return AsyncMock()


@pytest.fixture
def auth_service(
    mock_db,
    mock_user_repository,
    mock_refresh_token_service,
    mock_email_service,
):
    return AuthService(
        db=mock_db,
        repository=mock_user_repository,
        refresh_token_service=mock_refresh_token_service,
        email_service=mock_email_service,
    )


@pytest.fixture
def mock_job_repository():
    return AsyncMock()


@pytest.fixture
def job_service(mock_db, mock_job_repository):
    return JobService(
        db=mock_db,
        repository=mock_job_repository,
    )


import pytest

from app.services.implementations.job_seeker_service import (
    JobSeekerService,
)


@pytest.fixture
def mock_job_seeker_repository():
    return AsyncMock()




@pytest.fixture
def job_seeker_service(
    mock_db,
    mock_job_seeker_repository,
    mock_user_repository,
    mock_email_service,
):
    return JobSeekerService(
        db=mock_db,
        repository=mock_job_seeker_repository,
        user_repository=mock_user_repository,
        email_service=mock_email_service,
    )


@pytest.fixture
def mock_application_repository():
    return AsyncMock()


@pytest.fixture
def application_service(
    mock_db,
    mock_application_repository,
    mock_job_seeker_repository,
    mock_job_repository,
    mock_user_repository,
    mock_email_service,
):
    return ApplicationService(
        db=mock_db,
        repository=mock_application_repository,
        job_seeker_repository=mock_job_seeker_repository,
        job_repository=mock_job_repository,
        user_repository=mock_user_repository,
        email_service=mock_email_service,
    )
