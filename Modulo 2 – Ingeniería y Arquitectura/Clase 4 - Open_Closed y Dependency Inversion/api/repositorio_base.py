# api/repositorio_base.py
"""Define el contrato que todos los repositorios de tareas deben cumplir.

Este Protocol permite aplicar Dependency Inversion Principle (DIP):
el servicio depende de esta abstracción, no de implementaciones concretas.
"""
from typing import Protocol, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    # Solo para tipos (no se ejecuta en runtime, evita el ciclo)
    from api.servicio_tareas import Tarea


class RepositorioTareas(Protocol):
    """Contrato que define cómo CUALQUIER repositorio debe comportarse.

    Cualquier clase que implemente estos métodos con estas firmas
    automáticamente cumple el contrato (structural subtyping, PEP 544).
    """

    def guardar(self, tarea: "Tarea") -> None:
        """Persiste una tarea (nueva o existente).

        Si tarea.id == 0, se le debe asignar un ID único.
        Si tarea.id > 0, se actualiza la tarea existente.
        """
        ...

    def listar(self) -> List["Tarea"]:
        """Devuelve todas las tareas persistidas.

        Returns:
            Lista de tareas (puede estar vacía)
        """
        ...

    def obtener_por_id(self, id: int) -> Optional["Tarea"]:
        """Busca una tarea por su ID.

        Args:
            id: ID de la tarea a buscar

        Returns:
            La tarea si existe, None si no se encuentra
        """
        ...

    def eliminar(self, id: int) -> bool:
        """Elimina una tarea por su ID.

        Args:
            id: ID de la tarea a eliminar

        Returns:
            True si la tarea existía y fue eliminada
            False si la tarea no existía
        """
        ...

    def completar(self, id: int) -> Optional["Tarea"]:
        """Marca una tarea como completada.

        Args:
            id: ID de la tarea a completar

        Returns:
            La tarea actualizada si existía, None si no fue encontrada
        """
        ...
