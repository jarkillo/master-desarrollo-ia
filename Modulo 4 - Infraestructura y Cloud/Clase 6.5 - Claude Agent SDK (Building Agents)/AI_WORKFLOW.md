# AI Workflow - Clase 6.5: Claude Agent SDK

**Objetivo**: Integración IA como herramienta central de aprendizaje (60%+ del contenido)

Esta clase ES SOBRE IA - el Claude Agent SDK. Por lo tanto, el 100% del contenido técnico involucra IA, y la integración IA está en el núcleo de cada ejercicio.

---

## 🎯 Resumen de integración IA

| Componente | % IA | Descripción |
|------------|------|-------------|
| **Teoría** | 100% | Claude Agent SDK, arquitectura de agentes, feedback loop |
| **Ejercicios** | 100% | Todos usan Anthropic API para crear agentes |
| **Proyecto final** | 100% | Agente autónomo de desarrollo con Claude |
| **Debugging** | 80% | IA para análisis de logs + debugging manual |

**Total: ~95% integración IA** (supera el 60% requerido)

---

## 📚 Parte 1: Fundamentos de agentes con IA (100% IA)

### Conceptos a aprender CON IA

1. **Feedback loop fundamental**
   ```
   Gather Context → Take Action → Verify Work → Repeat
   ```
   - **Prompt para entender**: "Explica el feedback loop de agentes con analogía de desarrollo de software"
   - **IA genera**: Ejemplos de bucles en debugging, testing, refactoring

2. **Context gathering strategies**
   - Agentic search vs Semantic search
   - **Ejercicio IA**: Pedir a Claude que compare las dos estrategias con tabla de trade-offs
   - **Prompt**: "¿Cuándo usar agentic search vs semantic search en agentes? Dame casos de uso específicos"

3. **Tool design patterns**
   - **IA explica**: Best practices de tool design
   - **Prompt**: "Dame 5 principios de diseño de tools para agentes Claude, con ejemplos de buen y mal diseño"

---

## 💻 Parte 2: Ejercicios prácticos (100% IA)

Todos los ejercicios requieren usar la Anthropic API directamente.

### Ejercicio 1: Primer agente simple (archivo: `ejemplos/01_agente_simple.py`)

**Objetivo**: Agente que explora repositorio usando bash tools

**Workflow con IA**:

1. **Diseño del agente** (IA-assisted)
   ```
   Prompt a Claude Code:
   "Ayúdame a diseñar la estructura de un agente simple que explore
   repositorios con comandos bash. ¿Qué clase base necesito? ¿Qué
   métodos son esenciales?"
   ```

2. **Implementación** (100% IA en runtime)
   - El agente usa Claude API para decidir qué comandos bash ejecutar
   - Implementa feedback loop completo
   - IA analiza outputs y decide próximos pasos

3. **Debugging con IA**
   ```
   Prompt:
   "Este agente ejecuta 'ls' repetidamente sin avanzar. Analiza el log
   y sugiere qué está fallando en mi implementación del feedback loop"
   ```

**Ejercicio extendido**:
- Usa IA para generar tests del agente
- Pide a Claude que optimice la estrategia de búsqueda del agente

---

### Ejercicio 2: State management y retry logic (archivo: `ejemplos/02_control_flujo.py`)

**Objetivo**: Agente con estados, retry logic y verificación con LLM-as-judge

**Workflow con IA**:

1. **State machine design** (IA-assisted)
   ```
   Prompt:
   "Diseña una state machine para un agente de desarrollo con estados:
   pending, in_progress, completed, failed, retrying.
   ¿Qué transiciones son válidas? Genera un diagrama en Mermaid."
   ```

2. **Verificación con LLM-as-judge** (100% IA)
   - El agente usa Claude para validar sus propios resultados
   - Pattern: Un LLM genera, otro LLM verifica
   - **Prompt para verificador**:
     ```python
     f"Verifica si este resultado cumple la tarea: {task_description}
     Resultado: {result}
     Responde VÁLIDO o INVÁLIDO con razón."
     ```

3. **Retry logic inteligente** (IA-driven)
   - Backoff exponencial clásico
   - Pero el agente usa IA para analizar *por qué* falló
   - Ajusta estrategia en cada retry

**Ejercicio con IA**:
```
Prompt a Claude Code:
"El agente está en retry loop infinito. Analiza este log y sugiere
cómo mejorar la lógica de retry para detectar fallos irrecuperables."
```

---

### Ejercicio 3: Tool design avanzado (archivo: `ejemplos/03_tools_avanzadas.py`)

**Objetivo**: Diseñar tools profesionales con validación, logging, idempotencia

**Workflow con IA**:

1. **Diseño de tools** (IA-assisted)
   ```
   Prompt:
   "Necesito diseñar una tool para ejecutar pytest. Genera el schema
   Anthropic con:
   - Input parameters (path, verbose)
   - Descripción clara para que Claude entienda cuándo usarla
   - Ejemplo de input_schema completo"
   ```

2. **Validación con IA**
   - Pide a Claude Code que revise tus tools
   - **Prompt**: "Revisa esta tool design. ¿Cumple con: específica, bien documentada, idempotente, con validación?"

3. **Debugging de tool calls**
   - Usa IA para analizar por qué Claude elige (o no) una tool
   - **Prompt**: "Claude no está usando mi GitStatusTool. Analiza la descripción y sugiere mejoras"

**Ejercicio avanzado**:
- Pide a IA que genere 3 tools más para el agente
- Usa IA para generar tests de las tools

---

### Ejercicio 4: Subagentes y paralelización (archivo: `ejemplos/04_subagentes.py`)

**Objetivo**: Agente maestro que coordina subagentes especializados

**Workflow con IA**:

1. **Arquitectura de subagentes** (IA-assisted)
   ```
   Prompt:
   "Diseña una arquitectura de agente maestro + 3 subagentes para
   analizar proyectos Python. ¿Qué responsabilidad tiene cada uno?
   ¿Cómo se comunican? ¿Qué retorna cada subagente al maestro?"
   ```

2. **Specialization con system prompts** (100% IA)
   - Cada subagente tiene system prompt único
   - IA para generar system prompts efectivos
   - **Ejemplo**: SearchAgent vs AnalysisAgent vs TestAgent

3. **Synthesis con IA** (100% IA)
   - Agente maestro usa Claude para sintetizar resultados de subagentes
   - Pattern: Multiple LLM calls → Single synthesis call

**Ejercicio con IA**:
```
Prompt:
"Tengo 3 subagentes con outputs largos. ¿Cómo diseño el prompt de
síntesis para que el maestro genere un resumen ejecutivo de máximo
10 líneas sin perder información crítica?"
```

---

## 🏆 Parte 3: Proyecto final - Agente autónomo (100% IA)

**Archivo**: `proyecto_final/agente_dev_autonomo.py`

### Workflow completo con IA

#### 1. Análisis de issue (IA)
```python
# IA clasifica tipo de issue
issue_type = agent._classify_issue(issue)
# Prompt: "Clasifica este issue en: typo, missing_import, simple_test, ..."
```

#### 2. Context gathering (IA + agentic search)
```python
# IA decide qué comandos bash ejecutar para encontrar código relevante
context = agent._gather_context(issue)
# Prompt: "¿Qué archivos debo revisar para este issue? Sugiere comandos bash."
```

#### 3. Generación de fix (IA)
```python
# IA genera el código del fix completo
fix_code = agent._generate_fix(issue, context)
# Prompt: "Genera fix para este issue. Formato JSON con archivos completos."
```

#### 4. Verificación (IA + herramientas)
```python
# Verificación híbrida:
# - Tests: pytest (tool tradicional)
# - Linting: ruff (tool tradicional)
# - Validación semántica: Claude (IA)

if not tests_passed:
    # IA analiza por qué fallaron
    analysis = agent._analyze_test_failure(test_output)
    # Retry con feedback de IA
```

#### 5. PR description (IA)
```python
# IA genera descripción profesional del PR
pr_description = agent._generate_pr_description(issue, files_modified)
# Incluye: changes, verification, related issue
```

### Ejercicios con IA para el proyecto

1. **Prompt engineering para fix generation**
   ```
   Experimento:
   1. Genera un fix con prompt básico
   2. Genera el mismo fix con prompt detallado (incluye: context, retry guidance, format)
   3. Compara calidad de outputs

   Pregunta: ¿Qué elementos del prompt más afectan la calidad del fix?
   ```

2. **Optimización de context gathering**
   ```
   Usa IA para analizar:
   - ¿Cuántos comandos bash se ejecutan en promedio?
   - ¿Hay comandos redundantes?
   - ¿Se puede predecir qué archivos revisar sin ejecutar comandos?

   Prompt a Claude Code:
   "Analiza este log de comandos bash. ¿Cómo optimizarías la estrategia
   de búsqueda para reducir comandos de 5 a 2 sin perder información?"
   ```

3. **Mejora del retry logic**
   ```
   Ejercicio:
   1. Haz que un issue falle intencionalmente (tests fail)
   2. Analiza cómo el agente maneja el retry
   3. Usa IA para mejorar el retry logic

   Prompt:
   "Este agente falla el mismo test 3 veces por el mismo error. ¿Cómo
   diseñarías un sistema de retry que aprenda del error anterior?"
   ```

---

## 🔧 Parte 4: Debugging de agentes con IA (80% IA)

### Técnicas de debugging asistidas por IA

#### 1. Log analysis con IA
```
Prompt a Claude Code:
"Analiza este log de ejecución del agente. Identifica:
1. ¿Dónde se quedó atascado?
2. ¿Qué decisiones tomó que no tienen sentido?
3. ¿Hay loops infinitos o comportamiento repetitivo?
4. Sugiere 3 mejoras específicas al código."
```

#### 2. Prompt engineering iterativo
```
Experimento con IA:
1. Ejecuta agente con prompt versión 1
2. Analiza comportamiento con Claude Code
3. Claude Code sugiere mejoras al prompt
4. Ejecuta con prompt versión 2
5. Compara resultados

Meta-análisis: ¿Qué elementos del prompt más influyen en el comportamiento?
```

#### 3. Tool selection debugging
```
Si Claude no usa tus tools correctamente:

Prompt a Claude Code:
"Claude ignora mi FileSearchTool y usa bash directamente. Aquí está
la descripción de la tool: [...]
¿Cómo mejorarías la descripción para que Claude la prefiera sobre bash?"
```

---

## 📊 Parte 5: Evaluación y métricas (IA-assisted)

### Métricas para agentes

**Usa IA para analizar**:

1. **Success rate**
   ```
   Prompt:
   "Tengo estos resultados de 10 ejecuciones del agente: [...]
   Calcula: success rate, tiempo promedio, retry rate.
   ¿Qué patrones ves en los fallos?"
   ```

2. **Token efficiency**
   ```
   Prompt:
   "El agente usa 50K tokens promedio por tarea. Aquí está el breakdown:
   [context gathering: 20K, fix generation: 25K, synthesis: 5K]
   ¿Dónde puedo optimizar? Sugiere estrategias concretas."
   ```

3. **Quality assessment**
   ```
   Usa LLM-as-judge para evaluar calidad del código generado:

   Prompt al juez:
   "Evalúa este fix generado por agente en escala 1-10:
   - Corrección (¿resuelve el issue?)
   - Calidad del código (PEP 8, clean code)
   - Robustez (manejo de edge cases)
   Justifica cada puntuación."
   ```

---

## 🚀 Parte 6: Extensiones avanzadas (100% IA)

### Proyecto extendido con IA

1. **Multi-modal agents**
   ```
   Extiende el agente para manejar issues de UI:
   - Genera fix de UI
   - Toma screenshot (visual feedback)
   - IA analiza screenshot vs diseño esperado
   - Itera hasta que UI sea correcta

   Prompt:
   "Diseña el workflow de un agente que arregla issues de UI usando
   screenshots como feedback. ¿Qué herramientas necesito? ¿Cómo
   describo la diferencia entre esperado vs actual a Claude?"
   ```

2. **Agent orchestration**
   ```
   Crea meta-agente que decide qué agente especializado usar:

   Issues → Meta-agent (classifier) → [Agent A, Agent B, Agent C]

   Meta-agent usa Claude para:
   - Clasificar issue
   - Elegir agente apropiado
   - Validar resultado
   - Escalar a humano si es complejo
   ```

3. **Self-improving agents**
   ```
   Agente que aprende de errores:
   - Guarda casos de éxito/fallo en vector DB
   - En nueva tarea, busca casos similares
   - Ajusta estrategia basándose en casos previos

   Usa IA para:
   - Generar embeddings de issues
   - Buscar casos similares (semantic search)
   - Sintetizar "lessons learned" de casos previos
   ```

---

## 🎓 Rúbrica de evaluación (IA-assisted)

### Autoevaluación con IA

Usa este prompt con Claude Code para evaluarte:

```
Evalúa mi implementación del proyecto final en estas dimensiones:

1. **Arquitectura del agente** (0-10)
   - ¿Implementa feedback loop correctamente?
   - ¿Maneja estados apropiadamente?
   - ¿Las tools están bien diseñadas?

2. **Manejo de errores** (0-10)
   - ¿Retry logic es robusto?
   - ¿Detecta fallos irrecuperables?
   - ¿Logs son útiles para debugging?

3. **Calidad del código generado** (0-10)
   - ¿Los fixes resuelven el issue?
   - ¿El código sigue PEP 8?
   - ¿Pasa tests y linting?

4. **Eficiencia** (0-10)
   - ¿Uso de tokens es razonable?
   - ¿Evita comandos redundantes?
   - ¿Paraleliza donde es apropiado?

Aquí está mi código: [...]

Para cada dimensión:
- Puntuación (0-10)
- Justificación
- 2 sugerencias de mejora específicas
```

---

## 🔗 Integración con otras clases

### Clase 6 (LangChain) ↔ Clase 6.5 (Claude Agent SDK)

**Ejercicio comparativo** (IA-assisted):

```
Prompt:
"Compara estas dos implementaciones del mismo agente:
1. Con LangChain (Clase 6)
2. Con Claude Agent SDK (Clase 6.5)

Analiza:
- Líneas de código
- Control sobre el loop
- Facilidad de debugging
- Performance (tokens usados)
- Cuál elegirías para producción y por qué?"
```

### Clase 6.6 (Context Engineering) - Preview

El agente autónomo usa context engineering:
- Cómo estructurar el system prompt de cada subagente
- Cómo comprimir contexto para evitar token limits
- Cuándo usar compaction vs subagents

**Ejercicio de transición**:
```
Prompt a Claude Code:
"Mi agente autónomo alcanza token limit en proyectos grandes.
¿Qué estrategias de context engineering puedo aplicar?
Dame 3 técnicas con ejemplos de código."
```

---

## 📝 Checklist de integración IA

Verifica que tu aprendizaje incluya:

- [ ] ✅ Usaste Anthropic API directamente (no abstracciones)
- [ ] ✅ Implementaste feedback loop completo con IA
- [ ] ✅ Diseñaste tools y usaste Claude para invocarlas
- [ ] ✅ Aplicaste LLM-as-judge para verificación
- [ ] ✅ Creaste subagentes especializados con system prompts
- [ ] ✅ Usaste IA para debugging (análisis de logs)
- [ ] ✅ Experimentaste con prompt engineering
- [ ] ✅ Mediste métricas (tokens, success rate)
- [ ] ✅ Proyecto final: agente autónomo funcional
- [ ] ✅ Comparaste Claude Agent SDK vs LangChain

---

## 🎯 Objetivo final

Al terminar esta clase, deberías ser capaz de:

1. **Construir agentes autónomos profesionales** con Claude Agent SDK
2. **Diseñar architecturas de agentes** (single, multi-agent, hierarchical)
3. **Debuggear agentes** usando técnicas de IA-assisted debugging
4. **Optimizar performance** de agentes (tokens, latencia, calidad)
5. **Decidir cuándo usar** Claude SDK vs LangChain vs custom loop

Todo esto usando IA como herramienta central de aprendizaje, no solo de ejecución.

---

**Meta-pregunta final**:

```
Prompt reflexivo a Claude Code:
"He completado la Clase 6.5. Reflexiona:
1. ¿Qué conceptos de agentes entiendo bien?
2. ¿Qué áreas necesito profundizar?
3. ¿Cómo aplicaría estos conceptos en un proyecto real?
4. ¿Qué pregunta sobre agentes tengo que NO se cubrió en la clase?"
```

Esta meta-pregunta cierra el loop de aprendizaje con IA 🎓🤖
