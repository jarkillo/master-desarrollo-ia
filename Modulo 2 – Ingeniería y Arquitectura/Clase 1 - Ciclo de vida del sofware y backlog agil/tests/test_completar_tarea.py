# tests/test_completar_tarea.py
"""Tests para el endpoint de completar tareas"""

from api.api import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_completar_tarea_existente_devuelve_200():
    """
    Given: Existe una tarea sin completar
    When: Hago PATCH /tareas/{id}/completar
    Then: Responde 200 y la tarea tiene completada=True
    """
    # Arrange: Crear tarea
    response_crear = client.post("/tareas", json={"nombre": "Tarea a completar"})
    tarea_id = response_crear.json()["id"]

    # Act: Completar la tarea
    response = client.patch(f"/tareas/{tarea_id}/completar")

    # Assert
    assert response.status_code == 200
    tarea = response.json()
    assert tarea["id"] == tarea_id
    assert tarea["completada"] is True


def test_completar_tarea_inexistente_devuelve_404():
    """
    Given: No existe tarea con id=9999
    When: Intento completarla
    Then: Responde 404
    """
    response = client.patch("/tareas/9999/completar")
    assert response.status_code == 404
