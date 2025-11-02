# api/repositorio_memoria.py
"""Implementación en memoria del repositorio de tareas.

Esta implementación cumple el contrato RepositorioTareas usando
almacenamiento en memoria (listas de Python). Los datos se pierden
al reiniciar la aplicación.
"""

from api.servicio_tareas import Tarea


class RepositorioMemoria:
    """Repositorio que almacena tareas en memoria (RAM).

    Características:
    - Muy rápido (todo en RAM)
    - Perfecto para tests y demos
    - Thread-safe básico (Python GIL protege operaciones simples)

    Limitaciones:
    - Los datos se pierden al reiniciar (no hay persistencia)
    - No apto para producción
    """

    def __init__(self):
        """Inicializa el repositorio con una lista vacía."""
        self._tareas: list[Tarea] = []
        self._contador: int = 0

    def guardar(self, tarea: Tarea) -> None:
        """Guarda una tarea en memoria (crea o actualiza).

        Args:
            tarea: Tarea a guardar
                - Si id == 0: asigna ID autoincremental y la crea
                - Si id > 0: actualiza si existe, o la crea si no
        """
        if tarea.id == 0:
            # Caso: tarea nueva → asignar ID
            self._contador += 1
            tarea.id = self._contador
            self._tareas.append(tarea)
        else:
            # Caso: actualizar existente o crear
            for i, t in enumerate(self._tareas):
                if t.id == tarea.id:
                    self._tareas[i] = tarea
                    return
            # Si no existía, la agregamos
            self._tareas.append(tarea)

    def listar(self) -> list[Tarea]:
        """Devuelve todas las tareas almacenadas.

        Returns:
            Copia defensiva de la lista de tareas (para evitar modificaciones externas)
        """
        return self._tareas.copy()

    def obtener_por_id(self, id: int) -> Tarea | None:
        """Busca una tarea por su ID.

        Args:
            id: ID de la tarea a buscar

        Returns:
            La tarea si existe, None si no se encuentra
        """
        for tarea in self._tareas:
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
        for i, tarea in enumerate(self._tareas):
            if tarea.id == id:
                self._tareas.pop(i)
                return True
        return False

    def completar(self, id: int) -> Tarea | None:
        """Marca una tarea como completada.

        Args:
            id: ID de la tarea a completar

        Returns:
            La tarea actualizada si existía, None si no fue encontrada

        Nota:
            Modifica la tarea in-place (Pydantic permite mutabilidad)
        """
        for tarea in self._tareas:
            if tarea.id == id:
                tarea.completada = True
                return tarea
        return None
