"""
Capa de servicio con lógica de negocio para tareas.
"""
from api.repositorio_base import RepositorioTareas, Tarea


class ErrorValidacion(Exception):
    """Error personalizado para validaciones de negocio."""
    pass


class ServicioTareas:
    """
    Servicio que encapsula la lógica de negocio.

    Responsabilidades:
    - Validaciones de negocio
    - Orquestación de operaciones
    - Transformaciones de datos

    NO depende de implementación concreta (solo del Protocol).
    """

    def __init__(self, repositorio: RepositorioTareas) -> None:
        self._repo = repositorio

    def crear_tarea(self, nombre: str) -> Tarea:
        """
        Crea una nueva tarea con validaciones.

        Raises:
            ErrorValidacion: Si el nombre está vacío o solo tiene espacios.
        """
        nombre_limpio = nombre.strip()

        if not nombre_limpio:
            raise ErrorValidacion("El nombre de la tarea no puede estar vacío")

        if len(nombre_limpio) > 200:
            raise ErrorValidacion("El nombre de la tarea no puede exceder 200 caracteres")

        return self._repo.crear(nombre_limpio)

    def listar_tareas(self) -> list[Tarea]:
        """Retorna todas las tareas."""
        return self._repo.listar()

    def obtener_tarea(self, tarea_id: int) -> Tarea | None:
        """Obtiene una tarea por ID."""
        return self._repo.obtener(tarea_id)

    def actualizar_tarea(self, tarea_id: int, nombre: str | None = None,
                         completada: bool | None = None) -> Tarea | None:
        """
        Actualiza una tarea existente.

        Raises:
            ErrorValidacion: Si el nombre nuevo está vacío.
        """
        # Validar nombre si se provee
        if nombre is not None:
            nombre_limpio = nombre.strip()
            if not nombre_limpio:
                raise ErrorValidacion("El nombre de la tarea no puede estar vacío")
            if len(nombre_limpio) > 200:
                raise ErrorValidacion("El nombre no puede exceder 200 caracteres")
            nombre = nombre_limpio

        return self._repo.actualizar(tarea_id, nombre, completada)

    def eliminar_tarea(self, tarea_id: int) -> bool:
        """Elimina una tarea. Retorna True si se eliminó."""
        return self._repo.eliminar(tarea_id)

    def contar_tareas(self) -> dict[str, int]:
        """
        Retorna estadísticas de tareas sin cargar objetos completos.

        Optimizado: Usa método del repositorio que calcula en una sola pasada.
        """
        # Si el repositorio tiene método optimizado, usarlo
        if hasattr(self._repo, 'contar_estadisticas'):
            return self._repo.contar_estadisticas()

        # Fallback: calcular desde lista completa (menos eficiente)
        tareas = self.listar_tareas()
        total = len(tareas)
        completadas = sum(1 for t in tareas if t.completada)
        return {
            "total": total,
            "completadas": completadas,
            "pendientes": total - completadas
        }
