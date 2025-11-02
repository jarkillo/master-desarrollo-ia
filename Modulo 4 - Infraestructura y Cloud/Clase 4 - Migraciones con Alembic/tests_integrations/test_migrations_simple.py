# tests_integrations/test_migrations_simple.py
"""
Tests de integración simples para validar el schema post-migrations.

Nota: Estos tests asumen que las migrations ya fueron aplicadas con `alembic upgrade head`.
Para ejecutar:
    1. cd "Modulo 4 - Infraestructura y Cloud/Clase 4 - Migraciones con Alembic"
    2. alembic upgrade head  (aplicar migrations)
    3. pytest tests_integrations/test_migrations_simple.py
"""
import pytest
from api.models import TareaModel
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="module")
def engine():
    """Fixture que proporciona un engine conectado a la BD migrada"""
    test_engine = create_engine("sqlite:///./tareas.db")
    yield test_engine
    test_engine.dispose()


@pytest.fixture
def db_session(engine):
    """Fixture que proporciona una sesión de BD limpia para cada test"""
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    yield session

    # Cleanup: eliminar todos los datos de prueba
    session.query(TareaModel).delete()
    session.commit()
    session.close()


class TestSchemaPostMigrations:
    """Tests que validan el schema después de aplicar migrations"""

    def test_tabla_tareas_existe(self, engine):
        """Test que la tabla 'tareas' existe"""
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        assert "tareas" in tables

    def test_tabla_tareas_tiene_columnas_esperadas(self, engine):
        """Test que la tabla tiene todas las columnas esperadas"""
        inspector = inspect(engine)
        columns = {col["name"] for col in inspector.get_columns("tareas")}

        expected_columns = {
            "id",
            "nombre",
            "completada",
            "prioridad",
            "creado_en",
            "actualizado_en"
        }

        assert expected_columns.issubset(columns), \
            f"Faltan columnas. Esperadas: {expected_columns}, Encontradas: {columns}"

    def test_columna_id_es_primary_key(self, engine):
        """Test que 'id' es primary key"""
        inspector = inspect(engine)
        pk = inspector.get_pk_constraint("tareas")
        assert "id" in pk["constrained_columns"]

    def test_columna_nombre_no_permite_null(self, engine):
        """Test que 'nombre' no permite NULL"""
        inspector = inspect(engine)
        columns = {col["name"]: col for col in inspector.get_columns("tareas")}
        assert columns["nombre"]["nullable"] is False

    def test_columna_prioridad_existe(self, engine):
        """Test que la columna 'prioridad' existe"""
        inspector = inspect(engine)
        columns = {col["name"] for col in inspector.get_columns("tareas")}

        # Verificar que existe la columna (el default se prueba en otro test)
        assert "prioridad" in columns


class TestModeloORMFuncionaConBDMigrada:
    """Tests que verifican que el modelo ORM funciona con la BD migrada"""

    def test_crear_tarea_con_modelo_orm(self, db_session):
        """Test que se puede crear una tarea usando el modelo ORM"""
        nueva_tarea = TareaModel(
            nombre="Tarea de test",
            completada=False,
            prioridad=2
        )

        db_session.add(nueva_tarea)
        db_session.commit()
        db_session.refresh(nueva_tarea)

        assert nueva_tarea.id is not None
        assert nueva_tarea.nombre == "Tarea de test"
        assert nueva_tarea.completada is False
        assert nueva_tarea.prioridad == 2
        assert nueva_tarea.creado_en is not None

    def test_leer_tareas_con_modelo_orm(self, db_session):
        """Test que se pueden leer tareas usando el modelo ORM"""
        # Crear tareas de prueba
        tarea1 = TareaModel(nombre="Tarea 1", completada=False, prioridad=1)
        tarea2 = TareaModel(nombre="Tarea 2", completada=True, prioridad=3)

        db_session.add_all([tarea1, tarea2])
        db_session.commit()

        # Leer todas las tareas
        tareas = db_session.query(TareaModel).all()

        assert len(tareas) == 2
        assert any(t.nombre == "Tarea 1" for t in tareas)
        assert any(t.nombre == "Tarea 2" for t in tareas)

    def test_actualizar_tarea_con_modelo_orm(self, db_session):
        """Test que se pueden actualizar tareas"""
        tarea = TareaModel(nombre="Tarea inicial", completada=False, prioridad=2)
        db_session.add(tarea)
        db_session.commit()

        tarea_id = tarea.id

        # Actualizar
        tarea.nombre = "Tarea modificada"
        tarea.completada = True
        db_session.commit()

        # Leer de nuevo
        tarea_actualizada = db_session.query(TareaModel).filter_by(id=tarea_id).first()

        assert tarea_actualizada.nombre == "Tarea modificada"
        assert tarea_actualizada.completada is True
        assert tarea_actualizada.actualizado_en is not None

    def test_eliminar_tarea_con_modelo_orm(self, db_session):
        """Test que se pueden eliminar tareas"""
        tarea = TareaModel(nombre="Tarea a eliminar", completada=False, prioridad=2)
        db_session.add(tarea)
        db_session.commit()

        tarea_id = tarea.id

        # Eliminar
        db_session.delete(tarea)
        db_session.commit()

        # Verificar que no existe
        tarea_eliminada = db_session.query(TareaModel).filter_by(id=tarea_id).first()
        assert tarea_eliminada is None

    def test_campo_prioridad_tiene_default(self, db_session):
        """Test que el campo prioridad tiene un valor por defecto"""
        # Crear tarea sin especificar prioridad
        tarea = TareaModel(nombre="Tarea sin prioridad", completada=False)
        db_session.add(tarea)
        db_session.commit()
        db_session.refresh(tarea)

        # Debería tener el default (2)
        assert tarea.prioridad == 2


class TestAlembicVersionTable:
    """Tests que verifican que Alembic creó su tabla de versiones"""

    def test_alembic_version_existe(self, engine):
        """Test que la tabla alembic_version existe"""
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        assert "alembic_version" in tables

    def test_alembic_version_tiene_version_actual(self, engine):
        """Test que alembic_version registra la versión actual"""
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version_num FROM alembic_version"))
            version = result.scalar()

        # Debe tener alguna versión registrada
        assert version is not None
        # Debe ser una string de 12 caracteres (ej: '05702ef4b618')
        assert len(version) == 12
