from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.core import UserRole
from app.dependencies import get_current_user, get_job_service, require_roles
from app.models import User
from app.schemas import (
    JobCreate,
    JobFilterParams,
    JobListResponse,
    JobResponse,
    JobUpdate,
)
from app.services.protocols import JobServiceProtocol

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post(
    "/create",
    summary="create job posting",
    status_code=status.HTTP_201_CREATED,
    response_model=JobResponse,
)
async def create_job(
    job_data: JobCreate,
    user: Annotated[User, Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN))],
    service: Annotated[JobServiceProtocol, Depends(get_job_service)],
):
    return await service.create_job(user, job_data)


@router.get("/", summary="get all jobs", response_model=list[JobListResponse])
async def get_all_jobs(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[JobServiceProtocol, Depends(get_job_service)],
    filters: Annotated[JobFilterParams, Depends()],
    limit: int = Query(default=20, ge=0, le=100),
    offset: int = Query(default=0, ge=0),
):
    return await service.get_all_jobs(filters, limit, offset)


@router.get("/{job_id}", summary="Get job by id", response_model=JobResponse)
async def get_job_by_id(
    job_id: int,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[JobServiceProtocol, Depends(get_job_service)],
):
    return await service.get_job_by_id(job_id)


@router.patch("/{job_id}", summary="update job by id ", response_model=JobResponse)
async def update_job_by_id(
    job_id: int,
    job_data: JobUpdate,
    user: Annotated[User, Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN))],
    service: Annotated[JobServiceProtocol, Depends(get_job_service)],
):
    return await service.update_job(job_id , job_data) 


@router.delete(
    "/{job_id}", summary="Delete job by id ", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_job_by_id(
    job_id: int,
    user: Annotated[User, Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN))],
    service: Annotated[JobServiceProtocol, Depends(get_job_service)],
):
    return await service.delete_job_by_id( user , job_id)
