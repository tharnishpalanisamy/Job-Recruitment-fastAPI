from app.core import UserRole
from app.exceptions import JobProfileNotFoundException, UserNotFoundException
from app.models import JobSeeker, User


class JobSeekerService:
    def __init__(self, db, repository, user_repository):
        self.db = db
        self.job_seeker_repository = repository
        self.user_repository = user_repository

    async def create_job_seeker(self, user, job_seeker_data):
        job_seeker = JobSeeker(user_id=user.id, **job_seeker_data.model_dump())
        result = await self.job_seeker_repository.create(job_seeker)
        updated_user = await self.user_repository.update_role(
            user.id, UserRole.JOB_SEEKER
        )

        if updated_user is None:
            raise UserNotFoundException()
        await self.db.commit()
        return result

    async def get_all_job_seekers(self, filters, limit, offset):
        pass

    async def get_current_job_seeker(self, user: User):
        current_job_seeker = await self.job_seeker_repository.get_by_user_id(user.id)

        if current_job_seeker is None:
            raise JobProfileNotFoundException()
        return current_job_seeker
