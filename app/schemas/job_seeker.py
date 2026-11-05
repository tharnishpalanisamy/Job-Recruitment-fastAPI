from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class JobSeekerCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    phone: str = Field(pattern=r"^\d{10}$")
    date_of_birth: date

    qualification: str = Field(min_length=2, max_length=150)
    specialization: str | None = Field(default=None, max_length=150)

    experience_years: Decimal = Field(ge=0, decimal_places=1)

    current_company: str | None = Field(default=None, max_length=150)
    current_designation: str | None = Field(default=None, max_length=150)

    current_salary: int = Field(ge=0)


class JobSeekerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    full_name: str
    phone: str
    date_of_birth: date
    qualification: str
    specialization: str
    experience_years: Decimal
    current_company: str | None
    current_designation: str | None
    current_salary: int | None
    created_at: datetime


class JobSeekerUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )
    phone: str | None = Field(
        default=None,
        pattern=r"^\d{10}$",
    )
    date_of_birth: date | None = None
    qualification: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )
    specialization: str | None = Field(
        default=None,
        max_length=150,
    )
    experience_years: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=1,
    )
    current_company: str | None = Field(
        default=None,
        max_length=150,
    )
    current_designation: str | None = Field(
        default=None,
        max_length=150,
    )
    current_salary: int | None = Field(
        default=None,
        ge=0,
    )

    @model_validator(mode="after")
    def require_at_least_one_field(self) -> "JobSeekerUpdate":
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided")
        return self


class JobSeekerFilterParams(BaseModel):
    qualification: str | None = Field(default=None, min_length=1, max_length=30)
    specialization: str | None = Field(default=None, min_length=1, max_length=30)
    designation: str | None = Field(default=None, min_length=1, max_length=30)
    min_experience: Decimal | None = Field(default=None, ge=0)
    max_experience: Decimal | None = Field(default=None, gt=0)
    current_salary: int | None = Field(default=None)

    @model_validator(mode="after")
    def validate_experience_range(self) -> "JobSeekerFilterParams":
        if (
            self.min_experience is not None
            and self.max_experience is not None
            and self.min_experience > self.max_experience
        ):
            raise ValueError(
                "minimum experience cannot be greater than maximum experience"
            )

        return self
