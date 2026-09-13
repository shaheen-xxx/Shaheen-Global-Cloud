"""Application configuration"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # Environment
    environment: str = "development"
    debug: bool = True
    log_level: str = "DEBUG"

    # API
    api_title: str = "Shaheen Global Cloud API"
    api_version: str = "0.1.0"
    api_description: str = "Cloud provisioning platform MVP"

    # Database
    database_url: str = "postgresql://shaheen:shaheen_password@postgres:5432/shaheen_cloud"

    # Redis
    redis_url: str = "redis://redis:6379/0"

    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Dagger
    dagger_workdir: str = "/tmp/dagger-work"
    dagger_cache_dir: str = "/tmp/dagger-cache"

    # CORS
    cors_origins: list = ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
