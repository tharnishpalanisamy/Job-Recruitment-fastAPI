from app.exceptions import JobNotFoundException, JobProfileNotFoundException
from app.models import Application
from app.repositories.protocols import (
    ApplicationRepositoryProtocol,
    JobRepositoryProtocol,
    JobSeekersRepositoryProtocol,
)
from app.utilities import save_resume


class ApplicationService:
    def __init__(
        self,
        db,
        repository: ApplicationRepositoryProtocol,
        job_seeker_repository: JobSeekersRepositoryProtocol,
        job_repository: JobRepositoryProtocol,
    ):
        self.db = db
        self.application_repository = repository
        self.job_seeker_repository = job_seeker_repository
        self.job_repository = job_repository

    async def create_application(self, job_id, resume, user):
        job_seeker = await self.job_seeker_repository.get_by_user_id(user.id)

        if job_seeker is None:
            raise JobProfileNotFoundException("User do not have a job seeker profile ")
        job = await self.job_repository.get_by_id(job_id)

        if job is None:
            raise JobNotFoundException(f"Job with job id {job_id} not found ")
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
        return result

    async def get_all_applications(self, filters, limit, offset): ...

    async def get_all_by_recruiter(self, filters, limit, offset, recruiter): ...

    async def get_applications_by_job_id(self, job_id): ...

    async def update_application_status_by_id(self, id, status): ...

    async def delete_application_by_id(self, user, id): ...
