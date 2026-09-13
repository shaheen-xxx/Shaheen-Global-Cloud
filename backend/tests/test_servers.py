"""Integration tests for servers API"""

from fastapi.testclient import TestClient


def test_create_server(client: TestClient):
    """Test server creation"""
    response = client.post(
        "/api/v1/servers/",
        json={
            "name": "test-server",
            "provider": "mock",
            "region": "fsn1",
            "size": "cx22",
            "image": "ubuntu-24.04",
        },
    )
    assert response.status_code == 202
    data = response.json()
    assert "job_id" in data
    assert "server_id" in data
    assert data["status"] == "PENDING"


def test_create_server_invalid_provider(client: TestClient):
    """Test server creation with invalid provider"""
    response = client.post(
        "/api/v1/servers/",
        json={
            "name": "test-server",
            "provider": "invalid-provider",
            "region": "fsn1",
            "size": "cx22",
            "image": "ubuntu-24.04",
        },
    )
    assert response.status_code == 400


def test_list_servers(client: TestClient):
    """Test listing servers"""
    response = client.get("/api/v1/servers/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "servers" in data
    assert isinstance(data["servers"], list)
