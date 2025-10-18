# api/repositorio_base.py
from typing import Protocol, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    # Solo para tipos (no se ejecuta en runtime, evita el ciclo)
    from api.servicio_tareas import Tarea


class RepositorioTareas(Protocol):
    """
    Interfaz (Protocol) para repositorios de tareas.

    Define el contrato que TODOS los repositorios deben cumplir.
    Esto permite intercambiar implementaciones sin cambiar el servicio
    (Dependency Inversion Principle - SOLID).
    """
    def guardar(self, tarea: "Tarea") -> None:
        """Guarda una tarea (nueva o existente)"""
        ...

    def listar(self) -> List["Tarea"]:
        """Lista todas las tareas"""
        ...

    def obtener_por_id(self, id: int) -> Optional["Tarea"]:
        """Obtiene una tarea por ID, o None si no existe"""
        ...

    def actualizar(self, tarea: "Tarea") -> bool:
        """Actualiza una tarea existente. Retorna True si existía."""
        ...

    def eliminar(self, id: int) -> bool:
        """Elimina una tarea por ID. Retorna True si existía."""
        ...
