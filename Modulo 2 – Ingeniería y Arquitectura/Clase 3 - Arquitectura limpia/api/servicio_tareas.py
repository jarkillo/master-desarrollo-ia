from pydantic import BaseModel
from typing import List


class Tarea(BaseModel):
    id: int
    nombre: str
    completada: bool = False


class ServicioTareas:
    def __init__(self):
        self._tareas: List[Tarea] = []
        self._contador = 0

    def crear(self, nombre: str) -> Tarea:
        self._contador += 1
        tarea = Tarea(id=self._contador, nombre=nombre)
        self._tareas.append(tarea)
        return tarea

    def listar(self) -> List[Tarea]:
        return self._tareas
