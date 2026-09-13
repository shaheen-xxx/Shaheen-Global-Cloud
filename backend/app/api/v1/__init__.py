"""API v1 routes"""

from fastapi import APIRouter
from app.api.v1.endpoints import health, servers, jobs

api_router = APIRouter(prefix="/api/v1")

# Include routers
api_router.include_router(health.router)
api_router.include_router(servers.router)
api_router.include_router(jobs.router)

__all__ = ["api_router"]
