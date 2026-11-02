from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class JobSeeker(Base):
    __tablename__ = "job_seekers"

    __table_args__ = (
        CheckConstraint(
            "experience_years >= 0",
            name="ck_job_seekers_experience_non_negative",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    date_of_birth: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    qualification: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    specialization: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    experience_years: Mapped[Decimal] = mapped_column(
        Numeric(4, 1),
        nullable=False,
        default=0,
    )

    current_company: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    current_designation: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    ) 

    current_salary : Mapped[int] = mapped_column(
        Integer , 
        nullable=False 
    )

    skills: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False ,
    )
