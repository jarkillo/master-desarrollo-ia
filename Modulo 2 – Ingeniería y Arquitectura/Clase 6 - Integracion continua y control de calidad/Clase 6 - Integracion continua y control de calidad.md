# 🧠 Clase 6 - Integración continua y control de calidad arquitectónica

*(Módulo 2 – Ingeniería y Arquitectura)*

## 🧠 Antes de empezar

Hasta ahora has construido una API que no solo funciona, sino que **se sostiene con dignidad**:

- Tiene capas separadas (API, servicio, repositorio).
- Los tests cubren sus funcionalidades básicas.
- Puedes cambiar de memoria a JSON sin romper nada.

Pero te falta lo más importante si quieres que este proyecto crezca:

> Que nadie (ni tú mismo en 3 semanas) pueda romperlo sin enterarse.
> 

Aquí entra en juego la **Integración Continua (CI)**:

Un sistema que lanza los tests automáticamente **cada vez que haces push o abres un PR**.

Si todo va bien → ✅

Si algo se rompe → ❌ GitHub te lo canta sin que nadie lo tenga que revisar a mano.

---

## 🎯 ¿Qué vamos a montar hoy?

Una mini-fábrica que se encargue de:

1. Ejecutar los tests automáticamente.
2. Avisarte si algo falla.
3. (Más adelante) Medir cobertura, pasar linters, y desplegar.

No más “¡en mi máquina funciona!” ni “se me olvidó correr los tests”.

---

## 🧪 Paso a paso (a mano)

### 1. Crea la carpeta donde viven los workflows de GitHub:

```bash
mkdir -p .github/workflows

```
Importante, esto es en la raiz de tu proyecto

Y… ¿recuerdas que en la clase 2 generamos un requirements.txt? metelo tambien en la raiz

### 2. Dentro, crea el archivo `ci.yml`:

```yaml
name: CI - Tests automáticos

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Clonar el repo
        uses: actions/checkout@v4

      - name: Instalar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Instalar dependencias
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Ejecutar tests
        run: pytest -v

```

Guarda, haz commit, empuja la rama y abre PR.

GitHub va a lanzar automáticamente el workflow y te dirá si todo está OK o si se ha roto algo.

---

## 🤖 Orquestación Multi-Agente: Tu Ejército de Especialistas

Hasta ahora has trabajado con la IA como un "asistente general". Pero cuando construyes un proyecto completo (como este API de tareas), necesitas **especialistas que trabajen en equipo**.

Aquí entra la **orquestación de agentes**: usar múltiples agentes IA especializados, cada uno experto en su dominio, coordinados para lograr un objetivo común.

> **Analogía**: No contratas a un "constructor general" para hacer tu casa. Contratas un arquitecto, un electricista, un plomero, un carpintero... cada uno experto en su área.

### 🎯 Los 4 Agentes Especializados para este Proyecto

En el desarrollo del proyecto final del Módulo 2, vas a orquestar **4 agentes educacionales**:

#### 1️⃣ **Clean Architecture Enforcer**
   - **Especialidad**: Validar arquitectura en capas y principios SOLID
   - **Cuándo usarlo**: Al inicio (diseño) y al final (validación)
   - **Qué detecta**: Violaciones de separación de capas, dependency inversion, single responsibility
   - **Ubicación**: `.claude/agents/educational/clean-architecture-enforcer.md`

#### 2️⃣ **FastAPI Design Coach**
   - **Especialidad**: Diseño profesional de endpoints FastAPI
   - **Cuándo usarlo**: Al implementar endpoints, modelos Pydantic, async patterns
   - **Qué detecta**: Endpoints no-RESTful, validación incompleta, blocking I/O en async
   - **Ubicación**: `.claude/agents/educational/fastapi-design-coach.md`

#### 3️⃣ **API Design Reviewer**
   - **Especialidad**: Diseño RESTful, HTTP semantics, OpenAPI documentation
   - **Cuándo usarlo**: Al finalizar endpoints, antes de desplegar
   - **Qué detecta**: Status codes incorrectos, responses inconsistentes, URLs no-RESTful
   - **Ubicación**: `.claude/agents/educational/api-design-reviewer.md`

#### 4️⃣ **Test Coverage Strategist** (Python Best Practices Coach)
   - **Especialidad**: Testing completo (unit + integration), coverage strategies
   - **Cuándo usarlo**: Después de implementar cada feature
   - **Qué detecta**: Tests faltantes, coverage gaps, test anti-patterns
   - **Ubicación**: `.claude/agents/educational/python-best-practices-coach.md`

---

## 🔄 Workflow Completo: Desarrollo del Proyecto Final con Agentes

Aquí está el **workflow paso a paso** para desarrollar el proyecto final del Módulo 2 (API de tareas completa) usando orquestación de agentes:

### **Fase 1: Diseño Arquitectónico** (con Clean Architecture Enforcer)

**Objetivo**: Validar que tu diseño sigue arquitectura limpia ANTES de escribir código.

**Prompt para el agente**:
```markdown
Rol: Clean Architecture Enforcer
Contexto: Voy a desarrollar una API de tareas con FastAPI siguiendo arquitectura en capas.
Objetivo: Valida este diseño arquitectónico y sugiere mejoras.

Diseño propuesto:
- API Layer: FastAPI endpoints (api.py)
- Service Layer: Lógica de negocio (servicio_tareas.py)
- Repository Layer:
  - Protocol (repositorio_base.py)
  - Implementaciones: RepositorioMemoria, RepositorioJSON

¿Este diseño sigue SOLID? ¿Qué violaciones ves? ¿Qué mejorarías?
```

**Output esperado del agente**:
- ✅ Validación de separación de capas
- ✅ Verificación de Dependency Inversion
- ⚠️ Sugerencias de mejora (ej: "Añadir abstracción de dependencias.py")
- 📚 Explicación de principios SOLID aplicados

**Acción**: Ajustar el diseño según el feedback antes de codear.

---

### **Fase 2: Implementación de Endpoints** (con FastAPI Design Coach)

**Objetivo**: Desarrollar endpoints profesionales con validación completa.

**Prompt para el agente**:
```markdown
Rol: FastAPI Design Coach
Contexto: Estoy implementando endpoints para mi API de tareas.
Objetivo: Revisa este endpoint y sugiere mejoras en diseño FastAPI.

Endpoint propuesto:
```python
@app.post("/tareas")
def crear_tarea(titulo: str, descripcion: str):
    tarea = servicio.crear_tarea(titulo, descripcion)
    return tarea
```

¿Qué mejorarías en:
1. Pydantic models (validación)
2. Status codes HTTP
3. Response format
4. Async/await usage
5. Dependency injection
```

**Output esperado del agente**:
- ❌ Detecta: Falta Pydantic model, status code incorrecto (debería ser 201), sin validación
- ✅ Sugiere: Crear `TareaCreate` (request) y `TareaResponse` (response), usar `status.HTTP_201_CREATED`, añadir validación con `Field(...)`
- 📚 Explica: Por qué separar request/response models, cuándo usar async

**Acción**: Implementar el endpoint mejorado con Pydantic models completos.

---

### **Fase 3: Validación REST** (con API Design Reviewer)

**Objetivo**: Asegurar que toda la API sigue estándares REST e HTTP.

**Prompt para el agente**:
```markdown
Rol: API Design Reviewer
Contexto: He completado todos los endpoints de mi API de tareas.
Objetivo: Audita la API completa y valida diseño RESTful.

Endpoints implementados:
- POST /tareas - Crear tarea
- GET /tareas - Listar tareas
- GET /tareas/{id} - Obtener tarea
- PUT /tareas/{id} - Actualizar tarea
- DELETE /tareas/{id} - Eliminar tarea
- PUT /tareas/{id}/completar - Marcar como completada

¿Son RESTful? ¿Los status codes son correctos? ¿Las responses son consistentes?
```

**Output esperado del agente**:
- ✅ Valida: POST/GET/PUT/DELETE correctos
- ⚠️ Detecta: `/completar` no es RESTful (debería ser PATCH con body)
- ✅ Sugiere: Cambiar a `PATCH /tareas/{id}` con `{"completada": true}`
- 📚 Explica: Diferencia entre PUT (replace) y PATCH (partial update)

**Acción**: Refactorizar endpoints no-RESTful según estándares.

---

### **Fase 4: Testing Completo** (con Test Coverage Strategist)

**Objetivo**: Asegurar cobertura completa de tests (unit + integration).

**Prompt para el agente**:
```markdown
Rol: Test Coverage Strategist (Python Best Practices Coach)
Contexto: He implementado mi API de tareas con todos los endpoints.
Objetivo: Diseña una estrategia completa de testing.

Features implementadas:
- CRUD completo de tareas
- 2 repositorios (Memoria, JSON)
- Service layer con business logic
- Validación con Pydantic

¿Qué tests necesito? ¿Dónde están los gaps de coverage?
```

**Output esperado del agente**:
- ✅ Estrategia de testing:
  - **Unit tests**: Service layer (business logic aislada)
  - **Integration tests**: Repositories (persistencia real)
  - **API tests**: Endpoints (con TestClient)
- ✅ Detecta gaps:
  - Casos edge (títulos vacíos, IDs inexistentes)
  - Error handling (404, 422)
  - Validación de Pydantic
- 📚 Explica: Diferencia entre unit/integration/API tests

**Acción**: Implementar tests completos según la estrategia.

---

### **Fase 5: Validación Final de Arquitectura** (de nuevo Clean Architecture Enforcer)

**Objetivo**: Verificar que la implementación final sigue el diseño arquitectónico.

**Prompt para el agente**:
```markdown
Rol: Clean Architecture Enforcer
Contexto: He completado la implementación de mi API de tareas.
Objetivo: Audita el código completo y valida arquitectura limpia.

Estructura final:
- api/api.py (200 líneas)
- api/servicio_tareas.py (150 líneas)
- api/repositorio_base.py (Protocol)
- api/repositorio_memoria.py
- api/repositorio_json.py
- tests/ (unit tests)
- tests_integrations/ (integration tests)

¿La arquitectura se mantiene limpia? ¿Hay violaciones de SOLID?
```

**Output esperado del agente**:
- ✅ Valida: Capas separadas, dependency inversion correcta
- ⚠️ Detecta: Si hay business logic en API layer (moverla a Service)
- ✅ Confirma: Repository pattern bien implementado
- 📚 Explica: Qué hacer cuando la app crezca (módulos, DDD)

**Acción**: Refactorizar violaciones detectadas.

---

## 🧩 Guía de Orquestación: ¿Cuándo usar qué agente?

| **Situación** | **Agente a usar** | **Por qué** |
|---------------|-------------------|-------------|
| Diseñando la estructura del proyecto | Clean Architecture Enforcer | Valida diseño ANTES de codear |
| Implementando un nuevo endpoint | FastAPI Design Coach | Enseña patrones FastAPI profesionales |
| Completaste todos los endpoints | API Design Reviewer | Audita REST compliance y consistencia |
| Después de cada feature | Test Coverage Strategist | Asegura testing completo |
| Antes de hacer PR | Clean Architecture Enforcer + API Design Reviewer | Validación final doble |
| Encontraste bug en producción | Todos en orden inverso | Root cause analysis por capas |

---

## 🎓 Ejercicio Práctico: Desarrollo Guiado por Agentes

**Objetivo**: Implementar el endpoint `GET /tareas/{id}/historial` (listar cambios de una tarea) usando los 4 agentes.

### Paso 1: Diseño con Clean Architecture Enforcer
- Pregunta dónde va la lógica (¿service? ¿repository?)
- Valida que no rompes capas existentes

### Paso 2: Implementación con FastAPI Design Coach
- Crea el endpoint siguiendo sus sugerencias
- Define Pydantic models apropiados
- Usa status codes correctos

### Paso 3: Validación REST con API Design Reviewer
- ¿`/historial` es RESTful?
- ¿O debería ser `/tareas/{id}/audit-log`?
- ¿El formato de response es consistente?

### Paso 4: Testing con Test Coverage Strategist
- ¿Qué tests necesitas?
- ¿Unit? ¿Integration? ¿API?
- ¿Casos edge?

**Documenta en `notes.md`**:
- Qué agente usaste en cada paso
- Qué feedback te dio cada uno
- Qué cambió en tu implementación gracias a ellos

---

## 🔧 Prompt Estructurado para CI/CD (bonus)

Ahora que entiendes orquestación de agentes, aquí está el prompt profesional para generar CI/CD con IA:

```markdown
Rol: DevOps Python Specialist + CI/CD Expert
Contexto: Tengo un proyecto FastAPI con:
- Arquitectura en capas (API, Service, Repository)
- Tests en pytest (unit + integration)
- Coverage target: 80%
- Linting: Ruff
- Security: Bandit

Objetivo: Crea un pipeline de GitHub Actions que:
1. Ejecute tests con coverage (fail si <80%)
2. Corra Ruff linting
3. Ejecute Bandit security scan
4. No permita merge si falla alguno
5. Use Python 3.12
6. Optimice con caching de dependencias

Formato: YAML limpio y comentado, explicando cada step.

Restricciones:
- Debe correr en ubuntu-latest
- Timeout de 10 minutos max
- Artifacts de coverage report
```

Así obtienes una versión profesional con todos los checks de calidad.

**Pero ahora sabes qué hace cada parte** y puedes adaptarla, no solo copiarla a ciegas.

---

## 🧭 ¿Por qué esto importa?

Hasta hoy, **tú ejecutabas los tests**.

A partir de ahora, **los tests se ejecutan solos**. Siempre.

Eso es ingeniería de verdad. No confiar en la memoria, sino en procesos automáticos.

> Si alguien cambia RepositorioTareas y se carga el contrato, el PR no pasa.
> 
> 
> Si alguien olvida un test, la cobertura lo avisa.
> 
> Si alguien comete una burrada, la máquina lo frena.
> 

---

## 🛠️ Mini-ejercicio práctico

1. Crea la rama `feature/ci`.
2. Añade `.github/workflows/ci.yml`.
3. Haz push y abre PR.
4. Comprueba que GitHub lanza el workflow y los tests pasan.
5. Escribe en `notes.md`:
    - Qué hace el pipeline.
    - Qué protegerá en el futuro.
    - Qué te gustaría automatizar más adelante.

---

## ✅ Checklist de la clase

**Integración Continua (CI)**:
- [ ]  Entiendes qué es CI y para qué sirve.
- [ ]  Has creado un pipeline funcional con GitHub Actions.
- [ ]  Tu repo ahora lanza los tests automáticamente al hacer push o PR.

**Orquestación Multi-Agente** (40% AI integration):
- [ ]  Conoces los 4 agentes especializados para desarrollo de APIs.
- [ ]  Has aplicado el workflow de 5 fases (Diseño → Implementación → Validación REST → Testing → Validación Final).
- [ ]  Has usado al menos 2 agentes educacionales en tu desarrollo.
- [ ]  Entiendes cuándo usar cada agente según la situación.
- [ ]  Has documentado tu experiencia con agentes en `notes.md`.

**Documentación**:
- [ ]  Has documentado lo que aprendiste sobre CI/CD en `notes.md`.
- [ ]  Has documentado qué agentes usaste y qué feedback te dieron.
- [ ]  Has documentado cómo cambió tu código gracias al feedback de agentes.

---

## 🌱 Qué sigue

En el próximo módulo, entramos de lleno en **Calidad y Seguridad**:

- Vamos a añadir seguridad real (validación, JWT, .env…).
- Fortalecer la cobertura de tests.
- **Auditar con IA** (nuevos agentes especializados en seguridad).
- Preparar el despliegue real.

Porque una API que no se rompe es genial.

Pero una API que **no te hackean** y **se despliega sola**... eso ya es otro nivel.

---

## 🎯 Proyecto Final del Módulo 2: API Completa con Agentes

**Objetivo**: Desarrollar una API de tareas completa usando orquestación de agentes desde el diseño hasta el deployment.

### Requisitos Técnicos:
1. **Arquitectura limpia**: API → Service → Repository (validada por Clean Architecture Enforcer)
2. **Endpoints RESTful**: CRUD completo (validado por API Design Reviewer)
3. **Validación completa**: Pydantic models (revisado por FastAPI Design Coach)
4. **Tests completos**: 80%+ coverage (estrategia de Test Coverage Strategist)
5. **CI/CD**: Pipeline de GitHub Actions que ejecute tests, linting, coverage

### Requisitos de Agentes (40% AI integration):
- **Documenta en `AGENTS_WORKFLOW.md`**:
  - Qué agente usaste en cada fase
  - Qué prompt le enviaste
  - Qué feedback te dio
  - Cómo cambió tu código gracias a él
  - Tiempo ahorrado vs desarrollo manual

### Entregables:
1. **Código**: API completa en carpeta `proyecto-final/`
2. **Tests**: Unit + Integration + API tests (80%+ coverage)
3. **CI/CD**: `.github/workflows/ci.yml` funcional
4. **Documentación AI**: `AGENTS_WORKFLOW.md` completo
5. **Reflexión**: `notes.md` sobre tu experiencia con agentes

### Criterios de Evaluación:
- ✅ **Arquitectura** (25%): Clean Architecture Enforcer valida sin violaciones
- ✅ **API Design** (25%): API Design Reviewer confirma REST compliance
- ✅ **Calidad** (25%): Tests pasan, coverage >80%, linting OK
- ✅ **AI Integration** (25%): Workflow multi-agente documentado, 40%+ del desarrollo asistido por agentes

---

¿Listo para construir con tu ejército de agentes especializados?

Haz el PR de esta clase y pasamos al **Módulo 3: Calidad y Seguridad**.

## Posibles errores

En nuestro caso, como estamos dividiendo cada clase en carpetas diferentes, nuestro CI daba problemas. Asi que directamente hemos modificado nuestro CI para que haga los test por carpeta de forma independiente.

En nuestro caso, en la clase 1 solo esta hecho lo que explicamos en esa clase, para que podais ir viendo como va cambiando el archivo y los test a medida que avanzamos. Esto me provocaba un problema de carpetas.

Si en tu caso estas copiando el repo tal cual, pon el ci asi:

```sql
name: CI - Tests por clase

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      fail-fast: false
      matrix:
        class_dir:
          - "Modulo 2 – Ingeniería y Arquitectura/Clase 2 - Principios SOLID y paradigmas de programacion"
          - "Modulo 2 – Ingeniería y Arquitectura/Clase 3 - Arquitectura limpia"
          - "Modulo 2 – Ingeniería y Arquitectura/Clase 4 - Open_Closed y Dependency Inversion"
          - "Modulo 2 – Ingeniería y Arquitectura/Clase 5 - Integracion y pruebas de arquitectura"
          - "Modulo 2 – Ingeniería y Arquitectura/Clase 6 - Integracion continua y control de calidad"

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Pytest (tests)
        working-directory: ${{ matrix.class_dir }}
        run: |
          # Opcional: limpiar cachés por si vinieran del repo
          find . -type d -name "__pycache__" -exec rm -rf {} +
          find . -type f -name "*.pyc" -delete
          pytest -q

```

Si no es tu caso, deberian pasar los test como ya lo habiamos explicado.

Haz el PR de esta clase y pasamos al siguiente bloque.

