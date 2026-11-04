import enum


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"
    RECRUITER = "recruiter"
    JOB_SEEKER = "job_seeker"


class EmploymentType(str, enum.Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"


class JobStatus(str, enum.Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class ApplicationStatus(str, enum.Enum):
    APPLIED = "APPLIED"
    UNDER_REVIEW = "UNDER_REVIEW"
    SHORTLISTED = "SHORTLISTED"
    REJECTED = "REJECTED"
    SELECTED = "SELECTED"


class SortBy(str, enum.Enum):
    ASC = "asc"
    DESC = "desc"


class ApplicationResult(str, enum.Enum):
    SELECTED = "SELECTED"
    REJECTED = "REJECTED"
