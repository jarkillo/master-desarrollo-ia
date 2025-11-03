"""
Tests de health check.
"""

from fastapi import status


def test_health_check_ok(client):
    """Test de health check exitoso."""
    response = client.get("/health")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "ok"
    assert data["environment"] in ["dev", "staging", "prod"]
    assert data["database"] in ["connected", "disconnected"]
    assert "timestamp" in data


def test_root_endpoint(client):
    """Test de endpoint raíz."""
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "nombre" in data
    assert "version" in data
    assert "entorno" in data
    assert "documentacion" in data
