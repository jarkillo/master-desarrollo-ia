"""
Servicio de tareas (Service Layer).

Orquesta la lógica de negocio para la gestión de tareas.
"""

from math import ceil

from fastapi import HTTPException, status

from api.repositorio_base import RepositorioTareas
from api.schemas import PaginationParams, TareaCreate, TareaListResponse, TareaResponse, TareaUpdate


class ServicioTareas:
    """
    Servicio para gestión de tareas.

    Implementa la lógica de negocio:
    - CRUD de tareas
    - Filtros y búsqueda
    - Paginación
    - Soft delete
    """

    def __init__(self, repositorio: RepositorioTareas):
        """
        Inicializa el servicio con un repositorio.

        Args:
            repositorio: Repositorio de tareas
        """
        self._repo = repositorio

    def crear(
        self,
        datos: TareaCreate,
        usuario_id: int
    ) -> TareaResponse:
        """
        Crea una nueva tarea.

        Args:
            datos: Datos de la tarea a crear
            usuario_id: ID del usuario propietario

        Returns:
            Tarea creada
        """
        tarea = self._repo.crear(
            titulo=datos.titulo,
            descripcion=datos.descripcion,
            prioridad=datos.prioridad,
            usuario_id=usuario_id
        )
        return TareaResponse.model_validate(tarea)

    def obtener_por_id(
        self,
        tarea_id: int,
        usuario_id: int
    ) -> TareaResponse:
        """
        Obtiene una tarea por su ID.

        Args:
            tarea_id: ID de la tarea
            usuario_id: ID del usuario (para verificar propiedad)

        Returns:
            Tarea encontrada

        Raises:
            HTTPException 404: Si la tarea no existe o no pertenece al usuario
        """
        tarea = self._repo.obtener_por_id(tarea_id, usuario_id)
        if not tarea:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tarea {tarea_id} no encontrada"
            )
        return TareaResponse.model_validate(tarea)

    def listar(
        self,
        usuario_id: int,
        pagination: PaginationParams,
        completada: bool | None = None,
        prioridad: int | None = None,
        q: str | None = None
    ) -> TareaListResponse:
        """
        Lista tareas con filtros y paginación.

        Args:
            usuario_id: ID del usuario propietario
            pagination: Parámetros de paginación
            completada: Filtrar por estado (None = todas)
            prioridad: Filtrar por prioridad (None = todas)
            q: Búsqueda por texto en título (None = sin búsqueda)

        Returns:
            Lista paginada de tareas
        """
        # Calcular offset
        offset = (pagination.page - 1) * pagination.page_size

        # Si hay búsqueda, usar el método de búsqueda
        if q:
            tareas = self._repo.buscar(
                usuario_id=usuario_id,
                query=q,
                limite=pagination.page_size,
                offset=offset
            )
            # Contar total de resultados de búsqueda (para paginación correcta)
            total = self._repo.contar_busqueda(usuario_id, q)
        else:
            # Listar con filtros
            tareas = self._repo.listar(
                usuario_id=usuario_id,
                completada=completada,
                prioridad=prioridad,
                incluir_eliminadas=False,
                limite=pagination.page_size,
                offset=offset
            )
            # Contar total para calcular páginas
            total = self._repo.contar(
                usuario_id=usuario_id,
                completada=completada,
                prioridad=prioridad,
                incluir_eliminadas=False
            )

        # Calcular total de páginas
        total_pages = ceil(total / pagination.page_size) if total > 0 else 1

        return TareaListResponse(
            items=[TareaResponse.model_validate(t) for t in tareas],
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            total_pages=total_pages
        )

    def actualizar(
        self,
        tarea_id: int,
        datos: TareaUpdate,
        usuario_id: int
    ) -> TareaResponse:
        """
        Actualiza una tarea existente.

        Args:
            tarea_id: ID de la tarea
            datos: Datos a actualizar (campos opcionales)
            usuario_id: ID del usuario (para verificar propiedad)

        Returns:
            Tarea actualizada

        Raises:
            HTTPException 404: Si la tarea no existe o no pertenece al usuario
        """
        tarea = self._repo.obtener_por_id(tarea_id, usuario_id)
        if not tarea:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tarea {tarea_id} no encontrada"
            )

        # Actualizar solo los campos enviados (PATCH semántico)
        if datos.titulo is not None:
            tarea.titulo = datos.titulo
        if datos.descripcion is not None:
            tarea.descripcion = datos.descripcion
        if datos.completada is not None:
            tarea.completada = datos.completada
        if datos.prioridad is not None:
            tarea.prioridad = datos.prioridad

        tarea_actualizada = self._repo.actualizar(tarea)
        return TareaResponse.model_validate(tarea_actualizada)

    def eliminar(
        self,
        tarea_id: int,
        usuario_id: int
    ) -> None:
        """
        Elimina una tarea (soft delete).

        Args:
            tarea_id: ID de la tarea
            usuario_id: ID del usuario (para verificar propiedad)

        Raises:
            HTTPException 404: Si la tarea no existe o no pertenece al usuario
        """
        resultado = self._repo.eliminar(tarea_id, usuario_id)
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tarea {tarea_id} no encontrada"
            )

    def restaurar(
        self,
        tarea_id: int,
        usuario_id: int
    ) -> TareaResponse:
        """
        Restaura una tarea eliminada.

        Args:
            tarea_id: ID de la tarea
            usuario_id: ID del usuario (para verificar propiedad)

        Returns:
            Tarea restaurada

        Raises:
            HTTPException 404: Si la tarea no existe o no pertenece al usuario
        """
        resultado = self._repo.restaurar(tarea_id, usuario_id)
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tarea {tarea_id} no encontrada en la papelera"
            )

        # Obtener tarea restaurada
        tarea = self._repo.obtener_por_id(tarea_id, usuario_id)
        return TareaResponse.model_validate(tarea)

    def listar_papelera(
        self,
        usuario_id: int,
        pagination: PaginationParams
    ) -> TareaListResponse:
        """
        Lista tareas eliminadas (papelera).

        Args:
            usuario_id: ID del usuario propietario
            pagination: Parámetros de paginación

        Returns:
            Lista paginada de tareas eliminadas
        """
        offset = (pagination.page - 1) * pagination.page_size

        tareas = self._repo.listar_papelera(
            usuario_id=usuario_id,
            limite=pagination.page_size,
            offset=offset
        )

        # Contar total de eliminadas
        total = self._repo.contar(
            usuario_id=usuario_id,
            incluir_eliminadas=True
        )

        total_pages = ceil(total / pagination.page_size) if total > 0 else 1

        return TareaListResponse(
            items=[TareaResponse.model_validate(t) for t in tareas],
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            total_pages=total_pages
        )
