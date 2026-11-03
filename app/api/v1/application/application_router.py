from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.core import UserRole
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

@router.get('/me' , summary='get users applications') 
async def get_current_user_applications(
    user:Annotated[User , Depends(require_roles(UserRole.JOB_SEEKER))] , 
    service : Annotated[ApplicationServiceProtocol , Depends(get_application_service)]
) :
    return await service.get_current_user_applications(user) 