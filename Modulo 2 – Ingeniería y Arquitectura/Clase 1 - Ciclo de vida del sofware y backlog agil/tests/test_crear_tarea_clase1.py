# tests/test_crear_tarea_clase1.py
"""Tests para el endpoint de crear tareas"""

from fastapi.testclient import TestClient
from api.api import app

client = TestClient(app)


def test_crear_tarea_minima_devuelve_201_y_cuerpo_esperado():
    """
    Given: Envío datos válidos para crear una tarea
    When: Hago POST /tareas con nombre válido
    Then: Responde HTTP 201 con la tarea creada
    """
    cuerpo_peticion = {"nombre": "Estudiar SOLID"}
    response = client.post("/tareas", json=cuerpo_peticion)

    assert response.status_code == 201

    cuerpo_respuesta = response.json()
    assert cuerpo_respuesta["nombre"] == "Estudiar SOLID"
    assert cuerpo_respuesta["completada"] is False
    assert "id" in cuerpo_respuesta


def test_crear_tarea_con_nombre_vacio_devuelve_422():
    """
    Given: Envío datos inválidos (nombre vacío)
    When: Hago POST /tareas con nombre vacío
    Then: Responde HTTP 422 (error de validación)
    """
    response = client.post("/tareas", json={"nombre": ""})
    assert response.status_code == 422


def test_crear_tarea_con_descripcion_devuelve_201():
    """
    Given: Envío tarea con nombre y descripción
    When: Hago POST /tareas
    Then: Responde HTTP 201 con ambos campos
    """
    cuerpo = {
        "nombre": "Aprender FastAPI",
        "descripcion": "Completar la Clase 1 del Módulo 2"
    }
    response = client.post("/tareas", json=cuerpo)

    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Aprender FastAPI"
    assert data["descripcion"] == "Completar la Clase 1 del Módulo 2"


def test_listar_tareas_inicialmente_vacio():
    """
    Given: No hay tareas creadas
    When: Hago GET /tareas
    Then: Responde HTTP 200 con lista vacía o con tareas de tests anteriores
    """
    response = client.get("/tareas")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
