import os, tempfile
from fastapi.testclient import TestClient
from api import api as api_mod
from api.servicio_tareas import ServicioTareas
from api.repositorio_json import RepositorioJSON


def test_crear_tarea_con_repositorio_json_temporal():
    os.environ["API_KEY"] = "test-key"
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    try:
        api_mod.servicio = ServicioTareas(RepositorioJSON(tmp.name))
        cliente = TestClient(api_mod.app)

        r = cliente.post(
            "/tareas",
            json={"nombre": "Aprender tests con IA"},
            headers={"x-api-key": "test-key"},
        )

        assert r.status_code == 201
        cuerpo = r.json()
        assert cuerpo["id"] == 1
        assert cuerpo["nombre"] == "Aprender tests con IA"
        assert cuerpo["completada"] is False
    finally:
        os.remove(tmp.name)
