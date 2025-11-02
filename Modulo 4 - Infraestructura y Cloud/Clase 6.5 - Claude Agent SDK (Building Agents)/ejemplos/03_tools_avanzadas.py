"""
Ejercicio 3: Tool calling avanzado

Objetivo:
Diseñar tools personalizadas profesionales con validación, idempotencia,
logging y mejores prácticas.

Conceptos:
- Tool design patterns
- Input validation
- Idempotencia (misma entrada → misma salida)
- Logging y debugging
- Error handling en tools

Caso de uso:
Agente que gestiona un proyecto de desarrollo con tools para:
- Git operations (commit, branch, status)
- Test execution (pytest)
- Code quality (ruff, mypy)
"""

import json
import logging
import os
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from anthropic import Anthropic

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("agent_tools.log"),
        logging.StreamHandler(),
    ],
)


@dataclass
class ToolResult:
    """Resultado estandarizado de ejecución de tools."""

    success: bool
    output: str
    error: str | None = None
    metadata: dict[str, Any] | None = None


class BaseTool(ABC):
    """
    Clase base para todas las tools.

    Implementa:
    - Validación de inputs
    - Logging automático
    - Error handling consistente
    - Metadata tracking
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.logger = logging.getLogger(f"Tool.{name}")
        self.execution_count = 0

    @abstractmethod
    def _validate_inputs(self, **kwargs: Any) -> None:
        """
        Valida inputs antes de ejecutar.

        Raises:
            ValueError: Si los inputs son inválidos
        """
        pass

    @abstractmethod
    def _execute(self, **kwargs: Any) -> ToolResult:
        """
        Lógica de ejecución de la tool.

        Returns:
            ToolResult con el resultado
        """
        pass

    def execute(self, **kwargs: Any) -> ToolResult:
        """
        Ejecuta la tool con validación y logging.

        Patrón template method:
        1. Validar inputs
        2. Log inicio
        3. Ejecutar
        4. Log resultado
        5. Retornar resultado
        """
        self.execution_count += 1
        self.logger.info(f"Ejecutando {self.name} (ejecución #{self.execution_count})")

        start_time = datetime.now()

        try:
            # Validar inputs
            self._validate_inputs(**kwargs)

            # Ejecutar
            result = self._execute(**kwargs)

            # Añadir metadata
            execution_time = (datetime.now() - start_time).total_seconds()
            if result.metadata is None:
                result.metadata = {}

            result.metadata.update(
                {
                    "tool_name": self.name,
                    "execution_count": self.execution_count,
                    "execution_time_seconds": execution_time,
                    "timestamp": datetime.now().isoformat(),
                }
            )

            # Log resultado
            self.logger.info(f"{self.name} {'completado' if result.success else 'falló'} en {execution_time:.2f}s")

            return result

        except Exception as e:
            self.logger.error(f"Error en {self.name}: {str(e)}", exc_info=True)
            return ToolResult(
                success=False,
                output="",
                error=str(e),
                metadata={
                    "tool_name": self.name,
                    "execution_count": self.execution_count,
                    "execution_time_seconds": (datetime.now() - start_time).total_seconds(),
                },
            )

    def get_schema(self) -> dict[str, Any]:
        """
        Retorna el schema de la tool en formato Anthropic.

        Override en subclases para definir inputs específicos.
        """
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        }


class GitStatusTool(BaseTool):
    """Tool para obtener git status."""

    def __init__(self):
        super().__init__(
            name="git_status",
            description="Obtiene el estado actual del repositorio Git (archivos modificados, branch actual, commits pendientes)",
        )

    def _validate_inputs(self, **kwargs: Any) -> None:
        # No hay inputs para validar
        pass

    def _execute(self, **kwargs: Any) -> ToolResult:
        """Ejecuta git status."""
        try:
            result = subprocess.run(
                ["git", "status", "--short"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == 0:
                # Obtener también el branch actual
                branch_result = subprocess.run(
                    ["git", "branch", "--show-current"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )

                output = f"Branch: {branch_result.stdout.strip()}\n\n{result.stdout}"
                return ToolResult(success=True, output=output)
            else:
                return ToolResult(success=False, output="", error=result.stderr)

        except subprocess.TimeoutExpired:
            return ToolResult(success=False, output="", error="Git command timed out")
        except FileNotFoundError:
            return ToolResult(success=False, output="", error="Git no está instalado")

    def get_schema(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": {},
            },
        }


class RunTestsTool(BaseTool):
    """Tool para ejecutar tests con pytest."""

    def __init__(self):
        super().__init__(
            name="run_tests",
            description="Ejecuta tests unitarios usando pytest. Puede ejecutar todos los tests o filtrar por ruta/patrón.",
        )

    def _validate_inputs(self, **kwargs: Any) -> None:
        path = kwargs.get("path")
        if path and not isinstance(path, str):
            raise ValueError("'path' debe ser un string")

    def _execute(self, **kwargs: Any) -> ToolResult:
        """Ejecuta pytest con opciones configurables."""
        path = kwargs.get("path", ".")
        verbose = kwargs.get("verbose", False)

        cmd = ["pytest", path]
        if verbose:
            cmd.append("-v")

        # Siempre añadir summary
        cmd.extend(["-q", "--tb=short"])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,  # 1 minuto máximo
            )

            return ToolResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr if result.returncode != 0 else None,
                metadata={"exit_code": result.returncode},
            )

        except subprocess.TimeoutExpired:
            return ToolResult(success=False, output="", error="Tests timeout después de 60s")
        except FileNotFoundError:
            return ToolResult(success=False, output="", error="pytest no está instalado")

    def get_schema(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Ruta a tests específicos (opcional). Por defecto ejecuta todos los tests.",
                    },
                    "verbose": {
                        "type": "boolean",
                        "description": "Si True, muestra output verboso de pytest",
                    },
                },
            },
        }


class CodeQualityTool(BaseTool):
    """Tool para verificar calidad de código con ruff."""

    def __init__(self):
        super().__init__(
            name="check_code_quality",
            description="Verifica la calidad del código Python usando ruff (linter moderno y rápido)",
        )

    def _validate_inputs(self, **kwargs: Any) -> None:
        path = kwargs.get("path", ".")
        if not isinstance(path, str):
            raise ValueError("'path' debe ser un string")

    def _execute(self, **kwargs: Any) -> ToolResult:
        """Ejecuta ruff check."""
        path = kwargs.get("path", ".")

        try:
            result = subprocess.run(
                ["ruff", "check", path],
                capture_output=True,
                text=True,
                timeout=30,
            )

            # ruff retorna 0 si no hay errores, 1 si hay errores
            return ToolResult(
                success=result.returncode == 0,
                output=result.stdout if result.stdout else "✅ No se encontraron problemas de calidad",
                error=None,  # Errores de linting van en output, no en error
                metadata={"issues_found": result.returncode != 0},
            )

        except subprocess.TimeoutExpired:
            return ToolResult(success=False, output="", error="Ruff timeout después de 30s")
        except FileNotFoundError:
            return ToolResult(success=False, output="", error="Ruff no está instalado")

    def get_schema(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Ruta al código a analizar (por defecto: directorio actual)",
                    }
                },
            },
        }


class FileSearchTool(BaseTool):
    """Tool idempotente para buscar archivos."""

    def __init__(self):
        super().__init__(
            name="search_files",
            description="Busca archivos en el proyecto por patrón de nombre (glob pattern)",
        )
        # Caché para hacer la tool idempotente
        self._cache: dict[str, ToolResult] = {}

    def _validate_inputs(self, **kwargs: Any) -> None:
        pattern = kwargs.get("pattern")
        if not pattern or not isinstance(pattern, str):
            raise ValueError("'pattern' es requerido y debe ser un string")

    def _execute(self, **kwargs: Any) -> ToolResult:
        """Busca archivos. Usa caché para idempotencia."""
        pattern = kwargs["pattern"]
        path = kwargs.get("path", ".")

        # Clave de caché
        cache_key = f"{path}:{pattern}"

        # Verificar caché
        if cache_key in self._cache:
            self.logger.info(f"Usando resultado cacheado para {cache_key}")
            cached = self._cache[cache_key]
            # Actualizar metadata para indicar que vino del caché
            if cached.metadata:
                cached.metadata["from_cache"] = True
            return cached

        # Ejecutar búsqueda
        try:
            import glob

            matches = glob.glob(f"{path}/**/{pattern}", recursive=True)

            result = ToolResult(
                success=True,
                output="\n".join(matches) if matches else "No se encontraron archivos",
                metadata={"matches_count": len(matches), "from_cache": False},
            )

            # Guardar en caché
            self._cache[cache_key] = result

            return result

        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))

    def get_schema(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Patrón glob para buscar archivos (ej: '*.py', 'test_*.py')",
                    },
                    "path": {
                        "type": "string",
                        "description": "Directorio base para buscar (por defecto: directorio actual)",
                    },
                },
                "required": ["pattern"],
            },
        }


class DevelopmentAgent:
    """Agente de desarrollo con tools avanzadas."""

    def __init__(self, api_key: str | None = None):
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-sonnet-20241022"

        # Registrar tools
        self.tools = [
            GitStatusTool(),
            RunTestsTool(),
            CodeQualityTool(),
            FileSearchTool(),
        ]

    def run_task(self, task: str, max_iterations: int = 10) -> str:
        """
        Ejecuta una tarea de desarrollo usando las tools disponibles.

        Args:
            task: Descripción de la tarea
            max_iterations: Máximo de iteraciones del loop

        Returns:
            Resultado final del agente
        """
        conversation = [{"role": "user", "content": task}]

        for iteration in range(max_iterations):
            print(f"\n--- Iteración {iteration + 1}/{max_iterations} ---")

            # Llamar a Claude con tools
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                tools=[tool.get_schema() for tool in self.tools],
                messages=conversation,
            )

            # Procesar respuesta
            if response.stop_reason == "end_turn":
                # Respuesta final
                return next(
                    (block.text for block in response.content if hasattr(block, "text")),
                    "No response",
                )

            elif response.stop_reason == "tool_use":
                # Ejecutar tools
                tool_results = []

                for block in response.content:
                    if block.type == "tool_use":
                        # Buscar tool correspondiente
                        tool = next((t for t in self.tools if t.name == block.name), None)

                        if not tool:
                            tool_results.append(
                                {
                                    "type": "tool_result",
                                    "tool_use_id": block.id,
                                    "content": f"Error: Tool {block.name} no encontrada",
                                }
                            )
                            continue

                        # Ejecutar tool
                        print(f"🔧 Ejecutando tool: {tool.name}")
                        print(f"   Inputs: {json.dumps(block.input, indent=2)}")

                        result = tool.execute(**block.input)

                        print(f"   {'✅' if result.success else '❌'} {result.output[:100]}...")

                        tool_results.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": result.output if result.success else result.error or "Error desconocido",
                            }
                        )

                # Añadir a conversación
                conversation.append({"role": "assistant", "content": response.content})
                conversation.append({"role": "user", "content": tool_results})

        return "Máximo de iteraciones alcanzado"


def main() -> None:
    """Ejemplo de uso del agente con tools avanzadas."""
    print("=== Agente de Desarrollo con Tools Avanzadas ===\n")

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: Configura ANTHROPIC_API_KEY")
        return

    agent = DevelopmentAgent()

    # Tareas de ejemplo
    tasks = [
        "Analiza el estado del repositorio Git y dime qué archivos están modificados",
        "Ejecuta los tests del proyecto y reporta si hay algún fallo",
        "Verifica la calidad del código en el proyecto",
        "Busca todos los archivos de tests (test_*.py) en el proyecto",
    ]

    print("Tareas disponibles:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")

    choice = input(f"\nElige una tarea (1-{len(tasks)}): ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(tasks):
        task = tasks[int(choice) - 1]
    else:
        print("Opción inválida")
        return

    print(f"\n🤖 Ejecutando: {task}\n")
    result = agent.run_task(task)

    print("\n" + "=" * 60)
    print("📝 Resultado:")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()


# ================================
# EJERCICIO PARA EL ESTUDIANTE
# ================================

"""
1. Ejecuta el agente con cada una de las 4 tareas de ejemplo
2. Analiza los logs en agent_tools.log - ¿qué información se registra?
3. Observa el caché de FileSearchTool - ¿cuándo se usa?

4. Modifica el código para:
   a) Añadir una nueva tool: CreateBranchTool (crea una rama git)
   b) Implementar rate limiting en las tools (máx 5 ejecuciones/minuto)
   c) Añadir métricas: tiempo promedio de ejecución por tool

5. DESAFÍO: Crea estas tools adicionales:
   - CommitChangesTool: Hace commit de cambios con mensaje validado
   - GenerateChangelogTool: Genera CHANGELOG.md desde commits
   - DeployTool: Simula un deploy (con checks de tests, linting, etc.)

Preguntas de reflexión:
- ¿Por qué es importante la idempotencia en tools?
- ¿Qué otras validaciones podrías añadir a las tools existentes?
- ¿Cómo diseñarías tools para operaciones destructivas (delete, deploy)?
- ¿Qué métricas adicionales serían útiles para debugging?
"""
