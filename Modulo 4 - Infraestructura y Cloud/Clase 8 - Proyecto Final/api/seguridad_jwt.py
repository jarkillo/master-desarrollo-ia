"""
Módulo de seguridad con JWT (JSON Web Tokens).

Basado en el contenido del Módulo 3 - Clase 4.
Gestiona autenticación con JWT y hashing de contraseñas.
"""

from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from api.config import settings
from api.database import get_db
from api.models import UsuarioModel
from api.schemas import TokenData

# ============================================================================
# PASSWORD HASHING
# ============================================================================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashea una contraseña usando bcrypt.

    Args:
        password: Contraseña en texto plano

    Returns:
        Hash de la contraseña
    """
    return pwd_context.hash(password)


def verificar_password(password_plano: str, password_hash: str) -> bool:
    """
    Verifica que una contraseña coincide con su hash.

    Args:
        password_plano: Contraseña en texto plano
        password_hash: Hash almacenado en BD

    Returns:
        True si coincide, False en caso contrario
    """
    return pwd_context.verify(password_plano, password_hash)


# ============================================================================
# JWT TOKEN CREATION
# ============================================================================

def crear_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Crea un JWT token.

    Args:
        data: Datos a incluir en el token (payload)
        expires_delta: Tiempo de expiración opcional

    Returns:
        Token JWT codificado
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expiration_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def crear_access_token(email: str, user_id: int) -> str:
    """
    Crea un access token para un usuario.

    Args:
        email: Email del usuario
        user_id: ID del usuario

    Returns:
        Access token JWT
    """
    return crear_token(
        data={"sub": email, "user_id": user_id},
        expires_delta=timedelta(minutes=settings.jwt_expiration_minutes)
    )


# ============================================================================
# JWT TOKEN VALIDATION
# ============================================================================

security = HTTPBearer()


def decodificar_token(token: str) -> TokenData:
    """
    Decodifica y valida un JWT token.

    Args:
        token: Token JWT

    Returns:
        TokenData con los datos del token

    Raises:
        HTTPException: Si el token es inválido o expiró
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")

        if email is None or user_id is None:
            raise credentials_exception

        return TokenData(email=email, user_id=user_id)

    except JWTError:
        raise credentials_exception


# ============================================================================
# DEPENDENCIES PARA PROTEGER ENDPOINTS
# ============================================================================

def obtener_usuario_actual(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> UsuarioModel:
    """
    Dependency que obtiene el usuario actual desde el token JWT.

    Uso en endpoints protegidos:
        @app.get("/protected")
        def protected_route(usuario: UsuarioModel = Depends(obtener_usuario_actual)):
            return {"msg": f"Hola {usuario.nombre}"}

    Args:
        credentials: Credenciales HTTP Bearer
        db: Sesión de base de datos

    Returns:
        Usuario autenticado

    Raises:
        HTTPException 401: Si el token es inválido o el usuario no existe
        HTTPException 403: Si el usuario está inactivo
    """
    token = credentials.credentials
    token_data = decodificar_token(token)

    # Buscar usuario en BD
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.email == token_data.email
    ).first()

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar que el usuario esté activo
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )

    return usuario


def autenticar_usuario(email: str, password: str, db: Session) -> UsuarioModel | None:
    """
    Autentica un usuario verificando email y contraseña.

    Args:
        email: Email del usuario
        password: Contraseña en texto plano
        db: Sesión de base de datos

    Returns:
        Usuario si las credenciales son correctas, None en caso contrario
    """
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.email == email
    ).first()

    if not usuario:
        return None

    if not verificar_password(password, usuario.password_hash):
        return None

    return usuario
