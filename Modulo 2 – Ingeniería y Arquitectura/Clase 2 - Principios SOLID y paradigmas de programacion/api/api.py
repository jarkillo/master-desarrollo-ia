# api/api.py

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

# === MODELS ===

class TareaResponse(BaseModel):
    """Modelo de respuesta para una tarea."""
    id: int
    nombre: str
    completada: bool


class CrearTareaRequest(BaseModel):
    """Modelo de request para crear una tarea."""
    nombre: str = Field(..., min_length=1, description="Nombre de la tarea")


# === APPLICATION ===

app = FastAPI(
    title="API de Tareas",
    description="API REST para gestionar tareas con SOLID y TDD",
    version="1.0.0"
)

# Almacenamiento en memoria (simple para la clase)
_tareas: list[TareaResponse] = []
_contador_id: int = 0


# === ENDPOINTS ===

@app.post(
    "/tareas",
    response_model=TareaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva tarea",
    tags=["tareas"]
)
def crear_tarea(cuerpo: CrearTareaRequest) -> TareaResponse:
    """Crea una nueva tarea.

    Args:
        cuerpo: Datos de la tarea a crear (nombre requerido)

    Returns:
        Tarea creada con id asignado y estado inicial (no completada)
    """
    global _contador_id
    _contador_id += 1

    nueva_tarea = TareaResponse(
        id=_contador_id,
        nombre=cuerpo.nombre,
        completada=False
    )
    _tareas.append(nueva_tarea)

    return nueva_tarea


@app.get(
    "/tareas",
    response_model=list[TareaResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todas las tareas",
    tags=["tareas"]
)
def listar_tareas() -> list[TareaResponse]:
    """Devuelve la lista completa de tareas.

    Returns:
        Lista de todas las tareas (puede estar vacía)
    """
    return _tareas


@app.get(
    "/tareas/{id}",
    response_model=TareaResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener una tarea específica",
    tags=["tareas"],
    responses={
        200: {"description": "Tarea encontrada"},
        404: {"description": "Tarea no encontrada"}
    }
)
def obtener_tarea(id: int) -> TareaResponse:
    """Devuelve una tarea específica por su ID.

    Args:
        id: ID de la tarea a buscar

    Returns:
        Tarea encontrada con todos sus datos

    Raises:
        HTTPException: 404 si la tarea no existe
    """
    for tarea in _tareas:
        if tarea.id == id:
            return tarea

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tarea con id {id} no encontrada"
    )


@app.put(
    "/tareas/{id}/completar",
    response_model=TareaResponse,
    status_code=status.HTTP_200_OK,
    summary="Marcar tarea como completada",
    tags=["tareas"],
    responses={
        200: {"description": "Tarea actualizada correctamente"},
        404: {"description": "Tarea no encontrada"}
    }
)
def completar_tarea(id: int) -> TareaResponse:
    """Marca una tarea como completada.

    Args:
        id: ID de la tarea a completar

    Returns:
        Tarea actualizada con completada=True

    Raises:
        HTTPException: 404 si la tarea no existe
    """
    for tarea in _tareas:
        if tarea.id == id:
            tarea.completada = True
            return tarea

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tarea con id {id} no encontrada"
    )


@app.delete(
    "/tareas/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una tarea",
    tags=["tareas"],
    responses={
        204: {"description": "Tarea eliminada correctamente"},
        404: {"description": "Tarea no encontrada"}
    }
)
def eliminar_tarea(id: int) -> None:
    """Elimina una tarea por su ID.

    Args:
        id: ID de la tarea a eliminar

    Raises:
        HTTPException: 404 si la tarea no existe
    """
    for i, tarea in enumerate(_tareas):
        if tarea.id == id:
            _tareas.pop(i)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tarea con id {id} no encontrada"
    )
