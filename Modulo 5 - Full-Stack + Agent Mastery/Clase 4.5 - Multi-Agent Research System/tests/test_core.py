"""
Tests para el módulo core del sistema multi-agente.
"""

import pytest
from multi_agent_system import (
    AgentResult,
    AgentRole,
    LeadAgent,
    MultiAgentResearchSystem,
    SubAgent,
    Task,
)


class TestMessageBus:
    """Tests para MessageBus."""

    def test_publish_message(self, message_bus):
        """Test publicar mensaje."""
        message_bus.publish("agent_1", "agent_2", "Hello", "data")

        messages = message_bus.get_messages("agent_2")
        assert len(messages) == 1
        assert messages[0]["sender"] == "agent_1"
        assert messages[0]["message"] == "Hello"

    def test_get_messages_by_type(self, message_bus):
        """Test filtrar mensajes por tipo."""
        message_bus.publish("agent_1", "agent_2", "Data message", "data")
        message_bus.publish("agent_1", "agent_2", "Control message", "control")

        data_msgs = message_bus.get_messages("agent_2", message_type="data")
        assert len(data_msgs) == 1
        assert data_msgs[0]["message"] == "Data message"

    def test_clear_messages(self, message_bus):
        """Test limpiar mensajes."""
        message_bus.publish("agent_1", "agent_2", "Test", "data")
        message_bus.clear()

        messages = message_bus.get_messages("agent_2")
        assert len(messages) == 0

    def test_export_trace(self, message_bus):
        """Test exportar trace."""
        message_bus.publish("agent_1", "agent_2", "Msg 1", "data")
        message_bus.publish("agent_2", "agent_3", "Msg 2", "data")

        trace = message_bus.export_trace()
        assert len(trace) == 2
        assert trace[0]["sender"] == "agent_1"
        assert trace[1]["sender"] == "agent_2"


class TestSharedMemory:
    """Tests para SharedMemory."""

    def test_store_and_retrieve(self, shared_memory):
        """Test guardar y recuperar valor."""
        shared_memory.store("key1", "value1")
        assert shared_memory.retrieve("key1") == "value1"

    def test_retrieve_with_default(self, shared_memory):
        """Test recuperar con valor por defecto."""
        assert shared_memory.retrieve("nonexistent", "default") == "default"

    def test_update(self, shared_memory):
        """Test actualizar valor con función."""
        shared_memory.store("counter", 0)
        shared_memory.update("counter", lambda x: x + 1)
        assert shared_memory.retrieve("counter") == 1

    def test_delete(self, shared_memory):
        """Test eliminar valor."""
        shared_memory.store("key1", "value1")
        shared_memory.delete("key1")
        assert shared_memory.retrieve("key1") is None

    def test_clear(self, shared_memory):
        """Test limpiar toda la memoria."""
        shared_memory.store("key1", "value1")
        shared_memory.store("key2", "value2")
        shared_memory.clear()

        assert len(shared_memory.keys()) == 0

    def test_keys(self, shared_memory):
        """Test listar claves."""
        shared_memory.store("key1", "value1")
        shared_memory.store("key2", "value2")

        keys = shared_memory.keys()
        assert len(keys) == 2
        assert "key1" in keys
        assert "key2" in keys


class TestLeadAgent:
    """Tests para LeadAgent."""

    @pytest.mark.asyncio
    async def test_create_research_plan(
        self, mock_llm_client, message_bus, shared_memory
    ):
        """Test crear plan de investigación."""
        lead = LeadAgent(mock_llm_client, message_bus, shared_memory)

        tasks = await lead.create_research_plan("Test query")

        assert len(tasks) > 0
        assert all(isinstance(task, Task) for task in tasks)
        assert shared_memory.retrieve("research_plan") is not None

    @pytest.mark.asyncio
    async def test_synthesize_results(
        self, mock_llm_client, message_bus, shared_memory
    ):
        """Test sintetizar resultados."""
        lead = LeadAgent(mock_llm_client, message_bus, shared_memory)

        results = [
            AgentResult(
                task_id=1,
                agent_role=AgentRole.RESEARCHER,
                findings="Finding 1",
                sources=["source1.com"],
                confidence=0.8,
            ),
            AgentResult(
                task_id=2,
                agent_role=AgentRole.ANALYZER,
                findings="Finding 2",
                sources=["source2.com"],
                confidence=0.9,
            ),
        ]

        synthesis = await lead.synthesize_results(results)

        assert isinstance(synthesis, str)
        assert len(synthesis) > 0


class TestSubAgent:
    """Tests para SubAgent."""

    @pytest.mark.asyncio
    async def test_research(
        self, sample_task, mock_llm_client, message_bus, shared_memory
    ):
        """Test ejecutar investigación."""
        agent = SubAgent(sample_task, mock_llm_client, message_bus, shared_memory)

        result = await agent.research()

        assert isinstance(result, AgentResult)
        assert result.task_id == sample_task.id
        assert result.agent_role == sample_task.agent_role
        assert len(result.sources) > 0

    @pytest.mark.asyncio
    async def test_agent_publishes_result(
        self, sample_task, mock_llm_client, message_bus, shared_memory
    ):
        """Test que el agente publica resultado al message bus."""
        agent = SubAgent(sample_task, mock_llm_client, message_bus, shared_memory)

        await agent.research()

        messages = message_bus.get_messages("lead_agent", message_type="result")
        assert len(messages) == 1


class TestMultiAgentResearchSystem:
    """Tests para el sistema completo."""

    @pytest.mark.asyncio
    async def test_research_flow(self, mock_llm_client):
        """Test flujo completo de investigación."""
        system = MultiAgentResearchSystem(mock_llm_client)

        synthesis = await system.research("Test query")

        assert isinstance(synthesis, str)
        assert len(synthesis) > 0

    @pytest.mark.asyncio
    async def test_export_trace(self, mock_llm_client):
        """Test exportar trace de ejecución."""
        system = MultiAgentResearchSystem(mock_llm_client)

        await system.research("Test query")
        trace = system.export_trace()

        assert "messages" in trace
        assert "memory" in trace
        assert len(trace["messages"]) > 0
