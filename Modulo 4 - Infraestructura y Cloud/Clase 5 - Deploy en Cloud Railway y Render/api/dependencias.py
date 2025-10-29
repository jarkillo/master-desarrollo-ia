# api/dependencias.py
"""
Dependency Injection para FastAPI.

Proporciona instancias de servicio y repositorio
a los endpoints de la API.
"""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from api.database import get_db
from api.repositorio_db import RepositorioDB
from api.servicio_tareas import ServicioTareas


def get_repositorio(db: Session = Depends(get_db)) -> RepositorioDB:
    """
    Proporciona una instancia del repositorio de BD.

    Args:
        db: Sesión de BD (inyectada por FastAPI)

    Returns:
        Repositorio configurado con la sesión
    """
    return RepositorioDB(session=db)


def get_servicio(repo: RepositorioDB = Depends(get_repositorio)) -> ServicioTareas:
    """
    Proporciona una instancia del servicio de tareas.

    Args:
        repo: Repositorio (inyectado por FastAPI)

    Returns:
        Servicio configurado con el repositorio
    """
    return ServicioTareas(repositorio=repo)


# Type alias para usar en endpoints
ServicioTareasDepende = Annotated[ServicioTareas, Depends(get_servicio)]
