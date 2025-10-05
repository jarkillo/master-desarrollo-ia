# repositorio_memoria.py
from typing import List
from api.servicio_tareas import Tarea


class RepositorioMemoria:
    def __init__(self):
        self._tareas: List[Tarea] = []
        self._contador = 0

    def guardar(self, tarea: Tarea) -> None:
        self._contador += 1
        tarea.id = self._contador
        self._tareas.append(tarea)

    def listar(self) -> List[Tarea]:
        return self._tareas
