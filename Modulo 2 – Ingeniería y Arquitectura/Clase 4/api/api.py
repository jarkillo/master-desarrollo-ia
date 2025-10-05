# api.py
from fastapi import FastAPI
from api.servicio_tareas import ServicioTareas
from api.repositorio_memoria import RepositorioMemoria
from pydantic import BaseModel, Field

app = FastAPI()
repositorio = RepositorioMemoria()
servicio = ServicioTareas(repositorio)


class CrearTareaRequest(BaseModel):
    nombre: str = Field(..., min_length=1)


@app.post("/tareas", status_code=201)
def crear_tarea(cuerpo: CrearTareaRequest):
    tarea = servicio.crear(cuerpo.nombre)
    return tarea.model_dump()


@app.get("/tareas")
def listar_tareas():
    return [t.model_dump() for t in servicio.listar()]
