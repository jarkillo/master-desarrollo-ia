# repositorio_base.py
from typing import Protocol, List
from api.servicio_tareas import Tarea


class RepositorioTareas(Protocol):
    def guardar(self, tarea: Tarea) -> None: ...
    def listar(self) -> List[Tarea]: ...
