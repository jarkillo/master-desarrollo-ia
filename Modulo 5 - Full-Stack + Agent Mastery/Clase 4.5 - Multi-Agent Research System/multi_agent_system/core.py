"""
Core del sistema multi-agente.

Implementa los componentes principales:
- Lead Agent (orquestador)
- SubAgents (workers especializados)
- Message Bus (comunicación)
- Shared Memory (estado compartido)
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from datetime import datetime


class AgentRole(str, Enum):
    """Roles de agentes en el sistema."""

    LEAD = "lead"
    RESEARCHER = "researcher"
    ANALYZER = "analyzer"
    WRITER = "writer"
    CRITIC = "critic"
    CITATION_VERIFIER = "citation_verifier"


@dataclass
class Task:
    """
    Tarea asignada a un subagent.

    Attributes:
        id: Identificador único de la tarea
        description: Descripción específica de qué investigar
        agent_role: Rol del agente asignado
        tools: Herramientas disponibles para el agente
        max_searches: Número máximo de búsquedas permitidas
        success_criteria: Criterios para considerar la tarea completa
        output_format: Formato esperado del output
    """

    id: int
    description: str
    agent_role: AgentRole
    tools: List[str]
    max_searches: int
    success_criteria: str
    output_format: str


@dataclass
class AgentResult:
    """
    Resultado de investigación de un agente.

    Attributes:
        task_id: ID de la tarea completada
        agent_role: Rol del agente que ejecutó la tarea
        findings: Findings de la investigación
        sources: Lista de fuentes consultadas
        confidence: Score de confianza (0.0-1.0)
        gaps_identified: Lista de gaps de información encontrados
        metadata: Metadata adicional (búsquedas realizadas, tiempo, etc.)
    """

    task_id: int
    agent_role: AgentRole
    findings: str
    sources: List[str]
    confidence: float = 0.0
    gaps_identified: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class MessageBus:
    """
    Bus de comunicación entre agentes.

    Permite a los agentes enviarse mensajes entre sí de forma asíncrona.
    Registra todos los mensajes para auditoría y debugging.
    """

    def __init__(self):
        self._messages: List[Dict[str, Any]] = []
        self._subscribers: Dict[str, List[callable]] = {}

    def publish(self, sender: str, receiver: str, message: Any, message_type: str = "data"):
        """
        Publica un mensaje en el bus.

        Args:
            sender: ID del agente que envía
            receiver: ID del agente que recibe
            message: Contenido del mensaje
            message_type: Tipo de mensaje (data, control, error)
        """
        msg_entry = {
            "sender": sender,
            "receiver": receiver,
            "message": message,
            "message_type": message_type,
            "timestamp": datetime.now().isoformat(),
        }

        self._messages.append(msg_entry)

        # Notificar a subscribers si los hay
        if receiver in self._subscribers:
            for callback in self._subscribers[receiver]:
                callback(msg_entry)

    def subscribe(self, receiver: str, callback: callable):
        """
        Suscribe un callback para recibir mensajes.

        Args:
            receiver: ID del agente que recibe
            callback: Función a llamar cuando llegue mensaje
        """
        if receiver not in self._subscribers:
            self._subscribers[receiver] = []
        self._subscribers[receiver].append(callback)

    def get_messages(
        self, receiver: str, message_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtiene mensajes para un agente específico.

        Args:
            receiver: ID del agente
            message_type: Filtrar por tipo de mensaje (opcional)

        Returns:
            Lista de mensajes
        """
        messages = [m for m in self._messages if m["receiver"] == receiver]

        if message_type:
            messages = [m for m in messages if m["message_type"] == message_type]

        return messages

    def clear(self):
        """Limpia todos los mensajes del bus."""
        self._messages.clear()

    def export_trace(self) -> List[Dict[str, Any]]:
        """
        Exporta el trace completo de mensajes.

        Returns:
            Lista de todos los mensajes enviados
        """
        return self._messages.copy()


class SharedMemory:
    """
    Memoria compartida entre agentes.

    Permite a múltiples agentes leer y escribir datos compartidos.
    Útil para: plan de investigación, resultados intermedios, configuración.
    """

    def __init__(self):
        self._data: Dict[str, Any] = {}

    def store(self, key: str, value: Any):
        """
        Almacena un valor en memoria compartida.

        Args:
            key: Clave del dato
            value: Valor a almacenar
        """
        self._data[key] = value

    def retrieve(self, key: str, default: Any = None) -> Any:
        """
        Recupera un valor de memoria compartida.

        Args:
            key: Clave del dato
            default: Valor por defecto si no existe

        Returns:
            Valor almacenado o default
        """
        return self._data.get(key, default)

    def update(self, key: str, update_fn: callable):
        """
        Actualiza un valor usando una función.

        Args:
            key: Clave del dato
            update_fn: Función que recibe valor actual y retorna nuevo valor
        """
        current = self.retrieve(key)
        updated = update_fn(current)
        self.store(key, updated)

    def delete(self, key: str):
        """Elimina un valor de memoria."""
        if key in self._data:
            del self._data[key]

    def clear(self):
        """Limpia toda la memoria."""
        self._data.clear()

    def keys(self) -> List[str]:
        """Retorna todas las claves almacenadas."""
        return list(self._data.keys())


class LeadAgent:
    """
    Lead Agent (Orquestador).

    Responsabilidades:
    - Analizar query del usuario
    - Crear plan de investigación
    - Asignar tareas a subagents
    - Sintetizar resultados
    - Detectar gaps y lanzar investigación adicional
    """

    def __init__(
        self,
        llm_client: Any,
        message_bus: MessageBus,
        memory: SharedMemory,
        agent_id: str = "lead_agent",
    ):
        """
        Inicializa el Lead Agent.

        Args:
            llm_client: Cliente LLM para generar respuestas
            message_bus: Bus de mensajes para comunicación
            memory: Memoria compartida
            agent_id: ID único del agente
        """
        self.llm = llm_client
        self.bus = message_bus
        self.memory = memory
        self.agent_id = agent_id

    async def create_research_plan(self, query: str) -> List[Task]:
        """
        Crea plan de investigación dividiendo la query en subtareas.

        Estrategia:
        1. Analiza complejidad de la query
        2. Divide en subtareas específicas
        3. Asigna roles y recursos a cada subtarea
        4. Define criterios de éxito

        Args:
            query: Query del usuario

        Returns:
            Lista de tareas para subagents
        """
        prompt = self._build_planning_prompt(query)

        # Aquí iría la llamada al LLM
        # response = await self.llm.complete(prompt)
        # tasks = self._parse_tasks_from_response(response)

        # Por ahora, ejemplo hardcodeado para demostración
        tasks = self._create_example_tasks(query)

        # Guardar plan en memoria compartida
        self.memory.store("research_plan", tasks)
        self.memory.store("original_query", query)

        return tasks

    def _build_planning_prompt(self, query: str) -> str:
        """Construye el prompt para planificación."""
        return f"""
Eres el Lead Agent de un sistema de investigación multi-agente.

Query del usuario: "{query}"

Analiza la query y crea un plan de investigación. Divide el problema
en 2-4 subtareas específicas que puedan ser investigadas en paralelo.

Para cada subtarea, define:
1. Descripción específica (qué investigar exactamente)
2. Rol del agente (researcher, analyzer, writer)
3. Herramientas a usar (web_search, academic_search, data_analysis)
4. Número máximo de búsquedas (3-15)
5. Criterios de éxito claros y medibles
6. Formato de output esperado

Reglas de scaling:
- Simple (fact-finding): 1 agente, 3-10 búsquedas
- Moderado (comparación): 2-3 agentes, 10-15 búsquedas c/u
- Complejo (análisis profundo): 4+ agentes, 15+ búsquedas c/u

IMPORTANTE: Evita instrucciones vagas. Sé específico sobre:
- Qué periodo de tiempo cubrir
- Qué regiones/mercados analizar
- Qué métricas cuantitativas buscar
- Qué tipo de fuentes priorizar

Output en formato JSON con estructura Task[].
"""

    def _create_example_tasks(self, query: str) -> List[Task]:
        """Crea tareas de ejemplo para demostración."""
        # Esta función sería reemplazada por parsing del LLM response
        return [
            Task(
                id=1,
                description=f"Investiga aspectos técnicos de: {query}",
                agent_role=AgentRole.RESEARCHER,
                tools=["web_search", "academic_search"],
                max_searches=12,
                success_criteria="Identificar 5+ puntos técnicos clave con datos",
                output_format="Lista estructurada con ejemplos específicos",
            ),
            Task(
                id=2,
                description=f"Analiza tendencias y datos cuantitativos de: {query}",
                agent_role=AgentRole.ANALYZER,
                tools=["web_search", "data_analysis"],
                max_searches=10,
                success_criteria="Gráficos/datos de adopción con fuentes",
                output_format="Análisis cuantitativo con estadísticas",
            ),
        ]

    async def synthesize_results(self, results: List[AgentResult]) -> str:
        """
        Sintetiza resultados de múltiples subagents.

        Estrategia:
        1. Combinar findings de todos los agentes
        2. Identificar temas comunes
        3. Resolver contradicciones (si existen)
        4. Detectar gaps de información
        5. Generar síntesis coherente

        Args:
            results: Resultados de investigación de cada subagent

        Returns:
            Síntesis final en markdown
        """
        # Combinar findings
        all_findings = self._combine_findings(results)

        # Combinar fuentes únicas
        all_sources = self._collect_unique_sources(results)

        # Detectar gaps
        gaps = self._detect_gaps(results)

        # Construir prompt de síntesis
        prompt = self._build_synthesis_prompt(all_findings, all_sources, gaps)

        # Aquí iría la llamada al LLM
        # synthesis = await self.llm.complete(prompt)

        # Por ahora, síntesis de ejemplo
        synthesis = self._create_example_synthesis(all_findings, all_sources, gaps)

        return synthesis

    def _combine_findings(self, results: List[AgentResult]) -> str:
        """Combina findings de múltiples resultados."""
        sections = []
        for r in results:
            sections.append(f"## {r.agent_role.value.title()} - Tarea {r.task_id}")
            sections.append(r.findings)
            sections.append("")  # Línea vacía

        return "\n".join(sections)

    def _collect_unique_sources(self, results: List[AgentResult]) -> List[str]:
        """Recolecta fuentes únicas de todos los resultados."""
        all_sources = []
        for r in results:
            all_sources.extend(r.sources)
        return list(set(all_sources))

    def _detect_gaps(self, results: List[AgentResult]) -> List[str]:
        """Detecta gaps de información reportados por agentes."""
        all_gaps = []
        for r in results:
            all_gaps.extend(r.gaps_identified)
        return list(set(all_gaps))

    def _build_synthesis_prompt(
        self, findings: str, sources: List[str], gaps: List[str]
    ) -> str:
        """Construye prompt para síntesis."""
        return f"""
Eres el Lead Agent. Sintetiza los siguientes resultados de investigación
en una respuesta coherente y completa.

RESULTADOS DE SUBAGENTS:
{findings}

FUENTES ({len(sources)} únicas):
{chr(10).join(f"- {s}" for s in sources)}

GAPS IDENTIFICADOS:
{chr(10).join(f"- {g}" for g in gaps) if gaps else "Ninguno"}

Genera:
1. Executive Summary (3-5 puntos clave)
2. Findings detallados por área
3. Conclusiones integradas
4. Limitaciones y gaps (si los hay)

Formato: Markdown profesional con secciones claras.
Si hay contradicciones entre fuentes, repórtalas explícitamente.
"""

    def _create_example_synthesis(
        self, findings: str, sources: List[str], gaps: List[str]
    ) -> str:
        """Crea síntesis de ejemplo."""
        return f"""# Síntesis de Investigación

## Executive Summary

- Hallazgo clave 1: [Basado en análisis de datos]
- Hallazgo clave 2: [Basado en investigación técnica]
- Hallazgo clave 3: [Tendencias identificadas]

## Findings Detallados

{findings}

## Fuentes Consultadas

{chr(10).join(f"- {s}" for s in sources)}

## Limitaciones

{chr(10).join(f"- {g}" for g in gaps) if gaps else "No se identificaron gaps significativos."}
"""


class SubAgent:
    """
    SubAgent (Worker).

    Responsabilidades:
    - Ejecutar investigación especializada en un subtema
    - Realizar búsquedas iterativas
    - Evaluar resultados (usando thinking)
    - Reportar findings al Lead Agent
    """

    def __init__(
        self,
        task: Task,
        llm_client: Any,
        message_bus: MessageBus,
        memory: SharedMemory,
    ):
        """
        Inicializa el SubAgent.

        Args:
            task: Tarea asignada
            llm_client: Cliente LLM
            message_bus: Bus de mensajes
            memory: Memoria compartida
        """
        self.task = task
        self.llm = llm_client
        self.bus = message_bus
        self.memory = memory
        self.agent_id = f"{task.agent_role.value}_{task.id}"
        self.private_memory: Dict[str, Any] = {}

    async def research(self) -> AgentResult:
        """
        Ejecuta investigación según la tarea asignada.

        Proceso:
        1. Analiza la tarea
        2. Planifica estrategia de búsqueda
        3. Ejecuta búsquedas iterativas
        4. Evalúa resultados (thinking)
        5. Identifica gaps
        6. Retorna findings

        Returns:
            Resultados de investigación
        """
        prompt = self._build_research_prompt()

        # Aquí iría:
        # 1. Llamadas iterativas al LLM con tool use
        # 2. Web searches (hasta max_searches)
        # 3. Evaluación de resultados con thinking

        # Por ahora, resultado de ejemplo
        result = self._create_example_result()

        # Reportar al Lead Agent vía message bus
        self.bus.publish(
            sender=self.agent_id,
            receiver="lead_agent",
            message=result,
            message_type="result",
        )

        return result

    def _build_research_prompt(self) -> str:
        """Construye prompt para investigación."""
        return f"""
Eres un {self.task.agent_role.value} especializado.

TAREA: {self.task.description}

HERRAMIENTAS DISPONIBLES: {", ".join(self.task.tools)}
MAX BÚSQUEDAS: {self.task.max_searches}

CRITERIOS DE ÉXITO: {self.task.success_criteria}
FORMATO ESPERADO: {self.task.output_format}

Investiga exhaustivamente usando las herramientas disponibles.

Usa <thinking> para:
- Evaluar calidad de cada fuente encontrada
- Decidir si necesitas más búsquedas
- Identificar gaps en la información

Si encuentras información contradictoria, reporta ambas versiones.
Si encuentras gaps, repórtalos explícitamente.

Itera hasta cumplir los criterios de éxito o agotar búsquedas.
"""

    def _create_example_result(self) -> AgentResult:
        """Crea resultado de ejemplo."""
        return AgentResult(
            task_id=self.task.id,
            agent_role=self.task.agent_role,
            findings=f"""### Findings para Tarea {self.task.id}

1. **Punto clave 1**: Descripción detallada con datos
2. **Punto clave 2**: Análisis de tendencias
3. **Punto clave 3**: Conclusiones basadas en evidencia

Estos findings están basados en {len(self.task.tools)} tipos de fuentes.
""",
            sources=[
                "https://example.com/source1",
                "https://example.com/source2",
                "https://example.com/academic-paper",
            ],
            confidence=0.85,
            gaps_identified=["Falta información sobre región LATAM"],
            metadata={"searches_performed": 8, "time_taken_seconds": 45},
        )


class MultiAgentResearchSystem:
    """
    Sistema completo de investigación multi-agente.

    Orquesta múltiples agentes especializados para resolver
    tareas complejas de investigación.
    """

    def __init__(self, llm_client: Any):
        """
        Inicializa el sistema multi-agente.

        Args:
            llm_client: Cliente LLM para todos los agentes
        """
        self.llm = llm_client
        self.message_bus = MessageBus()
        self.shared_memory = SharedMemory()
        self.lead_agent = LeadAgent(
            llm_client, self.message_bus, self.shared_memory
        )

    async def research(self, query: str) -> str:
        """
        Ejecuta investigación multi-agente completa.

        Proceso:
        1. Lead Agent crea plan de investigación
        2. Crea subagents especializados
        3. Subagents investigan en paralelo
        4. Lead Agent sintetiza resultados
        5. Retorna síntesis final

        Args:
            query: Query del usuario

        Returns:
            Síntesis final de investigación
        """
        print(f"🔍 Iniciando investigación multi-agente\n")
        print(f"Query: {query}\n")

        # Paso 1: Lead Agent crea plan
        print("📋 Lead Agent creando plan de investigación...")
        tasks = await self.lead_agent.create_research_plan(query)
        print(f"✅ Plan creado con {len(tasks)} tareas\n")

        for i, task in enumerate(tasks, 1):
            print(f"   Tarea {i}: {task.description[:60]}...")

        print()

        # Paso 2: Crear subagents
        print("🤖 Creando subagents especializados...")
        subagents = [
            SubAgent(task, self.llm, self.message_bus, self.shared_memory)
            for task in tasks
        ]
        print(f"✅ {len(subagents)} subagents creados\n")

        # Paso 3: Ejecutar investigación en paralelo
        print("⚡ Ejecutando investigación en paralelo...")
        results = await asyncio.gather(*[agent.research() for agent in subagents])
        print(f"✅ {len(results)} investigaciones completadas\n")

        # Paso 4: Sintetizar resultados
        print("📊 Sintetizando resultados...")
        synthesis = await self.lead_agent.synthesize_results(results)
        print("✅ Síntesis completada\n")

        return synthesis

    def export_trace(self) -> Dict[str, Any]:
        """
        Exporta trace completo de la ejecución.

        Returns:
            Diccionario con mensajes y memoria
        """
        return {
            "messages": self.message_bus.export_trace(),
            "memory": {k: self.shared_memory.retrieve(k) for k in self.shared_memory.keys()},
        }
