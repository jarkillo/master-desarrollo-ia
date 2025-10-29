# tests/test_crear_tarea_json.py
import tempfile
import os

# IMPORTANTE: Configurar JWT_SECRET ANTES de importar módulos que lo usen
os.environ["JWT_SECRET"] = "secret-test"

from fastapi.testclient import TestClient
from api import api as api_mod
from api.servicio_tareas import ServicioTareas
from api.repositorio_json import RepositorioJSON


def test_crear_tarea_con_repositorio_json_temporal():
    # Crear archivo temporal vacío
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()

    try:
        # Inyectar el servicio con RepositorioJSON usando el archivo temporal
        api_mod.servicio = ServicioTareas(RepositorioJSON(tmp.name))

        # Lanzar cliente HTTP contra la API
        cliente = TestClient(api_mod.app)
        r = cliente.post("/tareas", json={"nombre": "Aprender tests con IA"})

        # Verificar respuesta
        assert r.status_code == 201
        tarea = r.json()
        assert tarea["id"] == 1
        assert tarea["nombre"] == "Aprender tests con IA"
        assert tarea["completada"] is False

    finally:
        # Borrar archivo después del test
        os.remove(tmp.name)
