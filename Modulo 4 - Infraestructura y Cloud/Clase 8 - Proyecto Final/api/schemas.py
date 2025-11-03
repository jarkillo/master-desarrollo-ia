"""
Schemas de Pydantic para validación de requests y responses.

Este módulo define los modelos de datos para la API,
separados de los modelos ORM de la base de datos.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

# ============================================================================
# SCHEMAS DE USUARIOS
# ============================================================================

class UsuarioBase(BaseModel):
    """Schema base para usuario (campos compartidos)."""
    email: EmailStr
    nombre: str = Field(..., min_length=1, max_length=200)


class UsuarioCreate(UsuarioBase):
    """Schema para crear un usuario (incluye contraseña)."""
    password: str = Field(..., min_length=8, max_length=100)


class UsuarioLogin(BaseModel):
    """Schema para login."""
    email: EmailStr
    password: str


class UsuarioResponse(UsuarioBase):
    """Schema para respuestas con datos del usuario."""
    id: int
    activo: bool
    creado_en: datetime
    actualizado_en: datetime

    model_config = ConfigDict(from_attributes=True)


class UsuarioMe(UsuarioResponse):
    """Schema para endpoint /auth/me (puede incluir más info)."""
    pass


# ============================================================================
# SCHEMAS DE AUTENTICACIÓN
# ============================================================================

class Token(BaseModel):
    """Schema para respuesta de token JWT."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema para datos decodificados del token."""
    email: str | None = None
    user_id: int | None = None


# ============================================================================
# SCHEMAS DE TAREAS
# ============================================================================

class TareaBase(BaseModel):
    """Schema base para tarea (campos compartidos)."""
    titulo: str = Field(..., min_length=1, max_length=200)
    descripcion: str | None = Field(None, max_length=1000)
    completada: bool = False
    prioridad: int = Field(default=2, ge=1, le=3)  # 1=Baja, 2=Media, 3=Alta


class TareaCreate(TareaBase):
    """Schema para crear una tarea."""
    pass


class TareaUpdate(BaseModel):
    """
    Schema para actualizar una tarea.
    Todos los campos son opcionales (PATCH semántico).
    """
    titulo: str | None = Field(None, min_length=1, max_length=200)
    descripcion: str | None = Field(None, max_length=1000)
    completada: bool | None = None
    prioridad: int | None = Field(None, ge=1, le=3)


class TareaResponse(TareaBase):
    """Schema para respuestas con datos de tarea."""
    id: int
    usuario_id: int
    eliminada: bool
    creado_en: datetime
    actualizado_en: datetime

    model_config = ConfigDict(from_attributes=True)


class TareaWithUsuario(TareaResponse):
    """Schema de tarea que incluye datos del usuario (para joins)."""
    usuario: UsuarioResponse


# ============================================================================
# SCHEMAS DE PAGINACIÓN Y FILTROS
# ============================================================================

class PaginationParams(BaseModel):
    """Parámetros de paginación."""
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)


class TareaFilters(BaseModel):
    """Filtros para búsqueda de tareas."""
    completada: bool | None = None
    prioridad: int | None = Field(None, ge=1, le=3)
    # Búsqueda en título - Solo permite letras, números, espacios y caracteres comunes
    # Pattern previene inyección de caracteres SQL especiales
    q: str | None = Field(
        None,
        max_length=200,
        pattern=r'^[a-zA-Z0-9\s\-_áéíóúÁÉÍÓÚñÑ]+$'
    )


class TareaListResponse(BaseModel):
    """Response con lista de tareas paginada."""
    items: list[TareaResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# ============================================================================
# SCHEMAS DE HEALTH CHECK
# ============================================================================

class HealthResponse(BaseModel):
    """Schema para respuesta del health check."""
    status: str
    environment: str
    database: str
    timestamp: datetime


# ============================================================================
# SCHEMAS DE ERRORES
# ============================================================================

class ErrorResponse(BaseModel):
    """Schema estándar para errores."""
    detail: str
    code: str | None = None
