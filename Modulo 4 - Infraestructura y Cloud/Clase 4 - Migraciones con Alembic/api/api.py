# api/api.py
"""
API REST con FastAPI y SQLAlchemy.

Demuestra:
- Lifespan events para inicialización de BD
- Dependency injection con SQLAlchemy
- CRUD completo con validaciones
- Manejo de errores HTTP apropiados
"""
from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, HTTPException, status
from api.database import crear_tablas
from api.servicio_tareas import Tarea, TareaCreate, TareaUpdate
from api.dependencias import ServicioTareasDepende


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler (FastAPI moderno).

    Ejecuta código al iniciar y al cerrar la aplicación.
    Reemplaza @app.on_event("startup") y @app.on_event("shutdown")

    Yield separa el startup (antes) del shutdown (después).
    """
    # STARTUP: Se ejecuta al iniciar la app
    print("🚀 Iniciando aplicación...")
    crear_tablas()
    print("✅ Tablas de BD creadas/verificadas")

    yield  # La aplicación corre aquí

    # SHUTDOWN: Se ejecuta al cerrar la app
    print("🛑 Cerrando aplicación...")


# Crear app con lifespan
app = FastAPI(
    title="API de Tareas con SQLAlchemy",
    description="CRUD completo usando FastAPI + SQLAlchemy 2.0",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/", tags=["Health"])
def health_check():
    """Endpoint de salud para verificar que la API está activa"""
    return {"status": "ok", "message": "API con SQLAlchemy funcionando"}


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
        HTTPException: Si la validación falla (Pydantic)
    """
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
    tarea = servicio.obtener(id)
    if not tarea:
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
    tarea = servicio.actualizar(id, tarea_data)
    if not tarea:
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
    eliminada = servicio.eliminar(id)
    if not eliminada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con id {id} no encontrada"
        )
