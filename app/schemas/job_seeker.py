from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


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
