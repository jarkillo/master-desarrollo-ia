# Clase 6.5 - Claude Agent SDK: Building Professional Agents

**Módulo 4 - Infraestructura y Cloud**

**Duración estimada**: 6-8 horas

---

## Índice

1. [Introducción](#introducción)
2. [Objetivos de aprendizaje](#objetivos-de-aprendizaje)
3. [Conceptos clave](#conceptos-clave)
4. [Arquitectura del SDK](#arquitectura-del-sdk)
5. [Ejercicios prácticos](#ejercicios-prácticos)
6. [Proyecto final](#proyecto-final)
7. [Recursos adicionales](#recursos-adicionales)

---

## Introducción

Esta clase profundiza en el **Claude Agent SDK** de Anthropic, la herramienta oficial para construir agentes autónomos profesionales. Después de haber explorado LangChain en la Clase 6, ahora veremos cómo Anthropic diseña agentes desde el punto de vista del creador del modelo.

### ¿Por qué Claude Agent SDK?

**LangChain vs Claude Agent SDK**:
- **LangChain**: Framework versátil, multi-modelo, rico ecosistema de integraciones
- **Claude Agent SDK**: Diseñado específicamente para Claude, optimizado para sus capacidades únicas, control fino del feedback loop

**Cuándo usar cada uno**:
- **LangChain**: Proyectos multi-modelo, necesitas cambiar entre providers, ecosistema rico de herramientas
- **Claude Agent SDK**: Máximo rendimiento con Claude, control preciso del loop de agente, debugging avanzado

### Filosofía del SDK

El SDK implementa el **feedback loop fundamental** de los agentes:

```
Gather Context → Take Action → Verify Work → Repeat
```

Este ciclo iterativo permite a los agentes refinar sus salidas y detectar errores antes de que se acumulen.

---

## Objetivos de aprendizaje

Al finalizar esta clase, podrás:

1. ✅ Entender la arquitectura del Claude Agent SDK
2. ✅ Implementar loops de control y flujo en agentes
3. ✅ Diseñar herramientas (tools) efectivas para agentes
4. ✅ Manejar errores y lógica de reintentos
5. ✅ Gestionar estado en agentes complejos
6. ✅ Debuggear agentes usando técnicas profesionales
7. ✅ Comparar LangChain y Claude SDK según contexto
8. ✅ Construir un agente de desarrollo autónomo

---

## Conceptos clave

### 1. Context Gathering (Recopilación de contexto)

#### Agentic Search & File Systems

El sistema de archivos como **almacenamiento estructurado de información**. Los agentes usan comandos bash (`grep`, `tail`, `find`) para cargar datos relevantes de forma inteligente.

**Analogía**: El file system es como una biblioteca organizada. El agente es un investigador que sabe qué estante revisar según la pregunta.

```python
# Ejemplo: Agente busca errores en logs
agent.run_bash("grep 'ERROR' logs/*.log | tail -20")
```

**Ventaja**: La estructura de carpetas es "una forma de context engineering" - organiza información para que el agente la encuentre fácilmente.

#### Semantic Search

Búsqueda por similitud vectorial (embeddings). Más rápida que agentic search, pero sacrifica precisión y transparencia.

**Recomendación**: Empieza con agentic search, añade semantic search solo si el rendimiento lo requiere.

#### Subagents (Sub-agentes)

Contextos de ejecución aislados que permiten:
- **Paralelización**: Múltiples tareas simultáneas
- **Gestión de contexto**: Compartimentación de información

**Ejemplo**: Un agente principal delega subtareas (buscar en docs, analizar código, ejecutar tests) a subagentes especializados.

#### Compaction (Compactación)

Resúmenes automáticos de conversaciones para evitar agotamiento del contexto durante ejecuciones largas.

**Analogía**: Como tomar notas de una reunión larga - guardas lo importante, descarta detalles innecesarios.

---

### 2. Action Execution (Ejecución de acciones)

#### Tool Design (Diseño de herramientas)

Las herramientas (tools) son **los bloques fundamentales de ejecución**. Aparecen prominentemente en el contexto de Claude, por lo que la selección estratégica de tools es crítica.

**Principios de diseño**:
- ✅ **Específicas**: Una tool = una función clara
- ✅ **Bien documentadas**: Descripciones claras para que Claude entienda cuándo usarlas
- ✅ **Idempotentes**: Llamadas repetidas = mismo resultado
- ✅ **Con validación**: Verificar inputs antes de ejecutar

#### Bash & Scripts

Flexibilidad general para tareas variadas: conversión de PDFs, búsquedas web, manipulación de archivos.

**Ejemplo**:
```python
# Tool para buscar en StackOverflow
bash_tool = BashTool(
    command="curl -s 'https://api.stackexchange.com/2.3/search?order=desc&sort=activity&intitle={query}&site=stackoverflow'"
)
```

#### Code Generation (Generación de código)

**"El código es preciso, componible e infinitamente reutilizable"**. Ideal para operaciones complejas y creación de archivos (hojas de cálculo, presentaciones, documentos).

**Ejemplo**: Un agente genera código Python para procesar datos, en lugar de hacerlo paso a paso con tools.

#### Model Context Protocol (MCP)

Integraciones estandarizadas con autenticación automática: Slack, GitHub, Asana. Sin gestión manual de OAuth.

**Ventaja**: Plug-and-play con servicios externos sin implementar flujos de autenticación.

---

### 3. Verification & Improvement (Verificación y mejora)

#### Rules-Based Feedback

Feedback basado en reglas definidas. Ejemplo: linting de código.

**Ejemplo**: TypeScript linting proporciona más capas de validación que JavaScript.

```python
# Después de generar código, ejecutar linter
result = agent.execute(generate_code_task)
lint_result = agent.run_bash(f"ruff check {result.output_file}")
if lint_result.errors:
    agent.retry_with_feedback(lint_result.errors)
```

#### Visual Feedback

Screenshots para refinamiento iterativo de contenido UI. Verifica layout, estilos, jerarquía, responsividad.

**Analogía**: Como un diseñador que revisa mockups - ve el resultado, ajusta, ve de nuevo.

#### LLM-as-Judge

Evaluación de un modelo secundario sobre criterios difusos. Sacrifica latencia por ganancias marginales de rendimiento.

**Ejemplo**: Evaluar la "calidad" de un texto generado usando otro LLM como juez.

---

### 4. Testing & Iteration

**Enfoques de evaluación**:
- ¿El agente malinterpreta por falta de información?
- ¿Falla repetidamente en tareas específicas?
- ¿Tiene problemas corrigiendo errores?
- ¿Varía el rendimiento al añadir features?

**Práctica recomendada**: Test sets representativos basados en uso real para mejora continua.

---

## Arquitectura del SDK

### Componentes principales

```
┌─────────────────────────────────────────────┐
│           Claude Agent SDK                  │
│                                             │
│  ┌────────────┐      ┌──────────────┐     │
│  │  Agent     │◄────►│ Tool Manager │     │
│  │  Loop      │      │              │     │
│  └────────────┘      └──────────────┘     │
│        │                     │             │
│        │                     │             │
│  ┌────────────┐      ┌──────────────┐     │
│  │  Context   │      │ Verification │     │
│  │  Manager   │      │  Engine      │     │
│  └────────────┘      └──────────────┘     │
│        │                     │             │
│        └──────────┬──────────┘             │
│                   │                        │
│            ┌──────────────┐                │
│            │    State     │                │
│            │  Management  │                │
│            └──────────────┘                │
└─────────────────────────────────────────────┘
```

### El Agent Loop

```python
while not task_complete:
    # 1. Gather Context
    context = context_manager.gather()

    # 2. Take Action
    action = agent.decide_action(context)
    result = tool_manager.execute(action)

    # 3. Verify Work
    is_valid = verification_engine.check(result)

    if not is_valid:
        # 4. Iterate with feedback
        context_manager.add_feedback(verification_engine.errors)
        continue

    task_complete = True
```

---

## Ejercicios prácticos

### Ejercicio 1: Primer agente simple con SDK
**Archivo**: `ejemplos/01_agente_simple.py`

Construye un agente que responda preguntas sobre un repositorio de código usando agentic search.

**Conceptos**: Context gathering, bash tools, feedback loop básico

---

### Ejercicio 2: Loops y control de flujo
**Archivo**: `ejemplos/02_control_flujo.py`

Implementa un agente con retry logic y manejo de estados (pendiente, en progreso, completado, fallido).

**Conceptos**: State management, error handling, iteración controlada

---

### Ejercicio 3: Tool calling avanzado
**Archivo**: `ejemplos/03_tools_avanzadas.py`

Diseña tools personalizadas con validación, idempotencia y logging.

**Conceptos**: Tool design, best practices, debugging

---

### Ejercicio 4: Subagentes y paralelización
**Archivo**: `ejemplos/04_subagentes.py`

Crea un agente principal que coordina subagentes especializados (búsqueda, análisis, ejecución).

**Conceptos**: Subagents, paralelización, context management

---

## Proyecto final

### Agente de desarrollo autónomo

**Descripción**: Construye un agente que automatiza tareas de desarrollo como:
- Analizar issues en GitHub
- Buscar código relevante en el repositorio
- Generar fix basado en patrones existentes
- Ejecutar tests y validar
- Crear Pull Request con los cambios

**Archivo**: `proyecto_final/agente_dev_autonomo.py`

**Requisitos**:
1. ✅ Context gathering desde GitHub API y file system
2. ✅ Tools personalizadas (git, pytest, code generation)
3. ✅ Verification engine con tests y linting
4. ✅ Retry logic para errores comunes
5. ✅ Logging detallado para debugging

**Acceptance criteria**:
- El agente resuelve al menos 3 tipos de issues simples (typos, imports faltantes, tests básicos)
- Ejecuta tests antes de crear PR
- Maneja errores comunes (tests fallan, linter falla)
- Genera logs claros del proceso

---

## Claude Agent SDK vs LangChain

| Aspecto | Claude Agent SDK | LangChain |
|---------|------------------|-----------|
| **Especialización** | Claude-only, optimizado | Multi-modelo |
| **Control del loop** | Muy fino | Abstracción más alta |
| **Debugging** | Tools específicas | Callbacks generales |
| **Curva aprendizaje** | Moderada | Más empinada |
| **Ecosistema** | Oficial Anthropic | Comunidad enorme |
| **Mejor para** | Máximo rendimiento Claude | Flexibilidad, multi-modelo |

**Recomendación práctica**:
- 🏆 **Prototipado rápido**: LangChain
- 🏆 **Producción con Claude**: Claude Agent SDK
- 🏆 **Multi-modelo**: LangChain
- 🏆 **Control fino**: Claude Agent SDK

---

## Recursos adicionales

### Documentación oficial
- [Building Agents with Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) (artículo base)
- [Anthropic Documentation](https://docs.anthropic.com/)
- [Tool Use Guide](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)

### Comparaciones
- [LangChain vs Custom Agent Loops](https://blog.langchain.dev/when-to-use-langchain/)
- [Agent Architectures Compared](https://www.anthropic.com/research/agent-architectures)

### Debugging
- [Debugging Claude Agents](https://docs.anthropic.com/en/docs/build-with-claude/debugging)
- [Prompt Engineering for Agents](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)

---

## Próximos pasos

Después de esta clase:
1. **Clase 6.6**: Context Engineering (cómo diseñar contexto efectivo para agentes)
2. **Clase 6.7**: Writing Tools for AI Agents (patrones avanzados de tool design)
3. **Módulo 5**: Full-Stack + Agent Orchestration Mastery

---

## Glosario

- **Agentic Search**: Búsqueda donde el agente decide qué datos cargar usando herramientas
- **Compaction**: Resumen automático de conversaciones largas para gestión de contexto
- **Feedback Loop**: Ciclo de gather context → action → verify → iterate
- **MCP (Model Context Protocol)**: Protocolo estándar para integraciones con autenticación
- **Subagent**: Contexto de ejecución aislado para subtareas especializadas
- **Tool**: Función que el agente puede invocar (bash, API calls, code execution)
- **Verification Engine**: Sistema que valida las salidas del agente antes de continuar

---

**Tiempo estimado**: 6-8 horas (2 horas teoría, 3 horas ejercicios, 3 horas proyecto final)

**Nivel**: Avanzado (requiere Módulo 4 Clase 6 - LangChain)
