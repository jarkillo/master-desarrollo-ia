# Proyecto: Agente de Asistencia al Desarrollo

## Descripción

Este proyecto implementa un **agente híbrido** que combina:
- **LangChain** como orchestrator
- **Agent Skills** para workflows complejos
- **Custom Tools** para operaciones de desarrollo

El agente puede asistir en tareas como:
- 🔍 **Code Review** usando Agent Skill especializado
- 📁 **Búsqueda de código** en el repositorio
- ✅ **Ejecución de tests** y análisis de resultados
- 📚 **Búsqueda en documentación** con RAG

## Arquitectura

```
┌────────────────────────────────────────┐
│        User Query                      │
│   "Review el código en api/tasks.py"  │
└───────────────┬────────────────────────┘
                ↓
┌────────────────────────────────────────┐
│    LangChain Agent (Orchestrator)     │
│                                        │
│  Tools:                               │
│  1. code_review (→ Agent Skill)       │
│  2. search_codebase (grep)            │
│  3. run_tests (pytest)                │
│  4. search_docs (RAG)                 │
└────────────────────────────────────────┘
```

## Estructura

```
proyecto/
├── README.md                    # Este archivo
├── dev_assistant.py             # Agente principal
├── .env.template                # Template de variables de entorno
├── .claude/
│   └── skills/
│       └── code-review/
│           ├── SKILL.md         # Agent Skill de code review
│           └── checklist.md     # Checklist de review
└── tools/
    ├── __init__.py
    ├── code_search.py           # Tool de búsqueda de código
    ├── test_runner.py           # Tool para ejecutar tests
    └── doc_search.py            # Tool de RAG para docs
```

## Instalación

### 1. Instalar dependencias

```bash
cd proyecto
pip install -r ../requirements.txt
```

### 2. Configurar variables de entorno

```bash
cp .env.template .env
# Editar .env y agregar tu ANTHROPIC_API_KEY
```

**Contenido de `.env`**:
```
ANTHROPIC_API_KEY=tu_api_key_aqui
```

### 3. (Opcional) Preparar documentación para RAG

Si quieres que el agente busque en documentación:

```bash
mkdir -p docs
# Copiar archivos .md de documentación a docs/
```

## Uso

### Ejecutar el agente

```bash
python dev_assistant.py
```

### Ejemplos de queries

**Code Review**:
```
> Review el archivo api/tasks.py

# El agente:
# 1. Lee el archivo
# 2. Invoca Agent Skill "code-review"
# 3. Retorna lista de issues con severidades
```

**Búsqueda de código**:
```
> Busca todas las funciones que usan SQLAlchemy

# El agente:
# 1. Usa tool "search_codebase" con query "from sqlalchemy"
# 2. Lista archivos y líneas relevantes
```

**Ejecutar tests**:
```
> Ejecuta los tests en tests/test_api.py

# El agente:
# 1. Usa tool "run_tests"
# 2. Retorna resultados (passed/failed)
# 3. Sugiere fixes si hay fallos
```

**Búsqueda en docs**:
```
> ¿Cómo validar inputs con Pydantic?

# El agente:
# 1. Usa RAG para buscar en docs/
# 2. Retorna respuesta con fuentes citadas
```

## Agent Skill: Code Review

El proyecto incluye un Agent Skill completo para code review.

**Ubicación**: `.claude/skills/code-review/SKILL.md`

**Checklist de review**:
1. ✅ **Arquitectura & Diseño**
   - Single Responsibility
   - Dependency Inversion
   - Open/Closed

2. ✅ **Calidad de Código**
   - Naming claro
   - Complejidad < 10
   - Sin duplicación

3. ✅ **Testing**
   - Cobertura > 80%
   - Tests aislados
   - Edge cases cubiertos

4. ✅ **Seguridad**
   - Input validation
   - No SQL injection
   - Secrets management

5. ✅ **Performance**
   - Sin N+1 queries
   - Operaciones costosas cacheadas
   - I/O bloqueante es async

**Niveles de severidad**:
- 🔴 **Critical**: Vulnerabilidades, pérdida de datos
- 🟡 **Major**: Performance, mantenibilidad
- 🟢 **Minor**: Estilo, sugerencias

## Extensión

### Agregar nuevo tool

```python
# En tools/my_tool.py
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class MyToolInput(BaseModel):
    param1: str = Field(description="Descripción")

class MyTool(BaseTool):
    name = "my_tool"
    description = "Qué hace este tool..."
    args_schema = MyToolInput

    def _run(self, param1: str) -> str:
        # Implementación
        return "resultado"

# En dev_assistant.py
from tools.my_tool import MyTool

tools = [
    code_review_tool,
    search_codebase_tool,
    MyTool()  # Agregar aquí
]
```

### Agregar nuevo Agent Skill

```bash
mkdir -p .claude/skills/my-skill
nano .claude/skills/my-skill/SKILL.md
```

**Template de SKILL.md**:
```markdown
---
name: My Skill Name
description: Brief description
---

# My Skill

## When to Use This Skill

Use this skill when...

## Workflow

1. Step 1
2. Step 2
...

## Examples

...
```

## Testing

```bash
# Ejecutar tests del agente
pytest tests/

# Test manual
python dev_assistant.py
> test query
```

## Troubleshooting

**Error: "ANTHROPIC_API_KEY not found"**
- Verifica que `.env` existe y contiene la API key

**Error: "Module not found"**
- Asegúrate de haber instalado las dependencias: `pip install -r requirements.txt`

**Agent no usa mi tool**
- Revisa la `description` del tool - debe ser clara y específica
- Verifica que el tool está en la lista de `tools`

**Agent Skills no se cargan**
- Verifica que la estructura de directorios es correcta (`.claude/skills/`)
- Revisa que `SKILL.md` tiene el YAML header correcto

## Recursos

- [Agent Skills - Anthropic](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [LangChain Docs](https://python.langchain.com/docs/get_started/introduction)
- [Writing Tools for Agents](../../Clase%206.7%20-%20Writing%20Tools%20for%20AI%20Agents/README.md)

## Contribuir

Para mejorar este proyecto:
1. Fork el repositorio
2. Crea un feature branch
3. Implementa tu mejora
4. Crea un Pull Request

## Licencia

Educational use - Master IA Development
