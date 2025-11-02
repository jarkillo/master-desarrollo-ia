# api/servicio_tareas.py

from pydantic import BaseModel, Field

from api.repositorio_base import RepositorioTareas


class Tarea(BaseModel):
    """Modelo de dominio para una tarea.

    Usa Pydantic para:
    - Validación automática de datos
    - Serialización JSON
    - Documentación OpenAPI automática
    """
    id: int = Field(default=0, description="ID único de la tarea (0 = no asignado)")
    nombre: str = Field(..., min_length=1, max_length=200, description="Nombre de la tarea")
    completada: bool = Field(default=False, description="Estado de completitud")


class ServicioTareas:
    """Capa de servicio que contiene la lógica de negocio.

    Ventajas de esta arquitectura:
    - Lógica de negocio separada de la API
    - Testeable sin levantar servidor HTTP
    - Reutilizable desde diferentes interfaces (API, CLI, tests)
    """

    def __init__(self, repositorio: RepositorioTareas):
        """Inyección de dependencias: recibe cualquier implementación del repositorio."""
        self._repo = repositorio

    def crear(self, nombre: str) -> Tarea:
        """Crea una nueva tarea con validación básica."""
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la tarea no puede estar vacío")

        nueva = Tarea(id=0, nombre=nombre.strip())
        self._repo.guardar(nueva)
        return nueva

    def listar(self) -> list[Tarea]:
        """Lista todas las tareas."""
        return self._repo.listar()

    def obtener(self, id: int) -> Tarea | None:
        """Obtiene una tarea por ID."""
        return self._repo.obtener(id)

    def marcar_completada(self, id: int, completada: bool) -> Tarea | None:
        """Marca una tarea como completada o no completada."""
        tarea = self._repo.obtener(id)
        if tarea is None:
            return None

        tarea.completada = completada
        self._repo.guardar(tarea)
        return tarea

    def eliminar(self, id: int) -> bool:
        """Elimina una tarea. Retorna True si se eliminó."""
        return self._repo.eliminar(id)
