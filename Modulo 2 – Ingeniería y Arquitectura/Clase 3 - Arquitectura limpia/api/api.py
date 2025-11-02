"""API REST de tareas con FastAPI y validaciones avanzadas.

Este módulo implementa los endpoints REST para la gestión de tareas,
usando Pydantic para validaciones robustas y FastAPI para la API.
"""

from datetime import date
from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field, field_validator, model_validator

from api.servicio_tareas import ServicioTareas

__all__ = ['app', 'CrearTareaRequest', 'TareaResponse', 'crear_tarea', 'listar_tareas', 'obtener_servicio']


app = FastAPI(
    title="API de Tareas",
    description="API educativa - Clase 3 con validaciones avanzadas y Dependency Injection",
    version="1.0.0"
)


def obtener_servicio() -> ServicioTareas:
    """Factory function para inyectar el servicio de tareas.

    Esta función crea una instancia del servicio que se inyecta
    automáticamente en los endpoints mediante Depends().

    Returns:
        ServicioTareas: Instancia del servicio de tareas

    Note:
        En aplicaciones reales, aquí podrías:
        - Inyectar diferentes implementaciones (memoria, BD, etc.)
        - Configurar el servicio según el entorno
        - Aplicar decoradores o middleware

    Example:
        >>> @app.get("/tareas")
        >>> def listar(servicio: ServicioTareas = Depends(obtener_servicio)):
        >>>     return servicio.listar()
    """
    return ServicioTareas()


class CrearTareaRequest(BaseModel):
    """Request para crear tarea con validaciones robustas.

    Valida y sanitiza todos los campos de entrada para crear una tarea.
    Los validadores personalizados garantizan integridad de datos.

    Attributes:
        nombre: Nombre de la tarea (1-100 caracteres, se capitaliza automáticamente)
        prioridad: Nivel de prioridad 1 (urgente) a 5 (baja), default 3
        fecha_limite: Fecha límite opcional, debe ser futura
        etiquetas: Lista de hasta 10 etiquetas (se normalizan automáticamente)

    Note:
        Validadores automáticos aplicados:

        - **nombre**: Sanitizado (capitalizado, sin espacios extra)
        - **fecha_limite**: Debe ser futura (no pasada)
        - **etiquetas**: Normalizadas (lowercase, sin duplicados)
        - **prioridad 1-2**: Requieren fecha límite obligatoria

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


class TareaResponse(BaseModel):
    """Response model para tareas.

    Este modelo define la estructura de las respuestas de la API,
    separando concerns entre Request y Response models.

    Attributes:
        id: Identificador único de la tarea
        nombre: Nombre de la tarea
        completada: Estado de completitud
        prioridad: Nivel de prioridad 1-5
        fecha_limite: Fecha límite opcional
        etiquetas: Lista de etiquetas

    Note:
        La configuración `from_attributes=True` permite que Pydantic
        convierta objetos Tarea del servicio a este modelo de respuesta,
        validando automáticamente que todos los campos sean correctos.

    Example:
        >>> tarea_servicio = Tarea(id=1, nombre="Test", completada=False)
        >>> response = TareaResponse.model_validate(tarea_servicio)
        >>> response.id
        1
    """
    id: int
    nombre: str
    completada: bool
    prioridad: int
    fecha_limite: date | None
    etiquetas: list[str]

    model_config = {"from_attributes": True}


@app.post("/tareas", status_code=201, response_model=TareaResponse)
def crear_tarea(
    cuerpo: CrearTareaRequest,
    servicio: Annotated[ServicioTareas, Depends(obtener_servicio)]
) -> TareaResponse:
    """Crea una nueva tarea en el sistema.

    Args:
        cuerpo: Datos de la tarea a crear (validados por Pydantic)
        servicio: Servicio de tareas inyectado automáticamente por FastAPI

    Returns:
        TareaResponse validado con los datos de la tarea creada

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

    Note:
        El servicio se inyecta automáticamente mediante Depends(),
        permitiendo testear fácilmente con mocks y facilitar el cambio
        de implementaciones (memoria → base de datos).
    """
    tarea = servicio.crear(
        nombre=cuerpo.nombre,
        prioridad=cuerpo.prioridad,
        fecha_limite=cuerpo.fecha_limite,
        etiquetas=cuerpo.etiquetas
    )
    # Validar respuesta con Pydantic antes de retornar
    return TareaResponse.model_validate(tarea)


@app.get("/tareas", response_model=list[TareaResponse])
def listar_tareas(
    servicio: Annotated[ServicioTareas, Depends(obtener_servicio)]
) -> list[TareaResponse]:
    """Lista todas las tareas almacenadas.

    Args:
        servicio: Servicio de tareas inyectado automáticamente por FastAPI

    Returns:
        Lista de TareaResponse validadas con los datos de cada tarea

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
        Cada tarea se valida con Pydantic antes de retornar.
    """
    tareas = servicio.listar()
    # Validar cada tarea con Pydantic antes de retornar
    return [TareaResponse.model_validate(tarea) for tarea in tareas]
