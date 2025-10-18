# tests_integrations/test_migrations.py
"""
Tests de integración para migrations de Alembic.

Estos tests verifican que:
- Las migrations se aplican correctamente
- El schema resultante es el esperado
- Los modelos ORM funcionan con la BD migrada
"""
import os
import subprocess
import pytest
from pathlib import Path
from sqlalchemy import create_engine, inspect, text, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Session
from api.models import Base, TareaModel
from api.database import DATABASE_URL


# Path al directorio del proyecto
PROJECT_DIR = Path(__file__).parent.parent


class TestMigrationsWorkflow:
    """Tests del workflow completo de migrations"""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Setup y teardown para cada test"""
        # Setup: Limpiar BD de test antes de cada test
        test_db = PROJECT_DIR / "test_migrations.db"
        if test_db.exists():
            test_db.unlink()

        yield

        # Teardown: Limpiar después del test
        if test_db.exists():
            test_db.unlink()

    def test_upgrade_crea_tabla_tareas(self):
        """Test que upgrade crea la tabla 'tareas' con todas las columnas"""
        # Crear alembic.ini temporal para testing
        test_db_url = "sqlite:///./test_migrations.db"

        # Aplicar migrations hasta la primera (crear tabla)
        result = subprocess.run(
            [
                "alembic", "upgrade", "58cbce442bf6"  # Primera migration
            ],
            cwd=str(PROJECT_DIR),
            capture_output=True,
            text=True,
            env={**os.environ, "DATABASE_URL": test_db_url}
        )

        assert result.returncode == 0, f"alembic upgrade falló: {result.stderr}"

        # Verificar que la tabla se creó
        engine = create_engine(test_db_url)
        inspector = inspect(engine)

        assert "tareas" in inspector.get_table_names()

        # Verificar columnas
        columns = {col["name"] for col in inspector.get_columns("tareas")}
        expected_columns = {"id", "nombre", "completada", "creado_en", "actualizado_en"}
        assert expected_columns.issubset(columns)

        engine.dispose()

    def test_upgrade_head_aplica_todas_las_migrations(self):
        """Test que upgrade head aplica todas las migrations"""
        test_db_url = "sqlite:///./test_migrations.db"

        # Aplicar todas las migrations
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            cwd=str(PROJECT_DIR),
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"alembic upgrade head falló: {result.stderr}"

        # Verificar que la tabla tiene todas las columnas (incluida prioridad)
        engine = create_engine(test_db_url)
        inspector = inspect(engine)

        columns = {col["name"] for col in inspector.get_columns("tareas")}
        expected_columns = {"id", "nombre", "completada", "prioridad", "creado_en", "actualizado_en"}
        assert expected_columns.issubset(columns)

        engine.dispose()

    def test_downgrade_elimina_columna_prioridad(self):
        """Test que downgrade revierte la migration de prioridad"""
        test_db_url = "sqlite:///./test_migrations.db"

        # Aplicar todas las migrations
        subprocess.run(
            ["alembic", "upgrade", "head"],
            cwd=str(PROJECT_DIR),
            capture_output=True
        )

        # Hacer downgrade de la última migration
        result = subprocess.run(
            ["alembic", "downgrade", "-1"],
            cwd=str(PROJECT_DIR),
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"alembic downgrade falló: {result.stderr}"

        # Verificar que la columna prioridad ya no existe
        engine = create_engine(test_db_url)
        inspector = inspect(engine)

        columns = {col["name"] for col in inspector.get_columns("tareas")}
        assert "prioridad" not in columns
        assert "nombre" in columns  # Pero otras columnas sí existen

        engine.dispose()

    def test_downgrade_base_elimina_todo(self):
        """Test que downgrade base elimina todas las tablas"""
        test_db_url = "sqlite:///./test_migrations.db"

        # Aplicar todas las migrations
        subprocess.run(
            ["alembic", "upgrade", "head"],
            cwd=str(PROJECT_DIR),
            capture_output=True
        )

        # Hacer downgrade completo
        result = subprocess.run(
            ["alembic", "downgrade", "base"],
            cwd=str(PROJECT_DIR),
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"alembic downgrade base falló: {result.stderr}"

        # Verificar que no hay tablas (excepto alembic_version)
        engine = create_engine(test_db_url)
        inspector = inspect(engine)

        tables = inspector.get_table_names()
        assert "tareas" not in tables

        engine.dispose()

    def test_upgrade_downgrade_upgrade_es_idempotente(self):
        """Test que aplicar upgrade-downgrade-upgrade produce el mismo resultado"""
        test_db_url = "sqlite:///./test_migrations.db"

        # Primera aplicación
        subprocess.run(["alembic", "upgrade", "head"], cwd=str(PROJECT_DIR), capture_output=True)

        engine = create_engine(test_db_url)
        inspector = inspect(engine)
        columns_before = {col["name"] for col in inspector.get_columns("tareas")}
        engine.dispose()

        # Downgrade y upgrade de nuevo
        subprocess.run(["alembic", "downgrade", "-1"], cwd=str(PROJECT_DIR), capture_output=True)
        subprocess.run(["alembic", "upgrade", "head"], cwd=str(PROJECT_DIR), capture_output=True)

        # Verificar que el schema es el mismo
        engine = create_engine(test_db_url)
        inspector = inspect(engine)
        columns_after = {col["name"] for col in inspector.get_columns("tareas")}
        engine.dispose()

        assert columns_before == columns_after


class TestMigrationsPreservanDatos:
    """Tests que verifican que las migrations no pierden datos"""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Setup y teardown para cada test"""
        test_db = PROJECT_DIR / "test_migrations_data.db"
        if test_db.exists():
            test_db.unlink()

        yield

        if test_db.exists():
            test_db.unlink()

    def test_agregar_columna_preserva_datos_existentes(self):
        """Test que agregar columna 'prioridad' no pierde datos de tareas"""
        test_db_url = "sqlite:///./test_migrations_data.db"

        # Aplicar solo la primera migration (sin prioridad)
        subprocess.run(
            ["alembic", "upgrade", "58cbce442bf6"],
            cwd=str(PROJECT_DIR),
            capture_output=True
        )

        # Insertar datos de prueba
        engine = create_engine(test_db_url)
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO tareas (nombre, completada)
                VALUES ('Tarea 1', 0), ('Tarea 2', 1)
            """))
            conn.commit()

        # Aplicar segunda migration (agregar prioridad)
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            cwd=str(PROJECT_DIR),
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"Migration falló: {result.stderr}"

        # Verificar que los datos siguen ahí
        with engine.connect() as conn:
            result = conn.execute(text("SELECT nombre, completada FROM tareas ORDER BY id"))
            rows = result.fetchall()

        assert len(rows) == 2
        assert rows[0][0] == "Tarea 1"
        assert rows[1][0] == "Tarea 2"

        engine.dispose()


class TestMigrationsSchema:
    """Tests que validan el schema generado por las migrations"""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Setup y teardown para cada test"""
        test_db = PROJECT_DIR / "test_migrations_schema.db"
        if test_db.exists():
            test_db.unlink()

        subprocess.run(
            ["alembic", "upgrade", "head"],
            cwd=str(PROJECT_DIR),
            capture_output=True
        )

        yield

        if test_db.exists():
            test_db.unlink()

    def test_columna_id_es_primary_key(self):
        """Test que la columna 'id' es primary key"""
        test_db_url = "sqlite:///./test_migrations_schema.db"
        engine = create_engine(test_db_url)
        inspector = inspect(engine)

        pk = inspector.get_pk_constraint("tareas")
        assert "id" in pk["constrained_columns"]

        engine.dispose()

    def test_columna_nombre_no_permite_null(self):
        """Test que la columna 'nombre' no permite NULL"""
        test_db_url = "sqlite:///./test_migrations_schema.db"
        engine = create_engine(test_db_url)
        inspector = inspect(engine)

        columns = {col["name"]: col for col in inspector.get_columns("tareas")}
        assert columns["nombre"]["nullable"] is False

        engine.dispose()

    def test_columna_prioridad_tiene_default(self):
        """Test que la columna 'prioridad' tiene un valor por defecto"""
        test_db_url = "sqlite:///./test_migrations_schema.db"
        engine = create_engine(test_db_url)

        # Insertar tarea sin especificar prioridad
        with engine.connect() as conn:
            conn.execute(text("INSERT INTO tareas (nombre, completada) VALUES ('Test', 0)"))
            conn.commit()

            result = conn.execute(text("SELECT prioridad FROM tareas WHERE nombre = 'Test'"))
            prioridad = result.fetchone()[0]

        # El default es 2 (media)
        assert prioridad == 2

        engine.dispose()
