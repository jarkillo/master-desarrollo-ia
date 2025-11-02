# api/servicio_tareas.py

from pydantic import BaseModel

from api.repositorio_base import RepositorioTareas


class Tarea(BaseModel):
    id: int
    nombre: str
    completada: bool = False


class ServicioTareas:
    def __init__(self, repositorio: RepositorioTareas):
        self._repo = repositorio

    def crear(self, nombre: str) -> Tarea:
        nueva = Tarea(id=0, nombre=nombre)  # el repo asigna ID real
        self._repo.guardar(nueva)
        return nueva

    def listar(self) -> list[Tarea]:
        return self._repo.listar()
