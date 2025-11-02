# api/dependencias.py
"""Gestión de dependencias inyectables para FastAPI.

Este módulo define factory functions para dependency injection, permitiendo
configurar el comportamiento de la aplicación sin modificar el código de los endpoints.
"""
import os
import secrets
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from api.repositorio_base import RepositorioTareas
from api.repositorio_json import RepositorioJSON
from api.repositorio_memoria import RepositorioMemoria
from api.servicio_tareas import ServicioTareas

# ==================== CONFIGURACIÓN ====================

@lru_cache(maxsize=1)
def _get_api_key_from_env() -> str:
    """Lee API_KEY una vez al inicio y la cachea.

    Raises:
        RuntimeError: Si API_KEY no está configurada

    Returns:
        La API key configurada en el entorno
    """
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise RuntimeError(
            "API_KEY environment variable not set. "
            "Set it before starting the application."
        )
    return api_key


# ==================== REPOSITORIOS ====================

def obtener_repositorio() -> RepositorioTareas:
    """Factory para repositorio basado en configuración de entorno.

    Lee la variable MODE del entorno para decidir qué implementación usar:
    - 'production': RepositorioJSON (persistente)
    - cualquier otro valor: RepositorioMemoria (para desarrollo/tests)

    Returns:
        Implementación del protocolo RepositorioTareas

    Example:
        >>> # En producción
        >>> os.environ["MODE"] = "production"
        >>> repo = obtener_repositorio()
        >>> isinstance(repo, RepositorioJSON)
        True
    """
    mode = os.getenv("MODE", "dev")

    if mode == "production":
        return RepositorioJSON("tareas_prod.json")
    else:
        # Memoria para desarrollo y tests (no persiste entre reinicios)
        return RepositorioMemoria()


def obtener_servicio(
    repositorio: RepositorioTareas = Depends(obtener_repositorio)
) -> ServicioTareas:
    """Inyecta ServicioTareas con el repositorio configurado.

    FastAPI resuelve la dependencia `repositorio` automáticamente
    llamando a `obtener_repositorio()` primero.

    Args:
        repositorio: Implementación del repositorio (inyectada por FastAPI)

    Returns:
        Instancia de ServicioTareas configurada

    Example:
        >>> # En un endpoint
        >>> @app.get("/tareas")
        >>> def listar(servicio: ServicioTareas = Depends(obtener_servicio)):
        >>>     return servicio.listar()
    """
    return ServicioTareas(repositorio)


# Type alias para inyección limpia
ServicioDependency = Annotated[ServicioTareas, Depends(obtener_servicio)]


# ==================== AUTENTICACIÓN ====================

def verificar_api_key(x_api_key: str = Header(..., alias="x-api-key")) -> None:
    """Valida API key desde header contra variable de entorno.

    Usa comparación constant-time para prevenir timing attacks.

    Args:
        x_api_key: API key enviada en el header x-api-key

    Raises:
        HTTPException: 401 si la API key es inválida o falta

    Example:
        >>> @app.get("/protegido", dependencies=[Depends(verificar_api_key)])
        >>> def endpoint_protegido():
        >>>     return {"message": "Acceso concedido"}
    """
    esperada = _get_api_key_from_env()

    # Comparación constant-time (previene timing attacks)
    if not secrets.compare_digest(x_api_key, esperada):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key inválida"
        )
