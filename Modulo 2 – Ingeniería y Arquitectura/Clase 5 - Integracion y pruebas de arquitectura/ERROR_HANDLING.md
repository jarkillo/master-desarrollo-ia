# Error Handling Profesional en FastAPI

**Duración estimada**: 2 horas
**Nivel**: Intermedio-Avanzado

## 🎯 Objetivos de Aprendizaje

Al finalizar esta sección serás capaz de:

1. Crear custom exceptions para tu dominio
2. Implementar global exception handlers
3. Diseñar error responses estandarizados
4. Integrar logging estructurado de errores
5. Testear error handling correctamente

## 📚 Contenido

### 1. ¿Por Qué Error Handling Profesional?

#### El Problema: Errores Genéricos

```python
# ❌ MAL: Error genérico sin contexto
@app.get("/tareas/{tarea_id}")
def obtener_tarea(tarea_id: int):
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Not found")
    return tarea
```

**Problemas**:
- ❌ Mensaje vago ("Not found" - ¿qué no se encontró?)
- ❌ No hay tracking/logging
- ❌ Respuesta inconsistente entre endpoints
- ❌ Difícil de debuggear
- ❌ Mala experiencia de usuario

#### La Solución: Error Handling Estructurado

```python
# ✅ BIEN: Error específico con contexto
@app.get("/tareas/{tarea_id}")
def obtener_tarea(tarea_id: int):
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if not tarea:
        raise TareaNotFoundError(tarea_id=tarea_id)
    return tarea
```

**Beneficios**:
- ✅ Mensaje claro y específico
- ✅ Logging automático
- ✅ Respuesta estandarizada
- ✅ Fácil de debuggear
- ✅ Buena experiencia de usuario

### 2. Custom Exception Classes

#### Jerarquía de Excepciones

```python
# api/exceptions.py
from fastapi import HTTPException
from typing import Optional, Dict, Any


class BaseAPIException(HTTPException):
    """Excepción base para toda la API"""

    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str,
        context: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.context = context or {}


class ResourceNotFoundError(BaseAPIException):
    """Error cuando un recurso no existe"""

    def __init__(self, resource: str, identifier: Any):
        super().__init__(
            status_code=404,
            detail=f"{resource} no encontrado",
            error_code="RESOURCE_NOT_FOUND",
            context={"resource": resource, "identifier": identifier}
        )


class TareaNotFoundError(ResourceNotFoundError):
    """Error específico cuando una tarea no existe"""

    def __init__(self, tarea_id: int):
        super().__init__(resource="Tarea", identifier=tarea_id)


class InvalidDataError(BaseAPIException):
    """Error cuando los datos son inválidos"""

    def __init__(self, field: str, reason: str):
        super().__init__(
            status_code=400,
            detail=f"Dato inválido en campo '{field}': {reason}",
            error_code="INVALID_DATA",
            context={"field": field, "reason": reason}
        )


class BusinessRuleViolationError(BaseAPIException):
    """Error cuando se viola una regla de negocio"""

    def __init__(self, rule: str, explanation: str):
        super().__init__(
            status_code=422,
            detail=f"Regla de negocio violada: {rule}",
            error_code="BUSINESS_RULE_VIOLATION",
            context={"rule": rule, "explanation": explanation}
        )


class DatabaseError(BaseAPIException):
    """Error de base de datos"""

    def __init__(self, operation: str, original_error: Optional[Exception] = None):
        super().__init__(
            status_code=500,
            detail=f"Error de base de datos durante: {operation}",
            error_code="DATABASE_ERROR",
            context={
                "operation": operation,
                "original_error": str(original_error) if original_error else None
            }
        )


class AuthenticationError(BaseAPIException):
    """Error de autenticación"""

    def __init__(self, reason: str = "Credenciales inválidas"):
        super().__init__(
            status_code=401,
            detail=reason,
            error_code="AUTHENTICATION_FAILED",
            context={"reason": reason}
        )


class AuthorizationError(BaseAPIException):
    """Error de autorización (permisos)"""

    def __init__(self, resource: str, action: str):
        super().__init__(
            status_code=403,
            detail=f"No tienes permisos para {action} {resource}",
            error_code="AUTHORIZATION_FAILED",
            context={"resource": resource, "action": action}
        )
```

**Ventajas de esta jerarquía**:
- ✅ Fácil de extender (herencia)
- ✅ Información contextual rica
- ✅ Error codes consistentes
- ✅ Status codes apropiados
- ✅ Tipado fuerte (type hints)

### 3. Error Response Format Estandarizado

#### Diseño del Error Response

```python
# api/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class ErrorDetail(BaseModel):
    """Detalle de un error individual"""
    field: Optional[str] = Field(None, description="Campo que causó el error")
    message: str = Field(..., description="Mensaje de error")
    code: Optional[str] = Field(None, description="Código de error específico")


class ErrorResponse(BaseModel):
    """Respuesta de error estandarizada"""

    status_code: int = Field(..., description="HTTP status code")
    error_code: str = Field(..., description="Código de error interno")
    message: str = Field(..., description="Mensaje de error legible")
    details: Optional[list[ErrorDetail]] = Field(
        None,
        description="Detalles adicionales del error"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp del error"
    )
    path: str = Field(..., description="Ruta del endpoint")
    request_id: Optional[str] = Field(None, description="ID de request para tracking")
    context: Optional[Dict[str, Any]] = Field(
        None,
        description="Contexto adicional (solo en desarrollo)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "status_code": 404,
                "error_code": "RESOURCE_NOT_FOUND",
                "message": "Tarea no encontrada",
                "details": [
                    {
                        "field": "tarea_id",
                        "message": "Tarea con ID 123 no existe",
                        "code": "NOT_FOUND"
                    }
                ],
                "timestamp": "2025-11-02T10:30:00Z",
                "path": "/tareas/123",
                "request_id": "abc-123-def",
                "context": {"tarea_id": 123}
            }
        }
```

### 4. Global Exception Handlers

#### Configuración de Handlers

```python
# api/error_handlers.py
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import traceback
from typing import Union
import uuid

from .exceptions import BaseAPIException
from .schemas import ErrorResponse, ErrorDetail

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI):
    """Configura todos los exception handlers de la aplicación"""

    @app.exception_handler(BaseAPIException)
    async def custom_exception_handler(
        request: Request,
        exc: BaseAPIException
    ) -> JSONResponse:
        """Handler para nuestras custom exceptions"""

        request_id = str(uuid.uuid4())

        # Log el error
        logger.error(
            f"[{request_id}] {exc.error_code}: {exc.detail}",
            extra={
                "request_id": request_id,
                "path": request.url.path,
                "method": request.method,
                "error_code": exc.error_code,
                "context": exc.context
            }
        )

        # Crear error response
        error_response = ErrorResponse(
            status_code=exc.status_code,
            error_code=exc.error_code,
            message=exc.detail,
            path=str(request.url.path),
            request_id=request_id,
            context=exc.context if app.debug else None  # Solo en dev
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.model_dump()
        )


    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ) -> JSONResponse:
        """Handler para errores de validación de Pydantic"""

        request_id = str(uuid.uuid4())

        # Convertir errores de Pydantic a nuestro formato
        details = []
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            details.append(
                ErrorDetail(
                    field=field,
                    message=error["msg"],
                    code=error["type"]
                ).model_dump()
            )

        logger.warning(
            f"[{request_id}] Validation error: {len(details)} campos inválidos",
            extra={
                "request_id": request_id,
                "path": request.url.path,
                "errors": details
            }
        )

        error_response = ErrorResponse(
            status_code=422,
            error_code="VALIDATION_ERROR",
            message="Datos de entrada inválidos",
            details=details,
            path=str(request.url.path),
            request_id=request_id
        )

        return JSONResponse(
            status_code=422,
            content=error_response.model_dump()
        )


    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request,
        exc: StarletteHTTPException
    ) -> JSONResponse:
        """Handler para HTTPException estándar"""

        request_id = str(uuid.uuid4())

        logger.warning(
            f"[{request_id}] HTTP {exc.status_code}: {exc.detail}",
            extra={
                "request_id": request_id,
                "path": request.url.path,
                "status_code": exc.status_code
            }
        )

        error_response = ErrorResponse(
            status_code=exc.status_code,
            error_code=f"HTTP_{exc.status_code}",
            message=exc.detail,
            path=str(request.url.path),
            request_id=request_id
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.model_dump()
        )


    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception
    ) -> JSONResponse:
        """Handler para excepciones no manejadas"""

        request_id = str(uuid.uuid4())

        # Log completo con stacktrace
        logger.exception(
            f"[{request_id}] Unhandled exception: {type(exc).__name__}",
            extra={
                "request_id": request_id,
                "path": request.url.path,
                "exception_type": type(exc).__name__
            }
        )

        # En producción, no exponer detalles
        if app.debug:
            message = f"{type(exc).__name__}: {str(exc)}"
            context = {"traceback": traceback.format_exc()}
        else:
            message = "Error interno del servidor"
            context = None

        error_response = ErrorResponse(
            status_code=500,
            error_code="INTERNAL_SERVER_ERROR",
            message=message,
            path=str(request.url.path),
            request_id=request_id,
            context=context
        )

        return JSONResponse(
            status_code=500,
            content=error_response.model_dump()
        )
```

#### Integración en la Aplicación

```python
# api/api.py
from fastapi import FastAPI
from .error_handlers import setup_exception_handlers

app = FastAPI(
    title="API Tareas",
    description="API con error handling profesional",
    version="1.0.0",
    debug=False  # Cambia a True en desarrollo
)

# Configurar exception handlers
setup_exception_handlers(app)

# Tus endpoints aquí...
```

### 5. Logging Estructurado

#### Configuración de Logging

```python
# api/logging_config.py
import logging
import logging.config
from typing import Any, Dict

LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "json",
            "filename": "logs/errors.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
    },
    "loggers": {
        "api": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
}


def setup_logging():
    """Configura el sistema de logging"""
    logging.config.dictConfig(LOGGING_CONFIG)
```

#### Uso en Endpoints

```python
# api/api.py
import logging
from .exceptions import TareaNotFoundError, InvalidDataError

logger = logging.getLogger(__name__)

@app.post("/tareas")
async def crear_tarea(tarea: TareaCreate):
    try:
        logger.info(f"Creando tarea: {tarea.nombre}")

        # Validación de negocio
        if len(tarea.nombre) < 3:
            raise InvalidDataError(
                field="nombre",
                reason="El nombre debe tener al menos 3 caracteres"
            )

        nueva_tarea = servicio.crear_tarea(tarea)
        logger.info(f"Tarea creada exitosamente: ID {nueva_tarea.id}")
        return nueva_tarea

    except InvalidDataError:
        raise  # Re-raise para que el handler lo maneje
    except Exception as e:
        logger.exception(f"Error inesperado creando tarea: {e}")
        raise DatabaseError("crear tarea", e)
```

### 6. Middleware de Request ID

```python
# api/middleware.py
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Agrega request_id a cada request para tracking"""

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        logger.info(
            f"[{request_id}] {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host if request.client else None
            }
        )

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        return response


# En api.py
from .middleware import RequestIDMiddleware

app.add_middleware(RequestIDMiddleware)
```

### 7. Ejemplos Prácticos

#### Ejemplo 1: Endpoint con Error Handling Completo

```python
from fastapi import FastAPI, Depends
from .exceptions import TareaNotFoundError, AuthorizationError
from .schemas import TareaResponse
import logging

logger = logging.getLogger(__name__)

@app.get("/tareas/{tarea_id}", response_model=TareaResponse)
async def obtener_tarea(
    tarea_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene una tarea por ID.

    Raises:
        TareaNotFoundError: Si la tarea no existe
        AuthorizationError: Si el usuario no tiene permisos
    """
    logger.info(f"Usuario {current_user.id} solicitando tarea {tarea_id}")

    # Buscar tarea
    tarea = servicio.obtener_tarea(tarea_id)
    if not tarea:
        raise TareaNotFoundError(tarea_id=tarea_id)

    # Verificar permisos
    if tarea.usuario_id != current_user.id:
        raise AuthorizationError(
            resource="tarea",
            action="ver"
        )

    logger.info(f"Tarea {tarea_id} obtenida exitosamente")
    return tarea
```

#### Ejemplo 2: Manejo de Errores de Base de Datos

```python
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

@app.post("/tareas", status_code=201)
async def crear_tarea(tarea: TareaCreate):
    try:
        nueva_tarea = servicio.crear_tarea(tarea)
        return nueva_tarea

    except IntegrityError as e:
        # Violación de constraint (ej: duplicado)
        logger.error(f"IntegrityError: {e}")
        raise BusinessRuleViolationError(
            rule="Unicidad de nombre",
            explanation="Ya existe una tarea con este nombre"
        )

    except SQLAlchemyError as e:
        # Otros errores de DB
        logger.exception(f"Database error: {e}")
        raise DatabaseError("crear tarea", e)
```

### 8. Testing Error Handling

#### Tests de Custom Exceptions

```python
# tests/test_error_handling.py
import pytest
from fastapi.testclient import TestClient
from api.api import app
from api.exceptions import TareaNotFoundError

client = TestClient(app)


def test_tarea_not_found_returns_404():
    """Test que tarea no encontrada retorna 404 con formato correcto"""
    response = client.get("/tareas/99999")

    assert response.status_code == 404

    data = response.json()
    assert data["status_code"] == 404
    assert data["error_code"] == "RESOURCE_NOT_FOUND"
    assert "Tarea" in data["message"]
    assert data["path"] == "/tareas/99999"
    assert "request_id" in data


def test_validation_error_returns_422():
    """Test que datos inválidos retornan 422 con detalles"""
    response = client.post("/tareas", json={"nombre": ""})

    assert response.status_code == 422

    data = response.json()
    assert data["status_code"] == 422
    assert data["error_code"] == "VALIDATION_ERROR"
    assert len(data["details"]) > 0
    assert data["details"][0]["field"] == "nombre"


def test_authorization_error_returns_403():
    """Test que falta de permisos retorna 403"""
    # Simular usuario sin permisos
    response = client.get(
        "/tareas/1",
        headers={"Authorization": "Bearer token_usuario_diferente"}
    )

    assert response.status_code == 403

    data = response.json()
    assert data["error_code"] == "AUTHORIZATION_FAILED"


def test_error_response_has_request_id():
    """Test que todas las respuestas de error tienen request_id"""
    response = client.get("/tareas/99999")

    assert response.status_code == 404
    assert "request_id" in response.json()
    assert "X-Request-ID" in response.headers


def test_internal_error_hides_details_in_production(monkeypatch):
    """Test que errores internos no exponen detalles en producción"""
    # Simular error interno
    def mock_servicio():
        raise Exception("Error de base de datos sensible")

    monkeypatch.setattr("api.api.servicio.obtener_tarea", mock_servicio)

    response = client.get("/tareas/1")

    assert response.status_code == 500
    data = response.json()
    assert data["error_code"] == "INTERNAL_SERVER_ERROR"
    assert "sensible" not in data["message"]  # No expone detalles
    assert data.get("context") is None  # No contexto en producción
```

### 9. Best Practices

#### ✅ DO: Buenas Prácticas

1. **Usa custom exceptions específicas**
   ```python
   # ✅ Específico y claro
   raise TareaNotFoundError(tarea_id=123)

   # ❌ Genérico
   raise HTTPException(404, "Not found")
   ```

2. **Incluye contexto en excepciones**
   ```python
   # ✅ Con contexto
   raise InvalidDataError(
       field="fecha_vencimiento",
       reason="Debe ser fecha futura"
   )
   ```

3. **Log antes de raise**
   ```python
   # ✅ Log + raise
   logger.error(f"Tarea {tarea_id} no encontrada")
   raise TareaNotFoundError(tarea_id=tarea_id)
   ```

4. **Usa error codes consistentes**
   ```python
   # ✅ Códigos estandarizados
   RESOURCE_NOT_FOUND
   VALIDATION_ERROR
   AUTHORIZATION_FAILED
   ```

5. **Oculta detalles en producción**
   ```python
   # ✅ Solo en debug
   context=exc.context if app.debug else None
   ```

#### ❌ DON'T: Anti-Patrones

1. **No expongas stack traces en producción**
   ```python
   # ❌ Expone información sensible
   return {"error": str(traceback.format_exc())}
   ```

2. **No uses status codes incorrectos**
   ```python
   # ❌ 200 OK con error
   return {"error": "Tarea no encontrada"}

   # ✅ 404 Not Found
   raise TareaNotFoundError(tarea_id=tarea_id)
   ```

3. **No captures Exception sin re-raise**
   ```python
   # ❌ Swallow exception
   try:
       operacion_critica()
   except Exception:
       pass  # Error silenciado

   # ✅ Log y re-raise o maneja específicamente
   try:
       operacion_critica()
   except Exception as e:
       logger.exception("Error crítico")
       raise DatabaseError("operación", e)
   ```

### 10. Checklist de Error Handling

- [ ] Custom exception classes creadas
- [ ] Global exception handlers configurados
- [ ] Error response format estandarizado
- [ ] Logging estructurado implementado
- [ ] Request ID tracking habilitado
- [ ] Tests de error handling completos
- [ ] Documentación de errores en OpenAPI
- [ ] Detalles ocultos en producción

## 🎯 Ejercicios Prácticos

Ver `EJERCICIOS_ERROR_HANDLING.md` para ejercicios prácticos.

## 📖 Recursos Adicionales

- [FastAPI Exception Handling](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [Python Logging HOWTO](https://docs.python.org/3/howto/logging.html)

---

**💡 Tip**: El error handling es lo que diferencia una API amateur de una profesional. Invierte tiempo en diseñarlo bien desde el principio.
