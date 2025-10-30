"""
Tool para ejecutar tests y analizar resultados.
"""

import os
import subprocess
from pathlib import Path
from typing import Optional

from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class TestRunnerInput(BaseModel):
    """Schema de input para test runner."""

    test_path: str = Field(
        default="",
        description="Ruta al archivo/directorio de tests. Vacío = todos los tests"
    )
    verbose: bool = Field(
        default=True,
        description="Mostrar output detallado de pytest"
    )
    coverage: bool = Field(
        default=False,
        description="Calcular cobertura de código"
    )


class TestRunnerTool(BaseTool):
    """
    Tool para ejecutar tests con pytest.

    Características:
    - Ejecuta tests individuales o suites completas
    - Soporte para coverage reporting
    - Timeout de seguridad
    - Analiza resultados (passed/failed/errors)
    """

    name: str = "run_tests"
    description: str = """
    Ejecuta tests con pytest y analiza los resultados.

    Útil para:
    - Verificar que el código funciona correctamente
    - Ejecutar tests después de cambios
    - Validar cobertura de código
    - Identificar tests fallidos

    Input:
    - test_path: Ruta a tests (vacío = todos)
    - verbose: Mostrar output detallado (default: true)
    - coverage: Calcular cobertura (default: false)

    Ejemplo: run_tests(test_path="tests/test_api.py", coverage=true)

    Output: Resumen de tests (passed/failed) + errores si los hay
    """
    args_schema: type[BaseModel] = TestRunnerInput

    def _run(
        self,
        test_path: str = "",
        verbose: bool = True,
        coverage: bool = False
    ) -> str:
        """Ejecuta los tests."""
        try:
            # Comando base
            test_cmd = os.getenv("TEST_COMMAND", "pytest")
            test_dir = os.getenv("TEST_DIR", "tests")

            # Construir comando
            cmd = [test_cmd]

            # Path a tests
            if test_path:
                cmd.append(test_path)
            else:
                cmd.append(test_dir)

            # Argumentos
            if verbose:
                cmd.extend(["--verbose", "--color=yes"])
            else:
                cmd.append("--quiet")

            # Coverage
            if coverage:
                cmd.extend([
                    "--cov=api",
                    "--cov-report=term-missing",
                    "--cov-fail-under=80"
                ])

            # Argumentos adicionales del env
            test_args = os.getenv("TEST_ARGS", "")
            if test_args:
                cmd.extend(test_args.split())

            # Ejecutar
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=int(os.getenv("TOOL_TIMEOUT", "30"))
            )

            # Analizar output
            output = result.stdout + result.stderr

            # Determinar estado
            if result.returncode == 0:
                status = "✅ Todos los tests pasaron"
            elif result.returncode == 1:
                status = "❌ Algunos tests fallaron"
            elif result.returncode == 5:
                status = "⚠️  No se encontraron tests"
            else:
                status = f"❌ Error al ejecutar tests (código {result.returncode})"

            # Extraer estadísticas
            stats = self._extract_stats(output)

            return f"""
{status}

📊 Estadísticas:
{stats}

📝 Output completo:
{output}
"""

        except subprocess.TimeoutExpired:
            return "❌ Error: Tests tardaron demasiado (timeout). Considera ejecutar tests específicos."

        except FileNotFoundError:
            return f"❌ Error: Comando '{test_cmd}' no encontrado. Instala pytest: pip install pytest"

        except Exception as e:
            return f"❌ Error al ejecutar tests: {str(e)}"

    def _extract_stats(self, output: str) -> str:
        """Extrae estadísticas del output de pytest."""
        stats = []

        # Buscar línea de resumen (e.g., "5 passed, 2 failed in 1.23s")
        for line in output.split("\n"):
            if "passed" in line or "failed" in line or "error" in line:
                if " in " in line:  # Línea de resumen
                    stats.append(f"  {line.strip()}")

        if not stats:
            return "  (No se pudieron extraer estadísticas)"

        return "\n".join(stats)

    async def _arun(self, *args, **kwargs) -> str:
        """Versión async."""
        return self._run(*args, **kwargs)
