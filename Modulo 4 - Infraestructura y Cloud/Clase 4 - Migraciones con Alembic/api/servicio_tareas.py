# api/servicio_tareas.py
"""
Capa de servicio con lógica de negocio.

Esta capa NO conoce la base de datos directamente.
Solo depende del Protocol RepositorioTareas (Dependency Inversion).
"""
from typing import List, Optional
from pydantic import BaseModel, Field
from api.repositorio_base import RepositorioTareas


class Tarea(BaseModel):
    """
    Modelo de dominio para una tarea (Pydantic).

    Este es el modelo que usa la lógica de negocio,
    independiente de cómo se persiste (BD, JSON, memoria, etc.)
    """
    id: int
    nombre: str = Field(..., min_length=1, max_length=100)
    completada: bool = False


class TareaCreate(BaseModel):
    """Request para crear una tarea"""
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre de la tarea")


class TareaUpdate(BaseModel):
    """Request para actualizar una tarea"""
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    completada: Optional[bool] = None


class ServicioTareas:
    """
    Servicio con la lógica de negocio para tareas.

    Depende del repositorio mediante el Protocol (interfaz),
    no de una implementación concreta (Dependency Inversion).
    """

    def __init__(self, repositorio: RepositorioTareas):
        """
        Inicializa el servicio con un repositorio.

        Args:
            repositorio: Cualquier implementación de RepositorioTareas
        """
        self._repo = repositorio

    def crear(self, nombre: str) -> Tarea:
        """
        Crea una nueva tarea.

        Args:
            nombre: Nombre de la tarea

        Returns:
            Tarea creada con su ID asignado
        """
        nueva = Tarea(id=0, nombre=nombre)  # ID=0 indica nueva tarea
        self._repo.guardar(nueva)
        return nueva

    def listar(self) -> List[Tarea]:
        """
        Lista todas las tareas.

        Returns:
            Lista de todas las tareas
        """
        return self._repo.listar()

    def obtener(self, id: int) -> Optional[Tarea]:
        """
        Obtiene una tarea por ID.

        Args:
            id: ID de la tarea

        Returns:
            Tarea si existe, None si no
        """
        return self._repo.obtener_por_id(id)

    def actualizar(self, id: int, datos: TareaUpdate) -> Optional[Tarea]:
        """
        Actualiza una tarea existente.

        Args:
            id: ID de la tarea
            datos: Datos a actualizar

        Returns:
            Tarea actualizada si existía, None si no
        """
        tarea = self._repo.obtener_por_id(id)
        if not tarea:
            return None

        # Actualizar solo los campos proporcionados
        if datos.nombre is not None:
            tarea.nombre = datos.nombre
        if datos.completada is not None:
            tarea.completada = datos.completada

        self._repo.actualizar(tarea)
        return tarea

    def eliminar(self, id: int) -> bool:
        """
        Elimina una tarea.

        Args:
            id: ID de la tarea

        Returns:
            True si se eliminó, False si no existía
        """
        return self._repo.eliminar(id)
