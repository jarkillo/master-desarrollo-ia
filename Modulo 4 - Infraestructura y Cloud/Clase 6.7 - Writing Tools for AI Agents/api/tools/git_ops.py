"""Tools para operaciones de Git."""

import re
import subprocess
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ToolSuccess(BaseModel):
    status: Literal["success"] = "success"
    data: dict


class ToolError(BaseModel):
    status: Literal["error"] = "error"
    error_type: str
    message: str
    suggestion: str


ToolResult = ToolSuccess | ToolError


class GitBranchInput(BaseModel):
    """Schema para crear rama de Git."""

    branch_name: str = Field(
        min_length=3,
        max_length=100,
        description="Nombre de la rama (e.g., 'feature/add-auth')",
    )

    @field_validator("branch_name")
    @classmethod
    def validate_branch_name(cls, v: str) -> str:
        """Valida nombre de rama según convenciones Git."""
        # Validar caracteres permitidos
        if not re.match(r"^[a-zA-Z0-9/_-]+$", v):
            raise ValueError(
                "Nombre de rama solo puede contener letras, números, /, - y _"
            )

        # Validar que no empieza con /
        if v.startswith("/"):
            raise ValueError("Nombre de rama no puede empezar con /")

        return v


def create_git_branch(branch_name: str) -> ToolResult:
    """
    Crea nueva rama de Git para feature/bugfix.

    **Cuándo usar:**
    - Iniciar trabajo en nueva feature
    - Crear branch para bugfix
    - Preparar branch para experimento

    Args:
        branch_name: Nombre de la rama
            Ejemplos:
            - "feature/add-authentication"
            - "bugfix/fix-login-error"
            - "refactor/improve-database"

    Returns:
        ToolSuccess con información de la rama O ToolError
    """
    try:
        validated = GitBranchInput(branch_name=branch_name)
    except Exception as e:
        return ToolError(
            error_type="validation_error",
            message=str(e),
            suggestion="Usa formato: feature/descripcion o bugfix/descripcion",
        )

    # Verificar que estamos en un repo git
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            check=True,
            capture_output=True,
            timeout=5,
        )
    except subprocess.CalledProcessError:
        return ToolError(
            error_type="not_a_git_repo",
            message="No estás en un repositorio Git",
            suggestion="Inicializa un repo con: git init",
        )

    # Crear rama
    try:
        result = subprocess.run(
            ["git", "checkout", "-b", validated.branch_name],
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )

        return ToolSuccess(
            data={
                "branch_name": validated.branch_name,
                "message": f"Rama '{validated.branch_name}' creada y checked out",
                "output": result.stdout,
            }
        )
    except subprocess.CalledProcessError as e:
        # Rama ya existe
        if "already exists" in e.stderr:
            return ToolError(
                error_type="branch_exists",
                message=f"Rama '{validated.branch_name}' ya existe",
                suggestion="Usa git checkout para cambiar a la rama existente.",
            )

        return ToolError(
            error_type="git_error",
            message=f"Error creando rama: {e.stderr}",
            suggestion="Verifica el estado de Git con: git status",
        )
    except Exception as e:
        return ToolError(
            error_type="unexpected_error",
            message=f"Error inesperado: {str(e)}",
            suggestion="Revisa los logs para más detalles.",
        )


def git_commit(message: str, files: list[str] | None = None) -> ToolResult:
    """
    Crea commit de Git con mensaje siguiendo convenciones.

    **Cuándo usar:**
    - Después de completar un cambio lógico
    - Siguiendo Conventional Commits

    Args:
        message: Mensaje de commit
            Formato: <type>: <description>
            Ejemplos:
            - "feat: add user authentication"
            - "fix: resolve login bug"
            - "docs: update README"

        files: Lista de archivos a commitear (None = todos los staged)

    Returns:
        ToolSuccess con commit hash O ToolError
    """
    # Validar formato de mensaje (Conventional Commits)
    valid_types = ["feat", "fix", "docs", "style", "refactor", "test", "chore"]
    if not any(message.startswith(f"{t}:") for t in valid_types):
        return ToolError(
            error_type="invalid_commit_message",
            message="Mensaje no sigue Conventional Commits",
            suggestion=(
                f"Usa formato: <type>: <description>. "
                f"Types válidos: {', '.join(valid_types)}"
            ),
        )

    try:
        # Add files si se especifican
        if files:
            for file in files:
                subprocess.run(
                    ["git", "add", file], check=True, capture_output=True, timeout=5
                )

        # Commit
        result = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )

        # Obtener commit hash
        hash_result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        commit_hash = hash_result.stdout.strip()[:7]

        return ToolSuccess(
            data={
                "commit_hash": commit_hash,
                "message": message,
                "output": result.stdout,
            }
        )
    except subprocess.CalledProcessError as e:
        if "nothing to commit" in e.stdout:
            return ToolError(
                error_type="nothing_to_commit",
                message="No hay cambios para commitear",
                suggestion="Usa git status para ver el estado actual.",
            )

        return ToolError(
            error_type="commit_failed",
            message=f"Error creando commit: {e.stderr}",
            suggestion="Verifica que hay archivos staged: git status",
        )
