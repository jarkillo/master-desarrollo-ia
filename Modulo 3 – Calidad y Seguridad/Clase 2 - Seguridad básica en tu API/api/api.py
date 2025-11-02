# api/api.py
from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field, constr

from api.dependencias import verificar_api_key
from api.repositorio_json import RepositorioJSON
from api.servicio_tareas import ServicioTareas

app = FastAPI()


# repositorio = RepositorioMemoria()
repositorio = RepositorioJSON("tareas.json")  # por ejemplo, dentro de /data
servicio = ServicioTareas(repositorio)


class CrearTareaRequest(BaseModel):
    nombre: constr(min_length=1, max_length=100)
    prioridad: str = Field(default="media", pattern="^(alta|media|baja)$")


@app.post("/tareas", status_code=201, dependencies=[Depends(verificar_api_key)])
def crear_tarea(cuerpo: CrearTareaRequest):
    tarea = servicio.crear(cuerpo.nombre)
    return tarea.model_dump()


@app.get("/tareas", dependencies=[Depends(verificar_api_key)])
def listar_tareas():
    return [tarea.model_dump() for tarea in servicio.listar()]
