"""Servicio de gestión de tareas con lógica de negocio.

Este módulo implementa la capa de servicio que orquesta
la lógica de negocio para la gestión de tareas.
"""

from pydantic import BaseModel, Field
from datetime import date


__all__ = ['Tarea', 'ServicioTareas']


class Tarea(BaseModel):
    """Modelo de tarea con validaciones avanzadas.

    Representa una tarea del sistema con sus atributos principales
    y validaciones automáticas mediante Pydantic.

    Attributes:
        id: Identificador único autoincremental
        nombre: Nombre descriptivo de la tarea
        completada: Estado de completitud (default: False)
        prioridad: Nivel de prioridad 1-5 (default: 3)
        fecha_limite: Fecha límite opcional (YYYY-MM-DD)
        etiquetas: Lista de etiquetas para categorización

    Example:
        >>> tarea = Tarea(
        ...     id=1,
        ...     nombre="Estudiar Python",
        ...     prioridad=1,
        ...     fecha_limite=date(2025, 12, 31),
        ...     etiquetas=["python", "educación"]
        ... )
        >>> tarea.completada
        False
    """
    id: int
    nombre: str
    completada: bool = False
    prioridad: int = 3
    fecha_limite: date | None = None
    etiquetas: list[str] = Field(default_factory=list)


class ServicioTareas:
    """Servicio de gestión de tareas en memoria.

    Maneja la lógica de negocio para crear, listar y gestionar tareas.
    Implementa almacenamiento en memoria (no persistente) con ID autoincremental.

    Attributes:
        _tareas: Lista privada de tareas almacenadas
        _contador: Contador interno para generar IDs únicos

    Example:
        >>> servicio = ServicioTareas()
        >>> tarea = servicio.crear("Estudiar Python", prioridad=1)
        >>> tarea.id
        1
        >>> len(servicio.listar())
        1

    Note:
        Este servicio usa almacenamiento en memoria. Los datos se pierden
        al terminar la ejecución del programa.
    """

    def __init__(self) -> None:
        """Inicializa el servicio con almacenamiento vacío.

        Crea una lista vacía de tareas y establece el contador en 0.
        """
        self._tareas: list[Tarea] = []
        self._contador: int = 0

    def crear(
        self,
        nombre: str,
        prioridad: int = 3,
        fecha_limite: date | None = None,
        etiquetas: list[str] | None = None
    ) -> Tarea:
        """Crea una nueva tarea con ID autoincremental.

        Args:
            nombre: Nombre descriptivo de la tarea
            prioridad: Nivel de prioridad 1-5 (default: 3)
            fecha_limite: Fecha límite opcional en formato YYYY-MM-DD
            etiquetas: Lista opcional de etiquetas para categorización

        Returns:
            Tarea creada con ID asignado automáticamente

        Example:
            >>> servicio = ServicioTareas()
            >>> tarea = servicio.crear(
            ...     "Estudiar Python",
            ...     prioridad=1,
            ...     fecha_limite=date(2025, 12, 31),
            ...     etiquetas=["python", "educación"]
            ... )
            >>> tarea.id
            1
            >>> tarea.completada
            False

        Note:
            El ID se genera automáticamente de forma incremental.
            La tarea se crea en estado no completada por defecto.
        """
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

    def listar(self) -> list[Tarea]:
        """Retorna todas las tareas almacenadas.

        Returns:
            Lista de todas las tareas en el sistema (puede estar vacía)

        Example:
            >>> servicio = ServicioTareas()
            >>> servicio.crear("Tarea 1")
            >>> servicio.crear("Tarea 2")
            >>> len(servicio.listar())
            2

        Note:
            La lista retornada es la lista interna. Para prevenir
            mutaciones, considera retornar una copia en producción.
        """
        return self._tareas
