# api/repositorio_db.py
"""
Implementación del repositorio usando SQLAlchemy.

Este repositorio implementa el Protocol RepositorioTareas,
pero usando una base de datos real en lugar de memoria o JSON.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from api.models import TareaModel
from api.servicio_tareas import Tarea


class RepositorioDB:
    """
    Repositorio que persiste tareas en base de datos.

    Implementa el patrón Repository con SQLAlchemy.
    La sesión se inyecta desde fuera (Dependency Injection).
    """

    def __init__(self, session: Session):
        """
        Inicializa el repositorio con una sesión de BD.

        Args:
            session: Sesión de SQLAlchemy (proporcionada por get_db())
        """
        self._session = session

    def guardar(self, tarea: Tarea) -> None:
        """
        Guarda una tarea en la base de datos.

        Si la tarea tiene id=0, se crea una nueva (INSERT).
        Si tiene un id existente, se actualiza (UPDATE).

        Args:
            tarea: Tarea del dominio (Pydantic)
        """
        if tarea.id == 0:
            # Nueva tarea - INSERT
            db_tarea = TareaModel(
                nombre=tarea.nombre,
                completada=tarea.completada
            )
            self._session.add(db_tarea)
            self._session.commit()
            self._session.refresh(db_tarea)  # Obtiene el ID generado
            tarea.id = db_tarea.id  # Actualiza el objeto Pydantic
        else:
            # Tarea existente - UPDATE
            db_tarea = self._session.get(TareaModel, tarea.id)
            if db_tarea:
                db_tarea.nombre = tarea.nombre
                db_tarea.completada = tarea.completada
                self._session.commit()

    def listar(self) -> List[Tarea]:
        """
        Lista todas las tareas de la base de datos.

        Returns:
            Lista de tareas del dominio (Pydantic)
        """
        # SELECT * FROM tareas
        db_tareas = self._session.query(TareaModel).all()

        # Convertir modelos ORM a objetos Pydantic (dominio)
        return [
            Tarea(
                id=t.id,
                nombre=t.nombre,
                completada=t.completada
            )
            for t in db_tareas
        ]

    def obtener_por_id(self, id: int) -> Optional[Tarea]:
        """
        Obtiene una tarea por su ID.

        Args:
            id: ID de la tarea

        Returns:
            Tarea si existe, None si no
        """
        # SELECT * FROM tareas WHERE id = ?
        db_tarea = self._session.get(TareaModel, id)

        if db_tarea:
            return Tarea(
                id=db_tarea.id,
                nombre=db_tarea.nombre,
                completada=db_tarea.completada
            )
        return None

    def actualizar(self, tarea: Tarea) -> bool:
        """
        Actualiza una tarea existente.

        Args:
            tarea: Tarea con datos actualizados

        Returns:
            True si la tarea existía y se actualizó, False si no existía
        """
        db_tarea = self._session.get(TareaModel, tarea.id)

        if db_tarea:
            db_tarea.nombre = tarea.nombre
            db_tarea.completada = tarea.completada
            self._session.commit()
            return True
        return False

    def eliminar(self, id: int) -> bool:
        """
        Elimina una tarea por ID.

        Args:
            id: ID de la tarea a eliminar

        Returns:
            True si la tarea existía y se eliminó, False si no existía
        """
        db_tarea = self._session.get(TareaModel, id)

        if db_tarea:
            self._session.delete(db_tarea)
            self._session.commit()
            return True
        return False
