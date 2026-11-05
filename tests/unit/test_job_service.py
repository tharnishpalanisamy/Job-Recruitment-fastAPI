from types import SimpleNamespace

import pytest

from app.core import UserRole
from app.schemas import JobCreate, JobUpdate


@pytest.mark.asyncio
async def test_create_job_success(
    job_service,
    mock_job_repository,
    mock_db,
    job_payload,
):

    user = SimpleNamespace(
        id=1,
        role=UserRole.RECRUITER,
    )

    mock_job_repository.create.return_value = SimpleNamespace(
        id=1,
        title="Software Engineer",
    )

    result = await job_service.create_job(
        user,
        JobCreate(**job_payload),
    )

    assert result.id == 1
    assert result.title == "Software Engineer"


@pytest.mark.asyncio
async def test_get_all_jobs(
    job_service,
    mock_job_repository,
):
    from app.schemas import JobFilterParams

    jobs = [
        SimpleNamespace(id=1, title="Python Developer"),
        SimpleNamespace(id=2, title="Backend Developer"),
    ]

    mock_job_repository.get_all.return_value = jobs

    filters = JobFilterParams.model_construct()

    result = await job_service.get_all_jobs(
        filters,
        limit=10,
        offset=0,
    )

    assert result == jobs


@pytest.mark.asyncio
async def test_get_job_by_id_success(
    job_service,
    mock_job_repository,
):
    job = SimpleNamespace(
        id=1,
        title="Python Developer",
    )

    mock_job_repository.get_by_id.return_value = job

    result = await job_service.get_job_by_id(1)

    assert result == job

    mock_job_repository.get_by_id.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_get_job_by_id_not_found(
    job_service,
    mock_job_repository,
):
    from app.exceptions import JobNotFoundException

    mock_job_repository.get_by_id.return_value = None

    with pytest.raises(JobNotFoundException):
        await job_service.get_job_by_id(999)

    mock_job_repository.get_by_id.assert_awaited_once_with(999)


@pytest.mark.asyncio
async def test_update_job_success(
    job_service,
    mock_job_repository,
    mock_db,
):

    user = SimpleNamespace(
        id=1,
        role=UserRole.RECRUITER,
    )

    existing_job = SimpleNamespace(
        id=10,
        created_by=1,
        title="Old Title",
    )

    updated_job = SimpleNamespace(
        id=10,
        created_by=1,
        title="New Title",
    )

    mock_job_repository.get_by_id.return_value = existing_job
    mock_job_repository.update.return_value = updated_job

    payload = JobUpdate.model_construct(title="New Title")

    result = await job_service.update_job(
        user,
        10,
        payload,
    )

    assert result.title == "New Title"
