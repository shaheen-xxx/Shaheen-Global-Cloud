"""Provider service"""

from app.providers.base import MockProvider, HetznerProvider, ProviderAdapter
from app.config import settings
from app.core.logging import get_logger
from typing import Optional
import os

logger = get_logger(__name__)


class ProviderService:
    """Service for managing provider adapters"""

    _providers = {}

    @classmethod
    def get_provider(cls, provider_name: str) -> Optional[ProviderAdapter]:
        """Get a provider adapter"""
        provider_name = provider_name.lower()

        if provider_name == "mock":
            return MockProvider()
        elif provider_name == "hetzner":
            api_token = os.getenv("HETZNER_API_TOKEN")
            if not api_token:
                logger.warning("hetzner_api_token_missing")
                return None
            return HetznerProvider(api_token)
        else:
            logger.error("unknown_provider", provider=provider_name)
            return None

    @classmethod
    def is_supported(cls, provider_name: str) -> bool:
        """Check if provider is supported"""
        supported = ["mock", "hetzner"]
        return provider_name.lower() in supported
