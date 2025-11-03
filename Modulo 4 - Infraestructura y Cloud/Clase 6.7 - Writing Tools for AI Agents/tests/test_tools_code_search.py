"""
Tests unitarios para code_search tool.
"""

from unittest.mock import Mock, patch

import pytest
from api.tools.code_search import SearchCodebaseInput, search_codebase


def test_search_codebase_input_validation():
    """Test que valida input schema con Pydantic."""
    # Input válido
    valid_input = SearchCodebaseInput(
        query="def test_function",
        file_pattern="*.py",
        context_lines=3,
        max_results=50,
    )
    assert valid_input.query == "def test_function"
    assert valid_input.context_lines == 3

    # Query vacío (inválido)
    with pytest.raises(ValueError):
        SearchCodebaseInput(query="")

    # Context lines fuera de rango (inválido)
    with pytest.raises(ValueError):
        SearchCodebaseInput(query="test", context_lines=20)

    # Max results fuera de rango (inválido)
    with pytest.raises(ValueError):
        SearchCodebaseInput(query="test", max_results=500)


def test_search_codebase_dangerous_chars():
    """Test que rechaza queries con caracteres peligrosos."""
    dangerous_queries = [
        "test; rm -rf /",
        "test | cat /etc/passwd",
        "test && malicious_command",
        "test $HOME",
        "test `whoami`",
    ]

    for query in dangerous_queries:
        with pytest.raises(ValueError, match="caracteres no permitidos"):
            SearchCodebaseInput(query=query)


def test_search_codebase_success():
    """Test happy path con resultados encontrados."""
    mock_result = Mock()
    mock_result.returncode = 0
    mock_result.stdout = "api/tasks.py:42:def process_task():\napi/tasks.py:43:    pass\n"
    mock_result.stderr = ""

    with patch("api.tools.code_search.subprocess.run", return_value=mock_result):
        result = search_codebase(query="def process_task", file_pattern="*.py")

        assert result.status == "success"
        assert "matches" in result.data
        assert len(result.data["matches"]) > 0
        assert result.data["matches"][0]["file"] == "api/tasks.py"
        assert result.data["matches"][0]["line_number"] == 42


def test_search_codebase_no_matches():
    """Test cuando no hay matches (no es error)."""
    mock_result = Mock()
    mock_result.returncode = 1  # rg retorna 1 cuando no hay matches
    mock_result.stdout = ""
    mock_result.stderr = ""

    with patch("api.tools.code_search.subprocess.run", return_value=mock_result):
        result = search_codebase(query="nonexistent_function")

        assert result.status == "success"
        assert result.data["count"] == 0
        assert len(result.data["matches"]) == 0


def test_search_codebase_timeout():
    """Test cuando la búsqueda excede el timeout."""
    import subprocess

    with patch(
        "api.tools.code_search.subprocess.run",
        side_effect=subprocess.TimeoutExpired("rg", 10),
    ):
        result = search_codebase(query=".*")

        assert result.status == "error"
        assert result.error_type == "timeout"
        assert "timeout" in result.message.lower()
        assert "específico" in result.suggestion.lower()


def test_search_codebase_tool_not_found():
    """Test cuando ripgrep no está instalado."""
    with patch(
        "api.tools.code_search.subprocess.run", side_effect=FileNotFoundError()
    ):
        result = search_codebase(query="test")

        assert result.status == "error"
        assert result.error_type == "tool_not_found"
        assert "ripgrep" in result.message.lower()
        assert "instala" in result.suggestion.lower()
