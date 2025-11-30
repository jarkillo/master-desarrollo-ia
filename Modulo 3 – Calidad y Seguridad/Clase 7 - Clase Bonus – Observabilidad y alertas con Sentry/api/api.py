# api/api.py
"""API FastAPI para gestión de tareas con observabilidad vía Sentry.

Esta API implementa:
- Autenticación JWT para endpoints protegidos
- Dependency Injection para ServicioTareas
- Response models para validación de respuestas
- Observabilidad segura con Sentry (scrubbing de datos sensibles)
- Modelos Pydantic con validación completa
"""
import os
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field
from sentry_sdk import capture_exception, set_context, set_user

from api.dependencias import ServicioDependency
from api.seguridad_jwt import crear_token, verificar_jwt

# Configuración modular
from api.sentry_config import configurar_sentry

# Inicializar Sentry ANTES de crear la app (así captura errores de inicialización)
configurar_sentry()

# Crear app con metadata
app = FastAPI(
    title="API de Tareas con Observabilidad",
    description="API para gestionar tareas con autenticación JWT y monitoring con Sentry",
    version=os.getenv("VERSION", "dev"),
    docs_url="/docs" if os.getenv("MODE") != "production" else None,  # Ocultar docs en prod
)


# ==================== MODELOS PYDANTIC ====================

class LoginRequest(BaseModel):
    """Modelo de request para autenticación."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "usuario": "demo",
                "password": "demo"
            }
        }
    )

    usuario: str = Field(
        min_length=1,
        max_length=50,
        description="Nombre de usuario",
        examples=["demo", "admin"]
    )
    password: str = Field(
        min_length=1,  # En producción, mínimo 8 caracteres
        max_length=100,
        description="Contraseña del usuario"
    )


class LoginResponse(BaseModel):
    """Modelo de response para autenticación exitosa."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
    )

    access_token: str = Field(description="JWT token de acceso")
    token_type: str = Field(default="bearer", description="Tipo de token")


class CrearTareaRequest(BaseModel):
    """Modelo de request para crear una tarea."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "nombre": "Completar documentación del proyecto"
            }
        }
    )

    nombre: str = Field(
        min_length=1,
        max_length=200,
        description="Descripción de la tarea a crear",
        examples=[
            "Completar documentación",
            "Escribir tests unitarios",
            "Revisar pull request"
        ]
    )


class TareaResponse(BaseModel):
    """Modelo de response para una tarea."""

    model_config = ConfigDict(
        from_attributes=True,  # Permite conversión automática desde Pydantic models
        json_schema_extra={
            "example": {
                "id": 1,
                "nombre": "Completar documentación",
                "completada": False
            }
        }
    )

    id: int = Field(description="ID único de la tarea", gt=0)
    nombre: str = Field(description="Descripción de la tarea")
    completada: bool = Field(description="¿Está completada?")


# ==================== ENDPOINTS ====================

@app.post(
    "/login",
    response_model=LoginResponse,
    summary="Autenticación de usuario",
    description="Valida credenciales y retorna un JWT token válido por 30 minutos",
    responses={
        200: {"description": "Login exitoso, retorna JWT token"},
        401: {"description": "Credenciales inválidas"}
    }
)
def login(cuerpo: LoginRequest) -> LoginResponse:
    """Endpoint de autenticación con JWT.

    NOTA: Esta es una implementación demo con credenciales hardcoded.
    En producción, validar contra base de datos con passwords hasheados (bcrypt).

    Args:
        cuerpo: Credenciales de usuario (usuario y password)

    Returns:
        LoginResponse con access_token JWT

    Raises:
        HTTPException: 401 si las credenciales son inválidas
    """
    # Demo: credenciales fijas. En producción, validar contra DB con bcrypt
    if cuerpo.usuario == "demo" and cuerpo.password == "demo":
        token = crear_token({"sub": cuerpo.usuario})

        # Sentry: Capturar login exitoso (opcional, para analytics)
        set_user({"username": cuerpo.usuario})

        return LoginResponse(access_token=token)

    # Sentry: Capturar intento de login fallido (sin exponer password!)
    set_context("login_attempt", {
        "username": cuerpo.usuario,  # OK: username no es sensible
        # ❌ NO incluir password aquí
    })

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas"
    )


@app.post(
    "/tareas",
    status_code=status.HTTP_201_CREATED,
    response_model=TareaResponse,
    summary="Crear una nueva tarea",
    description="Crea una tarea con el nombre proporcionado. Requiere autenticación JWT.",
    responses={
        201: {"description": "Tarea creada exitosamente"},
        401: {"description": "Token JWT inválido o ausente"},
        422: {"description": "Error de validación (nombre vacío, etc.)"}
    }
)
def crear_tarea(
    cuerpo: CrearTareaRequest,
    servicio: ServicioDependency,  # ✅ Inyección de dependencias
    payload: dict[str, Any] = Depends(verificar_jwt)
) -> TareaResponse:
    """Crea una nueva tarea.

    Args:
        cuerpo: Datos de la tarea a crear (nombre)
        servicio: Servicio de tareas (inyectado por FastAPI)
        payload: Claims del JWT (usuario autenticado)

    Returns:
        La tarea creada con ID asignado

    Raises:
        HTTPException: 401 si el token es inválido, 422 si validación falla
    """
    try:
        # Sentry: Agregar contexto de usuario
        set_user({"username": payload.get("sub")})

        # Sentry: Agregar contexto de la operación
        set_context("tarea_creation", {
            "nombre_length": len(cuerpo.nombre),
            "usuario": payload.get("sub"),
        })

        tarea = servicio.crear(cuerpo.nombre)
        return tarea  # FastAPI convierte automáticamente via response_model

    except Exception as e:
        # Sentry: Capturar excepción con contexto
        capture_exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear tarea. El incidente ha sido reportado."
        )


@app.get(
    "/tareas",
    response_model=list[TareaResponse],
    summary="Listar todas las tareas",
    description="Retorna todas las tareas del usuario autenticado",
    responses={
        200: {"description": "Lista de tareas (puede estar vacía)"},
        401: {"description": "Token JWT inválido o ausente"}
    }
)
def listar_tareas(
    servicio: ServicioDependency,  # ✅ Inyección de dependencias
    payload: dict[str, Any] = Depends(verificar_jwt)
) -> list[TareaResponse]:
    """Lista todas las tareas del usuario.

    Args:
        servicio: Servicio de tareas (inyectado por FastAPI)
        payload: Claims del JWT (usuario autenticado)

    Returns:
        Lista de tareas (vacía si no hay ninguna)
    """
    # Sentry: Contexto de usuario
    set_user({"username": payload.get("sub")})

    return servicio.listar()  # FastAPI convierte automáticamente


@app.get(
    "/error",
    summary="Endpoint de prueba para Sentry",
    description="Genera un error intencional para validar integración con Sentry"
)
def generar_error():
    """Endpoint de prueba para validar que Sentry captura errores.

    Este endpoint lanza un ValueError intencional para probar que:
    1. Sentry recibe el error
    2. El contexto (endpoint, timestamp) se captura correctamente
    3. Los filtros de scrubbing funcionan

    Raises:
        ValueError: Error intencional para testing
    """
    # Sentry: Agregar contexto de prueba
    set_context("test_error", {
        "endpoint": "/error",
        "intentional": True,
        "reason": "Validación de integración Sentry"
    })

    raise ValueError("Error intencional para probar Sentry")
