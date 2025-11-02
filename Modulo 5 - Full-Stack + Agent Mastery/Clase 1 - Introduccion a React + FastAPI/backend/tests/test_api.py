# tests/test_api.py
from api.api import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root_endpoint():
    """Test del endpoint raíz (health check)."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_crear_tarea():
    """Test de creación de una tarea."""
    response = client.post("/tareas", json={"nombre": "Test tarea"})
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Test tarea"
    assert data["completada"] is False
    assert "id" in data


def test_crear_tarea_nombre_vacio():
    """Test de validación: no se puede crear tarea con nombre vacío."""
    response = client.post("/tareas", json={"nombre": ""})
    assert response.status_code == 422


def test_listar_tareas():
    """Test de listado de tareas."""
    # Limpiar estado creando un nuevo cliente
    response = client.get("/tareas")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_obtener_tarea():
    """Test de obtención de tarea por ID."""
    # Crear una tarea primero
    create_response = client.post("/tareas", json={"nombre": "Tarea para obtener"})
    tarea_id = create_response.json()["id"]

    # Obtener la tarea
    response = client.get(f"/tareas/{tarea_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == tarea_id
    assert data["nombre"] == "Tarea para obtener"


def test_obtener_tarea_inexistente():
    """Test: obtener tarea que no existe retorna 404."""
    response = client.get("/tareas/9999")
    assert response.status_code == 404


def test_actualizar_tarea():
    """Test de actualización de estado de tarea."""
    # Crear una tarea primero
    create_response = client.post("/tareas", json={"nombre": "Tarea para actualizar"})
    tarea_id = create_response.json()["id"]

    # Marcar como completada
    response = client.patch(f"/tareas/{tarea_id}", json={"completada": True})
    assert response.status_code == 200
    data = response.json()
    assert data["completada"] is True


def test_actualizar_tarea_inexistente():
    """Test: actualizar tarea que no existe retorna 404."""
    response = client.patch("/tareas/9999", json={"completada": True})
    assert response.status_code == 404


def test_eliminar_tarea():
    """Test de eliminación de tarea."""
    # Crear una tarea primero
    create_response = client.post("/tareas", json={"nombre": "Tarea para eliminar"})
    tarea_id = create_response.json()["id"]

    # Eliminar la tarea
    response = client.delete(f"/tareas/{tarea_id}")
    assert response.status_code == 204

    # Verificar que ya no existe
    get_response = client.get(f"/tareas/{tarea_id}")
    assert get_response.status_code == 404


def test_eliminar_tarea_inexistente():
    """Test: eliminar tarea que no existe retorna 404."""
    response = client.delete("/tareas/9999")
    assert response.status_code == 404


def test_cors_headers():
    """Test de configuración CORS."""
    response = client.options("/tareas", headers={"Origin": "http://localhost:5173"})
    # CORS debe estar configurado para permitir requests desde el frontend
    assert response.status_code == 200
