import os
import tempfile
from fastapi.testclient import TestClient
from api import api as api_mod
from api.servicio_tareas import ServicioTareas
from api.repositorio_json import RepositorioJSON


def test_crear_tarea_con_repositorio_json_temporal():
    os.environ["JWT_SECRET"] = "secret-test"
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    try:
        api_mod.servicio = ServicioTareas(RepositorioJSON(tmp.name))
        c = TestClient(api_mod.app)

        token = c.post("/login", json={"usuario": "demo", "password": "demo"}).json()[
            "access_token"
        ]
        h = {"Authorization": f"Bearer {token}"}

        r = c.post("/tareas", json={"nombre": "Aprender tests con IA"}, headers=h)
        assert r.status_code == 201
        cuerpo = r.json()
        assert cuerpo["id"] == 1
        assert cuerpo["nombre"] == "Aprender tests con IA"
        assert cuerpo["completada"] is False
    finally:
        os.remove(tmp.name)
