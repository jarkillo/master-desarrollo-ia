# api/repositorio_json.py
from __future__ import annotations
import json, os
from typing import List
from api.servicio_tareas import Tarea  # usamos el mismo modelo Pydantic


class RepositorioJSON:
    """Repositorio que persiste tareas en un archivo JSON sencillo."""

    def __init__(self, ruta_archivo: str = "tareas.json"):
        self._ruta = ruta_archivo
        # si no existe, lo creamos vacío
        if not os.path.exists(self._ruta):
            with open(self._ruta, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def listar(self) -> List[Tarea]:
        with open(self._ruta, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
            datos = json.loads(contenido) if contenido else []
        # devolvemos objetos Tarea (Pydantic), no dicts
        return [Tarea(**d) for d in datos]

    def guardar(self, tarea: Tarea) -> None:
        # leemos lo existente
        tareas = self.listar()
        # generamos ID robusto (max + 1)
        nuevo_id = max((t.id for t in tareas), default=0) + 1
        tarea.id = nuevo_id
        tareas.append(tarea)
        # guardamos todo
        with open(self._ruta, "w", encoding="utf-8") as f:
            json.dump([t.model_dump() for t in tareas], f, ensure_ascii=False, indent=2)
