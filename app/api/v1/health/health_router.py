from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies import get_health_service
from app.services.protocols import HealthServiceProtocol

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", summary="check application health", status_code=status.HTTP_200_OK)
async def get_health() -> dict[str, str]:
    return {"status": "Healthy", "message": "Application is running"}


@router.get("/ready")
async def readiness_check(
    service: Annotated[HealthServiceProtocol, Depends(get_health_service)],
) -> dict[str, str]:
    return await service.check_readiness()
