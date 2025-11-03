"""
Suite completa de tools para agente de desarrollo.

Este módulo contiene tools profesionales que un agente IA
puede usar para asistir en tareas de desarrollo de software.
"""

from .code_search import search_codebase
from .file_ops import edit_file, read_file
from .git_ops import create_git_branch, git_commit
from .quality import analyze_code_quality
from .testing import run_tests

__all__ = [
    "search_codebase",
    "read_file",
    "edit_file",
    "create_git_branch",
    "git_commit",
    "run_tests",
    "analyze_code_quality",
]


def get_all_tools_schemas() -> list[dict]:
    """
    Retorna schemas de todos los tools para registrar con Claude API.

    Returns:
        Lista de tool schemas en formato Anthropic API
    """
    return [
        {
            "name": "search_codebase",
            "description": search_codebase.__doc__,
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Texto o regex a buscar",
                    },
                    "file_pattern": {
                        "type": "string",
                        "description": "Patrón glob para filtrar archivos (e.g., '*.py')",
                        "default": "*.py",
                    },
                    "context_lines": {
                        "type": "integer",
                        "description": "Líneas de contexto antes/después del match (0-10)",
                        "default": 3,
                    },
                },
                "required": ["query"],
            },
        },
        {
            "name": "read_file",
            "description": read_file.__doc__,
            "input_schema": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path al archivo a leer",
                    }
                },
                "required": ["file_path"],
            },
        },
        {
            "name": "run_tests",
            "description": run_tests.__doc__,
            "input_schema": {
                "type": "object",
                "properties": {
                    "test_path": {
                        "type": "string",
                        "description": "Path a test específico o directorio de tests",
                        "default": "tests/",
                    },
                    "verbose": {
                        "type": "boolean",
                        "description": "Mostrar output verbose de pytest",
                        "default": False,
                    },
                },
                "required": [],
            },
        },
        {
            "name": "analyze_code_quality",
            "description": analyze_code_quality.__doc__,
            "input_schema": {
                "type": "object",
                "properties": {
                    "target_path": {
                        "type": "string",
                        "description": "Path a archivo o directorio a analizar",
                        "default": ".",
                    }
                },
                "required": [],
            },
        },
    ]
