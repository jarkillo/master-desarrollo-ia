"""
Tests básicos para los ejemplos de la Clase 6.5

Estos tests verifican que los ejemplos tienen la estructura correcta
y pueden importarse sin errores.

NOTA: Tests completos con API calls requerirían ANTHROPIC_API_KEY
y se saltean si no está disponible.
"""

import os
import sys
from pathlib import Path

import pytest

# Importar desde ejemplos
ejemplos_dir = Path(__file__).parent.parent / "ejemplos"
sys.path.insert(0, str(ejemplos_dir))


class TestEjemplo01:
    """Tests para ejercicio 1: Agente simple."""

    def test_import_agente_simple(self):
        """Verifica que el módulo se puede importar."""
        from ejemplos import agente_simple as mod

        assert hasattr(mod, "SimpleAgent")

    def test_simple_agent_init(self):
        """Verifica que SimpleAgent se puede instanciar."""
        from ejemplos.agente_simple import SimpleAgent

        # Sin API key está OK para tests de estructura
        agent = SimpleAgent(api_key="test_key")
        assert agent is not None
        assert hasattr(agent, "run_bash_command")
        assert hasattr(agent, "answer_question")


class TestEjemplo02:
    """Tests para ejercicio 2: Control de flujo."""

    def test_import_control_flujo(self):
        """Verifica que el módulo se puede importar."""
        from ejemplos import control_flujo as mod

        assert hasattr(mod, "StatefulAgent")
        assert hasattr(mod, "TaskState")

    def test_task_state_enum(self):
        """Verifica que TaskState tiene todos los estados esperados."""
        from ejemplos.control_flujo import TaskState

        expected_states = {"PENDING", "IN_PROGRESS", "COMPLETED", "FAILED", "RETRYING"}
        actual_states = {state.name for state in TaskState}

        assert expected_states == actual_states

    def test_task_creation(self):
        """Verifica que Task se puede crear."""
        from ejemplos.control_flujo import Task, TaskState

        task = Task(id="test-1", description="Test task")
        assert task.id == "test-1"
        assert task.state == TaskState.PENDING
        assert task.attempts == 0

    def test_stateful_agent_init(self):
        """Verifica que StatefulAgent se puede instanciar."""
        from ejemplos.control_flujo import StatefulAgent

        agent = StatefulAgent(api_key="test_key")
        assert agent is not None
        assert hasattr(agent, "add_task")
        assert hasattr(agent, "execute_task_with_retry")


class TestEjemplo03:
    """Tests para ejercicio 3: Tools avanzadas."""

    def test_import_tools_avanzadas(self):
        """Verifica que el módulo se puede importar."""
        from ejemplos import tools_avanzadas as mod

        assert hasattr(mod, "BaseTool")
        assert hasattr(mod, "GitStatusTool")
        assert hasattr(mod, "RunTestsTool")

    def test_base_tool_structure(self):
        """Verifica que BaseTool tiene la estructura correcta."""
        from ejemplos.tools_avanzadas import BaseTool

        # Verificar que es clase abstracta
        with pytest.raises(TypeError):
            BaseTool("test", "description")

    def test_git_status_tool_init(self):
        """Verifica que GitStatusTool se puede instanciar."""
        from ejemplos.tools_avanzadas import GitStatusTool

        tool = GitStatusTool()
        assert tool.name == "git_status"
        assert hasattr(tool, "execute")
        assert hasattr(tool, "get_schema")

    def test_tool_result_structure(self):
        """Verifica estructura de ToolResult."""
        from ejemplos.tools_avanzadas import ToolResult

        result = ToolResult(success=True, output="test output")
        assert result.success is True
        assert result.output == "test output"
        assert result.error is None


class TestEjemplo04:
    """Tests para ejercicio 4: Subagentes."""

    def test_import_subagentes(self):
        """Verifica que el módulo se puede importar."""
        from ejemplos import subagentes as mod

        assert hasattr(mod, "BaseSubagent")
        assert hasattr(mod, "MasterAgent")

    def test_subagent_result_structure(self):
        """Verifica estructura de SubagentResult."""
        from ejemplos.subagentes import SubagentResult

        result = SubagentResult(
            agent_name="test",
            success=True,
            output="output",
            execution_time=1.5,
        )
        assert result.agent_name == "test"
        assert result.success is True
        assert result.execution_time == 1.5

    def test_search_agent_init(self):
        """Verifica que SearchAgent se puede instanciar."""
        from ejemplos.subagentes import SearchAgent

        agent = SearchAgent(api_key="test_key")
        assert agent.name == "SearchAgent"
        assert hasattr(agent, "execute")
        assert hasattr(agent, "_get_system_prompt")

    def test_master_agent_init(self):
        """Verifica que MasterAgent se puede instanciar."""
        from ejemplos.subagentes import MasterAgent

        agent = MasterAgent(api_key="test_key")
        assert hasattr(agent, "subagents")
        assert len(agent.subagents) > 0
        assert hasattr(agent, "analyze_project")


class TestProyectoFinal:
    """Tests para proyecto final: Agente autónomo."""

    def test_import_agente_autonomo(self):
        """Verifica que el módulo se puede importar."""
        proyecto_dir = Path(__file__).parent.parent / "proyecto_final"
        sys.path.insert(0, str(proyecto_dir))

        from proyecto_final import agente_dev_autonomo as mod

        assert hasattr(mod, "AutonomousDevelopmentAgent")
        assert hasattr(mod, "IssueType")

    def test_issue_type_enum(self):
        """Verifica que IssueType tiene los tipos esperados."""
        proyecto_dir = Path(__file__).parent.parent / "proyecto_final"
        sys.path.insert(0, str(proyecto_dir))

        from proyecto_final.agente_dev_autonomo import IssueType

        expected_types = {"TYPO", "MISSING_IMPORT", "SIMPLE_TEST", "DOCSTRING", "LINTING", "UNKNOWN"}
        actual_types = {itype.name for itype in IssueType}

        assert expected_types == actual_types

    def test_issue_creation(self):
        """Verifica que Issue se puede crear."""
        proyecto_dir = Path(__file__).parent.parent / "proyecto_final"
        sys.path.insert(0, str(proyecto_dir))

        from proyecto_final.agente_dev_autonomo import Issue, IssueType

        issue = Issue(
            id="1",
            title="Test issue",
            description="Test description",
            type=IssueType.TYPO,
        )
        assert issue.id == "1"
        assert issue.type == IssueType.TYPO

    def test_autonomous_agent_init(self):
        """Verifica que AutonomousDevelopmentAgent se puede instanciar."""
        proyecto_dir = Path(__file__).parent.parent / "proyecto_final"
        sys.path.insert(0, str(proyecto_dir))

        from proyecto_final.agente_dev_autonomo import AutonomousDevelopmentAgent

        agent = AutonomousDevelopmentAgent(repo_path=".", api_key="test_key")
        assert agent is not None
        assert hasattr(agent, "resolve_issue")
        assert hasattr(agent, "_classify_issue")
        assert hasattr(agent, "_gather_context")


# ================================
# TESTS OPCIONALES CON API
# ================================

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


@pytest.mark.skipif(not ANTHROPIC_API_KEY, reason="ANTHROPIC_API_KEY no configurada")
class TestConAPI:
    """
    Tests que requieren API key y hacen llamadas reales a Anthropic.

    Se saltean si ANTHROPIC_API_KEY no está configurada.
    """

    def test_simple_agent_bash_command(self):
        """Test real de SimpleAgent ejecutando comando bash."""
        from ejemplos.agente_simple import SimpleAgent

        agent = SimpleAgent()
        result = agent.run_bash_command("echo 'test'")

        assert "test" in result

    @pytest.mark.slow
    def test_simple_agent_answer_question(self):
        """Test real de SimpleAgent respondiendo pregunta."""
        from ejemplos.agente_simple import SimpleAgent

        agent = SimpleAgent()

        # Pregunta simple sobre el directorio actual
        answer = agent.answer_question(
            question="¿Cuántos archivos .py hay en este directorio?",
            repo_path=".",
            max_iterations=3,
        )

        assert isinstance(answer, str)
        assert len(answer) > 0

    @pytest.mark.slow
    def test_tool_execution(self):
        """Test real de ejecución de tool."""
        from ejemplos.tools_avanzadas import GitStatusTool

        tool = GitStatusTool()
        result = tool.execute()

        assert result is not None
        assert hasattr(result, "success")
        assert hasattr(result, "output")
