"""
Modelos ORM con SQLAlchemy 2.0.

Este módulo define las entidades de la base de datos usando
la sintaxis moderna de SQLAlchemy 2.0 con type hints nativos.
"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Clase base para todos los modelos ORM."""
    pass


class UsuarioModel(Base):
    """
    Modelo ORM para la tabla 'usuarios'.

    Representa un usuario del sistema con autenticación.

    Atributos:
        id: Identificador único del usuario
        email: Email único del usuario (usado para login)
        nombre: Nombre completo del usuario
        password_hash: Hash bcrypt de la contraseña
        activo: Flag para soft delete
        creado_en: Timestamp de creación (automático)
        actualizado_en: Timestamp de última actualización (automático)
        tareas: Relación con las tareas del usuario
    """

    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    activo: Mapped[bool] = mapped_column(default=True, server_default="1")

    # Timestamps automáticos
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relación: Un usuario tiene muchas tareas
    tareas: Mapped[list["TareaModel"]] = relationship(
        back_populates="usuario",
        cascade="all, delete-orphan"  # Si se elimina el usuario, se eliminan sus tareas
    )

    def __repr__(self) -> str:
        return f"<Usuario(id={self.id}, email='{self.email}', nombre='{self.nombre}')>"


class TareaModel(Base):
    """
    Modelo ORM para la tabla 'tareas'.

    Representa una tarea asignada a un usuario.

    Atributos:
        id: Identificador único de la tarea
        titulo: Título de la tarea (máx 200 caracteres)
        descripcion: Descripción opcional de la tarea
        completada: Estado de completitud
        prioridad: Prioridad (1=Baja, 2=Media, 3=Alta)
        usuario_id: ID del usuario propietario (FK)
        eliminada: Flag para soft delete
        creado_en: Timestamp de creación (automático)
        actualizado_en: Timestamp de última actualización (automático)
        usuario: Relación con el usuario propietario
    """

    __tablename__ = "tareas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    completada: Mapped[bool] = mapped_column(default=False, server_default="0")
    prioridad: Mapped[int] = mapped_column(default=2, server_default="2")  # 1=Baja, 2=Media, 3=Alta
    eliminada: Mapped[bool] = mapped_column(default=False, server_default="0")

    # Foreign Key
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False
    )

    # Timestamps automáticos
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relación inversa: Una tarea pertenece a un usuario
    usuario: Mapped["UsuarioModel"] = relationship(back_populates="tareas")

    # Índices compuestos para optimizar queries frecuentes
    __table_args__ = (
        # Índice para búsquedas por usuario + completada (query frecuente)
        Index("idx_usuario_completada", "usuario_id", "completada"),
        # Índice para búsquedas por usuario + eliminada (excluir eliminadas)
        Index("idx_usuario_eliminada", "usuario_id", "eliminada"),
        # Índice para ordenar por prioridad
        Index("idx_prioridad", "prioridad"),
    )

    def __repr__(self) -> str:
        return (
            f"<Tarea(id={self.id}, titulo='{self.titulo}', "
            f"completada={self.completada}, prioridad={self.prioridad})>"
        )
