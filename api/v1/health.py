from fastapi import APIRouter

from api.schemas import HealthResponse
from config import settings
from services.health_service import HealthService

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    service = HealthService(adapter_mode=settings.ADAPTER_MODE)
    health_data = service.get_health_status()
    return HealthResponse(**health_data)
