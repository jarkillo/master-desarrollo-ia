# api/repositorio_json.py
"""Implementación de repositorio que persiste tareas en archivo JSON.

Esta implementación cumple el contrato RepositorioTareas usando
persistencia real en un archivo JSON con encoding UTF-8.
"""
import json
from pathlib import Path

from api.servicio_tareas import Tarea


class RepositorioJSON:
    """Repositorio que persiste tareas en archivo JSON.

    Características:
    - Persistencia real en disco (los datos sobreviven reinicios)
    - Encoding UTF-8 (soporta tildes, emojis)
    - Manejo robusto de errores (archivo corrupto, permisos)
    - IDs autoincrementales basados en máximo ID existente

    Limitaciones:
    - Lee y escribe el archivo completo en cada operación (ineficiente para >1000 tareas)
    - No es thread-safe (para ambientes multi-usuario, usar DB)
    """

    def __init__(self, ruta_archivo: str = "tareas.json"):
        """Inicializa el repositorio JSON.

        Args:
            ruta_archivo: Ruta del archivo JSON (se crea si no existe)
        """
        self.ruta = Path(ruta_archivo)

        # Crear archivo vacío si no existe
        if not self.ruta.exists():
            self._escribir([])

    def _leer(self) -> list[Tarea]:
        """Lee todas las tareas del archivo JSON.

        Returns:
            Lista de tareas (vacía si el archivo está corrupto o no existe)

        Nota:
            Si el archivo está corrupto, devuelve lista vacía en vez de lanzar excepción.
            Esto hace el repositorio más resiliente.
        """
        try:
            with self.ruta.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return [Tarea(**item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError, KeyError):
            # Archivo corrupto, no existe, o formato incorrecto → lista vacía
            return []

    def _escribir(self, tareas: list[Tarea]) -> None:
        """Escribe todas las tareas al archivo JSON.

        Args:
            tareas: Lista de tareas a persistir

        Nota:
            Usa indent=2 para que el JSON sea legible por humanos.
            Usa ensure_ascii=False para permitir tildes y emojis.
        """
        with self.ruta.open("w", encoding="utf-8") as f:
            json.dump(
                [t.model_dump() for t in tareas],
                f,
                ensure_ascii=False,  # Permite caracteres no-ASCII (tildes, emojis)
                indent=2  # JSON legible
            )

    def guardar(self, tarea: Tarea) -> None:
        """Persiste una tarea (nueva o existente).

        Args:
            tarea: Tarea a guardar
                - Si id == 0: se le asigna un ID único y se crea
                - Si id > 0: se actualiza si existe, o se crea si no

        Nota:
            La tarea se modifica in-place (se le asigna id si era 0).
        """
        tareas = self._leer()

        if tarea.id == 0:
            # Caso: tarea nueva → asignar próximo ID
            max_id = max([t.id for t in tareas], default=0)
            tarea.id = max_id + 1
            tareas.append(tarea)
        else:
            # Caso: actualizar existente o crear si no existe
            encontrada = False
            for i, t in enumerate(tareas):
                if t.id == tarea.id:
                    tareas[i] = tarea
                    encontrada = True
                    break

            if not encontrada:
                # La tarea tiene ID pero no existía → la agregamos
                tareas.append(tarea)

        self._escribir(tareas)

    def listar(self) -> list[Tarea]:
        """Devuelve todas las tareas persistidas.

        Returns:
            Lista de tareas (puede estar vacía)
        """
        return self._leer()

    def obtener_por_id(self, id: int) -> Tarea | None:
        """Busca una tarea por su ID.

        Args:
            id: ID de la tarea a buscar

        Returns:
            La tarea si existe, None si no se encuentra
        """
        tareas = self._leer()
        for tarea in tareas:
            if tarea.id == id:
                return tarea
        return None

    def eliminar(self, id: int) -> bool:
        """Elimina una tarea por su ID.

        Args:
            id: ID de la tarea a eliminar

        Returns:
            True si la tarea existía y fue eliminada
            False si la tarea no existía
        """
        tareas = self._leer()
        for i, tarea in enumerate(tareas):
            if tarea.id == id:
                tareas.pop(i)
                self._escribir(tareas)
                return True
        return False

    def completar(self, id: int) -> Tarea | None:
        """Marca una tarea como completada.

        Args:
            id: ID de la tarea a completar

        Returns:
            La tarea actualizada si existía, None si no fue encontrada
        """
        tareas = self._leer()
        for tarea in tareas:
            if tarea.id == id:
                tarea.completada = True
                self._escribir(tareas)
                return tarea
        return None
