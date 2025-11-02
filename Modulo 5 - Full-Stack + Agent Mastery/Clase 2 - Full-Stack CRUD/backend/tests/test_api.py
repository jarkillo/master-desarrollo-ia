"""
Tests de integración para la API de tareas.
"""
import pytest
from api.api import app, repositorio
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def reset_repositorio():
    """Reinicia el estado del repositorio antes de cada test."""
    repositorio._tareas.clear()
    repositorio._siguiente_id = 1
    yield


@pytest.fixture
def client():
    """Cliente de pruebas para la API."""
    return TestClient(app)


def test_health_check(client):
    """Test del endpoint de health check."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["version"] == "2.0.0"


def test_crear_tarea(client):
    """Test de creación de tarea."""
    response = client.post("/tareas", json={"nombre": "Tarea de prueba"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["nombre"] == "Tarea de prueba"
    assert data["completada"] is False


def test_crear_tarea_nombre_vacio(client):
    """Test de validación con nombre vacío."""
    response = client.post("/tareas", json={"nombre": "   "})
    assert response.status_code == 400
    assert "no puede estar vacío" in response.json()["detail"]


def test_crear_tarea_nombre_muy_largo(client):
    """Test de validación con nombre muy largo."""
    nombre_largo = "a" * 201
    response = client.post("/tareas", json={"nombre": nombre_largo})
    assert response.status_code == 422  # Pydantic validation


def test_listar_tareas(client):
    """Test de listado de tareas."""
    # Crear algunas tareas
    client.post("/tareas", json={"nombre": "Tarea 1"})
    client.post("/tareas", json={"nombre": "Tarea 2"})

    # Listar
    response = client.get("/tareas")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert data[0]["nombre"] == "Tarea 1"
    assert data[1]["nombre"] == "Tarea 2"


def test_obtener_tarea(client):
    """Test de obtener tarea específica."""
    # Crear tarea
    create_response = client.post("/tareas", json={"nombre": "Tarea específica"})
    tarea_id = create_response.json()["id"]

    # Obtener
    response = client.get(f"/tareas/{tarea_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == tarea_id
    assert data["nombre"] == "Tarea específica"


def test_obtener_tarea_no_existe(client):
    """Test de obtener tarea que no existe."""
    response = client.get("/tareas/9999")
    assert response.status_code == 404
    assert "no encontrada" in response.json()["detail"]


def test_actualizar_tarea_nombre(client):
    """Test de actualizar nombre de tarea."""
    # Crear tarea
    create_response = client.post("/tareas", json={"nombre": "Nombre original"})
    tarea_id = create_response.json()["id"]

    # Actualizar nombre
    response = client.patch(
        f"/tareas/{tarea_id}",
        json={"nombre": "Nombre actualizado"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Nombre actualizado"
    assert data["completada"] is False


def test_actualizar_tarea_completada(client):
    """Test de marcar tarea como completada."""
    # Crear tarea
    create_response = client.post("/tareas", json={"nombre": "Tarea pendiente"})
    tarea_id = create_response.json()["id"]

    # Marcar como completada
    response = client.patch(
        f"/tareas/{tarea_id}",
        json={"completada": True}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["completada"] is True
    assert data["nombre"] == "Tarea pendiente"


def test_actualizar_tarea_parcial(client):
    """Test de actualización parcial (solo un campo)."""
    # Crear tarea
    create_response = client.post("/tareas", json={"nombre": "Tarea original"})
    tarea_id = create_response.json()["id"]

    # Actualizar solo completada
    response = client.patch(
        f"/tareas/{tarea_id}",
        json={"completada": True}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["completada"] is True
    assert data["nombre"] == "Tarea original"  # Nombre no cambió


def test_actualizar_tarea_no_existe(client):
    """Test de actualizar tarea que no existe."""
    response = client.patch(
        "/tareas/9999",
        json={"nombre": "Nuevo nombre"}
    )
    assert response.status_code == 404


def test_actualizar_tarea_vacio(client):
    """Test de validación: PATCH vacío debe fallar."""
    # Crear tarea
    tarea = client.post("/tareas", json={"nombre": "Tarea inicial"})
    tarea_id = tarea.json()["id"]

    # Intentar actualizar sin campos
    response = client.patch(f"/tareas/{tarea_id}", json={})
    assert response.status_code == 400
    assert "al menos un campo" in response.json()["detail"].lower()


def test_eliminar_tarea(client):
    """Test de eliminar tarea."""
    # Crear tarea
    create_response = client.post("/tareas", json={"nombre": "Tarea a eliminar"})
    tarea_id = create_response.json()["id"]

    # Eliminar
    response = client.delete(f"/tareas/{tarea_id}")
    assert response.status_code == 204

    # Verificar que no existe
    get_response = client.get(f"/tareas/{tarea_id}")
    assert get_response.status_code == 404


def test_eliminar_tarea_no_existe(client):
    """Test de eliminar tarea que no existe."""
    response = client.delete("/tareas/9999")
    assert response.status_code == 404


def test_estadisticas(client):
    """Test del endpoint de estadísticas."""
    # Crear algunas tareas
    client.post("/tareas", json={"nombre": "Tarea 1"})
    tarea2 = client.post("/tareas", json={"nombre": "Tarea 2"})
    client.post("/tareas", json={"nombre": "Tarea 3"})

    # Marcar una como completada
    tarea2_id = tarea2.json()["id"]
    client.patch(f"/tareas/{tarea2_id}", json={"completada": True})

    # Obtener estadísticas
    response = client.get("/tareas/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 3
    assert data["completadas"] >= 1
    assert data["pendientes"] >= 2


def test_flujo_completo_crud(client):
    """Test de flujo completo CRUD."""
    # 1. Crear
    create_response = client.post("/tareas", json={"nombre": "Tarea CRUD"})
    assert create_response.status_code == 201
    tarea_id = create_response.json()["id"]

    # 2. Leer (obtener específica)
    get_response = client.get(f"/tareas/{tarea_id}")
    assert get_response.status_code == 200
    assert get_response.json()["nombre"] == "Tarea CRUD"

    # 3. Actualizar
    update_response = client.patch(
        f"/tareas/{tarea_id}",
        json={"nombre": "Tarea CRUD actualizada", "completada": True}
    )
    assert update_response.status_code == 200
    assert update_response.json()["nombre"] == "Tarea CRUD actualizada"
    assert update_response.json()["completada"] is True

    # 4. Eliminar
    delete_response = client.delete(f"/tareas/{tarea_id}")
    assert delete_response.status_code == 204

    # 5. Verificar eliminación
    get_deleted = client.get(f"/tareas/{tarea_id}")
    assert get_deleted.status_code == 404
