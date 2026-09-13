"""Mock provider tests"""

import pytest
from app.providers.base import MockProvider


@pytest.mark.asyncio
async def test_mock_provider_provision():
    """Test mock provider provisioning"""
    provider = MockProvider()
    config = {
        "name": "test-server",
        "provider": "mock",
        "region": "fsn1",
        "size": "cx22",
        "image": "ubuntu-24.04",
    }
    result = await provider.provision(config)
    assert result.success
    assert result.server_id is not None
    assert result.ipv4 is not None
    assert result.ipv6 is not None


@pytest.mark.asyncio
async def test_mock_provider_destroy():
    """Test mock provider destroy"""
    provider = MockProvider()
    result = await provider.destroy("mock-1001")
    assert result is True


@pytest.mark.asyncio
async def test_mock_provider_status():
    """Test mock provider get status"""
    provider = MockProvider()
    status = await provider.get_status("mock-1001")
    assert status == "running"
