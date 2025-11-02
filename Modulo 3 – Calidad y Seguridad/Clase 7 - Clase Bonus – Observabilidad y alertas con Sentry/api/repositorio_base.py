# api/repositorio_base.py
"""Protocolo (interfaz) para repositorios de tareas.

Este módulo define el contrato que debe cumplir cualquier implementación
de repositorio usando el patrón Protocol de Python (Dependency Inversion).
"""
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    # Solo importado para type checking, no en runtime (evita dependencias circulares)
    from api.servicio_tareas import Tarea


class RepositorioTareas(Protocol):
    """Protocolo (interfaz) para repositorios de tareas.

    Define el contrato que debe cumplir cualquier implementación de repositorio
    (memoria, JSON, base de datos, etc.). Esto permite Dependency Inversion:
    el ServicioTareas depende de esta abstracción, no de implementaciones concretas.

    Example:
        >>> class MiRepositorio:
        ...     def guardar(self, tarea: Tarea) -> None:
        ...         pass
        ...     def listar(self) -> list[Tarea]:
        ...         return []
        >>> # MiRepositorio cumple el protocolo automáticamente (structural typing)
    """

    def guardar(self, tarea: "Tarea") -> None:
        """Persiste una tarea, asignándole un ID único.

        Args:
            tarea: La tarea a guardar (se modifica in-place para asignar ID)
        """
        ...

    def listar(self) -> list["Tarea"]:
        """Recupera todas las tareas almacenadas.

        Returns:
            Lista de todas las tareas en el repositorio
        """
        ...
