"""FastAPI main application"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.v1 import api_router
from app.config import settings
from app.core.logging import setup_logging, get_logger
from app.database.base import engine, Base

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for app startup/shutdown"""
    # Startup
    logger.info("app_startup", environment=settings.environment)
    Base.metadata.create_all(bind=engine)
    logger.info("database_tables_initialized")
    yield
    # Shutdown
    logger.info("app_shutdown")


def create_app() -> FastAPI:
    """Create FastAPI application"""
    # Setup logging
    setup_logging()

    # Create app
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description=settings.api_description,
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(api_router)

    logger.info(
        "app_created",
        title=settings.api_title,
        version=settings.api_version,
    )

    return app


app = create_app()
