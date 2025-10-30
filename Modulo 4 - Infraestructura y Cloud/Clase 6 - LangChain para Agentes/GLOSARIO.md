# Glosario - Clase 6: LangChain y Agent Skills

## A

### Agent (Agente)
Entidad de IA que puede:
1. **Razonar** sobre qué hacer (thinking)
2. **Decidir** qué tools usar (decision making)
3. **Ejecutar** acciones (tool calling)
4. **Iterar** hasta completar la tarea (loop)

**Ejemplo**: Un agente recibe "¿Cuál es el clima en Madrid multiplicado por π?" → Razona que necesita: 1) buscar clima, 2) multiplicar por π → Usa tools `search` y `calculator`.

### Agent Skills
Paradigma de Anthropic para extender capacidades de agentes mediante **paquetes modulares de conocimiento** (carpetas con SKILL.md + archivos de soporte).

**Ventaja clave**: **Progressive disclosure** - el agente carga solo lo que necesita, permitiendo escalar a 100+ skills sin saturar el context window.

### Affordances
Propiedades de un tool que "invitan" al agente a usarlo correctamente. Un tool bien diseñado tiene claras **affordances** (cuándo usarlo, cómo usarlo, qué esperar).

**Anti-ejemplo**: `process_data(data)` - ¿Qué hace? ¿Qué formato espera?
**Buen ejemplo**: `search_contacts(query: str, limit: int = 10)` - Claro qué hace y qué inputs espera.

## C

### Chain (Cadena)
En LangChain, una **secuencia de pasos** que transforman un input en un output.

**Ejemplo simple**:
```
Prompt Template → LLM → Output Parser → String
```

**Ejemplo complejo**:
```
Query → Translate to English → Search → Translate to Spanish → Format
```

### Context Window
Cantidad máxima de tokens que un LLM puede procesar en una sola llamada.

**Ejemplos**:
- Claude 3.5 Sonnet: 200K tokens (~150K palabras)
- GPT-4 Turbo: 128K tokens (~96K palabras)

**Problema en agents**: Si metes 100 tools en el prompt, consumes gran parte del context window antes de que el usuario haga una pregunta.

### ConversationBufferMemory
Tipo de memoria en LangChain que guarda **todos los mensajes** de una conversación sin modificar.

**Pros**: Contexto completo siempre disponible
**Contras**: Consume context window rápidamente

### ConversationSummaryMemory
Tipo de memoria que **resume** conversaciones periódicamente usando un LLM.

**Ejemplo**:
```
Mensajes 1-10: [detalles completos]
Mensajes 11-20: Resumen: "Discutieron sobre arquitectura de microservicios..."
Mensajes 21-30: [detalles completos]
```

## D

### Dependency Inversion (en Agent Skills)
Principio de diseño donde skills de alto nivel **no dependen** de detalles de implementación.

**Ejemplo**: El skill "financial-analysis" no importa si los datos vienen de una API, CSV, o base de datos - eso se abstrae en archivos de referencia.

## E

### Embeddings (Vectores)
Representación numérica de texto que captura significado semántico.

**Ejemplo**:
```python
"perro" → [0.2, 0.8, 0.1, ..., 0.5]  # 1536 dimensiones
"gato"  → [0.3, 0.7, 0.2, ..., 0.4]  # Similar a "perro"
"carro" → [0.9, 0.1, 0.8, ..., 0.2]  # Diferente a "perro"
```

Usado en RAG para **buscar documentos similares** a una query.

## F

### FAISS
**Facebook AI Similarity Search** - Librería de Meta para búsqueda eficiente en vectores.

Permite buscar "los k documentos más similares a X" en **millones de documentos** en milisegundos.

**Uso en RAG**:
```python
vectorstore = FAISS.from_documents(chunks, embeddings)
similar_docs = vectorstore.similarity_search("query", k=5)
```

## L

### LangChain
Framework de Python para construir aplicaciones con LLMs mediante **composición de componentes modulares** (chains, agents, tools, memory, etc.).

**Filosofía**: "LEGO blocks for LLMs"

### LLM (Large Language Model)
Modelo de IA entrenado en grandes cantidades de texto para generar lenguaje natural.

**Ejemplos**: Claude (Anthropic), GPT-4 (OpenAI), Llama (Meta), Gemini (Google)

## M

### MCP (Model Context Protocol)
Protocolo estándar para conectar LLMs con fuentes de datos externas (APIs, bases de datos, etc.).

**Analogía**: MCP es como USB - un estándar que permite conectar cualquier "dispositivo" (tool) a cualquier "computadora" (LLM).

**Componentes**:
- **Resources**: Datos/archivos que el LLM puede leer
- **Tools**: Funciones que el LLM puede ejecutar
- **Prompts**: Templates reutilizables

### Memory (Memoria)
Componente que permite a un agente **recordar** interacciones pasadas.

**Tipos en LangChain**:
- **BufferMemory**: Guarda todo
- **SummaryMemory**: Resume periódicamente
- **WindowMemory**: Últimos N mensajes
- **VectorStoreMemory**: Búsqueda semántica en historia

## P

### Progressive Disclosure
Técnica de Agent Skills donde información se carga **por capas** según necesidad:

```
Nivel 1: Metadata (nombres de skills) - Siempre cargado
Nivel 2: SKILL.md completo - Solo si relevante
Nivel 3: Archivos de soporte - Solo si se necesita detalle
```

**Ventaja**: Context window se usa eficientemente.

### Prompt Template
Plantilla reutilizable para generar prompts dinámicos.

**Ejemplo**:
```python
template = "Eres un experto en {topic}. Responde: {question}"

# Genera prompts específicos:
prompt1 = template.format(topic="Python", question="¿Qué es el GIL?")
prompt2 = template.format(topic="FastAPI", question="¿Cómo validar inputs?")
```

## R

### RAG (Retrieval-Augmented Generation)
Técnica que combina:
1. **Retrieval**: Buscar documentos relevantes
2. **Augmentation**: Agregar docs al contexto
3. **Generation**: LLM genera respuesta basada en docs

**Analogía**: RAG es como un estudiante que puede consultar apuntes durante un examen (en lugar de solo usar memoria).

**Workflow**:
```
Query → Buscar docs similares → Agregar al prompt → LLM genera respuesta
```

### ReAct Pattern
Patrón de razonamiento para agents:
- **Re**asoning (Pensamiento)
- **Act**ion (Acción)

**Ejemplo**:
```
Thought: Necesito el precio de Bitcoin
Action: search("precio Bitcoin hoy")
Observation: $65,432 USD
Thought: Ahora puedo responder
Final Answer: Bitcoin cotiza a $65,432 USD
```

### Reranking
Técnica de RAG avanzada donde:
1. Búsqueda vectorial retorna top-K candidatos (e.g., top-20)
2. Un modelo especializado **reordena** (rerank) por relevancia
3. Se usan solo top-N después de reranking (e.g., top-5)

**Ventaja**: Mejor precisión que búsqueda vectorial sola.

### Retriever
Componente de LangChain que busca documentos relevantes dada una query.

**Ejemplo**:
```python
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
docs = retriever.get_relevant_documents("query")
```

## S

### Semantic Search (Búsqueda Semántica)
Búsqueda basada en **significado** en lugar de coincidencia exacta de palabras.

**Ejemplo**:
```
Query: "cómo entrenar modelos"
Documentos encontrados:
- "guía de fine-tuning de LLMs"  ✅ (significado similar)
- "tutorial de machine learning" ✅ (relacionado)
- "receta de cocina"              ❌ (no relacionado)
```

**Implementación**: Comparar embeddings (vectores) con similitud coseno.

### SKILL.md
Archivo principal de un Agent Skill que contiene:
- **Metadata YAML**: nombre, descripción
- **Instrucciones**: cuándo usar el skill, workflow paso a paso
- **Referencias**: archivos de soporte, ejemplos, error handling

**Estructura**:
```markdown
---
name: PDF Form Processor
description: Extract and validate data from PDF forms
---

# PDF Form Processing Skill

## When to Use This Skill
...

## Workflow
...
```

## T

### Tool (Herramienta)
Función que un agente puede invocar para interactuar con el mundo exterior.

**Ejemplos de tools**:
- `search(query)` - Buscar en internet
- `calculator(expression)` - Calcular matemáticas
- `read_file(path)` - Leer archivo
- `create_git_branch(name)` - Crear rama Git

**Anatomía de un tool**:
```python
{
    "name": "search",
    "description": "Busca información en internet",
    "parameters": {
        "query": {"type": "string", "description": "Texto a buscar"}
    }
}
```

### Tool Calling
Capacidad de un LLM de **invocar funciones externas** durante la generación.

**Workflow**:
1. Usuario: "¿Cuál es el clima en Madrid?"
2. LLM decide: "Necesito tool `search`"
3. LLM genera: `{"tool": "search", "input": "clima Madrid hoy"}`
4. Sistema ejecuta tool → Retorna resultado
5. LLM genera respuesta final usando el resultado

## V

### Vector Store (Base de Datos Vectorial)
Base de datos optimizada para almacenar y buscar **vectores** (embeddings).

**Ejemplos**:
- **FAISS**: In-memory, muy rápido
- **Chroma**: Persistente, fácil de usar
- **Pinecone**: Cloud-hosted, escalable
- **Weaviate**: Open-source, features avanzados

**Uso principal**: RAG (buscar documentos similares a una query)

### VectorStoreRetrieverMemory
Tipo de memoria en LangChain que guarda mensajes en un **vector store** y recupera los más **semánticamente relevantes** a la conversación actual.

**Ventaja**: Escala a miles de mensajes (solo recupera los relevantes)

**Ejemplo**:
```python
# Guardar contexto
memory.save_context(
    {"input": "Mi proyecto usa FastAPI"},
    {"output": "Entendido"}
)

# 100 mensajes después...
memory.load_memory_variables({"prompt": "¿Qué framework uso?"})
# Retorna: "Mi proyecto usa FastAPI" (recuperado por similitud)
```

---

## Conceptos Clave Comparados

### Agent Skills vs LangChain

| Aspecto | Agent Skills | LangChain |
|---------|-------------|-----------|
| **Formato** | Markdown + scripts | Código Python |
| **Escalabilidad** | Ilimitada (progressive disclosure) | Limitada (context window) |
| **Mejor para** | Workflows complejos | Orchestración de tools |

### RAG vs Fine-tuning

| Aspecto | RAG | Fine-tuning |
|---------|-----|-------------|
| **Actualización** | Instantánea (agregar docs) | Requiere reentrenamiento |
| **Costo** | Bajo (solo embeddings) | Alto (GPU hours) |
| **Datos necesarios** | Documentos (sin etiquetar) | Pares input-output etiquetados |
| **Mejor para** | Conocimiento factual actualizado | Cambiar tono/estilo del LLM |

### Memory Types

| Tipo | Almacena | Mejor Para | Limitación |
|------|----------|------------|------------|
| **BufferMemory** | Todo | Conversaciones cortas | Context window |
| **SummaryMemory** | Resumen | Conversaciones largas | Pierde detalles |
| **WindowMemory** | Últimos N | Conversaciones enfocadas | Olvida contexto antiguo |
| **VectorStoreMemory** | Búsqueda semántica | Miles de mensajes | No preserva orden cronológico |

---

## Siglas y Acrónimos

- **API**: Application Programming Interface
- **FAISS**: Facebook AI Similarity Search
- **JSON**: JavaScript Object Notation
- **LLM**: Large Language Model
- **MCP**: Model Context Protocol
- **RAG**: Retrieval-Augmented Generation
- **REPL**: Read-Eval-Print Loop
- **ReAct**: Reasoning + Acting
- **REST**: Representational State Transfer
- **YAML**: YAML Ain't Markup Language

---

## Recursos para Profundizar

**Documentación oficial**:
- [Agent Skills - Anthropic](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [LangChain Docs](https://python.langchain.com/docs/get_started/introduction)
- [Model Context Protocol](https://modelcontextprotocol.io/)

**Papers académicos**:
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)

**Tutoriales**:
- [LangChain Cookbook](https://github.com/langchain-ai/langchain/tree/master/cookbook)
- [Claude Code Skills](https://github.com/anthropics/claude-code/tree/main/.claude/skills)
