"""Tools para análisis de calidad de código."""

import subprocess
from typing import Literal

from pydantic import BaseModel


class ToolSuccess(BaseModel):
    status: Literal["success"] = "success"
    data: dict


class ToolError(BaseModel):
    status: Literal["error"] = "error"
    error_type: str
    message: str
    suggestion: str


ToolResult = ToolSuccess | ToolError


def analyze_code_quality(target_path: str = ".") -> ToolResult:
    """
    Analiza calidad de código con linters (ruff, bandit).

    **Cuándo usar:**
    - Antes de hacer commit
    - Para revisar calidad de código nuevo
    - Identificar problemas de seguridad

    Args:
        target_path: Path a archivo o directorio a analizar

    Returns:
        ToolSuccess con reporte de issues O ToolError
    """
    issues = []

    # 1. Ruff (linting)
    try:
        ruff_result = subprocess.run(
            ["ruff", "check", target_path],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if ruff_result.returncode != 0 and ruff_result.stdout:
            issues.append(
                {
                    "tool": "ruff",
                    "severity": "warning",
                    "message": "Issues de linting encontrados",
                    "details": ruff_result.stdout,
                }
            )
    except FileNotFoundError:
        issues.append(
            {
                "tool": "ruff",
                "severity": "info",
                "message": "ruff no instalado (opcional)",
                "details": "Instala con: pip install ruff",
            }
        )

    # 2. Bandit (seguridad)
    try:
        bandit_result = subprocess.run(
            ["bandit", "-r", target_path, "-ll"],  # Solo high severity
            capture_output=True,
            text=True,
            timeout=30,
        )

        if bandit_result.returncode != 0 and bandit_result.stdout:
            issues.append(
                {
                    "tool": "bandit",
                    "severity": "high",
                    "message": "Issues de seguridad encontrados",
                    "details": bandit_result.stdout,
                }
            )
    except FileNotFoundError:
        issues.append(
            {
                "tool": "bandit",
                "severity": "info",
                "message": "bandit no instalado (recomendado)",
                "details": "Instala con: pip install bandit",
            }
        )

    # Generar reporte
    if any(issue["severity"] == "high" for issue in issues):
        return ToolError(
            error_type="quality_issues",
            message=f"Encontrados {len(issues)} issues de calidad",
            suggestion=(
                "Revisa los issues de alta severidad y corrígelos antes de continuar."
            ),
        )

    return ToolSuccess(
        data={
            "target_path": target_path,
            "issues_count": len(issues),
            "issues": issues,
            "status": "passed" if not issues else "warnings",
        }
    )
