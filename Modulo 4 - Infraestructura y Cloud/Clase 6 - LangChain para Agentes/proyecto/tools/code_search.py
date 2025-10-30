"""
Tool para búsqueda de código en el repositorio.
"""

import os
import subprocess
from pathlib import Path
from typing import Optional

from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class SearchCodeInput(BaseModel):
    """Schema de input para búsqueda de código."""

    query: str = Field(
        description="Texto o regex a buscar en el código"
    )
    file_pattern: str = Field(
        default="*.py",
        description="Patrón glob para filtrar archivos (e.g., '*.py', 'api/**/*.py')"
    )
    max_results: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Máximo de resultados a retornar (1-100)"
    )


class SearchCodeTool(BaseTool):
    """
    Tool para buscar código en el repositorio usando grep.

    Características:
    - Búsqueda recursiva en el directorio actual
    - Soporte para patrones glob
    - Limita resultados para no saturar el context window
    - Timeout de seguridad
    """

    name: str = "search_codebase"
    description: str = """
    Busca código en el repositorio usando grep.

    Útil para:
    - Encontrar definiciones de funciones/clases (e.g., "def calculate_total")
    - Buscar imports (e.g., "from fastapi import")
    - Encontrar referencias a variables/constantes
    - Localizar patrones de código

    Input:
    - query: Texto a buscar (soporta regex básico)
    - file_pattern: Filtrar por archivos (default: *.py)
    - max_results: Máximo de resultados (default: 20)

    Ejemplo: search_codebase(query="class.*BaseModel", file_pattern="api/**/*.py")

    Output: Lista de coincidencias con archivo y número de línea
    """
    args_schema: type[BaseModel] = SearchCodeInput

    def _run(
        self,
        query: str,
        file_pattern: str = "*.py",
        max_results: int = 20
    ) -> str:
        """Ejecuta la búsqueda de código."""
        try:
            # Obtener PROJECT_ROOT del env o usar directorio actual
            project_root = os.getenv("PROJECT_ROOT", ".")
            project_path = Path(project_root).resolve()

            # Ejecutar grep
            result = subprocess.run(
                [
                    "grep",
                    "-rn",  # Recursivo + números de línea
                    "--include", file_pattern,
                    query,
                    str(project_path)
                ],
                capture_output=True,
                text=True,
                timeout=int(os.getenv("TOOL_TIMEOUT", "30"))
            )

            if result.returncode != 0:
                return f"❌ No se encontró '{query}' en archivos {file_pattern}"

            # Procesar resultados
            lines = result.stdout.strip().split("\n")

            # Limitar resultados
            if len(lines) > max_results:
                truncated = lines[:max_results]
                output = "\n".join(truncated)
                return f"""
✅ Encontradas {len(lines)} coincidencias (mostrando primeras {max_results}):

{output}

... ({len(lines) - max_results} resultados más omitidos)

💡 Refina la búsqueda para ver resultados específicos.
"""

            output = "\n".join(lines)
            return f"""
✅ Encontradas {len(lines)} coincidencias:

{output}
"""

        except subprocess.TimeoutExpired:
            return "❌ Error: Búsqueda tardó demasiado (timeout). Intenta con un patrón más específico."

        except FileNotFoundError:
            return "❌ Error: Comando 'grep' no encontrado. Asegúrate de que está instalado."

        except Exception as e:
            return f"❌ Error al buscar: {str(e)}"

    async def _arun(self, *args, **kwargs) -> str:
        """Versión async (no implementada, usa la sync)."""
        return self._run(*args, **kwargs)
