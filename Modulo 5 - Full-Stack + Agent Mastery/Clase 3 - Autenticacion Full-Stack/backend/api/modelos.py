# api/modelos.py
"""
Modelos Pydantic para autenticación y usuarios.

Define las estructuras de datos para:
- Usuarios (User)
- Requests de registro (RegisterRequest)
- Requests de login (LoginRequest)
- Responses de autenticación (AuthResponse, UserResponse)
"""
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Request para registrar un nuevo usuario."""

    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(
        ..., min_length=8, max_length=100, description="Contraseña (mínimo 8 caracteres)"
    )
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del usuario")

    model_config = {"json_schema_extra": {"examples": [{"email": "user@example.com", "password": "password123", "nombre": "Juan Pérez"}]}}


class LoginRequest(BaseModel):
    """Request para login de usuario existente."""

    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., min_length=1, description="Contraseña")

    model_config = {"json_schema_extra": {"examples": [{"email": "user@example.com", "password": "password123"}]}}


class UserResponse(BaseModel):
    """Representación de un usuario (sin password)."""

    id: str = Field(..., description="ID único del usuario")
    email: str = Field(..., description="Email del usuario")
    nombre: str = Field(..., description="Nombre del usuario")
    created_at: datetime = Field(..., description="Fecha de creación")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "user_123",
                    "email": "user@example.com",
                    "nombre": "Juan Pérez",
                    "created_at": "2025-10-23T10:00:00Z",
                }
            ]
        }
    }


class AuthResponse(BaseModel):
    """Response de autenticación exitosa con token JWT."""

    access_token: str = Field(..., description="Token JWT para autenticación")
    token_type: str = Field(default="bearer", description="Tipo de token (siempre 'bearer')")
    user: UserResponse = Field(..., description="Información del usuario autenticado")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer",
                    "user": {
                        "id": "user_123",
                        "email": "user@example.com",
                        "nombre": "Juan Pérez",
                        "created_at": "2025-10-23T10:00:00Z",
                    },
                }
            ]
        }
    }


class User(BaseModel):
    """Modelo completo de usuario (incluyendo password hasheado) - SOLO uso interno."""

    id: str
    email: str
    nombre: str
    hashed_password: str
    created_at: datetime
