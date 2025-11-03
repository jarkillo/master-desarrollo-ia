# Glosario - Writing Tools for AI Agents

## A

**Affordances**
: Capacidades percibidas de un objeto o sistema. En el contexto de agentes IA, se refiere a las acciones que el agente "percibe" como posibles. Los tools deben diseñarse considerando que los agentes tienen context window limitado pero memoria computacional abundante.

**Actionable Error Message**
: Mensaje de error que no solo describe el problema, sino que también indica al agente cómo corregirlo. Ejemplo: "Formato de fecha inválido: '2025/10/23'. Formato esperado: YYYY-MM-DD (ejemplo: '2025-10-23')."

**Agent**
: Programa de IA (como Claude) que puede razonar sobre tareas, tomar decisiones, y ejecutar acciones mediante tools.

**Anthropic**
: Compañía creadora de Claude. Sus best practices para tool design son el estándar de la industria.

## C

**Consolidar Funcionalidad**
: Principio de diseño donde un tool maneja múltiples operaciones discretas bajo el capó. Ejemplo: `schedule_event` que busca disponibilidad + crea evento, en lugar de 3 tools separados.

**Context Engineering**
: Técnica de optimizar cómo se estructura la información para maximizar la efectividad del agente dentro de su context window limitado.

**Context Window**
: Límite de tokens que un agente puede "ver" a la vez. Claude tiene ~200K tokens de context window. Los tools deben retornar información relevante sin desperdiciarla.

**Concise Response**
: Formato de respuesta que retorna solo información esencial, ahorrando tokens. Contrasta con "Detailed Response" que incluye metadatos e IDs.

## D

**Description Efectiva**
: Documentación de un tool que explica claramente: cuándo usarlo, cuándo NO usarlo, qué hace, qué parámetros acepta, ejemplos de uso, y relaciones con otros tools.

**Detailed Response**
: Formato de respuesta que incluye toda la información disponible (IDs, metadatos, contexto) para llamadas downstream. Consume más tokens que "Concise Response".

## E

**Error Handling**
: Estrategia de manejar errores en tools retornando mensajes accionables en lugar de stack traces técnicos.

**Evaluation-Driven Optimization**
: Metodología de mejorar tools iterativamente basándose en evaluaciones reales con agentes, midiendo accuracy, tokens consumidos, y número de llamadas.

## F

**Function Calling**
: Capacidad de un LLM de invocar funciones externas (tools) basándose en la descripción y schema proporcionados.

## H

**High-Impact Workflows**
: Workflows específicos que tu agente realmente necesita resolver. Priorizar estos en lugar de "cubrir" toda una API.

## I

**Identificador Semántico**
: Identificador humano-legible (email, nombre) en lugar de UUID alfanumérico. Ejemplo: usar "juan@empresa.com" en lugar de "a3f2e8d1-4c5b-6a7d-8e9f".

**Input Validation**
: Proceso de verificar que los inputs del agente cumplen los requisitos del tool antes de ejecutar. Se implementa con Pydantic.

## L

**LLM (Large Language Model)**
: Modelo de lenguaje grande como Claude, GPT-4, etc. Base de los agentes de IA.

## N

**Namespacing**
: Técnica de nombrar tools usando prefijos para evitar ambigüedad cuando hay muchos tools. Ejemplo: `asana_projects_search`, `jira_users_search`.

## O

**Over-Implementation**
: Anti-patrón de wrappear todos los endpoints de una API como tools sin evaluar cuáles son realmente útiles para el agente.

## P

**Path Traversal**
: Vulnerabilidad de seguridad donde un atacante accede a archivos fuera del directorio permitido usando paths como `../../etc/passwd`.

**Property-Based Testing**
: Técnica de testing donde defines propiedades que siempre deben cumplirse (e.g., "el tool nunca crashea"), y Hypothesis genera cientos de inputs aleatorios para verificar.

**Pydantic**
: Librería Python para validación de datos usando type hints. Estándar para definir schemas de tools.

## R

**Rate Limiting**
: Técnica de limitar el número de llamadas a un tool en una ventana de tiempo para prevenir saturación de APIs externas.

**Response Format Parameter**
: Parámetro que permite al agente elegir el nivel de detalle de la respuesta (`detailed` vs `concise`), optimizando el consumo de tokens.

**Result Type**
: Patrón de diseño donde un tool retorna `ToolSuccess` O `ToolError`, nunca exceptions. Facilita el manejo de errores por el agente.

## S

**Schema**
: Definición estructurada de los inputs y outputs de un tool. Se define usando JSON Schema o Pydantic.

**Semantic Identifier**
: Ver "Identificador Semántico".

**Secret Management**
: Práctica de nunca retornar secrets (API keys, passwords) en respuestas de tools. Se filtran automáticamente usando regex patterns.

## T

**Tool**
: Función que un agente puede invocar para interactuar con sistemas externos (APIs, bases de datos, archivos, etc.).

**Tool Description**
: Documentación detallada de un tool que guía al agente sobre cuándo y cómo usarlo.

**Tool Schema**
: Definición JSON de los parámetros que acepta un tool y sus tipos.

**Transcript Analysis**
: Técnica de debugging donde se analiza el log completo de las llamadas del agente para identificar problemas en tool design.

**Type Hints**
: Anotaciones de tipos en Python (e.g., `def foo(x: int) -> str`). Críticas para documentar schemas de tools.

## V

**Validation Error**
: Error que ocurre cuando los inputs del agente no cumplen el schema del tool.

## W

**Workflow**
: Secuencia de pasos que un agente ejecuta para completar una tarea. Ejemplos: "crear usuario nuevo", "analizar logs de error", "refactorizar función".

---

## Referencias

- [Writing Tools for Agents - Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Tool Use Guide - Anthropic](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [Pydantic Documentation](https://docs.pydantic.dev/)
