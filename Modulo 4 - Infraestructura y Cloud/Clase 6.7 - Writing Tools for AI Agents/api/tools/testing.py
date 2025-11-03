"""Tools para ejecutar tests."""

import subprocess
from typing import Literal

from pydantic import BaseModel


class ToolSuccess(BaseModel):
    status: Literal["success"] = "success"
    data: dict


class ToolError(BaseModel):
    status: Literal["error"] = "error"
    error_type: str
    message: str
    suggestion: str


ToolResult = ToolSuccess | ToolError


def run_tests(test_path: str = "tests/", verbose: bool = False) -> ToolResult:
    """
    Ejecuta suite de tests con pytest.

    **Cuándo usar:**
    - Después de modificar código para verificar que funciona
    - Antes de hacer commit
    - Para verificar que un bugfix funciona

    Args:
        test_path: Path a test específico o directorio de tests
            Ejemplos:
            - "tests/" (todos los tests)
            - "tests/test_api.py" (archivo específico)
            - "tests/test_api.py::test_create_task" (test específico)

        verbose: Mostrar output verbose de pytest

    Returns:
        ToolSuccess con resultados de tests O ToolError
    """
    # Construir comando pytest
    cmd = ["pytest", test_path, "-v" if verbose else "-q", "--tb=short"]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60  # 1 minuto timeout
        )

        # Parsear output
        output_lines = result.stdout.splitlines()

        # Buscar línea de resumen (e.g., "5 passed, 2 failed in 1.23s")
        summary_line = next(
            (line for line in reversed(output_lines) if "passed" in line or "failed" in line),
            None,
        )

        # pytest retorna exit code != 0 si hay fallos
        if result.returncode != 0:
            return ToolError(
                error_type="tests_failed",
                message="Tests fallaron. Ver output para detalles.",
                suggestion=(
                    f"Revisa los tests que fallaron y corrige el código. "
                    f"Summary: {summary_line if summary_line else 'N/A'}"
                ),
            )

        return ToolSuccess(
            data={
                "test_path": test_path,
                "summary": summary_line or "Tests passed",
                "output": result.stdout if verbose else summary_line,
                "exit_code": result.returncode,
            }
        )

    except subprocess.TimeoutExpired:
        return ToolError(
            error_type="timeout",
            message="Tests excedieron timeout de 60 segundos",
            suggestion=(
                "Los tests tardan mucho. "
                "Considera ejecutar tests específicos en lugar de toda la suite."
            ),
        )
    except FileNotFoundError:
        return ToolError(
            error_type="pytest_not_found",
            message="pytest no está instalado",
            suggestion="Instala pytest con: pip install pytest",
        )
    except Exception as e:
        return ToolError(
            error_type="unexpected_error",
            message=f"Error inesperado: {str(e)}",
            suggestion="Revisa los logs para más detalles.",
        )
