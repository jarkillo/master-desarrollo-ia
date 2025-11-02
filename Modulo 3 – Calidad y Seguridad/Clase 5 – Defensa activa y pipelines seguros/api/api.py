# api/api.py
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, constr

from api.repositorio_memoria import RepositorioMemoria
from api.seguridad_jwt import crear_token, verificar_jwt  # <- NUEVO
from api.servicio_tareas import ServicioTareas

app = FastAPI()
servicio = ServicioTareas(RepositorioMemoria())


# ====== Login ======
class LoginRequest(BaseModel):
    usuario: constr(min_length=1)
    password: constr(min_length=1)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@app.post("/login", response_model=LoginResponse)
def login(cuerpo: LoginRequest):
    # Demo: credenciales fijas. En producción, valida contra tu store de usuarios.
    if cuerpo.usuario == "demo" and cuerpo.password == "demo":
        token = crear_token({"sub": cuerpo.usuario})
        return LoginResponse(access_token=token)
    raise HTTPException(status_code=401, detail="Credenciales inválidas")


# ====== Tareas ======
class CrearTareaRequest(BaseModel):
    nombre: constr(min_length=1, max_length=100)
    # si ya usabas prioridad, mantenla con default válido para no disparar 422:
    # prioridad: str = Field(default="media", pattern="^(alta|media|baja)$")


@app.post("/tareas", status_code=201, dependencies=[Depends(verificar_jwt)])
def crear_tarea(cuerpo: CrearTareaRequest):
    tarea = servicio.crear(cuerpo.nombre)
    return tarea.model_dump()


@app.get("/tareas", dependencies=[Depends(verificar_jwt)])
def listar_tareas():
    return [t.model_dump() for t in servicio.listar()]
