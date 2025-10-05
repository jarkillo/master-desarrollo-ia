# api/api.py
from fastapi import FastAPI
from pydantic import BaseModel, Field
from api.servicio_tareas import ServicioTareas
from api.repositorio_memoria import RepositorioMemoria
from api.repositorio_json import RepositorioJSON

app = FastAPI()


# repositorio = RepositorioMemoria()
repositorio = RepositorioJSON("tareas.json")  # por ejemplo, dentro de /data
servicio = ServicioTareas(repositorio)


class CrearTareaRequest(BaseModel):
    nombre: str = Field(..., min_length=1)


@app.post("/tareas", status_code=201)
def crear_tarea(cuerpo: CrearTareaRequest):
    tarea = servicio.crear(cuerpo.nombre)
    return tarea.model_dump()


@app.get("/tareas")
def listar_tareas():
    return [tarea.model_dump() for tarea in servicio.listar()]
