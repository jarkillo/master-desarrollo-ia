# api/api.py
"""
Mini API de Tareas - Clase 1 Módulo 2
API REST simple para gestión de tareas con FastAPI
"""


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Crear la aplicación FastAPI
app = FastAPI(
    title="API de Tareas",
    description="Una API simple para gestionar tareas - Clase 1 Módulo 2",
    version="1.0.0"
)

# Modelo para la request (lo que el cliente envía)
class CrearTareaRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200,
                        description="Nombre de la tarea")
    descripcion: str | None = Field(None, max_length=500,
                                       description="Descripción opcional de la tarea")

    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Estudiar FastAPI",
                "descripcion": "Completar el tutorial básico y hacer ejercicios"
            }
        }


# Modelo para la response (lo que la API devuelve)
class TareaResponse(BaseModel):
    id: int = Field(..., description="ID único de la tarea")
    nombre: str = Field(..., description="Nombre de la tarea")
    descripcion: str | None = Field(None, description="Descripción de la tarea")
    completada: bool = Field(False, description="Estado de la tarea")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Estudiar FastAPI",
                "descripcion": "Completar el tutorial básico y hacer ejercicios",
                "completada": False
            }
        }


# Almacenamiento temporal en memoria (se mejorará en Clase 2 con repositorios)
tareas_db = []
contador_id = 0


# Endpoint de salud (health check)
@app.get("/health")
def health_check():
    """
    Endpoint para verificar que la API está funcionando.

    Útil para monitoreo y deployment.

    Returns:
        dict: Estado de la API
    """
    return {"status": "ok", "message": "API de Tareas funcionando correctamente"}


@app.post("/tareas", response_model=TareaResponse, status_code=201)
def crear_tarea(tarea: CrearTareaRequest):
    """
    Crea una nueva tarea.

    - **nombre**: Nombre de la tarea (requerido, 1-200 caracteres)
    - **descripcion**: Descripción opcional (máximo 500 caracteres)

    Returns:
        TareaResponse: La tarea creada con su ID asignado

    Raises:
        HTTPException 422: Si la validación falla (nombre vacío, etc.)
    """
    global contador_id
    contador_id += 1

    nueva_tarea = TareaResponse(
        id=contador_id,
        nombre=tarea.nombre,
        descripcion=tarea.descripcion,
        completada=False
    )

    tareas_db.append(nueva_tarea.model_dump())
    return nueva_tarea


@app.get("/tareas", response_model=list[TareaResponse])
def listar_tareas():
    """
    Lista todas las tareas creadas.

    Devuelve un array de tareas (puede estar vacío si no hay ninguna).

    Returns:
        list[TareaResponse]: Lista de todas las tareas
    """
    return tareas_db


@app.get("/tareas/{tarea_id}", response_model=TareaResponse)
def obtener_tarea(tarea_id: int):
    """
    Obtiene una tarea específica por su ID.

    - **tarea_id**: ID de la tarea a buscar

    Returns:
        TareaResponse: La tarea encontrada

    Raises:
        HTTPException 404: Si la tarea no existe
    """
    for tarea in tareas_db:
        if tarea["id"] == tarea_id:
            return tarea

    raise HTTPException(
        status_code=404,
        detail=f"Tarea con id={tarea_id} no encontrada"
    )


@app.patch("/tareas/{tarea_id}/completar", response_model=TareaResponse)
def completar_tarea(tarea_id: int):
    """
    Marca una tarea como completada.

    - **tarea_id**: ID de la tarea a completar

    Returns:
        TareaResponse: La tarea actualizada con completada=True

    Raises:
        HTTPException 404: Si la tarea no existe
    """
    for tarea in tareas_db:
        if tarea["id"] == tarea_id:
            tarea["completada"] = True
            return tarea

    raise HTTPException(
        status_code=404,
        detail=f"Tarea con id={tarea_id} no encontrada"
    )
