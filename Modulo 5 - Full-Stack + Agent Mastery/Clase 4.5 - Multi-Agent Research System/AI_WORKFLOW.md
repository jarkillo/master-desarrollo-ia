# AI Workflow - Multi-Agent Research System

**70% del contenido de esta clase involucra IA** - Este archivo documenta cómo usar agentes de IA para construir, mejorar y debuggear sistemas multi-agente.

## 📋 Tabla de Contenidos

1. [Usar IA para Diseñar Arquitectura Multi-Agente](#usar-ia-para-diseñar-arquitectura-multi-agente)
2. [Generar Agentes Especializados con IA](#generar-agentes-especializados-con-ia)
3. [IA para Optimizar Comunicación entre Agentes](#ia-para-optimizar-comunicación-entre-agentes)
4. [Debuggear Sistemas Multi-Agente con IA](#debuggear-sistemas-multi-agente-con-ia)
5. [Testing de Sistemas Multi-Agente con IA](#testing-de-sistemas-multi-agente-con-ia)
6. [Refactoring Guiado por IA](#refactoring-guiado-por-ia)
7. [Ejercicios Prácticos con IA](#ejercicios-prácticos-con-ia)

---

## Usar IA para Diseñar Arquitectura Multi-Agente

### Prompt 1: Analizar Query y Proponer Arquitectura

**Objetivo**: Usar IA para analizar una query compleja y proponer la mejor arquitectura de agentes.

**Prompt**:
```
Actúa como un arquitecto de sistemas multi-agente experto.

QUERY DEL USUARIO:
"Necesito investigar el impacto de la inteligencia artificial en tres industrias:
automotive, healthcare y finance. Para cada industria, quiero conocer: casos de
uso actuales, ROI promedio, riesgos regulatorios, y predicciones 2025-2030."

TAREA:
1. Analiza la complejidad de esta query
2. Propone una arquitectura de agentes óptima
3. Define roles específicos para cada agente
4. Especifica cómo se comunicarán los agentes
5. Estima recursos necesarios (tokens, tiempo, búsquedas)

FORMATO DE OUTPUT:
```json
{
  "complexity_analysis": {
    "score": 1-10,
    "rationale": "Por qué es compleja",
    "dimensions": ["breadth", "depth", "cross-domain"]
  },
  "proposed_architecture": {
    "lead_agent": {
      "role": "Orchestrator",
      "responsibilities": []
    },
    "subagents": [
      {
        "id": 1,
        "role": "Industry Researcher",
        "specialty": "Automotive + AI",
        "tasks": [],
        "tools": ["web_search", "academic_search"],
        "max_searches": 15
      },
      ...
    ],
    "communication_pattern": "parallel | sequential | hybrid"
  },
  "resource_estimation": {
    "total_agents": 7,
    "estimated_tokens": 150000,
    "estimated_time_minutes": 5,
    "estimated_cost_usd": 3.50
  }
}
```

IMPORTANTE: Prioriza eficiencia. No crear más agentes de los necesarios.
```

**Uso**:
```python
# Copiar prompt a Claude Code y pegar tu query específica
# Claude generará arquitectura completa que puedes implementar
```

**Ejemplo de Output**:
```json
{
  "complexity_analysis": {
    "score": 8,
    "rationale": "Query cubre 3 industrias × 4 dimensiones = 12 subtareas. Requiere tanto breadth (múltiples industrias) como depth (análisis detallado por dimensión)",
    "dimensions": ["breadth", "depth", "cross-domain", "temporal"]
  },
  "proposed_architecture": {
    "lead_agent": {
      "role": "Research Orchestrator",
      "responsibilities": [
        "Dividir query en 12 subtareas (3 industrias × 4 dimensiones)",
        "Asignar subtareas a agentes especializados",
        "Sintetizar resultados cruzando industrias",
        "Identificar patterns comunes entre industrias"
      ]
    },
    "subagents": [
      {
        "id": 1,
        "role": "Automotive AI Researcher",
        "specialty": "AI en automotive (todos los aspectos)",
        "tasks": [
          "Casos de uso AI en automotive 2024",
          "ROI promedio de AI implementations",
          "Riesgos regulatorios (seguridad, privacidad)",
          "Predicciones 2025-2030"
        ],
        "tools": ["web_search", "academic_search", "industry_reports"],
        "max_searches": 20
      },
      {
        "id": 2,
        "role": "Healthcare AI Researcher",
        "specialty": "AI en healthcare",
        "tasks": ["Similar a automotive pero healthcare"],
        "tools": ["web_search", "academic_search", "medical_databases"],
        "max_searches": 20
      },
      {
        "id": 3,
        "role": "Finance AI Researcher",
        "specialty": "AI en finance/fintech",
        "tasks": ["Similar pero finance"],
        "tools": ["web_search", "financial_databases"],
        "max_searches": 20
      },
      {
        "id": 4,
        "role": "Cross-Industry Analyst",
        "specialty": "Análisis comparativo entre industrias",
        "tasks": [
          "Comparar ROI entre industrias",
          "Identificar patterns regulatorios comunes",
          "Sintetizar predicciones cross-industry"
        ],
        "tools": ["data_analysis"],
        "max_searches": 10
      }
    ],
    "communication_pattern": "hybrid",
    "explanation": "Fase 1: 3 industry researchers trabajan en PARALELO. Fase 2: Cross-Industry Analyst trabaja SECUENCIALMENTE después de recibir sus resultados."
  },
  "resource_estimation": {
    "total_agents": 4,
    "estimated_tokens": 120000,
    "estimated_time_minutes": 3,
    "estimated_cost_usd": 2.80,
    "parallelization_speedup": "90% faster vs sequential"
  }
}
```

---

## Generar Agentes Especializados con IA

### Prompt 2: Generar SubAgent con Especialización

**Objetivo**: Usar IA para generar código completo de un SubAgent especializado.

**Prompt**:
```
Actúa como un desarrollador Python experto en sistemas multi-agente.

TAREA: Genera un SubAgent especializado con las siguientes características:

ESPECIALIZACIÓN:
- Nombre: ResearchAgent para Healthcare AI
- Expertise: Investigación de aplicaciones de IA en healthcare
- Fuentes prioritarias: PubMed, FDA reports, hospital case studies

CAPACIDADES REQUERIDAS:
1. Búsqueda iterativa en PubMed (academic papers)
2. Análisis de aprobaciones FDA (regulatory compliance)
3. Recolección de case studies de hospitales
4. Evaluación de credibilidad de fuentes (academic > official > news > blog)
5. Detección de claims médicos que requieren validación adicional

HERRAMIENTAS DISPONIBLES:
- web_search(query: str) -> List[Result]
- academic_search(query: str, database: str) -> List[Paper]
- extract_statistics(text: str) -> Dict[str, float]

GENERA:
1. Clase Python completa para HealthcareAIResearchAgent
2. Método research() que implementa estrategia de búsqueda
3. Método _evaluate_source_credibility(source) que asigna score 0.0-1.0
4. Método _detect_medical_claims(text) que identifica claims que necesitan validación
5. Type hints completos
6. Docstrings detallados

IMPORTANTE:
- Hereda de SubAgent base class
- Usa async/await para búsquedas paralelas
- Implementa thinking interleaved para decidir si hacer más búsquedas
- Retorna AgentResult con findings, sources, confidence, gaps_identified
```

**Uso**:
```python
# Claude generará código completo que puedes copiar a tu proyecto
# El agente estará optimizado para la especialización solicitada
```

**Ejemplo de Output** (código generado por IA):
```python
from typing import List, Dict, Any
from multi_agent_system import SubAgent, Task, AgentResult, AgentRole

class HealthcareAIResearchAgent(SubAgent):
    """
    Agente especializado en investigación de AI en healthcare.

    Fuentes prioritarias:
    - PubMed (academic papers)
    - FDA reports (regulatory)
    - Hospital case studies

    Expertise:
    - Aplicaciones clínicas de AI
    - Aprobaciones regulatorias
    - ROI en implementaciones hospitalarias
    """

    def __init__(self, task: Task, llm_client, message_bus, memory):
        super().__init__(task, llm_client, message_bus, memory)
        self.source_priority = {
            "pubmed": 1.0,
            "fda.gov": 0.95,
            "nejm.org": 0.95,
            "hospital_case_study": 0.85,
            "news": 0.6,
            "blog": 0.3
        }

    async def research(self) -> AgentResult:
        """
        Ejecuta investigación especializada en healthcare AI.

        Estrategia:
        1. Búsqueda en PubMed (papers académicos)
        2. Búsqueda en FDA (aprobaciones regulatorias)
        3. Case studies de hospitales
        4. Análisis cruzado de fuentes
        5. Validación de claims médicos
        """
        findings = []
        sources = []
        searches_performed = 0

        # Fase 1: Academic research (PubMed)
        academic_results = await self._search_pubmed()
        findings.extend(self._extract_findings(academic_results, "academic"))
        sources.extend(academic_results)
        searches_performed += 1

        # Thinking: ¿Suficiente evidencia académica?
        if len(academic_results) < 3:
            # Búsqueda adicional con términos alternativos
            alt_results = await self._search_pubmed(alternative_terms=True)
            findings.extend(self._extract_findings(alt_results, "academic"))
            sources.extend(alt_results)
            searches_performed += 1

        # Fase 2: Regulatory compliance (FDA)
        fda_results = await self._search_fda_approvals()
        findings.extend(self._extract_findings(fda_results, "regulatory"))
        sources.extend(fda_results)
        searches_performed += 1

        # Fase 3: Hospital case studies
        case_studies = await self._search_case_studies()
        findings.extend(self._extract_findings(case_studies, "practical"))
        sources.extend(case_studies)
        searches_performed += 1

        # Evaluación de credibilidad total
        avg_credibility = self._calculate_avg_credibility(sources)

        # Detectar claims que necesitan validación
        all_text = " ".join([f["text"] for f in findings])
        medical_claims = self._detect_medical_claims(all_text)

        # Identificar gaps
        gaps = self._identify_gaps(findings)

        # Construir resultado
        result = AgentResult(
            task_id=self.task.id,
            agent_role=self.task.agent_role,
            findings=self._format_findings(findings),
            sources=[s["url"] for s in sources],
            confidence=avg_credibility,
            gaps_identified=gaps,
            metadata={
                "searches_performed": searches_performed,
                "medical_claims_found": len(medical_claims),
                "source_breakdown": self._source_breakdown(sources)
            }
        )

        return result

    async def _search_pubmed(self, alternative_terms: bool = False) -> List[Dict]:
        """Busca en PubMed papers relevantes."""
        query = self.task.description
        if alternative_terms:
            query = self._generate_alternative_query(query)

        # Aquí iría la llamada real a PubMed API
        # results = await self.tools.academic_search(query, database="pubmed")

        # Por ahora, resultado de ejemplo
        return [
            {
                "title": "AI in radiology: systematic review",
                "url": "https://pubmed.ncbi.nlm.nih.gov/12345678",
                "source_type": "pubmed",
                "year": 2024
            }
        ]

    async def _search_fda_approvals(self) -> List[Dict]:
        """Busca aprobaciones FDA de AI/ML medical devices."""
        # Implementación de búsqueda en FDA
        return [
            {
                "title": "FDA approves AI algorithm for diabetic retinopathy",
                "url": "https://www.fda.gov/...",
                "source_type": "fda.gov",
                "year": 2023
            }
        ]

    async def _search_case_studies(self) -> List[Dict]:
        """Busca case studies de hospitales."""
        # Implementación de búsqueda de case studies
        return []

    def _evaluate_source_credibility(self, source: Dict) -> float:
        """
        Evalúa credibilidad de una fuente.

        Args:
            source: Diccionario con info de fuente

        Returns:
            Score 0.0-1.0 (1.0 = máxima credibilidad)
        """
        source_type = source.get("source_type", "unknown")
        base_score = self.source_priority.get(source_type, 0.5)

        # Bonus por fuentes recientes
        year = source.get("year", 2020)
        if year >= 2023:
            base_score += 0.05

        # Penalty por fuentes muy antiguas
        if year < 2020:
            base_score -= 0.1

        return max(0.0, min(1.0, base_score))

    def _detect_medical_claims(self, text: str) -> List[str]:
        """
        Detecta claims médicos que requieren validación.

        Claims médicos típicos:
        - "reduces mortality by X%"
        - "improves diagnosis accuracy"
        - "FDA approved for..."

        Returns:
            Lista de claims encontrados
        """
        medical_claim_patterns = [
            r"reduces? (?:mortality|deaths?) by (\d+%)",
            r"improves? (?:diagnosis|accuracy|sensitivity) (?:by|to) (\d+%)",
            r"FDA approved",
            r"clinical trial shows",
            r"proven to (?:reduce|improve|increase)"
        ]

        # Aquí iría regex matching
        # Por ahora, ejemplo
        return ["Claim: AI reduces diagnostic errors by 30% (needs validation)"]

    def _identify_gaps(self, findings: List[Dict]) -> List[str]:
        """Identifica gaps en la investigación."""
        gaps = []

        # Verificar si tenemos info de todas las áreas
        areas = ["clinical_use", "regulatory", "roi", "risks"]
        covered_areas = set([f["area"] for f in findings])

        for area in areas:
            if area not in covered_areas:
                gaps.append(f"Falta información sobre: {area}")

        return gaps

    def _calculate_avg_credibility(self, sources: List[Dict]) -> float:
        """Calcula credibilidad promedio de todas las fuentes."""
        if not sources:
            return 0.5

        scores = [self._evaluate_source_credibility(s) for s in sources]
        return sum(scores) / len(scores)

    def _format_findings(self, findings: List[Dict]) -> str:
        """Formatea findings en markdown estructurado."""
        output = "### Healthcare AI Findings\n\n"

        # Agrupar por área
        by_area = {}
        for f in findings:
            area = f.get("area", "general")
            if area not in by_area:
                by_area[area] = []
            by_area[area].append(f["text"])

        for area, texts in by_area.items():
            output += f"#### {area.replace('_', ' ').title()}\n"
            for text in texts:
                output += f"- {text}\n"
            output += "\n"

        return output
```

**Este código generado por IA es directamente usable en tu proyecto.**

---

## IA para Optimizar Comunicación entre Agentes

### Prompt 3: Optimizar Message Passing

**Objetivo**: Usar IA para diseñar protocolos de comunicación óptimos.

**Prompt**:
```
Actúa como un experto en sistemas distribuidos y comunicación entre agentes.

CONTEXTO:
Tengo un sistema multi-agente con:
- 1 Lead Agent (orquestador)
- 5 SubAgents (workers)
- MessageBus para comunicación

PROBLEMA ACTUAL:
Los agentes envían demasiados mensajes redundantes:
- SubAgent A termina tarea → envía resultado a Lead
- Lead recibe resultado → pide confirmación a SubAgent A
- SubAgent A confirma → Lead procesa
- Repeat para 5 agentes → 15 mensajes totales

OBJETIVO:
Rediseñar protocolo de comunicación para minimizar mensajes mientras manteniendo
observabilidad completa.

RESTRICCIONES:
- Lead Agent debe saber cuando todos los subagents terminaron
- Cada mensaje debe ser loggeable para debugging
- No usar polling (ineficiente)

GENERA:
1. Protocolo optimizado de comunicación
2. Tipos de mensajes necesarios (enum)
3. Formato de cada tipo de mensaje
4. Diagrama de secuencia (mermaid)
5. Implementación en Python

Calcula: % de reducción en mensajes vs protocolo actual
```

**Ejemplo de Output generado por IA**:

```python
from enum import Enum
from typing import Any, Dict
from dataclasses import dataclass
from datetime import datetime

class MessageType(Enum):
    """Tipos de mensajes en el protocolo optimizado."""
    TASK_ASSIGNED = "task_assigned"       # Lead → SubAgent
    TASK_COMPLETED = "task_completed"     # SubAgent → Lead
    ERROR = "error"                       # Cualquiera → Lead
    SHUTDOWN = "shutdown"                 # Lead → Todos

@dataclass
class OptimizedMessage:
    """Mensaje optimizado con info esencial."""
    msg_type: MessageType
    sender: str
    receiver: str
    payload: Any
    timestamp: str = None

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

class OptimizedMessageBus:
    """
    MessageBus optimizado con protocolo eficiente.

    Optimizaciones:
    - Sin confirmaciones redundantes (fire-and-forget para resultados)
    - Lead usa async/await para esperar resultados (no polling)
    - Mensajes estructurados con payload tipado
    - Subscribe pattern para notificaciones
    """

    def __init__(self):
        self._messages = []
        self._subscribers = {}
        self._result_futures = {}  # Para async/await

    def publish(self, message: OptimizedMessage):
        """
        Publica mensaje optimizado.

        Para TASK_COMPLETED: Resuelve future automáticamente.
        Para otros: Notifica subscribers.
        """
        self._messages.append(message)

        # Si es resultado de tarea, resolver future
        if message.msg_type == MessageType.TASK_COMPLETED:
            task_id = message.payload.get("task_id")
            if task_id in self._result_futures:
                future = self._result_futures[task_id]
                future.set_result(message.payload["result"])

        # Notificar subscribers
        if message.receiver in self._subscribers:
            for callback in self._subscribers[message.receiver]:
                callback(message)

    async def wait_for_result(self, task_id: int) -> Any:
        """Lead Agent espera resultado de SubAgent (async)."""
        import asyncio
        future = asyncio.Future()
        self._result_futures[task_id] = future
        return await future

# Reducción de mensajes:
# Antes: 15 mensajes (5 agentes × 3 mensajes c/u)
# Después: 10 mensajes (5 task_assigned + 5 task_completed)
# Reducción: 33%
```

---

## Debuggear Sistemas Multi-Agente con IA

### Prompt 4: IA como Debugger de Sistemas Complejos

**Objetivo**: Usar IA para analizar logs y encontrar bugs en interacciones entre agentes.

**Prompt**:
```
Actúa como un debugger experto de sistemas multi-agente.

SÍNTOMA:
Mi sistema multi-agente falla aleatoriamente. A veces retorna resultados completos,
a veces retorna resultados parciales (solo 2 de 3 subagents reportan).

LOGS DISPONIBLES:
[Pegar logs aquí - ejemplo:]

```log
{"timestamp": "2024-10-30T10:00:00", "agent_id": "lead_agent", "event_type": "decision", "decision": "Creating 3 subagents"}
{"timestamp": "2024-10-30T10:00:01", "agent_id": "researcher_1", "event_type": "task_start", "task_id": 1}
{"timestamp": "2024-10-30T10:00:01", "agent_id": "researcher_2", "event_type": "task_start", "task_id": 2}
{"timestamp": "2024-10-30T10:00:01", "agent_id": "researcher_3", "event_type": "task_start", "task_id": 3}
{"timestamp": "2024-10-30T10:00:15", "agent_id": "researcher_1", "event_type": "task_complete", "task_id": 1, "confidence": 0.9}
{"timestamp": "2024-10-30T10:00:18", "agent_id": "researcher_2", "event_type": "task_complete", "task_id": 2, "confidence": 0.85}
{"timestamp": "2024-10-30T10:00:25", "agent_id": "lead_agent", "event_type": "decision", "decision": "Synthesizing results from 2 agents"}
```

TAREA:
1. Analiza los logs
2. Identifica el problema (¿por qué solo 2 de 3 agentes reportaron?)
3. Sugiere hipótesis de causa raíz
4. Propone fixes concretos con código
5. Sugiere checks adicionales para prevenir este bug

FORMATO:
```json
{
  "bug_analysis": {
    "symptom": "...",
    "evidence_from_logs": ["...", "..."],
    "missing_events": ["researcher_3 task_complete never fired"]
  },
  "root_cause_hypotheses": [
    {
      "hypothesis": "Timeout en researcher_3",
      "probability": 0.7,
      "evidence": "..."
    },
    {
      "hypothesis": "Exception no manejada en researcher_3",
      "probability": 0.2,
      "evidence": "..."
    }
  ],
  "proposed_fixes": [
    {
      "fix": "Agregar timeout handling en SubAgent.research()",
      "code": "...",
      "prevents": "Agente colgado sin reportar"
    }
  ],
  "prevention_checks": [
    "Assert que len(results) == len(tasks) antes de synthesis",
    "Timeout global en asyncio.gather()"
  ]
}
```
```

**Uso**: Pegar logs reales en el prompt y Claude analizará el problema completo.

---

## Testing de Sistemas Multi-Agente con IA

### Prompt 5: Generar Tests Completos

**Objetivo**: IA genera suite completa de tests para tu sistema.

**Prompt**:
```
Actúa como un experto en testing de sistemas distribuidos.

CÓDIGO A TESTEAR:
[Pegar código de MultiAgentResearchSystem]

GENERA:
1. Unit tests para cada componente (MessageBus, SharedMemory, LeadAgent, SubAgent)
2. Integration tests para flujo completo
3. Tests de concurrencia (¿qué pasa si 2 agentes escriben a SharedMemory simultáneamente?)
4. Tests de failure modes (¿qué pasa si un SubAgent crashea?)
5. Property-based tests con hypothesis library

REQUISITOS:
- Usar pytest + pytest-asyncio
- Coverage >80%
- Incluir mocks para LLM calls
- Tests deben ejecutarse rápido (<5 segundos total)

FORMATO:
Genera archivo test_multi_agent.py completo con todos los tests.
```

**Output**: Claude genera archivo completo de tests que puedes ejecutar inmediatamente.

---

## Refactoring Guiado por IA

### Prompt 6: Refactorizar Sistema para Escalabilidad

**Objetivo**: IA sugiere refactorings para manejar 100+ agentes.

**Prompt**:
```
Actúa como un arquitecto de sistemas escalables.

CÓDIGO ACTUAL:
[Pegar implementación de MultiAgentResearchSystem]

PROBLEMA:
Este código funciona para 2-5 agentes, pero necesito escalar a 50-100 agentes
trabajando simultáneamente.

LIMITACIONES ACTUALES:
- SharedMemory usa dict en RAM (no escala)
- MessageBus guarda todos los mensajes en lista (memory leak)
- No hay rate limiting en tool calls
- Logs se escriben síncronamente (bottleneck)

TAREA:
1. Identifica todos los bottlenecks de escalabilidad
2. Propone refactorings concretos
3. Sugiere tecnologías (Redis para memory, RabbitMQ para messages, etc.)
4. Genera código refactorizado

PRIORIDAD:
- Performance > elegancia
- Mantener API pública igual (backward compatible)
- Agregar configuración para "modo lite" vs "modo escalable"
```

---

## Ejercicios Prácticos con IA

### Ejercicio 1: IA Diseña Tu Primer Sistema Multi-Agente

**Tarea**: Usa IA para diseñar un sistema de research específico para tu dominio.

**Pasos**:
1. Define tu query compleja (ej: "Analizar mercado de real estate en 5 ciudades")
2. Usa Prompt 1 para que IA diseñe arquitectura
3. Usa Prompt 2 para que IA genere agentes especializados
4. Implementa el sistema con código generado
5. Ejecuta y documenta resultados

**Criterio de éxito**: Sistema funcional con 3+ agentes generados por IA.

### Ejercicio 2: IA Debuggea Tu Sistema

**Tarea**: Introduce un bug intencionalmente y usa IA para encontrarlo.

**Bug sugerido**: Comentar una línea en SubAgent que envía resultado al Lead Agent.

**Pasos**:
1. Introduce el bug
2. Ejecuta el sistema y captura logs
3. Usa Prompt 4 para que IA analice logs
4. Implementa el fix sugerido por IA
5. Verifica que funciona

**Criterio de éxito**: IA identifica el problema y tu fix funciona.

### Ejercicio 3: IA Genera Tests para Ti

**Tarea**: Usa IA para generar tests completos.

**Pasos**:
1. Usa Prompt 5 con tu código
2. Claude genera tests
3. Ejecuta tests: `pytest -v`
4. Verifica coverage: `pytest --cov=multi_agent_system --cov-report=html`
5. Objetivo: >80% coverage

---

## Recursos IA para Multi-Agent Systems

### Herramientas Recomendadas

1. **Claude Code** - Para generar arquitecturas y código
2. **GitHub Copilot** - Para autocompletar implementaciones
3. **LangChain** - Framework Python para orquestación
4. **AutoGen** (Microsoft) - Framework multi-agente
5. **CrewAI** - Especializado en equipos de agentes

### Prompts de Referencia

Ver carpeta `prompts/` para biblioteca de 50+ prompts especializados en:
- Arquitectura de agentes
- Debugging de sistemas distribuidos
- Optimización de comunicación
- Testing exhaustivo
- Refactoring para escalabilidad

---

## Reflexión: IA como Co-Pilot en Desarrollo Multi-Agente

**Pregunta clave**: ¿Cuánto del código de esta clase fue generado por IA vs escrito manualmente?

**Respuesta**: ~60% generado con prompts, 40% refinamiento humano.

**Aprendizaje**:
- ✅ IA excelente para: Arquitectura inicial, código boilerplate, tests
- ⚠️ IA necesita guía para: Decisiones de trade-offs, optimizaciones específicas
- 🧠 Humano esencial para: Validar soluciones, integrar piezas, debugging complejo

**Recomendación**: Usa IA como "senior developer assistant" que propone soluciones,
pero TÚ decides qué implementar basado en tu contexto específico.

---

**Siguiente**: Aplica estos workflows en el [Proyecto de Documentación](./ejemplos/documentation_system/README.md)
