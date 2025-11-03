"""
Protocolos base para repositorios (Dependency Inversion Principle).

Define las interfaces que deben implementar los repositorios,
permitiendo cambiar la implementación sin afectar la lógica de negocio.
"""

from typing import Protocol

from api.models import TareaModel, UsuarioModel


class RepositorioUsuarios(Protocol):
    """
    Protocolo para el repositorio de usuarios.

    Define las operaciones que debe implementar cualquier
    repositorio de usuarios (BD, memoria, API externa, etc.).
    """

    def crear(self, email: str, nombre: str, password_hash: str) -> UsuarioModel:
        """Crea un nuevo usuario."""
        ...

    def obtener_por_id(self, user_id: int) -> UsuarioModel | None:
        """Obtiene un usuario por su ID."""
        ...

    def obtener_por_email(self, email: str) -> UsuarioModel | None:
        """Obtiene un usuario por su email."""
        ...

    def listar(self, solo_activos: bool = True) -> list[UsuarioModel]:
        """Lista usuarios (opcionalmente solo activos)."""
        ...

    def actualizar(self, usuario: UsuarioModel) -> UsuarioModel:
        """Actualiza un usuario existente."""
        ...

    def desactivar(self, user_id: int) -> bool:
        """Desactiva un usuario (soft delete)."""
        ...


class RepositorioTareas(Protocol):
    """
    Protocolo para el repositorio de tareas.

    Define las operaciones que debe implementar cualquier
    repositorio de tareas.
    """

    def crear(
        self,
        titulo: str,
        usuario_id: int,
        descripcion: str | None = None,
        prioridad: int = 2
    ) -> TareaModel:
        """Crea una nueva tarea."""
        ...

    def obtener_por_id(self, tarea_id: int, usuario_id: int) -> TareaModel | None:
        """
        Obtiene una tarea por su ID.

        Args:
            tarea_id: ID de la tarea
            usuario_id: ID del usuario (para verificar propiedad)

        Returns:
            Tarea si existe y pertenece al usuario, None en caso contrario
        """
        ...

    def listar(
        self,
        usuario_id: int,
        completada: bool | None = None,
        prioridad: int | None = None,
        incluir_eliminadas: bool = False,
        limite: int = 10,
        offset: int = 0
    ) -> list[TareaModel]:
        """
        Lista tareas con filtros opcionales.

        Args:
            usuario_id: ID del usuario propietario
            completada: Filtrar por estado de completitud (None = todas)
            prioridad: Filtrar por prioridad (None = todas)
            incluir_eliminadas: Si True, incluye tareas eliminadas
            limite: Número máximo de resultados
            offset: Offset para paginación

        Returns:
            Lista de tareas que cumplen los criterios
        """
        ...

    def contar(
        self,
        usuario_id: int,
        completada: bool | None = None,
        prioridad: int | None = None,
        incluir_eliminadas: bool = False
    ) -> int:
        """Cuenta tareas que cumplen los criterios (para paginación)."""
        ...

    def buscar(
        self,
        usuario_id: int,
        query: str,
        limite: int = 10,
        offset: int = 0
    ) -> list[TareaModel]:
        """
        Busca tareas por texto en el título.

        Args:
            usuario_id: ID del usuario propietario
            query: Texto a buscar (case-insensitive)
            limite: Número máximo de resultados
            offset: Offset para paginación

        Returns:
            Lista de tareas que coinciden con la búsqueda
        """
        ...

    def contar_busqueda(self, usuario_id: int, query: str) -> int:
        """
        Cuenta tareas que coinciden con la búsqueda (para paginación).

        Args:
            usuario_id: ID del usuario propietario
            query: Texto a buscar

        Returns:
            Total de tareas que coinciden
        """
        ...

    def actualizar(self, tarea: TareaModel) -> TareaModel:
        """Actualiza una tarea existente."""
        ...

    def eliminar(self, tarea_id: int, usuario_id: int) -> bool:
        """Elimina una tarea (soft delete)."""
        ...

    def restaurar(self, tarea_id: int, usuario_id: int) -> bool:
        """Restaura una tarea eliminada."""
        ...

    def listar_papelera(
        self,
        usuario_id: int,
        limite: int = 10,
        offset: int = 0
    ) -> list[TareaModel]:
        """Lista tareas eliminadas (papelera)."""
        ...
