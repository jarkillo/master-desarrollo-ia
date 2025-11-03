"""
Servicio de usuarios (Service Layer).

Orquesta la lógica de negocio para la gestión de usuarios.
No depende directamente de SQLAlchemy (usa el repositorio).
"""


from fastapi import HTTPException, status

from api.repositorio_base import RepositorioUsuarios
from api.schemas import UsuarioCreate, UsuarioResponse
from api.seguridad_jwt import hash_password


class ServicioUsuarios:
    """
    Servicio para gestión de usuarios.

    Implementa la lógica de negocio:
    - Registro de usuarios
    - Autenticación
    - Validaciones de negocio
    """

    def __init__(self, repositorio: RepositorioUsuarios):
        """
        Inicializa el servicio con un repositorio.

        Args:
            repositorio: Repositorio de usuarios (implementa RepositorioUsuarios)
        """
        self._repo = repositorio

    def registrar(self, datos: UsuarioCreate) -> UsuarioResponse:
        """
        Registra un nuevo usuario.

        Args:
            datos: Datos del usuario a registrar

        Returns:
            Usuario creado

        Raises:
            HTTPException 400: Si el email ya existe
        """
        # Verificar que el email no exista
        usuario_existente = self._repo.obtener_por_email(datos.email)
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El email {datos.email} ya está registrado"
            )

        # Hashear contraseña
        password_hash = hash_password(datos.password)

        # Crear usuario
        usuario = self._repo.crear(
            email=datos.email,
            nombre=datos.nombre,
            password_hash=password_hash
        )

        return UsuarioResponse.model_validate(usuario)

    def obtener_por_id(self, user_id: int) -> UsuarioResponse | None:
        """
        Obtiene un usuario por su ID.

        Args:
            user_id: ID del usuario

        Returns:
            Usuario si existe, None en caso contrario
        """
        usuario = self._repo.obtener_por_id(user_id)
        if not usuario:
            return None

        return UsuarioResponse.model_validate(usuario)

    def desactivar(self, user_id: int) -> bool:
        """
        Desactiva un usuario (soft delete).

        Args:
            user_id: ID del usuario a desactivar

        Returns:
            True si se desactivó, False si no existe

        Raises:
            HTTPException 404: Si el usuario no existe
        """
        resultado = self._repo.desactivar(user_id)
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario {user_id} no encontrado"
            )
        return True
