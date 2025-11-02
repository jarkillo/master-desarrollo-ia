"""
Sistema Multi-Agente para Investigación.

Este paquete implementa un sistema de investigación basado en múltiples
agentes especializados que colaboran para resolver tareas complejas.

Basado en: https://www.anthropic.com/engineering/multi-agent-research-system
"""

from .core import (
    AgentResult,
    AgentRole,
    LeadAgent,
    MessageBus,
    MultiAgentResearchSystem,
    SharedMemory,
    SubAgent,
    Task,
)
from .logging import AgentLogger
from .memory import PersistentMemory

__all__ = [
    "AgentRole",
    "Task",
    "AgentResult",
    "MessageBus",
    "SharedMemory",
    "LeadAgent",
    "SubAgent",
    "MultiAgentResearchSystem",
    "PersistentMemory",
    "AgentLogger",
]
