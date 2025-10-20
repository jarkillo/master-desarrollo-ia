from pydantic import BaseModel, Field
from typing import List
from datetime import date


class Tarea(BaseModel):
    """Modelo de tarea con validaciones avanzadas."""
    id: int
    nombre: str
    completada: bool = False
    prioridad: int = 3
    fecha_limite: date | None = None
    etiquetas: list[str] = Field(default_factory=list)


class ServicioTareas:
    def __init__(self):
        self._tareas: List[Tarea] = []
        self._contador = 0

    def crear(
        self,
        nombre: str,
        prioridad: int = 3,
        fecha_limite: date | None = None,
        etiquetas: list[str] | None = None
    ) -> Tarea:
        """Crea una nueva tarea con validaciones avanzadas."""
        self._contador += 1
        tarea = Tarea(
            id=self._contador,
            nombre=nombre,
            prioridad=prioridad,
            fecha_limite=fecha_limite,
            etiquetas=etiquetas or []
        )
        self._tareas.append(tarea)
        return tarea

    def listar(self) -> List[Tarea]:
        return self._tareas
