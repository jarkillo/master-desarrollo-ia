# tests/test_api_clase5.py
"""
Tests para la API REST optimizada para cloud.

Tests específicos de Clase 5:
- Health checks (/ y /health)
- CRUD básico con SQLAlchemy
- Validación de Pydantic
- Status codes correctos
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.api import app
from api.database import get_db
from api.models import Base


# Database de pruebas (en memoria)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def test_db():
    """
    Crea una base de datos limpia para cada test.

    Yields:
        Session de prueba
    """
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """
    Cliente de prueba de FastAPI con DB de prueba inyectada.

    Args:
        test_db: Session de prueba

    Yields:
        TestClient configurado
    """
    def override_get_db():
        # Crear nueva sesión para cada request
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ==============================================================================
# HEALTH CHECKS (Específico de Clase 5)
# ==============================================================================

def test_root_endpoint(client):
    """
    Test del endpoint raíz (/).

    Railway y Render usan este endpoint para health checks básicos.
    """
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert "message" in data
    assert "environment" in data
    assert "version" in data


def test_health_check_endpoint(client):
    """
    Test del health check completo (/health).

    Verifica que tanto la API como la base de datos están funcionando.
    """
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["api"] == "ok"
    assert "database" in data
    assert data["database"]["status"] == "ok"


# ==============================================================================
# CRUD TESTS
# ==============================================================================

def test_crear_tarea_exitosa(client):
    """Test de creación de tarea"""
    response = client.post(
        "/tareas",
        json={"nombre": "Tarea de prueba"}
    )
    assert response.status_code == 201

    data = response.json()
    assert data["nombre"] == "Tarea de prueba"
    assert data["completada"] is False
    assert "id" in data
    assert data["id"] > 0


def test_crear_tarea_nombre_vacio_falla(client):
    """Test de validación: nombre vacío debe fallar"""
    response = client.post(
        "/tareas",
        json={"nombre": ""}
    )
    assert response.status_code == 422  # Validation Error


def test_listar_tareas_vacia(client):
    """Test de listado cuando no hay tareas"""
    response = client.get("/tareas")
    assert response.status_code == 200
    assert response.json() == []


def test_listar_tareas_con_datos(client):
    """Test de listado con tareas existentes"""
    # Crear 3 tareas
    client.post("/tareas", json={"nombre": "Tarea 1"})
    client.post("/tareas", json={"nombre": "Tarea 2"})
    client.post("/tareas", json={"nombre": "Tarea 3"})

    response = client.get("/tareas")
    assert response.status_code == 200

    tareas = response.json()
    assert len(tareas) == 3
    assert tareas[0]["nombre"] == "Tarea 1"


def test_obtener_tarea_existente(client):
    """Test de obtención de tarea por ID"""
    # Crear tarea
    create_response = client.post(
        "/tareas",
        json={"nombre": "Tarea a obtener"}
    )
    tarea_id = create_response.json()["id"]

    # Obtener tarea
    response = client.get(f"/tareas/{tarea_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == tarea_id
    assert data["nombre"] == "Tarea a obtener"


def test_obtener_tarea_inexistente(client):
    """Test de obtención de tarea que no existe"""
    response = client.get("/tareas/999")
    assert response.status_code == 404
    assert "no encontrada" in response.json()["detail"]


def test_actualizar_tarea_exitosa(client):
    """Test de actualización de tarea"""
    # Crear tarea
    create_response = client.post(
        "/tareas",
        json={"nombre": "Tarea original"}
    )
    tarea_id = create_response.json()["id"]

    # Actualizar tarea
    response = client.put(
        f"/tareas/{tarea_id}",
        json={"nombre": "Tarea modificada", "completada": True}
    )
    assert response.status_code == 200

    data = response.json()
    assert data["nombre"] == "Tarea modificada"
    assert data["completada"] is True


def test_actualizar_tarea_inexistente(client):
    """Test de actualización de tarea que no existe"""
    response = client.put(
        "/tareas/999",
        json={"nombre": "No existe"}
    )
    assert response.status_code == 404


def test_eliminar_tarea_exitosa(client):
    """Test de eliminación de tarea"""
    # Crear tarea
    create_response = client.post(
        "/tareas",
        json={"nombre": "Tarea a eliminar"}
    )
    tarea_id = create_response.json()["id"]

    # Eliminar tarea
    response = client.delete(f"/tareas/{tarea_id}")
    assert response.status_code == 204

    # Verificar que ya no existe
    get_response = client.get(f"/tareas/{tarea_id}")
    assert get_response.status_code == 404


def test_eliminar_tarea_inexistente(client):
    """Test de eliminación de tarea que no existe"""
    response = client.delete("/tareas/999")
    assert response.status_code == 404


# ==============================================================================
# VALIDACIONES PYDANTIC (Clase 5 específico)
# ==============================================================================

def test_validacion_nombre_muy_largo(client):
    """Test de validación: nombre >100 caracteres debe fallar"""
    nombre_largo = "a" * 101
    response = client.post(
        "/tareas",
        json={"nombre": nombre_largo}
    )
    assert response.status_code == 422


def test_validacion_json_invalido(client):
    """Test de validación: JSON inválido debe fallar"""
    response = client.post(
        "/tareas",
        data="esto no es json",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422


# ==============================================================================
# CORS (Clase 5 específico)
# ==============================================================================

def test_cors_headers_present(client):
    """
    Test de CORS headers.

    Verifica que la API incluye headers CORS necesarios para
    permitir requests desde frontends en otros dominios.
    """
    response = client.get(
        "/tareas",
        headers={"Origin": "https://mi-frontend.com"}
    )
    assert response.status_code == 200

    # CORS headers presentes
    assert "access-control-allow-origin" in response.headers
