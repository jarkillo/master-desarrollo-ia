"""
Ejercicio 1: Primer agente simple con Claude Agent SDK

Objetivo:
Construir un agente que responda preguntas sobre un repositorio de código
usando agentic search (búsqueda con comandos bash).

Conceptos:
- Context gathering desde file system
- Bash tools para exploración
- Feedback loop básico

Requisitos:
- anthropic>=0.18.0

Instalación:
    pip install anthropic

Uso:
    export ANTHROPIC_API_KEY="tu_api_key"
    python 01_agente_simple.py
"""

import os
from typing import Any

from anthropic import Anthropic


class SimpleAgent:
    """
    Agente simple que explora un repositorio de código usando comandos bash.

    Implementa el feedback loop básico:
    1. Gather Context: Ejecuta comandos bash para explorar
    2. Take Action: Analiza resultados
    3. Verify: Valida si la información es suficiente
    4. Repeat: Si no, ejecuta más comandos
    """

    def __init__(self, api_key: str | None = None):
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-sonnet-20241022"
        self.conversation_history: list[dict[str, Any]] = []

    def run_bash_command(self, command: str) -> str:
        """
        Ejecuta un comando bash y retorna el resultado.

        IMPORTANTE: En producción, deberías:
        - Validar comandos (whitelist)
        - Sandboxing (Docker, chroot)
        - Timeout para evitar comandos bloqueantes
        """
        import subprocess

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10,  # 10 segundos máximo
            )
            return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
        except subprocess.TimeoutExpired:
            return "Error: Command timed out"
        except Exception as e:
            return f"Error: {str(e)}"

    def answer_question(self, question: str, repo_path: str, max_iterations: int = 5) -> str:
        """
        Responde una pregunta sobre el repositorio usando agentic search.

        Args:
            question: Pregunta del usuario
            repo_path: Ruta al repositorio
            max_iterations: Máximo de iteraciones del feedback loop

        Returns:
            Respuesta del agente
        """
        # Inicializar conversación
        self.conversation_history = [
            {
                "role": "user",
                "content": f"""Responde esta pregunta sobre el repositorio en {repo_path}:

{question}

Puedes explorar el repositorio usando comandos bash. Usa herramientas como:
- ls: listar archivos
- find: buscar archivos por nombre/patrón
- grep: buscar texto en archivos
- cat: ver contenido de archivos
- head/tail: ver inicio/final de archivos

Explora de forma inteligente - no cargues archivos completos innecesariamente.
Usa grep con contexto (-A, -B, -C) para ver líneas alrededor de matches.
""",
            }
        ]

        # Feedback loop
        for iteration in range(max_iterations):
            print(f"\n--- Iteración {iteration + 1}/{max_iterations} ---")

            # Llamar a Claude con herramienta bash
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                tools=[
                    {
                        "name": "bash",
                        "description": "Ejecuta un comando bash en el sistema. Usa esto para explorar el repositorio (ls, find, grep, cat, etc.). IMPORTANTE: No ejecutes comandos destructivos (rm, mv, etc.).",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                "command": {
                                    "type": "string",
                                    "description": "El comando bash a ejecutar",
                                }
                            },
                            "required": ["command"],
                        },
                    }
                ],
                messages=self.conversation_history,
            )

            # Procesar respuesta
            if response.stop_reason == "end_turn":
                # Claude tiene la respuesta final
                final_answer = next(
                    (block.text for block in response.content if hasattr(block, "text")),
                    "No pude encontrar una respuesta.",
                )
                return final_answer

            elif response.stop_reason == "tool_use":
                # Claude quiere usar herramientas
                tool_results = []

                for block in response.content:
                    if block.type == "tool_use":
                        command = block.input["command"]
                        print(f"🔧 Ejecutando: {command}")

                        # Ejecutar comando
                        result = self.run_bash_command(command)
                        print(f"📄 Resultado (primeras 200 chars): {result[:200]}...")

                        tool_results.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": result,
                            }
                        )

                # Añadir herramientas a conversación
                self.conversation_history.append({"role": "assistant", "content": response.content})
                self.conversation_history.append({"role": "user", "content": tool_results})

            else:
                return f"Unexpected stop reason: {response.stop_reason}"

        return "Alcanzado el máximo de iteraciones sin respuesta definitiva."


def main() -> None:
    """Ejemplo de uso del agente simple."""
    print("=== Agente Simple - Exploración de Repositorio ===\n")

    # Verificar API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: Debes configurar ANTHROPIC_API_KEY")
        print("   export ANTHROPIC_API_KEY='tu_api_key'")
        return

    # Crear agente
    agent = SimpleAgent()

    # Preguntas de ejemplo
    questions = [
        "¿Cuántos archivos Python hay en este proyecto?",
        "¿Qué hace el archivo api.py?",
        "¿Hay tests en este proyecto? ¿Dónde están?",
    ]

    # Ruta al repositorio (ajustar según tu entorno)
    repo_path = "."  # Directorio actual

    # Preguntar al usuario qué pregunta hacer
    print("Preguntas disponibles:")
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")
    print(f"{len(questions) + 1}. Pregunta personalizada")

    choice = input(f"\nElige una pregunta (1-{len(questions) + 1}): ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(questions):
        question = questions[int(choice) - 1]
    elif choice == str(len(questions) + 1):
        question = input("Escribe tu pregunta: ").strip()
    else:
        print("Opción inválida")
        return

    # Ejecutar agente
    print(f"\n🤖 Pregunta: {question}\n")
    answer = agent.answer_question(question, repo_path)

    print("\n" + "=" * 60)
    print("📝 Respuesta final:")
    print("=" * 60)
    print(answer)


if __name__ == "__main__":
    main()


# ================================
# EJERCICIO PARA EL ESTUDIANTE
# ================================

"""
1. Ejecuta el agente con las 3 preguntas de ejemplo
2. Analiza qué comandos bash ejecuta Claude en cada caso
3. Modifica el código para:
   a) Añadir logging de todos los comandos ejecutados a un archivo
   b) Implementar un whitelist de comandos permitidos
   c) Añadir un contador de tokens usados

4. Crea una pregunta personalizada y observa cómo el agente la resuelve

5. DESAFÍO: Modifica el agente para que:
   - Guarde un caché de resultados de comandos repetidos
   - Sugiera mejoras al código encontrado (usando otro tool call)
   - Genere un resumen markdown del repositorio

Preguntas de reflexión:
- ¿Cuántas iteraciones necesitó Claude para cada pregunta?
- ¿Qué estrategia de búsqueda usó? (breadth-first, depth-first, etc.)
- ¿Ejecutó comandos innecesarios? ¿Cómo lo optimizarías?
"""
