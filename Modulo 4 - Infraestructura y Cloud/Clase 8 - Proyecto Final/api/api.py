"""
API principal con FastAPI - Proyecto Final Módulo 4.

Implementa todos los endpoints REST para la gestión de tareas:
- Autenticación (registro, login)
- CRUD de tareas
- Filtros, búsqueda y paginación
- Soft delete y papelera
- Health check
"""

from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.config import settings
from api.database import crear_tablas, get_db, verificar_conexion
from api.dependencias import get_servicio_tareas, get_servicio_usuarios
from api.models import UsuarioModel
from api.schemas import (
    ErrorResponse,
    HealthResponse,
    PaginationParams,
    TareaCreate,
    TareaListResponse,
    TareaResponse,
    TareaUpdate,
    Token,
    UsuarioCreate,
    UsuarioLogin,
    UsuarioResponse,
)
from api.seguridad_jwt import autenticar_usuario, crear_access_token, obtener_usuario_actual
from api.servicio_tareas import ServicioTareas
from api.servicio_usuarios import ServicioUsuarios

# ============================================================================
# LIFESPAN EVENTS
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicación.

    Startup:
        - Crea las tablas de BD (en dev/tests)
        - Verifica conexión a BD

    Shutdown:
        - Limpieza de recursos si es necesario
    """
    # STARTUP
    print("Iniciando aplicación...")
    print(f"Entorno: {settings.environment}")
    print(f"Base de datos: {settings.database_url[:50]}...")

    # Crear tablas (solo en desarrollo)
    if settings.is_development:
        print("Creando tablas (modo desarrollo)...")
        crear_tablas()

    # Verificar conexión
    if verificar_conexion():
        print("OK - Conexión a BD exitosa")
    else:
        print("ERROR - Fallo al conectar a BD")

    yield

    # SHUTDOWN
    print("Cerrando aplicación...")


# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="API de gestión de tareas con autenticación JWT y PostgreSQL",
    lifespan=lifespan
)


# ============================================================================
# EXCEPTION HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Handler personalizado para HTTPException."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            detail=exc.detail,
            code=str(exc.status_code)
        ).model_dump()
    )


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health check"
)
def health_check(db: Session = Depends(get_db)):
    """
    Verifica el estado de la aplicación y la conexión a BD.

    Returns:
        Estado de la aplicación
    """
    db_status = "connected" if verificar_conexion() else "disconnected"

    return HealthResponse(
        status="ok",
        environment=settings.environment,
        database=db_status,
        timestamp=datetime.utcnow()
    )


# ============================================================================
# AUTENTICACIÓN
# ============================================================================

@app.post(
    "/auth/register",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Auth"],
    summary="Registrar nuevo usuario"
)
def registrar_usuario(
    datos: UsuarioCreate,
    servicio: ServicioUsuarios = Depends(get_servicio_usuarios)
):
    """
    Registra un nuevo usuario en el sistema.

    - **email**: Email único del usuario
    - **nombre**: Nombre completo
    - **password**: Contraseña (mínimo 8 caracteres)

    Returns:
        Usuario creado (sin contraseña)

    Raises:
        400: Si el email ya está registrado
    """
    return servicio.registrar(datos)


@app.post(
    "/auth/login",
    response_model=Token,
    tags=["Auth"],
    summary="Login de usuario"
)
def login(
    credenciales: UsuarioLogin,
    db: Session = Depends(get_db)
):
    """
    Autentica un usuario y devuelve un JWT token.

    - **email**: Email del usuario
    - **password**: Contraseña

    Returns:
        Access token JWT

    Raises:
        401: Si las credenciales son incorrectas
    """
    usuario = autenticar_usuario(credenciales.email, credenciales.password, db)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = crear_access_token(
        email=usuario.email,
        user_id=usuario.id
    )

    return Token(access_token=access_token)


@app.get(
    "/auth/me",
    response_model=UsuarioResponse,
    tags=["Auth"],
    summary="Obtener usuario actual"
)
def obtener_usuario_logueado(
    usuario: UsuarioModel = Depends(obtener_usuario_actual)
):
    """
    Obtiene la información del usuario autenticado.

    Requiere autenticación (Bearer token).

    Returns:
        Información del usuario actual
    """
    return UsuarioResponse.model_validate(usuario)


# ============================================================================
# TAREAS - CRUD
# ============================================================================

@app.post(
    "/tareas",
    response_model=TareaResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Tareas"],
    summary="Crear tarea"
)
def crear_tarea(
    datos: TareaCreate,
    usuario: UsuarioModel = Depends(obtener_usuario_actual),
    servicio: ServicioTareas = Depends(get_servicio_tareas)
):
    """
    Crea una nueva tarea para el usuario autenticado.

    - **titulo**: Título de la tarea (obligatorio)
    - **descripcion**: Descripción opcional
    - **prioridad**: 1=Baja, 2=Media, 3=Alta (default: 2)
    - **completada**: Estado inicial (default: false)

    Returns:
        Tarea creada
    """
    return servicio.crear(datos, usuario.id)


@app.get(
    "/tareas",
    response_model=TareaListResponse,
    tags=["Tareas"],
    summary="Listar tareas"
)
def listar_tareas(
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    completada: bool | None = Query(None, description="Filtrar por completada"),
    prioridad: int | None = Query(None, ge=1, le=3, description="Filtrar por prioridad (1-3)"),
    q: str | None = Query(None, max_length=200, description="Buscar en título"),
    usuario: UsuarioModel = Depends(obtener_usuario_actual),
    servicio: ServicioTareas = Depends(get_servicio_tareas)
):
    """
    Lista las tareas del usuario autenticado con filtros y paginación.

    Query parameters opcionales:
    - **page**: Número de página (default: 1)
    - **page_size**: Tamaño de página (default: 10, max: 100)
    - **completada**: Filtrar por estado (true/false)
    - **prioridad**: Filtrar por prioridad (1, 2, 3)
    - **q**: Buscar por texto en el título

    Returns:
        Lista paginada de tareas con metadatos
    """
    pagination = PaginationParams(page=page, page_size=page_size)
    return servicio.listar(
        usuario_id=usuario.id,
        pagination=pagination,
        completada=completada,
        prioridad=prioridad,
        q=q
    )


@app.get(
    "/tareas/{tarea_id}",
    response_model=TareaResponse,
    tags=["Tareas"],
    summary="Obtener tarea por ID"
)
def obtener_tarea(
    tarea_id: int,
    usuario: UsuarioModel = Depends(obtener_usuario_actual),
    servicio: ServicioTareas = Depends(get_servicio_tareas)
):
    """
    Obtiene una tarea específica por su ID.

    Raises:
        404: Si la tarea no existe o no pertenece al usuario
    """
    return servicio.obtener_por_id(tarea_id, usuario.id)


@app.put(
    "/tareas/{tarea_id}",
    response_model=TareaResponse,
    tags=["Tareas"],
    summary="Actualizar tarea"
)
def actualizar_tarea(
    tarea_id: int,
    datos: TareaUpdate,
    usuario: UsuarioModel = Depends(obtener_usuario_actual),
    servicio: ServicioTareas = Depends(get_servicio_tareas)
):
    """
    Actualiza una tarea existente (PATCH semántico).

    Todos los campos son opcionales:
    - **titulo**: Nuevo título
    - **descripcion**: Nueva descripción
    - **completada**: Nuevo estado
    - **prioridad**: Nueva prioridad (1-3)

    Solo se actualizan los campos enviados.

    Raises:
        404: Si la tarea no existe o no pertenece al usuario
    """
    return servicio.actualizar(tarea_id, datos, usuario.id)


@app.delete(
    "/tareas/{tarea_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tareas"],
    summary="Eliminar tarea"
)
def eliminar_tarea(
    tarea_id: int,
    usuario: UsuarioModel = Depends(obtener_usuario_actual),
    servicio: ServicioTareas = Depends(get_servicio_tareas)
):
    """
    Elimina una tarea (soft delete).

    La tarea se marca como eliminada pero no se borra de la BD.
    Puedes recuperarla desde /tareas/papelera.

    Raises:
        404: Si la tarea no existe o no pertenece al usuario
    """
    servicio.eliminar(tarea_id, usuario.id)


# ============================================================================
# TAREAS - PAPELERA
# ============================================================================

@app.get(
    "/tareas/papelera/listar",
    response_model=TareaListResponse,
    tags=["Papelera"],
    summary="Listar tareas eliminadas"
)
def listar_papelera(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    usuario: UsuarioModel = Depends(obtener_usuario_actual),
    servicio: ServicioTareas = Depends(get_servicio_tareas)
):
    """
    Lista las tareas eliminadas del usuario (papelera de reciclaje).

    Returns:
        Lista paginada de tareas eliminadas
    """
    pagination = PaginationParams(page=page, page_size=page_size)
    return servicio.listar_papelera(usuario.id, pagination)


@app.post(
    "/tareas/{tarea_id}/restaurar",
    response_model=TareaResponse,
    tags=["Papelera"],
    summary="Restaurar tarea eliminada"
)
def restaurar_tarea(
    tarea_id: int,
    usuario: UsuarioModel = Depends(obtener_usuario_actual),
    servicio: ServicioTareas = Depends(get_servicio_tareas)
):
    """
    Restaura una tarea eliminada desde la papelera.

    Raises:
        404: Si la tarea no existe en la papelera
    """
    return servicio.restaurar(tarea_id, usuario.id)


# ============================================================================
# ROOT
# ============================================================================

@app.get(
    "/",
    tags=["Root"],
    summary="Información de la API"
)
def root():
    """Endpoint raíz con información de la API."""
    return {
        "nombre": settings.app_name,
        "version": "1.0.0",
        "entorno": settings.environment,
        "documentacion": "/docs",
        "health": "/health"
    }
