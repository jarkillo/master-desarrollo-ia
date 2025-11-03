# 🤖 Ejercicios Prácticos con IA - Writing Tools for AI Agents

Este documento contiene ejercicios diseñados para practicar el diseño de tools **usando Claude como asistente**. El objetivo es aprender a iterar con IA para mejorar tus tools.

---

## 📋 Metodología: TDD con IA

**Test-Driven Design con IA**:
1. **Describe** el tool que necesitas (prompt a Claude)
2. **Claude genera** el código inicial
3. **Tú auditas** usando la checklist de best practices
4. **Claude refactoriza** basándose en tu feedback
5. **Tú validas** con tests

---

## Ejercicio 1: Diseñar un Tool de Inventario (45 min)

### Parte 1: Generación con Claude (15 min)

**Tu rol**: Product Owner que define requisitos

**Prompt inicial para Claude**:

```markdown
Necesito diseñar un tool para un agente IA que gestiona un sistema de inventario.

**Requisitos funcionales**:
1. Buscar productos por nombre, categoría o SKU
2. Retornar stock disponible
3. Alertar si stock está bajo (< 10 unidades)
4. Sugerir productos relacionados si el buscado no tiene stock

**Requisitos técnicos**:
- Nombre del tool claro y descriptivo
- Description completa siguiendo best practices de Anthropic
- Schema de input con Pydantic (validación estricta)
- Schema de output bien estructurado
- Casos de error con mensajes accionables
- 3 ejemplos de uso
- Parámetro response_format (detailed/concise)

Diseña el tool en Python con type hints completos.
```

**Acción**: Copia la respuesta de Claude a un archivo `inventory_tool.py`

### Parte 2: Auditoría Manual (15 min)

**Tu rol**: Security & Quality Reviewer

**Checklist de auditoría** (márcalas mientras revisas):

```markdown
## Nombre del Tool
- [ ] ¿Es descriptivo y sin ambigüedad?
- [ ] ¿Usa verbos de acción (search, get, create)?
- [ ] ¿No overlappea con otros tools potenciales?

## Description
- [ ] ¿Explica cuándo usar el tool?
- [ ] ¿Explica cuándo NO usarlo?
- [ ] ¿Incluye ejemplos de uso concretos?
- [ ] ¿Documenta relaciones con otros tools?
- [ ] ¿Menciona consideraciones de performance?

## Input Schema
- [ ] ¿Usa Pydantic para validación?
- [ ] ¿Parámetros tienen nombres específicos (no ambiguos)?
- [ ] ¿Incluye valores default razonables?
- [ ] ¿Rangos de valores están validados?
- [ ] ¿Hay field_validators para lógica custom?

## Output Schema
- [ ] ¿Retorna solo información relevante?
- [ ] ¿Usa identificadores semánticos (no UUIDs)?
- [ ] ¿Formato es parseable (JSON, Markdown)?
- [ ] ¿Incluye metadata útil (count, timestamp)?

## Error Handling
- [ ] ¿Usa Result type (Success/Error)?
- [ ] ¿Errores son accionables (dicen cómo corregir)?
- [ ] ¿Evita stack traces técnicos?
- [ ] ¿Sugiere alternativas cuando falla?
- [ ] ¿Tiene error_type categorizado?

## Security
- [ ] ¿Valida TODOS los inputs?
- [ ] ¿Previene injection attacks?
- [ ] ¿No expone secrets en outputs?
- [ ] ¿Limita tamaño de respuestas?
- [ ] ¿Tiene rate limiting (si aplica)?
```

**Documenta** los ❌ que encontraste:

```markdown
## Issues Encontrados

1. [Crítico/Alto/Medio/Bajo] Descripción del issue
   - **Problema**: [Qué está mal]
   - **Impacto**: [Por qué es un problema]
   - **Fix recomendado**: [Cómo corregirlo]

2. ...
```

### Parte 3: Iteración con Claude (15 min)

**Tu rol**: Tech Lead que da feedback constructivo

**Prompt de mejora para Claude**:

```markdown
Audité el tool que diseñaste. Aquí está el feedback:

## Issues Críticos
[Pega tu lista de issues críticos]

## Issues de Alta Prioridad
[Pega tu lista de issues altos]

## Mejoras Sugeridas
[Pega tu lista de mejoras]

**Refactoriza el tool para**:
1. Corregir todos los issues críticos y altos
2. Mejorar la description para ser más clara sobre cuándo NO usar el tool
3. Añadir el parámetro `response_format` (detailed/concise)
4. Implementar rate limiting con decorator
5. Añadir ejemplos de error handling en los docstrings

Muestra el código refactorizado completo.
```

**Valida** que Claude corrigió los issues. Si no, itera de nuevo con prompts más específicos.

---

## Ejercicio 2: Auditar Tool Mal Diseñado (30 min)

### Escenario

Tu compañero de equipo (Claude 😉) diseñó un tool, pero los agentes no lo usan correctamente. Tu misión: identificar qué está mal.

**Prompt para Claude**:

```markdown
Actúa como un desarrollador junior que NO conoce las best practices de Anthropic.

Diseña un tool llamado `get_data` que:
- Accede a una base de datos PostgreSQL
- Busca registros de usuarios
- Retorna información del usuario

Hazlo **deliberadamente mal** siguiendo estos antipatrones:
1. Nombre ambiguo
2. Description vaga
3. Sin validación de inputs
4. Expone información sensible (passwords)
5. Usa UUIDs en lugar de identificadores semánticos
6. Errores crípticos sin sugerencias
7. SQL injection posible

Dame solo el código (sin explicaciones), para que practique auditarlo.
```

### Tu Tarea

1. **Lee el código** que Claude generó
2. **Identifica 7+ antipatrones** usando la checklist
3. **Documenta cada issue** con:
   - Severidad (Critical/High/Medium/Low)
   - Línea de código
   - Anti-patrón específico
   - Impacto en el agente
   - Fix recomendado

4. **Pide a Claude que lo refactorice**:

```markdown
Identifiqué estos antipatrones en tu código:

[Tu análisis completo]

Refactoriza el tool siguiendo TODAS las best practices de Anthropic.
El nuevo tool debe:
- Tener un nombre descriptivo
- Description completa con ejemplos
- Validación Pydantic estricta
- Prevenir SQL injection (prepared statements)
- No exponer secrets
- Errores accionables
- Usar email en lugar de UUID para buscar usuarios

Muestra el código refactorizado.
```

5. **Compara** el código before/after. ¿Qué tan diferente es?

---

## Ejercicio 3: Tool Composition (45 min)

### Objetivo

Diseñar un tool de alto nivel que orquesta múltiples tools de bajo nivel.

**Prompt para Claude (Parte 1)**:

```markdown
Diseña 3 tools básicos para un sistema de análisis de API:

1. `search_logs` - Busca en logs del servidor
   - Input: query (regex), time_range (últimas N horas)
   - Output: Líneas de logs relevantes

2. `calculate_percentiles` - Calcula percentiles de response times
   - Input: response_times (list[float])
   - Output: p50, p95, p99

3. `get_error_rate` - Calcula tasa de errores
   - Input: logs (list[str])
   - Output: error_rate (float), common_errors (list[str])

Sigue best practices. Usa Pydantic.
```

**Prompt para Claude (Parte 2)**:

```markdown
Ahora diseña un tool de ALTO NIVEL llamado `analyze_api_endpoint` que:

**Funcionalidad**:
1. Internamente llama a los 3 tools que diseñaste antes
2. Busca logs del endpoint especificado
3. Extrae response times de los logs
4. Calcula percentiles (p50, p95, p99)
5. Calcula error rate
6. Genera recomendación basada en las métricas

**Input**:
- endpoint: str (e.g., "/api/tasks")
- time_window_hours: int (default: 24)

**Output consolidado**:
{
    "endpoint": "/api/tasks",
    "requests_analyzed": 1000,
    "avg_response_time_ms": 45.3,
    "p95_response_time_ms": 120.5,
    "p99_response_time_ms": 250.8,
    "error_rate_percent": 0.5,
    "common_errors": ["Timeout", "ValidationError"],
    "recommendation": "Consider adding caching"
}

Implementa la composición de tools. Sigue best practices.
```

### Tu Tarea

1. **Revisa** los 4 tools generados por Claude
2. **Verifica** que `analyze_api_endpoint`:
   - Llama a los 3 tools internamente
   - Maneja errores de cada tool
   - Consolida resultados de forma útil
   - Retorna recomendaciones accionables

3. **Pregúntate**:
   - ¿El agente prefiere usar 1 tool consolidado o 4 tools separados?
   - ¿En qué casos es mejor consolidar?
   - ¿En qué casos es mejor separar?

4. **Documenta** tu análisis:

```markdown
## Análisis: Consolidación vs Separación

### Ventajas de Consolidar
1. ...
2. ...

### Desventajas de Consolidar
1. ...
2. ...

### Conclusión
Para este caso específico, [consolidar/separar] es mejor porque...
```

---

## Ejercicio 4: Response Format Optimization (30 min)

### Objetivo

Optimizar tokens comparando respuestas `concise` vs `detailed`.

**Prompt para Claude**:

```markdown
Diseña un tool `search_slack_messages` con:

**Input**:
- query: str
- channel: str (opcional)
- limit: int (default: 10)
- response_format: "concise" | "detailed"

**Output (concise)**:
Solo información mínima: text, author, timestamp

**Output (detailed)**:
Información completa: text, author, timestamp, thread_ts, channel_id, user_id, reactions, attachments

Implementa ambos formatos. Usa Pydantic.
```

### Tu Tarea

1. **Genera** 2 respuestas ejemplo:
   - Una respuesta `concise` con 10 mensajes
   - Una respuesta `detailed` con 10 mensajes

2. **Cuenta tokens** de cada respuesta:
   - Usa Claude: "¿Cuántos tokens tiene esta respuesta?"
   - Compara: ¿Cuál consume más tokens?

3. **Analiza casos de uso**:

```markdown
## Cuándo usar Concise
- [Caso 1]
- [Caso 2]

## Cuándo usar Detailed
- [Caso 1]
- [Caso 2]

## Ahorro de Tokens
- Concise: X tokens
- Detailed: Y tokens
- Ahorro: (Y-X)/Y * 100 = Z%
```

4. **Pregunta a Claude**:

```markdown
Basándome en el análisis de tokens, ¿cuál debería ser el default para `response_format`?

Contexto:
- Concise: {X} tokens
- Detailed: {Y} tokens
- El agente típicamente necesita hacer llamadas downstream en 30% de los casos

¿Qué recomiendas y por qué?
```

---

## Ejercicio 5: Debugging Tool Issues (60 min)

### Escenario Real

Un agente NO está usando tu tool correctamente. Tienes estos logs:

```
[LOG] Tools available: ['search_code', 'read_file', 'execute_command']
[LOG] User: "Busca la función process_payment en el código"
[LOG] Agent: "No encuentro esa información. ¿Puedes darme más contexto?"
[LOG] Agent did NOT call: search_code
```

### Parte 1: Diagnóstico con Claude

**Prompt**:

```markdown
Tengo un problema: Mi agente NO está usando el tool `search_code` cuando debería.

**Tool actual**:
```python
def search_code(query: str) -> list:
    """Searches code."""
    # ... implementation
```

**Logs del agente**:
[Pega los logs de arriba]

**Pregunta**: ¿Por qué el agente no usó el tool? ¿Qué está mal en el diseño?

Analiza:
1. Nombre del tool
2. Description
3. Schema de input
4. Casos donde debería vs no debería usarse
```

### Parte 2: Fix Iterativo

1. **Claude propone** un fix
2. **Tú lo implementas**
3. **Simulas** llamar al agente de nuevo (prompt):

```markdown
Imagina que eres Claude (el agente) y tienes estos tools disponibles:

[Tool refactorizado]

El usuario dice: "Busca la función process_payment en el código"

¿Qué tool usarías? ¿Por qué?
```

4. **Itera** hasta que Claude (actuando como agente) diga que usaría el tool correctamente

---

## Ejercicio 6: Security Audit (30 min)

### Objetivo

Practicar security review de tools usando Claude como auditor.

**Prompt para Claude**:

```markdown
Actúa como un Security Engineer experto.

Audita este tool para vulnerabilidades de seguridad:

```python
def execute_command(cmd: str) -> str:
    """Runs a command."""
    import subprocess
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return result.stdout.decode()
```

Identifica:
1. Vulnerabilidades críticas (con ejemplos de exploit)
2. Vulnerabilidades altas
3. Vulnerabilidades medias
4. Mejoras de seguridad recomendadas

Para cada issue:
- Severity (Critical/High/Medium/Low)
- OWASP Category (si aplica)
- Exploit ejemplo
- Fix recomendado con código
```

### Tu Tarea

1. **Lee** el análisis de Claude
2. **Implementa** los fixes recomendados
3. **Pide re-audit**:

```markdown
Implementé tus recomendaciones. Audita esta nueva versión:

```python
[Tu código refactorizado]
```

¿Quedan vulnerabilidades? ¿Es seguro para producción?
```

4. **Itera** hasta que Claude diga "Aprobado para producción"

---

## Ejercicio 7: Real-World Tool (90 min)

### Proyecto Final

Diseña un tool REAL que necesitas en tu trabajo diario.

**Workflow con Claude**:

1. **Define requisitos** (15 min):

```markdown
Necesito un tool para [tu caso de uso real].

**Contexto**:
- [Describe tu workflow actual]
- [Qué hace manualmente un humano]
- [Qué debería hacer el agente]

**Requisitos funcionales**:
1. ...
2. ...

**Requisitos no funcionales**:
- Performance: [respuesta < X segundos]
- Security: [qué datos sensibles maneja]
- Reliability: [qué pasa si falla]
```

2. **Claude diseña** (20 min)
3. **Tú auditas** (20 min) - Usa checklist completa
4. **Claude refactoriza** (15 min)
5. **Tú implementas tests** (20 min)

**Prompt para tests**:

```markdown
Genera tests unitarios para este tool usando pytest.

Incluye:
1. Test happy path
2. Test de cada caso de error
3. Test de validación de inputs
4. Property-based test con Hypothesis
5. Mock de dependencias externas

Coverage objetivo: 90%+
```

---

## 📊 Rubrica de Evaluación

| Criterio | Peso | Evaluación |
|----------|------|------------|
| **Tool Design** | 30% | ¿Sigue best practices de Anthropic? |
| **Security** | 25% | ¿Previene vulnerabilidades comunes? |
| **Error Handling** | 20% | ¿Errores son accionables? |
| **Testing** | 15% | ¿Coverage >80%? ¿Tests significativos? |
| **Documentation** | 10% | ¿Description completa con ejemplos? |

---

## 🎓 Reflexión Final

Después de completar los ejercicios, responde:

1. **¿Qué diferencia clave notaste entre tools mal diseñados y bien diseñados?**

2. **¿Cuál fue el antipatrón más común que encontraste?**

3. **¿Cómo cambió tu forma de diseñar tools después de estos ejercicios?**

4. **¿En qué casos consolidarías tools vs mantenerlos separados?**

5. **¿Qué checklist mental usarás en el futuro al diseñar tools?**

---

## 📚 Recursos Adicionales

- [Anthropic Tool Use Guide](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

**Nota**: Estos ejercicios están diseñados para usar Claude como **asistente de aprendizaje**. El objetivo NO es que Claude haga todo el trabajo, sino que **tú aprendas a iterar con IA** para diseñar mejores tools.
