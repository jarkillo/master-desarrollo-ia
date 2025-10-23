# Clase 6.6 - Context Engineering for AI Agents: maximizar la efectividad de tus agentes

## 🎬 El problema

Has creado agentes IA que funcionan bien con tareas simples, pero cuando les das tareas complejas o múltiples archivos para analizar, empiezan a fallar:

> "El agente ignoró archivos importantes que estaban en el contexto..."
> "Cuando le di 10 archivos, solo analizó los primeros 3..."
> "El agente se confunde cuando hay demasiada información..."

¿Por qué ocurre?

Porque los LLMs sufren de **"context rot"** (degradación de contexto):
- **Accuracy degrades** a medida que el contexto crece
- Cada token "compite" por la atención del modelo
- Los modelos tienen menos experiencia con secuencias muy largas
- El rendimiento se degrada gradualmente, no de golpe

Para solucionar esto existe **Context Engineering**: la disciplina de curar y gestionar estratégicamente los tokens que le das a un LLM durante la inferencia.

---

## 🧠 Concepto

### La analogía de la memoria de trabajo humana

Piensa en el contexto de un LLM como la **memoria de trabajo humana**:

- **Capacidad limitada**: Solo puedes mantener ~7±2 elementos en tu mente simultáneamente
- **Degradación con sobrecarga**: Más información no siempre es mejor
- **Priorización**: Tu cerebro automáticamente prioriza lo importante y descarta lo irrelevante
- **Acceso just-in-time**: No intentas memorizar todo; buscas información cuando la necesitas

Por eso:

- **Context engineering** es como organizar tu escritorio: dejas a mano solo lo que necesitas ahora
- **Dynamic retrieval** es como tener un archivador cerca: traes información solo cuando la necesitas
- **Compaction** es como resumir notas: condensas información preservando lo esencial
- **Sub-agents** es como delegar: personas especializadas manejan subtareas y te dan resúmenes

### El problema de atención cuadrática

Los transformers (arquitectura de los LLMs) tienen una característica clave:

**Cada token atiende a todos los demás tokens** → Complejidad O(n²)

Si tienes 100 tokens:
- El modelo procesa 100 × 100 = **10,000 relaciones**

Si tienes 10,000 tokens:
- El modelo procesa 10,000 × 10,000 = **100,000,000 relaciones**

**Resultado**: Más contexto = menos atención disponible por token = degradación de calidad.

### Context Engineering vs Prompt Engineering

| Aspecto | Prompt Engineering | Context Engineering |
|---------|-------------------|---------------------|
| **Scope** | Solo la instrucción del usuario | Sistema completo (prompts, tools, historial, datos) |
| **Objetivo** | Obtener la respuesta correcta | Optimizar el "attention budget" |
| **Cuando usarlo** | Tareas simples, chat one-shot | Agentes autónomos, tareas largas |
| **Técnicas** | Few-shot, chain-of-thought | Retrieval dinámico, compaction, sub-agents |

**Insight clave**: Context engineering es **gestión de recursos escasos**. Trata cada token como si fuera RAM en tu computadora.

---

## 🛠️ Anatomía de un contexto efectivo

### 1. System Prompts: encontrar la "altitud" correcta

El system prompt debe estar en el punto óptimo entre especificidad y flexibilidad:

```
┌─────────────────────────────────────┐
│  TOO HIGH (Vague)                   │
│  "Be a helpful assistant"           │
│  ❌ Insuficientes señales concretas │
└─────────────────────────────────────┘
                ⬆
┌─────────────────────────────────────┐
│  OPTIMAL                            │
│  "You are a code reviewer           │
│   specializing in FastAPI.          │
│   Focus on: security, performance,  │
│   and REST API design patterns."    │
│  ✅ Clear, directo, flexible        │
└─────────────────────────────────────┘
                ⬇
┌─────────────────────────────────────┐
│  TOO LOW (Brittle)                  │
│  "If status code is 404, return X.  │
│   If 500, return Y. If 403..."      │
│  ❌ Frágil, alto mantenimiento      │
└─────────────────────────────────────┘
```

**Best practices para system prompts**:

✅ **Usa secciones organizadas**:
```xml
<role>
You are a Python code optimization specialist.
</role>

<guidelines>
- Prioritize readability over micro-optimizations
- Use type hints and docstrings
- Follow PEP 8 style guide
</guidelines>

<constraints>
- Do not suggest dependencies outside stdlib
- Preserve existing function signatures
</constraints>
```

✅ **Empieza mínimo, itera basado en fallos**:
```
# Versión 1 (mínima)
"You are a database migration expert."

# Versión 2 (después de observar fallos)
"You are a database migration expert specializing in zero-downtime deployments.
Always consider backward compatibility."

# Versión 3 (más específica)
"You are a database migration expert specializing in zero-downtime deployments.
Check: 1) Backward compatibility, 2) Index creation time, 3) Data loss risks."
```

❌ **Evita listas exhaustivas de edge cases** en el prompt. Usa ejemplos en su lugar.

### 2. Tools: el contrato entre agentes y su entorno

**Principios de diseño de tools**:

✅ **Token-efficient en retorno**:
```python
# ❌ MAL: Retorna todo el archivo (1000s de tokens)
def get_file_content(path: str) -> str:
    return open(path).read()

# ✅ BIEN: Retorna solo metadata primero
def get_file_info(path: str) -> dict:
    return {
        "path": path,
        "size": os.path.getsize(path),
        "lines": count_lines(path),
        "modified": os.path.getmtime(path)
    }
```

✅ **Sin overlaps ni ambigüedades**:
```python
# ❌ MAL: Tres tools que hacen lo mismo
search_codebase()
grep_files()
find_in_code()

# ✅ BIEN: Una tool clara
search_code(pattern: str, file_glob: str = "**/*.py")
```

✅ **Parámetros descriptivos**:
```python
# ❌ MAL: Ambiguo
def search(query: str, mode: int)

# ✅ BIEN: Auto-documentado
def search(
    query: str,
    search_mode: Literal["exact", "fuzzy", "regex"] = "exact"
)
```

**Ejemplo práctico: Tool para análisis de código**

```python
from typing import Literal, Optional
from pydantic import BaseModel, Field

class CodeSearchTool(BaseModel):
    """Search for code patterns in the codebase."""

    pattern: str = Field(
        description="The code pattern to search for (supports regex)"
    )
    file_pattern: str = Field(
        default="**/*.py",
        description="Glob pattern for files to search (e.g., 'src/**/*.py')"
    )
    context_lines: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Number of context lines before/after match"
    )
    max_results: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of results to return"
    )

    def execute(self) -> list[dict]:
        """Execute search and return token-efficient results."""
        results = []
        for match in search_codebase(self.pattern, self.file_pattern):
            results.append({
                "file": match.file,
                "line_number": match.line,
                "snippet": match.get_snippet(self.context_lines),
                # No retornamos el archivo completo
            })
            if len(results) >= self.max_results:
                break
        return results
```

**Por qué funciona**:
- Parámetros auto-documentados con `Field(description=...)`
- Límites de tokens claros (`max_results`, `context_lines`)
- Retorna referencias ligeras, no archivos completos
- Un solo propósito claro

### 3. Examples: few-shot learning efectivo

Los ejemplos son **"una imagen vale más que mil palabras"** para los LLMs.

**Estrategia de ejemplos canónicos**:

```python
# System prompt
"""
You are a FastAPI code reviewer. Review endpoints for:
1. Security (input validation, auth)
2. Performance (N+1 queries, caching)
3. REST design (HTTP methods, status codes)
"""

# Ejemplo 1: Security issue
"""
<example>
Code:
```python
@app.get("/users/{user_id}")
def get_user(user_id: str):
    return db.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

Review:
🔴 CRITICAL: SQL injection vulnerability
- Never use f-strings for SQL queries
- Use parameterized queries: db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
</example>
"""

# Ejemplo 2: Performance issue
"""
<example>
Code:
```python
@app.get("/users/{user_id}/posts")
def get_user_posts(user_id: int):
    user = db.query(User).get(user_id)
    # N+1 query problem
    posts = [db.query(Post).get(pid) for pid in user.post_ids]
    return posts
```

Review:
⚠️  PERFORMANCE: N+1 query detected
- Loading posts one by one
- Use: db.query(Post).filter(Post.id.in_(user.post_ids)).all()
- Or use eager loading: db.query(User).options(joinedload(User.posts)).get(user_id)
</example>
"""
```

**Cuántos ejemplos usar**:
- **0-1 ejemplos**: Tareas muy simples, LLM ya conoce el patrón
- **2-3 ejemplos**: Mayoría de casos (diversidad de escenarios)
- **5+ ejemplos**: Patrones complejos o poco comunes

❌ **Evita**: Ejemplos exhaustivos de edge cases → Infla el contexto sin mejorar el rendimiento

---

## 🔍 Dynamic Context Retrieval: just-in-time information

### El problema del "context dumping"

**Approach ingenuo** (❌ MAL):
```python
# Cargar TODO en el contexto de una vez
context = ""
for file in all_project_files:  # 100 archivos
    context += f"File: {file}\n{read_file(file)}\n\n"

agent.run(context + user_query)  # 50,000 tokens de contexto
```

**Problemas**:
- Context rot: El agente ignora archivos al final
- Información irrelevante: 90% de archivos no son necesarios
- Lento: Procesar 50k tokens toma tiempo
- Caro: Cada token cuesta dinero

### Progressive disclosure: descubrimiento incremental

**Approach inteligente** (✅ BIEN):

```python
# Fase 1: Metadata ligera
file_index = [
    {"path": "src/api/endpoints.py", "size": 1200, "modified": "2025-10-20"},
    {"path": "src/models/user.py", "size": 450, "modified": "2025-10-19"},
    # ... solo metadata, ~100 tokens
]

# Fase 2: El agente explora autónomamente
agent_tools = [
    list_files(directory: str),  # Listar archivos
    get_file_info(path: str),    # Ver metadata
    read_file_head(path: str, lines: int = 20),  # Primeras N líneas
    search_in_file(path: str, pattern: str),     # Buscar patrón
    read_full_file(path: str)   # Último recurso
]

# Fase 3: Agente decide qué necesita
"""
Agent thinking:
"User asked about authentication. Let me:
1. Search for 'auth' across files → Found in endpoints.py, auth.py
2. Read head of auth.py → Looks relevant
3. Read full auth.py → Found the issue"
"""
```

**Ventajas**:
- **Efficient**: Solo lee lo necesario (300 tokens vs 50,000)
- **Accurate**: Contexto relevante, no ruido
- **Flexible**: Se adapta a la query
- **Scalable**: Funciona con 10 archivos o 10,000

### Estrategias de retrieval

**1. Metadata signals (navegación por jerarquía)**

```python
# Dar estructura al agente, no contenido
project_structure = {
    "src/": {
        "api/": ["endpoints.py", "middleware.py"],
        "models/": ["user.py", "post.py"],
        "services/": ["email.py", "storage.py"]
    },
    "tests/": {
        "test_api.py": "modified 2 days ago",
        "test_models.py": "modified 1 week ago"
    }
}

# El agente puede navegar basándose en:
# - Nombres de carpetas (api/ probablemente tiene endpoints)
# - Nombres de archivos (email.py probablemente maneja correos)
# - Timestamps (archivos recientes = más probable cambio reciente)
```

**2. Lightweight identifiers (referencias, no contenido)**

```python
# ❌ MAL: Cargar SQL queries completas
saved_queries = {
    "get_active_users": "SELECT users.id, users.name, users.email FROM users JOIN subscriptions ON users.id = subscriptions.user_id WHERE subscriptions.status = 'active' AND users.deleted_at IS NULL ORDER BY users.created_at DESC",
    # ... 20 queries más, 5000 tokens
}

# ✅ BIEN: Referencias + tool para obtener detalles
saved_queries_index = {
    "get_active_users": {
        "description": "Fetch active users with subscriptions",
        "returns": "List of users",
        "query_id": "q_001"
    }
}

def get_query_details(query_id: str) -> str:
    """Retrieve full query only when needed."""
    return database.get_query(query_id)
```

**3. Runtime exploration (herramientas de exploración)**

```python
# Tools para que el agente explore en runtime
exploration_tools = {
    "bash": {
        "head": "head -n 20 file.py",  # Primeras 20 líneas
        "tail": "tail -n 20 file.py",  # Últimas 20 líneas
        "wc": "wc -l file.py",         # Contar líneas
        "grep": "grep -n 'pattern' file.py"  # Buscar patrón
    },
    "custom": {
        "list_functions": "Extract function names from file",
        "get_function": "Get specific function source code",
        "get_imports": "List file imports"
    }
}
```

**Ejemplo real: Claude Code approach**

Claude Code usa **hybrid retrieval**:

```
┌──────────────────────────────────────┐
│  Critical upfront (pre-computed)     │
│  - Project structure                 │
│  - Recently modified files           │
│  - Open files in editor              │
│  ≈ 500-1000 tokens                   │
└──────────────────────────────────────┘
              +
┌──────────────────────────────────────┐
│  On-demand exploration (agent tools) │
│  - grep/search files                 │
│  - Read file contents                │
│  - List directory                    │
│  ≈ Retrieved as needed               │
└──────────────────────────────────────┘
```

**Trade-off: Speed vs Efficiency**

| Approach | Speed | Token Efficiency | Best For |
|----------|-------|------------------|----------|
| **Pre-computed retrieval** | ⚡ Fast (todo pre-cargado) | ❌ Baja (mucho ruido) | Datasets pequeños (<1000 archivos) |
| **Runtime exploration** | 🐌 Slower (llama tools en runtime) | ✅ Alta (solo lo necesario) | Codebases grandes, información dinámica |
| **Hybrid** | ⚡ Balanced | ✅ Balanced | Producción (Claude Code) |

---

## 🔧 Técnicas para tareas de horizonte largo

Cuando los agentes trabajan en tareas que toman **decenas de minutos a horas**, surgen problemas de contaminación de contexto:

- Historial de 100+ tool calls
- Outputs redundantes acumulados
- Context window lleno de información obsoleta

### Técnica 1: Compaction (compactación)

**Cuándo usar**: Conversaciones largas con mucho back-and-forth.

**Cómo funciona**:

```
┌────────────────────────────────┐
│  Context window lleno          │
│  [40,000 / 200,000 tokens]     │
│  - 50 mensajes                 │
│  - 30 tool outputs             │
│  - Información redundante      │
└────────────────────────────────┘
          ⬇ Compaction
┌────────────────────────────────┐
│  Context compactado            │
│  [8,000 / 200,000 tokens]      │
│  - Resumen de decisiones clave │
│  - Bugs sin resolver           │
│  - Detalles de implementación  │
│  - Tool outputs descartados    │
└────────────────────────────────┘
```

**Implementación**:

```python
def compact_conversation(messages: list[Message]) -> list[Message]:
    """
    Compacta conversación preservando información crítica.
    """
    # 1. Identificar información crítica
    critical_info = extract_critical_decisions(messages)
    unresolved_issues = extract_unresolved_bugs(messages)
    implementation_details = extract_key_implementations(messages)

    # 2. Generar summary con LLM
    summary_prompt = f"""
    Summarize this conversation preserving:
    - Architectural decisions: {critical_info}
    - Unresolved bugs: {unresolved_issues}
    - Implementation details: {implementation_details}

    Discard:
    - Tool outputs (unless contain critical errors)
    - Redundant messages
    - Completed tasks
    """

    summary = llm.generate(summary_prompt)

    # 3. Reiniciar context window con summary
    return [
        SystemMessage(content=system_prompt),
        UserMessage(content=summary),  # High-fidelity summary
        UserMessage(content="Continue from where we left off...")
    ]
```

**Tool result clearing** (forma ligera de compaction):

```python
# Mantener solo el último resultado de cada tool
def clear_old_tool_results(messages: list[Message]) -> list[Message]:
    tool_results = {}
    filtered = []

    for msg in messages:
        if isinstance(msg, ToolResultMessage):
            # Solo guardar el último resultado de cada tool
            tool_results[msg.tool_name] = msg
        else:
            filtered.append(msg)

    # Añadir solo últimos resultados
    filtered.extend(tool_results.values())
    return filtered
```

### Técnica 2: Structured Note-Taking (memoria agéntica)

**Cuándo usar**: Desarrollo iterativo con milestones claros.

**Cómo funciona**:

```
┌─────────────────────────────────────┐
│  Agent working memory (context)     │
│  Current task: "Implement auth"     │
│  Recent messages: ...               │
└─────────────────────────────────────┘
              ⬇ Writes notes
┌─────────────────────────────────────┐
│  Persistent notes (outside context) │
│  ✅ Completed: User model           │
│  ✅ Completed: JWT generation       │
│  ⏳ In progress: Password hashing   │
│  📝 TODO: Refresh tokens            │
│  🐛 Bug: Email validation fails     │
└─────────────────────────────────────┘
              ⬆ Reads when needed
```

**Ejemplo práctico: Agente jugando Pokémon** (ejemplo real de Anthropic)

```python
class PokemonAgentMemory:
    """
    Notas persistentes para agente jugando Pokémon.
    """

    def __init__(self):
        self.notes = {
            "objectives": [],
            "explored_regions": set(),
            "pokemon_team": [],
            "combat_strategies": {},
            "inventory": {},
            "achievements": []
        }

    def update_exploration(self, region: str):
        """El agente anota regiones exploradas."""
        self.notes["explored_regions"].add(region)
        self.save()

    def log_combat_outcome(self, opponent: str, strategy: str, won: bool):
        """Aprende de combates."""
        if opponent not in self.notes["combat_strategies"]:
            self.notes["combat_strategies"][opponent] = []

        self.notes["combat_strategies"][opponent].append({
            "strategy": strategy,
            "outcome": "win" if won else "loss",
            "timestamp": datetime.now()
        })
        self.save()

    def get_relevant_notes(self, current_situation: str) -> str:
        """Recupera solo notas relevantes para situación actual."""
        if "battle" in current_situation:
            return self.format_combat_notes()
        elif "explore" in current_situation:
            return self.format_exploration_notes()
        # ...
```

**Ventajas**:
- Mantiene contexto a través de miles de acciones
- Solo trae información relevante al contexto actual
- Puede trackear progreso complejo (mapas, inventarios, objetivos)

**Implementación simple con archivos**:

```python
import json
from pathlib import Path

class AgentNotebook:
    """Simple persistent notes for agents."""

    def __init__(self, notebook_path: str = ".agent_notes.json"):
        self.path = Path(notebook_path)
        self.load()

    def load(self):
        if self.path.exists():
            self.notes = json.loads(self.path.read_text())
        else:
            self.notes = {"tasks": [], "decisions": [], "bugs": []}

    def save(self):
        self.path.write_text(json.dumps(self.notes, indent=2))

    def log_decision(self, decision: str, reasoning: str):
        """Agente registra decisión arquitectónica."""
        self.notes["decisions"].append({
            "decision": decision,
            "reasoning": reasoning,
            "timestamp": datetime.now().isoformat()
        })
        self.save()

    def log_bug(self, bug: str, status: str = "open"):
        """Agente registra bug encontrado."""
        self.notes["bugs"].append({
            "description": bug,
            "status": status,
            "timestamp": datetime.now().isoformat()
        })
        self.save()

    def get_summary(self) -> str:
        """Resumen para inyectar en contexto."""
        return f"""
        Decisions made: {len(self.notes['decisions'])}
        Open bugs: {len([b for b in self.notes['bugs'] if b['status'] == 'open'])}
        Tasks completed: {len([t for t in self.notes['tasks'] if t['done']])}

        Recent decisions:
        {self.notes['decisions'][-3:]}

        Open bugs:
        {[b for b in self.notes['bugs'] if b['status'] == 'open']}
        """
```

### Técnica 3: Sub-Agent Architectures

**Cuándo usar**: Investigación/análisis complejo donde exploración paralela ayuda.

**Cómo funciona**:

```
┌────────────────────────────────────────┐
│  Main Agent (Orchestrator)             │
│  "Analyze security of authentication"  │
└────────────────────────────────────────┘
         ⬇ Delegates to specialized sub-agents
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ Sub-Agent 1 │  │ Sub-Agent 2 │  │ Sub-Agent 3 │
│ Analyze JWT │  │ Check SQL   │  │ Review      │
│ impl        │  │ injection   │  │ password    │
│             │  │             │  │ hashing     │
└─────────────┘  └─────────────┘  └─────────────┘
       ⬇                ⬇                ⬇
  1000 tokens      1500 tokens      800 tokens
       ⬇ Condensed summaries back to main agent
┌────────────────────────────────────────┐
│  Main Agent receives summaries         │
│  Total: 3,300 tokens (vs 20k if direct)│
│  Makes final assessment                │
└────────────────────────────────────────┘
```

**Ejemplo práctico**:

```python
from typing import List
from dataclasses import dataclass

@dataclass
class SubAgentTask:
    name: str
    instructions: str
    context: str
    max_tokens: int = 2000

class MultiAgentOrchestrator:
    """
    Orquestador que delega tareas a sub-agentes especializados.
    """

    def analyze_codebase_security(self, codebase_files: List[str]):
        # Define sub-agent tasks
        tasks = [
            SubAgentTask(
                name="JWT Security Analyst",
                instructions="""
                Analyze JWT implementation for:
                - Secret key management
                - Token expiration
                - Signature verification
                - Algorithm security (avoid 'none')
                """,
                context=self.filter_files(codebase_files, pattern="*jwt*")
            ),
            SubAgentTask(
                name="SQL Injection Hunter",
                instructions="""
                Find SQL injection vulnerabilities:
                - String concatenation in queries
                - Unparameterized queries
                - ORM misuse
                """,
                context=self.filter_files(codebase_files, pattern="*model*,*db*")
            ),
            SubAgentTask(
                name="Auth Flow Reviewer",
                instructions="""
                Review authentication flow:
                - Password hashing (bcrypt/argon2)
                - Session management
                - CSRF protection
                """,
                context=self.filter_files(codebase_files, pattern="*auth*")
            )
        ]

        # Run sub-agents in parallel
        sub_results = []
        for task in tasks:
            result = self.run_sub_agent(task)
            # Sub-agent retorna resumen condensado (1-2k tokens)
            sub_results.append({
                "agent": task.name,
                "summary": result.summary,  # Condensed findings
                "critical_issues": result.critical_issues
            })

        # Main agent synthesizes
        final_analysis = self.main_agent.synthesize(
            prompt="""
            Based on these security analyses from specialized agents,
            provide a comprehensive security assessment:

            {sub_results}

            Prioritize issues and suggest remediation steps.
            """,
            context=sub_results
        )

        return final_analysis

    def run_sub_agent(self, task: SubAgentTask) -> dict:
        """
        Ejecuta sub-agente con contexto limpio.
        """
        # Sub-agente tiene su propio context window limpio
        sub_agent_messages = [
            SystemMessage(content=task.instructions),
            UserMessage(content=task.context)
        ]

        # Sub-agente explora extensamente (puede usar 50k tokens)
        response = llm.run(sub_agent_messages)

        # Pero retorna solo summary condensado (1-2k tokens)
        return {
            "summary": response.summary,
            "critical_issues": response.issues[:5],  # Top 5
            "recommendations": response.recommendations[:3]
        }
```

**Ventajas**:
- **Separation of concerns**: Cada sub-agente tiene contexto limpio
- **Parallelización**: Sub-agentes pueden correr simultáneamente
- **Expertise**: Sub-agentes especializados en subtareas
- **Token efficiency**: Main agent solo recibe resúmenes condensados

**Trade-off**: Mayor latencia (múltiples llamadas LLM) vs mejor calidad y token efficiency.

### Cuándo usar cada técnica

| Técnica | Best For | Pros | Cons |
|---------|----------|------|------|
| **Compaction** | Conversaciones largas, soporte chat | Simple, mantiene flujo | Pierde detalles finos |
| **Note-taking** | Desarrollo iterativo, tareas con milestones | Trackea progreso complejo | Requiere estructura |
| **Multi-agent** | Análisis/research con múltiples aspectos | Separation of concerns, paralelizable | Mayor latencia, más costoso |

---

## 🤖 Aplicación con IA (50%+ del contenido)

### Prompt Engineering para Agentes vs Chat

**Diferencia clave**: Los agentes tienen **autonomía y herramientas**, no solo generan texto.

**Chat LLM** (ChatGPT, Claude):
```
User: "Explícame qué es un índice en SQL"
LLM: "Un índice es una estructura de datos que mejora..."
```
→ One-shot, respuesta directa, sin estado

**Agent LLM** (Claude Code, AutoGPT):
```
User: "Optimiza las queries de este proyecto"
Agent:
  1. list_files("**/*.py")
  2. search_code("db.query")
  3. read_file("src/models.py")
  4. analyze_query_performance()
  5. edit_file("src/models.py", add_index)
  6. run_tests()
```
→ Multi-step, usa herramientas, mantiene estado

### System Prompts para Agentes: Estrategias Avanzadas

**1. Role + Constraints + Success Criteria**

```python
AGENT_SYSTEM_PROMPT = """
<role>
You are a senior Python backend developer specializing in FastAPI and SQLAlchemy.
</role>

<capabilities>
You have access to:
- File system operations (read, write, search)
- Code analysis tools (grep, AST parsing)
- Test execution (pytest)
- Git operations
</capabilities>

<constraints>
- Never modify files without running tests first
- Always check for existing tests before writing new ones
- Preserve backward compatibility in public APIs
- Use type hints and docstrings
</constraints>

<workflow>
When implementing features:
1. Understand requirements by reading existing code
2. Write tests first (TDD approach)
3. Implement minimal code to pass tests
4. Refactor for clarity
5. Run full test suite before finishing
</workflow>

<success_criteria>
A task is complete when:
- All tests pass
- Code coverage >= 80%
- No linting errors (ruff)
- Changes are documented
</success_criteria>
"""
```

**Por qué funciona**:
- **Claridad**: El agente sabe exactamente su rol
- **Guardrails**: Constraints previenen errores comunes
- **Workflow**: Guía el proceso de pensamiento
- **Verification**: Success criteria claros para auto-verificación

**2. Tool-Specific Guidance**

```python
TOOL_USAGE_GUIDELINES = """
<tool_usage>
When to use each tool:

- `search_code(pattern)`: Find all occurrences of a pattern
  Use when: You need to understand where/how something is used
  Don't use: If you already know the exact file

- `read_file(path)`: Read entire file
  Use when: You need full context of a file
  Don't use: For large files (>500 lines), use read_file_section instead

- `read_file_section(path, start_line, end_line)`: Read specific lines
  Use when: You found relevant code via search and need surrounding context

- `edit_file(path, old_content, new_content)`: Make precise edits
  Use when: Making targeted changes
  Don't use: For whole-file rewrites, use write_file instead
</tool_usage>

<anti_patterns>
❌ Reading all files in the project hoping to find something
   → Use search_code first to narrow down

❌ Making edits without reading the file first
   → Always read before editing to understand context

❌ Running tests after every tiny change
   → Batch changes, then test
</anti_patterns>
```

**3. Domain-Specific Knowledge**

```python
FASTAPI_AGENT_KNOWLEDGE = """
<fastapi_patterns>
Common patterns you should follow:

1. Dependency Injection
```python
# Good
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

2. Pydantic Models for Validation
```python
# Good
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    # email is validated, password length checked
```

3. Response Models
```python
# Good - separate response model
class UserResponse(BaseModel):
    id: int
    email: str
    # No password field!

@app.get("/users/{id}", response_model=UserResponse)
def get_user(id: int):
    return db.query(User).get(id)
```
</fastapi_patterns>

<common_mistakes>
- Returning ORM models directly (exposes all fields)
- Not using status codes correctly (use 201 for creation, 204 for deletion)
- Missing input validation (use Pydantic Field validators)
- Synchronous database calls in async endpoints
</common_mistakes>
```

### Prompt para Optimizar Contexto de un Agente Existente

```
Rol: Context engineering specialist para agentes IA

Contexto: Tengo un agente que [descripción del agente y su tarea].
Actualmente le paso [descripción del contexto actual].

El agente está fallando porque [descripción del problema]:
- [Problema específico 1]
- [Problema específico 2]

Objetivo: Optimiza el contexto para maximizar la efectividad del agente.

Analiza:
1. ¿Qué información es crítica y debe estar siempre en el contexto?
2. ¿Qué información se puede proveer on-demand (via tools)?
3. ¿Hay información redundante que se puede eliminar?
4. ¿El system prompt está en la "altitud" correcta?
5. ¿Los ejemplos (si los hay) son representativos y diversos?

Entrega:
- Nuevo system prompt optimizado
- Lista de tools necesarias
- Estrategia de retrieval (qué pre-cargar vs qué buscar on-demand)
- Ejemplos de 2-3 casos de uso bien resueltos

Restricciones:
- Contexto inicial debe ser <5000 tokens
- Tools deben retornar <1000 tokens por llamada
- Mantener capacidad de debugging (logs, error handling)
```

### Debugging de Contexto: Por Qué el Agente Falla

**Checklist de debugging**:

**1. Verificar token count**
```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Analizar contexto
system_prompt_tokens = count_tokens(system_prompt)
context_tokens = count_tokens(context_data)
total = system_prompt_tokens + context_tokens

print(f"""
Context Analysis:
- System prompt: {system_prompt_tokens} tokens
- Context data: {context_tokens} tokens
- Total: {total} tokens
- Model limit: 200,000 tokens
- Usage: {(total/200000)*100:.1f}%
""")

if total > 100_000:
    print("⚠️  WARNING: High context usage, accuracy may degrade")
```

**2. Verificar información crítica al final**

```python
def analyze_context_position(context: str, critical_terms: list[str]):
    """
    Verifica si información crítica está al final (context rot zone).
    """
    lines = context.split('\n')
    total_lines = len(lines)

    for term in critical_terms:
        for i, line in enumerate(lines):
            if term in line:
                position_pct = (i / total_lines) * 100
                if position_pct > 70:
                    print(f"⚠️  '{term}' found at {position_pct:.0f}% (at-risk zone)")
                else:
                    print(f"✅ '{term}' found at {position_pct:.0f}% (safe zone)")
```

**3. Audit de tool usage**

```python
def audit_tool_calls(agent_trace: list):
    """
    Analiza patrón de uso de tools para detectar ineficiencias.
    """
    tool_stats = {}

    for call in agent_trace:
        tool_name = call['tool']
        tool_stats[tool_name] = tool_stats.get(tool_name, 0) + 1

    print("Tool Usage Analysis:")
    for tool, count in sorted(tool_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {tool}: {count} calls")

    # Detectar anti-patterns
    if tool_stats.get('read_file', 0) > 20:
        print("⚠️  WARNING: Too many read_file calls, consider caching")

    if tool_stats.get('search_code', 0) > tool_stats.get('read_file', 0):
        print("✅ Good: More searches than reads (efficient exploration)")
```

**4. Prompt iteration basada en failure modes**

```python
class PromptEvolver:
    """
    Itera system prompts basándose en fallos observados.
    """

    def __init__(self):
        self.version = 1
        self.failures = []

    def log_failure(self, failure_description: str, agent_output: str):
        self.failures.append({
            "version": self.version,
            "failure": failure_description,
            "output": agent_output
        })

    def evolve_prompt(self, current_prompt: str) -> str:
        """
        Usa LLM para mejorar prompt basado en failures.
        """
        failures_summary = "\n".join([
            f"- {f['failure']}" for f in self.failures
            if f['version'] == self.version
        ])

        evolution_prompt = f"""
        Current system prompt (v{self.version}):
        ```
        {current_prompt}
        ```

        Observed failures:
        {failures_summary}

        Generate an improved system prompt (v{self.version + 1}) that addresses these failures.
        Add specific instructions or constraints to prevent these issues.
        """

        new_prompt = llm.generate(evolution_prompt)
        self.version += 1
        return new_prompt
```

### Chain-of-Thought para Agentes

**Standard CoT** (para chat):
```
Q: "¿Cuántas ventanas tiene el Empire State Building?"

Let's think step by step:
1. El Empire State Building tiene 102 pisos
2. Cada piso tiene aproximadamente 40 ventanas
3. 102 × 40 = 4,080 ventanas
```

**Agentic CoT** (para agentes con tools):

```python
AGENTIC_COT_PROMPT = """
<thinking_process>
When solving complex tasks, use this structured thinking:

1. **Understand**: What is the user asking for?
   - Restate the goal in your own words
   - Identify success criteria

2. **Explore**: What information do I need?
   - What do I know already?
   - What do I need to find out?
   - Which tools can help?

3. **Plan**: What's the strategy?
   - Break task into subtasks
   - Order subtasks by dependencies
   - Identify potential blockers

4. **Execute**: Carry out the plan
   - Execute one subtask at a time
   - Verify each step before proceeding
   - Adapt if blockers arise

5. **Verify**: Did I achieve the goal?
   - Check against success criteria
   - Run tests if applicable
   - Document what was done
</thinking_process>

<example>
User: "Add JWT authentication to the /users endpoint"

Agent thinking:
1. Understand: Need to protect /users endpoint with JWT tokens
   Success: Only requests with valid JWT can access the endpoint

2. Explore:
   - Do we have JWT utilities? → search_code("jwt")
   - How are other endpoints protected? → search_code("Depends")
   - What's the user model? → read_file("models.py")

3. Plan:
   a. Create JWT dependency function
   b. Add dependency to endpoint
   c. Write tests for auth + non-auth cases
   d. Update documentation

4. Execute:
   [Agent proceeds with tool calls]

5. Verify:
   - Run tests → All pass
   - Test endpoint manually with/without token
   - Document in API docs
</example>
"""
```

**Ventajas**:
- Más transparente para debugging
- Agente auto-corrige cuando detecta errores en su razonamiento
- Fácil de auditar el proceso de pensamiento

---

## 🧪 Proyecto práctico: Optimiza un agente de code review

### Objetivo

Tienes un agente de code review que está fallando porque recibe demasiado contexto. Vas a optimizarlo usando context engineering.

### Estado inicial (❌ Ineficiente)

```python
# agent_v1.py - VERSION INEFICIENTE

SYSTEM_PROMPT = """
You are a code reviewer. Review the code.
"""

def review_pull_request(pr_files: list[str]) -> str:
    # Cargar TODO el código en el contexto
    context = ""
    for file in pr_files:
        context += f"\n\n=== {file} ===\n"
        context += open(file).read()

    # Puede ser 50,000+ tokens
    response = llm.generate(
        system=SYSTEM_PROMPT,
        user=f"Review this code:\n{context}"
    )

    return response

# Problemas:
# - System prompt muy vago
# - Carga todos los archivos (incluso no modificados)
# - Sin guía de qué buscar
# - Sin ejemplos de buenas reviews
```

### Tarea 1: Optimizar System Prompt

**Objetivo**: Mejorar system prompt con estructura clara.

```python
# Tu implementación aquí
SYSTEM_PROMPT_V2 = """
<role>
[Define el rol del agente]
</role>

<review_criteria>
[Qué debe revisar: security, performance, style, etc.]
</review_criteria>

<guidelines>
[Cómo debe presentar feedback]
</guidelines>
"""
```

**Criterios de éxito**:
- System prompt <1000 tokens
- Incluye criterios específicos (no vago)
- Tiene ejemplos de reviews bien hechas

### Tarea 2: Dynamic Context Retrieval

**Objetivo**: Solo cargar archivos modificados, no todo el proyecto.

```python
def get_modified_files(pr_number: int) -> list[str]:
    """
    Obtener solo archivos modificados en el PR.
    """
    # Tu implementación aquí
    pass

def get_file_diff(file_path: str) -> str:
    """
    Obtener solo las líneas modificadas (diff), no el archivo completo.
    """
    # Tu implementación aquí
    pass

def review_pull_request_v2(pr_number: int) -> str:
    # 1. Obtener solo archivos modificados
    modified_files = get_modified_files(pr_number)

    # 2. Obtener solo diffs
    diffs = {f: get_file_diff(f) for f in modified_files}

    # 3. Context es mucho más pequeño
    context = format_diffs(diffs)

    response = llm.generate(
        system=SYSTEM_PROMPT_V2,
        user=f"Review these changes:\n{context}"
    )

    return response
```

**Criterios de éxito**:
- Contexto <5000 tokens (vs 50k inicial)
- Solo carga archivos modificados
- Solo incluye diffs, no archivos completos

### Tarea 3: Tools para Exploración On-Demand

**Objetivo**: Dar tools al agente para explorar el código cuando necesite más contexto.

```python
from typing import Literal

class CodeExplorationTools:
    """
    Tools que el agente puede usar para explorar el codebase.
    """

    def search_definition(self, symbol: str) -> str:
        """
        Busca la definición de una función/clase.

        Args:
            symbol: Nombre de función o clase a buscar

        Returns:
            Código de la definición + ubicación
        """
        # Tu implementación aquí
        pass

    def get_function_usages(self, function_name: str) -> list[dict]:
        """
        Encuentra dónde se usa una función.

        Returns:
            Lista de ubicaciones donde se llama la función
        """
        # Tu implementación aquí
        pass

    def get_test_coverage(self, file_path: str) -> dict:
        """
        Obtiene coverage de tests para un archivo.

        Returns:
            {"coverage_percent": 85, "uncovered_lines": [23, 45, 67]}
        """
        # Tu implementación aquí
        pass

# Usar en el agente
def review_with_tools(pr_number: int) -> str:
    tools = CodeExplorationTools()

    agent = Agent(
        system_prompt=SYSTEM_PROMPT_V2,
        tools=[
            tools.search_definition,
            tools.get_function_usages,
            tools.get_test_coverage
        ]
    )

    # Agente puede explorar autónomamente cuando necesite contexto
    response = agent.run(f"Review PR #{pr_number}")

    return response
```

**Criterios de éxito**:
- Al menos 3 tools disponibles
- Tools retornan <500 tokens cada uno
- Agente usa tools solo cuando necesita más contexto

### Tarea 4: Few-Shot Examples

**Objetivo**: Dar ejemplos de buenas reviews para guiar al agente.

```python
FEW_SHOT_EXAMPLES = """
<example_1>
Code:
```python
@app.post("/users")
def create_user(email: str, password: str):
    user = User(email=email, password=password)
    db.add(user)
    return user
```

Review:
🔴 CRITICAL Security Issues:
1. Password stored in plaintext
   - Use password hashing: `bcrypt.hashpw(password.encode(), bcrypt.gensalt())`
2. No input validation
   - Use Pydantic model: `class UserCreate(BaseModel): email: EmailStr; password: str = Field(min_length=8)`
3. Missing status code
   - Add `status_code=201` for resource creation

⚠️  Best Practices:
- Return response model (don't expose password)
- Use dependency injection for database session
</example_1>

<example_2>
Code:
```python
@app.get("/posts")
def get_posts():
    posts = db.query(Post).all()
    for post in posts:
        post.author = db.query(User).get(post.author_id)  # N+1 query
    return posts
```

Review:
🔴 CRITICAL Performance Issue:
- N+1 query problem detected
- Loading authors one-by-one in loop
- Solution: Use eager loading
  ```python
  posts = db.query(Post).options(joinedload(Post.author)).all()
  ```

✅ Good:
- Appropriate HTTP method (GET for reading)
- Clean function name
</example_2>
"""

SYSTEM_PROMPT_V3 = SYSTEM_PROMPT_V2 + f"\n\n{FEW_SHOT_EXAMPLES}"
```

**Criterios de éxito**:
- 2-3 ejemplos diversos
- Cada ejemplo muestra patrón diferente (security, performance, style)
- Ejemplos <2000 tokens totales

### Comparación Before/After

**Before (v1)**:
```
Token usage: 52,000 tokens
Review quality: Generic, miss issues
Time: 45 seconds
Cost: $0.50 per review
```

**After (v3)**:
```
Token usage: 6,500 tokens (87% reduction)
Review quality: Specific, catches critical issues
Time: 12 seconds (73% faster)
Cost: $0.06 per review (88% cheaper)
```

**Mejoras logradas**:
- ✅ 87% reducción de tokens
- ✅ 73% más rápido
- ✅ 88% más barato
- ✅ Mejor calidad (más específico y relevante)

---

## ✅ Checklist de la Clase 6.6

### Fundamentos (obligatorio)

- [ ] Entiendes qué es context engineering y por qué importa
- [ ] Comprendes el concepto de "context rot" y attention budget
- [ ] Sabes la diferencia entre prompt engineering y context engineering
- [ ] Identificas cuándo un system prompt está "too high" o "too low"
- [ ] Implementaste dynamic retrieval (on-demand vs pre-carga)

### Técnicas avanzadas

- [ ] Aplicaste al menos una técnica de horizonte largo (compaction, notes, o sub-agents)
- [ ] Diseñaste tools token-efficient para un agente
- [ ] Creaste examples canónicos para few-shot learning
- [ ] Implementaste debugging de contexto (token counting, position analysis)

### Proyecto práctico

- [ ] Optimizaste un agente existente reduciendo tokens >50%
- [ ] Mediste mejora en calidad/velocidad/costo
- [ ] Documentaste before/after con métricas
- [ ] Comparaste diferentes estrategias de retrieval

### Integración con IA (50%+)

- [ ] Usaste IA para generar system prompts optimizados
- [ ] Prompt iteration basada en failure modes
- [ ] IA te ayudó a diseñar tools
- [ ] Generaste ejemplos few-shot con IA
- [ ] Documentaste qué prompts fueron más efectivos

---

## 🎯 Conceptos clave para recordar

1. **Context es un recurso escaso**: Cada token compite por atención
2. **More is not better**: Más contexto ≠ mejor rendimiento (context rot)
3. **Just-in-time retrieval**: Trae información solo cuando la necesitas
4. **System prompt altitude matters**: Ni muy específico ni muy vago
5. **Tools should be token-efficient**: Retornar referencias, no contenido completo
6. **Long-horizon needs special techniques**: Compaction, notes, o sub-agents
7. **Iterate based on failures**: Prompts evolucionan basados en problemas observados

---

## 📖 Recursos adicionales

**Artículos de Anthropic**:
- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (artículo base)
- [Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [Claude Context Window Specs](https://docs.anthropic.com/en/docs/about-claude/models)

**Herramientas útiles**:
- `tiktoken`: Count tokens for different models
- Anthropic Memory Cookbook: Implementation examples
- LangChain Context Compression: Pre-built solutions

**Papers relevantes**:
- "Lost in the Middle" (context rot research)
- "Many-Shot Learning" (scaling few-shot examples)
- "Retrieval-Augmented Generation" (RAG patterns)

---

## 🚀 Próxima clase

**Clase 6.7: Writing Tools for AI Agents**

En la próxima clase aprenderás:
- Diseñar herramientas efectivas para agentes
- Patrones de tool design (input validation, error handling)
- Tool composition y chaining
- Testing y debugging de tools

---

¡Felicitaciones! Ahora dominas context engineering y puedes crear agentes IA mucho más efectivos y eficientes. 🚀
