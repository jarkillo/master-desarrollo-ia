"""
Configuración de la base de datos con SQLAlchemy.

Este módulo gestiona:
- Engine de SQLAlchemy
- Session factory
- Creación de tablas
- Dependency para FastAPI
"""

from collections.abc import Generator

from sqlalchemy import create_engine, event, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from api.config import settings
from api.models import Base

# ============================================================================
# ENGINE CONFIGURATION
# ============================================================================

# Configuración específica para SQLite
connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Crear engine
engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    echo=settings.debug,  # Log de queries SQL en modo debug
    pool_pre_ping=True,  # Verifica conexiones antes de usarlas
)


# ============================================================================
# SQLITE FOREIGN KEYS ENFORCEMENT
# ============================================================================

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """
    Habilita FOREIGN KEY constraints en SQLite.

    SQLite requiere habilitar las FK manualmente en cada conexión.
    PostgreSQL las tiene habilitadas por defecto.
    """
    if settings.database_url.startswith("sqlite"):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


# ============================================================================
# SESSION FACTORY
# ============================================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def crear_tablas() -> None:
    """
    Crea todas las tablas definidas en los modelos.

    NOTA: En producción, usa Alembic en lugar de esto.
    Esta función es útil para desarrollo y tests.
    """
    Base.metadata.create_all(bind=engine)


def drop_tablas() -> None:
    """
    Elimina todas las tablas.

    ⚠️ PELIGRO: Usa solo en tests o desarrollo.
    """
    Base.metadata.drop_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency de FastAPI para obtener una sesión de BD.

    Uso en endpoints:
        @app.get("/tareas")
        def listar(db: Session = Depends(get_db)):
            return db.query(TareaModel).all()

    Yields:
        Session de SQLAlchemy

    Garantiza:
        - La sesión se cierra automáticamente al terminar el request
        - En caso de error, se hace rollback automático
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verificar_conexion() -> bool:
    """
    Verifica que la conexión a la BD funciona.

    Returns:
        True si la conexión es exitosa, False en caso contrario
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Error al conectar a la BD: {e}")
        return False
