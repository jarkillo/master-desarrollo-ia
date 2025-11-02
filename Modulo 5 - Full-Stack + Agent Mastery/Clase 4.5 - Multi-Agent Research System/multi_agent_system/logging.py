"""
Logging estructurado para sistemas multi-agente.

Implementa:
- AgentLogger (logging por agente)
- Structured logging (JSON format)
- Decision tracking
- Tool call tracking
- Error tracking
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any


class AgentLogger:
    """
    Logger especializado para sistemas multi-agente.

    Registra:
    - Decisiones de agentes
    - Uso de herramientas
    - Errores y excepciones
    - Métricas de performance
    """

    def __init__(self, agent_id: str, log_dir: str = "./logs"):
        """
        Inicializa el logger.

        Args:
            agent_id: ID único del agente
            log_dir: Directorio donde guardar logs
        """
        self.agent_id = agent_id
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        # Crear logger específico para este agente
        self.logger = logging.getLogger(f"agent.{agent_id}")
        self.logger.setLevel(logging.INFO)

        # Handler para archivo JSON
        log_file = self.log_dir / f"{agent_id}.log"
        handler = logging.FileHandler(log_file, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(handler)

        # También log a consola (opcional)
        console = logging.StreamHandler()
        console.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(console)

    def log_decision(self, decision: str, context: dict[str, Any]):
        """
        Registra una decisión del agente.

        Args:
            decision: Descripción de la decisión
            context: Contexto de la decisión
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": self.agent_id,
            "event_type": "decision",
            "decision": decision,
            "context": context,
        }
        self.logger.info(json.dumps(log_entry, ensure_ascii=False))

    def log_tool_call(self, tool: str, params: dict[str, Any], result: Any):
        """
        Registra uso de herramienta.

        Args:
            tool: Nombre de la herramienta
            params: Parámetros pasados
            result: Resultado de la herramienta
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": self.agent_id,
            "event_type": "tool_call",
            "tool": tool,
            "params": params,
            "result_preview": str(result)[:200] if result else None,  # Truncar
        }
        self.logger.info(json.dumps(log_entry, ensure_ascii=False, default=str))

    def log_error(self, error: Exception, context: dict[str, Any]):
        """
        Registra error.

        Args:
            error: Excepción capturada
            context: Contexto donde ocurrió el error
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": self.agent_id,
            "event_type": "error",
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
        }
        self.logger.error(json.dumps(log_entry, ensure_ascii=False))

    def log_metric(self, metric_name: str, value: Any, unit: str = ""):
        """
        Registra métrica de performance.

        Args:
            metric_name: Nombre de la métrica
            value: Valor de la métrica
            unit: Unidad de medida (opcional)
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": self.agent_id,
            "event_type": "metric",
            "metric_name": metric_name,
            "value": value,
            "unit": unit,
        }
        self.logger.info(json.dumps(log_entry, ensure_ascii=False, default=str))

    def log_message(self, message_type: str, sender: str, receiver: str, content: Any):
        """
        Registra mensaje enviado/recibido.

        Args:
            message_type: Tipo de mensaje
            sender: Agente que envía
            receiver: Agente que recibe
            content: Contenido del mensaje
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": self.agent_id,
            "event_type": "message",
            "message_type": message_type,
            "sender": sender,
            "receiver": receiver,
            "content_preview": str(content)[:100],  # Truncar
        }
        self.logger.info(json.dumps(log_entry, ensure_ascii=False, default=str))

    def log_task_start(self, task_id: int, description: str):
        """
        Registra inicio de tarea.

        Args:
            task_id: ID de la tarea
            description: Descripción de la tarea
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": self.agent_id,
            "event_type": "task_start",
            "task_id": task_id,
            "description": description,
        }
        self.logger.info(json.dumps(log_entry, ensure_ascii=False))

    def log_task_complete(
        self, task_id: int, duration_seconds: float, confidence: float
    ):
        """
        Registra finalización de tarea.

        Args:
            task_id: ID de la tarea
            duration_seconds: Duración en segundos
            confidence: Score de confianza (0.0-1.0)
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": self.agent_id,
            "event_type": "task_complete",
            "task_id": task_id,
            "duration_seconds": duration_seconds,
            "confidence": confidence,
        }
        self.logger.info(json.dumps(log_entry, ensure_ascii=False))


class SystemLogger:
    """
    Logger para el sistema multi-agente completo.

    Registra eventos a nivel de sistema (no de agente individual).
    """

    def __init__(self, log_dir: str = "./logs"):
        """
        Inicializa el logger de sistema.

        Args:
            log_dir: Directorio donde guardar logs
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        self.logger = logging.getLogger("system")
        self.logger.setLevel(logging.INFO)

        # Handler para archivo
        log_file = self.log_dir / "system.log"
        handler = logging.FileHandler(log_file, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(handler)

    def log_research_start(self, query: str, num_tasks: int):
        """Registra inicio de investigación."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "research_start",
            "query": query,
            "num_tasks": num_tasks,
        }
        self.logger.info(json.dumps(log_entry, ensure_ascii=False))

    def log_research_complete(
        self, query: str, duration_seconds: float, num_sources: int
    ):
        """Registra finalización de investigación."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "research_complete",
            "query": query,
            "duration_seconds": duration_seconds,
            "num_sources": num_sources,
        }
        self.logger.info(json.dumps(log_entry, ensure_ascii=False))

    def log_error(self, error: Exception, context: dict[str, Any]):
        """Registra error a nivel de sistema."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "system_error",
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
        }
        self.logger.error(json.dumps(log_entry, ensure_ascii=False))


def analyze_logs(log_file: Path) -> dict[str, Any]:
    """
    Analiza archivo de logs y genera estadísticas.

    Args:
        log_file: Path al archivo de logs

    Returns:
        Diccionario con estadísticas
    """
    if not log_file.exists():
        return {"error": f"Log file not found: {log_file}"}

    events = []
    with open(log_file, encoding="utf-8") as f:
        for line in f:
            try:
                events.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue

    if not events:
        return {"error": "No events found in log file"}

    # Contar eventos por tipo
    event_counts = {}
    for event in events:
        event_type = event.get("event_type", "unknown")
        event_counts[event_type] = event_counts.get(event_type, 0) + 1

    # Calcular métricas
    tool_calls = [e for e in events if e.get("event_type") == "tool_call"]
    errors = [e for e in events if e.get("event_type") == "error"]
    tasks = [e for e in events if e.get("event_type") == "task_complete"]

    avg_confidence = (
        sum(t.get("confidence", 0) for t in tasks) / len(tasks) if tasks else 0
    )

    return {
        "total_events": len(events),
        "event_counts": event_counts,
        "total_tool_calls": len(tool_calls),
        "total_errors": len(errors),
        "total_tasks_completed": len(tasks),
        "avg_task_confidence": round(avg_confidence, 2),
        "time_range": {
            "first_event": events[0].get("timestamp") if events else None,
            "last_event": events[-1].get("timestamp") if events else None,
        },
    }
