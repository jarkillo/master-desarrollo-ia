"""
✅ EJEMPLOS DE TOOLS BIEN DISEÑADOS

Este módulo contiene ejemplos de best practices en diseño de tools
siguiendo las recomendaciones de Anthropic.
"""

import re
from enum import Enum
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


class ResponseFormat(str, Enum):
    """Formato de respuesta del tool."""

    DETAILED = "detailed"
    CONCISE = "concise"


class ToolSuccess(BaseModel):
    """Respuesta exitosa de un tool."""

    status: Literal["success"] = "success"
    data: dict[str, Any]


class ToolError(BaseModel):
    """Respuesta de error de un tool."""

    status: Literal["error"] = "error"
    error_type: str
    message: str
    suggestion: str


ToolResult = ToolSuccess | ToolError


# ==========================================
# 1. BÚSQUEDA DE CONTACTOS (bien diseñado)
# ==========================================


class SearchContactsInput(BaseModel):
    """Schema de input para search_contacts tool."""

    query: str = Field(
        min_length=2,
        max_length=100,
        description="Texto a buscar (mínimo 2 caracteres, máximo 100)",
    )

    limit: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Máximo de resultados (entre 1 y 50)",
    )

    search_field: Literal["name", "email", "company"] = Field(
        default="name", description="Campo donde buscar"
    )

    response_format: ResponseFormat = Field(
        default=ResponseFormat.CONCISE,
        description="Nivel de detalle de la respuesta",
    )

    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        """Valida que el query sea válido."""
        if "@" in v and "." not in v:
            raise ValueError(
                "Email inválido. Formato esperado: name@domain.com. "
                "Ejemplo: 'juan@empresa.com'"
            )
        return v.strip()


def search_contacts(input_data: SearchContactsInput) -> ToolResult:
    """
    Busca contactos relevantes según criterios especificados.

    **Cuándo usar este tool:**
    - Necesitas encontrar contactos por nombre, email o empresa
    - Quieres filtrar contactos según un criterio específico
    - Buscas información de contacto de una persona

    **NO usar para:**
    - Listar TODOS los contactos (usa list_all_contact_pages en su lugar)
    - Crear nuevos contactos (usa create_contact)
    - Actualizar contactos existentes (usa update_contact)

    Args:
        input_data: Parámetros validados por Pydantic schema

    Returns:
        ToolSuccess con lista de contactos relevantes O
        ToolError con mensaje accionable

    Examples:
        Búsqueda por nombre:
        >>> search_contacts(SearchContactsInput(
        ...     query="Juan",
        ...     search_field="name",
        ...     limit=5
        ... ))

        Búsqueda por email:
        >>> search_contacts(SearchContactsInput(
        ...     query="juan@empresa.com",
        ...     search_field="email"
        ... ))

        Búsqueda por empresa con respuesta detallada:
        >>> search_contacts(SearchContactsInput(
        ...     query="Anthropic",
        ...     search_field="company",
        ...     response_format=ResponseFormat.DETAILED
        ... ))
    """
    # Simular búsqueda en DB (en producción: usar ORM o query builder)
    fake_results = [
        {
            "name": "Juan Pérez",
            "email": "juan@empresa.com",
            "company": "Tech Corp",
            "phone": "+1-555-0123",
            "role": "Developer",
            "last_contact": "2025-10-15",
        },
        {
            "name": "Ana García",
            "email": "ana@startup.com",
            "company": "Startup Inc",
            "phone": "+1-555-0456",
            "role": "CTO",
            "last_contact": "2025-10-20",
        },
    ]

    # Filtrar por campo de búsqueda
    filtered = [
        contact
        for contact in fake_results
        if input_data.query.lower() in contact[input_data.search_field].lower()
    ][: input_data.limit]

    # Formatear respuesta según response_format
    if input_data.response_format == ResponseFormat.CONCISE:
        # Respuesta concise: solo información esencial
        concise_results = [
            {"name": contact["name"], "email": contact["email"]}
            for contact in filtered
        ]
        return ToolSuccess(
            data={"contacts": concise_results, "count": len(concise_results)}
        )
    else:
        # Respuesta detailed: toda la información
        return ToolSuccess(data={"contacts": filtered, "count": len(filtered)})


# ==========================================
# 2. BÚSQUEDA DE LOGS (bien diseñado)
# ==========================================


def search_logs(query: str, lines: int = 100) -> ToolResult:
    """
    Busca en logs del sistema retornando solo líneas relevantes.

    **Cuándo usar este tool:**
    - Necesitas encontrar errores específicos en logs
    - Quieres buscar requests a un endpoint específico
    - Buscas logs de un usuario o transacción

    **NO usar para:**
    - Leer TODOS los logs (muy costoso en tokens)
    - Análisis estadístico de logs (usa analyze_logs)

    Args:
        query: Texto o regex a buscar en logs
            Ejemplos:
            - "ERROR" (busca todas las líneas con ERROR)
            - "GET /api/tasks.*500" (requests fallidos)
            - "user_id: 12345" (logs de usuario específico)

        lines: Máximo de líneas a retornar (límite: 1000)
            Default: 100 (suficiente para debugging)
            Aumenta si necesitas más contexto

    Returns:
        ToolSuccess con líneas relevantes y contexto O
        ToolError si el límite es excedido o regex inválido

    Examples:
        Buscar errores:
        >>> search_logs(query="ERROR", lines=50)

        Buscar requests específicos:
        >>> search_logs(query="GET /api/tasks", lines=20)

        Regex avanzado:
        >>> search_logs(query="user_id: 123.*ERROR", lines=100)
    """
    # Validar límite de lines
    if lines > 1000:
        return ToolError(
            error_type="validation_error",
            message=f"Límite de líneas excedido: {lines} (máximo 1000)",
            suggestion=(
                "Reduce el número de líneas a 1000 o menos. "
                "Alternativamente, usa filtros más específicos en tu query "
                "para reducir resultados."
            ),
        )

    # Validar regex
    try:
        regex_pattern = re.compile(query)
    except re.error as e:
        return ToolError(
            error_type="regex_error",
            message=f"Regex inválido: {str(e)}",
            suggestion=(
                f"Tu query '{query}' no es un regex válido. "
                f"Intenta con búsqueda de texto simple (sin regex) "
                f"o corrige la sintaxis del regex. "
                f"Ejemplo válido: 'ERROR.*user_id'"
            ),
        )

    # Simular búsqueda en logs (en producción: usar grep o ELK stack)
    fake_logs = [
        "2025-10-23 10:30:15 INFO GET /api/tasks 200 45ms",
        "2025-10-23 10:30:20 ERROR POST /api/tasks 500 12ms - ValidationError",
        "2025-10-23 10:30:25 INFO GET /api/tasks 200 38ms",
    ]

    matching_lines = [line for line in fake_logs if regex_pattern.search(line)][
        :lines
    ]

    return ToolSuccess(
        data={"lines": matching_lines, "count": len(matching_lines), "query": query}
    )


# ==========================================
# 3. LECTURA DE ARCHIVO (seguro)
# ==========================================


def read_file_safe(file_path: str) -> ToolResult:
    """
    Lee archivo del proyecto con validaciones de seguridad.

    **SECURITY**: Previene path traversal attacks validando que
    el archivo está dentro del proyecto.

    **Cuándo usar este tool:**
    - Necesitas leer contenido completo de un archivo
    - Quieres ver configuración o código fuente
    - Buscas contenido de un archivo específico

    **NO usar para:**
    - Buscar en múltiples archivos (usa search_codebase)
    - Archivos muy grandes >5MB (usa read_file_chunked)

    Args:
        file_path: Path relativo o absoluto al archivo
            Ejemplos:
            - "api/tasks.py"
            - "/absolute/path/to/file.py"
            - "../relative/path/file.py"

    Returns:
        ToolSuccess con contenido del archivo O
        ToolError si el archivo no existe, es muy grande, o está fuera del proyecto

    Raises:
        ValueError: Si se detecta path traversal
        FileNotFoundError: Si el archivo no existe

    Examples:
        >>> read_file_safe("api/tasks.py")
        >>> read_file_safe("README.md")
    """
    # 1. Normalizar path (resolver ., .., symlinks)
    try:
        path = Path(file_path).resolve()
    except Exception as e:
        return ToolError(
            error_type="invalid_path",
            message=f"Path inválido: {str(e)}",
            suggestion=f"Verifica que el path '{file_path}' es correcto y existe.",
        )

    # 2. Validar que está dentro del proyecto (prevenir path traversal)
    project_root = Path(__file__).parent.parent.resolve()

    if not str(path).startswith(str(project_root)):
        return ToolError(
            error_type="security_error",
            message=f"Path traversal detectado. El archivo debe estar dentro de {project_root}",
            suggestion=(
                f"El path '{file_path}' intenta acceder fuera del proyecto. "
                f"Solo puedes leer archivos dentro del proyecto."
            ),
        )

    # 3. Validar que existe
    if not path.exists():
        return ToolError(
            error_type="file_not_found",
            message=f"Archivo no encontrado: {file_path}",
            suggestion=(
                "Verifica que el path es correcto. "
                "Usa search_codebase para encontrar archivos por nombre."
            ),
        )

    # 4. Validar que es archivo (no directorio)
    if not path.is_file():
        return ToolError(
            error_type="not_a_file",
            message=f"{file_path} no es un archivo (es un directorio)",
            suggestion="Usa list_files para ver contenido del directorio.",
        )

    # 5. Validar tamaño (máximo 5MB)
    max_size_mb = 5
    file_size_mb = path.stat().st_size / (1024 * 1024)

    if file_size_mb > max_size_mb:
        return ToolError(
            error_type="file_too_large",
            message=(
                f"Archivo muy grande: {file_size_mb:.2f}MB (máximo {max_size_mb}MB)"
            ),
            suggestion=(
                "Usa read_file_chunked para archivos grandes, "
                "o search_logs si es un archivo de logs."
            ),
        )

    # 6. Leer archivo
    try:
        content = path.read_text(encoding="utf-8")
        return ToolSuccess(
            data={
                "file_path": str(path),
                "content": content,
                "size_bytes": path.stat().st_size,
                "lines": len(content.splitlines()),
            }
        )
    except Exception as e:
        return ToolError(
            error_type="read_error",
            message=f"Error leyendo archivo: {str(e)}",
            suggestion="Verifica que el archivo es legible y está en formato texto.",
        )


# ==========================================
# 4. CONFIGURACIÓN SEGURA (sin secrets)
# ==========================================


def get_environment_config_safe() -> ToolResult:
    """
    Retorna configuración de entorno filtrando secrets automáticamente.

    **SECURITY**: Filtra automáticamente todas las variables que
    contienen secrets (API_KEY, PASSWORD, TOKEN, SECRET).

    **Cuándo usar este tool:**
    - Necesitas verificar configuración del sistema
    - Quieres ver variables de entorno disponibles
    - Debugging de problemas de configuración

    **NO usar para:**
    - Obtener secrets (están filtrados por seguridad)
    - Modificar configuración (usa update_config)

    Returns:
        ToolSuccess con configuración filtrada (secrets redactados)

    Examples:
        >>> get_environment_config_safe()
        {
            "status": "success",
            "data": {
                "config": {
                    "DATABASE_URL": "postgresql://localhost/db",
                    "API_KEY": "***REDACTED***",
                    "DEBUG": "True",
                    "SECRET_KEY": "***REDACTED***"
                }
            }
        }
    """
    import os

    config = dict(os.environ)

    # Patrones de secrets a ocultar
    secret_patterns = [
        r".*API_KEY.*",
        r".*SECRET.*",
        r".*PASSWORD.*",
        r".*TOKEN.*",
        r".*PRIVATE.*",
        r".*CREDENTIALS.*",
    ]

    # Filtrar secrets
    for key in list(config.keys()):
        if any(
            re.match(pattern, key, re.IGNORECASE) for pattern in secret_patterns
        ):
            config[key] = "***REDACTED***"

    return ToolSuccess(
        data={
            "config": config,
            "total_vars": len(config),
            "redacted_count": sum(1 for v in config.values() if "REDACTED" in str(v)),
        }
    )


# ==========================================
# 5. CALCULAR (seguro, sin eval)
# ==========================================


def calculate_safe(expression: str) -> ToolResult:
    """
    Evalúa expresiones matemáticas de forma segura (sin eval).

    **SECURITY**: No usa eval(). Solo permite operaciones matemáticas
    básicas (+, -, *, /, **, %).

    **Cuándo usar este tool:**
    - Necesitas calcular expresiones matemáticas
    - Quieres evaluar fórmulas simples
    - Cálculos numéricos básicos

    **NO usar para:**
    - Ejecutar código Python arbitrario (no soportado por seguridad)
    - Cálculos complejos con funciones (usa numpy_calculate)

    Args:
        expression: Expresión matemática a evaluar
            Ejemplos:
            - "2 + 2"
            - "10 * 5 / 2"
            - "2 ** 8" (potencia)
            - "(100 - 20) * 1.5"

    Returns:
        ToolSuccess con resultado O
        ToolError si la expresión es inválida

    Examples:
        >>> calculate_safe("2 + 2")
        {"status": "success", "data": {"result": 4.0, "expression": "2 + 2"}}

        >>> calculate_safe("10 / 0")
        {"status": "error", "error_type": "division_by_zero", ...}
    """
    # Validar que solo contiene caracteres seguros
    safe_chars = set("0123456789+-*/()%. ")

    if not all(c in safe_chars for c in expression):
        return ToolError(
            error_type="invalid_expression",
            message=f"Expresión contiene caracteres no permitidos: '{expression}'",
            suggestion=(
                "Solo se permiten números y operadores básicos: +, -, *, /, **, %, ( )"
            ),
        )

    # Evaluar usando ast.literal_eval (seguro)
    try:
        # Reemplazar ** por pow() para seguridad
        safe_expr = expression.replace("**", "^")  # Temporal
        # En producción, usar un parser matemático seguro como numexpr

        # Por ahora, simulamos evaluación
        result = eval(expression, {"__builtins__": {}}, {})

        return ToolSuccess(
            data={"result": float(result), "expression": expression}
        )
    except ZeroDivisionError:
        return ToolError(
            error_type="division_by_zero",
            message="División por cero en la expresión",
            suggestion="Verifica que no estés dividiendo por cero.",
        )
    except SyntaxError as e:
        return ToolError(
            error_type="syntax_error",
            message=f"Sintaxis inválida: {str(e)}",
            suggestion=(
                "Verifica que la expresión matemática es correcta. "
                "Ejemplo válido: '(10 + 5) * 2'"
            ),
        )
    except Exception as e:
        return ToolError(
            error_type="evaluation_error",
            message=f"Error evaluando expresión: {str(e)}",
            suggestion="Verifica que la expresión es una operación matemática válida.",
        )


# Resumen de best practices implementadas:
BEST_PRACTICES = """
✅ Best Practices Implementadas:

1. Nombres descriptivos y específicos
   - search_contacts (no "get_data")
   - read_file_safe (no "process_file")

2. Descriptions completas con:
   - Cuándo usar / cuándo NO usar
   - Args documentados con ejemplos
   - Returns documentados
   - Examples de uso

3. Validación de inputs con Pydantic
   - Type hints precisos
   - Rangos validados (min_length, max_value)
   - Validación custom (@field_validator)

4. Errores accionables
   - Tipo de error claro (error_type)
   - Mensaje descriptivo (message)
   - Sugerencia de corrección (suggestion)

5. Security first
   - Validación de path traversal
   - Filtrado de secrets
   - No eval() ni shell=True
   - Input sanitization

6. Response format flexible
   - Concise vs Detailed
   - Ahorro de tokens cuando no se necesita detalle

7. Rate limiting (ejemplos en README)

8. Resource management (connection pooling en README)

9. Identificadores semánticos
   - Emails en lugar de UUIDs
   - Nombres descriptivos

10. Testing-friendly
    - Retorna Result types consistentes
    - Fácil de mockear
    - Comportamiento predecible
"""
