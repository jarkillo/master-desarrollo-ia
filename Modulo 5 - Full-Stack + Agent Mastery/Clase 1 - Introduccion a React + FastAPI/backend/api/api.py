# api/api.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from api.repositorio_memoria import RepositorioMemoria
from api.servicio_tareas import ServicioTareas

# Configuración de la aplicación FastAPI
app = FastAPI(
    title="API de Tareas",
    description="API RESTful para gestión de tareas con React + FastAPI",
    version="1.0.0"
)

# Configuración de CORS para permitir peticiones desde el frontend React
# En desarrollo, permite cualquier origen. En producción, especifica dominios exactos.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Puerto por defecto de Vite
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Permite todos los headers
)

# Inicialización del repositorio y servicio (Dependency Injection)
repositorio = RepositorioMemoria()
servicio = ServicioTareas(repositorio)


# --- Modelos de Request/Response ---

class CrearTareaRequest(BaseModel):
    """Modelo para crear una nueva tarea."""
    nombre: str = Field(..., min_length=1, max_length=200, description="Nombre de la tarea")


class ActualizarTareaRequest(BaseModel):
    """Modelo para actualizar el estado de una tarea."""
    completada: bool = Field(..., description="Estado de completitud")


class TareaResponse(BaseModel):
    """Modelo de respuesta para una tarea."""
    id: int
    nombre: str
    completada: bool


# --- Endpoints ---

@app.get("/")
def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "API de Tareas funcionando correctamente",
        "version": "1.0.0"
    }


@app.post("/tareas", status_code=201, response_model=TareaResponse)
def crear_tarea(cuerpo: CrearTareaRequest):
    """Crea una nueva tarea.

    Returns:
        201 Created: Tarea creada exitosamente
        422 Unprocessable Entity: Datos de entrada inválidos
    """
    try:
        tarea = servicio.crear(cuerpo.nombre)
        return tarea.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.get("/tareas", response_model=list[TareaResponse])
def listar_tareas():
    """Lista todas las tareas.

    Returns:
        200 OK: Lista de tareas (puede estar vacía)
    """
    return [tarea.model_dump() for tarea in servicio.listar()]


@app.get("/tareas/{id}", response_model=TareaResponse)
def obtener_tarea(id: int):
    """Obtiene una tarea por ID.

    Args:
        id: ID de la tarea

    Returns:
        200 OK: Tarea encontrada
        404 Not Found: Tarea no existe
    """
    tarea = servicio.obtener(id)
    if tarea is None:
        raise HTTPException(status_code=404, detail=f"Tarea con ID {id} no encontrada")
    return tarea.model_dump()


@app.patch("/tareas/{id}", response_model=TareaResponse)
def actualizar_tarea(id: int, cuerpo: ActualizarTareaRequest):
    """Actualiza el estado de completitud de una tarea.

    Args:
        id: ID de la tarea
        cuerpo: Nuevo estado de completitud

    Returns:
        200 OK: Tarea actualizada
        404 Not Found: Tarea no existe
    """
    tarea = servicio.marcar_completada(id, cuerpo.completada)
    if tarea is None:
        raise HTTPException(status_code=404, detail=f"Tarea con ID {id} no encontrada")
    return tarea.model_dump()


@app.delete("/tareas/{id}", status_code=204)
def eliminar_tarea(id: int):
    """Elimina una tarea.

    Args:
        id: ID de la tarea

    Returns:
        204 No Content: Tarea eliminada exitosamente
        404 Not Found: Tarea no existe
    """
    eliminada = servicio.eliminar(id)
    if not eliminada:
        raise HTTPException(status_code=404, detail=f"Tarea con ID {id} no encontrada")
    return None
