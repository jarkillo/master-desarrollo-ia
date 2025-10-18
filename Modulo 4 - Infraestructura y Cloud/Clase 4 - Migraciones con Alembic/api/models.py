# api/models.py
"""
Modelos ORM usando SQLAlchemy 2.0

SQLAlchemy 2.0 introduce cambios importantes:
- Declarative base moderna con mapped_column()
- Type hints nativos (Mapped[int], Mapped[str])
- Mejor integración con mypy y type checkers
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Clase base para todos los modelos ORM.

    En SQLAlchemy 2.0, heredamos de DeclarativeBase
    en lugar de usar declarative_base()
    """
    pass


class TareaModel(Base):
    """
    Modelo ORM para la tabla 'tareas'.

    Representa una tarea en la base de datos.
    Usamos Mapped[] para type hints nativos (SQLAlchemy 2.0).
    """
    __tablename__ = "tareas"

    # Primary key con auto-incremento
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Nombre de la tarea (máximo 100 caracteres, no puede ser NULL)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)

    # Estado de completitud (por defecto False)
    completada: Mapped[bool] = mapped_column(default=False)

    # Prioridad (1=baja, 2=media, 3=alta)
    prioridad: Mapped[int] = mapped_column(default=2)

    # Timestamps automáticos
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # Se asigna en el servidor
        nullable=False
    )

    actualizado_en: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),  # Se actualiza automáticamente
        nullable=True
    )

    def __repr__(self) -> str:
        """Representación legible del modelo para debugging"""
        return (
            f"<TareaModel(id={self.id}, nombre='{self.nombre}', "
            f"completada={self.completada}, prioridad={self.prioridad})>"
        )
