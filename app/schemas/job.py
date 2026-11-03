from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.core import EmploymentType, JobStatus


class JobCreate(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: str = Field(min_length=10)
    requirements: str = Field(min_length=5)
    qualification: str = Field(min_length=2, max_length=150)

    experience_min: float = Field(default=0, ge=0)
    experience_max: float | None = Field(default=None, ge=0)

    salary_min: float | None = Field(default=None, ge=0)
    salary_max: float | None = Field(default=None, ge=0)

    employment_type: EmploymentType
    location: str = Field(min_length=2, max_length=150)

    vacancies: int = Field(default=1, ge=1)

    @model_validator(mode="after")
    def validate_ranges(self):
        if (
            self.experience_max is not None
            and self.experience_max < self.experience_min
        ):
            raise ValueError(
                "Maximum experience cannot be less than minimum experience"
            )

        if (
            self.salary_min is not None
            and self.salary_max is not None
            and self.salary_max < self.salary_min
        ):
            raise ValueError("Maximum salary cannot be less than minimum salary")

        return self


class JobListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    qualification: str
    experience_min: float
    experience_max: float | None
    salary_min: float | None
    salary_max: float | None
    employment_type: EmploymentType
    location: str
    status: JobStatus
    created_at: datetime


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    requirements: str
    qualification: str
    experience_min: float
    experience_max: float | None
    salary_min: float | None
    salary_max: float | None
    employment_type: EmploymentType
    location: str
    vacancies: int
    status: JobStatus
    created_by: int
    created_at: datetime


class JobFilterParams(BaseModel):
    title: str | None = Field(max_length=150, default=None)
    requirements: str | None = Field(max_length=255, default=None)

    qualification: str | None = Field(max_length=150, default=None)
    experience_min: float | None = Field(ge=0, default=None)
    experience_max: float | None = Field(gt=0, default=None)
    salary_min: float | None = Field(ge=0, default=None)
    salary_max: float | None = Field(gt=0, default=None)
    employment_type: EmploymentType | None = Field(default=None)
    location: str | None = Field(default=None, max_length=150)
    created_at: date | None = Field(default=None)


class JobUpdate(BaseModel):
    title: str | None = Field(min_length=3, max_length=150, default=None)
    description: str | None = Field(min_length=10, default=None)
    requirements: str | None = Field(min_length=5, default=None)
    qualification: str | None = Field(min_length=2, max_length=150, default=None)

    experience_min: float | None = Field(ge=0, default=None)
    experience_max: float | None = Field(default=None, ge=0)

    salary_min: float | None = Field(default=None, ge=0)
    salary_max: float | None = Field(default=None, ge=0)

    employment_type: EmploymentType | None = Field(default=None)
    location: str | None = Field(min_length=2, max_length=150, default=None)

    vacancies: int | None = Field(ge=1, default=None)

    @model_validator(mode="after")
    def validate_ranges(self):
        if (
            self.experience_min is not None
            and self.experience_max is not None
            and self.experience_max < self.experience_min
        ):
            raise ValueError(
                "Maximum experience cannot be less than minimum experience"
            )

        if (
            self.salary_min is not None
            and self.salary_max is not None
            and self.salary_max < self.salary_min
        ):
            raise ValueError("Maximum salary cannot be less than minimum salary")

        return self
