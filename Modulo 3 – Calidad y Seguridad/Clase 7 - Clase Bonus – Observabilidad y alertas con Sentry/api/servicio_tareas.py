# api/servicio_tareas.py
"""Capa de servicio para lógica de negocio de tareas.

Este módulo implementa el patrón Service Layer, separando la lógica de negocio
de la capa de API (endpoints) y la capa de persistencia (repositorio).
"""
from pydantic import BaseModel, Field

from api.repositorio_base import RepositorioTareas


class Tarea(BaseModel):
    """Modelo de dominio para una tarea.

    Representa una tarea en el sistema con su estado completo.

    Attributes:
        id: Identificador único de la tarea (asignado por el repositorio)
        nombre: Descripción de la tarea
        completada: Estado de completitud (False por defecto)

    Example:
        >>> tarea = Tarea(id=1, nombre="Escribir tests", completada=False)
        >>> print(tarea.nombre)
        'Escribir tests'
    """
    id: int = Field(default=0, description="ID único de la tarea")
    nombre: str = Field(
        min_length=1,
        max_length=200,
        description="Descripción de la tarea"
    )
    completada: bool = Field(default=False, description="¿Está completada?")


class ServicioTareas:
    """Servicio de gestión de tareas con lógica de negocio.

    Este servicio orquesta operaciones sobre tareas, delegando la persistencia
    al repositorio inyectado. Implementa Dependency Inversion Principle (SOLID):
    depende de la abstracción RepositorioTareas, no de implementaciones concretas.

    Args:
        repositorio: Implementación del protocolo RepositorioTareas

    Example:
        >>> from api.repositorio_memoria import RepositorioMemoria
        >>> repo = RepositorioMemoria()
        >>> servicio = ServicioTareas(repo)
        >>> tarea = servicio.crear("Completar documentación")
        >>> print(tarea.nombre)
        'Completar documentación'
    """

    def __init__(self, repositorio: RepositorioTareas) -> None:
        self._repo = repositorio

    def crear(self, nombre: str) -> Tarea:
        """Crea una nueva tarea y la persiste en el repositorio.

        El ID de la tarea es asignado por el repositorio (auto-incremental).
        La tarea se crea en estado no completada por defecto.

        Args:
            nombre: Descripción de la tarea (no vacío, max 200 caracteres)

        Returns:
            La tarea creada con ID asignado

        Example:
            >>> tarea = servicio.crear("Escribir tests")
            >>> assert tarea.id > 0
            >>> assert tarea.completada is False
        """
        nueva = Tarea(id=0, nombre=nombre)  # ID temporal, el repo asigna el real
        self._repo.guardar(nueva)
        return nueva

    def listar(self) -> list[Tarea]:
        """Obtiene todas las tareas almacenadas.

        Returns:
            Lista de tareas (vacía si no hay ninguna)

        Example:
            >>> tareas = servicio.listar()
            >>> print(len(tareas))
            3
        """
        return self._repo.listar()
