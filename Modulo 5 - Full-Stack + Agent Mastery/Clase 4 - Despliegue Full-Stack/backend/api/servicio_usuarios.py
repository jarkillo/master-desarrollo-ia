# api/servicio_usuarios.py
"""
Servicio de usuarios con lógica de negocio de autenticación.

Maneja:
- Registro de nuevos usuarios con hashing de passwords
- Login con verificación de credenciales
- Creación de tokens JWT
"""
from typing import Optional
import bcrypt
from api.repositorio_usuarios import RepositorioUsuarios
from api.modelos import User, RegisterRequest, LoginRequest, AuthResponse, UserResponse
from api.seguridad_jwt import crear_token


class ServicioUsuarios:
    """Servicio de lógica de negocio para usuarios."""

    def __init__(self, repositorio: RepositorioUsuarios):
        self._repo = repositorio

    def registrar(self, request: RegisterRequest) -> AuthResponse:
        """
        Registra un nuevo usuario.

        Args:
            request: Datos del nuevo usuario

        Returns:
            AuthResponse: Token JWT y datos del usuario

        Raises:
            ValueError: Si el email ya está registrado
        """
        # Validar que el email no exista
        if self._repo.existe_email(request.email):
            raise ValueError(f"El email {request.email} ya está registrado")

        # Hash de password con bcrypt
        hashed = bcrypt.hashpw(request.password.encode("utf-8"), bcrypt.gensalt())

        # Crear usuario en el repositorio
        usuario = self._repo.crear_usuario(
            email=request.email, nombre=request.nombre, hashed_password=hashed.decode("utf-8")
        )

        # Generar token JWT
        token = crear_token({"sub": usuario.id, "email": usuario.email, "nombre": usuario.nombre})

        return AuthResponse(
            access_token=token,
            token_type="bearer",
            user=UserResponse(
                id=usuario.id, email=usuario.email, nombre=usuario.nombre, created_at=usuario.created_at
            ),
        )

    def login(self, request: LoginRequest) -> AuthResponse:
        """
        Autentica un usuario existente.

        Args:
            request: Credenciales de login

        Returns:
            AuthResponse: Token JWT y datos del usuario

        Raises:
            ValueError: Si las credenciales son inválidas
        """
        # Buscar usuario por email
        usuario = self._repo.obtener_por_email(request.email)
        if not usuario:
            raise ValueError("Credenciales inválidas")

        # Verificar password
        if not bcrypt.checkpw(request.password.encode("utf-8"), usuario.hashed_password.encode("utf-8")):
            raise ValueError("Credenciales inválidas")

        # Generar token JWT
        token = crear_token({"sub": usuario.id, "email": usuario.email, "nombre": usuario.nombre})

        return AuthResponse(
            access_token=token,
            token_type="bearer",
            user=UserResponse(
                id=usuario.id, email=usuario.email, nombre=usuario.nombre, created_at=usuario.created_at
            ),
        )

    def obtener_usuario_actual(self, user_id: str) -> Optional[UserResponse]:
        """
        Obtiene los datos del usuario autenticado.

        Args:
            user_id: ID del usuario (extraído del token JWT)

        Returns:
            UserResponse si el usuario existe, None si no
        """
        usuario = self._repo.obtener_por_id(user_id)
        if not usuario:
            return None

        return UserResponse(
            id=usuario.id, email=usuario.email, nombre=usuario.nombre, created_at=usuario.created_at
        )
