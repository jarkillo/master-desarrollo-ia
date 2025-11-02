# api/repositorio_base.py
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    # Solo para tipos (no se ejecuta en runtime, evita el ciclo)
    from api.servicio_tareas import Tarea


class RepositorioTareas(Protocol):
    def guardar(self, tarea: "Tarea") -> None: ...
    def listar(self) -> list["Tarea"]: ...
