from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import date
from api.servicio_tareas import ServicioTareas

app = FastAPI(
    title="API de Tareas",
    description="API educativa - Clase 3 con validaciones avanzadas",
    version="1.0.0"
)
servicio = ServicioTareas()


class CrearTareaRequest(BaseModel):
    """Request para crear tarea con validaciones robustas.

    Example:
        {
            "nombre": "Estudiar Pydantic",
            "prioridad": 1,
            "fecha_limite": "2025-12-31",
            "etiquetas": ["python", "educación"]
        }
    """

    nombre: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre de la tarea (1-100 caracteres)",
        examples=["Estudiar Pydantic"]
    )

    prioridad: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Prioridad: 1 (urgente) a 5 (baja). Default: 3",
        examples=[1, 3, 5]
    )

    fecha_limite: date | None = Field(
        default=None,
        description="Fecha límite opcional (YYYY-MM-DD)",
        examples=["2025-12-31"]
    )

    etiquetas: list[str] = Field(
        default_factory=list,
        max_length=10,
        description="Lista de etiquetas (máximo 10)",
        examples=[["python", "educación"]]
    )

    @field_validator('nombre')
    @classmethod
    def nombre_no_solo_espacios(cls, v: str) -> str:
        """Valida y sanitiza el nombre de la tarea."""
        v = v.strip()
        if not v:
            raise ValueError('El nombre no puede estar vacío o ser solo espacios')
        return v.capitalize()

    @field_validator('fecha_limite')
    @classmethod
    def fecha_no_pasada(cls, v: date | None) -> date | None:
        """Valida que la fecha límite no sea pasada."""
        if v is not None and v < date.today():
            raise ValueError(
                f'La fecha límite no puede estar en el pasado '
                f'(recibido: {v}, hoy: {date.today()})'
            )
        return v

    @field_validator('etiquetas')
    @classmethod
    def normalizar_etiquetas(cls, v: list[str]) -> list[str]:
        """Normaliza etiquetas: lowercase, strip, unique."""
        etiquetas_normalizadas = [tag.lower().strip() for tag in v]
        # Eliminar duplicados manteniendo orden
        return list(dict.fromkeys(etiquetas_normalizadas))

    @model_validator(mode='after')
    def validar_tareas_urgentes(self):
        """Tareas urgentes (prioridad 1-2) requieren fecha límite."""
        if self.prioridad <= 2 and self.fecha_limite is None:
            raise ValueError(
                f'Las tareas urgentes (prioridad {self.prioridad}) '
                'requieren una fecha límite'
            )
        return self


@app.post("/tareas", status_code=201)
def crear_tarea(cuerpo: CrearTareaRequest):
    tarea = servicio.crear(
        nombre=cuerpo.nombre,
        prioridad=cuerpo.prioridad,
        fecha_limite=cuerpo.fecha_limite,
        etiquetas=cuerpo.etiquetas
    )
    return tarea.model_dump()


@app.get("/tareas")
def listar_tareas():
    return [tarea.model_dump() for tarea in servicio.listar()]
