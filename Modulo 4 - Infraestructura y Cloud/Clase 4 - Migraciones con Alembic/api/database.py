# api/database.py
"""
Configuración de la base de datos con SQLAlchemy 2.0

Este módulo gestiona:
- Creación del engine (motor de BD)
- Session factory (fábrica de sesiones)
- Dependency injection para FastAPI
"""
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from api.models import Base

# URL de conexión a la base de datos
# SQLite para desarrollo (archivo local)
# En producción usarías PostgreSQL, MySQL, etc.
DATABASE_URL = "sqlite:///./tareas.db"

# Engine: motor que gestiona conexiones a la BD
# check_same_thread=False es necesario para SQLite + FastAPI
# (SQLite por defecto no permite múltiples threads)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # Cambia a True para ver SQL en consola (útil para debugging)
)

# SessionLocal: fábrica de sesiones
# Cada sesión representa una "conversación" con la BD
SessionLocal = sessionmaker(
    autocommit=False,  # Commits manuales (más control)
    autoflush=False,   # Flush manual (evita sorpresas)
    bind=engine        # Vinculada al engine
)


def crear_tablas():
    """
    Crea todas las tablas definidas en los modelos.

    ⚠️ DEPRECATED: Este método NO debe usarse en Clase 4+.

    En Clase 4+ usamos Alembic migrations:
        alembic upgrade head

    Este método existe solo para compatibilidad con Clases 2-3 donde
    aún no habíamos aprendido migraciones.

    Razones para usar Alembic en lugar de create_all():
    - create_all() no actualiza tablas existentes
    - No hay historial de cambios
    - No es reversible (no hay rollback)
    - Imposible gestionar cambios incrementales en producción
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
