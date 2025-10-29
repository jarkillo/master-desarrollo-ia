# api/api.py
"""
API REST con FastAPI optimizada para producción en cloud.

Mejoras respecto a Clase 4:
- CORS configurado para frontend
- Health checks completos (app + database)
- Configuración dinámica (Settings)
- Logging apropiado
- Manejo de errores mejorado
- OpenAPI docs condicionales (solo en dev)

Deploy targets:
- Railway: https://railway.app
- Render: https://render.com
- Cualquier platform-as-a-service que soporte Python
"""
import logging
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.config import settings
from api.database import crear_tablas, check_database_health
from api.servicio_tareas import Tarea, TareaCreate, TareaUpdate
from api.dependencias import ServicioTareasDepende

# Configurar logging
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler (FastAPI moderno).

    STARTUP (antes del yield):
    - Crea tablas de BD (solo dev, prod usa Alembic)
    - Log del entorno actual
    - Verifica conexión a BD

    SHUTDOWN (después del yield):
    - Cleanup si es necesario
    """
    # STARTUP
    logger.info(f"🚀 Iniciando aplicación en modo: {settings.environment}")
    logger.info(f"📊 Database URL: {settings.database_url.split('@')[-1] if '@' in settings.database_url else settings.database_url}")

    # Solo en dev: crear tablas automáticamente
    # En producción, esto se hace con Alembic migrations
    if settings.is_development:
        logger.info("🛠️  Modo desarrollo: creando tablas con create_all()")
        crear_tablas()
    else:
        logger.info("🏭 Modo producción: asegúrate de ejecutar 'alembic upgrade head'")

    # Verificar conexión a BD
    db_health = check_database_health()
    if db_health["status"] == "ok":
        logger.info("✅ Base de datos conectada correctamente")
    else:
        logger.error(f"❌ Error de base de datos: {db_health.get('error')}")

    yield  # La aplicación corre aquí

    # SHUTDOWN
    logger.info("🛑 Cerrando aplicación...")


# Crear app con configuración dinámica
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    lifespan=lifespan,
    # En producción, puedes deshabilitar docs para seguridad
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
)

# CORS Middleware
# Permite que frontends en otros dominios consuman esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # ["https://tu-frontend.com"]
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Accept, Content-Type, Authorization, etc.
)


# ============================================================================
# HEALTH CHECKS
# ============================================================================

@app.get("/", tags=["Health"])
def root():
    """
    Endpoint raíz para verificar que la API está activa.

    Railway y Render usan este endpoint para health checks.
    """
    return {
        "status": "ok",
        "message": "API de Tareas - Cloud Ready",
        "environment": settings.environment,
        "version": settings.api_version
    }


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check completo: API + Base de datos.

    Retorna:
    - 200 OK: Todo funciona
    - 503 Service Unavailable: BD desconectada

    Usado por:
    - Load balancers (Railway, Render)
    - Monitoring tools (UptimeRobot, Pingdom)
    - CI/CD pipelines
    """
    db_health = check_database_health()

    if db_health["status"] == "error":
        logger.error(f"Health check failed: {db_health.get('error')}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "api": "ok",
                "database": "disconnected",
                "reason": "internal error"
            }
        )

    return {
        "status": "healthy",
        "api": "ok",
        "database": db_health,
        "environment": settings.environment
    }


# ============================================================================
# CRUD ENDPOINTS
# ============================================================================

@app.post(
    "/tareas",
    response_model=Tarea,
    status_code=status.HTTP_201_CREATED,
    tags=["Tareas"]
)
def crear_tarea(
    tarea_data: TareaCreate,
    servicio: ServicioTareasDepende
) -> Tarea:
    """
    Crea una nueva tarea.

    Args:
        tarea_data: Datos de la tarea a crear
        servicio: Servicio de tareas (inyectado)

    Returns:
        Tarea creada con su ID asignado

    Raises:
        HTTPException 400: Si la validación falla (Pydantic)
    """
    logger.info(f"Creando tarea: {tarea_data.nombre}")
    return servicio.crear(nombre=tarea_data.nombre)


@app.get(
    "/tareas",
    response_model=List[Tarea],
    tags=["Tareas"]
)
def listar_tareas(servicio: ServicioTareasDepende) -> List[Tarea]:
    """
    Lista todas las tareas.

    Args:
        servicio: Servicio de tareas (inyectado)

    Returns:
        Lista de todas las tareas (puede estar vacía)
    """
    logger.debug("Listando todas las tareas")
    return servicio.listar()


@app.get(
    "/tareas/{id}",
    response_model=Tarea,
    tags=["Tareas"]
)
def obtener_tarea(id: int, servicio: ServicioTareasDepende) -> Tarea:
    """
    Obtiene una tarea por ID.

    Args:
        id: ID de la tarea
        servicio: Servicio de tareas (inyectado)

    Returns:
        Tarea encontrada

    Raises:
        HTTPException 404: Si la tarea no existe
    """
    logger.debug(f"Obteniendo tarea con id: {id}")
    tarea = servicio.obtener(id)
    if not tarea:
        logger.warning(f"Tarea {id} no encontrada")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con id {id} no encontrada"
        )
    return tarea


@app.put(
    "/tareas/{id}",
    response_model=Tarea,
    tags=["Tareas"]
)
def actualizar_tarea(
    id: int,
    tarea_data: TareaUpdate,
    servicio: ServicioTareasDepende
) -> Tarea:
    """
    Actualiza una tarea existente.

    Args:
        id: ID de la tarea a actualizar
        tarea_data: Datos a actualizar (campos opcionales)
        servicio: Servicio de tareas (inyectado)

    Returns:
        Tarea actualizada

    Raises:
        HTTPException 404: Si la tarea no existe
    """
    logger.info(f"Actualizando tarea {id}")
    tarea = servicio.actualizar(id, tarea_data)
    if not tarea:
        logger.warning(f"Tarea {id} no encontrada para actualizar")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con id {id} no encontrada"
        )
    return tarea


@app.delete(
    "/tareas/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tareas"]
)
def eliminar_tarea(id: int, servicio: ServicioTareasDepende):
    """
    Elimina una tarea.

    Args:
        id: ID de la tarea a eliminar
        servicio: Servicio de tareas (inyectado)

    Returns:
        No content (204)

    Raises:
        HTTPException 404: Si la tarea no existe
    """
    logger.info(f"Eliminando tarea {id}")
    eliminada = servicio.eliminar(id)
    if not eliminada:
        logger.warning(f"Tarea {id} no encontrada para eliminar")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con id {id} no encontrada"
        )
