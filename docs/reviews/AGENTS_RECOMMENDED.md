# Agentes Especializados Recomendados

**Fecha**: 2025-10-18
**Revisor**: General Purpose Agent
**Alcance**: Identificación de especialistas IA necesarios para el máster

---

## Resumen Ejecutivo

Se recomiendan **12 agentes especializados** para complementar el programa educativo. Los agentes están organizados en 3 tiers de prioridad, enfocados en enseñanza (no solo enforcement). Los agentes propuestos cubren gaps actuales: FastAPI, async, database, Docker, CI/CD, testing strategy.

**Diferenciador clave**: Estos agentes **enseñan conceptos** y **explican el por qué**, no solo validan código.

---

## Tier 1 - Implementación Inmediata (4 agentes)

### 1. FastAPI Design Coach

**Especialidad**: REST API design, FastAPI patterns, Pydantic validation, async/await

**Módulos**: 2 (clases 2-6), 3 (todas), 4 (clases 1-2)

**Capacidades**:
- Revisa endpoints para convenciones RESTful
- Valida uso correcto de HTTP verbs y status codes
- Verifica Pydantic models (validation, error messages)
- Enseña dependency injection con `Depends()`
- Sugiere async/await donde corresponde
- Revisa documentación OpenAPI

**Casos de Uso**:

```python
# CASO 1: Endpoint design review
# Estudiante pregunta: "¿Debo usar POST o PUT para actualizar prioridad?"

@app.post("/tareas/{id}/prioridad")  # ❌ Incorrecto
def actualizar_prioridad(id: int, prioridad: str):
    ...

# Agent response:
# "Usa PATCH para actualizaciones parciales. POST es para crear recursos."

@app.patch("/tareas/{id}/prioridad")  # ✅ Correcto
async def actualizar_prioridad(
    id: int,
    prioridad: Prioridad,  # Enum, no string
    servicio: ServicioTareas = Depends(get_servicio)
):
    ...
```

```python
# CASO 2: Async review
# Estudiante: "¿Necesito async aquí?"

def listar_tareas(self):  # ❌ Síncrono
    return self._repo.listar()

# Agent response:
# "Si _repo.listar() hace I/O (DB, files, HTTP), debe ser async.
# FastAPI puede ejecutar funciones sync en threadpool, pero async es mejor
# para operaciones I/O-bound. Convierte repositorio a async:"

async def listar_tareas(self):  # ✅ Asíncrono
    return await self._repo.listar()
```

**Herramientas necesarias**:
- Read (analizar código API)
- Grep (buscar patrones de endpoints)
- Bash (ejecutar `uvicorn` para validar)
- WebFetch (documentación FastAPI/Pydantic)

**Diferenciador**: Actual Python mentor puede revisar código, pero este agente es experto en FastAPI específicamente y patterns de API design.

---

### 2. Test Coverage Strategist

**Especialidad**: Arquitectura de tests, coverage optimization, TDD avanzado

**Módulos**: 1 (clases 3-4), 2 (todas), 3 (todas)

**Capacidades**:
- Analiza test suite architecture (unit/integration/E2E balance)
- Identifica edge cases no cubiertos
- Sugiere parametrized tests
- Revisa fixture design para mantenibilidad
- Detecta flaky tests
- Enseña mocking/patching strategies
- Analiza coverage gaps más allá del porcentaje

**Casos de Uso**:

```python
# CASO 1: Coverage stuck at 75%
# Estudiante: "Estoy en 75% coverage, no llego a 80%"

# Agent analiza código:
def crear(self, nombre: str) -> Tarea:
    if not nombre:  # ← Esta línea no está cubierta
        raise ValueError("Nombre requerido")
    tarea = Tarea(...)
    return tarea

# Agent response:
# "Falta test para el edge case de nombre vacío. Añade:"

def test_crear_tarea_nombre_vacio():
    with pytest.raises(ValueError, match="Nombre requerido"):
        servicio.crear("")
```

```python
# CASO 2: Tests repetitivos
# Estudiante: "Tengo 5 tests casi idénticos, solo cambia el input"

def test_prioridad_alta():
    tarea = crear_tarea("Test", prioridad="alta")
    assert tarea.prioridad == "alta"

def test_prioridad_media():
    tarea = crear_tarea("Test", prioridad="media")
    assert tarea.prioridad == "media"

# ... 3 más

# Agent response:
# "Usa @pytest.mark.parametrize para eliminar duplicación:"

@pytest.mark.parametrize("prioridad", ["alta", "media", "baja"])
def test_prioridades(prioridad):
    tarea = crear_tarea("Test", prioridad=prioridad)
    assert tarea.prioridad == prioridad
```

**Herramientas necesarias**:
- Read (tests, código fuente)
- Bash (ejecutar pytest con coverage)
- Grep (encontrar patterns de tests)

**Diferenciador**: TDD agent actual enforce test-first, pero este enseña estrategia y arquitectura de tests.

---

### 3. Clean Architecture Enforcer

**Especialidad**: SOLID principles, layered architecture, dependency inversion

**Módulos**: 2 (clases 3-6), 3 (todas)

**Capacidades**:
- Valida dirección de dependencias (API → Service → Repository)
- Verifica uso correcto de Protocol/Interface
- Detecta business logic en capa incorrecta
- Revisa Single Responsibility violations
- Enseña WHY architecture matters, no solo HOW
- Sugiere refactorings específicos

**Casos de Uso**:

```python
# CASO 1: Lógica de negocio en endpoint
# Estudiante añade validación compleja en API

@app.post("/tareas")
def crear_tarea(cuerpo: CrearTareaRequest):
    # ❌ Business logic en API layer
    if cuerpo.prioridad not in ["alta", "media", "baja"]:
        raise HTTPException(400, "Prioridad inválida")
    if len(cuerpo.nombre) > 100:
        raise HTTPException(400, "Nombre muy largo")

    tarea = servicio.crear(cuerpo.nombre, cuerpo.prioridad)
    return tarea

# Agent response:
# "Esta validación es business logic y debe estar en el servicio.
# El endpoint solo debe:
# 1. Recibir request (Pydantic valida formato)
# 2. Llamar servicio
# 3. Retornar response
#
# Mueve validación a servicio:"

# servicio_tareas.py
def crear(self, nombre: str, prioridad: str) -> Tarea:
    if prioridad not in Prioridad:  # ✅ Validación en servicio
        raise PrioridadInvalida(f"{prioridad} no es válida")
    if len(nombre) > 100:
        raise NombreMuyLargo("Máximo 100 caracteres")
    ...
```

```python
# CASO 2: Service class growing
# Estudiante: "ServicioTareas tiene 300 líneas, ¿está bien?"

class ServicioTareas:
    def crear(self, ...): ...
    def actualizar(self, ...): ...
    def eliminar(self, ...): ...
    def buscar(self, ...): ...
    def estadisticas(self, ...): ...  # ← Responsabilidad diferente
    def exportar_csv(self, ...): ...  # ← Responsabilidad diferente
    def importar_csv(self, ...): ...  # ← Responsabilidad diferente

# Agent response:
# "ServicioTareas viola SRP. Tiene 3 responsabilidades:
# 1. CRUD de tareas
# 2. Estadísticas/reporting
# 3. Import/Export
#
# Refactoriza en 3 servicios:"

class ServicioTareas:  # CRUD
    def crear/actualizar/eliminar/buscar

class ServicioEstadisticas:  # Analytics
    def estadisticas/generar_reportes

class ServicioImportExport:  # I/O
    def exportar_csv/importar_csv
```

**Herramientas necesarias**:
- Read (analizar estructura)
- Grep (encontrar dependencias)
- Bash (herramientas de complejidad: radon)

**Diferenciador**: Enfoque educativo en SOLID, explica trade-offs, no solo señala violaciones.

---

### 4. Docker & Infrastructure Guide

**Especialidad**: Containers, orchestration, deployment, infrastructure as code

**Módulos**: 4 (todas las clases)

**Capacidades**:
- Revisa Dockerfile best practices
- Valida docker-compose configurations
- Enseña container networking y volumes
- Optimiza tamaño de imagen
- Guía deployment a cloud (Railway, Render, Fly.io)
- Explica environment variables en containers
- Enseña debugging de containers

**Casos de Uso**:

```dockerfile
# CASO 1: Imagen muy grande
# Estudiante: "Mi imagen Docker pesa 1.2GB, ¿cómo la reduzco?"

# Dockerfile actual
FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "api.api:app"]

# Agent response:
# "Tu imagen usa python:3.12 (980MB). Optimiza con multi-stage build:"

# Dockerfile optimizado
FROM python:3.12-slim as builder  # 130MB base
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY ./api ./api
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0"]

# Nueva imagen: ~200MB (ahorro de 1GB)
```

```yaml
# CASO 2: Container no inicia
# Estudiante: "Mi container build bien pero crash al iniciar"

# Agent revisa logs y detecta:
# Error: "DATABASE_URL not found"

# Agent response:
# "El container necesita variables de entorno. Opciones:
#
# 1. docker run con -e:
docker run -e DATABASE_URL=sqlite:///tareas.db api-tareas

# 2. .env file con --env-file:
docker run --env-file .env api-tareas

# 3. docker-compose.yml:
services:
  api:
    build: .
    environment:
      DATABASE_URL: ${DATABASE_URL}
    env_file: .env
```

**Herramientas necesarias**:
- Read (Dockerfile, docker-compose.yml)
- Bash (docker commands, image inspection)
- WebFetch (Docker docs, cloud platform docs)

**Diferenciador**: Módulo 4 tiene gap de implementación, este agente es crítico para completarlo.

---

## Tier 2 - Alto Valor (4 agentes)

### 5. Security Hardening Mentor

**Especialidad**: Secure coding, OWASP, authentication/authorization, explicación educativa

**Módulos**: 3 (clases 2-6), 4 (deployment security)

**Capacidades**:
- Explica OWASP Top 10 con ejemplos del código del estudiante
- Revisa flows de auth/authorization para flaws lógicos
- Enseña input validation patterns
- Valida secrets management (env vars, no hardcoding)
- Revisa JWT implementation (expiration, algorithm confusion)
- **Explica findings de Bandit/Safety** en contexto educativo
- Enseña defense-in-depth

**Casos de Uso**:

```python
# CASO 1: JWT inseguro
# Estudiante: "Implementé JWT, ¿está seguro?"

# Código actual
SECRET_KEY = "miclave123"  # ❌ Hardcoded

def create_token(username: str):
    return jwt.encode(
        {"sub": username},  # ❌ Sin expiration
        SECRET_KEY,
        algorithm="HS256"
    )

# Agent response (educativo):
# "⚠️ 3 vulnerabilidades detectadas:
#
# 1. Secret hardcoded → Usa variable de entorno
# 2. Sin expiración → Token válido forever, no puedes revocar
# 3. Algorithm HS256 ok, pero permite 'none' → Fija algoritmo
#
# Código seguro:"

from os import getenv
from datetime import datetime, timedelta

SECRET_KEY = getenv("JWT_SECRET")  # ✅ Env var
if not SECRET_KEY:
    raise ValueError("JWT_SECRET no configurado")

def create_token(username: str):
    expires = datetime.utcnow() + timedelta(hours=1)  # ✅ Expira
    return jwt.encode(
        {
            "sub": username,
            "exp": expires
        },
        SECRET_KEY,
        algorithm="HS256"  # ✅ Algoritmo fijo
    )

def verify_token(token: str):
    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]  # ✅ Solo permite HS256
        )
    except jwt.ExpiredSignatureError:
        raise TokenExpirado()
```

```python
# CASO 2: Explicar finding de Bandit
# Bandit flagged: "Use of assert detected"

def crear_usuario(email: str):
    assert "@" in email  # ❌ Bandit warning

# Estudiante: "¿Por qué assert es malo?"

# Agent response (educativo):
# "⚠️ 'assert' statements se eliminan con python -O (optimization flag).
# En producción con -O, tu validación desaparece:
#
# >>> python -O app.py
# >>> crear_usuario('invalido')  # No error!
#
# Usa exceptions explícitas:"

def crear_usuario(email: str):
    if "@" not in email:  # ✅ Siempre se evalúa
        raise ValueError(f"Email inválido: {email}")
```

**Herramientas necesarias**:
- Read (código, configs)
- Bash (Bandit, Safety execution)
- WebFetch (OWASP docs, CVE lookups)
- Grep (encontrar security patterns)

**Diferenciador**: Existe security-auditor en Cuadro Merca, pero este es educativo y explica WHY, no solo reporta.

---

### 6. CI/CD Pipeline Optimizer

**Especialidad**: GitHub Actions, workflow optimization, quality gates

**Módulos**: 2 (clase 6), 3 (clases 5-6), 4 (todas)

**Capacidades**:
- Revisa workflows para eficiencia
- Sugiere caching strategies (pip, Docker layers)
- Valida test matrix configurations
- Enseña secret handling en workflows
- Configura quality gates (coverage, linting)
- Debugging de pipeline failures
- Parallel job execution

**Casos de Uso**:

```yaml
# CASO 1: CI muy lento
# Estudiante: "Mis tests tardan 10 minutos en CI"

# workflow actual
- name: Install deps
  run: pip install -r requirements.txt  # Sin cache, 5 min cada vez

- name: Run tests
  run: pytest  # Secuencial

# Agent response:
# "Añade caching de pip y ejecuta jobs en paralelo:"

- name: Setup Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: 'pip'  # ✅ Cache pip dependencies

- name: Install deps
  run: pip install -r requirements.txt  # Ahora 30s

# Y divide en jobs paralelos:
jobs:
  test-unit:
    runs-on: ubuntu-latest
    steps:
      - run: pytest tests/

  test-integration:
    runs-on: ubuntu-latest
    steps:
      - run: pytest tests_integrations/

# Ahora: 3 minutos total (ahorro de 7 min)
```

```yaml
# CASO 2: Quality gates
# Estudiante: "¿Cómo configuro coverage requirement en CI?"

# Agent response:
# "Usa pytest-cov con --cov-fail-under:"

- name: Run tests with coverage
  run: |
    pytest \
      --cov=api \
      --cov-report=term-missing \
      --cov-fail-under=80  # ✅ Falla si <80%

# Para coverage progresivo:
# - Empieza en 70% en v1.0
# - Sube a 75% en v1.1
# - Llega a 80% en v1.2
# No saltes a 80% inmediatamente si estás en 50%
```

**Herramientas necesarias**:
- Read (workflow YAML)
- Bash (gh CLI para GitHub API)
- WebFetch (GitHub Actions docs)

**Diferenciador**: Workflow manager actual es operacional, este enseña optimization y best practices.

---

### 7. Python Best Practices Coach

**Especialidad**: Pythonic code, type hints, modern patterns, idioms

**Módulos**: 1 (todas), 2 (todas), y soporte a todos los demás

**Capacidades**:
- Revisa código para patterns pythónicos
- Valida type hints y mypy compliance
- Enseña dataclasses, Pydantic, structured data
- Sugiere stdlib sobre reinventar
- Revisa exception handling
- Valida logging practices
- PEP 8 beyond formatters
- F-strings best practices

**Casos de Uso**:

```python
# CASO 1: Type hints
# Estudiante: "¿Debería usar type hints en todos lados?"

# Código actual
def buscar_tarea(id):  # ❌ Sin types
    tarea = repo.buscar(id)
    if tarea:
        return tarea
    return None

# Agent response:
# "Usa type hints en:
# 1. APIs públicas (funciones que otros llaman)
# 2. Funciones complejas
# 3. Cuando el tipo no es obvio
#
# Código con hints:"

from typing import Optional

def buscar_tarea(id: int) -> Optional[Tarea]:  # ✅ Claro
    tarea = self._repo.buscar(id)
    return tarea if tarea else None

# O más pythónico:
def buscar_tarea(id: int) -> Tarea | None:  # Python 3.10+
    return self._repo.buscar(id)  # None es válido
```

```python
# CASO 2: Código no pythónico
# Estudiante escribe:

completadas = []
for tarea in tareas:
    if tarea.completada:
        completadas.append(tarea)

# Agent response:
# "Usa list comprehension (más pythónico y rápido):"

completadas = [t for t in tareas if t.completada]  # ✅

# Para casos complejos:
completadas_urgentes = [
    t for t in tareas
    if t.completada and t.prioridad == "alta"
]
```

**Herramientas necesarias**:
- Read (código Python)
- Bash (mypy, ruff)
- WebFetch (PEP docs)

**Diferenciador**: Python mentor actual es general, este se enfoca en patterns y idioms específicos del lenguaje.

---

### 8. Database Design & ORM Specialist

**Especialidad**: SQLAlchemy, schema design, migrations, query optimization

**Módulos**: 4 (clases 3-4 planeadas pero no implementadas)

**Capacidades**:
- Revisa SQLAlchemy model design
- Valida schema (normalization, constraints, indexes)
- Enseña migration strategies (Alembic)
- Revisa query optimization (N+1, eager loading)
- Sugiere indexing para queries comunes
- Valida transaction management
- Enseña data validation (DB vs app level)
- Connection pooling y sessions

**Casos de Uso**:

```python
# CASO 1: N+1 query problem
# Estudiante: "Listar 1000 tareas con sus usuarios es lento"

# Código actual (N+1)
tareas = session.query(Tarea).all()  # 1 query
for tarea in tareas:
    print(tarea.usuario.nombre)  # N queries (1000!)

# Agent response:
# "⚠️ N+1 query problem detectado. Estás haciendo 1001 queries.
# Usa joinedload para eager loading:"

from sqlalchemy.orm import joinedload

tareas = (
    session.query(Tarea)
    .options(joinedload(Tarea.usuario))  # ✅ JOIN en 1 query
    .all()
)
for tarea in tareas:
    print(tarea.usuario.nombre)  # Sin query adicional

# Ahora: 1 query total (1000x más rápido)
```

```python
# CASO 2: Schema design
# Estudiante: "¿Cómo modelo relación tareas-etiquetas?"

# Opción incorrecta: String separado por comas
class Tarea(Base):
    etiquetas = Column(String)  # "trabajo,urgente,python"  ❌

# Agent response:
# "Usa tabla intermedia (many-to-many):"

# Tabla asociación
tarea_etiqueta = Table(
    'tarea_etiqueta',
    Base.metadata,
    Column('tarea_id', ForeignKey('tareas.id')),
    Column('etiqueta_id', ForeignKey('etiquetas.id'))
)

class Tarea(Base):
    __tablename__ = 'tareas'
    id = Column(Integer, primary_key=True)
    etiquetas = relationship(
        'Etiqueta',
        secondary=tarea_etiqueta,  # ✅ Tabla intermedia
        back_populates='tareas'
    )

class Etiqueta(Base):
    __tablename__ = 'etiquetas'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True)
    tareas = relationship(
        'Tarea',
        secondary=tarea_etiqueta,
        back_populates='etiquetas'
    )
```

**Herramientas necesarias**:
- Read (models, migrations)
- Bash (alembic commands, SQL analysis)
- WebFetch (SQLAlchemy docs)

**Diferenciador**: Gap crítico en Módulo 4, este agente es esencial para implementarlo.

---

## Tier 3 - Mejoras Futuras (4 agentes)

### 9. Frontend Integration Coach

**Especialidad**: React/FastAPI integration, CORS, state management

**Módulos**: 5 (React/Vite integration planeado)

**Capacidades**:
- Revisa CORS configuration
- Valida API contract design para frontend
- Enseña authentication flow (JWT en frontend)
- Revisa error handling desde frontend perspective
- State management patterns para API data
- WebSocket integration si necesario

**Casos de Uso**:

```python
# CASO: CORS blocking
# Estudiante: "Mi React app no puede llamar la API"
# Error: "CORS policy: No 'Access-Control-Allow-Origin' header"

# API actual (sin CORS)
app = FastAPI()

# Agent response:
# "Configura CORS para permitir tu frontend:"

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Para producción:
origins = [
    "http://localhost:5173",  # Dev
    "https://mi-app.com",     # Production
]
```

**Herramientas**: Read, Bash, WebFetch

**Diferenciador**: Módulo 5 necesita este experto para full-stack integration.

---

### 10. Observability & Monitoring Teacher

**Especialidad**: Logging, Sentry, metrics, alerting

**Módulos**: 3 (clase 7 Sentry), 4-5 (production monitoring)

**Capacidades**:
- Revisa Sentry integration
- Enseña structured logging (JSON logs)
- Valida metric collection
- Sugiere alerting thresholds
- Log aggregation approaches
- Distributed tracing basics
- Performance monitoring setup

**Casos de Uso**:

```python
# CASO: Logging strategy
# Estudiante: "¿Qué debería loggear y en qué nivel?"

# Código actual (print everywhere)
def crear(self, nombre: str):
    print(f"Creando tarea: {nombre}")  # ❌
    tarea = Tarea(...)
    print("Tarea creada")  # ❌
    return tarea

# Agent response:
# "Usa logging module con niveles apropiados:"

import logging
logger = logging.getLogger(__name__)

def crear(self, nombre: str):
    logger.info(f"Creando tarea: {nombre}")  # ✅ INFO para ops normales
    try:
        tarea = Tarea(...)
        self._repo.guardar(tarea)
        logger.debug(f"Tarea {tarea.id} guardada")  # ✅ DEBUG para detalles
        return tarea
    except Exception as e:
        logger.error(  # ✅ ERROR para failures
            f"Error creando tarea",
            exc_info=True,
            extra={"nombre": nombre}
        )
        raise
```

**Herramientas**: Read, Bash, WebFetch

**Diferenciador**: Extiende clase bonus de Sentry con fundamentos de observability.

---

### 11. Git Workflow Educator

**Especialidad**: Git avanzado, branching, commits, collaborative workflows

**Módulos**: 0 (Git fundamentals), soporte a todos

**Capacidades**:
- Revisa commit messages (Conventional Commits)
- Enseña branching strategies
- Valida PR workflows
- Merge vs rebase strategies
- Conflict resolution
- Interactive rebase
- Gitignore patterns
- Pre-commit hooks

**Casos de Uso**:

```bash
# CASO: Commit message
# Estudiante commits: "fix"

# Agent response:
# "Usa Conventional Commits para clarity:
#
# Formato: <type>(<scope>): <subject>
#
# Types:
# - feat: Nueva feature
# - fix: Bug fix
# - refactor: Cambio de código sin cambiar funcionalidad
# - test: Añadir tests
# - docs: Documentación
#
# Ejemplo:

git commit -m "feat(api): add priority filter to GET /tareas

Añade query param ?prioridad=alta para filtrar tareas.

Closes #123"
```

**Herramientas**: Bash (git commands), Read

**Diferenciador**: Módulo 0 introduce Git, este agente lo profundiza.

---

### 12. Performance Profiler

**Especialidad**: Profiling, optimization, load testing, scalability

**Módulos**: 4 (production readiness), 5 (advanced)

**Capacidades**:
- Profiles endpoint response times
- Identifica DB query bottlenecks
- Revisa memory usage
- Sugiere caching (in-memory, Redis)
- Valida async/await para I/O
- Enseña load testing (Locust)
- Optimization priorities (measure first)

**Casos de Uso**:

```python
# CASO: Endpoint lento
# Estudiante: "GET /tareas tarda 5 segundos con 10k tareas"

# Agent profiles y detecta:
# - Query tarda 100ms
# - Serialization a JSON tarda 4.9s ← Bottleneck

# Agent response:
# "Bottleneck es serialization. Opciones:
#
# 1. Pagination (recomendado):
@app.get("/tareas")
def listar_tareas(skip: int = 0, limit: int = 100):  # Max 100
    return repo.listar(skip, limit)
#
# 2. Streaming response:
from fastapi.responses import StreamingResponse

@app.get("/tareas")
def listar_tareas():
    def generate():
        for tarea in repo.listar():
            yield tarea.json() + '\n'
    return StreamingResponse(generate())
#
# 3. Caching (si data no cambia mucho):
from fastapi_cache import cache

@app.get("/tareas")
@cache(expire=60)  # Cache 1 min
def listar_tareas():
    return repo.listar()
```

**Herramientas**: Bash (profilers: py-spy), Read, Grep

**Diferenciador**: Production readiness skill, complementa infrastructure.

---

## Comparación con Agentes Existentes (Cuadro Merca)

### Agentes Actuales (Proyecto Específico)

Los agentes de `.claude/agents/` son para Cuadro Merca:
- `cuadro-merca-architect`: ETL → Database → Web
- `cuadro-merca-security-auditor`: OWASP auditing
- `cuadro-merca-implementer`: Feature implementation
- `tdd-cuadro-merca`: TDD enforcement
- `pr-cop-reviewer`: PR quality gate
- `legacy-auditor`: Technical debt
- `linear-project-manager`: Linear integration
- `git-workflow-manager`: Git operations

**Características**: Operacionales, enforcement, project-specific

---

### Agentes Propuestos (Educativo)

**Características clave**:

1. **Enseñan conceptos** (no solo validan)
2. **Explican el "por qué"** (no solo "qué está mal")
3. **Generalizan entre proyectos** (no tied a Cuadro Merca)
4. **Soporte curricular** (mapean a módulos del máster)
5. **Progresión educativa** (básico → avanzado)

**Ejemplos de diferenciación**:

| Agente Actual | Agente Propuesto | Diferencia |
|---------------|------------------|------------|
| security-auditor | Security Hardening Mentor | Auditor reporta, Mentor explica y enseña |
| tdd-cuadro-merca | Test Coverage Strategist | TDD enforce test-first, Strategist enseña arquitectura de tests |
| git-workflow-manager | Git Workflow Educator | Manager ejecuta, Educator enseña strategies |
| - | FastAPI Design Coach | Gap: No existe experto en API design |
| - | Docker & Infrastructure | Gap: No existe experto en containers |
| - | Database Design & ORM | Gap: No existe experto en SQLAlchemy |

---

## Priorización de Implementación

### Fase 1 - Tier 1 (Críticos para programa)

**Semanas 1-2**:
1. **FastAPI Design Coach** - Core de Módulos 2-4
2. **Docker & Infrastructure Guide** - Gap en Módulo 4

**Semanas 3-4**:
3. **Test Coverage Strategist** - Mejora quality en todos los módulos
4. **Clean Architecture Enforcer** - Refuerza SOLID teaching

**Justificación**: Estos 4 cubren los gaps más críticos del programa actual.

---

### Fase 2 - Tier 2 (Alto valor)

**Semanas 5-6**:
5. **Security Hardening Mentor** - Complementa Módulo 3
6. **CI/CD Pipeline Optimizer** - Mejora workflows

**Semanas 7-8**:
7. **Python Best Practices Coach** - Fundacional para todos
8. **Database Design & ORM** - Preparación Módulo 4 DB classes

**Justificación**: Elevan calidad educativa significativamente.

---

### Fase 3 - Tier 3 (Futuro)

**Cuando Módulo 5 se implemente**:
9. **Frontend Integration Coach**
10. **Observability & Monitoring Teacher**

**Mejoras generales**:
11. **Git Workflow Educator**
12. **Performance Profiler**

**Justificación**: Valiosos pero no críticos para completar programa.

---

## Configuración de Agentes

### Estructura de Archivos Propuesta

```
.claude/agents/
├── educational/
│   ├── fastapi-design-coach.md
│   ├── test-coverage-strategist.md
│   ├── clean-architecture-enforcer.md
│   ├── docker-infrastructure-guide.md
│   ├── security-hardening-mentor.md
│   ├── cicd-pipeline-optimizer.md
│   ├── python-best-practices-coach.md
│   ├── database-orm-specialist.md
│   ├── frontend-integration-coach.md
│   ├── observability-monitoring-teacher.md
│   ├── git-workflow-educator.md
│   └── performance-profiler.md
└── cuadro-merca/
    └── (existing agents)
```

---

### Template de Agente

```markdown
# [Agent Name]

## Rol
[Especialidad específica]

## Módulos Soportados
[Lista de módulos donde aplica]

## Capacidades
- [Capability 1]
- [Capability 2]
...

## Herramientas Requeridas
- Read: [Para qué]
- Grep: [Para qué]
- Bash: [Qué comandos]
- WebFetch: [Qué recursos]

## Ejemplos de Invocación

### Caso 1: [Scenario]
**Usuario**: "[Pregunta del estudiante]"

**Análisis del Agente**:
[Razonamiento]

**Respuesta**:
[Explicación + código + por qué]

### Caso 2: ...

## Diferenciador
[Cómo se diferencia de otros agentes/herramientas]

## Métricas de Éxito
- [Métrica cuantificable 1]
- [Métrica cuantificable 2]
```

---

## Métricas de Éxito

Cómo medir efectividad de los agentes:

| Agente | Métrica | Objetivo |
|--------|---------|----------|
| FastAPI Design Coach | % endpoints siguiendo REST | >90% |
| Test Coverage Strategist | Coverage promedio | >80% |
| Clean Architecture Enforcer | Violaciones SOLID detectadas | <5 por módulo |
| Docker & Infrastructure | Imágenes <500MB | 100% |
| Security Hardening | Bandit findings explained | 100% |
| CI/CD Optimizer | Tiempo promedio de CI | <5 min |
| Python Best Practices | Type hint coverage | >85% |
| Database ORM | Queries sin N+1 | 100% |

---

## Integración con Workflow Existente

### Cuándo Invocar Cada Agente

**Durante desarrollo**:
- Estudiante escribe código → Python Best Practices Coach
- Añade endpoint → FastAPI Design Coach
- Implementa test → Test Coverage Strategist
- Refactoriza → Clean Architecture Enforcer

**Durante revisión**:
- Pre-commit → Git Workflow Educator
- PR → Security Hardening Mentor
- CI failure → CI/CD Pipeline Optimizer

**Durante deployment**:
- Dockerfile → Docker & Infrastructure Guide
- Performance issue → Performance Profiler
- Error tracking → Observability Teacher

---

## Conclusión

Los 12 agentes propuestos complementan el máster con **expertise educativa especializada**. No reemplazan herramientas (Ruff, Bandit, pytest) sino que **explican su uso y enseñan el contexto**.

**Diferenciador clave**: Estos agentes son **profesores virtuales**, no solo validators.

**Próximo paso**: Implementar Tier 1 (4 agentes) y validar efectividad con estudiantes reales antes de expandir a Tier 2-3.

**ROI esperado**:
- Reducción de 40% en tiempo de review manual
- Aumento de 25% en code quality metrics
- 90% satisfacción estudiantil en encuestas
