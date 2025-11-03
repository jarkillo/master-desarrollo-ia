"""
Repositorio de tareas con SQLAlchemy.

Implementa las operaciones CRUD avanzadas para tareas:
- Filtros por completada, prioridad
- Búsqueda por texto
- Paginación
- Soft delete
"""


from sqlalchemy import and_
from sqlalchemy.orm import Session

from api.models import TareaModel


class RepositorioTareasDB:
    """
    Implementación del repositorio de tareas con SQLAlchemy.

    Maneja la persistencia de tareas con funcionalidades avanzadas.
    """

    def __init__(self, session: Session):
        """
        Inicializa el repositorio con una sesión de BD.

        Args:
            session: Sesión activa de SQLAlchemy
        """
        self._session = session

    def crear(
        self,
        titulo: str,
        usuario_id: int,
        descripcion: str | None = None,
        prioridad: int = 2
    ) -> TareaModel:
        """
        Crea una nueva tarea en la base de datos.

        Args:
            titulo: Título de la tarea
            usuario_id: ID del usuario propietario
            descripcion: Descripción opcional
            prioridad: Prioridad (1=Baja, 2=Media, 3=Alta)

        Returns:
            Tarea creada con ID asignado
        """
        tarea = TareaModel(
            titulo=titulo,
            descripcion=descripcion,
            usuario_id=usuario_id,
            prioridad=prioridad,
            completada=False,
            eliminada=False
        )
        self._session.add(tarea)
        self._session.commit()
        self._session.refresh(tarea)
        return tarea

    def obtener_por_id(self, tarea_id: int, usuario_id: int) -> TareaModel | None:
        """
        Obtiene una tarea por su ID.

        Args:
            tarea_id: ID de la tarea
            usuario_id: ID del usuario (para verificar propiedad)

        Returns:
            Tarea si existe y pertenece al usuario, None en caso contrario
        """
        return self._session.query(TareaModel).filter(
            and_(
                TareaModel.id == tarea_id,
                TareaModel.usuario_id == usuario_id,
                TareaModel.eliminada == False  # No devolver eliminadas
            )
        ).first()

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
        Lista tareas con filtros opcionales y paginación.

        Args:
            usuario_id: ID del usuario propietario
            completada: Filtrar por estado (None = todas)
            prioridad: Filtrar por prioridad (None = todas)
            incluir_eliminadas: Si True, incluye eliminadas
            limite: Número máximo de resultados
            offset: Offset para paginación

        Returns:
            Lista de tareas que cumplen los criterios
        """
        query = self._session.query(TareaModel).filter(
            TareaModel.usuario_id == usuario_id
        )

        # Aplicar filtros
        if not incluir_eliminadas:
            query = query.filter(TareaModel.eliminada == False)

        if completada is not None:
            query = query.filter(TareaModel.completada == completada)

        if prioridad is not None:
            query = query.filter(TareaModel.prioridad == prioridad)

        # Ordenar y paginar
        query = query.order_by(
            TareaModel.prioridad.desc(),  # Prioridad más alta primero
            TareaModel.creado_en.desc()   # Más recientes primero
        ).limit(limite).offset(offset)

        return query.all()

    def contar(
        self,
        usuario_id: int,
        completada: bool | None = None,
        prioridad: int | None = None,
        incluir_eliminadas: bool = False
    ) -> int:
        """
        Cuenta tareas que cumplen los criterios.

        Usa los mismos filtros que listar() para calcular total_pages.

        Args:
            usuario_id: ID del usuario propietario
            completada: Filtrar por estado (None = todas)
            prioridad: Filtrar por prioridad (None = todas)
            incluir_eliminadas: Si True, incluye eliminadas

        Returns:
            Número de tareas que cumplen los criterios
        """
        query = self._session.query(TareaModel).filter(
            TareaModel.usuario_id == usuario_id
        )

        if not incluir_eliminadas:
            query = query.filter(TareaModel.eliminada == False)

        if completada is not None:
            query = query.filter(TareaModel.completada == completada)

        if prioridad is not None:
            query = query.filter(TareaModel.prioridad == prioridad)

        return query.count()

    def buscar(
        self,
        usuario_id: int,
        query: str,
        limite: int = 10,
        offset: int = 0
    ) -> list[TareaModel]:
        """
        Busca tareas por texto en el título (case-insensitive).

        Args:
            usuario_id: ID del usuario propietario
            query: Texto a buscar
            limite: Número máximo de resultados
            offset: Offset para paginación

        Returns:
            Lista de tareas que coinciden con la búsqueda
        """
        search_query = self._session.query(TareaModel).filter(
            and_(
                TareaModel.usuario_id == usuario_id,
                TareaModel.eliminada == False,
                TareaModel.titulo.ilike(f"%{query}%")  # Case-insensitive LIKE
            )
        ).order_by(
            TareaModel.prioridad.desc(),
            TareaModel.creado_en.desc()
        ).limit(limite).offset(offset)

        return search_query.all()

    def contar_busqueda(
        self,
        usuario_id: int,
        query: str
    ) -> int:
        """
        Cuenta tareas que coinciden con la búsqueda.

        Args:
            usuario_id: ID del usuario propietario
            query: Texto a buscar

        Returns:
            Número de tareas que coinciden con la búsqueda
        """
        return self._session.query(TareaModel).filter(
            and_(
                TareaModel.usuario_id == usuario_id,
                TareaModel.eliminada == False,
                TareaModel.titulo.ilike(f"%{query}%")
            )
        ).count()

    def actualizar(self, tarea: TareaModel) -> TareaModel:
        """
        Actualiza una tarea existente.

        Args:
            tarea: Tarea con los cambios (debe tener ID)

        Returns:
            Tarea actualizada

        Note:
            SQLAlchemy detecta automáticamente los cambios si el objeto
            está attached a la sesión.
        """
        self._session.commit()
        self._session.refresh(tarea)
        return tarea

    def eliminar(self, tarea_id: int, usuario_id: int) -> bool:
        """
        Elimina una tarea (soft delete).

        Args:
            tarea_id: ID de la tarea
            usuario_id: ID del usuario (para verificar propiedad)

        Returns:
            True si se eliminó, False si no existe o no pertenece al usuario
        """
        tarea = self.obtener_por_id(tarea_id, usuario_id)
        if not tarea:
            return False

        tarea.eliminada = True
        self._session.commit()
        return True

    def restaurar(self, tarea_id: int, usuario_id: int) -> bool:
        """
        Restaura una tarea eliminada.

        Args:
            tarea_id: ID de la tarea
            usuario_id: ID del usuario (para verificar propiedad)

        Returns:
            True si se restauró, False si no existe o no pertenece al usuario
        """
        # Buscar incluyendo eliminadas
        tarea = self._session.query(TareaModel).filter(
            and_(
                TareaModel.id == tarea_id,
                TareaModel.usuario_id == usuario_id,
                TareaModel.eliminada == True  # Solo restaurar si está eliminada
            )
        ).first()

        if not tarea:
            return False

        tarea.eliminada = False
        self._session.commit()
        return True

    def listar_papelera(
        self,
        usuario_id: int,
        limite: int = 10,
        offset: int = 0
    ) -> list[TareaModel]:
        """
        Lista tareas eliminadas (papelera).

        Args:
            usuario_id: ID del usuario propietario
            limite: Número máximo de resultados
            offset: Offset para paginación

        Returns:
            Lista de tareas eliminadas
        """
        return self._session.query(TareaModel).filter(
            and_(
                TareaModel.usuario_id == usuario_id,
                TareaModel.eliminada == True
            )
        ).order_by(
            TareaModel.actualizado_en.desc()  # Más recientemente eliminadas
        ).limit(limite).offset(offset).all()
