"""
Implementación in-memory del repositorio de tareas.
Usa un diccionario para almacenar las tareas en memoria.
"""
from api.repositorio_base import Tarea


class RepositorioMemoria:
    """
    Repositorio que almacena tareas en memoria (diccionario).

    Ideal para:
    - Desarrollo y pruebas
    - Demos
    - Prototipado rápido

    No persistente: los datos se pierden al reiniciar.
    """

    def __init__(self) -> None:
        self._tareas: dict[int, Tarea] = {}
        self._siguiente_id: int = 1

    def crear(self, nombre: str) -> Tarea:
        """Crea una nueva tarea con ID autogenerado."""
        tarea = Tarea(
            id=self._siguiente_id,
            nombre=nombre,
            completada=False
        )
        self._tareas[tarea.id] = tarea
        self._siguiente_id += 1
        return tarea

    def listar(self) -> list[Tarea]:
        """Retorna todas las tareas ordenadas por ID."""
        return sorted(self._tareas.values(), key=lambda t: t.id)

    def obtener(self, tarea_id: int) -> Tarea | None:
        """Obtiene una tarea por ID. Retorna None si no existe."""
        return self._tareas.get(tarea_id)

    def actualizar(self, tarea_id: int, nombre: str | None = None,
                   completada: bool | None = None) -> Tarea | None:
        """
        Actualiza una tarea existente.

        Solo actualiza los campos provistos (parcial).
        Retorna None si la tarea no existe.
        """
        tarea = self._tareas.get(tarea_id)
        if not tarea:
            return None

        # Actualizar solo campos provistos
        if nombre is not None:
            tarea.nombre = nombre
        if completada is not None:
            tarea.completada = completada

        return tarea

    def eliminar(self, tarea_id: int) -> bool:
        """Elimina una tarea. Retorna True si se eliminó, False si no existía."""
        if tarea_id in self._tareas:
            del self._tareas[tarea_id]
            return True
        return False

    def contar_estadisticas(self) -> dict[str, int]:
        """
        Calcula estadísticas en una sola iteración.

        Optimizado: O(n) con una sola pasada vs O(3n) de múltiples iteraciones.

        Returns:
            Diccionario con total, completadas y pendientes.
        """
        total = len(self._tareas)
        completadas = sum(1 for t in self._tareas.values() if t.completada)

        return {
            "total": total,
            "completadas": completadas,
            "pendientes": total - completadas  # Cálculo derivado
        }
