from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.core import UserRole
from app.dependencies import get_job_seeker_service, require_roles
from app.models import User
from app.schemas import (
    JobSeekerCreate,
    JobSeekerFilterParams,
    JobSeekerResponse,
    JobSeekerUpdate,
)
from app.services.protocols import JobSeekerServiceProtocol

router = APIRouter(prefix="/job-seekers", tags=["Job Seekers"])


@router.post(
    "/create",
    summary="Create job profile",
    status_code=status.HTTP_201_CREATED,
    response_model=JobSeekerResponse,
)
async def create_job_seeker(
    data: JobSeekerCreate,
    user: Annotated[User, Depends(require_roles(UserRole.JOB_SEEKER))],
    service: Annotated[JobSeekerServiceProtocol, Depends(get_job_seeker_service)],
):
    return await service.create_job_seeker(user, data)


@router.get("/me", summary="get own profile", response_model=JobSeekerResponse)
async def get_current_user(
    user: Annotated[User, Depends(require_roles(UserRole.JOB_SEEKER))],
    service: Annotated[JobSeekerServiceProtocol, Depends(get_job_seeker_service)],
):
    return await service.get_current_job_seeker(user)


@router.patch(
    "/me", summary="update job seeker profile", response_model=JobSeekerResponse
)
async def update_current_jobseeker(
    job_seeker_data: JobSeekerUpdate,
    user: Annotated[User, Depends(require_roles(UserRole.JOB_SEEKER))],
    service: Annotated[JobSeekerServiceProtocol, Depends(get_job_seeker_service)],
):
    return await service.update_current_job_seeker(user, job_seeker_data)


@router.delete(
    "/me", summary="Delete job seeker profile", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_current_job_seeker(
    user: Annotated[User, Depends(require_roles(UserRole.JOB_SEEKER))],
    service: Annotated[JobSeekerServiceProtocol, Depends(get_job_seeker_service)],
):
    return await service.delete_current_job_seeker(user.id)


@router.get("/", summary="get all job seekers")
async def get_all_job_seekers(
    user: Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.RECRUITER))],
    service: Annotated[JobSeekerServiceProtocol, Depends(get_job_seeker_service)],
    filters: Annotated[JobSeekerFilterParams, Depends()],
    limit: int = Query(ge=0, le=100, default=20),
    offset: int = Query(ge=0, default=0),
):

    return await service.get_all_job_seekers(filters, limit, offset)


@router.get("/{job_seeker_id}", summary="get job seeker by id")
async def get_job_seeker_by_id(
    job_seeker_id: int,
    user: Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.RECRUITER))],
    service: Annotated[JobSeekerServiceProtocol, Depends(get_job_seeker_service)],
):
    return await service.get_job_seeker_by_id(job_seeker_id)
