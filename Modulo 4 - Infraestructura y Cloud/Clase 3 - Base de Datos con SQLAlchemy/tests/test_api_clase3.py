# tests/test_api_clase3.py
"""
Tests de la API usando SQLAlchemy.

Tests unitarios que usan TestClient de FastAPI.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.api import app
from api.models import Base
from api.database import get_db
from api.repositorio_db import RepositorioDB
from api.servicio_tareas import ServicioTareas
from api.dependencias import get_servicio


# Base de datos en memoria para tests (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    """
    Fixture que crea/limpia la BD antes de cada test.

    autouse=True hace que se ejecute automáticamente.
    """
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    yield
    # Limpiar después del test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Proporciona una sesión de BD para tests"""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def test_servicio(db_session):
    """Proporciona un servicio configurado para tests"""
    repo = RepositorioDB(session=db_session)
    return ServicioTareas(repositorio=repo)


@pytest.fixture
def client(test_servicio):
    """
    Cliente de prueba con override de dependencias.

    Usa la BD de test en lugar de la real.
    """
    def override_get_servicio():
        return test_servicio

    app.dependency_overrides[get_servicio] = override_get_servicio
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# ============================================================================
# TESTS
# ============================================================================

def test_health_check(client):
    """Test del endpoint de health check"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_crear_tarea_success(client):
    """Test de creación exitosa de tarea"""
    response = client.post("/tareas", json={"nombre": "Tarea de prueba"})

    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Tarea de prueba"
    assert data["completada"] is False
    assert "id" in data
    assert data["id"] > 0


def test_crear_tarea_nombre_vacio(client):
    """Test de validación: nombre vacío debe fallar"""
    response = client.post("/tareas", json={"nombre": ""})
    assert response.status_code == 422  # Unprocessable Entity


def test_crear_tarea_nombre_muy_largo(client):
    """Test de validación: nombre muy largo debe fallar"""
    nombre_largo = "a" * 101  # Máximo es 100
    response = client.post("/tareas", json={"nombre": nombre_largo})
    assert response.status_code == 422


def test_listar_tareas_vacio(client):
    """Test de listar cuando no hay tareas"""
    response = client.get("/tareas")
    assert response.status_code == 200
    assert response.json() == []


def test_listar_tareas_con_datos(client):
    """Test de listar con tareas existentes"""
    # Crear 3 tareas
    client.post("/tareas", json={"nombre": "Tarea 1"})
    client.post("/tareas", json={"nombre": "Tarea 2"})
    client.post("/tareas", json={"nombre": "Tarea 3"})

    # Listar
    response = client.get("/tareas")
    assert response.status_code == 200
    tareas = response.json()
    assert len(tareas) == 3
    assert tareas[0]["nombre"] == "Tarea 1"


def test_obtener_tarea_existente(client):
    """Test de obtener una tarea por ID"""
    # Crear tarea
    create_response = client.post("/tareas", json={"nombre": "Mi tarea"})
    tarea_id = create_response.json()["id"]

    # Obtener
    response = client.get(f"/tareas/{tarea_id}")
    assert response.status_code == 200
    assert response.json()["nombre"] == "Mi tarea"


def test_obtener_tarea_no_existente(client):
    """Test de obtener tarea que no existe"""
    response = client.get("/tareas/999")
    assert response.status_code == 404
    assert "no encontrada" in response.json()["detail"]


def test_actualizar_tarea_nombre(client):
    """Test de actualizar el nombre de una tarea"""
    # Crear tarea
    create_response = client.post("/tareas", json={"nombre": "Nombre original"})
    tarea_id = create_response.json()["id"]

    # Actualizar nombre
    response = client.put(
        f"/tareas/{tarea_id}",
        json={"nombre": "Nombre actualizado"}
    )
    assert response.status_code == 200
    assert response.json()["nombre"] == "Nombre actualizado"


def test_actualizar_tarea_completada(client):
    """Test de marcar tarea como completada"""
    # Crear tarea
    create_response = client.post("/tareas", json={"nombre": "Por completar"})
    tarea_id = create_response.json()["id"]

    # Marcar como completada
    response = client.put(
        f"/tareas/{tarea_id}",
        json={"completada": True}
    )
    assert response.status_code == 200
    assert response.json()["completada"] is True


def test_actualizar_tarea_no_existente(client):
    """Test de actualizar tarea que no existe"""
    response = client.put(
        "/tareas/999",
        json={"nombre": "No importa"}
    )
    assert response.status_code == 404


def test_eliminar_tarea_existente(client):
    """Test de eliminar una tarea"""
    # Crear tarea
    create_response = client.post("/tareas", json={"nombre": "A eliminar"})
    tarea_id = create_response.json()["id"]

    # Eliminar
    response = client.delete(f"/tareas/{tarea_id}")
    assert response.status_code == 204

    # Verificar que ya no existe
    get_response = client.get(f"/tareas/{tarea_id}")
    assert get_response.status_code == 404


def test_eliminar_tarea_no_existente(client):
    """Test de eliminar tarea que no existe"""
    response = client.delete("/tareas/999")
    assert response.status_code == 404


def test_flujo_completo_crud(client):
    """Test de flujo completo: crear, leer, actualizar, eliminar"""
    # 1. Crear
    response = client.post("/tareas", json={"nombre": "Flujo CRUD"})
    assert response.status_code == 201
    tarea_id = response.json()["id"]

    # 2. Leer
    response = client.get(f"/tareas/{tarea_id}")
    assert response.status_code == 200
    assert response.json()["completada"] is False

    # 3. Actualizar
    response = client.put(
        f"/tareas/{tarea_id}",
        json={"completada": True}
    )
    assert response.status_code == 200
    assert response.json()["completada"] is True

    # 4. Eliminar
    response = client.delete(f"/tareas/{tarea_id}")
    assert response.status_code == 204

    # 5. Verificar eliminación
    response = client.get(f"/tareas/{tarea_id}")
    assert response.status_code == 404
