"""
Protocol (interfaz) para repositorios de tareas.
Define el contrato que deben cumplir todas las implementaciones.
"""
from typing import Protocol
from pydantic import BaseModel


class Tarea(BaseModel):
    """Modelo de dominio para una tarea."""
    id: int
    nombre: str
    completada: bool = False


class CrearTareaRequest(BaseModel):
    """Request para crear una nueva tarea."""
    nombre: str


class ActualizarTareaRequest(BaseModel):
    """Request para actualizar una tarea."""
    nombre: str | None = None
    completada: bool | None = None


class RepositorioTareas(Protocol):
    """
    Protocol que define las operaciones CRUD para tareas.

    Cualquier implementación debe proveer estos métodos.
    """

    def crear(self, nombre: str) -> Tarea:
        """Crea una nueva tarea."""
        ...

    def listar(self) -> list[Tarea]:
        """Retorna todas las tareas."""
        ...

    def obtener(self, tarea_id: int) -> Tarea | None:
        """Obtiene una tarea por ID."""
        ...

    def actualizar(self, tarea_id: int, nombre: str | None = None,
                   completada: bool | None = None) -> Tarea | None:
        """Actualiza una tarea existente."""
        ...

    def eliminar(self, tarea_id: int) -> bool:
        """Elimina una tarea. Retorna True si se eliminó."""
        ...
