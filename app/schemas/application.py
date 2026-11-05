from datetime import datetime

from pydantic import BaseModel

from app.core import ApplicationStatus


class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    job_seeker_id: int
    resume_filename: str
    status: ApplicationStatus
    applied_at: datetime


class ApplicationDetailedResponse(BaseModel):
    id: int
    job_id: int
    job_seeker_id: int
    resume_filename: str
    status: ApplicationStatus
    applied_at: datetime
