# Quick Start - Clase 6.5: Claude Agent SDK

Guía de inicio rápido para empezar a trabajar con agentes Claude en **5 minutos**.

---

## 1. Instalación (2 minutos)

```bash
# Navegar a la carpeta de la clase
cd "Modulo 4 - Infraestructura y Cloud/Clase 6.5 - Claude Agent SDK (Building Agents)"

# Instalar dependencias
pip install -r requirements.txt
```

**Dependencias principales**:
- `anthropic>=0.18.0` - Claude Agent SDK
- `pytest>=8.0.0` - Testing (opcional)

---

## 2. Configuración de API Key (1 minuto)

### Obtener API Key

1. Ve a [Anthropic Console](https://console.anthropic.com/)
2. Crea una cuenta o inicia sesión
3. Navega a "API Keys"
4. Genera una nueva API key

### Configurar en tu entorno

**Opción A: Variable de entorno** (recomendado)

```bash
# Linux/Mac
export ANTHROPIC_API_KEY="tu_api_key_aqui"

# Windows PowerShell
$env:ANTHROPIC_API_KEY="tu_api_key_aqui"

# Windows CMD
set ANTHROPIC_API_KEY=tu_api_key_aqui
```

**Opción B: Archivo .env**

```bash
# Copiar template
cp .env.template .env

# Editar .env con tu editor favorito
# ANTHROPIC_API_KEY=tu_api_key_aqui
```

---

## 3. Primer agente - ¡Hola mundo! (2 minutos)

Crea un archivo `hello_agent.py`:

```python
import os
from anthropic import Anthropic

# Crear cliente
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Llamada simple (sin tools)
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explica en 2 líneas qué es un agente autónomo"}
    ],
)

print(response.content[0].text)
```

Ejecutar:
```bash
python hello_agent.py
```

**Salida esperada**:
```
Un agente autónomo es un sistema de IA que puede tomar decisiones y ejecutar
acciones de forma independiente usando herramientas, iterando hasta completar
una tarea sin intervención humana constante.
```

---

## 4. Ejercicios progresivos

### Ejercicio 1: Agente simple con bash tools

```bash
python ejemplos/01_agente_simple.py
```

**Qué hace**: Explora un repositorio respondiendo preguntas usando comandos bash.

**Ejemplo de pregunta**: "¿Cuántos archivos Python hay en este proyecto?"

---

### Ejercicio 2: State management y retry logic

```bash
python ejemplos/02_control_flujo.py
```

**Qué hace**: Ejecuta tareas con estados, retry automático y verificación LLM-as-judge.

**Concepto clave**: Backoff exponencial y state machine.

---

### Ejercicio 3: Tools profesionales

```bash
python ejemplos/03_tools_avanzadas.py
```

**Qué hace**: Agente con tools personalizadas (git, pytest, ruff) con validación e idempotencia.

**Concepto clave**: Tool design patterns.

---

### Ejercicio 4: Subagentes y paralelización

```bash
python ejemplos/04_subagentes.py
```

**Qué hace**: Agente maestro que coordina 3 subagentes especializados en paralelo.

**Concepto clave**: Paralelización con ThreadPoolExecutor.

---

## 5. Proyecto final - Agente autónomo

```bash
python proyecto_final/agente_dev_autonomo.py
```

**Qué hace**: Resuelve issues completos de desarrollo de forma autónoma:
- Analiza el issue
- Busca código relevante
- Genera fix
- Ejecuta tests
- Crea Pull Request

**Issues de ejemplo**:
1. Typo en nombre de función
2. Import faltante
3. Docstring faltante

---

## 6. Tests (opcional)

```bash
# Tests de estructura (no requieren API key)
pytest tests/test_ejemplos.py -v

# Tests con API (requieren ANTHROPIC_API_KEY)
pytest tests/test_ejemplos.py::TestConAPI -v
```

---

## 🎯 Próximos pasos

1. **Lee el README.md**: Conceptos fundamentales del SDK
2. **Sigue el AI_WORKFLOW.md**: Integración IA completa (60%+)
3. **Experimenta con los ejercicios**: Modifícalos, rompe cosas, aprende
4. **Completa el proyecto final**: Agente de desarrollo autónomo

---

## 🚨 Troubleshooting

### Error: "ANTHROPIC_API_KEY not found"
```bash
# Verifica que la variable está configurada
echo $ANTHROPIC_API_KEY  # Linux/Mac
echo %ANTHROPIC_API_KEY%  # Windows

# Si no aparece, configurar de nuevo
export ANTHROPIC_API_KEY="tu_api_key"
```

### Error: "ModuleNotFoundError: No module named 'anthropic'"
```bash
# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
python -c "import anthropic; print(anthropic.__version__)"
```

### Error: Rate limit exceeded
```bash
# Has alcanzado el límite de API calls
# Opciones:
# 1. Espera unos minutos
# 2. Reduce max_iterations en los agentes
# 3. Usa un tier de API más alto
```

### Los tests fallan
```bash
# Tests opcionales con API requieren API key
# Si no tienes API key, los tests se saltean automáticamente
pytest tests/ -v --tb=short
```

---

## 📚 Recursos adicionales

- [Anthropic Documentation](https://docs.anthropic.com/)
- [Tool Use Guide](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [Building Agents (artículo base)](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)

---

## 💡 Tips para aprender rápido

1. **Empieza simple**: Ejecuta cada ejercicio en orden
2. **Modifica y rompe**: Cambia parámetros, observa qué pasa
3. **Lee los logs**: Están diseñados para enseñar
4. **Usa IA para aprender IA**: Pide a Claude Code que explique conceptos
5. **Compara con LangChain**: Si hiciste la Clase 6, compara enfoques

---

**Tiempo estimado para Quick Start**: 5 minutos
**Tiempo estimado para todos los ejercicios**: 2-3 horas
**Tiempo estimado para dominar el SDK**: 6-8 horas (clase completa)

¡Buena suerte! 🚀🤖
