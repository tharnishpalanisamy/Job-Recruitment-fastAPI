from fastapi import APIRouter

from .auth import auth_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)
