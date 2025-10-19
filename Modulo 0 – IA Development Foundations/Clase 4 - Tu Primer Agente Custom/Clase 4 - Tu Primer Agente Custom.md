# Clase 4 - Tu Primer Agente Custom

**Duración**: 6 horas
**Objetivo**: Crear agentes de IA especializados que actúan como asistentes educativos, entendiendo la diferencia entre "validar código" y "enseñar a programar", y diseñar tu primer agente custom para un problema específico.

---

## Índice

1. [Conceptos Clave](#1-conceptos-clave-45-min)
2. [Anatomía de un Agente Educativo](#2-anatomía-de-un-agente-educativo-1h)
3. [Agentes Existentes - Análisis](#3-agentes-existentes---análisis-1h)
4. [Crear Tu Primer Agente - Manual](#4-crear-tu-primer-agente---manual-15h)
5. [IA para Diseñar Agentes](#5-ia-para-diseñar-agentes-1h)
6. [Proyecto Final - Agente de Refactoring](#6-proyecto-final---agente-de-refactoring-45-min)
7. [Evaluación y Entregables](#7-evaluación-y-entregables)

---

## 1. Conceptos Clave (45 min)

### 1.1 ¿Qué es un Agente de IA? (15 min)

**Definición**: Un agente es una instancia de IA con **instrucciones específicas** (prompt system) diseñadas para resolver un **tipo particular de problemas**.

**Analogía**: Un médico general vs un cardiólogo.
- **IA General** (ChatGPT, Claude sin instrucciones): Médico general. Sabe de todo, pero no es experto en nada específico.
- **Agente Especializado** (con prompt system): Cardiólogo. Sabe TODO sobre el corazón, puede diagnosticar problemas cardíacos complejos.

**Ejemplo técnico**:

**IA General**:
```
Usuario: "Revisa mi código"
IA: "Tu código funciona pero podría mejorar en varios aspectos."
```

**Agente Especializado (Test Coverage Strategist)**:
```
Usuario: "Revisa mis tests"
Agente: "Detecté que estás en 75% coverage. Te falta testear:
1. Función crear_usuario() - CRÍTICO (maneja auth)
2. Validación de prioridad - MEDIO
3. Utils de fecha - BAJO

PRIORIZA así:
1. Tests de auth (riesgo alto)
2. Tests de validación (lógica de negocio)
3. Tests de utils (bajo riesgo)

¿Quieres que te explique cómo testear crear_usuario()?"
```

**Diferencia clave**: El agente tiene **contexto especializado** y **workflow específico**.

---

### 1.2 Agente Validator vs Agente Educational (15 min)

**Problema**: Muchos "agentes" solo validan, no enseñan.

**Agente Validator** (tradicional):
```
Input: Código con bug
Output: "❌ Error: Variable 'x' no definida. Arréglalo."
```

**Agente Educational** (este curso):
````
Input: Código con bug
Output:
"❌ Error: Variable 'x' no definida en línea 10.

🤔 POR QUÉ ocurre:
Python ejecuta código línea por línea. Cuando llega a línea 10,
busca la variable 'x' pero no la encuentra porque:
- La definiste en línea 15 (después de usarla)
- O olvidaste definirla

🔧 CÓMO arreglarlo:
1. Define 'x' ANTES de usarla:
```python
x = 10  # Línea 5 (antes de línea 10)
print(x)  # Línea 10 (ahora funciona)
```

💡 PRINCIPIO GENERAL:
En Python, debes DEFINIR variables antes de USARLAS.
El intérprete lee de arriba hacia abajo.

❓ ¿Entiendes por qué pasó esto? Explícamelo con tus palabras."
````

**Diferencia clave**:
- **Validator**: Solo señala el error
- **Educational**: Explica POR QUÉ, CÓMO arreglar, PRINCIPIO general, y VALIDA comprensión

**Tu objetivo en este máster**: Crear agentes que ENSEÑAN, no solo validan.

---

### 1.3 La Visión: "Un Ejército de Agentes" (15 min)

**Visión del máster**: Ser capaz de hacer proyectos grandes estando tú solo con **un ejército de agentes especializados**.

**Analogía**: Empresa de desarrollo.
- **Tú**: CEO/Arquitecto (decides QUÉ hacer)
- **Agentes**: Equipo especializado (CÓMO hacerlo)
  - Test Coverage Strategist = QA Lead
  - Clean Architecture Enforcer = Senior Architect
  - Security Hardening Mentor = Security Engineer
  - Git Commit Helper = DevOps Engineer

**Workflow ideal**:

```
1. Tienes idea de proyecto
2. Divides en tareas
3. Asignas cada tarea al agente especializado
4. Agentes te asisten con su expertise
5. Tú validas, decides, integras
```

**Ejemplo práctico**:

**Proyecto**: API de e-commerce

**División de trabajo**:
```
Tarea 1: Diseñar arquitectura
→ Agente: Clean Architecture Enforcer
→ Output: Estructura de carpetas, separación de capas

Tarea 2: Implementar auth
→ Agente: Security Hardening Mentor
→ Output: JWT, validación, hashing de passwords

Tarea 3: Escribir tests
→ Agente: Test Coverage Strategist
→ Output: Plan de tests, priorización, cobertura 80%+

Tarea 4: Documentar decisiones
→ Agente: (Tú en Clase 3 - ADRs)
→ Output: ADRs de arquitectura, tech stack

Tarea 5: Commits
→ Agente: Git Commit Helper
→ Output: Conventional commits, mensajes claros
```

**Tú coordinas** todo, **agentes asisten** en sus especialidades.

---

## 2. Anatomía de un Agente Educativo (1h)

### 2.1 Estructura de un Agente (15 min)

**Template básico** (archivo `.md` en `.claude/agents/`):

```markdown
# [Nombre del Agente]

**Rol**: [Especialidad específica - ej: "Mentor de testing"]

**Propósito**: [Qué ENSEÑA, no solo qué valida]

---

## Capacidades

1. [Qué puede hacer]
2. [Qué puede detectar]
3. [Qué puede explicar]

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
- Tono: [Educativo/Constructivo/Práctico]

---

## Restricciones

- NO hace: [Qué NO debe hacer]
- SÍ hace: [Qué SÍ debe hacer]

---

**Objetivo**: [Qué habilidad desarrolla en el estudiante]
```

---

### 2.2 Componentes Clave de un Agente (20 min)

#### 1. Rol y Propósito

**Rol**: Define la **identidad** del agente.

Ejemplos:
- ✅ "Mentor de seguridad que ENSEÑA, no solo audita"
- ✅ "Coach de arquitectura limpia especializado en SOLID"
- ❌ "Agente de validación" (muy genérico)
- ❌ "Helper" (sin identidad clara)

**Propósito**: Define **QUÉ enseña**.

Ejemplos:
- ✅ "Explicar vulnerabilidades de forma educativa, especialmente en código generado por IA"
- ✅ "Enseñar arquitectura limpia validando que el código sigue separation of concerns"
- ❌ "Revisar código" (no dice QUÉ enseña)

---

#### 2. Capacidades

Lista específica de **QUÉ puede hacer** el agente.

**Ejemplo** (Test Coverage Strategist):

```markdown
## Capacidades

1. Analizar reportes de coverage (pytest-cov, coverage.py)
2. Identificar gaps críticos vs gaps de bajo riesgo
3. Priorizar qué testear primero (auth > business logic > utils)
4. Explicar POR QUÉ un gap es crítico
5. Sugerir estrategias de testing (unit, integration, e2e)
6. ENSEÑAR cómo diseñar tests efectivos
```

**NO incluyas** capacidades genéricas:
- ❌ "Revisar código"
- ❌ "Ayudar con desarrollo"

---

#### 3. Workflow

**Paso a paso** de cómo opera el agente.

**Ejemplo** (Security Hardening Mentor):

```markdown
## Workflow

### Paso 1: Detectar vulnerabilidad
- Escanear código en busca de patrones inseguros
- Identificar OWASP category (A01, A02, etc.)

### Paso 2: Explicar el riesgo
- Describir QUÉ puede pasar si se explota
- Mostrar EJEMPLO de ataque (sin código malicioso real)

### Paso 3: Demostrar fix
- Mostrar código SEGURO
- Explicar POR QUÉ el fix funciona

### Paso 4: Enseñar prevención
- Principio general para evitar en futuro
- Checklist de validación
```

**Beneficio**: Workflow claro → Respuestas consistentes.

---

#### 4. Educational Approach

Define **CÓMO enseña** el agente.

**Elementos clave**:
- **Tono**: Educativo, constructivo, no alarmista
- **Estructura**: POR QUÉ → QUÉ → CÓMO → PREVENCIÓN
- **Ejemplos**: Siempre concretos, nunca abstractos
- **Validación**: Pregunta si el estudiante entendió

**Ejemplo**:

```markdown
## Educational Approach

**Tono**: Educativo, no alarmista

✅ "Esto permite SQL injection. Un atacante podría..."
✅ "Vamos a hacer esto más seguro. Aquí está cómo..."

❌ "Tu código es completamente inseguro"
❌ "Esto es terrible"

**Estructura de feedback**:
1. Contexto: Qué hace el código
2. Problema: Qué está mal
3. Riesgo: Qué puede pasar (con ejemplo)
4. Fix: Código correcto
5. Principio: Concepto general para prevenir

**Validación**: Siempre terminar con:
"¿Entiendes por qué esto es problema? Explícamelo con tus palabras."
```

---

#### 5. Restricciones

Define **QUÉ NO HACE** el agente (tan importante como qué sí hace).

**Ejemplo** (Test Coverage Strategist):

```markdown
## Restricciones

**NO hace**:
- ❌ NO genera tests automáticamente (solo enseña cómo)
- ❌ NO decide por el estudiante (sugiere, no impone)
- ❌ NO solo incrementa coverage sin explicar

**SÍ hace**:
- ✅ Explica QUÉ testear y POR QUÉ
- ✅ Prioriza gaps por criticidad
- ✅ Enseña estrategias de testing
- ✅ Valida comprensión del estudiante
```

**Beneficio**: Evita que el agente se convierta en "hace todo automáticamente".

---

### 2.3 Ejercicio: Analiza un Agente Existente (25 min)

**Tarea**: Lee el agente `test-coverage-strategist.md` (ya creado en `.claude/agents/educational/`).

**Preguntas**:
1. ¿Cuál es el **rol** del agente?
2. ¿Cuál es su **propósito educativo**?
3. Lista 3 **capacidades** del agente
4. Describe el **workflow** en 3 pasos
5. ¿Qué NO hace este agente? (restricciones)
6. ¿Qué habilidad desarrolla en el estudiante?

**Tiempo**: 15 min de lectura + 10 min de respuestas

**Validación**: Compara tus respuestas con el contenido del archivo.

---

## 3. Agentes Existentes - Análisis (1h)

### 3.1 Agentes Tier 1 (Críticos para el Máster) (30 min)

Ya tienes 4 agentes creados en `.claude/agents/educational/`:

1. **test-coverage-strategist.md**
2. **clean-architecture-enforcer.md**
3. **git-commit-helper.md**
4. **security-hardening-mentor.md**

**Tarea**: Lee TODOS los agentes (10 min cada uno = 40 min total).

Para cada agente, identifica:
- **Especialidad**: En qué es experto
- **Cuándo usarlo**: Qué situaciones requieren este agente
- **Qué enseña**: Skill que desarrolla

---

### 3.2 Comparación de Agentes (15 min)

**Crea una tabla comparativa**:

| Agente | Especialidad | Cuándo usar | Skill que desarrolla |
|--------|-------------|-------------|---------------------|
| Test Coverage Strategist | Coverage optimization | Estás <80% coverage | Diseñar tests efectivos |
| Clean Architecture Enforcer | SOLID, separation of concerns | Código mezclado entre capas | Arquitectura limpia |
| Git Commit Helper | Conventional Commits | Antes de commit | Mensajes descriptivos |
| Security Hardening Mentor | OWASP, seguridad | Código de auth/security | Código seguro |

**Observación**: Cada agente cubre un **aspecto diferente** del desarrollo. No hay overlap.

---

### 3.3 Ejercicio: Cuándo Usar Cada Agente (15 min)

**Escenarios**: Para cada situación, elige qué agente invocar.

**Situación 1**: Acabas de implementar un endpoint POST /usuarios con password hashing.
- **Agente**: ?
- **Por qué**: ?

<details>
<summary>Respuesta</summary>

**Agente**: Security Hardening Mentor
**Por qué**: Código de auth/security SIEMPRE debe revisarse por seguridad. El agente verificará:
- ¿Password bien hasheado? (bcrypt, no plain text)
- ¿Secrets en env vars?
- ¿Validación de inputs?
</details>

---

**Situación 2**: Tus tests están en 75% coverage y no sabes cómo llegar a 80%.
- **Agente**: ?
- **Por qué**: ?

<details>
<summary>Respuesta</summary>

**Agente**: Test Coverage Strategist
**Por qué**: Especializado en analizar gaps, priorizar qué testear, y enseñar estrategias para alcanzar coverage mínimo.
</details>

---

**Situación 3**: Tienes business logic en endpoints (api.py).
- **Agente**: ?
- **Por qué**: ?

<details>
<summary>Respuesta</summary>

**Agente**: Clean Architecture Enforcer
**Por qué**: Detecta violaciones de separation of concerns, explica por qué es malo, y sugiere refactoring para mover lógica a Service layer.
</details>

---

**Situación 4**: Hiciste cambios y no sabes qué commit message usar.
- **Agente**: ?
- **Por qué**: ?

<details>
<summary>Respuesta</summary>

**Agente**: Git Commit Helper
**Por qué**: Analiza cambios, sugiere mensaje Conventional Commit, y explica por qué ese type/scope es apropiado.
</details>

---

## 4. Crear Tu Primer Agente - Manual (1.5h)

### 4.1 Proceso de Diseño de un Agente (20 min)

**Paso 1: Identificar el Problema** (5 min)

Pregunta: **¿Qué problema recurrente tienes que un agente podría asistir?**

Ejemplos:
- "Olvido documentar funciones con docstrings"
- "Mis variables tienen nombres vagos (x, temp, data)"
- "No sé cómo estructurar tests (dónde van fixtures, helpers)"
- "Duplico código en múltiples archivos"

**Tu problema**: ______________ (escribe uno real que tengas)

---

**Paso 2: Definir el Rol** (5 min)

Pregunta: **¿Qué especialista resolvería este problema?**

Ejemplos:
- Problema: "Olvido docstrings" → Rol: "Mentor de Documentación de Código"
- Problema: "Variables mal nombradas" → Rol: "Coach de Clean Code y Naming"
- Problema: "Tests desordenados" → Rol: "Arquitecto de Tests"

**Tu rol**: ______________ (para tu problema)

---

**Paso 3: Definir Capacidades** (5 min)

Pregunta: **¿Qué debe SABER hacer este agente?**

Ejemplo (Mentor de Documentación):
1. Detectar funciones sin docstrings
2. Sugerir docstrings en formato Google/NumPy
3. Explicar POR QUÉ documentar (mantenibilidad, onboarding)
4. Enseñar CUÁNDO documentar (funciones públicas siempre, privadas si complejas)

**Tus capacidades** (lista 3-5): ______________

---

**Paso 4: Definir Workflow** (5 min)

Pregunta: **¿Qué pasos sigue el agente al trabajar?**

Ejemplo (Mentor de Documentación):
1. Escanear archivo en busca de funciones sin docstrings
2. Analizar complejidad de cada función (simple vs compleja)
3. Priorizar documentación (funciones públicas primero)
4. Generar docstring sugerido con explicación
5. Enseñar principio general (cuándo documentar)

**Tu workflow** (3-5 pasos): ______________

---

### 4.2 Escribir el Agente (40 min)

**Tarea**: Crea un archivo `.claude/agents/educational/mi-primer-agente.md`

**Usa el template**:

```markdown
# [Nombre de Tu Agente]

**Rol**: [Especialista en X]

**Propósito**: [Qué enseña, no solo qué valida]

---

## Capacidades

1. [Capacidad 1]
2. [Capacidad 2]
3. [Capacidad 3]

---

## Workflow

### Paso 1: [Primer paso]
[Descripción detallada]

### Paso 2: [Segundo paso]
[Descripción]

### Paso 3: [Tercer paso]
[Descripción]

---

## Educational Approach

**Tono**: [Educativo/Constructivo/Práctico]

**Estructura de feedback**:
1. [Elemento 1]
2. [Elemento 2]
3. [Elemento 3]

**Ejemplos**: [Siempre incluir ejemplos concretos]

---

## Restricciones

**NO hace**:
- ❌ [Qué NO debe hacer]
- ❌ [Qué NO debe hacer]

**SÍ hace**:
- ✅ [Qué SÍ debe hacer]
- ✅ [Qué SÍ debe hacer]

---

**Objetivo**: [Qué habilidad desarrolla en el estudiante]
```

**Tiempo**: 30 min de escritura + 10 min de validación

---

### 4.3 Validar Tu Agente (30 min)

**Checklist de validación**:

- [ ] **Rol claro**: ¿Se entiende en qué es especialista?
- [ ] **Propósito educativo**: ¿Dice QUÉ enseña, no solo qué valida?
- [ ] **Capacidades específicas**: ¿Son concretas, no genéricas?
- [ ] **Workflow detallado**: ¿Tiene 3+ pasos claros?
- [ ] **Educational Approach**: ¿Define CÓMO enseña?
- [ ] **Restricciones**: ¿Dice qué NO hace?
- [ ] **Objetivo claro**: ¿Qué skill desarrolla?

**Validación práctica**: Muéstrale tu agente a otra persona. Pregunta:
1. ¿Entiendes qué hace este agente?
2. ¿Cuándo lo usarías?
3. ¿Qué te enseñaría?

Si responde correctamente a las 3 preguntas → Agente bien diseñado ✅

---

## 5. IA para Diseñar Agentes (1h)

### 5.1 IA Como Asistente de Diseño (15 min)

**Pattern**: TÚ defines el problema → IA genera template → TÚ personalizas

**Ejemplo**:

**Tu problema**: "Olvido añadir type hints a funciones Python"

**Prompt para IA**:

```bash
claude "Diseña un agente educativo especializado en enseñar type hints en Python.

Contexto:
- Soy estudiante que olvida añadir type hints a funciones
- Quiero que el agente ENSEÑE por qué type hints importan
- No quiero que solo genere type hints automáticamente

Genera un template de agente siguiendo esta estructura:
1. Rol y Propósito
2. Capacidades (qué detecta, qué enseña)
3. Workflow (pasos que sigue)
4. Educational Approach (cómo enseña)
5. Restricciones (qué NO hace)

El agente debe ser EDUCATIVO, no solo un validator."
```

**IA genera**:

`````markdown
# Type Hints Coach

**Rol**: Mentor de Python moderno especializado en type hints y type safety

**Propósito**: Enseñar POR QUÉ type hints mejoran código, CÓMO usarlos efectivamente, y CUÁNDO son críticos vs opcionales.

---

## Capacidades

1. Detectar funciones sin type hints
2. Analizar complejidad de tipos (simple vs generic)
3. Explicar beneficios (IDE support, bug detection, documentación)
4. Enseñar sintaxis (List[str], Optional[int], Union, etc.)
5. Mostrar herramientas (mypy, type checkers)

---

## Workflow

### Paso 1: Escanear código
- Identificar funciones sin type hints
- Clasificar por criticidad (API públicas > internas)

### Paso 2: Analizar tipos
- Determinar tipos de parámetros y return
- Detectar casos complejos (Union, Optional, Generic)

### Paso 3: Enseñar con ejemplos
- Mostrar código SIN type hints (problemas)
- Mostrar código CON type hints (beneficios)
- Explicar cómo IDE usa esta información

### Paso 4: Herramientas
- Introducir mypy para validación
- Enseñar cómo correr type checking

---

## Educational Approach

**Tono**: Práctico y motivador

**Estructura de feedback**:
````markdown
## Función sin type hints detectada

**Código actual**:
```python
def calcular_total(items):
    return sum(items)
```

**Problema**: Sin type hints, IDE no puede ayudarte:
- No autocomplete para 'items'
- No detección de errores (pasar string por error)

**Solución con type hints**:
```python
from typing import List

def calcular_total(items: List[float]) -> float:
    return sum(items)
```

**Beneficios**:
✅ IDE muestra que 'items' es lista de floats
✅ Error si pasas tipo incorrecto
✅ Documentación auto-generada

**Herramienta**:
```bash
mypy mi_codigo.py  # Valida tipos
```

**¿Ves la diferencia? Prueba añadir type hints a una función tuya.**
````

---

## Restricciones

**NO hace**:
- ❌ NO añade type hints automáticamente sin explicar
- ❌ NO obliga type hints en TODOS lados (algunos casos no valen la pena)
- ❌ NO asume que type hints son siempre necesarios

**SÍ hace**:
- ✅ Explica POR QUÉ type hints ayudan
- ✅ Muestra CÓMO añadirlos paso a paso
- ✅ Enseña CUÁNDO son críticos (APIs, funciones complejas)
- ✅ Introduce herramientas (mypy)

---

**Objetivo**: Desarrollador que usa type hints conscientemente, no ciegamente.
`````

**Tu trabajo**: Revisar, personalizar, mejorar con tu experiencia.

---

### 5.2 Ejercicio: IA Genera, Tú Mejoras (30 min)

**Tarea**: Elige un problema que tengas y usa IA para generar template de agente.

**Problemas sugeridos**:
1. "Duplico código en múltiples archivos" → Agente: DRY Enforcer
2. "Mis funciones son muy largas (50+ líneas)" → Agente: Function Complexity Coach
3. "No sé cuándo usar clases vs funciones" → Agente: OOP vs FP Advisor
4. "Mis tests no cubren edge cases" → Agente: Edge Case Detective

**Prompt template**:

```bash
claude "Diseña un agente educativo para enseñar [TEMA].

Problema que tengo: [DESCRIPCIÓN]

Contexto: [TU NIVEL, TU SITUACIÓN]

Requisitos:
- Debe ENSEÑAR, no solo validar
- Debe explicar POR QUÉ
- Debe mostrar ejemplos concretos

Genera template con: Rol, Propósito, Capacidades, Workflow, Educational Approach, Restricciones, Objetivo"
```

**Tiempo**: 10 min IA genera + 20 min tú personalizas

**Validación**: ¿El agente generado es EDUCATIVO o solo validador?

---

### 5.3 Iterar con IA (15 min)

**Pattern**: Generación inicial → Feedback → Iteración

**Ejemplo**:

**Primera generación de IA** (demasiado genérica):
```markdown
# Code Quality Enforcer

**Rol**: Validador de calidad de código

**Propósito**: Revisar código y señalar problemas
```

**Tu feedback a IA**:

```bash
claude "Este agente es demasiado genérico. Reescríbelo con:

1. Especialidad ESPECÍFICA (no 'calidad general', sino algo como 'complejidad de funciones')
2. Enfoque EDUCATIVO (explicar POR QUÉ complejidad es mala)
3. Workflow DETALLADO (qué pasos sigue)
4. Restricciones CLARAS (qué NO hace)

Usa como ejemplo el Clean Architecture Enforcer que ya tengo en .claude/agents/educational/"
```

**IA itera** y genera versión mejorada.

**Repetir hasta** que el agente sea específico, educativo, y detallado.

---

## 6. Proyecto Final - Agente de Refactoring (45 min)

### 6.1 Contexto del Proyecto

**Problema común**: Código que crece sin estructura, funciones largas, duplicación.

**Solución**: Agente que ENSEÑA refactoring, no solo lo hace automáticamente.

**Tu tarea**: Crear un agente `refactoring-mentor.md`

---

### 6.2 Requisitos del Agente

**Nombre**: Refactoring Mentor

**Rol**: Coach de refactoring que enseña cómo mejorar código existente sin cambiar comportamiento

**Especialidad**: Detectar code smells (funciones largas, duplicación, nombres vagos) y enseñar técnicas de refactoring

**Capacidades mínimas**:
1. Detectar code smells (funciones >50 líneas, duplicación, nombres vagos)
2. Clasificar por gravedad (crítico, medio, bajo)
3. Explicar POR QUÉ cada smell es problema
4. Enseñar técnica de refactoring apropiada (Extract Method, Rename Variable, etc.)
5. Mostrar código ANTES y DESPUÉS del refactoring

**Workflow mínimo**:
1. Escanear código en busca de code smells
2. Priorizar por impacto (funciones largas > nombres vagos)
3. Explicar el smell con ejemplo
4. Enseñar técnica de refactoring
5. Mostrar refactoring paso a paso

**Educational Approach**:
- Tono: Constructivo, motivador (no crítico)
- Estructura: SMELL → POR QUÉ MALO → TÉCNICA → EJEMPLO ANTES/DESPUÉS
- Validación: Preguntar si el estudiante entiende el cambio

**Restricciones**:
- NO hace refactoring automático completo
- SÍ enseña técnicas paso a paso
- SÍ explica beneficios de cada cambio

---

### 6.3 Ejemplo de Output Esperado

**Input**: Código con función larga

```python
def procesar_pedido(pedido):
    # Validar cliente (10 líneas)
    if not pedido.cliente:
        raise ValueError("Cliente requerido")
    if not pedido.cliente.email:
        raise ValueError("Email requerido")
    # ... más validaciones

    # Calcular total (15 líneas)
    total = 0
    for item in pedido.items:
        precio = item.precio
        if item.descuento:
            precio = precio * (1 - item.descuento)
        total += precio * item.cantidad

    # Guardar en DB (10 líneas)
    db.connect()
    db.insert(pedido)
    db.commit()
    db.close()

    # Enviar email (10 líneas)
    # ... código de email

    return pedido
```

**Output del agente**:

```markdown
## 🔍 Code Smell Detectado: Función Larga (Long Method)

**Función**: `procesar_pedido()` - 50+ líneas

**POR QUÉ es problema**:
1. Difícil de entender (hace 4 cosas distintas)
2. Difícil de testear (tienes que mockear cliente, DB, email)
3. Rompe Single Responsibility Principle

**TÉCNICA de refactoring**: Extract Method

**CÓMO refactorizar** (paso a paso):

### Paso 1: Identifica bloques lógicos
- Validación → `validar_cliente()`
- Cálculo → `calcular_total()`
- DB → `guardar_pedido()`
- Email → `enviar_confirmacion()`

### Paso 2: Extrae cada bloque a función

**ANTES** (función larga):
```python
def procesar_pedido(pedido):
    # Validar (10 líneas)
    if not pedido.cliente:
        raise ValueError("Cliente requerido")
    # ...

    # Calcular (15 líneas)
    total = 0
    # ...

    # ...
```

**DESPUÉS** (funciones pequeñas):
```python
def procesar_pedido(pedido):
    validar_cliente(pedido.cliente)
    total = calcular_total(pedido.items)
    guardar_pedido(pedido)
    enviar_confirmacion(pedido)
    return pedido

def validar_cliente(cliente):
    if not cliente:
        raise ValueError("Cliente requerido")
    if not cliente.email:
        raise ValueError("Email requerido")

def calcular_total(items):
    total = 0
    for item in items:
        precio = aplicar_descuento(item)
        total += precio * item.cantidad
    return total

# ... otras funciones
```

**BENEFICIOS**:
✅ Función principal es CLARA (5 líneas, fácil de entender)
✅ Cada función tiene UNA responsabilidad
✅ Fácil de testear (test cada función por separado)
✅ Reusable (calcular_total() se puede usar en otros lados)

**PRINCIPIO**: Una función debe hacer UNA COSA, y hacerla bien.

**Ejercicio**: Identifica en tu código una función larga y extrae 2-3 métodos.
¿Qué funciones extraerías? Explícamelo.
```

---

### 6.4 Implementación (30 min)

**Archivo**: `.claude/agents/educational/refactoring-mentor.md`

**Estructura**:
1. Rol y Propósito (5 min)
2. Capacidades (5 min)
3. Workflow (10 min)
4. Educational Approach con ejemplos (10 min)
5. Restricciones (5 min)

**Validación**:
- [ ] Tiene ejemplos concretos de code smells
- [ ] Enseña técnicas de refactoring específicas
- [ ] Muestra código ANTES/DESPUÉS
- [ ] Explica POR QUÉ y BENEFICIOS
- [ ] Tono constructivo, no crítico

---

## 7. Evaluación y Entregables

### 7.1 Entregables de la Clase

1. **Análisis de agentes existentes** (Ejercicio 2.3) - 10%
2. **Tabla comparativa de agentes** (Ejercicio 3.2) - 10%
3. **Mi primer agente** (Ejercicio 4.2) - 30%
4. **Refactoring Mentor** (Proyecto Final) - 50%

**Mínimo para aprobar**: 70/100

---

### 7.2 Rúbrica del Proyecto Final (Refactoring Mentor)

#### Rol y Propósito (10 puntos)
- [ ] Rol específico y claro (3 pts)
- [ ] Propósito educativo bien definido (4 pts)
- [ ] Enfoque en enseñar, no solo validar (3 pts)

#### Capacidades (10 puntos)
- [ ] Mínimo 5 capacidades (2 pts)
- [ ] Capacidades específicas, no genéricas (4 pts)
- [ ] Incluye detección + enseñanza (4 pts)

#### Workflow (15 puntos)
- [ ] Mínimo 5 pasos (3 pts)
- [ ] Pasos claros y detallados (6 pts)
- [ ] Workflow lógico (detección → priorización → enseñanza) (6 pts)

#### Educational Approach (15 puntos)
- [ ] Tono definido (constructivo, no crítico) (3 pts)
- [ ] Estructura de feedback clara (SMELL → POR QUÉ → TÉCNICA → EJEMPLO) (6 pts)
- [ ] Incluye validación de comprensión (3 pts)
- [ ] Mínimo 2 ejemplos concretos (ANTES/DESPUÉS) (3 pts)

#### Restricciones (5 puntos)
- [ ] Define qué NO hace (3 pts)
- [ ] Define qué SÍ hace (2 pts)

#### Calidad General (5 puntos)
- [ ] Formato Markdown correcto (1 pt)
- [ ] Sin errores ortográficos (1 pt)
- [ ] Objetivo claro (qué habilidad desarrolla) (2 pts)
- [ ] Agente es REALMENTE educativo (1 pt)

**Total**: 60 puntos (50% de la nota final)

---

### 7.3 Autoevaluación

- [ ] ¿Entiendo la diferencia entre validator y educational agent?
- [ ] ¿Puedo diseñar un agente desde cero sin IA?
- [ ] ¿Puedo usar IA para generar templates y luego personalizarlos?
- [ ] ¿Mi agente ENSEÑA o solo valida?
- [ ] ¿El workflow de mi agente tiene sentido?
- [ ] ¿Incluí ejemplos concretos, no solo teoría?

**Si respondiste NO a 2+ preguntas**: Repasa las secciones correspondientes.

---

### 7.4 Recursos Adicionales

**Agentes Existentes para Estudiar**:
- `.claude/agents/educational/test-coverage-strategist.md`
- `.claude/agents/educational/clean-architecture-enforcer.md`
- `.claude/agents/educational/git-commit-helper.md`
- `.claude/agents/educational/security-hardening-mentor.md`

**Libros sobre Teaching**:
- "Make It Stick" (técnicas de enseñanza efectiva)
- "The Pragmatic Programmer" (principios de código limpio)

**Refactoring**:
- Martin Fowler - "Refactoring: Improving the Design of Existing Code"
- Catalog de refactorings: https://refactoring.com/catalog/

---

## Resumen de la Clase

En esta clase aprendiste:

1. **Diferencia clave**: Validator vs Educational Agent
2. **Anatomía de un agente**: Rol, Capacidades, Workflow, Educational Approach, Restricciones
3. **Análisis de agentes existentes**: 4 agentes tier 1 ya disponibles
4. **Diseño manual**: Crear agente desde cero identificando problema → rol → capacidades → workflow
5. **IA como asistente**: Generar templates, iterar, personalizar
6. **Proyecto**: Refactoring Mentor (agente educativo completo)

**Skill clave**: Diseñar agentes especializados que ENSEÑAN, no solo validan.

**Visión**: Construir tu "ejército de agentes" para asistirte en desarrollo.

**Próxima clase**: Clase 5 - Prompt Engineering Avanzado (técnicas para obtener mejor output de agentes).

---

**Regla de oro para agentes educativos**: Si el estudiante no aprende el concepto después de usar el agente, el agente falló (aunque haya arreglado el código).

¡Tu agente debe ser un MAESTRO, no solo una herramienta!
