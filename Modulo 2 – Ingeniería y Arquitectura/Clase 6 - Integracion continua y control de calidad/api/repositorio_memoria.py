# api/repositorio_memoria.py

from api.servicio_tareas import Tarea


class RepositorioMemoria:
    def __init__(self):
        self._tareas: list[Tarea] = []
        self._contador = 0

    def guardar(self, tarea: Tarea) -> None:
        self._contador += 1
        tarea.id = self._contador
        self._tareas.append(tarea)

    def listar(self) -> list[Tarea]:
        return self._tareas
