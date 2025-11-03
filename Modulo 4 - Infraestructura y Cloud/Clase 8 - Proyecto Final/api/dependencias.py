"""
Dependency injection para FastAPI.

Define las dependencias que se inyectan en los endpoints:
- Sesión de base de datos
- Repositorios
- Servicios
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from api.database import get_db
from api.repositorio_tareas import RepositorioTareasDB
from api.repositorio_usuarios import RepositorioUsuariosDB
from api.servicio_tareas import ServicioTareas
from api.servicio_usuarios import ServicioUsuarios

# ============================================================================
# REPOSITORIOS
# ============================================================================

def get_repositorio_usuarios(
    db: Session = Depends(get_db)
) -> RepositorioUsuariosDB:
    """
    Dependency para obtener el repositorio de usuarios.

    Args:
        db: Sesión de base de datos

    Returns:
        Repositorio de usuarios configurado
    """
    return RepositorioUsuariosDB(session=db)


def get_repositorio_tareas(
    db: Session = Depends(get_db)
) -> RepositorioTareasDB:
    """
    Dependency para obtener el repositorio de tareas.

    Args:
        db: Sesión de base de datos

    Returns:
        Repositorio de tareas configurado
    """
    return RepositorioTareasDB(session=db)


# ============================================================================
# SERVICIOS
# ============================================================================

def get_servicio_usuarios(
    repo: RepositorioUsuariosDB = Depends(get_repositorio_usuarios)
) -> ServicioUsuarios:
    """
    Dependency para obtener el servicio de usuarios.

    Args:
        repo: Repositorio de usuarios

    Returns:
        Servicio de usuarios configurado
    """
    return ServicioUsuarios(repositorio=repo)


def get_servicio_tareas(
    repo: RepositorioTareasDB = Depends(get_repositorio_tareas)
) -> ServicioTareas:
    """
    Dependency para obtener el servicio de tareas.

    Args:
        repo: Repositorio de tareas

    Returns:
        Servicio de tareas configurado
    """
    return ServicioTareas(repositorio=repo)
