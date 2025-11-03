"""
Tools para búsqueda de código en repositorios.

Implementa search_codebase siguiendo best practices de Anthropic.
"""

import subprocess
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class SearchCodebaseInput(BaseModel):
    """Schema de input para search_codebase tool."""

    query: str = Field(
        min_length=1,
        max_length=500,
        description="Texto o regex a buscar en código",
    )

    file_pattern: str = Field(
        default="*.py",
        description="Patrón glob para filtrar archivos (e.g., '*.py', 'api/**/*.py')",
    )

    context_lines: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Líneas de contexto antes/después del match",
    )

    max_results: int = Field(
        default=50,
        ge=1,
        le=200,
        description="Máximo de resultados a retornar",
    )

    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        """Valida que el query es seguro."""
        # Validar que no contiene caracteres peligrosos para shell
        dangerous_chars = [";", "|", "&", "$", "`"]
        if any(char in v for char in dangerous_chars):
            raise ValueError(
                f"Query contiene caracteres no permitidos. "
                f"Evita: {', '.join(dangerous_chars)}"
            )
        return v.strip()


class ToolSuccess(BaseModel):
    """Respuesta exitosa."""

    status: Literal["success"] = "success"
    data: dict


class ToolError(BaseModel):
    """Respuesta de error."""

    status: Literal["error"] = "error"
    error_type: str
    message: str
    suggestion: str


ToolResult = ToolSuccess | ToolError


def search_codebase(
    query: str,
    file_pattern: str = "*.py",
    context_lines: int = 3,
    max_results: int = 50,
) -> ToolResult:
    """
    Busca código en el repositorio usando grep semántico.

    **Cuándo usar este tool:**
    - Necesitas encontrar dónde se define una función/clase
    - Quieres ver ejemplos de uso de una API
    - Buscas referencias a una variable/constante específica

    **NO usar para:**
    - Leer archivos completos (usa `read_file` en su lugar)
    - Listar todos los archivos (usa `list_files`)

    Args:
        query: Texto o regex a buscar
            Ejemplos:
            - "def calculate_total" (busca definición de función)
            - "import requests" (busca imports)
            - "class.*Task" (regex para clases que terminan en Task)

        file_pattern: Patrón glob para filtrar archivos
            Ejemplos:
            - "*.py" (solo Python)
            - "tests/**/*.py" (solo tests)
            - "api/endpoints/**" (solo en api/endpoints/)

        context_lines: Líneas de contexto antes/después del match
            Rango válido: 0-10
            Default: 3 (suficiente para entender contexto)

        max_results: Máximo de resultados a retornar (límite: 200)

    Returns:
        ToolSuccess con lista de matches O
        ToolError con mensaje accionable

    **Relaciones con otros tools:**
    - Usa `read_file` después de encontrar el archivo correcto
    - Usa `get_function_definition` para ver función completa

    **Formato especializado:**
    Este tool soporta regex de Python. Escapa caracteres especiales:
    - Punto literal: "\\." no "."
    - Paréntesis literal: "\\(" no "("

    Examples:
        Buscar definición de función:
        >>> search_codebase(query="def process_payment", file_pattern="api/**/*.py")

        Buscar imports de biblioteca específica:
        >>> search_codebase(query="from fastapi import", context_lines=0)

        Buscar clases que heredan de BaseModel:
        >>> search_codebase(query="class.*\\(BaseModel\\)", file_pattern="models/*.py")
    """
    # Validar input usando Pydantic
    try:
        validated = SearchCodebaseInput(
            query=query,
            file_pattern=file_pattern,
            context_lines=context_lines,
            max_results=max_results,
        )
    except Exception as e:
        return ToolError(
            error_type="validation_error",
            message=str(e),
            suggestion="Verifica que los parámetros cumplen los requisitos del schema.",
        )

    # Obtener project root
    project_root = Path(__file__).parent.parent.parent.resolve()

    # Construir comando rg (ripgrep) de forma segura
    cmd = [
        "rg",  # ripgrep (más rápido que grep)
        validated.query,
        str(project_root),
        "--glob",
        validated.file_pattern,
        "--context",
        str(validated.context_lines),
        "--line-number",
        "--no-heading",
        "--max-count",
        str(validated.max_results),
        "--color",
        "never",
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,  # Timeout de 10 segundos
        )

        # rg retorna exit code 1 si no encuentra matches (no es error)
        if result.returncode not in [0, 1]:
            return ToolError(
                error_type="search_failed",
                message=f"Búsqueda falló: {result.stderr}",
                suggestion=(
                    "Verifica que ripgrep (rg) está instalado. "
                    "Instala con: pip install ripgrep-cli"
                ),
            )

        # Parsear resultados
        matches = []
        if result.stdout:
            lines = result.stdout.splitlines()
            current_match = None

            for line in lines:
                # Formato: path/to/file.py:123:contenido
                if ":" in line:
                    parts = line.split(":", 2)
                    if len(parts) >= 3:
                        file_path, line_num, content = parts
                        matches.append(
                            {
                                "file": file_path,
                                "line_number": int(line_num),
                                "content": content.strip(),
                            }
                        )

        return ToolSuccess(
            data={
                "matches": matches[: validated.max_results],
                "count": len(matches),
                "query": validated.query,
                "file_pattern": validated.file_pattern,
            }
        )

    except subprocess.TimeoutExpired:
        return ToolError(
            error_type="timeout",
            message="Búsqueda excedió el timeout de 10 segundos",
            suggestion=(
                "La búsqueda es muy amplia. "
                "Intenta con: "
                "1. Pattern más específico en file_pattern, "
                "2. Query más restrictivo, "
                "3. Reducir max_results"
            ),
        )
    except FileNotFoundError:
        return ToolError(
            error_type="tool_not_found",
            message="ripgrep (rg) no está instalado",
            suggestion=(
                "Instala ripgrep para usar este tool: "
                "pip install ripgrep-cli (o brew install ripgrep en Mac)"
            ),
        )
    except Exception as e:
        return ToolError(
            error_type="unexpected_error",
            message=f"Error inesperado: {str(e)}",
            suggestion="Verifica los logs del sistema para más detalles.",
        )
