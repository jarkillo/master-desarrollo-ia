# tests_integrations/test_integracion_repositorio_clase5.py
"""
Tests de integración para RepositorioDB.

Verifican que el repositorio funciona correctamente con
SQLAlchemy y base de datos real (SQLite en tests).
"""
import pytest
from api.models import Base, TareaModel
from api.repositorio_db import RepositorioDB
from api.servicio_tareas import Tarea
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database de pruebas (en memoria)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Crea una sesión de BD limpia para cada test.

    Yields:
        Session de SQLAlchemy
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def repositorio(db_session):
    """
    Crea una instancia del repositorio para tests.

    Args:
        db_session: Session de prueba

    Returns:
        RepositorioDB configurado
    """
    return RepositorioDB(session=db_session)


# ==============================================================================
# TESTS DE GUARDAR
# ==============================================================================

def test_guardar_tarea_nueva_asigna_id(repositorio, db_session):
    """Test: guardar tarea nueva asigna un ID automáticamente"""
    tarea = Tarea(id=0, nombre="Tarea nueva", completada=False)
    repositorio.guardar(tarea)

    assert tarea.id > 0  # ID asignado por la BD

    # Verificar que se guardó en la BD
    db_tarea = db_session.query(TareaModel).filter_by(id=tarea.id).first()
    assert db_tarea is not None
    assert db_tarea.nombre == "Tarea nueva"


def test_guardar_tarea_existente_actualiza(repositorio, db_session):
    """Test: guardar tarea existente actualiza sus datos"""
    # Crear tarea
    tarea = Tarea(id=0, nombre="Original", completada=False)
    repositorio.guardar(tarea)
    original_id = tarea.id

    # Modificar y guardar
    tarea.nombre = "Modificada"
    tarea.completada = True
    repositorio.guardar(tarea)

    # ID no cambia
    assert tarea.id == original_id

    # Datos actualizados en BD
    db_tarea = db_session.query(TareaModel).filter_by(id=original_id).first()
    assert db_tarea.nombre == "Modificada"
    assert db_tarea.completada is True


# ==============================================================================
# TESTS DE LISTAR
# ==============================================================================

def test_listar_sin_tareas_retorna_lista_vacia(repositorio):
    """Test: listar cuando no hay tareas retorna lista vacía"""
    tareas = repositorio.listar()
    assert tareas == []


def test_listar_retorna_todas_las_tareas(repositorio):
    """Test: listar retorna todas las tareas guardadas"""
    # Guardar 3 tareas
    tarea1 = Tarea(id=0, nombre="Tarea 1", completada=False)
    tarea2 = Tarea(id=0, nombre="Tarea 2", completada=True)
    tarea3 = Tarea(id=0, nombre="Tarea 3", completada=False)

    repositorio.guardar(tarea1)
    repositorio.guardar(tarea2)
    repositorio.guardar(tarea3)

    # Listar
    tareas = repositorio.listar()

    assert len(tareas) == 3
    assert tareas[0].nombre == "Tarea 1"
    assert tareas[1].nombre == "Tarea 2"
    assert tareas[2].nombre == "Tarea 3"


# ==============================================================================
# TESTS DE OBTENER POR ID
# ==============================================================================

def test_obtener_por_id_existente_retorna_tarea(repositorio):
    """Test: obtener por ID existente retorna la tarea"""
    # Guardar tarea
    tarea = Tarea(id=0, nombre="Tarea a buscar", completada=False)
    repositorio.guardar(tarea)

    # Obtener por ID
    encontrada = repositorio.obtener_por_id(tarea.id)

    assert encontrada is not None
    assert encontrada.id == tarea.id
    assert encontrada.nombre == "Tarea a buscar"


def test_obtener_por_id_inexistente_retorna_none(repositorio):
    """Test: obtener por ID inexistente retorna None"""
    tarea = repositorio.obtener_por_id(999)
    assert tarea is None


# ==============================================================================
# TESTS DE ACTUALIZAR
# ==============================================================================

def test_actualizar_tarea_existente_retorna_true(repositorio):
    """Test: actualizar tarea existente retorna True"""
    # Guardar tarea
    tarea = Tarea(id=0, nombre="Original", completada=False)
    repositorio.guardar(tarea)

    # Modificar y actualizar
    tarea.nombre = "Actualizada"
    tarea.completada = True
    resultado = repositorio.actualizar(tarea)

    assert resultado is True

    # Verificar cambios
    encontrada = repositorio.obtener_por_id(tarea.id)
    assert encontrada.nombre == "Actualizada"
    assert encontrada.completada is True


def test_actualizar_tarea_inexistente_retorna_false(repositorio):
    """Test: actualizar tarea inexistente retorna False"""
    tarea = Tarea(id=999, nombre="No existe", completada=False)
    resultado = repositorio.actualizar(tarea)
    assert resultado is False


# ==============================================================================
# TESTS DE ELIMINAR
# ==============================================================================

def test_eliminar_tarea_existente_retorna_true(repositorio):
    """Test: eliminar tarea existente retorna True"""
    # Guardar tarea
    tarea = Tarea(id=0, nombre="A eliminar", completada=False)
    repositorio.guardar(tarea)

    # Eliminar
    resultado = repositorio.eliminar(tarea.id)
    assert resultado is True

    # Verificar que ya no existe
    encontrada = repositorio.obtener_por_id(tarea.id)
    assert encontrada is None


def test_eliminar_tarea_inexistente_retorna_false(repositorio):
    """Test: eliminar tarea inexistente retorna False"""
    resultado = repositorio.eliminar(999)
    assert resultado is False


def test_eliminar_no_afecta_otras_tareas(repositorio):
    """Test: eliminar una tarea no afecta a las demás"""
    # Guardar 3 tareas
    tarea1 = Tarea(id=0, nombre="Tarea 1", completada=False)
    tarea2 = Tarea(id=0, nombre="Tarea 2", completada=False)
    tarea3 = Tarea(id=0, nombre="Tarea 3", completada=False)

    repositorio.guardar(tarea1)
    repositorio.guardar(tarea2)
    repositorio.guardar(tarea3)

    # Eliminar tarea2
    repositorio.eliminar(tarea2.id)

    # Verificar que tarea1 y tarea3 siguen existiendo
    assert repositorio.obtener_por_id(tarea1.id) is not None
    assert repositorio.obtener_por_id(tarea3.id) is not None
    assert repositorio.obtener_por_id(tarea2.id) is None
