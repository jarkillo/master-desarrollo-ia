# tests/test_health.py
"""Tests para el endpoint de health check"""

from fastapi.testclient import TestClient
from api.api import app

client = TestClient(app)


def test_health_check_devuelve_200():
    """
    Given: La API está corriendo
    When: Hago GET /health
    Then: Responde HTTP 200 con status "ok"
    """
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "message" in data
