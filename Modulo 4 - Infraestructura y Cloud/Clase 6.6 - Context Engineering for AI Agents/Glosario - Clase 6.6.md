# Glosario - Clase 6.6: Context Engineering for AI Agents

## A

**Attention Budget**
Capacidad limitada de un LLM para procesar y "prestar atención" a todos los tokens en su contexto. Como cada token atiende a todos los demás (O(n²)), más tokens significa menos atención disponible por token.

**Agentic Memory**
Técnica de structured note-taking donde un agente escribe notas persistentes fuera del context window y las recupera cuando las necesita. Permite mantener estado a través de tareas largas.

## C

**Compaction**
Técnica para tareas de horizonte largo donde se resume el contenido de la conversación cuando el context window se llena, preservando información crítica y descartando contenido redundante.

**Context Engineering**
Disciplina de curar y gestionar estratégicamente los tokens que se proporcionan a un LLM durante la inferencia, optimizando el "attention budget" a través de system prompts, tools, ejemplos y datos externos.

**Context Rot (Degradación de Contexto)**
Fenómeno donde la precisión de un LLM se degrada a medida que el tamaño del context window aumenta. No es un cliff (acantilado) sino una degradación gradual de rendimiento.

**Context Window**
Cantidad máxima de tokens que un modelo de lenguaje puede procesar en una sola inferencia. Para Claude 3.5 Sonnet es de 200,000 tokens (~150,000 palabras).

**Chain-of-Thought (CoT)**
Técnica de prompting donde el modelo explicita su proceso de razonamiento paso a paso antes de dar una respuesta. Mejora la precisión en tareas complejas.

## D

**Dynamic Retrieval**
Estrategia donde el agente mantiene referencias ligeras (IDs, paths) en contexto y recupera información completa solo cuando la necesita (just-in-time), en vez de pre-cargar todo.

## F

**Few-Shot Learning**
Técnica donde se dan al modelo 2-5 ejemplos canónicos de la tarea deseada para que aprenda el patrón sin entrenamiento adicional. Los ejemplos sirven como "una imagen vale más que mil palabras".

## H

**Hybrid Retrieval**
Estrategia que combina pre-computed retrieval (información crítica cargada de antemano) con runtime exploration (exploración autónoma on-demand). Usado por Claude Code.

## L

**Lightweight Identifiers**
Referencias compactas (file paths, URLs, query IDs) que el agente mantiene en contexto en lugar del contenido completo. Reduce tokens y permite retrieval just-in-time.

**Long-Horizon Tasks**
Tareas que toman decenas de minutos a horas y requieren múltiples iteraciones. Necesitan técnicas especiales (compaction, note-taking, sub-agents) para evitar context pollution.

## M

**Metadata Signals**
Información estructural ligera (nombres de carpetas, timestamps, tamaños de archivo) que guía la navegación del agente sin incluir contenido completo.

**Multi-Agent Architecture (Sub-Agents)**
Patrón donde un agente principal delega subtareas a agentes especializados que trabajan con context windows limpios y retornan resúmenes condensados al orquestador.

## O

**O(n²) Complexity**
Complejidad computacional de la atención en transformers donde cada token atiende a todos los demás. Con n tokens, hay n × n relaciones a procesar, causando degradación cuadrática.

## P

**Progressive Disclosure**
Estrategia donde el agente descubre información incrementalmente a través de exploración, manteniendo solo lo necesario en memoria de trabajo (similar a humanos).

**Prompt Altitude**
Metáfora del nivel de especificidad de un system prompt. "Too high" = muy vago, "too low" = muy rígido/frágil, "optimal" = específico pero flexible.

**Prompt Engineering**
Disciplina de optimizar la instrucción del usuario para obtener la respuesta deseada. Subset de context engineering enfocado solo en el prompt.

## R

**Runtime Exploration**
Exploración autónoma del agente usando tools (grep, head, tail, search) en tiempo de ejecución para descubrir información relevante dinámicamente.

## S

**Structured Note-Taking**
Ver "Agentic Memory". Técnica donde el agente mantiene notas organizadas (objetivos, bugs, decisiones) fuera del contexto y las consulta cuando las necesita.

**System Prompt**
Instrucciones iniciales que definen el rol, capacidades, constraints y comportamiento esperado de un agente. Primera parte del contexto que el modelo recibe.

**Sub-Agent Architecture**
Ver "Multi-Agent Architecture". Patrón de separación de concerns donde agentes especializados manejan subtareas con contextos limpios.

## T

**Token**
Unidad básica de procesamiento en LLMs. Aproximadamente 1 token = 4 caracteres en inglés o ~0.75 palabras. "Hello world" = 2 tokens.

**Tool Result Clearing**
Forma ligera de compaction donde se eliminan outputs redundantes de tools, manteniendo solo los últimos resultados relevantes.

**Transformer Architecture**
Arquitectura de redes neuronales que usan mecanismos de atención para procesar secuencias. Base de LLMs como GPT, Claude, LLaMA.

## Z

**Zero-Shot**
Capacidad del modelo de realizar tareas sin ejemplos previos, solo con instrucciones. Contrasta con few-shot (con ejemplos).

---

## Términos Técnicos de Anthropic

**Claude Code**
Agente de desarrollo autónomo de Anthropic que usa context engineering efectivo con hybrid retrieval y tool-based exploration.

**Context Pollution**
Acumulación de información irrelevante o redundante en el contexto que degrada el rendimiento del agente en tareas largas.

**Attention Scarcity**
Problema fundamental donde los LLMs tienen recursos limitados de "atención" que deben distribuir entre todos los tokens del contexto.

---

## Analogías Usadas en la Clase

**Memoria de Trabajo Humana**
Analogía para context window: capacidad limitada (~7 ítems), degradación con sobrecarga, priorización automática.

**Escritorio Organizado**
Analogía para context engineering: dejas a mano solo lo que necesitas ahora, el resto va al archivador (retrieval on-demand).

**Prompt Altitude**
Analogía de altura de vuelo: muy alto = panorama vago, muy bajo = detalles innecesarios, óptimo = balance entre contexto y especificidad.

---

## Métricas y Números Clave

- **Claude 3.5 Sonnet context window**: 200,000 tokens
- **Complejidad de atención**: O(n²) relaciones entre tokens
- **Few-shot óptimo**: 2-3 ejemplos para la mayoría de tareas
- **Context rot zone**: >70% del context window
- **Target context inicial**: <5,000 tokens
- **Target tool output**: <1,000 tokens por llamada
- **Typical compaction ratio**: 5:1 a 10:1 (50k → 5-10k tokens)

---

## Comandos y Tools Comunes

```bash
# Contar tokens (Python)
import tiktoken
encoding = tiktoken.encoding_for_model("gpt-4")
tokens = len(encoding.encode(text))

# Herramientas de exploración
head -n 20 file.py          # Primeras 20 líneas
tail -n 20 file.py          # Últimas 20 líneas
grep -n 'pattern' file.py   # Buscar patrón con números de línea
wc -l file.py               # Contar líneas
```

---

## Patrones y Anti-Patrones

### ✅ Patrones Recomendados

- Progressive disclosure (exploración incremental)
- Lightweight identifiers (referencias, no contenido)
- Tool-based exploration (runtime discovery)
- Compaction when approaching limits
- Few-shot with diverse canonical examples

### ❌ Anti-Patrones a Evitar

- Context dumping (cargar todo de una vez)
- Exhaustive edge case lists in prompts
- Overlapping/ambiguous tools
- Tools que retornan >2000 tokens
- System prompts demasiado vagos o rígidos
- Ignorar token counts

---

## Recursos Externos Mencionados

- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [Claude Models & Context Windows](https://docs.anthropic.com/en/docs/about-claude/models)
- `tiktoken` library (OpenAI)
- Anthropic Memory Cookbook
