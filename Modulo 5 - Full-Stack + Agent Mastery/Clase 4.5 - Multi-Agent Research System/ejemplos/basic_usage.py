"""
Ejemplo básico de uso del sistema multi-agente.

Este script demuestra cómo usar el sistema para investigación simple.
"""

import asyncio
import sys
from pathlib import Path

# Agregar parent directory al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from multi_agent_system import MultiAgentResearchSystem, PersistentMemory, AgentLogger


class MockLLMClient:
    """Cliente LLM mock para demostración (sin API real)."""

    async def complete(self, prompt: str) -> str:
        """Simula completion del LLM."""
        return "Mock response from LLM"


async def main():
    """Ejemplo de investigación multi-agente."""

    # Crear cliente LLM (en producción usarías Anthropic client real)
    llm_client = MockLLMClient()

    # Crear sistema multi-agente
    print("=" * 60)
    print("SISTEMA MULTI-AGENTE DE INVESTIGACIÓN")
    print("=" * 60)
    print()

    system = MultiAgentResearchSystem(llm_client)

    # Query de ejemplo
    query = "¿Cómo está impactando la inteligencia artificial en la industria automotriz?"

    # Ejecutar investigación
    synthesis = await system.research(query)

    # Mostrar resultados
    print("=" * 60)
    print("RESULTADOS")
    print("=" * 60)
    print()
    print(synthesis)
    print()

    # Exportar trace para debugging
    print("=" * 60)
    print("TRACE DE EJECUCIÓN")
    print("=" * 60)
    print()

    trace = system.export_trace()

    print(f"Mensajes intercambiados: {len(trace['messages'])}")
    print(f"Datos en memoria: {len(trace['memory'])}")
    print()

    print("Detalle de mensajes:")
    for i, msg in enumerate(trace["messages"], 1):
        print(f"  {i}. {msg['sender']} → {msg['receiver']}: {msg['message_type']}")

    print()


async def example_with_persistent_memory():
    """Ejemplo con memoria persistente y checkpoints."""

    print("=" * 60)
    print("EJEMPLO CON MEMORIA PERSISTENTE")
    print("=" * 60)
    print()

    # Crear memoria persistente
    memory = PersistentMemory(storage_dir="./memory_example")

    # Guardar algunos datos
    memory.store("research_topic", "AI en automotive")
    memory.store("num_agents", 2)
    memory.store("max_depth", 3)

    print("✅ Datos guardados en memoria persistente")
    print()

    # Crear checkpoint
    memory.checkpoint("before_research")
    print()

    # Simular cambio de estado
    memory.store("status", "research_in_progress")
    memory.store("current_agent", "researcher_1")

    print("✅ Estado actualizado")
    print()

    # Listar checkpoints
    checkpoints = memory.list_checkpoints()
    print(f"Checkpoints disponibles: {len(checkpoints)}")
    for cp in checkpoints:
        print(f"  - {cp['name']} ({cp['timestamp']})")

    print()

    # Restaurar checkpoint
    print("Restaurando checkpoint anterior...")
    memory.restore_checkpoint("before_research")
    print()

    # Verificar que el estado se restauró
    print(f"Status después de restore: {memory.retrieve('status', 'not found')}")
    print(f"(Debería ser 'not found' porque el checkpoint es anterior)")
    print()


async def example_with_logging():
    """Ejemplo de logging estructurado."""

    print("=" * 60)
    print("EJEMPLO DE LOGGING")
    print("=" * 60)
    print()

    # Crear logger para un agente
    logger = AgentLogger("researcher_1", log_dir="./logs_example")

    # Registrar decisión
    logger.log_decision(
        "Starting web search for automotive AI",
        {"query": "AI automotive industry 2024", "max_results": 10},
    )

    # Registrar tool call
    logger.log_tool_call(
        "web_search",
        {"query": "Tesla AI technology", "filters": {"year": 2024}},
        {"results_count": 15, "sources": ["news", "academic"]},
    )

    # Registrar métrica
    logger.log_metric("search_latency", 1.23, "seconds")

    # Registrar inicio de tarea
    logger.log_task_start(1, "Research AI impact on automotive manufacturing")

    # Simular trabajo...
    await asyncio.sleep(0.1)

    # Registrar finalización
    logger.log_task_complete(task_id=1, duration_seconds=5.67, confidence=0.85)

    print("✅ Eventos registrados en logs_example/researcher_1.log")
    print()
    print("Para ver los logs:")
    print("  cat logs_example/researcher_1.log | python -m json.tool")
    print()


if __name__ == "__main__":
    # Ejecutar ejemplo básico
    asyncio.run(main())

    # Ejecutar ejemplo con memoria persistente
    asyncio.run(example_with_persistent_memory())

    # Ejecutar ejemplo con logging
    asyncio.run(example_with_logging())

    print("=" * 60)
    print("EJEMPLOS COMPLETADOS")
    print("=" * 60)
