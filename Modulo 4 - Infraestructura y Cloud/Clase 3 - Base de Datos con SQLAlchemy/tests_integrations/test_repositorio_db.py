# tests_integrations/test_repositorio_db.py
"""
Tests de integración del RepositorioDB.

Estos tests verifican que el repositorio funciona correctamente
con una base de datos real (SQLite en memoria).
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.models import Base
from api.repositorio_db import RepositorioDB
from api.servicio_tareas import Tarea


# Base de datos en memoria para tests
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    """Crea y limpia las tablas antes de cada test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Proporciona una sesión de BD para tests"""
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def repositorio(db_session):
    """Proporciona un repositorio configurado"""
    return RepositorioDB(session=db_session)


# ============================================================================
# TESTS
# ============================================================================

def test_guardar_nueva_tarea(repositorio):
    """Test de guardar una nueva tarea"""
    tarea = Tarea(id=0, nombre="Tarea nueva", completada=False)
    repositorio.guardar(tarea)

    # Verificar que se asignó un ID
    assert tarea.id > 0


def test_guardar_asigna_id_incremental(repositorio):
    """Test de que los IDs se asignan incrementalmente"""
    tarea1 = Tarea(id=0, nombre="Primera")
    tarea2 = Tarea(id=0, nombre="Segunda")

    repositorio.guardar(tarea1)
    repositorio.guardar(tarea2)

    assert tarea1.id > 0
    assert tarea2.id > tarea1.id


def test_listar_vacio(repositorio):
    """Test de listar cuando no hay tareas"""
    tareas = repositorio.listar()
    assert tareas == []


def test_listar_con_tareas(repositorio):
    """Test de listar con tareas guardadas"""
    # Guardar 3 tareas
    for i in range(1, 4):
        tarea = Tarea(id=0, nombre=f"Tarea {i}")
        repositorio.guardar(tarea)

    # Listar
    tareas = repositorio.listar()
    assert len(tareas) == 3
    assert tareas[0].nombre == "Tarea 1"
    assert tareas[1].nombre == "Tarea 2"
    assert tareas[2].nombre == "Tarea 3"


def test_obtener_por_id_existente(repositorio):
    """Test de obtener una tarea que existe"""
    # Guardar tarea
    tarea = Tarea(id=0, nombre="Mi tarea")
    repositorio.guardar(tarea)
    tarea_id = tarea.id

    # Obtener
    tarea_obtenida = repositorio.obtener_por_id(tarea_id)
    assert tarea_obtenida is not None
    assert tarea_obtenida.id == tarea_id
    assert tarea_obtenida.nombre == "Mi tarea"


def test_obtener_por_id_no_existente(repositorio):
    """Test de obtener una tarea que no existe"""
    tarea = repositorio.obtener_por_id(999)
    assert tarea is None


def test_actualizar_tarea_existente(repositorio):
    """Test de actualizar una tarea existente"""
    # Crear tarea
    tarea = Tarea(id=0, nombre="Original", completada=False)
    repositorio.guardar(tarea)
    tarea_id = tarea.id

    # Actualizar
    tarea_actualizada = Tarea(id=tarea_id, nombre="Actualizada", completada=True)
    resultado = repositorio.actualizar(tarea_actualizada)

    assert resultado is True

    # Verificar cambios
    tarea_obtenida = repositorio.obtener_por_id(tarea_id)
    assert tarea_obtenida.nombre == "Actualizada"
    assert tarea_obtenida.completada is True


def test_actualizar_tarea_no_existente(repositorio):
    """Test de actualizar una tarea que no existe"""
    tarea = Tarea(id=999, nombre="No existe", completada=True)
    resultado = repositorio.actualizar(tarea)
    assert resultado is False


def test_eliminar_tarea_existente(repositorio):
    """Test de eliminar una tarea existente"""
    # Crear tarea
    tarea = Tarea(id=0, nombre="A eliminar")
    repositorio.guardar(tarea)
    tarea_id = tarea.id

    # Eliminar
    resultado = repositorio.eliminar(tarea_id)
    assert resultado is True

    # Verificar que ya no existe
    tarea_obtenida = repositorio.obtener_por_id(tarea_id)
    assert tarea_obtenida is None


def test_eliminar_tarea_no_existente(repositorio):
    """Test de eliminar una tarea que no existe"""
    resultado = repositorio.eliminar(999)
    assert resultado is False


def test_persistencia_entre_operaciones(repositorio):
    """Test de que los datos persisten entre operaciones"""
    # Crear tarea
    tarea = Tarea(id=0, nombre="Persistente")
    repositorio.guardar(tarea)
    tarea_id = tarea.id

    # Listar (operación diferente)
    tareas = repositorio.listar()
    assert len(tareas) == 1
    assert tareas[0].id == tarea_id

    # Obtener (otra operación)
    tarea_obtenida = repositorio.obtener_por_id(tarea_id)
    assert tarea_obtenida is not None
    assert tarea_obtenida.nombre == "Persistente"


def test_completada_default_false(repositorio):
    """Test de que completada es False por defecto"""
    tarea = Tarea(id=0, nombre="Nueva tarea")
    repositorio.guardar(tarea)

    tarea_obtenida = repositorio.obtener_por_id(tarea.id)
    assert tarea_obtenida.completada is False


def test_multiples_actualizaciones(repositorio):
    """Test de múltiples actualizaciones sobre la misma tarea"""
    # Crear
    tarea = Tarea(id=0, nombre="Original")
    repositorio.guardar(tarea)
    tarea_id = tarea.id

    # Primera actualización
    tarea1 = Tarea(id=tarea_id, nombre="Actualización 1", completada=False)
    repositorio.actualizar(tarea1)

    # Segunda actualización
    tarea2 = Tarea(id=tarea_id, nombre="Actualización 2", completada=True)
    repositorio.actualizar(tarea2)

    # Verificar última actualización
    tarea_final = repositorio.obtener_por_id(tarea_id)
    assert tarea_final.nombre == "Actualización 2"
    assert tarea_final.completada is True
