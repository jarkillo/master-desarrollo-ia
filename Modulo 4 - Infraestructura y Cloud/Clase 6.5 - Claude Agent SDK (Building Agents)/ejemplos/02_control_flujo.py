"""
Ejercicio 2: Loops y control de flujo en agentes

Objetivo:
Implementar un agente con manejo de estados, retry logic y control de flujo avanzado.

Conceptos:
- State management (estados de tareas)
- Error handling con retry logic
- Feedback loop con verificación
- Iteración controlada

Caso de uso:
Agente que procesa una lista de tareas de desarrollo (refactoring, testing, documentation)
con reintentos automáticos en caso de fallo.
"""

import os
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any

from anthropic import Anthropic


class TaskState(Enum):
    """Estados posibles de una tarea."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


@dataclass
class Task:
    """Representa una tarea a ejecutar."""

    id: str
    description: str
    state: TaskState = TaskState.PENDING
    attempts: int = 0
    max_attempts: int = 3
    result: str | None = None
    error: str | None = None


class StatefulAgent:
    """
    Agente con manejo de estados y retry logic.

    Implementa:
    - State machine para tareas (pending → in_progress → completed/failed)
    - Retry logic con backoff exponencial
    - Verificación de resultados antes de marcar como completado
    """

    def __init__(self, api_key: str | None = None):
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-sonnet-20241022"
        self.tasks: list[Task] = []

    def add_task(self, task_id: str, description: str, max_attempts: int = 3) -> None:
        """Añade una tarea a la cola."""
        self.tasks.append(
            Task(id=task_id, description=description, max_attempts=max_attempts)
        )

    def get_task_by_id(self, task_id: str) -> Task | None:
        """Obtiene una tarea por ID."""
        return next((t for t in self.tasks if t.id == task_id), None)

    def transition_state(self, task: Task, new_state: TaskState) -> None:
        """
        Transición de estado con validación.

        Flujo válido:
        PENDING → IN_PROGRESS → COMPLETED
                             → FAILED → RETRYING → IN_PROGRESS
        """
        valid_transitions = {
            TaskState.PENDING: [TaskState.IN_PROGRESS],
            TaskState.IN_PROGRESS: [TaskState.COMPLETED, TaskState.FAILED],
            TaskState.FAILED: [TaskState.RETRYING],
            TaskState.RETRYING: [TaskState.IN_PROGRESS],
        }

        if new_state not in valid_transitions.get(task.state, []):
            raise ValueError(
                f"Invalid transition: {task.state.value} → {new_state.value}"
            )

        print(f"📊 Task {task.id}: {task.state.value} → {new_state.value}")
        task.state = new_state

    def verify_result(self, task: Task, result: str) -> tuple[bool, str]:
        """
        Verifica si el resultado de una tarea es válido.

        Usa Claude como verificador (LLM-as-judge pattern).

        Returns:
            (is_valid, feedback)
        """
        verification_prompt = f"""Verifica si este resultado es válido para la tarea:

Tarea: {task.description}
Resultado: {result}

Responde SOLO con:
- "VÁLIDO" si el resultado cumple la tarea
- "INVÁLIDO: [razón]" si no cumple, explicando por qué

Sé estricto pero justo."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": verification_prompt}],
        )

        answer = response.content[0].text.strip()

        if answer.startswith("VÁLIDO"):
            return True, "Resultado validado correctamente"
        else:
            return False, answer.replace("INVÁLIDO:", "").strip()

    def execute_task_with_retry(self, task: Task) -> None:
        """
        Ejecuta una tarea con retry logic.

        Implementa:
        - Backoff exponencial (1s, 2s, 4s, ...)
        - Máximo de reintentos configurables
        - Verificación de resultados
        """
        while task.attempts < task.max_attempts:
            task.attempts += 1

            # Transition to IN_PROGRESS
            if task.state == TaskState.PENDING or task.state == TaskState.RETRYING:
                self.transition_state(task, TaskState.IN_PROGRESS)

            print(f"\n🔄 Ejecutando tarea {task.id} (intento {task.attempts}/{task.max_attempts})")

            try:
                # Ejecutar tarea
                result = self._execute_task(task)

                # Verificar resultado
                is_valid, feedback = self.verify_result(task, result)

                if is_valid:
                    # Tarea completada exitosamente
                    task.result = result
                    self.transition_state(task, TaskState.COMPLETED)
                    print(f"✅ Tarea {task.id} completada")
                    return
                else:
                    # Resultado inválido, pero no es un error técnico
                    print(f"⚠️ Resultado inválido: {feedback}")
                    task.error = f"Verificación falló: {feedback}"

                    if task.attempts < task.max_attempts:
                        # Retry
                        self.transition_state(task, TaskState.FAILED)
                        self.transition_state(task, TaskState.RETRYING)

                        # Backoff exponencial
                        wait_time = 2 ** (task.attempts - 1)
                        print(f"⏳ Esperando {wait_time}s antes de reintentar...")
                        time.sleep(wait_time)
                    else:
                        # Máximo de intentos alcanzado
                        self.transition_state(task, TaskState.FAILED)
                        print(f"❌ Tarea {task.id} falló después de {task.attempts} intentos")
                        return

            except Exception as e:
                # Error técnico durante ejecución
                task.error = str(e)
                print(f"💥 Error ejecutando tarea: {e}")

                if task.attempts < task.max_attempts:
                    self.transition_state(task, TaskState.FAILED)
                    self.transition_state(task, TaskState.RETRYING)

                    wait_time = 2 ** (task.attempts - 1)
                    print(f"⏳ Esperando {wait_time}s antes de reintentar...")
                    time.sleep(wait_time)
                else:
                    self.transition_state(task, TaskState.FAILED)
                    print(f"❌ Tarea {task.id} falló después de {task.attempts} intentos")
                    return

    def _execute_task(self, task: Task) -> str:
        """
        Ejecuta la tarea usando Claude.

        En un agente real, esto podría incluir:
        - Tool calls para ejecutar código
        - Verificación de tests
        - Generación de documentación
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": f"""Ejecuta esta tarea de desarrollo:

{task.description}

Proporciona el resultado de forma clara y concisa.
Si la tarea requiere código, genera el código completo.
Si requiere documentación, escribe documentación clara.""",
                }
            ],
        )

        return response.content[0].text

    def run_all_tasks(self) -> dict[str, Any]:
        """
        Ejecuta todas las tareas pendientes.

        Returns:
            Resumen de ejecución con estadísticas
        """
        print("=" * 60)
        print("🚀 Ejecutando todas las tareas")
        print("=" * 60)

        for task in self.tasks:
            if task.state == TaskState.PENDING:
                self.execute_task_with_retry(task)

        # Generar resumen
        summary = {
            "total": len(self.tasks),
            "completed": sum(1 for t in self.tasks if t.state == TaskState.COMPLETED),
            "failed": sum(1 for t in self.tasks if t.state == TaskState.FAILED),
            "total_attempts": sum(t.attempts for t in self.tasks),
        }

        return summary

    def print_status(self) -> None:
        """Imprime el estado actual de todas las tareas."""
        print("\n" + "=" * 60)
        print("📊 Estado de tareas")
        print("=" * 60)

        for task in self.tasks:
            status_emoji = {
                TaskState.PENDING: "⏳",
                TaskState.IN_PROGRESS: "🔄",
                TaskState.COMPLETED: "✅",
                TaskState.FAILED: "❌",
                TaskState.RETRYING: "🔁",
            }

            print(f"{status_emoji[task.state]} [{task.id}] {task.description}")
            print(f"   Estado: {task.state.value} | Intentos: {task.attempts}/{task.max_attempts}")

            if task.result:
                print(f"   Resultado: {task.result[:100]}...")
            if task.error:
                print(f"   Error: {task.error}")
            print()


def main() -> None:
    """Ejemplo de uso del agente stateful."""
    print("=== Agente con State Management y Retry Logic ===\n")

    # Verificar API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: Debes configurar ANTHROPIC_API_KEY")
        return

    # Crear agente
    agent = StatefulAgent()

    # Añadir tareas
    agent.add_task(
        "refactor-1",
        "Refactoriza esta función para usar list comprehension:\n\n"
        "def get_evens(nums):\n"
        "    result = []\n"
        "    for n in nums:\n"
        "        if n % 2 == 0:\n"
        "            result.append(n)\n"
        "    return result",
        max_attempts=2,
    )

    agent.add_task(
        "test-1",
        "Escribe tests unitarios con pytest para una función que calcula el factorial de un número",
        max_attempts=3,
    )

    agent.add_task(
        "doc-1",
        "Escribe documentación en formato docstring para una función que valida emails usando regex",
        max_attempts=2,
    )

    # Ejecutar todas las tareas
    summary = agent.run_all_tasks()

    # Mostrar estado final
    agent.print_status()

    # Mostrar resumen
    print("=" * 60)
    print("📈 Resumen de ejecución")
    print("=" * 60)
    print(f"Total de tareas: {summary['total']}")
    print(f"Completadas: {summary['completed']}")
    print(f"Fallidas: {summary['failed']}")
    print(f"Intentos totales: {summary['total_attempts']}")
    print(f"Tasa de éxito: {summary['completed'] / summary['total'] * 100:.1f}%")


if __name__ == "__main__":
    main()


# ================================
# EJERCICIO PARA EL ESTUDIANTE
# ================================

"""
1. Ejecuta el agente y observa:
   - ¿Cuántos intentos necesitó cada tarea?
   - ¿Hubo alguna tarea que falló la verificación?
   - ¿Cuánto tiempo tomó el backoff exponencial?

2. Modifica el código para:
   a) Añadir un estado CANCELLED (usuario puede cancelar tareas)
   b) Implementar prioridades (high, medium, low) en las tareas
   c) Persistir el estado de tareas en un archivo JSON

3. Crea tu propia tarea personalizada y prueba el retry logic

4. DESAFÍO: Implementa estas mejoras:
   - Circuit breaker: Si 3 tareas fallan seguidas, parar el agente
   - Métricas: Tiempo promedio por tarea, tasa de éxito por tipo
   - Notificaciones: Enviar email cuando una tarea falla definitivamente

Preguntas de reflexión:
- ¿Cuándo es apropiado el backoff exponencial vs backoff lineal?
- ¿Qué otras verificaciones podrías añadir además de LLM-as-judge?
- ¿Cómo escalarías esto para 1000+ tareas concurrentes?
"""
