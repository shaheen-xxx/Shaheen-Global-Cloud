"""Health check endpoints"""

from fastapi import APIRouter
from app.api.v1.schemas import HealthResponse
from app.config import settings

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        environment=settings.environment,
    )
