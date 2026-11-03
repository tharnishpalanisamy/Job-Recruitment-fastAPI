from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status

from app.core import UserRole , ApplicationStatus
from app.dependencies import get_application_service, require_roles
from app.models import User
from app.services.protocols import ApplicationServiceProtocol

router = APIRouter(prefix="/application", tags=["Application"])


@router.post("/apply", summary="Apply to job")
async def apply(
    job_id: Annotated[int, Form(...)],
    resume: Annotated[UploadFile, File(...)],
    user: Annotated[User, Depends(require_roles(UserRole.JOB_SEEKER))],
    service: Annotated[ApplicationServiceProtocol, Depends(get_application_service)],
):

    return await service.create_application(job_id, resume, user)


@router.get("/me", summary="get users applications")
async def get_current_user_applications(
    user: Annotated[User, Depends(require_roles(UserRole.JOB_SEEKER))],
    service: Annotated[ApplicationServiceProtocol, Depends(get_application_service)],
):
    return await service.get_current_user_applications(user)


@router.delete(
    "/{application_id}",
    summary="Delete job applications using id ",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_application(
    application_id: int,
    user: Annotated[
        User,
        Depends(require_roles(UserRole.JOB_SEEKER, UserRole.ADMIN, UserRole.RECRUITER)),
    ],
    service: Annotated[ApplicationServiceProtocol, Depends(get_application_service)],
):
    return await service.delete_application_by_id(user, application_id)


@router.get("/", summary="get all applications")
async def get_all_applications(
    user: Annotated[
        User,
        Depends(require_roles( UserRole.ADMIN, UserRole.RECRUITER)),
    ],
    service: Annotated[ApplicationServiceProtocol, Depends(get_application_service)],
    job_id:int | None = Query(default=None) ,
    limit: int = Query(ge=1, le=100, default=20),
    offset: int = Query(ge=0, default=0),
):
    return await service.get_all_applications(user , job_id , limit , offset )

@router.patch('/{application_id}/status') 
async def update_application_status(
    application_id:int , 
    status : ApplicationStatus ,
    user: Annotated[
            User,
            Depends(require_roles( UserRole.RECRUITER)),
        ],
    service: Annotated[ApplicationServiceProtocol, Depends(get_application_service)],  
) : 
    return await service.update_application_status_by_id(user , application_id , status)