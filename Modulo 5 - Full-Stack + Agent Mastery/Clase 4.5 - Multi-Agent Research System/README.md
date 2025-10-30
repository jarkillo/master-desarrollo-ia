# Módulo 5 - Clase 4.5: Multi-Agent Research System

**Construye tu primer sistema de investigación multi-agente** - Aprende cómo múltiples agentes especializados colaboran para resolver tareas complejas que un solo agente no podría manejar eficientemente.

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [¿Qué es un Sistema Multi-Agente?](#qué-es-un-sistema-multi-agente)
3. [Arquitectura de Agentes Especializados](#arquitectura-de-agentes-especializados)
4. [Patrones de Comunicación entre Agentes](#patrones-de-comunicación-entre-agentes)
5. [Implementación Práctica](#implementación-práctica)
6. [Gestión de Memoria y Estado](#gestión-de-memoria-y-estado)
7. [Debugging y Observabilidad](#debugging-y-observabilidad)
8. [Proyecto: Sistema de Research para Documentación](#proyecto-sistema-de-research-para-documentación)
9. [Ejercicios Prácticos](#ejercicios-prácticos)
10. [Recursos Adicionales](#recursos-adicionales)

---

## Introducción

### El Problema que Resuelven los Sistemas Multi-Agente

Imagina que necesitas investigar **"El impacto de la IA en la industria automotriz"**.

**Enfoque tradicional (un solo agente)**:
```
Usuario → Claude → Busca todo → Procesa todo → Respuesta
```
**Problemas**:
- ❌ El agente se abruma con demasiados aspectos (manufactura, diseño, seguridad, regulaciones)
- ❌ Información superficial (toca muchos temas pero ninguno en profundidad)
- ❌ Trabajo duplicado (busca lo mismo varias veces desde diferentes ángulos)
- ❌ Resultados inconsistentes (pierde el hilo entre subtemas)

**Enfoque multi-agente**:
```
Usuario → Lead Agent (Orquestador)
              ↓
    ┌─────────┼─────────┬─────────┐
    ↓         ↓         ↓         ↓
Researcher  Researcher Researcher Researcher
(Manufactura) (Diseño) (Seguridad) (Regulaciones)
    ↓         ↓         ↓         ↓
    └─────────┼─────────┴─────────┘
              ↓
     CitationAgent (verifica fuentes)
              ↓
          Síntesis final
```

**Ventajas**:
- ✅ **Especialización**: Cada agente se enfoca en un subtema específico
- ✅ **Profundidad**: Investigación exhaustiva por área
- ✅ **Paralelización**: Agentes trabajan simultáneamente (90% más rápido)
- ✅ **División del trabajo**: Sin duplicación, sin overlap
- ✅ **Escalabilidad**: Agrega más agentes para tareas más complejas

**Datos reales del artículo de Anthropic**:
- 🚀 **90.2% mejor performance** en queries de breadth-first
- ⚡ **90% reducción en tiempo** gracias a paralelización
- 💰 **15x más tokens** pero con resultados cualitativamente superiores

---

## ¿Qué es un Sistema Multi-Agente?

### Definición

Un **sistema multi-agente** es una arquitectura donde múltiples agentes de IA especializados colaboran para resolver una tarea compleja que requiere:

1. **División de trabajo** en subtareas especializadas
2. **Comunicación** entre agentes para compartir resultados
3. **Coordinación** para evitar duplicación y conflictos
4. **Agregación** de resultados en una respuesta coherente

### Analogía: Equipo de Investigadores Académicos

| Elemento | En Academia | En Sistema Multi-Agente |
|----------|-------------|-------------------------|
| **Líder del proyecto** | Profesor principal | Lead Agent (Orchestrator) |
| **Investigadores** | Doctorandos especializados | Subagents (Workers) |
| **Área de expertise** | Cada uno investiga un subtema | Cada agente tiene un objetivo específico |
| **Comunicación** | Reuniones semanales | Message passing entre agentes |
| **Paper final** | Coautoría, todos contribuyen | Síntesis de resultados |
| **Revisión de fuentes** | Peer review | CitationAgent verifica credibilidad |

**Clave**: El profesor (Lead Agent) no investiga todo. Divide el problema, asigna subtemas, y coordina las contribuciones.

### Componentes Principales

```python
# Estructura conceptual de un sistema multi-agente

class MultiAgentSystem:
    """
    Sistema de investigación multi-agente.

    Componentes:
    - Lead Agent: Planifica y coordina
    - Subagents: Ejecutan investigación especializada
    - Message Bus: Comunicación entre agentes
    - Shared Memory: Estado compartido
    - Citation Verifier: Valida fuentes
    """

    def __init__(self):
        self.lead_agent = LeadAgent()
        self.subagents = []
        self.message_bus = MessageBus()
        self.shared_memory = SharedMemory()
        self.citation_verifier = CitationAgent()

    async def research(self, query: str) -> str:
        """
        Proceso de investigación multi-agente.

        1. Lead agent analiza query y planifica estrategia
        2. Lead agent crea subagents especializados
        3. Subagents investigan en paralelo
        4. Lead agent agrega resultados
        5. Citation verifier valida fuentes
        6. Retorna síntesis final
        """
        # Paso 1: Planificación
        plan = await self.lead_agent.create_research_plan(query)

        # Paso 2: Crear subagents especializados
        self.subagents = [
            SubAgent(task) for task in plan.tasks
        ]

        # Paso 3: Investigación paralela
        results = await asyncio.gather(*[
            agent.research() for agent in self.subagents
        ])

        # Paso 4: Agregar resultados
        synthesis = await self.lead_agent.synthesize(results)

        # Paso 5: Verificar citaciones
        verified = await self.citation_verifier.verify(synthesis)

        return verified
```

---

## Arquitectura de Agentes Especializados

### 1. Lead Agent (Orquestador)

**Responsabilidades**:
- 📋 Analizar la query del usuario
- 🎯 Desarrollar estrategia de investigación
- 🤝 Crear y asignar tareas a subagents
- 🔄 Esperar resultados (ejecución síncrona)
- 📊 Sintetizar resultados finales
- ⚠️ Detectar gaps y lanzar investigación adicional

**Características técnicas** (según Anthropic):
- Usa **extended thinking** para planificar
- Opera **síncronamente** (espera a que subagents terminen)
- Determina **resource allocation** (cuántos agentes, cuántas búsquedas)
- Maneja **context limits** guardando en memoria externa

**Ejemplo de prompt para Lead Agent**:
```
Eres el Lead Agent de un sistema de investigación.

Tu tarea: Analizar la siguiente query y crear un plan de investigación:
"{user_query}"

Genera un plan con:
1. Subtareas específicas (cada una asignable a un subagent)
2. Objetivos claros para cada subtarea
3. Formato de output esperado
4. Fuentes/herramientas a usar
5. Criterios de éxito

Reglas de scaling (según complejidad):
- Fact-finding simple: 1 agente, 3-10 tool calls
- Comparaciones: 2-4 subagents, 10-15 calls cada uno
- Research complejo: 10+ subagents con responsabilidades divididas

Output en formato JSON:
{
  "tasks": [
    {
      "id": 1,
      "description": "Investigar impacto de IA en manufactura automotriz",
      "agent_role": "Manufacturing Researcher",
      "tools": ["web_search", "academic_search"],
      "max_searches": 15,
      "success_criteria": "Identificar 5+ casos de uso con datos cuantitativos"
    },
    ...
  ],
  "estimated_complexity": "high",
  "estimated_agents": 4
}
```

### 2. Subagents (Workers)

**Responsabilidades**:
- 🔍 Ejecutar investigación especializada en un subtema
- 📚 Realizar búsquedas iterativas (web, academic papers, docs)
- 🧠 Usar **interleaved thinking** para evaluar resultados
- 🔄 Identificar gaps y ajustar búsquedas
- 📝 Retornar findings al Lead Agent

**Características técnicas**:
- Reciben **objetivos claros** del Lead Agent
- **Autonomía** para decidir estrategia de búsqueda
- **Iteran** hasta completar la tarea
- **Paralelización**: Pueden ejecutarse simultáneamente

**Ejemplo de instrucciones para Subagent**:
```
Eres un Subagent especializado en: {specialty}

Objetivo: {task_description}

Output esperado:
- Formato: {expected_format}
- Longitud: {expected_length}
- Fuentes: Mínimo {min_sources} fuentes creíbles

Herramientas disponibles:
{tools_list}

Guidance:
- Usa máximo {max_searches} búsquedas
- Prioriza fuentes académicas y oficiales sobre blogs
- Si encuentras información contradictoria, reporta ambas versiones
- Si no encuentras información suficiente, reporta el gap explícitamente

Criterios de éxito:
{success_criteria}

Itera hasta cumplir los criterios. Usa thinking para evaluar si necesitas más búsquedas.
```

**Anti-patrón (del artículo de Anthropic)**:
```
❌ MALO - Instrucción vaga:
"Research the semiconductor shortage"

Problema: Múltiples subagents investigaron el mismo tema
(shortage de 2021 en automotive + shortage de 2025 en chips)
sin división de trabajo clara.
```

```
✅ BUENO - Instrucción específica:
"Research the 2021 semiconductor shortage impact on automotive
manufacturing in North America. Focus on: production delays
(quantify in units), financial impact (revenue loss), and
recovery timeline. Time period: Jan 2021 - Dec 2022."

Resultado: Subagent sabe exactamente qué buscar, evita overlap.
```

### 3. Citation Agent (Verificador de Fuentes)

**Responsabilidades**:
- ✅ Verificar que todas las afirmaciones tengan fuentes
- 🔗 Validar que los URLs sean accesibles
- 📊 Evaluar credibilidad de fuentes (académicas > blogs)
- 🚫 Detectar claims sin evidencia
- 📝 Formatear citaciones correctamente

**Por qué es necesario**:
- Los subagents pueden "alucinar" fuentes
- Asegurar trazabilidad de información
- Cumplir estándares académicos/profesionales

**Ejemplo**:
```
Eres el Citation Agent. Valida las fuentes del siguiente texto:

"{synthesis_text}"

Por cada claim:
1. Verificar que tenga citación
2. Verificar que la fuente exista (URL accesible)
3. Evaluar credibilidad (academic > official > news > blog)
4. Si falta citación, marcar como [NEEDS CITATION]

Output:
- Texto corregido con citaciones verificadas
- Lista de fuentes no verificables
- Score de credibilidad (0.0-1.0)
```

---

## Patrones de Comunicación entre Agentes

### 1. Query Decomposition (Descomposición de Queries)

El Lead Agent divide queries complejas en subtareas discretas con instrucciones detalladas.

**Ejemplo real - Query compleja**:
```
"¿Cómo están las empresas automotrices adaptándose a la era de los vehículos eléctricos?"
```

**Descomposición por Lead Agent**:
```json
{
  "tasks": [
    {
      "id": 1,
      "subtask": "Inversión en infraestructura de carga",
      "agent_focus": "Investiga cuánto están invirtiendo las top 5 automotrices (Tesla, VW, GM, Ford, Toyota) en estaciones de carga. Datos: inversión USD, número de estaciones, timeline.",
      "output_format": "Tabla comparativa con datos cuantitativos"
    },
    {
      "id": 2,
      "subtask": "Desarrollo de baterías",
      "agent_focus": "Investiga innovaciones en tecnología de baterías: densidad energética (Wh/kg), tiempo de carga, vida útil (ciclos), costos (USD/kWh). Compara LFP vs NMC vs solid-state.",
      "output_format": "Análisis técnico con especificaciones"
    },
    {
      "id": 3,
      "subtask": "Adaptación de líneas de producción",
      "agent_focus": "Investiga cómo las plantas tradicionales están siendo retooled para EVs. Casos de estudio: tiempos de conversión, costos, desafíos laborales.",
      "output_format": "Narrativa con 3+ casos específicos"
    },
    {
      "id": 4,
      "subtask": "Regulaciones y subsidios",
      "agent_focus": "Mapea políticas gubernamentales que incentivan EVs por región (US, EU, China): subsidios, mandatos de ventas, prohibiciones de ICE.",
      "output_format": "Timeline de regulaciones 2020-2030"
    }
  ]
}
```

**Principio clave**: Instrucciones vagas → trabajo duplicado. Instrucciones específicas → eficiencia.

### 2. Result Synthesis (Síntesis de Resultados)

El Lead Agent agrega los findings de todos los subagents en una respuesta coherente.

**Pattern**:
```python
async def synthesize_results(self, subagent_results: List[AgentResult]) -> str:
    """
    Sintetiza resultados de múltiples subagents.

    Estrategia:
    1. Identificar temas comunes entre resultados
    2. Resolver contradicciones (si las hay)
    3. Llenar gaps (lanzar investigación adicional si es necesario)
    4. Estructurar narrativa coherente
    5. Agregar executive summary
    """
    synthesis_prompt = f"""
    Eres el Lead Agent. Sintetiza los siguientes resultados de investigación:

    {format_results(subagent_results)}

    Genera:
    1. Executive Summary (3-5 bullets)
    2. Findings detallados por área
    3. Conclusiones integradas
    4. Gaps identificados (si los hay)

    Si encuentras contradicciones entre fuentes, repórtalas explícitamente.
    """

    return await self.llm.complete(synthesis_prompt)
```

**Ciclo iterativo** (del artículo de Anthropic):
```
Lead Agent → Crea subagents → Subagents investigan → Lead sintetiza
     ↑                                                       ↓
     └────── ¿Gaps detectados? → Lanza nueva ronda ─────────┘
```

### 3. Parallel Execution (Ejecución Paralela)

**Dos tipos de paralelización** (según Anthropic):

**Tipo 1: Lead agent spawns múltiples subagents**
```python
# Lead Agent lanza 3-5 subagents simultáneamente
subagents = [
    SubAgent("Manufacturing Research"),
    SubAgent("Battery Technology"),
    SubAgent("Regulatory Landscape"),
]

# Ejecución paralela (asyncio.gather)
results = await asyncio.gather(*[
    agent.research() for agent in subagents
])

# Reducción de tiempo: ~90% (según Anthropic)
# Sequential: 15 min → Parallel: 1.5 min
```

**Tipo 2: Subagents usan múltiples tools en paralelo**
```python
# Cada subagent ejecuta 3+ tool calls simultáneamente
async def research(self):
    results = await asyncio.gather(
        self.web_search("EV battery technology 2024"),
        self.academic_search("lithium-ion energy density"),
        self.news_search("solid-state battery breakthroughs"),
    )
    return self.analyze(results)
```

**Impacto combinado**: Reducción dramática en tiempo total.

---

## Implementación Práctica

### Sistema Básico Multi-Agente (3 Agentes)

Vamos a implementar un sistema real de investigación con:
- 1 Lead Agent (orquestador)
- 2 Subagents (workers especializados)
- 1 Message Bus (comunicación)

**Archivo**: `multi_agent_system/core.py`

```python
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum
import asyncio

class AgentRole(str, Enum):
    """Roles de agentes en el sistema."""
    LEAD = "lead"
    RESEARCHER = "researcher"
    ANALYZER = "analyzer"
    WRITER = "writer"
    CITATION_VERIFIER = "citation_verifier"

@dataclass
class Task:
    """Tarea asignada a un subagent."""
    id: int
    description: str
    agent_role: AgentRole
    tools: List[str]
    max_searches: int
    success_criteria: str
    output_format: str

@dataclass
class AgentResult:
    """Resultado de investigación de un agente."""
    task_id: int
    agent_role: AgentRole
    findings: str
    sources: List[str]
    confidence: float  # 0.0-1.0
    gaps_identified: List[str]

class MessageBus:
    """Bus de comunicación entre agentes."""

    def __init__(self):
        self._messages: List[Dict[str, Any]] = []

    def publish(self, sender: str, receiver: str, message: Any):
        """Envía mensaje de un agente a otro."""
        self._messages.append({
            "sender": sender,
            "receiver": receiver,
            "message": message,
            "timestamp": asyncio.get_event_loop().time()
        })

    def get_messages(self, receiver: str) -> List[Dict[str, Any]]:
        """Obtiene mensajes para un agente específico."""
        return [m for m in self._messages if m["receiver"] == receiver]

class SharedMemory:
    """Memoria compartida entre agentes."""

    def __init__(self):
        self._data: Dict[str, Any] = {}

    def store(self, key: str, value: Any):
        """Almacena dato en memoria compartida."""
        self._data[key] = value

    def retrieve(self, key: str) -> Any:
        """Recupera dato de memoria compartida."""
        return self._data.get(key)

    def clear(self):
        """Limpia toda la memoria."""
        self._data.clear()

class LeadAgent:
    """
    Lead Agent (Orquestador).

    Responsabilidades:
    - Analizar query del usuario
    - Crear plan de investigación
    - Asignar tareas a subagents
    - Sintetizar resultados
    """

    def __init__(self, llm_client, message_bus: MessageBus, memory: SharedMemory):
        self.llm = llm_client
        self.bus = message_bus
        self.memory = memory

    async def create_research_plan(self, query: str) -> List[Task]:
        """
        Crea plan de investigación dividiendo la query en subtareas.

        Args:
            query: Query del usuario

        Returns:
            Lista de tareas para subagents
        """
        prompt = f"""
        Eres el Lead Agent de un sistema de investigación multi-agente.

        Query del usuario: "{query}"

        Analiza la query y crea un plan de investigación. Divide el problema
        en 2-4 subtareas específicas que puedan ser investigadas en paralelo.

        Para cada subtarea, define:
        1. Descripción específica (qué investigar exactamente)
        2. Rol del agente (researcher, analyzer)
        3. Herramientas a usar (web_search, academic_search)
        4. Número máximo de búsquedas (3-15)
        5. Criterios de éxito
        6. Formato de output esperado

        Reglas de scaling:
        - Simple (fact-finding): 1 agente, 3-10 búsquedas
        - Moderado (comparación): 2-3 agentes, 10-15 búsquedas c/u
        - Complejo (análisis profundo): 4+ agentes, 15+ búsquedas c/u

        Output en formato JSON.
        """

        # Aquí iría la llamada al LLM
        # response = await self.llm.complete(prompt)
        # tasks = parse_tasks_from_json(response)

        # Por ahora, ejemplo hardcodeado
        tasks = [
            Task(
                id=1,
                description="Investiga el impacto de IA en manufactura automotriz",
                agent_role=AgentRole.RESEARCHER,
                tools=["web_search", "academic_search"],
                max_searches=12,
                success_criteria="Identificar 5+ casos de uso con datos cuantitativos",
                output_format="Lista estructurada con ejemplos específicos"
            ),
            Task(
                id=2,
                description="Analiza tendencias en vehículos eléctricos 2020-2024",
                agent_role=AgentRole.ANALYZER,
                tools=["web_search", "data_analysis"],
                max_searches=10,
                success_criteria="Gráficos de adopción por región con datos",
                output_format="Análisis cuantitativo con visualizaciones"
            )
        ]

        # Guardar plan en memoria compartida
        self.memory.store("research_plan", tasks)

        return tasks

    async def synthesize_results(self, results: List[AgentResult]) -> str:
        """
        Sintetiza resultados de múltiples subagents.

        Args:
            results: Resultados de investigación de cada subagent

        Returns:
            Síntesis final
        """
        # Combinar findings
        all_findings = "\n\n".join([
            f"## {r.agent_role.value.title()} - Task {r.task_id}\n{r.findings}"
            for r in results
        ])

        # Combinar fuentes
        all_sources = []
        for r in results:
            all_sources.extend(r.sources)
        unique_sources = list(set(all_sources))

        prompt = f"""
        Eres el Lead Agent. Sintetiza los siguientes resultados de investigación
        en una respuesta coherente y completa.

        RESULTADOS DE SUBAGENTS:
        {all_findings}

        FUENTES:
        {chr(10).join(f"- {s}" for s in unique_sources)}

        Genera:
        1. Executive Summary (3-5 puntos clave)
        2. Findings detallados por área
        3. Conclusiones integradas
        4. Limitaciones y gaps (si los hay)

        Formato: Markdown profesional con secciones claras.
        """

        # Aquí iría la llamada al LLM
        # synthesis = await self.llm.complete(prompt)

        synthesis = f"""
        # Síntesis de Investigación

        ## Executive Summary
        - Hallazgo 1
        - Hallazgo 2
        - Hallazgo 3

        ## Findings Detallados
        {all_findings}

        ## Fuentes
        {chr(10).join(f"- {s}" for s in unique_sources)}
        """

        return synthesis

class SubAgent:
    """
    SubAgent (Worker).

    Responsabilidades:
    - Ejecutar investigación especializada
    - Reportar resultados al Lead Agent
    """

    def __init__(
        self,
        task: Task,
        llm_client,
        message_bus: MessageBus,
        memory: SharedMemory
    ):
        self.task = task
        self.llm = llm_client
        self.bus = message_bus
        self.memory = memory

    async def research(self) -> AgentResult:
        """
        Ejecuta investigación según la tarea asignada.

        Returns:
            Resultados de investigación
        """
        prompt = f"""
        Eres un {self.task.agent_role.value} especializado.

        TAREA: {self.task.description}

        HERRAMIENTAS DISPONIBLES: {", ".join(self.task.tools)}
        MAX BÚSQUEDAS: {self.task.max_searches}

        CRITERIOS DE ÉXITO: {self.task.success_criteria}
        FORMATO ESPERADO: {self.task.output_format}

        Investiga exhaustivamente usando las herramientas disponibles.
        Usa thinking interleaved para evaluar si necesitas más búsquedas.

        Si encuentras gaps en la información, repórtalos explícitamente.
        """

        # Aquí iría:
        # 1. Llamadas iterativas al LLM con tool use
        # 2. Web searches
        # 3. Evaluación de resultados

        # Por ahora, resultado de ejemplo
        result = AgentResult(
            task_id=self.task.id,
            agent_role=self.task.agent_role,
            findings=f"Findings para tarea {self.task.id}...",
            sources=[
                "https://example.com/source1",
                "https://example.com/source2"
            ],
            confidence=0.85,
            gaps_identified=["Falta información sobre región LATAM"]
        )

        # Reportar al Lead Agent vía message bus
        self.bus.publish(
            sender=f"{self.task.agent_role.value}_{self.task.id}",
            receiver="lead_agent",
            message=result
        )

        return result

class MultiAgentResearchSystem:
    """Sistema completo de investigación multi-agente."""

    def __init__(self, llm_client):
        self.llm = llm_client
        self.message_bus = MessageBus()
        self.shared_memory = SharedMemory()
        self.lead_agent = LeadAgent(llm_client, self.message_bus, self.shared_memory)

    async def research(self, query: str) -> str:
        """
        Ejecuta investigación multi-agente completa.

        Args:
            query: Query del usuario

        Returns:
            Síntesis final de investigación
        """
        print(f"🔍 Iniciando investigación: {query}\n")

        # Paso 1: Lead Agent crea plan
        print("📋 Lead Agent creando plan de investigación...")
        tasks = await self.lead_agent.create_research_plan(query)
        print(f"✅ Plan creado con {len(tasks)} tareas\n")

        # Paso 2: Crear subagents
        print("🤖 Creando subagents especializados...")
        subagents = [
            SubAgent(task, self.llm, self.message_bus, self.shared_memory)
            for task in tasks
        ]
        print(f"✅ {len(subagents)} subagents creados\n")

        # Paso 3: Ejecutar investigación en paralelo
        print("⚡ Ejecutando investigación en paralelo...")
        results = await asyncio.gather(*[
            agent.research() for agent in subagents
        ])
        print(f"✅ Investigación completada\n")

        # Paso 4: Sintetizar resultados
        print("📊 Sintetizando resultados...")
        synthesis = await self.lead_agent.synthesize_results(results)
        print("✅ Síntesis completada\n")

        return synthesis
```

Este código implementa los conceptos clave del artículo de Anthropic. En las próximas secciones veremos cómo expandirlo con memoria persistente, debugging, y el proyecto completo.

---

## Gestión de Memoria y Estado

### Problema: Context Limits

**Desafío**: Claude tiene un límite de 200,000 tokens. En investigaciones largas, el contexto puede excederse.

**Solución del artículo de Anthropic**:
1. **External Memory**: Lead Agent guarda el plan de investigación en memoria externa
2. **Context Truncation**: Cuando se acerca al límite, trunca conservando lo esencial
3. **Stateful Handoffs**: Nuevos subagents heredan contexto desde memoria externa

### Implementación de Memoria Persistente

```python
import json
from pathlib import Path
from datetime import datetime

class PersistentMemory(SharedMemory):
    """
    Memoria compartida con persistencia en disco.

    Permite:
    - Guardar estado entre sesiones
    - Recuperarse de errores
    - Auditar decisiones de agentes
    """

    def __init__(self, storage_dir: str = "./memory"):
        super().__init__()
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    def store(self, key: str, value: Any):
        """Almacena en memoria y persiste a disco."""
        super().store(key, value)

        # Persistir a disco
        file_path = self.storage_dir / f"{self.session_id}_{key}.json"
        with open(file_path, 'w') as f:
            json.dump({
                "key": key,
                "value": value,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2, default=str)

    def retrieve(self, key: str) -> Any:
        """Recupera de memoria o disco."""
        # Intentar memoria primero
        value = super().retrieve(key)
        if value is not None:
            return value

        # Si no está en memoria, buscar en disco
        file_path = self.storage_dir / f"{self.session_id}_{key}.json"
        if file_path.exists():
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data["value"]

        return None

    def checkpoint(self, checkpoint_name: str):
        """Crea checkpoint del estado actual."""
        checkpoint_data = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "state": self._data
        }

        checkpoint_path = self.storage_dir / f"checkpoint_{checkpoint_name}.json"
        with open(checkpoint_path, 'w') as f:
            json.dump(checkpoint_data, f, indent=2, default=str)

        print(f"✅ Checkpoint guardado: {checkpoint_name}")

    def restore_checkpoint(self, checkpoint_name: str):
        """Restaura estado desde checkpoint."""
        checkpoint_path = self.storage_dir / f"checkpoint_{checkpoint_name}.json"

        if not checkpoint_path.exists():
            raise FileNotFoundError(f"Checkpoint no encontrado: {checkpoint_name}")

        with open(checkpoint_path, 'r') as f:
            checkpoint_data = json.load(f)

        self._data = checkpoint_data["state"]
        print(f"✅ Checkpoint restaurado: {checkpoint_name}")
```

### Memory Compartida vs Privada

**Memory Compartida** (SharedMemory):
- ✅ Todos los agentes pueden leer/escribir
- ✅ Útil para: plan de investigación, resultados agregados
- ❌ Riesgo: conflictos si múltiples agentes escriben simultáneamente

**Memory Privada** (por agente):
- ✅ Cada agente tiene su propio contexto
- ✅ Útil para: notas de investigación, búsquedas intermedias
- ✅ Sin conflictos

**Ejemplo**:
```python
class SubAgent:
    def __init__(self, task, llm, message_bus, shared_memory):
        self.task = task
        self.llm = llm
        self.bus = message_bus
        self.shared_memory = shared_memory  # Compartida
        self.private_memory = {}  # Privada

    async def research(self):
        # Escribir en memoria privada (solo este agente)
        self.private_memory["search_history"] = []

        # Leer de memoria compartida (todos los agentes)
        research_plan = self.shared_memory.retrieve("research_plan")

        # ...
```

---

## Debugging y Observabilidad

### Desafío

**Problema**: En un sistema multi-agente, cuando algo falla, ¿cómo sabes qué agente causó el error?

**Solución**: Logging estructurado + tracing de decisiones.

### Logging Estructurado

```python
import logging
import json
from datetime import datetime

class AgentLogger:
    """Logger especializado para sistemas multi-agente."""

    def __init__(self, agent_id: str, log_file: str = "agents.log"):
        self.agent_id = agent_id
        self.logger = logging.getLogger(f"agent.{agent_id}")

        # Handler para archivo JSON
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log_decision(self, decision: str, context: Dict[str, Any]):
        """Registra una decisión del agente."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": self.agent_id,
            "event_type": "decision",
            "decision": decision,
            "context": context
        }
        self.logger.info(json.dumps(log_entry))

    def log_tool_call(self, tool: str, params: Dict[str, Any], result: Any):
        """Registra uso de herramienta."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": self.agent_id,
            "event_type": "tool_call",
            "tool": tool,
            "params": params,
            "result_preview": str(result)[:200]  # Truncar
        }
        self.logger.info(json.dumps(log_entry))

    def log_error(self, error: Exception, context: Dict[str, Any]):
        """Registra error."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": self.agent_id,
            "event_type": "error",
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context
        }
        self.logger.error(json.dumps(log_entry))
```

**Uso**:
```python
class SubAgent:
    def __init__(self, task, llm, message_bus, shared_memory):
        # ...
        self.logger = AgentLogger(f"{task.agent_role}_{task.id}")

    async def research(self):
        self.logger.log_decision(
            "Starting research",
            {"task_id": self.task.id, "description": self.task.description}
        )

        # Simular búsqueda
        self.logger.log_tool_call(
            "web_search",
            {"query": "IA in automotive"},
            {"results": 10, "sources": ["..."]}
        )

        # ...
```

### Tracing de Interacciones

**Visualizar flujo de mensajes** entre agentes:

```python
class MessageBus:
    def __init__(self):
        self._messages = []
        self.trace_file = "message_trace.json"

    def publish(self, sender: str, receiver: str, message: Any):
        msg_entry = {
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "receiver": receiver,
            "message_type": type(message).__name__,
            "message_preview": str(message)[:100]
        }

        self._messages.append(msg_entry)

        # Persistir trace
        with open(self.trace_file, 'a') as f:
            f.write(json.dumps(msg_entry) + "\n")

    def export_trace(self) -> str:
        """Exporta trace completo para análisis."""
        return json.dumps(self._messages, indent=2)
```

**Análisis post-mortem**:
```bash
# Ver todos los mensajes
cat message_trace.json | jq '.sender, .receiver, .message_type'

# Ver mensajes de un agente específico
cat message_trace.json | jq 'select(.sender == "researcher_1")'
```

---

## Proyecto: Sistema de Research para Documentación

### Objetivo

Construir un sistema multi-agente que **genere documentación técnica completa** para un proyecto de código.

**Input**: Repositorio de código (ej: FastAPI project)
**Output**: Documentación markdown profesional con:
- README.md
- API_REFERENCE.md
- ARCHITECTURE.md
- DEPLOYMENT.md

### Agentes Especializados

1. **CodeAnalyzer Agent**: Analiza el código fuente
2. **APIDocumenter Agent**: Genera documentación de API
3. **ArchitectureMapper Agent**: Crea diagramas de arquitectura
4. **DeploymentGuide Agent**: Escribe guía de deployment
5. **WriterAgent**: Redacta documentación final

### Implementación

Ver carpeta `ejemplos/documentation_system/` para código completo.

**Ejemplo de ejecución**:
```python
# main.py
from multi_agent_system.documentation import DocumentationSystem

async def main():
    system = DocumentationSystem(llm_client)

    docs = await system.generate_documentation(
        repo_path="./my-fastapi-project",
        output_dir="./docs"
    )

    print(f"✅ Documentación generada en: {docs.output_dir}")

asyncio.run(main())
```

**Output esperado**:
```
docs/
├── README.md (overview del proyecto)
├── API_REFERENCE.md (endpoints documentados)
├── ARCHITECTURE.md (diagramas + decisiones)
└── DEPLOYMENT.md (guía de deployment)
```

---

## Ejercicios Prácticos

### Ejercicio 1: Sistema de Research de 2 Agentes

**Objetivo**: Implementar un sistema simple con 1 Lead Agent + 1 Subagent.

**Task**: Investiga "Lenguajes de programación más populares en 2024"

**Requisitos**:
- Lead Agent divide en 2 subtareas
- 2 Subagents investigan en paralelo
- Lead Agent sintetiza resultados

**Criterio de éxito**: Respuesta con datos de al menos 2 fuentes distintas.

### Ejercicio 2: Sistema con Citation Verifier

**Objetivo**: Agregar validación de fuentes.

**Task**: Usa el sistema del Ejercicio 1, pero agrega un CitationAgent que:
- Verifica que cada claim tenga fuente
- Valida URLs accesibles
- Genera score de credibilidad

### Ejercicio 3: Sistema de Documentación (Proyecto Final)

**Objetivo**: Implementar el sistema completo de documentación técnica.

**Task**: Genera documentación para un proyecto FastAPI real.

**Requisitos**:
- 5 agentes especializados
- Memoria persistente (checkpoints)
- Logging estructurado
- Output en markdown profesional

---

## Recursos Adicionales

### Artículos de Anthropic (Lectura Obligatoria)

1. **[Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)** ⭐ BASE DE ESTA CLASE
   - Arquitectura real de Anthropic
   - Patrones de comunicación
   - Métricas de performance

2. **[Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)**
   - Memory management
   - Context truncation strategies

3. **[Agent Skills Framework](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)**
   - Composición de habilidades
   - Especialización de agentes

### Frameworks y Herramientas

- **[LangGraph](https://github.com/langchain-ai/langgraph)**: Framework para sistemas multi-agente
- **[AutoGen](https://microsoft.github.io/autogen/)**: Microsoft's multi-agent framework
- **[CrewAI](https://github.com/joaomdmoura/crewAI)**: Framework para equipos de agentes

### Papers Académicos

- "Communicating Agent Architectures" (Multi-agent systems)
- "Hierarchical Reinforcement Learning with Subgoals" (Task decomposition)

---

## Glosario

- **Lead Agent**: Agente orquestador que planifica y coordina
- **Subagent**: Agente worker especializado en una subtarea
- **Query Decomposition**: Dividir query compleja en subtareas
- **Result Synthesis**: Agregar resultados de múltiples agentes
- **Extended Thinking**: Modo de razonamiento profundo para planificación
- **Interleaved Thinking**: Razonamiento intercalado durante ejecución
- **Message Passing**: Comunicación entre agentes via mensajes
- **Shared Memory**: Memoria accesible por todos los agentes
- **Private Memory**: Memoria exclusiva de un agente
- **Citation Agent**: Agente que verifica fuentes y citaciones
- **Breadth-first Search**: Estrategia de búsqueda amplia antes de profunda
- **Token Budget**: Límite de tokens en contexto del LLM
- **Context Truncation**: Reducir contexto para evitar exceder límite
- **Checkpoint**: Snapshot del estado del sistema para recuperación

---

## Reflexión Final

Al completar esta clase, deberías poder responder:

1. **¿Cuándo usar multi-agente vs un solo agente?**
   - Multi-agente: Tareas complejas que requieren especialización
   - Single-agente: Tareas simples, lineales

2. **¿Cuál es el trade-off principal?**
   - ✅ Mayor calidad y profundidad
   - ❌ Mayor costo en tokens (15x según Anthropic)
   - ✅ Pero: 90.2% mejor performance en tareas complejas

3. **¿Cómo evitar trabajo duplicado entre agentes?**
   - Instrucciones específicas (no vagas)
   - División clara de responsabilidades
   - Lead Agent coordina y evita overlap

4. **¿Qué aprendiste sobre coordinación?**
   - La coordinación es el reto principal
   - Message passing debe ser claro
   - Memoria compartida requiere gestión cuidadosa

---

**Siguiente clase**: [Clase 5 - Agent Orchestration Mastery](../Clase%205%20-%20Agent%20Orchestration%20Mastery/README.md) - Aplicarás estos conceptos para orquestar equipos completos de agentes en proyectos reales.

**Clase anterior**: [Clase 4 - Despliegue Full-Stack](../Clase%204%20-%20Despliegue%20Full-Stack/README.md)

---

**🎯 Logros de esta clase**:
- ✅ Entiendes arquitectura multi-agente
- ✅ Puedes dividir tareas complejas en subtareas
- ✅ Implementaste sistema de research básico
- ✅ Conoces patrones de comunicación entre agentes
- ✅ Sabes gestionar memoria y estado
- ✅ Puedes debuggear sistemas multi-agente
