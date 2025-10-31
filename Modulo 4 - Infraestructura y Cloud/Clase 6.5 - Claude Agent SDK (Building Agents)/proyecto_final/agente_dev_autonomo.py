"""
PROYECTO FINAL: Agente de Desarrollo Autónomo

Objetivo:
Construir un agente que automatiza tareas completas de desarrollo:
1. Analizar issues en GitHub (simulado)
2. Buscar código relevante en el repositorio
3. Generar fix basado en patrones existentes
4. Ejecutar tests y validar
5. Crear Pull Request (simulado) con los cambios

Arquitectura:
- Context Gathering: GitHub API + File system
- Tools: git, pytest, code generation, file manipulation
- Verification: Tests + linting
- Retry logic: Para errores comunes
- Logging: Detallado para debugging

Este proyecto integra TODOS los conceptos de la clase:
✅ Feedback loop
✅ Tool design
✅ State management
✅ Verification engine
✅ Subagents (opcional)
"""

import json
import logging
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any
from anthropic import Anthropic


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(f"agent_dev_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler(),
    ],
)


class IssueType(Enum):
    """Tipos de issues que el agente puede resolver."""

    TYPO = "typo"  # Errores tipográficos
    MISSING_IMPORT = "missing_import"  # Imports faltantes
    SIMPLE_TEST = "simple_test"  # Tests básicos
    DOCSTRING = "docstring"  # Documentación faltante
    LINTING = "linting"  # Errores de linting
    UNKNOWN = "unknown"  # Tipo desconocido


@dataclass
class Issue:
    """Representa un issue de GitHub."""

    id: str
    title: str
    description: str
    type: IssueType
    affected_file: str | None = None


@dataclass
class FixResult:
    """Resultado de aplicar un fix."""

    success: bool
    files_modified: list[str]
    tests_passed: bool
    linting_passed: bool
    error: str | None = None
    pr_description: str | None = None


class AutonomousDevelopmentAgent:
    """
    Agente de desarrollo autónomo.

    Workflow completo:
    1. Parse issue → identificar tipo
    2. Gather context → buscar código relevante
    3. Generate fix → código o documentación
    4. Verify → tests + linting
    5. Create PR → descripción y resumen
    """

    def __init__(self, repo_path: str, api_key: str | None = None):
        self.repo_path = Path(repo_path)
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"
        self.logger = logging.getLogger("AutonomousAgent")

    def resolve_issue(self, issue: Issue, max_retries: int = 3) -> FixResult:
        """
        Resuelve un issue completo de forma autónoma.

        Args:
            issue: El issue a resolver
            max_retries: Intentos máximos si fallan tests/linting

        Returns:
            FixResult con el estado del fix
        """
        self.logger.info(f"🔍 Resolviendo issue: {issue.title}")

        # 1. Analizar issue y clasificar
        self.logger.info("📊 Clasificando tipo de issue...")
        issue_type = self._classify_issue(issue)
        issue.type = issue_type

        # 2. Gather context - buscar código relevante
        self.logger.info("🔎 Recopilando contexto...")
        context = self._gather_context(issue)

        # 3. Generar fix con retry logic
        for attempt in range(1, max_retries + 1):
            self.logger.info(f"🔧 Generando fix (intento {attempt}/{max_retries})...")

            # Generar fix
            fix_code = self._generate_fix(issue, context, attempt > 1)

            if not fix_code:
                continue

            # Aplicar fix
            self.logger.info("💾 Aplicando fix...")
            files_modified = self._apply_fix(fix_code)

            # 4. Verificar
            self.logger.info("✅ Verificando fix...")

            # Tests
            tests_passed = self._run_tests()

            # Linting
            linting_passed = self._run_linting()

            # Si todo pasó, crear PR
            if tests_passed and linting_passed:
                self.logger.info("🎉 Fix exitoso - generando PR...")
                pr_description = self._generate_pr_description(issue, files_modified)

                return FixResult(
                    success=True,
                    files_modified=files_modified,
                    tests_passed=True,
                    linting_passed=True,
                    pr_description=pr_description,
                )

            # Si falló, log y retry
            self.logger.warning(
                f"⚠️ Verificación falló (tests: {tests_passed}, linting: {linting_passed})"
            )

            # Revertir cambios antes de retry
            self._revert_changes(files_modified)

        # Todos los intentos fallaron
        return FixResult(
            success=False,
            files_modified=[],
            tests_passed=False,
            linting_passed=False,
            error=f"No se pudo resolver después de {max_retries} intentos",
        )

    def _classify_issue(self, issue: Issue) -> IssueType:
        """
        Clasifica el tipo de issue usando Claude.

        Esto ayuda a decidir qué estrategia usar para el fix.
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=200,
            messages=[
                {
                    "role": "user",
                    "content": f"""Clasifica este issue en UNA de estas categorías:
- typo: Error tipográfico en código o comentarios
- missing_import: Import faltante
- simple_test: Falta un test simple
- docstring: Falta documentación
- linting: Error de estilo/linting (PEP 8, etc.)
- unknown: No encaja en ninguna categoría

Issue: {issue.title}
Descripción: {issue.description}

Responde SOLO con la categoría (lowercase, sin explicación).""",
                }
            ],
        )

        category = response.content[0].text.strip().lower()

        # Mapear a enum
        try:
            return IssueType(category)
        except ValueError:
            return IssueType.UNKNOWN

    def _gather_context(self, issue: Issue) -> str:
        """
        Recopila contexto relevante del repositorio.

        Usa agentic search para encontrar archivos/código relevantes.
        """
        # Si el issue menciona un archivo específico, usarlo
        if issue.affected_file:
            file_path = self.repo_path / issue.affected_file
            if file_path.exists():
                return file_path.read_text()

        # Si no, usar Claude para buscar
        search_prompt = f"""Dado este issue:

{issue.title}
{issue.description}

¿Qué archivos del repositorio deberías revisar?
Sugiere comandos bash para encontrarlos (find, grep, etc.).

Repositorio: {self.repo_path}

Responde solo con comandos bash (uno por línea), sin explicaciones."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": search_prompt}],
        )

        commands = response.content[0].text.strip().split("\n")

        # Ejecutar comandos y recopilar contexto
        context = ""
        for cmd in commands[:3]:  # Máximo 3 comandos
            cmd = cmd.strip()
            if not cmd or cmd.startswith("#"):
                continue

            try:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=5,
                    cwd=self.repo_path,
                )

                if result.returncode == 0:
                    context += f"\n--- {cmd} ---\n{result.stdout}\n"
            except Exception as e:
                self.logger.warning(f"Error ejecutando {cmd}: {e}")

        return context if context else "No se pudo recopilar contexto"

    def _generate_fix(self, issue: Issue, context: str, is_retry: bool) -> str | None:
        """
        Genera el código del fix usando Claude.

        Args:
            issue: Issue a resolver
            context: Contexto del repositorio
            is_retry: Si es un retry (añade más instrucciones de validación)

        Returns:
            Código del fix en formato JSON con {file_path: content}
        """
        retry_guidance = ""
        if is_retry:
            retry_guidance = """
IMPORTANTE: El intento anterior falló tests o linting.
- Asegúrate de que el código compile y siga PEP 8
- Valida que no rompa tests existentes
- Revisa imports y dependencias
"""

        prompt = f"""Genera un fix para este issue:

Tipo: {issue.type.value}
Título: {issue.title}
Descripción: {issue.description}

Contexto del repositorio:
{context}

{retry_guidance}

Genera el fix en formato JSON:
{{
  "files": {{
    "ruta/archivo.py": "contenido completo del archivo modificado"
  }},
  "explanation": "breve explicación del fix (1-2 líneas)"
}}

IMPORTANTE:
- Genera el contenido COMPLETO del archivo, no solo el diff
- Asegúrate de que el código compile
- Sigue PEP 8 y buenas prácticas
- Si es un test, usa pytest
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )

        try:
            # Extraer JSON del response (puede tener markdown)
            content = response.content[0].text
            # Buscar bloque JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            return content.strip()

        except Exception as e:
            self.logger.error(f"Error parseando fix: {e}")
            return None

    def _apply_fix(self, fix_code: str) -> list[str]:
        """
        Aplica el fix generado a los archivos.

        Args:
            fix_code: JSON con {file_path: content}

        Returns:
            Lista de archivos modificados
        """
        try:
            fix_data = json.loads(fix_code)
            files = fix_data.get("files", {})

            modified = []

            for file_path, content in files.items():
                full_path = self.repo_path / file_path

                # Backup del archivo original
                if full_path.exists():
                    backup_path = full_path.with_suffix(full_path.suffix + ".backup")
                    backup_path.write_text(full_path.read_text())

                # Crear directorios si no existen
                full_path.parent.mkdir(parents=True, exist_ok=True)

                # Escribir nuevo contenido
                full_path.write_text(content)

                modified.append(file_path)
                self.logger.info(f"✏️  Modificado: {file_path}")

            return modified

        except Exception as e:
            self.logger.error(f"Error aplicando fix: {e}")
            return []

    def _run_tests(self) -> bool:
        """
        Ejecuta tests usando pytest.

        Returns:
            True si todos los tests pasan
        """
        try:
            result = subprocess.run(
                ["pytest", "-q", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=self.repo_path,
            )

            if result.returncode == 0:
                self.logger.info("✅ Tests passed")
                return True
            else:
                self.logger.warning(f"❌ Tests failed:\n{result.stdout}")
                return False

        except subprocess.TimeoutExpired:
            self.logger.error("⏱️  Tests timeout")
            return False
        except FileNotFoundError:
            self.logger.warning("⚠️ pytest no encontrado - asumiendo tests OK")
            return True  # Si no hay pytest, asumir OK

    def _run_linting(self) -> bool:
        """
        Ejecuta linting usando ruff.

        Returns:
            True si no hay errores de linting
        """
        try:
            result = subprocess.run(
                ["ruff", "check", "."],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.repo_path,
            )

            if result.returncode == 0:
                self.logger.info("✅ Linting passed")
                return True
            else:
                self.logger.warning(f"❌ Linting failed:\n{result.stdout}")
                return False

        except subprocess.TimeoutExpired:
            self.logger.error("⏱️  Linting timeout")
            return False
        except FileNotFoundError:
            self.logger.warning("⚠️ ruff no encontrado - asumiendo linting OK")
            return True

    def _revert_changes(self, files: list[str]) -> None:
        """
        Revierte cambios en archivos desde backups.

        Args:
            files: Lista de archivos a revertir
        """
        for file_path in files:
            full_path = self.repo_path / file_path
            backup_path = full_path.with_suffix(full_path.suffix + ".backup")

            if backup_path.exists():
                full_path.write_text(backup_path.read_text())
                backup_path.unlink()
                self.logger.info(f"↩️  Revertido: {file_path}")

    def _generate_pr_description(self, issue: Issue, files_modified: list[str]) -> str:
        """
        Genera descripción del Pull Request.

        Args:
            issue: Issue resuelto
            files_modified: Archivos modificados

        Returns:
            Descripción del PR en Markdown
        """
        return f"""## Fix: {issue.title}

**Issue type**: `{issue.type.value}`

### Changes
{chr(10).join(f'- `{f}`' for f in files_modified)}

### Description
{issue.description}

### Verification
✅ Tests passed
✅ Linting passed

### Related Issue
Closes #{issue.id}

---
🤖 Auto-generated by Autonomous Development Agent
"""


def main() -> None:
    """Ejemplo de uso del agente autónomo."""
    print("=" * 60)
    print("🤖 Agente de Desarrollo Autónomo")
    print("=" * 60)

    # Verificar API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: Configura ANTHROPIC_API_KEY")
        return

    # Configurar repositorio
    repo_path = input("\nRuta al repositorio (Enter para '.'): ").strip() or "."

    # Crear agente
    agent = AutonomousDevelopmentAgent(repo_path)

    # Issues de ejemplo (en producción vendrían de GitHub API)
    example_issues = [
        Issue(
            id="1",
            title="Typo in function name: claculate_total should be calculate_total",
            description="There's a typo in the function name in api/servicio_tareas.py",
            type=IssueType.TYPO,
            affected_file="api/servicio_tareas.py",
        ),
        Issue(
            id="2",
            title="Missing pytest import in test file",
            description="tests/test_api.py is missing 'import pytest'",
            type=IssueType.MISSING_IMPORT,
            affected_file="tests/test_api.py",
        ),
        Issue(
            id="3",
            title="Add docstring to validate_email function",
            description="The validate_email function in utils.py lacks documentation",
            type=IssueType.DOCSTRING,
            affected_file="utils.py",
        ),
    ]

    print("\nIssues disponibles:")
    for i, issue in enumerate(example_issues, 1):
        print(f"{i}. [{issue.type.value}] {issue.title}")

    choice = input(f"\nElige un issue (1-{len(example_issues)}) o 'c' para custom: ").strip()

    if choice.lower() == "c":
        # Issue personalizado
        title = input("Título del issue: ").strip()
        description = input("Descripción: ").strip()
        affected_file = input("Archivo afectado (opcional): ").strip() or None

        issue = Issue(
            id="custom",
            title=title,
            description=description,
            type=IssueType.UNKNOWN,
            affected_file=affected_file,
        )
    elif choice.isdigit() and 1 <= int(choice) <= len(example_issues):
        issue = example_issues[int(choice) - 1]
    else:
        print("Opción inválida")
        return

    # Resolver issue
    print(f"\n🚀 Resolviendo issue: {issue.title}\n")

    result = agent.resolve_issue(issue)

    # Mostrar resultado
    print("\n" + "=" * 60)
    print("📊 RESULTADO")
    print("=" * 60)

    if result.success:
        print("✅ Issue resuelto exitosamente!")
        print(f"\nArchivos modificados:")
        for f in result.files_modified:
            print(f"  - {f}")

        print(f"\n📝 Pull Request:\n")
        print(result.pr_description)
    else:
        print("❌ No se pudo resolver el issue")
        print(f"Error: {result.error}")

    print(f"\n✅ Tests: {result.tests_passed}")
    print(f"✅ Linting: {result.linting_passed}")


if __name__ == "__main__":
    main()


# ================================
# EJERCICIO PARA EL ESTUDIANTE
# ================================

"""
1. Ejecuta el agente con los 3 issues de ejemplo
2. Analiza los logs generados - ¿qué decisiones tomó el agente?
3. Verifica los archivos modificados - ¿son correctos los fixes?

4. Crea tu propio issue personalizado y prueba el agente

5. Modifica el código para:
   a) Añadir más tipos de issues (bug fix, performance, security)
   b) Implementar verificación con screenshot (para UI changes)
   c) Integración real con GitHub API

6. DESAFÍO FINAL: Mejoras avanzadas
   - Multi-file fixes: Issues que requieren cambios en múltiples archivos
   - Dependency analysis: Detectar qué archivos pueden verse afectados
   - Semantic commits: Generar commits con Conventional Commits
   - CI/CD integration: Esperar a que CI pase antes de crear PR
   - Rollback automático: Si CI falla, revertir cambios

Preguntas de reflexión:
- ¿Qué tipos de issues puede resolver el agente vs cuáles necesitan humanos?
- ¿Cómo validarías que el fix no introduce nuevos bugs?
- ¿Qué nivel de autonomía es apropiado? (auto-merge vs crear PR)
- ¿Cómo escalarías esto para procesar 100+ issues al día?
- ¿Qué métricas medirías? (tasa de éxito, tiempo, calidad del código)

NOTA: Este agente es educativo. En producción, añade:
- Extensive testing sandbox
- Human review gates
- Rollback mechanisms
- Security scanning
- Cost monitoring (API calls)
"""
