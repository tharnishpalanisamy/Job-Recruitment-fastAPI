from types import SimpleNamespace

import pytest

from app.core import UserRole
from app.exceptions import JobSeekerProfileAlreadyExistsException
from app.schemas import JobSeekerCreate


@pytest.mark.asyncio
async def test_create_job_seeker_success(
    job_seeker_service,
    mock_job_seeker_repository,
    mock_user_repository,
    mock_db,
    mock_email_service,
    job_seeker_payload,
):
    user = SimpleNamespace(
        id=1,
        username="arun",
        email="arun@gmail.com",
    )

    profile = SimpleNamespace(
        id=1,
        user_id=1,
    )

    updated_user = SimpleNamespace(
        id=1,
        username="arun",
        email="arun@gmail.com",
        role=UserRole.JOB_SEEKER,
    )

    mock_job_seeker_repository.get_by_user_id.return_value = None
    mock_job_seeker_repository.create.return_value = profile
    mock_user_repository.update_role.return_value = updated_user

    result = await job_seeker_service.create_job_seeker(
        user,
        JobSeekerCreate(**job_seeker_payload),
    )

    assert result == profile


@pytest.mark.asyncio
async def test_create_job_seeker_duplicate(
    job_seeker_service,
    mock_job_seeker_repository,
    mock_user_repository,
    mock_db,
):
    user = SimpleNamespace(id=1)

    existing_profile = SimpleNamespace(id=10, user_id=1)

    mock_job_seeker_repository.get_by_user_id.return_value = existing_profile

    with pytest.raises(JobSeekerProfileAlreadyExistsException):
        await job_seeker_service.create_job_seeker(
            user,
            SimpleNamespace(model_dump=dict),
        )


@pytest.mark.asyncio
async def test_get_current_job_seeker_success(
    job_seeker_service,
    mock_job_seeker_repository,
):
    user = SimpleNamespace(id=1)

    profile = SimpleNamespace(id=10, user_id=1)

    mock_job_seeker_repository.get_by_user_id.return_value = profile

    result = await job_seeker_service.get_current_job_seeker(user)

    assert result == profile

    mock_job_seeker_repository.get_by_user_id.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_update_current_job_seeker_success(
    job_seeker_service,
    mock_job_seeker_repository,
    mock_db,
):
    from app.schemas import JobSeekerUpdate

    user = SimpleNamespace(id=1)

    existing_profile = SimpleNamespace(id=10, user_id=1)

    updated_profile = SimpleNamespace(
        id=10,
        user_id=1,
        current_company="New Company",
    )

    mock_job_seeker_repository.get_by_user_id.return_value = existing_profile

    mock_job_seeker_repository.update_by_user_id.return_value = updated_profile

    payload = JobSeekerUpdate.model_construct(current_company="New Company")

    result = await job_seeker_service.update_current_job_seeker(user, payload)

    assert result.current_company == "New Company"

    mock_job_seeker_repository.update_by_user_id.assert_awaited_once_with(
        existing_profile,
        {"current_company": "New Company"},
    )

    mock_db.commit.assert_awaited_once()
