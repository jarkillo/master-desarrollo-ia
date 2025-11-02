# api/repositorio_usuarios.py
"""
Repositorio en memoria para almacenar usuarios.

En producción esto debería usar una base de datos (PostgreSQL, MongoDB, etc.),
pero para propósitos educativos usamos un diccionario en memoria.
"""
from datetime import UTC, datetime

from api.modelos import User


class RepositorioUsuarios:
    """Repositorio en memoria para usuarios."""

    def __init__(self):
        # Almacena usuarios: {email: User}
        self._usuarios: dict[str, User] = {}
        self._id_counter = 1

    def crear_usuario(self, email: str, nombre: str, hashed_password: str) -> User:
        """
        Crea un nuevo usuario.

        Args:
            email: Email del usuario (único)
            nombre: Nombre del usuario
            hashed_password: Password hasheado con bcrypt

        Returns:
            User: Usuario creado

        Raises:
            ValueError: Si el email ya está registrado
        """
        if email in self._usuarios:
            raise ValueError(f"Email {email} ya está registrado")

        user_id = f"user_{self._id_counter}"
        self._id_counter += 1

        usuario = User(
            id=user_id,
            email=email,
            nombre=nombre,
            hashed_password=hashed_password,
            created_at=datetime.now(tz=UTC),
        )

        self._usuarios[email] = usuario
        return usuario

    def obtener_por_email(self, email: str) -> User | None:
        """
        Obtiene un usuario por email.

        Args:
            email: Email del usuario

        Returns:
            User si existe, None si no
        """
        return self._usuarios.get(email)

    def obtener_por_id(self, user_id: str) -> User | None:
        """
        Obtiene un usuario por ID.

        Args:
            user_id: ID del usuario

        Returns:
            User si existe, None si no
        """
        for user in self._usuarios.values():
            if user.id == user_id:
                return user
        return None

    def existe_email(self, email: str) -> bool:
        """
        Verifica si un email ya está registrado.

        Args:
            email: Email a verificar

        Returns:
            bool: True si existe, False si no
        """
        return email in self._usuarios

    def listar_todos(self) -> list[User]:
        """
        Lista todos los usuarios (útil para debugging/admin).

        Returns:
            list[User]: Lista de todos los usuarios
        """
        return list(self._usuarios.values())

    def limpiar(self):
        """Limpia todos los usuarios (útil para tests)."""
        self._usuarios.clear()
        self._id_counter = 1
