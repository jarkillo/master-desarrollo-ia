"""
Configuración de pytest para tests del sistema multi-agente.
"""

import sys
from pathlib import Path

# Agregar parent directory al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from multi_agent_system import (
    AgentRole,
    Task,
    MessageBus,
    SharedMemory,
    PersistentMemory,
)


@pytest.fixture
def message_bus():
    """Fixture para MessageBus."""
    return MessageBus()


@pytest.fixture
def shared_memory():
    """Fixture para SharedMemory."""
    return SharedMemory()


@pytest.fixture
def persistent_memory(tmp_path):
    """Fixture para PersistentMemory con directorio temporal."""
    return PersistentMemory(storage_dir=str(tmp_path / "memory"))


@pytest.fixture
def sample_task():
    """Fixture para tarea de ejemplo."""
    return Task(
        id=1,
        description="Investigar impacto de IA en manufactura automotriz",
        agent_role=AgentRole.RESEARCHER,
        tools=["web_search", "academic_search"],
        max_searches=10,
        success_criteria="Identificar 5+ casos de uso con datos",
        output_format="Lista estructurada con ejemplos específicos",
    )


@pytest.fixture
def mock_llm_client():
    """Fixture para cliente LLM mock."""

    class MockLLMClient:
        async def complete(self, prompt: str) -> str:
            return "Mock LLM response"

    return MockLLMClient()
