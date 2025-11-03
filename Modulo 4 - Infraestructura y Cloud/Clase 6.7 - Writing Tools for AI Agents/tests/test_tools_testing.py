"""
Tests unitarios para testing tool.
"""

from unittest.mock import Mock, patch

from api.tools.testing import run_tests


def test_run_tests_success():
    """Test cuando todos los tests pasan."""
    mock_result = Mock()
    mock_result.returncode = 0
    mock_result.stdout = "test_api.py::test_create ... PASSED\ntest_api.py::test_list ... PASSED\n\n5 passed in 1.23s"
    mock_result.stderr = ""

    with patch("api.tools.testing.subprocess.run", return_value=mock_result):
        result = run_tests(test_path="tests/")

        assert result.status == "success"
        assert "passed" in result.data["summary"].lower()


def test_run_tests_failure():
    """Test cuando hay tests que fallan."""
    mock_result = Mock()
    mock_result.returncode = 1
    mock_result.stdout = "test_api.py::test_create ... FAILED\n\n3 passed, 1 failed in 1.23s"
    mock_result.stderr = ""

    with patch("api.tools.testing.subprocess.run", return_value=mock_result):
        result = run_tests()

        assert result.status == "error"
        assert result.error_type == "tests_failed"
        assert "fallaron" in result.message.lower()


def test_run_tests_timeout():
    """Test cuando los tests exceden el timeout."""
    import subprocess

    with patch(
        "api.tools.testing.subprocess.run",
        side_effect=subprocess.TimeoutExpired("pytest", 60),
    ):
        result = run_tests()

        assert result.status == "error"
        assert result.error_type == "timeout"
        assert "60 segundos" in result.message


def test_run_tests_pytest_not_installed():
    """Test cuando pytest no está instalado."""
    with patch(
        "api.tools.testing.subprocess.run", side_effect=FileNotFoundError()
    ):
        result = run_tests()

        assert result.status == "error"
        assert result.error_type == "pytest_not_found"
        assert "pytest" in result.message.lower()
