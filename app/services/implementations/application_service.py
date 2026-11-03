import logging
from pathlib import Path

from app.core import UserRole
from app.exceptions import (
    ApplicationAlreadyExistsException,
    ApplicationNotFoundException,
    JobNotFoundException,
    JobProfileNotFoundException,
    NotAuthorizedException,
)
from app.models import Application
from app.repositories.protocols import (
    ApplicationRepositoryProtocol,
    JobRepositoryProtocol,
    JobSeekersRepositoryProtocol,
    UserRepositoryProtocol,
)
from app.services.protocols import EmailServiceProtocol
from app.utilities import save_resume

logger = logging.getLogger(__name__)


class ApplicationService:
    def __init__(
        self,
        db,
        repository: ApplicationRepositoryProtocol,
        job_seeker_repository: JobSeekersRepositoryProtocol,
        job_repository: JobRepositoryProtocol,
        user_repository: UserRepositoryProtocol,
        email_service: EmailServiceProtocol,
    ):
        self.db = db
        self.application_repository = repository
        self.job_seeker_repository = job_seeker_repository
        self.job_repository = job_repository
        self.user_repository = user_repository
        self.email_service = email_service

    async def create_application(self, job_id, resume, user):
        job_seeker = await self.job_seeker_repository.get_by_user_id(user.id)

        if job_seeker is None:
            raise JobProfileNotFoundException("User do not have a job seeker profile ")
        job = await self.job_repository.get_by_id(job_id)

        if job is None:
            raise JobNotFoundException(f"Job with job id {job_id} not found ")

        existing_application = await self.application_repository.get_existing_application(
            job_seeker.id, job.id
        )

        if existing_application is not None:
            raise ApplicationAlreadyExistsException(
                f"You have already applied to the job {job_id}"
            )
        file_name = resume.filename
        file_path = await save_resume(resume)

        application = Application(
            job_seeker_id=job_seeker.id,
            job_id=job_id,
            resume_filename=file_name,
            resume_path=file_path,
        )

        result = await self.application_repository.create(application)
        await self.db.commit()
        applicant = await self.user_repository.get_by_id(user.id)
        if applicant is not None:
            await self.email_service.send_application_confirmation(
                recipient=applicant.email,
                username=applicant.username,
                job_title=job.title,
            )
        return result

    async def get_current_user_applications(self, user):
        job_seeker = await self.job_seeker_repository.get_by_user_id(user.id)
        if job_seeker is None:
            raise JobProfileNotFoundException("User do not have a job seeker profile ")
        result = await self.application_repository.get_all_by_job_seeker_id(
            job_seeker.id
        )
        return result

    async def get_all_applications(self, user, job_id, limit, offset):
        recruiter_id = None

        if user.role == UserRole.RECRUITER:
            recruiter_id = user.id

        result = await self.application_repository.get_all(
            recruiter_id, job_id, limit, offset
        )

        return result

    async def get_applications_by_job_id(self, job_id): ...

    async def update_application_status_by_id(self, user, application_id, status):
        application = await self.application_repository.get_by_application_id(
            application_id
        )
        if application is None:
            raise ApplicationNotFoundException(
                f"Application with id {application_id} not found "
            )

        job = await self.job_repository.get_by_id(application.job_id)

        if job.created_by != user.id:
            raise NotAuthorizedException(
                "You are not allowed to perform this operation "
            )
        title = job.title 
        result = await self.application_repository.update_status(application, status)
        await self.db.commit()  

        applicant = await self.user_repository.get_by_id(user.id)
        if applicant is not None:
            await self.email_service.send_application_status_update(
                recipient=applicant.email,
                username=applicant.username,
                job_title=title,
                status=status.capitalize(),
            )

        return result

    async def delete_application_by_id(self, user, id):
        application = await self.application_repository.get_by_application_id(id)

        if application is None:
            raise ApplicationNotFoundException(f"Job application with {id} not found")
        job = await self.job_repository.get_by_id(application.job_id)

        if user.role == UserRole.JOB_SEEKER:
            job_seeker = await self.job_seeker_repository.get_by_user_id(user.id)

            if job_seeker is None:
                raise JobProfileNotFoundException(
                    "Cannot find job profile associated with user"
                )
            if application.job_seeker_id != job_seeker.id:
                raise NotAuthorizedException("Not Authorized to perform this action")
        elif user.role == UserRole.RECRUITER:
            if job.created_by != user.id:
                raise NotAuthorizedException("Not Authorized to perform this action")

        resume_path = Path(application.resume_path)

        result = await self.application_repository.delete_by_id(id)
        await self.db.commit()

        try:
            if resume_path.exists():
                resume_path.unlink()
        except OSError:
            logger.exception("Failed to delete resume file: %s", resume_path)

        return result
