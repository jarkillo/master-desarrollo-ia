import os

from api import api as api_mod  # accedemos al módulo, no solo al app
from api.repositorio_memoria import RepositorioMemoria
from api.servicio_tareas import ServicioTareas
from fastapi.testclient import TestClient


def test_crear_tarea_minima_devuelve_201_y_cuerpo_esperado():
    os.environ["API_KEY"] = "test-key"  # 1) fijar clave
    api_mod.servicio = ServicioTareas(RepositorioMemoria())
    cliente = TestClient(api_mod.app)

    r = cliente.post(
        "/tareas",
        json={"nombre": "Estudiar SOLID"},
        headers={"x-api-key": "test-key"},  # 2) mandar cabecera
    )
    assert r.status_code == 201
    cuerpo = r.json()
    assert cuerpo["id"] == 1
    assert cuerpo["nombre"] == "Estudiar SOLID"
    assert cuerpo["completada"] is False


def test_crear_tarea_con_nombre_vacio_devuelve_422():
    api_mod.servicio = ServicioTareas(RepositorioMemoria())
    cliente = TestClient(api_mod.app)

    respuesta_con_nombre_vacio = cliente.post("/tareas", json={"nombre": ""})
    assert respuesta_con_nombre_vacio.status_code == 422
