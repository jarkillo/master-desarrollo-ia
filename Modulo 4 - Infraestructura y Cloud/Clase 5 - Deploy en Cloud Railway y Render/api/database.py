# api/database.py
"""
Configuración de la base de datos con SQLAlchemy 2.0 para producción.

Diferencias con Clase 4:
- Soporta PostgreSQL en producción (Railway, Render, etc.)
- Usa configuración dinámica (Settings)
- Connection pooling optimizado para cloud
- Health check de base de datos

🔧 CONFIGURACIÓN POR ENTORNO:

Development (SQLite):
    DATABASE_URL=sqlite:///./tareas.db

Production (PostgreSQL en Railway):
    DATABASE_URL=postgresql://user:pass@host:port/dbname

Production (PostgreSQL en Render):
    DATABASE_URL=postgresql://user:pass@host:port/dbname
"""
import logging
from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool, QueuePool

from api.config import settings
from api.models import Base


def get_engine_config():
    """
    Retorna la configuración del engine según el entorno.

    SQLite (dev):
    - NullPool (sin pooling, SQLite no lo necesita)
    - check_same_thread=False (permite FastAPI multi-thread)

    PostgreSQL (staging/prod):
    - QueuePool (pool de conexiones)
    - Pool size y overflow configurables
    """
    if settings.database_url.startswith("sqlite"):
        # Configuración para SQLite
        return {
            "connect_args": {"check_same_thread": False},
            "poolclass": NullPool,  # SQLite no necesita pooling
            "echo": settings.database_echo  # SQL logs en dev
        }
    else:
        # Configuración para PostgreSQL/MySQL
        return {
            "poolclass": QueuePool,
            "pool_size": settings.db_pool_size,  # Conexiones simultáneas
            "max_overflow": settings.db_max_overflow,  # Conexiones extra
            "pool_pre_ping": True,  # Verifica conexiones antes de usar
            "echo": settings.database_echo
        }


# Engine: motor que gestiona conexiones a la BD
engine = create_engine(
    settings.database_url,
    **get_engine_config()
)

# SessionLocal: fábrica de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def crear_tablas():
    """
    Crea todas las tablas definidas en los modelos.

    ⚠️ DEPRECATED: En Clase 4+ usamos Alembic migrations.

    Este método solo debe usarse en:
    - Desarrollo rápido (prototipos)
    - Tests (crear DB temporal)

    En producción SIEMPRE usa Alembic:
        alembic upgrade head

    Razones:
    - create_all() no actualiza tablas existentes
    - Sin historial de cambios
    - No reversible
    - Imposible gestionar cambios incrementales
    """
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency injection para FastAPI.

    Proporciona una sesión de BD a cada endpoint.
    La sesión se cierra automáticamente al terminar el request.

    Uso en FastAPI:
        @app.get("/tareas")
        def listar(db: Session = Depends(get_db)):
            ...

    Yields:
        Session: Sesión de SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_database_health() -> dict:
    """
    Verifica que la conexión a la base de datos funciona.

    Útil para health checks en producción.
    Railway, Render y otros clouds usan esto para monitorear la app.

    Returns:
        dict: {"status": "ok"} si funciona, lanza excepción si no

    Raises:
        Exception: Si la BD no está disponible
    """
    try:
        with engine.connect() as conn:
            # Ejecuta una query simple para verificar conexión
            result = conn.execute(text("SELECT 1"))
            result.scalar()  # Obtiene el valor
        return {
            "status": "ok",
            "database": "connected",
            "url": settings.database_url.split("@")[-1] if "@" in settings.database_url else "local"
        }
    except Exception:
        logging.exception("Database health check failed")
        return {
            "status": "error",
            "database": "disconnected",
            "error": "Database connection failed"
        }
