from fastapi import APIRouter

from api.v1.documents import router as documents_router
from api.v1.health import router as health_router
from api.v1.transcribe import router as transcribe_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health_router, tags=["health"])
api_router.include_router(transcribe_router, tags=["transcription"])
api_router.include_router(documents_router, tags=["documents"])
