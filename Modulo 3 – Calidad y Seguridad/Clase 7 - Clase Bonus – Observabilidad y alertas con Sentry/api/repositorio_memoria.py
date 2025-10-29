# api/repositorio_memoria.py
"""Repositorio de tareas con almacenamiento en memoria (volátil).

Este módulo implementa el patrón Repository usando almacenamiento en memoria.
Los datos NO persisten entre reinicios de la aplicación - útil para desarrollo y tests.
"""
from api.servicio_tareas import Tarea


class RepositorioMemoria:
    """Repositorio que almacena tareas en memoria (no persistente).

    Implementa el protocolo RepositorioTareas usando una lista en memoria.
    Los datos se pierden al reiniciar la aplicación.

    Attributes:
        _tareas: Lista de tareas en memoria
        _contador: Contador auto-incremental para IDs únicos

    Example:
        >>> repo = RepositorioMemoria()
        >>> tarea = Tarea(id=0, nombre="Test")
        >>> repo.guardar(tarea)
        >>> tarea.id  # ID asignado por el repositorio
        1
        >>> len(repo.listar())
        1

    Note:
        Este repositorio es útil para:
        - Desarrollo rápido (no requiere archivo/DB)
        - Tests unitarios (datos aislados por instancia)
        - Demos (datos temporales)

        NO usar en producción (datos volátiles).
    """

    def __init__(self) -> None:
        self._tareas: list[Tarea] = []
        self._contador: int = 0

    def guardar(self, tarea: Tarea) -> None:
        """Guarda una tarea en memoria, asignándole un ID único.

        El ID es auto-incremental y se asigna en el momento de guardar.

        Args:
            tarea: La tarea a guardar (se modifica in-place para asignar ID)

        Example:
            >>> repo = RepositorioMemoria()
            >>> tarea = Tarea(id=0, nombre="Escribir tests")
            >>> repo.guardar(tarea)
            >>> assert tarea.id == 1
        """
        self._contador += 1
        tarea.id = self._contador
        self._tareas.append(tarea)

    def listar(self) -> list[Tarea]:
        """Retorna todas las tareas almacenadas en memoria.

        Returns:
            Lista de tareas (vacía si no hay ninguna)

        Example:
            >>> repo = RepositorioMemoria()
            >>> tareas = repo.listar()
            >>> len(tareas)
            0
        """
        return self._tareas
