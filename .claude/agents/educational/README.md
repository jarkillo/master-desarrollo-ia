# Educational Agents Library

**Propósito**: Agentes especializados para enseñar desarrollo con IA, no solo validar código.

---

## Filosofía de los Agentes Educativos

Estos agentes son **profesores virtuales**, no solo herramientas de validación.

### Diferencia clave:

**Agente Validator** (tradicional):
```
Input: Código
Output: "❌ Esto está mal. Arréglalo."
```

**Agente Educational** (este repo):
```
Input: Código
Output:
- "⚠️ Detecté este problema: [explicación]"
- "Por qué es problema: [contexto]"
- "Cómo arreglarlo: [solución con código]"
- "Cómo prevenir en futuro: [principio general]"
- "¿Entiendes? Explícame con tus palabras."
```

---

## Agentes Disponibles

### Tier 1 (Críticos para el Máster)

#### 1. **test-coverage-strategist.md**
**Especialidad**: Arquitectura de tests, coverage optimization

**Cuándo usarlo**:
- Estudiante está en <80% coverage
- Tests duplicados o mal organizados
- No sabe qué testear

**No hace**: No genera tests automáticamente
**Sí hace**: Explica QUÉ testear, POR QUÉ, y cómo priorizar

**Ejemplo de invocación**:
```
"Revisa mis tests. Estoy en 75% coverage y no sé cómo llegar a 80%."
```

---

#### 2. **clean-architecture-enforcer.md**
**Especialidad**: SOLID principles, separation of concerns

**Cuándo usarlo**:
- Código mezclado entre capas (API/Service/Repository)
- Business logic en endpoints
- God classes creciendo

**No hace**: No refactoriza automáticamente
**Sí hace**: Detecta violaciones, explica por qué importa, sugiere refactoring

**Ejemplo de invocación**:
```
"¿Mi arquitectura está bien? Revisa separación de capas."
```

---

#### 3. **git-commit-helper.md**
**Especialidad**: Conventional Commits, mensajes descriptivos

**Cuándo usarlo**:
- Antes de hacer commit
- No sabes qué type usar (feat/fix/refactor)
- Commit message vago

**No hace**: No hace commits automáticamente
**Sí hace**: Analiza cambios, sugiere mensaje, explica por qué

**Ejemplo de invocación**:
```
"Ayúdame a escribir un buen commit message para estos cambios."
```

---

#### 4. **security-hardening-mentor.md**
**Especialidad**: OWASP, seguridad en código IA-generated

**Cuándo usarlo**:
- Código de auth/security (SIEMPRE)
- Después de generar código con IA
- Antes de merge a main

**No hace**: No solo lista vulnerabilidades
**Sí hace**: Explica exploit, muestra fix, enseña prevención

**Ejemplo de invocación**:
```
"Revisa mi código de JWT. ¿Es seguro?"
```

---

## Tier 2 (Próximamente)

**fastapi-design-coach.md**:
- REST API design
- Pydantic validation
- Async/await patterns

**docker-infrastructure-guide.md**:
- Dockerfile optimization
- Docker Compose
- Deployment

**python-best-practices-coach.md**:
- Type hints
- Pythonic patterns
- Code quality

---

## Cómo Usar los Agentes

### Método 1: Invocación Directa (Claude Code CLI)

```bash
# Invocar agente específico
claude --agent test-coverage-strategist "Revisa mis tests"

# O con contexto de archivos
claude --agent clean-architecture-enforcer --files api/*.py "Valida arquitectura"
```

### Método 2: Mención en Prompt

```
"@test-coverage-strategist: Estoy en 75% coverage. ¿Qué me falta?"
```

### Método 3: Workflow Automatizado

En tu flujo de desarrollo:

```bash
# Antes de commit
claude --agent git-commit-helper

# Antes de PR
claude --agent clean-architecture-enforcer --files api/
claude --agent security-hardening-mentor --files api/

# Después de escribir tests
claude --agent test-coverage-strategist
```

---

## Mejores Prácticas

### ✅ Úsalos cuando:
- Estás aprendiendo un concepto
- Código generado por IA (SIEMPRE revisar con Security Mentor)
- Atascado en problema (coverage, arquitectura)
- Quieres segunda opinión

### ❌ No los uses cuando:
- Solo quieres "pasar" validación sin aprender
- Esperas que arreglen todo automáticamente
- No estás dispuesto a iterar y mejorar

---

## Progresión de Uso

### Semana 1-4 (Novice):
Usa agentes para TODO:
- Git Commit Helper en cada commit
- Test Coverage para cada test suite
- Aprendiendo patrones

### Semana 5-8 (Intermediate):
Usa agentes selectivamente:
- Security Mentor en código crítico
- Architecture Enforcer en refactors grandes
- Internalizando principios

### Semana 9+ (Advanced):
Usas agentes como segunda opinión:
- Tú sabes qué hacer
- Agente valida tu razonamiento
- Discutes trade-offs con agente

---

## Customización

Puedes crear tus propios agentes educativos:

### Template de Agente

```markdown
# [Nombre del Agente]

**Rol**: [Especialidad específica]

**Propósito**: [Qué enseña, no solo qué valida]

---

## Capacidades

1. [Capacidad 1]
2. [Capacidad 2]

---

## Workflow

### Paso 1: [Qué hace primero]
### Paso 2: [Análisis]
### Paso 3: [Feedback educativo]

---

## Educational Approach

- Explica POR QUÉ
- Muestra ejemplos concretos
- Enseña prevención
- Tono: Educativo, constructivo

---

**Objetivo**: [Qué habilidad desarrolla en el estudiante]
```

---

## Contribuir

¿Creaste un agente útil? Compártelo:

1. Sigue el template
2. Enfócate en ENSEÑAR, no solo validar
3. Incluye ejemplos concretos
4. Explica el "por qué", no solo el "qué"
5. Añade a este README

---

## Feedback

Si un agente:
- ✅ Te ayudó a entender un concepto → Excelente
- ⚠️ Solo te dio respuestas sin explicar → Mejora el agente
- ❌ Hiciste lo que dijo sin entender → Pregunta más, itera

**Regla de oro**: Si no entiendes el feedback del agente, pregúntale que explique mejor.

---

## Diferencia con Agentes de Proyecto (Cuadro Merca)

### Educational Agents (aquí):
- **Objetivo**: Enseñar
- **Audiencia**: Estudiantes aprendiendo
- **Enfoque**: "Por qué" y "cómo aprender"
- **Generalizable**: Cualquier proyecto Python/FastAPI

### Project Agents (`.claude/agents/cuadro-merca/`):
- **Objetivo**: Validar y automatizar
- **Audiencia**: Desarrollo en producción
- **Enfoque**: Enforcement de reglas
- **Específico**: Solo para proyecto Cuadro Merca

**Ambos son valiosos**, pero para diferentes contextos.

---

## Roadmap

### Próximos agentes a crear:

**Corto plazo** (1-2 semanas):
- [ ] fastapi-design-coach
- [ ] python-best-practices-coach
- [ ] docker-infrastructure-guide

**Mediano plazo** (1 mes):
- [ ] database-orm-specialist
- [ ] frontend-integration-coach
- [ ] performance-profiler

**Largo plazo** (2-3 meses):
- [ ] cicd-pipeline-optimizer
- [ ] observability-monitoring-teacher
- [ ] git-workflow-educator

---

## Métricas de Éxito

Un agente educativo es exitoso si:

- ✅ Estudiantes entienden conceptos (no solo copian soluciones)
- ✅ Preguntan "¿por qué?" y agente puede explicar
- ✅ Después de usarlo varias veces, necesitan usarlo menos
- ✅ Estudiantes pueden explicar principios a otros

---

## Notas Finales

**Filosofía**:
> "Dale un pescado a un desarrollador y comerá un día. Enséñale a pescar (y a usar agentes IA) y comerá siempre."

Estos agentes son **entrenadores**, no **hacedores**. El objetivo es que el estudiante aprenda a desarrollar con IA como copiloto, no como piloto automático.

**Visión del máster**: "Un desarrollador solo con un ejército de agentes"

Estos agentes son tu primer ejército. Aprende a liderarlos.

🚀
