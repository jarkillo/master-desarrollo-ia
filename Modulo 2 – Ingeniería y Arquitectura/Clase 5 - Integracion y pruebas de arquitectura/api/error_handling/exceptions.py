"""
Custom Exception Classes para FastAPI
Ejemplo de implementación profesional
"""

from typing import Any

from fastapi import HTTPException


class BaseAPIException(HTTPException):
    """Excepción base para toda la API"""

    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str,
        context: dict[str, Any] | None = None
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

    def __init__(self, operation: str, original_error: Exception | None = None):
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
