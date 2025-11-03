"""
Fixtures compartidos para tests.

Configura:
- Base de datos de testing (SQLite in-memory)
- Cliente de testing de FastAPI
- Fixtures de usuarios y tareas
"""

import sys
from pathlib import Path

# Agregar el directorio padre al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.api import app
from api.database import get_db
from api.models import Base, TareaModel, UsuarioModel
from api.seguridad_jwt import crear_access_token, hash_password

# ============================================================================
# DATABASE FIXTURES
# ============================================================================

@pytest.fixture(scope="function")
def test_db():
    """
    Crea una base de datos SQLite en memoria para cada test.

    Yields:
        Session de SQLAlchemy
    """
    # Crear engine de testing (SQLite in-memory)
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)

    # Crear session factory
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    # Crear sesión
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """
    Cliente de testing de FastAPI con BD de testing.

    Args:
        test_db: Fixture de base de datos de testing

    Yields:
        TestClient de FastAPI
    """
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# ============================================================================
# USER FIXTURES
# ============================================================================

@pytest.fixture
def usuario_test(test_db):
    """
    Crea un usuario de prueba en la BD.

    Returns:
        UsuarioModel creado
    """
    usuario = UsuarioModel(
        email="test@example.com",
        nombre="Usuario Test",
        password_hash=hash_password("password123"),
        activo=True
    )
    test_db.add(usuario)
    test_db.commit()
    test_db.refresh(usuario)
    return usuario


@pytest.fixture
def usuario2_test(test_db):
    """
    Crea un segundo usuario de prueba (para tests de aislamiento).

    Returns:
        UsuarioModel creado
    """
    usuario = UsuarioModel(
        email="test2@example.com",
        nombre="Usuario Test 2",
        password_hash=hash_password("password456"),
        activo=True
    )
    test_db.add(usuario)
    test_db.commit()
    test_db.refresh(usuario)
    return usuario


@pytest.fixture
def token_test(usuario_test):
    """
    Genera un token JWT válido para el usuario de prueba.

    Args:
        usuario_test: Fixture del usuario

    Returns:
        Token JWT string
    """
    return crear_access_token(
        email=usuario_test.email,
        user_id=usuario_test.id
    )


@pytest.fixture
def auth_headers(token_test):
    """
    Headers de autenticación para requests.

    Args:
        token_test: Token JWT

    Returns:
        Dict con headers de autorización
    """
    return {"Authorization": f"Bearer {token_test}"}


# ============================================================================
# TAREA FIXTURES
# ============================================================================

@pytest.fixture
def tarea_test(test_db, usuario_test):
    """
    Crea una tarea de prueba.

    Returns:
        TareaModel creada
    """
    tarea = TareaModel(
        titulo="Tarea de prueba",
        descripcion="Descripción de prueba",
        completada=False,
        prioridad=2,
        usuario_id=usuario_test.id,
        eliminada=False
    )
    test_db.add(tarea)
    test_db.commit()
    test_db.refresh(tarea)
    return tarea


@pytest.fixture
def tareas_multiples(test_db, usuario_test):
    """
    Crea múltiples tareas con diferentes estados.

    Returns:
        List de TareaModel
    """
    tareas = [
        TareaModel(
            titulo="Tarea 1 - Alta prioridad",
            prioridad=3,
            completada=False,
            usuario_id=usuario_test.id,
            eliminada=False
        ),
        TareaModel(
            titulo="Tarea 2 - Completada",
            prioridad=2,
            completada=True,
            usuario_id=usuario_test.id,
            eliminada=False
        ),
        TareaModel(
            titulo="Tarea 3 - Baja prioridad",
            prioridad=1,
            completada=False,
            usuario_id=usuario_test.id,
            eliminada=False
        ),
        TareaModel(
            titulo="Tarea 4 - Eliminada",
            prioridad=2,
            completada=False,
            usuario_id=usuario_test.id,
            eliminada=True
        ),
    ]

    for tarea in tareas:
        test_db.add(tarea)

    test_db.commit()

    for tarea in tareas:
        test_db.refresh(tarea)

    return tareas
