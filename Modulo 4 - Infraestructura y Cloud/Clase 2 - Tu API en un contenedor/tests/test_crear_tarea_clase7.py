# al inicio del archivo
import os

# IMPORTANTE: Configurar JWT_SECRET ANTES de importar la API
os.environ["JWT_SECRET"] = "secret-test"

from fastapi.testclient import TestClient
from api import api as api_mod
from api.servicio_tareas import ServicioTareas
from api.repositorio_memoria import RepositorioMemoria


def _cliente_y_headers():
    # Resetear servicio para cada test (aislamiento)
    api_mod.servicio = ServicioTareas(RepositorioMemoria())
    c = TestClient(api_mod.app)
    token = c.post("/login", json={"usuario": "demo", "password": "demo"}).json()[
        "access_token"
    ]
    return c, {"Authorization": f"Bearer {token}"}


def test_crear_tarea_minima_devuelve_201_y_cuerpo_esperado():
    c, h = _cliente_y_headers()
    r = c.post("/tareas", json={"nombre": "Estudiar SOLID"}, headers=h)
    assert r.status_code == 201
    cuerpo = r.json()
    assert cuerpo["id"] == 1
    assert cuerpo["nombre"] == "Estudiar SOLID"
    assert cuerpo["completada"] is False


def test_crear_tarea_con_nombre_vacio_devuelve_422():
    c, h = _cliente_y_headers()
    r = c.post("/tareas", json={"nombre": ""}, headers=h)
    assert r.status_code == 422
