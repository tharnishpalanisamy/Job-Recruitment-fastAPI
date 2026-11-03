from pydantic import BaseModel


class ApplicationCreate(BaseModel):

        job_id: int
    
        resume_filename: str
    
        resume_path: str