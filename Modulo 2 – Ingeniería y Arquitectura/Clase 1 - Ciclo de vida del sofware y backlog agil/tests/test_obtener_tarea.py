# tests/test_obtener_tarea.py
"""Tests para el endpoint de obtener tarea por ID"""

from fastapi.testclient import TestClient
from api.api import app

client = TestClient(app)


def test_obtener_tarea_existente_devuelve_200_y_tarea():
    """
    Given: Existe una tarea con id específico
    When: Hago GET /tareas/{id}
    Then: Responde HTTP 200 con la tarea completa
    """
    # Arrange: Crear una tarea primero
    response_crear = client.post("/tareas", json={"nombre": "Test tarea para obtener"})
    tarea_id = response_crear.json()["id"]

    # Act: Obtener la tarea
    response = client.get(f"/tareas/{tarea_id}")

    # Assert
    assert response.status_code == 200
    tarea = response.json()
    assert tarea["id"] == tarea_id
    assert tarea["nombre"] == "Test tarea para obtener"
    assert tarea["completada"] is False


def test_obtener_tarea_inexistente_devuelve_404():
    """
    Given: No existe tarea con id=9999
    When: Hago GET /tareas/9999
    Then: Responde HTTP 404 con mensaje de error
    """
    response = client.get("/tareas/9999")

    assert response.status_code == 404
    assert "detail" in response.json()
