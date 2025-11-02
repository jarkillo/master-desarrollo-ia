"""
Ejercicio 4: Subagentes y paralelización

Objetivo:
Crear un agente principal que coordina subagentes especializados,
demostrando paralelización y gestión de contexto compartimentado.

Conceptos:
- Arquitectura de subagentes
- Paralelización de tareas
- Context management compartimentado
- Agregación de resultados

Caso de uso:
Agente principal que analiza un proyecto completo delegando tareas
a subagentes especializados:
- SearchAgent: Busca en documentación y código
- AnalysisAgent: Analiza calidad y arquitectura
- TestAgent: Ejecuta y valida tests
"""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from anthropic import Anthropic


@dataclass
class SubagentResult:
    """Resultado de ejecución de un subagente."""

    agent_name: str
    success: bool
    output: str
    error: str | None = None
    execution_time: float = 0.0
    metadata: dict[str, Any] | None = None


class BaseSubagent:
    """
    Clase base para todos los subagentes.

    Los subagentes son contextos de ejecución aislados que:
    - Operan independientemente
    - Retornan solo información relevante (no todo el contexto)
    - Pueden ejecutarse en paralelo
    """

    def __init__(self, name: str, api_key: str | None = None):
        self.name = name
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-sonnet-20241022"

    def execute(self, task: str) -> SubagentResult:
        """
        Ejecuta la tarea asignada al subagente.

        Args:
            task: Tarea específica para este subagente

        Returns:
            SubagentResult con el resultado
        """
        start_time = datetime.now()

        try:
            # Llamar a Claude con contexto específico del subagente
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system=self._get_system_prompt(),
                messages=[{"role": "user", "content": task}],
            )

            execution_time = (datetime.now() - start_time).total_seconds()

            return SubagentResult(
                agent_name=self.name,
                success=True,
                output=response.content[0].text,
                execution_time=execution_time,
                metadata={"tokens_used": response.usage.input_tokens + response.usage.output_tokens},
            )

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return SubagentResult(
                agent_name=self.name,
                success=False,
                output="",
                error=str(e),
                execution_time=execution_time,
            )

    def _get_system_prompt(self) -> str:
        """
        System prompt específico del subagente.

        Override en subclases para especialización.
        """
        return "Eres un asistente útil."


class SearchAgent(BaseSubagent):
    """Subagente especializado en búsqueda de información."""

    def __init__(self, api_key: str | None = None):
        super().__init__("SearchAgent", api_key)

    def _get_system_prompt(self) -> str:
        return """Eres un agente de búsqueda especializado.

Tu trabajo:
- Buscar información relevante en código, docs, y archivos
- Proporcionar SOLO excerpts relevantes, no archivos completos
- Usar comandos bash eficientemente (grep, find, cat con head/tail)
- Ser preciso y conciso

Formato de respuesta:
1. Qué encontraste
2. Dónde lo encontraste (archivo:línea)
3. Contexto relevante (3-5 líneas alrededor)

NO devuelvas archivos completos. Solo información relevante."""


class AnalysisAgent(BaseSubagent):
    """Subagente especializado en análisis de código."""

    def __init__(self, api_key: str | None = None):
        super().__init__("AnalysisAgent", api_key)

    def _get_system_prompt(self) -> str:
        return """Eres un agente de análisis de código especializado.

Tu trabajo:
- Analizar calidad de código (SOLID, clean code, etc.)
- Detectar code smells y anti-patterns
- Sugerir mejoras arquitectónicas
- Evaluar test coverage conceptualmente

Formato de respuesta:
1. Resumen ejecutivo (2-3 líneas)
2. Aspectos positivos
3. Áreas de mejora (priorizado)
4. Recomendaciones específicas

Sé constructivo pero directo. Enfócate en lo más importante."""


class TestAgent(BaseSubagent):
    """Subagente especializado en testing."""

    def __init__(self, api_key: str | None = None):
        super().__init__("TestAgent", api_key)

    def _get_system_prompt(self) -> str:
        return """Eres un agente de testing especializado.

Tu trabajo:
- Validar existencia y calidad de tests
- Identificar gaps en test coverage
- Sugerir tests adicionales
- Evaluar estrategia de testing (unit, integration, e2e)

Formato de respuesta:
1. Estado actual de tests
2. Coverage (estimado conceptualmente)
3. Gaps identificados
4. Tests recomendados (priorizado)

Enfócate en calidad, no cantidad. Tests valiosos sobre tests innecesarios."""


class MasterAgent:
    """
    Agente principal que coordina subagentes especializados.

    Implementa:
    - Delegación de tareas a subagentes
    - Ejecución paralela (ThreadPoolExecutor)
    - Agregación de resultados
    - Síntesis final
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"

        # Inicializar subagentes
        self.subagents = [
            SearchAgent(self.api_key),
            AnalysisAgent(self.api_key),
            TestAgent(self.api_key),
        ]

    def analyze_project(self, project_path: str) -> dict[str, Any]:
        """
        Analiza un proyecto completo usando subagentes en paralelo.

        Args:
            project_path: Ruta al proyecto

        Returns:
            Análisis completo agregado
        """
        print("=" * 60)
        print("🚀 Análisis de proyecto con subagentes")
        print("=" * 60)

        # Definir tareas para cada subagente
        tasks = {
            "SearchAgent": f"""Analiza la estructura del proyecto en {project_path}.

Busca:
1. Archivos principales (api.py, main.py, etc.)
2. Tests existentes
3. Archivos de configuración importantes

Retorna SOLO un resumen con las ubicaciones clave.""",
            "AnalysisAgent": f"""Analiza la calidad del código en {project_path}.

Enfócate en:
1. Estructura general del proyecto
2. Patrones arquitectónicos usados
3. Principales code smells si los hay

Sé breve - máximo 10 líneas.""",
            "TestAgent": f"""Evalúa la estrategia de testing en {project_path}.

Verifica:
1. ¿Hay tests? ¿Dónde?
2. ¿Qué tipos de tests? (unit, integration)
3. ¿Hay gaps obvios?

Respuesta concisa - máximo 8 líneas.""",
        }

        # Ejecutar subagentes en paralelo
        print("\n⚡ Ejecutando subagentes en paralelo...\n")
        results = self._execute_parallel(tasks)

        # Mostrar resultados individuales
        for result in results:
            print(f"\n--- {result.agent_name} ---")
            print(f"⏱️  Tiempo: {result.execution_time:.2f}s")
            if result.success:
                print(f"✅ Output:\n{result.output}")
            else:
                print(f"❌ Error: {result.error}")

        # Sintetizar resultados
        print("\n" + "=" * 60)
        print("🧠 Sintetizando resultados...")
        print("=" * 60)

        synthesis = self._synthesize_results(results)

        return {
            "project_path": project_path,
            "timestamp": datetime.now().isoformat(),
            "subagent_results": [
                {
                    "agent": r.agent_name,
                    "success": r.success,
                    "execution_time": r.execution_time,
                    "output": r.output[:200] + "..." if len(r.output) > 200 else r.output,
                }
                for r in results
            ],
            "synthesis": synthesis,
            "total_execution_time": sum(r.execution_time for r in results),
        }

    def _execute_parallel(self, tasks: dict[str, str]) -> list[SubagentResult]:
        """
        Ejecuta subagentes en paralelo usando ThreadPoolExecutor.

        Args:
            tasks: {agent_name: task_description}

        Returns:
            Lista de resultados de todos los subagentes
        """
        results: list[SubagentResult] = []

        # Usar ThreadPoolExecutor para paralelización
        with ThreadPoolExecutor(max_workers=len(self.subagents)) as executor:
            # Crear futures
            future_to_agent = {}
            for agent in self.subagents:
                if agent.name in tasks:
                    future = executor.submit(agent.execute, tasks[agent.name])
                    future_to_agent[future] = agent.name

            # Recoger resultados a medida que se completan
            for future in as_completed(future_to_agent):
                agent_name = future_to_agent[future]
                print(f"✓ {agent_name} completado")
                results.append(future.result())

        return results

    def _synthesize_results(self, results: list[SubagentResult]) -> str:
        """
        Sintetiza los resultados de todos los subagentes en un análisis coherente.

        Usa Claude para agregar y sintetizar la información.
        """
        # Preparar contexto con todos los resultados
        context = "Resultados de análisis de proyecto por subagentes especializados:\n\n"

        for result in results:
            context += f"--- {result.agent_name} ---\n"
            if result.success:
                context += f"{result.output}\n\n"
            else:
                context += f"ERROR: {result.error}\n\n"

        # Pedir síntesis a Claude
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"""{context}

Sintetiza estos análisis en un reporte ejecutivo coherente.

Estructura:
1. Resumen general (2-3 líneas)
2. Hallazgos clave (bullets)
3. Recomendaciones prioritarias (máx 3)

Máximo 15 líneas total. Sé conciso y accionable.""",
                }
            ],
        )

        return response.content[0].text


def main() -> None:
    """Ejemplo de uso del agente maestro con subagentes."""
    print("=== Agente Maestro con Subagentes Especializados ===\n")

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: Configura ANTHROPIC_API_KEY")
        return

    # Crear agente maestro
    master = MasterAgent()

    # Analizar proyecto (directorio actual)
    project_path = input("\nRuta al proyecto a analizar (Enter para '.'): ").strip() or "."

    print(f"\n🔍 Analizando proyecto: {project_path}\n")

    # Ejecutar análisis
    result = master.analyze_project(project_path)

    # Mostrar síntesis final
    print("\n" + "=" * 60)
    print("📊 REPORTE FINAL")
    print("=" * 60)
    print(result["synthesis"])

    print(f"\n⏱️  Tiempo total de ejecución: {result['total_execution_time']:.2f}s")
    print(f"    (Ejecución paralela - sin paralelización: ~{sum(r['execution_time'] for r in result['subagent_results']):.2f}s)")


if __name__ == "__main__":
    main()


# ================================
# EJERCICIO PARA EL ESTUDIANTE
# ================================

"""
1. Ejecuta el agente maestro en diferentes proyectos
2. Mide el speedup de paralelización vs ejecución secuencial
3. Observa cómo cada subagente se especializa en su área

4. Modifica el código para:
   a) Añadir un nuevo subagente: SecurityAgent (analiza vulnerabilidades)
   b) Implementar timeout por subagente (10s máximo)
   c) Añadir retry logic si un subagente falla

5. DESAFÍO: Implementa estas mejoras:
   - Subagentes asíncronos usando asyncio en lugar de threads
   - Cache de resultados de subagentes (si el proyecto no cambió)
   - Priorización: subagentes críticos primero, otros después
   - Dashboard en terminal (rich library) mostrando progreso en vivo

6. Experimenta con paralelización:
   - ¿Cuántos subagentes puedes ejecutar en paralelo antes de throttling de API?
   - ¿Cómo afecta el max_tokens de cada subagente al rendimiento?
   - ¿Vale la pena la complejidad de subagentes vs un agente monolítico?

Preguntas de reflexión:
- ¿Cuándo es apropiado usar subagentes vs un agente único?
- ¿Qué trade-offs hay entre especialización y flexibilidad?
- ¿Cómo manejarías dependencias entre subagentes?
  (ej: AnalysisAgent necesita resultados de SearchAgent)
- ¿Cómo escalarías esto a 10+ subagentes?
"""
