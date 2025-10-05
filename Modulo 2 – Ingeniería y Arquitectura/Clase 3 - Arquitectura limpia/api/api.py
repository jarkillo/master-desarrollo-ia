from fastapi import FastAPI
from pydantic import BaseModel, Field
from api.servicio_tareas import ServicioTareas

app = FastAPI()
servicio = ServicioTareas()


class CrearTareaRequest(BaseModel):
    nombre: str = Field(..., min_length=1)


@app.post("/tareas", status_code=201)
def crear_tarea(cuerpo: CrearTareaRequest):
    tarea = servicio.crear(cuerpo.nombre)
    return tarea.model_dump()


@app.get("/tareas")
def listar_tareas():
    return [t.model_dump() for t in servicio.listar()]
