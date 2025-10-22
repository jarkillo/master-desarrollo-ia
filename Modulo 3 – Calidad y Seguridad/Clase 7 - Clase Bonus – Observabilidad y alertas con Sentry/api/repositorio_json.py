# api/repositorio_json.py
"""Repositorio de tareas con persistencia en archivo JSON.

Este módulo implementa el patrón Repository para almacenar tareas en un archivo
JSON local. Usa pathlib para operaciones de archivo cross-platform.
"""
from __future__ import annotations
import json
from pathlib import Path
from api.servicio_tareas import Tarea


class RepositorioJSON:
    """Repositorio que persiste tareas en un archivo JSON.

    Implementa el protocolo RepositorioTareas usando almacenamiento en archivo.
    Usa pathlib para operaciones de archivo seguras y cross-platform.

    Args:
        ruta_archivo: Ruta al archivo JSON (acepta str o Path)

    Example:
        >>> repo = RepositorioJSON("tareas.json")
        >>> tarea = Tarea(id=0, nombre="Test")
        >>> repo.guardar(tarea)
        >>> tareas = repo.listar()
    """

    def __init__(self, ruta_archivo: str | Path = "tareas.json") -> None:
        # Convertir a Path para operaciones robustas
        self._ruta = Path(ruta_archivo)

        # Asegurar que el directorio padre existe
        self._ruta.parent.mkdir(parents=True, exist_ok=True)

        # Inicializar archivo si no existe
        if not self._ruta.exists():
            self._ruta.write_text(
                json.dumps([], ensure_ascii=False, indent=2),
                encoding="utf-8"
            )

    def listar(self) -> list[Tarea]:
        """Obtiene todas las tareas almacenadas.

        Returns:
            Lista de tareas (vacía si no hay ninguna)

        Raises:
            RuntimeError: Si el archivo JSON está corrupto
        """
        try:
            contenido = self._ruta.read_text(encoding="utf-8").strip()
            datos = json.loads(contenido) if contenido else []
        except json.JSONDecodeError as e:
            raise RuntimeError(
                f"Archivo JSON corrupto en {self._ruta}: {e}"
            ) from e

        # Devolvemos objetos Tarea (Pydantic), no dicts
        return [Tarea(**d) for d in datos]

    def guardar(self, tarea: Tarea) -> None:
        """Guarda una nueva tarea en el archivo JSON.

        Asigna un ID único incremental a la tarea antes de guardarla.

        Args:
            tarea: La tarea a guardar (se modifica in-place para asignar ID)

        Note:
            Esta implementación tiene una race condition si múltiples procesos
            escriben simultáneamente. Para producción, usar una base de datos
            con transacciones.
        """
        # Leemos lo existente
        tareas = self.listar()

        # Generamos ID robusto (max + 1)
        nuevo_id = max((t.id for t in tareas), default=0) + 1
        tarea.id = nuevo_id
        tareas.append(tarea)

        # Guardamos todo (write_text es más conciso que with open)
        contenido_json = json.dumps(
            [t.model_dump() for t in tareas],
            ensure_ascii=False,
            indent=2
        )
        self._ruta.write_text(contenido_json, encoding="utf-8")
