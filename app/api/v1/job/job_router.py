from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core import UserRole
from app.dependencies import get_job_service, require_roles
from app.models import User
from app.schemas import JobCreate, JobResponse
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
