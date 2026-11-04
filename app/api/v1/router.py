from fastapi import APIRouter

from .application import application_router
from .auth import auth_router
from .health import health_router
from .job import job_router
from .job_seekers import job_seekers_route

router = APIRouter(prefix="/api/v1")

router.include_router(health_router)
router.include_router(auth_router)
router.include_router(job_seekers_route)
router.include_router(job_router)
router.include_router(application_router)
