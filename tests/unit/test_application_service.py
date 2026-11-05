from io import BytesIO
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from fastapi import UploadFile

from app.core import ApplicationStatus, JobStatus, UserRole
from app.exceptions import (
    ApplicationAlreadyExistsException,
    JobNotAcceptingApplicationsException,
)


@pytest.mark.asyncio
async def test_create_application_success(
    application_service,
    mock_job_seeker_repository,
    mock_job_repository,
    mock_application_repository,
    mock_user_repository,
    mock_email_service,
    mock_db,
):
    user = SimpleNamespace(id=1)

    job_seeker = SimpleNamespace(id=10, user_id=1)

    job = SimpleNamespace(
        id=20,
        vacancies=3,
        status=JobStatus.OPEN,
        title="Python Developer",
        created_by=2,
    )

    applicant = SimpleNamespace(
        id=1,
        email="applicant@test.com",
        username="applicant",
    )

    recruiter = SimpleNamespace(
        id=2,
        email="recruiter@test.com",
        username="recruiter",
    )

    created_application = SimpleNamespace(
        id=100,
        job_id=20,
        job_seeker_id=10,
    )

    mock_job_seeker_repository.get_by_user_id.return_value = job_seeker
    mock_job_repository.get_by_id.return_value = job
    mock_application_repository.get_existing_application.return_value = None
    mock_application_repository.create.return_value = created_application
    mock_job_seeker_repository.get_by_id.return_value = job_seeker

    mock_user_repository.get_by_id.side_effect = [
        applicant,
        recruiter,
    ]

    resume = UploadFile(
        filename="resume.pdf",
        file=BytesIO(b"fake resume"),
    )

    with patch(
        "app.services.implementations.application_service.save_resume",
        return_value="/tmp/fake_resume.pdf",
    ):
        result = await application_service.create_application(20, resume, user)

    assert result == created_application

    mock_db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_application_duplicate(
    application_service,
    mock_job_seeker_repository,
    mock_job_repository,
    mock_application_repository,
    mock_db,
):
    user = SimpleNamespace(id=1)

    mock_job_seeker_repository.get_by_user_id.return_value = SimpleNamespace(id=10)

    mock_job_repository.get_by_id.return_value = SimpleNamespace(
        id=20,
        vacancies=3,
        status=JobStatus.OPEN,
    )

    mock_application_repository.get_existing_application.return_value = SimpleNamespace(
        id=100
    )

    with pytest.raises(ApplicationAlreadyExistsException):
        await application_service.create_application(20, None, user)


@pytest.mark.asyncio
async def test_create_application_closed_job(
    application_service,
    mock_job_seeker_repository,
    mock_job_repository,
    mock_application_repository,
    mock_db,
):
    user = SimpleNamespace(id=1)

    mock_job_seeker_repository.get_by_user_id.return_value = SimpleNamespace(id=10)

    mock_job_repository.get_by_id.return_value = SimpleNamespace(
        id=20,
        vacancies=3,
        status=JobStatus.CLOSED,
    )

    with pytest.raises(JobNotAcceptingApplicationsException):
        await application_service.create_application(20, None, user)


@pytest.mark.asyncio
async def test_select_applicant_reduces_vacancy(
    application_service,
    mock_application_repository,
    mock_job_repository,
    mock_job_seeker_repository,
    mock_user_repository,
    mock_email_service,
    mock_db,
):
    user = SimpleNamespace(
        id=1,
        role=UserRole.RECRUITER,
    )

    application = SimpleNamespace(
        id=10,
        job_id=20,
        job_seeker_id=30,
        status=ApplicationStatus.SHORTLISTED,
    )

    job = SimpleNamespace(
        id=20,
        created_by=1,
        title="Python Developer",
        status=JobStatus.OPEN,
        vacancies=2,
    )

    job_seeker = SimpleNamespace(
        id=30,
        user_id=40,
    )

    applicant = SimpleNamespace(
        id=40,
        email="applicant@test.com",
        username="applicant",
    )

    mock_application_repository.get_by_application_id.return_value = application
    mock_job_repository.get_by_id_for_update.return_value = job
    mock_application_repository.update_status.return_value = application

    mock_job_seeker_repository.get_by_id.return_value = job_seeker
    mock_user_repository.get_by_id.return_value = applicant

    result = await application_service.update_application_status_by_id(
        user,
        10,
        ApplicationStatus.SELECTED,
    )

    assert result == application

    mock_application_repository.update_status.assert_awaited_once_with(
        application,
        ApplicationStatus.SELECTED,
    )
