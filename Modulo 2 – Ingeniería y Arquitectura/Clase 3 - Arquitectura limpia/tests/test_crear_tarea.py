from fastapi.testclient import TestClient
from api.api import app

cliente_http = TestClient(app)


def test_crear_tarea_minima_devuelve_201_y_cuerpo_esperado():
    cuerpo_peticion = {"nombre": "Estudiar SOLID"}
    respuesta = cliente_http.post("/tareas", json=cuerpo_peticion)
    assert respuesta.status_code == 201

    cuerpo_respuesta = respuesta.json()
    assert cuerpo_respuesta["id"] == 1
    assert cuerpo_respuesta["nombre"] == "Estudiar SOLID"
    assert cuerpo_respuesta["completada"] is False


def test_crear_tarea_con_nombre_vacio_devuelve_422():
    respuesta = cliente_http.post("/tareas", json={"nombre": ""})
    assert respuesta.status_code == 422
