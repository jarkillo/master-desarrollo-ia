"""API REST de tareas con FastAPI y validaciones avanzadas.

Este módulo implementa los endpoints REST para la gestión de tareas,
usando Pydantic para validaciones robustas y FastAPI para la API.
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import date
from typing import Any
from api.servicio_tareas import ServicioTareas


__all__ = ['app', 'CrearTareaRequest', 'crear_tarea', 'listar_tareas']


app = FastAPI(
    title="API de Tareas",
    description="API educativa - Clase 3 con validaciones avanzadas",
    version="1.0.0"
)
servicio = ServicioTareas()


class CrearTareaRequest(BaseModel):
    """Request para crear tarea con validaciones robustas.

    Valida y sanitiza todos los campos de entrada para crear una tarea.
    Incluye validadores personalizados para reglas de negocio complejas.

    Attributes:
        nombre: Nombre de la tarea (1-100 caracteres, se capitaliza automáticamente)
        prioridad: Nivel de prioridad 1 (urgente) a 5 (baja), default 3
        fecha_limite: Fecha límite opcional, debe ser futura
        etiquetas: Lista de hasta 10 etiquetas (se normalizan automáticamente)

    Validators:
        - nombre_no_solo_espacios: Sanitiza y valida el nombre
        - fecha_no_pasada: Valida que la fecha límite sea futura
        - normalizar_etiquetas: Normaliza a lowercase, elimina duplicados
        - validar_tareas_urgentes: Requiere fecha límite para prioridad 1-2

    Example:
        >>> request = CrearTareaRequest(
        ...     nombre="estudiar pydantic",
        ...     prioridad=1,
        ...     fecha_limite=date(2025, 12, 31),
        ...     etiquetas=["Python", "EDUCACIÓN"]
        ... )
        >>> request.nombre
        'Estudiar pydantic'
        >>> request.etiquetas
        ['python', 'educación']
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
        """Valida y sanitiza el nombre de la tarea.

        Args:
            v: Nombre a validar

        Returns:
            Nombre sanitizado (capitalizado, sin espacios extra)

        Raises:
            ValueError: Si el nombre está vacío o es solo espacios
        """
        v = v.strip()
        if not v:
            raise ValueError('El nombre no puede estar vacío o ser solo espacios')
        return v.capitalize()

    @field_validator('fecha_limite')
    @classmethod
    def fecha_no_pasada(cls, v: date | None) -> date | None:
        """Valida que la fecha límite no sea pasada.

        Args:
            v: Fecha límite a validar

        Returns:
            Fecha validada o None

        Raises:
            ValueError: Si la fecha está en el pasado
        """
        if v is not None and v < date.today():
            raise ValueError(
                f'La fecha límite no puede estar en el pasado '
                f'(recibido: {v}, hoy: {date.today()})'
            )
        return v

    @field_validator('etiquetas')
    @classmethod
    def normalizar_etiquetas(cls, v: list[str]) -> list[str]:
        """Normaliza etiquetas: lowercase, strip, unique.

        Args:
            v: Lista de etiquetas a normalizar

        Returns:
            Lista de etiquetas normalizadas (lowercase, sin duplicados)
        """
        etiquetas_normalizadas = [tag.lower().strip() for tag in v]
        # Eliminar duplicados manteniendo orden
        return list(dict.fromkeys(etiquetas_normalizadas))

    @model_validator(mode='after')
    def validar_tareas_urgentes(self) -> 'CrearTareaRequest':
        """Tareas urgentes (prioridad 1-2) requieren fecha límite.

        Returns:
            Self para encadenamiento

        Raises:
            ValueError: Si tarea urgente no tiene fecha límite
        """
        if self.prioridad <= 2 and self.fecha_limite is None:
            raise ValueError(
                f'Las tareas urgentes (prioridad {self.prioridad}) '
                'requieren una fecha límite'
            )
        return self


@app.post("/tareas", status_code=201)
def crear_tarea(cuerpo: CrearTareaRequest) -> dict[str, Any]:
    """Crea una nueva tarea en el sistema.

    Args:
        cuerpo: Datos de la tarea a crear (validados por Pydantic)

    Returns:
        Diccionario con los datos de la tarea creada incluyendo ID

    Example:
        POST /tareas
        {
            "nombre": "Estudiar Python",
            "prioridad": 1,
            "fecha_limite": "2025-12-31",
            "etiquetas": ["python", "educación"]
        }

        Response 201:
        {
            "id": 1,
            "nombre": "Estudiar python",
            "completada": false,
            "prioridad": 1,
            "fecha_limite": "2025-12-31",
            "etiquetas": ["python", "educación"]
        }
    """
    tarea = servicio.crear(
        nombre=cuerpo.nombre,
        prioridad=cuerpo.prioridad,
        fecha_limite=cuerpo.fecha_limite,
        etiquetas=cuerpo.etiquetas
    )
    return tarea.model_dump()


@app.get("/tareas")
def listar_tareas() -> list[dict[str, Any]]:
    """Lista todas las tareas almacenadas.

    Returns:
        Lista de diccionarios con los datos de cada tarea

    Example:
        GET /tareas

        Response 200:
        [
            {
                "id": 1,
                "nombre": "Estudiar python",
                "completada": false,
                "prioridad": 1,
                "fecha_limite": "2025-12-31",
                "etiquetas": ["python", "educación"]
            },
            {
                "id": 2,
                "nombre": "Revisar código",
                "completada": true,
                "prioridad": 3,
                "fecha_limite": null,
                "etiquetas": []
            }
        ]

    Note:
        Retorna una lista vacía si no hay tareas.
    """
    return [tarea.model_dump() for tarea in servicio.listar()]
