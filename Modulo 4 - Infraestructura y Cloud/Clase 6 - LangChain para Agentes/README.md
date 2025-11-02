# Clase 6: LangChain y Agent Skills - Frameworks Modernos para Agentes IA

## Índice

1. [Introducción](#introducción)
2. [La Evolución de los Frameworks de Agentes](#la-evolución-de-los-frameworks-de-agentes)
3. [Agent Skills de Anthropic](#agent-skills-de-anthropic)
4. [LangChain: El Framework Tradicional](#langchain-el-framework-tradicional)
5. [Comparación: Agent Skills vs LangChain](#comparación-agent-skills-vs-langchain)
6. [Memory en Agentes IA](#memory-en-agentes-ia)
7. [RAG (Retrieval-Augmented Generation) Básico](#rag-retrieval-augmented-generation-básico)
8. [MCP (Model Context Protocol)](#mcp-model-context-protocol)
9. [Proyecto: Agente de Asistencia al Desarrollo](#proyecto-agente-de-asistencia-al-desarrollo)
10. [Ejercicios Prácticos con IA](#ejercicios-prácticos-con-ia)

---

## Introducción

**"A solo developer with an army of agents"** - Esta es la visión del futuro del desarrollo de software. Para lograrlo, necesitas dominar los frameworks que permiten **orquestar agentes IA** efectivamente.

### ¿Qué aprenderás en esta clase?

En las últimas dos clases aprendiste:
- **Clase 6.6**: Cómo diseñar contexto efectivo para agentes (Context Engineering)
- **Clase 6.7**: Cómo escribir tools que los agentes pueden usar

Ahora darás el siguiente paso: **construir agentes completos** usando dos paradigmas complementarios:

1. **Agent Skills** (Anthropic) - El nuevo paradigma basado en conocimiento modular
2. **LangChain** - El framework tradicional basado en composición de chains

### ¿Por qué dos frameworks?

No es "uno u otro" - son **complementarios**:

- **Agent Skills** → Excelente para **workflows complejos** que requieren conocimiento procedimental
- **LangChain** → Excelente para **orchestración de tools** y pipelines de procesamiento

Un desarrollador moderno debe dominar **ambos** y saber cuándo usar cada uno.

### Analogía: Arquitectura de Software

Piensa en estos frameworks como patrones arquitectónicos:

| Framework | Analogía | Cuándo Usar |
|-----------|----------|-------------|
| **Agent Skills** | **Microservicios** con documentación viva | Workflows con muchos pasos, conocimiento específico de dominio |
| **LangChain** | **Pipeline de datos** con transformaciones | Procesamiento secuencial, integración de múltiples APIs/LLMs |

---

## La Evolución de los Frameworks de Agentes

### Primera Generación: Prompt Engineering Manual (2020-2022)

```python
# Agente "hardcodeado" con prompts estáticos
def simple_agent(query: str) -> str:
    prompt = f"""
    Eres un asistente que responde preguntas.

    Pregunta: {query}

    Respuesta:
    """
    return llm.generate(prompt)
```

**Problemas**:
- ❌ No puede usar herramientas externas
- ❌ Sin memoria entre conversaciones
- ❌ Limitado por el conocimiento del LLM (cutoff date)
- ❌ No puede razonar paso a paso

### Segunda Generación: Agents con Tools (2022-2023)

Frameworks como **LangChain** introdujeron **tool calling**:

```python
from langchain.agents import create_react_agent

# Agente que puede llamar tools
agent = create_react_agent(
    llm=llm,
    tools=[search_tool, calculator_tool, python_repl],
    prompt=prompt_template
)

agent.run("¿Cuál es la raíz cuadrada de 2024 multiplicada por el PIB de España en 2023?")
# El agente razona: necesito buscar PIB de España → usar calculator → retornar resultado
```

**Avances**:
- ✅ Puede usar herramientas externas
- ✅ Razonamiento paso a paso (ReAct pattern)
- ✅ Acceso a información actualizada

**Limitaciones**:
- ❌ Context window limitado (todos los tools en el prompt)
- ❌ Difícil escalar a 100+ tools
- ❌ No hay "conocimiento procedimental" estructurado

### Tercera Generación: Agent Skills + MCP (2024+)

**Agent Skills** de Anthropic introduce **progressive disclosure**:

```
.claude/skills/
├── pdf-processing/
│   ├── SKILL.md          # Conocimiento sobre procesamiento de PDFs
│   ├── forms.md          # Tipos de formularios comunes
│   └── extract.py        # Script de extracción
├── financial-analysis/
│   ├── SKILL.md
│   ├── ratios.md
│   └── validate.py
└── code-review/
    ├── SKILL.md
    └── checklist.md
```

**Innovación clave**: El agente carga **solo lo que necesita** en cada momento.

---

## Agent Skills de Anthropic

### ¿Qué son los Agent Skills?

**Agent Skills** son **paquetes modulares de capacidades** que extienden las habilidades de Claude. Cada skill es un directorio con:

1. **SKILL.md** - Descripción del skill + instrucciones procedimentales
2. **Archivos de soporte** (opcionales) - Referencias, ejemplos, scripts Python

### Arquitectura: Progressive Disclosure

La clave de Agent Skills es **cargar información por capas**:

```
┌─────────────────────────────────────────────┐
│  Nivel 1: Metadata (siempre en prompt)     │
│  - Nombres de skills disponibles           │
│  - Descripciones cortas                    │
└─────────────────────────────────────────────┘
          ↓ (Claude decide que skill es relevante)
┌─────────────────────────────────────────────┐
│  Nivel 2: SKILL.md completo                │
│  - Instrucciones detalladas                │
│  - Workflows paso a paso                   │
│  - Referencias a archivos de soporte       │
└─────────────────────────────────────────────┘
          ↓ (Claude necesita más detalle)
┌─────────────────────────────────────────────┐
│  Nivel 3: Archivos de soporte             │
│  - forms.md, reference.md, etc.            │
│  - Scripts Python ejecutables              │
└─────────────────────────────────────────────┘
```

**Ventaja**: Context window se usa eficientemente - solo carga lo necesario.

### Anatomía de un Agent Skill

**Estructura de `SKILL.md`**:

```markdown
---
name: PDF Form Processor
description: Extract and validate data from PDF forms
---

# PDF Form Processing Skill

## When to Use This Skill

Use this skill when you need to:
- Extract data from PDF forms
- Validate extracted information
- Fill PDF forms programmatically

**DO NOT use for**:
- Reading plain text PDFs (use standard PDF reading instead)
- OCR of scanned documents (use vision models)

## Prerequisites

- Python 3.12+
- PyPDF2 library installed
- Forms must be digital (not scanned images)

## Workflow

### Step 1: Identify Form Type

Common form types:
- W-2 (Tax form) → See `tax_forms.md` for fields
- Invoice → See `invoice_fields.md`
- Application form → Generic extraction

### Step 2: Extract Fields

Use the `extract.py` script:

```bash
python extract.py --input form.pdf --type w2
```

Expected output:
```json
{
  "employer_name": "Acme Corp",
  "wages": "75000.00",
  "tax_withheld": "12000.00"
}
```

### Step 3: Validate Extracted Data

Run validation checks:
- Numeric fields are valid numbers
- Required fields are present
- Checksums match (if applicable)

See `validation_rules.md` for complete checklist.

## Error Handling

**Common errors**:

| Error | Cause | Solution |
|-------|-------|----------|
| `PDFReadError` | Encrypted PDF | Ask user for password |
| `KeyError: 'field_name'` | Form field not found | Check form type mapping |
| `ValueError: invalid literal` | Non-numeric value | Report to user for correction |

## Examples

See `examples/` directory for:
- `w2_extraction.py` - Complete W-2 extraction
- `invoice_processing.py` - Invoice data extraction

## Related Skills

- `financial-analysis` - For analyzing extracted financial data
- `data-validation` - For advanced validation rules
```

### Creando Tu Primer Agent Skill

**Ejemplo: Skill para Code Review**

**Paso 1**: Crear estructura

```bash
mkdir -p .claude/skills/code-review
cd .claude/skills/code-review
```

**Paso 2**: Escribir `SKILL.md`

```markdown
---
name: Code Review Assistant
description: Perform comprehensive code reviews following best practices
---

# Code Review Skill

## When to Use

Use this skill when reviewing:
- Pull requests before merge
- Refactoring proposals
- Security-sensitive code changes

## Review Checklist

### 1. Architecture & Design

- [ ] **Single Responsibility**: Each class/function does one thing
- [ ] **Dependency Inversion**: Depends on abstractions, not concretions
- [ ] **Open/Closed**: Open for extension, closed for modification

### 2. Code Quality

- [ ] **Naming**: Variables/functions have clear, descriptive names
- [ ] **Complexity**: Cyclomatic complexity < 10 per function
- [ ] **DRY**: No code duplication (3+ lines repeated)

### 3. Testing

- [ ] **Coverage**: Critical paths have tests (>80% coverage)
- [ ] **Test Quality**: Tests are isolated, deterministic
- [ ] **Edge Cases**: Error conditions are tested

### 4. Security

- [ ] **Input Validation**: All user inputs validated
- [ ] **SQL Injection**: Parameterized queries used
- [ ] **Secrets**: No hardcoded credentials

### 5. Performance

- [ ] **N+1 Queries**: No database query loops
- [ ] **Caching**: Expensive operations cached
- [ ] **Async I/O**: Blocking operations are async

## Severity Levels

- **🔴 Critical**: Security vulnerabilities, data loss risks
- **🟡 Major**: Performance issues, maintainability problems
- **🟢 Minor**: Style inconsistencies, suggestions

## Example Review

```python
# Code being reviewed
def get_user_orders(user_id: str) -> list[Order]:
    user = db.query(User).get(user_id)
    orders = []
    for order_id in user.order_ids:
        order = db.query(Order).get(order_id)  # ⚠️ N+1 query!
        orders.append(order)
    return orders
```

**Review output**:

```
🟡 MAJOR: N+1 Query Detected

**Issue**: Line 5 executes a database query inside a loop, causing N+1 queries.

**Impact**: Performance degrades linearly with number of orders (100 orders = 101 queries).

**Fix**:
```python
def get_user_orders(user_id: str) -> list[Order]:
    user = db.query(User).get(user_id)
    # Single query with eager loading
    orders = db.query(Order).filter(
        Order.id.in_(user.order_ids)
    ).all()
    return orders
```

**Reference**: See `performance_patterns.md` section 3.2
```

## Integration with Tools

Skills can bundle **executable scripts** as tools:

**`extract.py`**:

```python
#!/usr/bin/env python3
"""
PDF extraction tool for Agent Skills.

This script is invoked by Claude when processing PDFs.
"""

import sys
import json
from pathlib import Path
from PyPDF2 import PdfReader

def extract_form_data(pdf_path: str, form_type: str) -> dict:
    """Extract structured data from PDF form."""
    reader = PdfReader(pdf_path)

    # Get form fields
    fields = reader.get_form_text_fields()

    # Map to standard schema
    if form_type == "w2":
        return {
            "employer_name": fields.get("employer_name"),
            "wages": fields.get("wages"),
            "tax_withheld": fields.get("federal_tax")
        }

    return fields

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--type", required=True)
    args = parser.parse_args()

    result = extract_form_data(args.input, args.type)
    print(json.dumps(result, indent=2))
```

**Claude invoca el script así**:

```python
# Claude genera este código cuando necesita extraer un PDF
result = subprocess.run(
    ["python", "extract.py", "--input", "form.pdf", "--type", "w2"],
    capture_output=True,
    text=True
)
data = json.loads(result.stdout)
```

### Best Practices para Agent Skills

#### 1. Diseñar para Descubrimiento

**❌ Mal nombre/descripción**:

```yaml
---
name: Processor
description: Processes things
---
```

**✅ Buen nombre/descripción**:

```yaml
---
name: Financial Statement Analyzer
description: Analyze balance sheets, income statements, and cash flow statements using GAAP standards
---
```

#### 2. Estructurar Iterativamente

**Señales de que un skill está "creciendo demasiado"**:
- SKILL.md > 500 líneas
- Múltiples workflows no relacionados
- Instrucciones contradictorias

**Solución**: Split en archivos de referencia

```
financial-analysis/
├── SKILL.md               # Overview + workflow principal
├── balance_sheet.md       # Análisis de balance
├── income_statement.md    # Análisis de ingresos
├── cash_flow.md          # Análisis de flujo de caja
└── ratios.md             # Ratios financieros
```

**En SKILL.md**:

```markdown
## Análisis de Balance Sheet

Para analizar un balance sheet:

1. Identifica las secciones principales (ver `balance_sheet.md` sección 1)
2. Calcula ratios de liquidez (ver `ratios.md` sección 2.1)
3. Compara con industria benchmarks (ver `balance_sheet.md` sección 3)
```

#### 3. Security-First

**Validar TODOS los skills antes de deployment**:

```python
# Auditoría automática de skills
def audit_skill(skill_path: Path) -> list[str]:
    """Audita un skill buscando problemas de seguridad."""
    issues = []

    skill_md = skill_path / "SKILL.md"
    content = skill_md.read_text()

    # Buscar patrones peligrosos
    dangerous_patterns = [
        r"os\.system\(",           # Ejecución de shell
        r"eval\(",                  # Code injection
        r"exec\(",                  # Code execution
        r"__import__\(",            # Import dinámico
        r"subprocess\.call.*shell=True"  # Shell injection
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, content):
            issues.append(f"⚠️ Dangerous pattern found: {pattern}")

    # Verificar scripts Python
    for script in skill_path.glob("*.py"):
        code = script.read_text()
        # Run bandit security linter
        result = subprocess.run(
            ["bandit", "-r", str(script)],
            capture_output=True
        )
        if result.returncode != 0:
            issues.append(f"🔴 Security issue in {script.name}")

    return issues
```

#### 4. Versionado de Skills

**Problema**: Skills evolucionan → versiones antiguas pueden romper workflows

**Solución**: Metadata de versión

```yaml
---
name: PDF Form Processor
description: Extract and validate data from PDF forms
version: 2.1.0
min_claude_version: "3.5"
dependencies:
  - PyPDF2>=3.0.0
  - pydantic>=2.0.0
changelog: |
  2.1.0 (2025-10-20):
    - Added support for encrypted PDFs
    - Improved field detection accuracy
  2.0.0 (2025-09-15):
    - BREAKING: Changed output format to JSON
    - Added validation rules
---
```

---

## LangChain: El Framework Tradicional

### ¿Qué es LangChain?

**LangChain** es un framework para construir aplicaciones con LLMs mediante **composición de componentes**:

- **Chains**: Secuencias de pasos (prompts → LLM → parsers → output)
- **Agents**: Entidades que deciden qué tools usar
- **Memory**: Persistencia de contexto entre llamadas
- **Tools**: Funciones que el agente puede invocar

**Filosofía**: "LEGO blocks for LLMs" - componentes modulares que se conectan.

### Instalación

```bash
pip install langchain langchain-anthropic langchain-community
```

### Chains Básicos

#### Simple Chain: Prompt → LLM → Output

```python
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

# 1. Definir LLM
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.7
)

# 2. Definir prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente experto en {topic}"),
    ("user", "{question}")
])

# 3. Chain: prompt | llm | parser
chain = prompt | llm | StrOutputParser()

# 4. Ejecutar
result = chain.invoke({
    "topic": "Python",
    "question": "¿Cómo funciona el GIL (Global Interpreter Lock)?"
})

print(result)
```

**Output**:
```
El GIL (Global Interpreter Lock) es un mutex que protege el acceso a objetos Python,
previniendo que múltiples threads ejecuten bytecode Python simultáneamente...
```

#### Sequential Chain: Múltiples Pasos Encadenados

```python
from langchain.chains import LLMChain, SequentialChain

# Chain 1: Generar outline de artículo
outline_chain = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        "Genera un outline detallado para un artículo sobre: {topic}"
    ),
    output_key="outline"
)

# Chain 2: Escribir introducción basada en outline
intro_chain = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        "Escribe una introducción compelling basada en este outline:\n\n{outline}"
    ),
    output_key="introduction"
)

# Chain 3: Escribir conclusión
conclusion_chain = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        """
        Outline: {outline}
        Introducción: {introduction}

        Escribe una conclusión que conecte los puntos principales.
        """
    ),
    output_key="conclusion"
)

# Encadenar todo
full_chain = SequentialChain(
    chains=[outline_chain, intro_chain, conclusion_chain],
    input_variables=["topic"],
    output_variables=["outline", "introduction", "conclusion"]
)

# Ejecutar
result = full_chain({"topic": "Agent Skills vs LangChain"})

print("OUTLINE:", result["outline"])
print("\nINTRO:", result["introduction"])
print("\nCONCLUSION:", result["conclusion"])
```

### Agents y Tools en LangChain

#### Definir Tools

```python
from langchain.tools import Tool
from langchain.utilities import SerpAPIWrapper

# Tool 1: Búsqueda en internet
search = SerpAPIWrapper()
search_tool = Tool(
    name="Search",
    func=search.run,
    description="""
    Busca información actualizada en internet.
    Útil para: noticias recientes, datos en tiempo real, información no en el training data.
    Input: query de búsqueda (string)
    """
)

# Tool 2: Calculator
from langchain.tools import Tool

def calculator(expression: str) -> str:
    """Evalúa expresión matemática."""
    try:
        result = eval(expression, {"__builtins__": {}})  # Restricted eval
        return str(result)
    except Exception as e:
        return f"Error: {e}"

calculator_tool = Tool(
    name="Calculator",
    func=calculator,
    description="""
    Calcula expresiones matemáticas.
    Input: expresión Python válida (e.g., "2 + 2", "sqrt(16)", "10 ** 3")
    """
)

# Tool 3: Python REPL
from langchain.tools import PythonREPLTool

python_repl = PythonREPLTool()
```

#### Crear Agent con Tools

```python
from langchain.agents import create_react_agent, AgentExecutor

# Definir prompt del agente (ReAct pattern)
from langchain.prompts import PromptTemplate

react_prompt = PromptTemplate.from_template("""
Responde la siguiente pregunta usando las herramientas disponibles.

Herramientas:
{tools}

Formato de razonamiento (ReAct):

Thought: Razona sobre qué hacer
Action: Nombre de la herramienta a usar
Action Input: Input para la herramienta
Observation: Resultado de la herramienta
... (repite Thought/Action/Observation hasta tener la respuesta)
Thought: Ahora sé la respuesta final
Final Answer: La respuesta a la pregunta original

Pregunta: {input}

{agent_scratchpad}
""")

# Crear agent
tools = [search_tool, calculator_tool, python_repl]

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=react_prompt
)

# Wrapper para ejecutar el agent
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # Muestra el razonamiento paso a paso
    max_iterations=10
)

# Ejecutar consulta compleja
result = agent_executor.invoke({
    "input": "¿Cuál es el precio de las acciones de Apple hoy multiplicado por el número de días en octubre 2025?"
})
```

**Output (verbose=True)**:
```
> Entering new AgentExecutor chain...

Thought: Necesito dos piezas de información: precio de acciones de Apple y días en octubre 2025
Action: Search
Action Input: "precio acciones Apple hoy"

Observation: Apple (AAPL) cotiza a $175.23 USD (20 Oct 2025)

Thought: Ahora necesito calcular días en octubre 2025
Action: Calculator
Action Input: 31

Observation: 31

Thought: Ahora puedo calcular el resultado final
Action: Calculator
Action Input: 175.23 * 31

Observation: 5432.13

Thought: Tengo la respuesta final
Final Answer: El precio de las acciones de Apple ($175.23) multiplicado por los días de octubre (31) es $5,432.13

> Finished chain.
```

### Custom Tools en LangChain

```python
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

# Schema de input con Pydantic
class SearchCodeInput(BaseModel):
    query: str = Field(description="Texto a buscar en el código")
    file_pattern: str = Field(
        default="*.py",
        description="Patrón glob para filtrar archivos"
    )

# Custom tool
class SearchCodeTool(BaseTool):
    name: str = "search_codebase"
    description: str = """
    Busca código en el repositorio usando grep.
    Útil para encontrar definiciones de funciones, imports, o referencias a variables.
    """
    args_schema: Type[BaseModel] = SearchCodeInput

    def _run(self, query: str, file_pattern: str = "*.py") -> str:
        """Ejecuta búsqueda en el codebase."""
        import subprocess

        result = subprocess.run(
            ["grep", "-r", "--include", file_pattern, query, "."],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return f"No se encontró '{query}' en archivos {file_pattern}"

        # Limitar resultados a 10 líneas
        lines = result.stdout.split("\n")[:10]
        return "\n".join(lines)

# Usar el tool
search_code_tool = SearchCodeTool()
result = search_code_tool._run("def calculate_total", "api/**/*.py")
print(result)
```

---

## Comparación: Agent Skills vs LangChain

### Tabla Comparativa

| Aspecto | Agent Skills | LangChain |
|---------|-------------|-----------|
| **Paradigma** | Knowledge-based (markdown + scripts) | Code-based (Python chains) |
| **Context Management** | Progressive disclosure (lazy loading) | All-or-nothing (todos los tools en prompt) |
| **Escalabilidad** | ✅ Ilimitada (filesystem-based) | ⚠️ Limitada por context window |
| **Complejidad de Workflows** | ✅ Excelente (instrucciones procedimentales) | ⚠️ Requiere código para orquestar |
| **Curva de Aprendizaje** | 🟢 Baja (escribir markdown) | 🟡 Media (API de LangChain) |
| **Flexibilidad de Tools** | ⚠️ Solo lo que se puede documentar | ✅ Cualquier función Python |
| **Debugging** | 🟡 Difícil (decisiones del agente) | 🟢 Fácil (stack traces estándar) |
| **Versionado** | 🟢 Fácil (archivos Git) | 🟢 Fácil (código Git) |
| **Testing** | 🟡 Complejo (E2E con agente) | ✅ Unit tests estándar |
| **Multi-LLM Support** | ⚠️ Anthropic Claude solo | ✅ Soporta OpenAI, Anthropic, etc. |

### Cuándo Usar Cada Uno

#### Usa Agent Skills Si:

✅ **Tienes workflows complejos con muchos pasos procedimentales**

Ejemplo: "Analizar un contrato legal requiere revisar 15 secciones diferentes, cada una con criterios específicos"

```markdown
# Contract Review Skill

## Workflow

1. **Identify contract type** (see `contract_types.md`)
2. **Check standard clauses** (see `standard_clauses.md`)
3. **Validate legal requirements** by jurisdiction
4. **Flag non-standard terms** (see `red_flags.md`)
...
```

✅ **Necesitas escalar a 50+ skills sin saturar el context window**

Agent Skills carga solo lo relevante → puedes tener 100+ skills disponibles.

✅ **Conocimiento de dominio es más importante que lógica de código**

Ejemplo: "Cómo interpretar un formulario fiscal W-2" es conocimiento procedimental, no código.

#### Usa LangChain Si:

✅ **Necesitas orquestar múltiples LLMs o APIs**

```python
# Chain que usa 2 LLMs diferentes
translation_chain = LLMChain(llm=opus, prompt=translate_prompt)
refinement_chain = LLMChain(llm=sonnet, prompt=refine_prompt)

full_chain = translation_chain | refinement_chain
```

✅ **Tu workflow es principalmente transformaciones de datos**

Ejemplo: "Extraer entidades → normalizar formatos → almacenar en DB"

✅ **Necesitas testing granular y debugging fácil**

LangChain chains son código Python → puedes hacer unit tests normales.

✅ **Quieres usar LLMs de múltiples providers**

LangChain abstrae diferencias entre OpenAI, Anthropic, Cohere, etc.

### Arquitectura Híbrida (Recomendado)

**Lo mejor de ambos mundos**: Usa Agent Skills para workflows + LangChain para orchestración.

```python
from langchain.agents import create_react_agent
from langchain.tools import Tool

# Tool 1: Invoca Agent Skill para code review
def code_review_with_skill(code: str) -> str:
    """
    Usa Agent Skill de code review.

    Internamente carga:
    - .claude/skills/code-review/SKILL.md
    - .claude/skills/code-review/checklist.md
    """
    # El agente con Agent Skills ejecuta el review
    return claude_with_skills.review_code(code)

code_review_tool = Tool(
    name="code_review",
    func=code_review_with_skill,
    description="Perform comprehensive code review using industry best practices"
)

# Tool 2: Ejecutar tests (Python puro, no necesita skill)
def run_tests(test_file: str) -> str:
    result = subprocess.run(["pytest", test_file], capture_output=True)
    return result.stdout.decode()

test_tool = Tool(
    name="run_tests",
    func=run_tests,
    description="Run pytest tests and return results"
)

# Agent LangChain que orquesta ambos
tools = [code_review_tool, test_tool]
agent = create_react_agent(llm=llm, tools=tools, prompt=react_prompt)

# Workflow híbrido
result = agent.invoke({
    "input": "Review el código en api/tasks.py y ejecuta los tests correspondientes"
})
```

**Resultado**:
1. LangChain agent decide usar `code_review_tool` primero
2. `code_review_tool` invoca Agent Skill (carga workflow de code review)
3. Agent Skill retorna lista de issues
4. LangChain agent decide ejecutar tests con `test_tool`
5. Combina resultados de ambos

---

## Memory en Agentes IA

### ¿Por qué Memoria?

Los LLMs son **stateless** - cada llamada es independiente. Para conversaciones coherentes, necesitas **memoria**.

**Analogía**: Un LLM sin memoria es como un médico que no recuerda tu historial médico en cada visita.

### Tipos de Memoria

#### 1. ConversationBufferMemory (Memoria Completa)

Guarda **toda la conversación** sin modificar.

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

memory = ConversationBufferMemory()

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# Primera interacción
conversation.predict(input="Hola, me llamo Carlos")
# Output: "Hola Carlos, ¿en qué puedo ayudarte?"

# Segunda interacción
conversation.predict(input="¿Cuál es mi nombre?")
# Output: "Tu nombre es Carlos"
```

**Pros**:
- ✅ Contexto completo siempre disponible
- ✅ Simple de implementar

**Contras**:
- ❌ Consume context window rápidamente
- ❌ No escala para conversaciones largas (>50 mensajes)

#### 2. ConversationSummaryMemory (Memoria Resumida)

Usa un LLM para **resumir** la conversación periódicamente.

```python
from langchain.memory import ConversationSummaryMemory

memory = ConversationSummaryMemory(llm=llm)

conversation = ConversationChain(
    llm=llm,
    memory=memory
)

# Después de varios mensajes, la memoria contiene un resumen
conversation.predict("¿De qué hemos hablado hasta ahora?")
# Output: "Hemos discutido sobre Agent Skills, LangChain, y las diferencias entre ambos frameworks..."
```

**Pros**:
- ✅ Escala mejor que BufferMemory
- ✅ Mantiene contexto importante

**Contras**:
- ❌ Consume tokens extra (para generar resúmenes)
- ❌ Puede perder detalles específicos

#### 3. ConversationBufferWindowMemory (Ventana Deslizante)

Guarda solo los **últimos N mensajes**.

```python
from langchain.memory import ConversationBufferWindowMemory

# Mantener solo últimos 5 mensajes
memory = ConversationBufferWindowMemory(k=5)

conversation = ConversationChain(
    llm=llm,
    memory=memory
)
```

**Pros**:
- ✅ Context window predecible
- ✅ Bueno para conversaciones enfocadas

**Contras**:
- ❌ Olvida contexto antiguo
- ❌ No apto para workflows que referencian mensajes anteriores

#### 4. VectorStore Memory (Memoria Semántica)

Guarda mensajes en un **vector store** y recupera los más relevantes.

```python
from langchain.memory import VectorStoreRetrieverMemory
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# 1. Crear vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(
    ["Initial context"],
    embedding=embeddings
)

# 2. Crear retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 3. Crear memoria
memory = VectorStoreRetrieverMemory(retriever=retriever)

# Agregar contexto
memory.save_context(
    {"input": "Mi proyecto usa FastAPI y PostgreSQL"},
    {"output": "Entendido, trabajas con FastAPI y PostgreSQL"}
)

memory.save_context(
    {"input": "Necesito optimizar queries lentas"},
    {"output": "Puedo ayudarte con eso"}
)

# Recuperar contexto relevante
memory.load_memory_variables({"prompt": "¿Qué base de datos uso?"})
# Retorna: "Mi proyecto usa FastAPI y PostgreSQL" (recuperado por similitud semántica)
```

**Pros**:
- ✅ Escala a miles de mensajes
- ✅ Recupera contexto relevante semánticamente

**Contras**:
- ❌ Requiere embeddings (costo + latencia)
- ❌ No preserva orden cronológico

### Memoria en Agent Skills

Agent Skills usan **archivos de estado** para persistir información:

```
.claude/skills/financial-analysis/
├── SKILL.md
├── state/
│   ├── portfolio_20251020.json   # Estado del portfolio
│   └── preferences.json           # Preferencias del usuario
└── history/
    └── analyses_oct2025.md        # Historial de análisis
```

**En SKILL.md**:

```markdown
## State Management

### Portfolio State

Current portfolio is saved in `state/portfolio_YYYYMMDD.json`.

When user asks "¿Cuál es mi portfolio?":
1. Read latest `state/portfolio_*.json`
2. Summarize holdings
3. Calculate current value

### User Preferences

Saved in `state/preferences.json`:
```json
{
  "risk_tolerance": "moderate",
  "investment_horizon": "5 years",
  "sectors_avoid": ["tobacco", "weapons"]
}
```

Reference these preferences when making recommendations.
```

---

## RAG (Retrieval-Augmented Generation) Básico

### ¿Qué es RAG?

**RAG** combina:
1. **Retrieval** - Buscar documentos relevantes en una base de conocimiento
2. **Augmentation** - Agregar esos documentos al contexto del LLM
3. **Generation** - Generar respuesta basada en documentos + pregunta

**Analogía**: RAG es como un estudiante que puede consultar apuntes durante un examen (en lugar de solo usar memoria).

### Casos de Uso

- ✅ **Knowledge bases** - Responder preguntas sobre documentación interna
- ✅ **Customer support** - Responder basándose en tickets históricos
- ✅ **Legal/Medical** - Citar documentos específicos en respuestas
- ✅ **Code search** - Encontrar ejemplos de código similares

### Arquitectura RAG

```
┌─────────────────────────────────────────────┐
│  1. INDEXING PHASE (offline)               │
│                                             │
│  Documents → Chunking → Embeddings → DB    │
│  [doc1.txt]  [chunks]    [vectors]   [FAISS]│
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  2. RETRIEVAL PHASE (runtime)              │
│                                             │
│  Query → Embedding → Search → Top-K chunks │
│  "¿Cómo X?"  [vector]   [similarity] [3 docs]│
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  3. GENERATION PHASE                        │
│                                             │
│  Context: [doc1, doc2, doc3]               │
│  Query: "¿Cómo X?"                         │
│  → LLM generates answer                    │
└─────────────────────────────────────────────┘
```

### Implementación RAG Básica con LangChain

```python
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

# PASO 1: Cargar documentos
loader = DirectoryLoader(
    "docs/",
    glob="**/*.md",
    loader_cls=TextLoader
)
documents = loader.load()

print(f"Loaded {len(documents)} documents")

# PASO 2: Dividir en chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,        # Tamaño de cada chunk
    chunk_overlap=200,      # Overlap entre chunks (mantiene contexto)
    separators=["\n\n", "\n", " ", ""]
)
chunks = text_splitter.split_documents(documents)

print(f"Split into {len(chunks)} chunks")

# PASO 3: Crear embeddings y vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# (Opcional) Guardar para reutilizar
vectorstore.save_local("faiss_index")
# Cargar después: vectorstore = FAISS.load_local("faiss_index", embeddings)

# PASO 4: Crear retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}  # Retornar top 3 chunks más relevantes
)

# PASO 5: Crear QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",     # "stuff" = meter todos los docs en el prompt
    retriever=retriever,
    return_source_documents=True
)

# PASO 6: Hacer preguntas
query = "¿Cómo funcionan los Agent Skills?"
result = qa_chain({"query": query})

print("ANSWER:", result["result"])
print("\nSOURCES:")
for doc in result["source_documents"]:
    print(f"- {doc.metadata['source']}")
```

### Chain Types en RAG

LangChain ofrece 4 estrategias para combinar documentos:

#### 1. Stuff (Meter Todo)

Mete **todos los documentos** en un solo prompt.

```python
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever
)
```

**Pros**:
- ✅ Simple
- ✅ 1 sola llamada al LLM

**Contras**:
- ❌ Limitado por context window
- ❌ No escala si recuperas muchos documentos

#### 2. Map-Reduce

Procesa **cada documento por separado**, luego combina resultados.

```python
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="map_reduce",
    retriever=retriever
)
```

**Workflow**:
1. **Map**: Para cada doc, generar respuesta parcial
2. **Reduce**: Combinar todas las respuestas parciales

**Pros**:
- ✅ Escala a muchos documentos
- ✅ Procesa en paralelo (con async)

**Contras**:
- ❌ Múltiples llamadas al LLM (más caro)
- ❌ Puede perder coherencia entre docs

#### 3. Refine

Procesa documentos **secuencialmente**, refinando la respuesta.

```python
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="refine",
    retriever=retriever
)
```

**Workflow**:
1. Generar respuesta inicial con doc1
2. Refinar respuesta con doc2
3. Refinar respuesta con doc3
...

**Pros**:
- ✅ Mantiene coherencia
- ✅ Puede construir respuestas complejas

**Contras**:
- ❌ Secuencial (no paralelizable)
- ❌ Costoso (N llamadas al LLM)

#### 4. Map-Rerank

Genera respuestas con **score de confianza**, retorna la mejor.

```python
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="map_rerank",
    retriever=retriever
)
```

**Pros**:
- ✅ Bueno cuando solo 1 doc tiene la respuesta
- ✅ Retorna score de confianza

**Contras**:
- ❌ No combina información de múltiples docs
- ❌ Costoso

### RAG Avanzado: Reranking

**Problema**: La búsqueda por similitud vectorial no siempre retorna los mejores documentos.

**Solución**: **Reranking** con un modelo especializado.

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

# Retriever base (vector search)
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

# Compressor: Rerank con LLM
compressor = LLMChainExtractor.from_llm(llm)

# Retriever con reranking
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever
)

# Ahora retorna solo chunks REALMENTE relevantes
relevant_docs = compression_retriever.get_relevant_documents(
    "¿Cómo funcionan los Agent Skills?"
)
```

**Workflow**:
1. Buscar top-10 con vector search
2. Rerank con LLM (¿cuáles son MÁS relevantes?)
3. Retornar top-3 después de reranking

---

## MCP (Model Context Protocol)

### ¿Qué es MCP?

**MCP** (Model Context Protocol) es un **protocolo estándar** para conectar LLMs con fuentes de datos externas (APIs, bases de datos, sistemas de archivos, etc.).

**Analogía**: MCP es como USB - un estándar que permite conectar cualquier dispositivo (tool) a cualquier computadora (LLM).

### Arquitectura MCP

```
┌──────────────────────────────────────┐
│         LLM (Claude, GPT, etc.)     │
│                                      │
│   "Necesito datos de GitHub..."     │
└───────────────┬──────────────────────┘
                │ MCP Protocol
                ↓
┌──────────────────────────────────────┐
│        MCP Server (GitHub)           │
│                                      │
│  Tools:                              │
│  - list_repos()                      │
│  - get_issues()                      │
│  - create_pr()                       │
│                                      │
│  Resources:                          │
│  - README.md                         │
│  - CONTRIBUTING.md                   │
└──────────────────────────────────────┘
```

### Componentes de MCP

1. **Resources** - Archivos, datos, URIs que el LLM puede leer
2. **Tools** - Funciones que el LLM puede ejecutar
3. **Prompts** - Templates de prompts reutilizables

### Ejemplo: MCP Server para GitHub

```python
# mcp_github_server.py
from mcp.server import MCPServer
from mcp.types import Tool, Resource

server = MCPServer("github-mcp-server")

# Definir Tool
@server.tool(
    name="list_repos",
    description="List repositories for a GitHub user or organization"
)
async def list_repos(owner: str) -> list[dict]:
    """List GitHub repos."""
    import httpx

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/users/{owner}/repos"
        )
        repos = response.json()

        return [
            {
                "name": repo["name"],
                "description": repo["description"],
                "stars": repo["stargazers_count"],
                "url": repo["html_url"]
            }
            for repo in repos[:10]  # Top 10
        ]

# Definir Resource
@server.resource("readme://{owner}/{repo}")
async def get_readme(owner: str, repo: str) -> str:
    """Fetch README.md from a GitHub repo."""
    import httpx

    url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text

# Ejecutar server
if __name__ == "__main__":
    server.run()
```

### Cliente MCP (Claude Code)

Claude Code puede conectarse a MCP servers:

```python
# .claude/config.json
{
  "mcpServers": {
    "github": {
      "command": "python",
      "args": ["mcp_github_server.py"]
    }
  }
}
```

**Uso en Claude Code**:

```
User: "Lista los repos de anthropics en GitHub"

Claude: [Invoca tool list_repos vía MCP]

        Repositorios de anthropics:
        1. anthropic-sdk-python - SDK oficial para Claude API
        2. courses - Material educativo de Anthropic
        3. anthropic-cookbook - Recetas y ejemplos
        ...
```

### MCP vs Agent Skills

| Aspecto | MCP | Agent Skills |
|---------|-----|--------------|
| **Propósito** | Conectar LLMs a **datos/tools externos** | Empaquetar **conocimiento procedimental** |
| **Formato** | Protocolo (JSON-RPC) | Filesystem (markdown + scripts) |
| **Uso principal** | APIs, databases, servicios externos | Workflows internos, procedimientos |
| **Ejemplos** | GitHub MCP, Slack MCP, PostgreSQL MCP | PDF processing skill, Code review skill |

**Son complementarios**:
- **MCP** → "¿Cómo conecto a GitHub?"
- **Agent Skills** → "¿Qué hago con los datos de GitHub cuando los tengo?"

---

## Proyecto: Agente de Asistencia al Desarrollo

### Objetivo

Construir un **agente que asiste en desarrollo de software** usando **Agent Skills + LangChain** de forma híbrida.

### Funcionalidades

1. **Code Review** (Agent Skill)
2. **Search Codebase** (LangChain Tool)
3. **Run Tests** (LangChain Tool)
4. **Git Operations** (LangChain Tool)
5. **Documentation Search** (RAG + LangChain)

### Arquitectura

```
┌────────────────────────────────────────────────────┐
│              User Query                            │
│  "Review el código en api/tasks.py"               │
└───────────────────┬────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────────────┐
│         LangChain Agent (Orchestrator)            │
│                                                    │
│  Tools:                                           │
│  1. code_review (→ Agent Skill)                   │
│  2. search_codebase (Python)                      │
│  3. run_tests (subprocess)                        │
│  4. git_operations (subprocess)                   │
│  5. search_docs (RAG)                             │
└────────────────────────────────────────────────────┘
```

### Implementación

Ver archivos en `proyecto/`:
- `proyecto/README.md` - Instrucciones de setup
- `proyecto/dev_assistant.py` - Implementación principal
- `proyecto/.claude/skills/code-review/SKILL.md` - Agent Skill de code review

**Ejecutar**:

```bash
cd proyecto
python dev_assistant.py

# Ejemplo de query
> Review el código en api/tasks.py y sugiere mejoras

# El agente:
# 1. Usa tool "search_codebase" para encontrar api/tasks.py
# 2. Lee el archivo
# 3. Invoca Agent Skill "code-review"
# 4. Retorna lista de issues con sugerencias
```

---

## Ejercicios Prácticos con IA

### Ejercicio 1: Crear un Agent Skill (60 min)

**Objetivo**: Diseñar un Agent Skill para un dominio específico.

**Prompt para Claude**:

```
Diseña un Agent Skill para [DOMINIO: e.g., "análisis de vulnerabilidades de seguridad"].

El skill debe:
1. Tener un nombre claro y descripción (YAML header)
2. Definir cuándo usarlo y cuándo NO usarlo
3. Incluir un workflow paso a paso
4. Documentar herramientas/scripts necesarios
5. Tener ejemplos de uso
6. Incluir error handling

Formato: SKILL.md completo siguiendo las best practices de Anthropic.
```

**Checklist de auditoría**:

- [ ] ¿Nombre es descriptivo y específico?
- [ ] ¿Description explica casos de uso claramente?
- [ ] ¿Workflow tiene pasos numerados y accionables?
- [ ] ¿Incluye ejemplos concretos?
- [ ] ¿Documenta errores comunes y soluciones?
- [ ] ¿Referencias a archivos de soporte son claras?
- [ ] ¿Ningún comando peligroso (eval, shell=True, etc.)?

### Ejercicio 2: LangChain Custom Tool (45 min)

**Objetivo**: Implementar un custom tool para LangChain.

**Prompt**:

```
Implementa un LangChain custom tool para [TAREA: e.g., "analizar logs de servidor"].

Requisitos:
1. Hereda de BaseTool
2. Define args_schema con Pydantic
3. Implementa _run() con lógica completa
4. Maneja errores con mensajes accionables
5. Incluye descripción clara para el agente
6. 3 ejemplos de uso

Formato: Código Python completo + docstrings
```

**Testing**:

```python
# Test unitario
def test_custom_tool():
    tool = MyCustomTool()
    result = tool._run(arg1="value1", arg2="value2")
    assert result == expected_output
```

### Ejercicio 3: RAG para Documentación Interna (90 min)

**Objetivo**: Implementar un sistema RAG para documentación técnica.

**Prompt**:

```
Implementa un sistema RAG para responder preguntas sobre [DOCS: e.g., "documentación de FastAPI"].

Pasos:
1. Cargar documentos desde docs/
2. Dividir en chunks (tamaño óptimo: 500-1000 tokens)
3. Crear vector store (FAISS o Chroma)
4. Implementar retriever con k=5
5. Crear QA chain (chain_type="stuff")
6. Agregar reranking para mejorar precisión
7. Retornar respuestas con fuentes citadas

Formato: Código Python completo funcional
```

**Evaluación**:

```python
# Evalúa calidad del RAG
test_questions = [
    "¿Cómo crear un endpoint POST en FastAPI?",
    "¿Cómo validar inputs con Pydantic?",
    "¿Cómo manejar errores 404?"
]

for q in test_questions:
    result = qa_chain({"query": q})
    print(f"Q: {q}")
    print(f"A: {result['result']}")
    print(f"Sources: {[d.metadata['source'] for d in result['source_documents']]}")
    print()
```

### Ejercicio 4: Agente Híbrido (120 min)

**Objetivo**: Construir un agente que combine Agent Skills + LangChain.

**Prompt**:

```
Diseña un agente híbrido para [USE_CASE: e.g., "asistente de customer support"].

Arquitectura:
1. LangChain Agent como orchestrator
2. 3+ Agent Skills para workflows complejos
3. 5+ LangChain Tools para operaciones básicas
4. Memory con ConversationSummaryMemory
5. RAG para documentación de producto

Componentes a entregar:
1. LangChain agent setup
2. 3 Agent Skills (SKILL.md completos)
3. 5 Custom Tools (código Python)
4. RAG implementation
5. README con instrucciones de uso

Formato: Proyecto completo con estructura de directorios
```

---

## Recursos Adicionales

### Artículos Oficiales

- [Agent Skills - Anthropic Engineering Blog](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)

### Repositorios de Ejemplo

- [Claude Code Agent Skills](https://github.com/anthropics/claude-code/tree/main/.claude/skills)
- [MCP Servers](https://github.com/modelcontextprotocol/servers)
- [LangChain Examples](https://github.com/langchain-ai/langchain/tree/master/cookbook)

### Herramientas

- [LangChain](https://github.com/langchain-ai/langchain) - Framework de agents
- [FAISS](https://github.com/facebookresearch/faiss) - Vector store rápido
- [Chroma](https://www.trychroma.com/) - Vector database
- [Anthropic Claude API](https://docs.anthropic.com/en/api/getting-started)

---

## Conclusión

Has aprendido **dos paradigmas complementarios** para construir agentes IA:

### Agent Skills (Anthropic)
✅ Excelente para workflows complejos con conocimiento procedimental
✅ Escalable a 100+ skills sin saturar context window
✅ Fácil de versionar y compartir (markdown en Git)

### LangChain
✅ Excelente para orchestración y composición
✅ Soporte multi-LLM (OpenAI, Anthropic, etc.)
✅ Testing y debugging fácil (código Python estándar)

### Arquitectura Híbrida (Recomendado)
Combina lo mejor de ambos:
- **LangChain** como orchestrator
- **Agent Skills** para workflows complejos
- **RAG** para acceso a conocimiento
- **MCP** para integración con servicios externos

**Next Steps**:
1. Implementa el proyecto de agente de desarrollo
2. Crea 3 Agent Skills para tu dominio
3. Experimenta con RAG en tu documentación
4. Explora MCP servers disponibles

**Recuerda**: El futuro del desarrollo es **"a solo developer with an army of agents"**. Domina estos frameworks y serás ese developer.
