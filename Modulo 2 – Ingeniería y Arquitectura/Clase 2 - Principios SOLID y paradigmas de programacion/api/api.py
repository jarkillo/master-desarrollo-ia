# api/api.py
from fastapi import FastAPI
from pydantic import BaseModel, Field


class CrearTareaRequest(BaseModel):
    nombre: str = Field(..., min_length=1)


app = FastAPI()


@app.post("/tareas", status_code=201)
def crear_tarea(cuerpo: CrearTareaRequest):
    return {
        "id": 1,
        "nombre": cuerpo.nombre,
        "completada": False,
    }
