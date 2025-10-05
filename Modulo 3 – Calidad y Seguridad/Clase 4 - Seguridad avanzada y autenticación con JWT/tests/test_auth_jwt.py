# tests/test_auth_jwt.py
import os
import time
from fastapi.testclient import TestClient
from api import api as api_mod
from api.servicio_tareas import ServicioTareas
from api.repositorio_memoria import RepositorioMemoria


def _cliente():
    # Inyecta repo limpio en cada test
    api_mod.servicio = ServicioTareas(RepositorioMemoria())
    return TestClient(api_mod.app)


def test_login_devuelve_token():
    os.environ["JWT_SECRET"] = "secret-test"
    c = _cliente()
    r = c.post("/login", json={"usuario": "demo", "password": "demo"})
    assert r.status_code == 200
    cuerpo = r.json()
    assert "access_token" in cuerpo
    assert cuerpo["token_type"] == "bearer"


def test_acceso_protegido_con_token():
    os.environ["JWT_SECRET"] = "secret-test"
    c = _cliente()
    token = c.post("/login", json={"usuario": "demo", "password": "demo"}).json()[
        "access_token"
    ]
    r = c.post(
        "/tareas",
        json={"nombre": "Estudiar JWT"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 201


def test_token_invalido_da_401():
    os.environ["JWT_SECRET"] = "secret-test"
    c = _cliente()
    r = c.get("/tareas", headers={"Authorization": "Bearer chorizo"})
    assert r.status_code == 401


def test_token_expirado_da_401(monkeypatch):
    os.environ["JWT_SECRET"] = "secret-test"
    os.environ["JWT_MINUTOS"] = "0"  # forzamos expiración inmediata
    c = _cliente()
    token = c.post("/login", json={"usuario": "demo", "password": "demo"}).json()[
        "access_token"
    ]
    # pequeña espera para vencerlo (cero minutos ⇒ exp en pasado inmediato)
    time.sleep(1)
    r = c.get("/tareas", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401
