from app.core import ApplicationStatus

ALLOWED_TRANSITIONS = {
    ApplicationStatus.APPLIED: {
        ApplicationStatus.UNDER_REVIEW,
    },
    ApplicationStatus.UNDER_REVIEW: {
        ApplicationStatus.SHORTLISTED,
        ApplicationStatus.REJECTED,
    },
    ApplicationStatus.SHORTLISTED: {
        ApplicationStatus.SELECTED,
        ApplicationStatus.REJECTED,
    },
    ApplicationStatus.SELECTED: set(),
    ApplicationStatus.REJECTED: set(),
}
