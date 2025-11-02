"""
API REST con FastAPI para gestión de tareas.
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from api.repositorio_memoria import RepositorioMemoria
from api.servicio_tareas import ErrorValidacion, ServicioTareas

# === Modelos de Request/Response ===

class CrearTareaRequest(BaseModel):
    """Request para crear una nueva tarea."""
    nombre: str = Field(..., min_length=1, max_length=200,
                        description="Nombre de la tarea")


class ActualizarTareaRequest(BaseModel):
    """Request para actualizar una tarea (campos opcionales)."""
    nombre: str | None = Field(None, min_length=1, max_length=200)
    completada: bool | None = None


class TareaResponse(BaseModel):
    """Response con los datos de una tarea."""
    id: int
    nombre: str
    completada: bool


class EstadisticasResponse(BaseModel):
    """Response con estadísticas de tareas."""
    total: int
    completadas: int
    pendientes: int


class ErrorResponse(BaseModel):
    """Response para errores."""
    detail: str


# === Aplicación FastAPI ===

app = FastAPI(
    title="API de Tareas - Módulo 5 Clase 2",
    description="API REST completa con CRUD para gestión de tareas",
    version="2.0.0"
)

# CORS para desarrollo (React en localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencias (Singleton pattern simple)
repositorio = RepositorioMemoria()
servicio = ServicioTareas(repositorio)


# === Endpoints ===

@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": "2.0.0"}


@app.post(
    "/tareas",
    response_model=TareaResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Tareas"],
    responses={
        201: {"description": "Tarea creada exitosamente"},
        400: {"model": ErrorResponse, "description": "Validación fallida"}
    }
)
def crear_tarea(request: CrearTareaRequest):
    """
    Crea una nueva tarea.

    - **nombre**: Nombre de la tarea (1-200 caracteres)
    """
    try:
        tarea = servicio.crear_tarea(request.nombre)
        return TareaResponse(**tarea.model_dump())
    except ErrorValidacion as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.get(
    "/tareas",
    response_model=list[TareaResponse],
    tags=["Tareas"],
    responses={
        200: {"description": "Lista de tareas obtenida exitosamente"}
    }
)
def listar_tareas():
    """
    Retorna todas las tareas ordenadas por ID.
    """
    tareas = servicio.listar_tareas()
    return [TareaResponse(**t.model_dump()) for t in tareas]


@app.get(
    "/tareas/stats",
    response_model=EstadisticasResponse,
    tags=["Tareas"],
    responses={
        200: {"description": "Estadísticas obtenidas exitosamente"}
    }
)
def obtener_estadisticas():
    """
    Retorna estadísticas agregadas del recurso tareas.

    Este es un sub-recurso de /tareas que proporciona una vista agregada.
    """
    stats = servicio.contar_tareas()
    return EstadisticasResponse(**stats)


@app.get(
    "/tareas/{tarea_id}",
    response_model=TareaResponse,
    tags=["Tareas"],
    responses={
        200: {"description": "Tarea obtenida exitosamente"},
        404: {"model": ErrorResponse, "description": "Tarea no encontrada"}
    }
)
def obtener_tarea(tarea_id: int):
    """
    Obtiene una tarea específica por ID.

    - **tarea_id**: ID de la tarea
    """
    tarea = servicio.obtener_tarea(tarea_id)
    if not tarea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {tarea_id} no encontrada"
        )
    return TareaResponse(**tarea.model_dump())


@app.patch(
    "/tareas/{tarea_id}",
    response_model=TareaResponse,
    tags=["Tareas"],
    responses={
        200: {"description": "Tarea actualizada exitosamente"},
        400: {"model": ErrorResponse, "description": "Validación fallida"},
        404: {"model": ErrorResponse, "description": "Tarea no encontrada"}
    }
)
def actualizar_tarea(tarea_id: int, request: ActualizarTareaRequest):
    """
    Actualiza una tarea existente (parcial).

    - **tarea_id**: ID de la tarea
    - **nombre**: Nuevo nombre (opcional)
    - **completada**: Nuevo estado (opcional)
    """
    # Validar que al menos un campo esté presente
    if request.nombre is None and request.completada is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe proporcionar al menos un campo para actualizar (nombre o completada)"
        )

    try:
        tarea = servicio.actualizar_tarea(
            tarea_id,
            nombre=request.nombre,
            completada=request.completada
        )

        if not tarea:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tarea con ID {tarea_id} no encontrada"
            )

        return TareaResponse(**tarea.model_dump())

    except ErrorValidacion as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.delete(
    "/tareas/{tarea_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tareas"],
    responses={
        204: {"description": "Tarea eliminada exitosamente"},
        404: {"model": ErrorResponse, "description": "Tarea no encontrada"}
    }
)
def eliminar_tarea(tarea_id: int):
    """
    Elimina una tarea por ID.

    - **tarea_id**: ID de la tarea a eliminar
    """
    eliminada = servicio.eliminar_tarea(tarea_id)
    if not eliminada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {tarea_id} no encontrada"
        )
    return None
