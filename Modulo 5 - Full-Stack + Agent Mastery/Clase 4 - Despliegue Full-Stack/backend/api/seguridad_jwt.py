# api/seguridad_jwt.py
"""
Módulo de seguridad JWT para autenticación en FastAPI.

Este módulo proporciona funciones para:
- Crear tokens JWT con claims personalizados
- Verificar tokens JWT en endpoints protegidos
- Configuración de secreto y expiración desde variables de entorno
"""
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import os

from fastapi import Header, HTTPException
from jose import jwt, JWTError


def _config() -> tuple[str, int]:
    """
    Lee configuración JWT desde variables de entorno.

    Returns:
        tuple: (secret_key, minutos_expiracion)
    """
    secret = os.getenv("JWT_SECRET", "dev-secret-change-in-production")
    minutos = int(os.getenv("JWT_MINUTOS", "60"))
    return secret, minutos


def crear_token(claims: Dict[str, Any], minutos: Optional[int] = None) -> str:
    """
    Crea un token JWT con los claims proporcionados.

    Args:
        claims: Diccionario con datos a incluir en el token (ej: {"sub": "user123", "email": "user@example.com"})
        minutos: Minutos hasta expiración (usa JWT_MINUTOS si es None)

    Returns:
        str: Token JWT firmado

    Example:
        >>> token = crear_token({"sub": "user123", "email": "user@example.com"})
        >>> print(token)
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
    """
    secret, default_min = _config()
    exp_min = default_min if minutos is None else minutos
    to_encode = claims.copy()
    to_encode["exp"] = datetime.now(tz=timezone.utc) + timedelta(minutes=exp_min)
    return jwt.encode(to_encode, secret, algorithm="HS256")


def verificar_jwt(
    authorization: Optional[str] = Header(None, alias="Authorization")
) -> Dict[str, Any]:
    """
    Verifica un token JWT desde el header Authorization.

    Args:
        authorization: Header HTTP "Authorization: Bearer <token>"

    Returns:
        Dict: Payload decodificado del token

    Raises:
        HTTPException(401): Si el token es inválido, expirado o ausente

    Example:
        >>> @app.get("/protected")
        >>> async def protected_route(payload: dict = Depends(verificar_jwt)):
        >>>     return {"user": payload["sub"]}
    """
    # 401 si no hay cabecera o formato incorrecto
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Token ausente o formato inválido")

    token = authorization.split(" ", 1)[1].strip()
    secret, _ = _config()
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload  # lo puedes inyectar en el endpoint si lo necesitas
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
