# api/repositorio_base.py
from typing import TYPE_CHECKING, Optional, Protocol

if TYPE_CHECKING:
    # Solo para tipos (no se ejecuta en runtime, evita el ciclo)
    from api.servicio_tareas import Tarea


class RepositorioTareas(Protocol):
    """Protocol que define la interfaz de un repositorio de tareas.

    Implementa el principio de Inversión de Dependencias (SOLID):
    Las capas superiores dependen de abstracciones, no de implementaciones concretas.
    """

    def guardar(self, tarea: "Tarea") -> None:
        """Guarda una nueva tarea o actualiza una existente."""
        ...

    def listar(self) -> list["Tarea"]:
        """Retorna todas las tareas almacenadas."""
        ...

    def obtener(self, id: int) -> Optional["Tarea"]:
        """Obtiene una tarea por su ID."""
        ...

    def eliminar(self, id: int) -> bool:
        """Elimina una tarea por su ID. Retorna True si se eliminó."""
        ...
