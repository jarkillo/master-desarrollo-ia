# servicio_tareas.py
from typing import List
from api.repositorio_base import RepositorioTareas
from api.servicio_tareas import Tarea


class ServicioTareas:
    def __init__(self, repositorio: RepositorioTareas):
        self._repositorio = repositorio

    def crear(self, nombre: str) -> Tarea:
        tarea = Tarea(id=0, nombre=nombre)
        self._repositorio.guardar(tarea)
        return tarea

    def listar(self) -> List[Tarea]:
        return self._repositorio.listar()
