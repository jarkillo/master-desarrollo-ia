# api/seguridad_jwt.py
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import os

from fastapi import Header, HTTPException
from jose import jwt, JWTError


def _config():
    # Leer SIEMPRE del entorno para que los tests puedan setearlo al vuelo
    secret = os.getenv("JWT_SECRET", "dev-secret")
    minutos = int(os.getenv("JWT_MINUTOS", "30"))
    return secret, minutos


def crear_token(claims: Dict[str, Any], minutos: Optional[int] = None) -> str:
    secret, default_min = _config()
    exp_min = default_min if minutos is None else minutos
    to_encode = claims.copy()
    to_encode["exp"] = datetime.now(tz=timezone.utc) + timedelta(minutes=exp_min)
    return jwt.encode(to_encode, secret, algorithm="HS256")


def verificar_jwt(
    authorization: Optional[str] = Header(None, alias="Authorization")
) -> Dict[str, Any]:
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
