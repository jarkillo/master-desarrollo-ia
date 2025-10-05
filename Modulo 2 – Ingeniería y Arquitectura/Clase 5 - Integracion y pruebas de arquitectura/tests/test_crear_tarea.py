from fastapi.testclient import TestClient
from api import api as api_mod  # accedemos al módulo, no solo al app
from api.servicio_tareas import ServicioTareas
from api.repositorio_memoria import RepositorioMemoria


def test_crear_tarea_minima_devuelve_201_y_cuerpo_esperado():
    # 1. Resetear el servicio a uno limpio
    api_mod.servicio = ServicioTareas(RepositorioMemoria())
    # 2. Crear el cliente justo después
    cliente = TestClient(api_mod.app)

    respuesta_con_nombre = cliente.post("/tareas", json={"nombre": "Estudiar SOLID"})
    assert respuesta_con_nombre.status_code == 201
    cuerpo = respuesta_con_nombre.json()
    assert cuerpo["id"] == 1
    assert cuerpo["nombre"] == "Estudiar SOLID"
    assert cuerpo["completada"] is False


def test_crear_tarea_con_nombre_vacio_devuelve_422():
    api_mod.servicio = ServicioTareas(RepositorioMemoria())
    cliente = TestClient(api_mod.app)

    respuesta_con_nombre_vacio = cliente.post("/tareas", json={"nombre": ""})
    assert respuesta_con_nombre_vacio.status_code == 422
