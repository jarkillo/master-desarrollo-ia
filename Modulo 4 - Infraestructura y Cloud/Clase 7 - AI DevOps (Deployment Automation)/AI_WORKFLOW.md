# AI_WORKFLOW: AI DevOps - Deployment Automation

## Objetivo de Integración de IA

Aprender a usar **IA como copiloto de DevOps** en cada etapa del ciclo de deployment:
- Generar workflows de CI/CD
- Optimizar configuraciones de infraestructura
- Debuggear pipelines fallidos
- Monitorear y detectar anomalías
- Automatizar respuesta a incidentes

**Meta**: Al final de esta clase, la IA será tu **DevOps expert on-demand**.

---

## Agente Educativo Recomendado

**Agente principal**: `docker-infrastructure-guide.md`

**Por qué este agente:**
- Experto en Dockerfiles, docker-compose, CI/CD
- Conoce mejores prácticas de deployment
- Puede revisar configuraciones de infraestructura
- Enseña optimización de builds y seguridad

**Cómo usarlo:**

```bash
# Revisar Dockerfile con el agente
claude --agent docker-infrastructure-guide \
  "Revisa este Dockerfile y sugiere optimizaciones para CI/CD: [pegar contenido]"

# Generar docker-compose.yml
claude --agent docker-infrastructure-guide \
  "Genera docker-compose para FastAPI + PostgreSQL + Redis con health checks"
```

**Agente secundario**: `python-best-practices-coach.md`
- Para scripts de deployment en Python
- Validar código de automation scripts
- Revisar configuraciones de herramientas (pytest, ruff, etc.)

---

## Fase 1: Generación de Workflows (40% AI)

### 1.1 Generar GitHub Actions Workflow Básico

**Prompt efectivo:**

```
Genera un GitHub Actions workflow para una API FastAPI con estos requisitos:

CONTEXTO:
- Python 3.12 con FastAPI
- Tests con pytest (coverage mínimo 80%)
- Linting con ruff
- Dependencias en requirements.txt

WORKFLOW:
- Trigger: push a main y pull requests
- Jobs: lint → test → deploy (solo en main)
- Deploy a Railway usando RAILWAY_TOKEN (secret)

MEJORES PRÁCTICAS:
- Usar cache de pip para acelerar builds
- Separar jobs para paralelizar
- Solo deploy si tests pasan
- Usar últimas versiones de actions (@v4, @v5)

Output: Archivo .github/workflows/ci-cd.yml completo
```

**Resultado esperado:**

IA genera workflow funcional con:
- Setup de Python con cache
- Jobs separados (independientes)
- Dependencias entre jobs (`needs: test`)
- Condicionales (`if: github.ref == 'refs/heads/main'`)
- Secrets management seguro

**Validación:**

```bash
# Verificar sintaxis YAML
yamllint .github/workflows/ci-cd.yml

# Dry-run local con act
act -n
```

---

### 1.2 Optimizar Dockerfile para CI/CD

**Prompt efectivo:**

```
Optimiza este Dockerfile para uso en CI/CD:

DOCKERFILE ACTUAL:
[pegar Dockerfile]

OBJETIVOS:
- Builds rápidos (usar layer caching efectivo)
- Imagen pequeña (<100MB si es posible)
- Multi-stage build
- Security: non-root user
- Health check incluido

CONTEXTO:
- Se construye en cada push (frecuentes builds)
- Se despliega en Railway
- API FastAPI con uvicorn

Output: Dockerfile optimizado con comentarios explicativos
```

**Resultado esperado:**

IA genera Dockerfile con:
- Multi-stage build (builder + production)
- Cache de `pip install` en capa separada
- `python:3.12-slim` para imagen pequeña
- User `appuser` (non-root)
- HEALTHCHECK configurado
- Comentarios educativos en cada sección

**Ejemplo de output:**

```dockerfile
# Stage 1: Instalar dependencias (cached si requirements.txt no cambia)
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Imagen de producción (solo lo necesario)
FROM python:3.12-slim
RUN useradd -m -u 1000 appuser
WORKDIR /app
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .
ENV PATH=/home/appuser/.local/bin:$PATH
USER appuser
HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0"]
```

---

### 1.3 Generar docker-compose para Testing Local

**Prompt efectivo:**

```
Genera docker-compose.yml para desarrollo local:

SERVICIOS:
1. api: FastAPI (Dockerfile en ./Dockerfile)
2. db: PostgreSQL 15
3. redis: Redis 7 (para caching)

REQUISITOS:
- Health checks en todos los servicios
- Volúmenes persistentes para DB
- Hot reload para API (bind mount código)
- Variables de entorno en .env
- Redes aisladas

PUERTOS:
- API: 8000
- DB: 5432
- Redis: 6379

Output: docker-compose.yml production-ready con comentarios
```

**Resultado esperado:**

IA genera compose file con:
- Definición de servicios con `depends_on` + conditions
- Health checks (`interval`, `timeout`, `retries`)
- Volúmenes nombrados (`postgres_data`)
- Bind mounts para hot reload
- Variables de entorno con defaults
- Network definida explícitamente

---

## Fase 2: Debugging de Pipelines (30% AI)

### 2.1 Diagnosticar Errores de CI

**Escenario común**: GitHub Actions falla con error críptico.

**Prompt de debugging:**

```
Mi GitHub Actions workflow está fallando. Ayuda a diagnosticar:

ERROR:
[pegar error message del workflow]

LOGS COMPLETOS:
[pegar logs del step que falla]

ARCHIVO workflow.yml:
[pegar workflow completo]

CONTEXTO ADICIONAL:
- Funcionaba ayer, empezó a fallar hoy
- No cambié el workflow, solo código Python
- Falla en el step "Run tests"

PREGUNTA:
1. ¿Cuál es la causa raíz?
2. ¿Cómo lo soluciono?
3. ¿Cómo prevengo esto en el futuro?
```

**Resultado esperado:**

IA analiza y provee:
1. **Root cause**: "pytest no encuentra módulos porque falta PYTHONPATH"
2. **Fix inmediato**: Añadir `pip install -e .` o `PYTHONPATH: .`
3. **Prevención**: Usar `setup.py` o configurar `pytest.ini`

**Validación:**

```bash
# Reproducir error localmente
docker run --rm -v $(pwd):/app python:3.12 /bin/bash -c "cd /app && pytest"

# Verificar que fix funciona
# ... (aplicar sugerencia de IA)
```

---

### 2.2 Depurar Builds de Docker Lentos

**Prompt de optimización:**

```
Mis builds de Docker en CI tardan 8 minutos. Necesito optimizar:

DOCKERFILE:
[pegar Dockerfile]

ESTADÍSTICAS:
- Build time: 8m 14s
- Image size: 450MB
- Step más lento: "RUN pip install -r requirements.txt" (6 minutos)

OBJETIVO:
- Build time < 2 minutos en CI (con cache)
- Image size < 150MB

¿Qué optimizaciones aplico?
```

**Resultado esperado:**

IA identifica problemas y sugiere fixes:

**Problemas detectados:**
1. No usa multi-stage build → imagen incluye compiladores
2. `requirements.txt` cambia frecuentemente → no aprovecha cache
3. Instala `gcc`, `build-essential` pero no los borra
4. Copia todo el código antes de `pip install` → invalida cache

**Soluciones:**
1. Multi-stage build (builder + production)
2. Copiar `requirements.txt` primero, luego código
3. Usar `--no-cache-dir` en pip
4. Base image slim en vez de completa

**Resultado**: Build time 8min → 1.5min, image 450MB → 120MB

---

## Fase 3: Monitoring y Detección de Anomalías (20% AI)

### 3.1 Analizar Métricas con IA

**Caso de uso**: Detectar si métricas son normales o indican problema.

**Prompt de análisis:**

```
Analiza estas métricas de mi API en producción:

PERÍODO: Últimos 30 minutos (11:30 - 12:00)

MÉTRICAS:
- Requests/seg: 720 (pico: 950)
- Error rate: 2.3%
- Response time p50: 85ms
- Response time p95: 420ms
- Response time p99: 1200ms
- CPU usage: 78%
- Memory usage: 82%

BASELINE HISTÓRICO (últimos 7 días):
- Requests/seg promedio: 250-350
- Error rate promedio: 0.2-0.5%
- Response time p95: 80-150ms
- CPU usage: 35-45%

PREGUNTA:
1. ¿Hay anomalías?
2. ¿Qué severidad? (low/medium/high/critical)
3. ¿Requiere acción inmediata?
4. ¿Posible causa?
```

**Resultado esperado:**

IA analiza y responde:

```json
{
  "anomaly_detected": true,
  "severity": "high",
  "anomalies": [
    {
      "metric": "requests_per_second",
      "value": 720,
      "baseline": "250-350",
      "deviation": "+106%",
      "description": "Tráfico 2x mayor que lo normal"
    },
    {
      "metric": "error_rate",
      "value": "2.3%",
      "baseline": "0.2-0.5%",
      "deviation": "+360%",
      "description": "Error rate 4x mayor que baseline"
    },
    {
      "metric": "response_time_p95",
      "value": "420ms",
      "baseline": "80-150ms",
      "deviation": "+180%",
      "description": "Latencia significativamente alta"
    }
  ],
  "probable_cause": "Spike de tráfico (posible ataque DDoS o viral post) causando sobrecarga del servidor y timeout de requests",
  "immediate_action_required": true,
  "recommended_actions": [
    "1. Verificar logs de errores para confirmar tipo de error (timeout vs 500)",
    "2. Revisar fuente de tráfico (país, IPs) para descartar ataque",
    "3. Escalar horizontalmente (añadir instancias) si tráfico legítimo",
    "4. Activar rate limiting si se confirma abuso"
  ]
}
```

---

### 3.2 Root Cause Analysis de Incidentes

**Escenario**: API caída, error rate 95%, necesitas diagnóstico rápido.

**Prompt de RCA:**

```
INCIDENTE EN PRODUCCIÓN:

SÍNTOMAS:
- Error rate: 95% (normal: <1%)
- Todos los errores: "500 Internal Server Error"
- Comenzó: 2024-11-01 14:32 UTC
- Duración: 12 minutos (ongoing)

LOGS (últimos 100 errores):
[pegar logs]

MÉTRICAS EN MOMENTO DEL INCIDENTE:
- CPU: 15% (bajo, no es sobrecarga)
- Memory: 45% (normal)
- Database connections: 95/100 (casi agotado! 🔴)
- Response time: >10 segundos (timeouts)

CAMBIOS RECIENTES:
- Deploy v2.1.3 hace 15 minutos
- Cambios: Añadido endpoint GET /users con query de todos los usuarios

PREGUNTA:
1. ¿Cuál es la root cause?
2. ¿Cómo mitigo AHORA (fix inmediato)?
3. ¿Cómo lo arreglo permanentemente?
```

**Resultado esperado:**

IA diagnostica:

```markdown
## Root Cause Analysis

### Root Cause
**N+1 Query Problem en el nuevo endpoint GET /users**

El endpoint `/users` está cargando todos los usuarios (posiblemente miles),
y para cada usuario hace una query adicional para cargar relaciones (posts, comments, etc.).

Esto resulta en:
- 1 query inicial: SELECT * FROM users
- N queries adicionales: SELECT * FROM posts WHERE user_id = ? (para cada user)

Si hay 1000 usuarios → 1001 queries → agota connection pool → timeouts.

### Evidencia
1. Database connections al 95% (casi agotado)
2. Incidente comenzó exactamente después de deploy con nuevo endpoint /users
3. Response times >10s indican queries lentas/múltiples
4. CPU/Memory normales → descarta sobrecarga, apunta a DB bottleneck

### Mitigación Inmediata (5 minutos)
1. **Rollback a v2.1.2**:
   ```bash
   git checkout v2.1.2
   railway up
   ```

2. **O rate-limit el endpoint** (si no puedes hacer rollback):
   ```python
   # En api.py
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)

   @app.get("/users")
   @limiter.limit("5/minute")  # Máximo 5 requests por minuto
   async def get_users():
       ...
   ```

### Fix Permanente (v2.1.4)
1. **Añadir eager loading** (cargar relaciones en 1 query):
   ```python
   # En vez de:
   users = db.query(User).all()  # N+1 problem

   # Usar:
   from sqlalchemy.orm import joinedload

   users = db.query(User).options(
       joinedload(User.posts),
       joinedload(User.comments)
   ).all()  # Single query con JOINs
   ```

2. **Añadir paginación**:
   ```python
   @app.get("/users")
   async def get_users(skip: int = 0, limit: int = 20):
       users = db.query(User).offset(skip).limit(limit).all()
       return users
   ```

3. **Añadir caching** (Redis):
   ```python
   @cache(expire=300)  # Cache 5 minutos
   async def get_users():
       ...
   ```

### Prevención Futura
1. Añadir test de performance para endpoints que retornan listas
2. Configurar query logging en desarrollo para detectar N+1
3. Añadir alertas cuando connection pool > 80%
4. Code review checklist: "¿Este endpoint puede causar N+1?"
```

**Valor**: Lo que tomaría 1 hora de investigación → 2 minutos con IA.

---

## Fase 4: Automatización con IA (10% AI)

### 4.1 Generar Scripts de Deployment

**Prompt para rollback script:**

```
Genera un script de rollback para mi API en Railway:

REQUISITOS:
1. Detectar última versión estable (git tag con formato v*.*.*)
2. Hacer checkout a esa versión
3. Deploy a Railway usando railway CLI
4. Verificar que deploy funcionó (health check)
5. Notificar resultado a Slack

CONTEXTO:
- Repositorio usa semantic versioning (v1.0.0, v1.1.0, etc.)
- Health check endpoint: /health (retorna 200 si OK)
- URL producción: https://mi-api.railway.app
- Slack webhook en variable SLACK_WEBHOOK

Output: Script bash production-ready con manejo de errores
```

**Resultado esperado:**

IA genera `rollback.sh`:

```bash
#!/bin/bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures

echo "🔄 Starting rollback process..."

# 1. Find last stable tag (excluding current)
CURRENT_TAG=$(git describe --tags --abbrev=0)
LAST_STABLE=$(git tag -l "v*.*.*" | sort -V | grep -v "$CURRENT_TAG" | tail -n 1)

if [ -z "$LAST_STABLE" ]; then
  echo "❌ Error: No previous stable version found"
  exit 1
fi

echo "📌 Current version: $CURRENT_TAG"
echo "📌 Rolling back to: $LAST_STABLE"

# 2. Checkout last stable version
git checkout "$LAST_STABLE"

# 3. Deploy to Railway
echo "🚀 Deploying to Railway..."
railway up --detach

# 4. Wait for deployment to complete
echo "⏳ Waiting 30s for deployment..."
sleep 30

# 5. Health check
HEALTH_URL="https://mi-api.railway.app/health"
MAX_RETRIES=5
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
  echo "🏥 Health check attempt $((RETRY_COUNT + 1))/$MAX_RETRIES..."

  if curl -f -s "$HEALTH_URL" > /dev/null 2>&1; then
    echo "✅ Rollback successful! Running $LAST_STABLE"

    # Notify Slack
    curl -X POST "$SLACK_WEBHOOK" \
      -H 'Content-Type: application/json' \
      -d "{
        \"text\": \"✅ Rollback successful\",
        \"blocks\": [{
          \"type\": \"section\",
          \"text\": {
            \"type\": \"mrkdwn\",
            \"text\": \"*Rollback Completed*\n• From: \`$CURRENT_TAG\`\n• To: \`$LAST_STABLE\`\n• Status: ✅ Healthy\"
          }
        }]
      }"

    exit 0
  fi

  RETRY_COUNT=$((RETRY_COUNT + 1))
  sleep 10
done

# Health check failed
echo "❌ Rollback failed! Health check not passing after $MAX_RETRIES attempts"

curl -X POST "$SLACK_WEBHOOK" \
  -H 'Content-Type: application/json' \
  -d "{
    \"text\": \"❌ Rollback failed\",
    \"blocks\": [{
      \"type\": \"section\",
      \"text\": {
        \"type\": \"mrkdwn\",
        \"text\": \"*Rollback Failed*\n• Target version: \`$LAST_STABLE\`\n• Health check: ❌ Not responding\n• Action: Manual intervention required\"
      }
    }]
  }"

exit 1
```

**Incluye:**
- Error handling (`set -euo pipefail`)
- Retries con timeout
- Notificaciones ricas a Slack (con Markdown)
- Logging claro de cada step
- Exit codes apropiados (0 = success, 1 = error)

---

## Fase 5: Integración Continua del Conocimiento

### 5.1 Documentación Auto-Generada

**Prompt para CHANGELOG:**

```
Genera CHANGELOG.md para el próximo release basado en commits recientes:

COMMITS (últimos 30 días):
[pegar output de: git log --oneline --since="30 days ago"]

FORMATO:
- Sigue https://keepachangelog.com/
- Agrupa por: Added, Changed, Fixed, Security
- Escribe en español, bullets concisos
- Incluye enlaces a issues si los hay (formato: #123)

VERSIÓN ACTUAL: v2.0.3
TIPO DE RELEASE: [determínalo tú según commits - MAJOR/MINOR/PATCH]

Output: Sección para añadir a CHANGELOG.md
```

**Resultado esperado:**

IA analiza commits, detecta tipo de release (MINOR porque hay features nuevas), y genera:

```markdown
## [2.1.0] - 2024-11-01

### Added
- Endpoint `GET /users` con paginación y filtros (#156)
- Cache de Redis para queries frecuentes (#159)
- Health check detallado en `/health` (#162)

### Changed
- Mejorado performance de `GET /tasks` con eager loading (#158)
- Actualizado FastAPI de 0.104 a 0.118 (#160)

### Fixed
- Corregido N+1 query en endpoint de usuarios (#157)
- Solucionado memory leak en background tasks (#161)

### Security
- Añadido rate limiting a endpoints públicos (#163)
- Actualizado dependencias con vulnerabilidades (bandit scan) (#164)
```

---

### 5.2 Code Review Automatizado Pre-Deploy

**Prompt para PR review:**

```
Revisa este Pull Request antes de merge a main:

TÍTULO PR: "feat: Add user search endpoint"

ARCHIVOS CAMBIADOS:
[pegar git diff]

CONTEXTO:
- Este código se desplegará automáticamente a producción si se mergea
- Debe pasar: tests, linting, security scan
- Es un endpoint público (sin autenticación)

REVISAR:
1. ¿Hay vulnerabilidades de seguridad?
2. ¿Performance concerns? (N+1 queries, missing indexes)
3. ¿Tests adecuados?
4. ¿Falta manejo de errores?
5. ¿Cambios breaking (incompatibles con clientes)?

Output: Code review estructurado (aprobar/rechazar + comentarios)
```

**Resultado esperado:**

IA hace review profundo:

```markdown
## Code Review: feat: Add user search endpoint

### ⚠️ SOLICITAR CAMBIOS

### Critical Issues

1. **🔴 Security: SQL Injection Risk**
   - **Ubicación**: `api/api.py:45`
   - **Problema**:
     ```python
     query = f"SELECT * FROM users WHERE name LIKE '%{search_term}%'"
     ```
   - **Por qué es peligroso**: Usuario puede inyectar SQL en `search_term`
   - **Fix**:
     ```python
     # Usar prepared statements
     query = db.query(User).filter(User.name.ilike(f"%{search_term}%"))
     ```

2. **🟡 Performance: Missing Index**
   - **Ubicación**: Query en `name` sin índice
   - **Impacto**: Búsquedas lentas con >1000 usuarios (full table scan)
   - **Fix**: Añadir migración de Alembic:
     ```python
     op.create_index('idx_users_name', 'users', ['name'])
     ```

3. **🟡 Missing Rate Limiting**
   - **Problema**: Endpoint público sin rate limit
   - **Riesgo**: Abuso (DoS por búsquedas masivas)
   - **Fix**:
     ```python
     @limiter.limit("30/minute")
     @app.get("/search")
     ```

### Minor Issues

4. **Missing Input Validation**
   - `search_term` acepta cualquier string (hasta 10KB)
   - **Fix**: Validar con Pydantic:
     ```python
     class SearchQuery(BaseModel):
         q: str = Field(..., min_length=1, max_length=50)
     ```

5. **Tests Incompletos**
   - Falta test para edge case: `search_term=""` (string vacío)
   - Falta test de SQL injection (`search_term="'; DROP TABLE users; --"`)

### Positives ✅

- ✅ Endpoint documentado con OpenAPI
- ✅ Manejo de errores 404 si no hay resultados
- ✅ Tests básicos presentes

### Recommendation

**❌ NO APROBAR** hasta que se corrija issue #1 (SQL Injection).

Issues #2-#5 son importantes pero no blockers. Pueden ser issues de follow-up si el equipo acepta tech debt temporalmente.

### Suggested Changes

```python
# api/api.py
from pydantic import BaseModel, Field
from slowapi import Limiter

class SearchQuery(BaseModel):
    q: str = Field(..., min_length=1, max_length=50, description="Search term")

@app.get("/search")
@limiter.limit("30/minute")
async def search_users(query: SearchQuery, db: Session = Depends(get_db)):
    # Usar ORM (previene SQL injection)
    results = db.query(User).filter(
        User.name.ilike(f"%{query.q}%")
    ).limit(100).all()

    if not results:
        raise HTTPException(status_code=404, detail="No users found")

    return {"results": results, "count": len(results)}
```
```

**Valor**: Detecta vulnerabilidades críticas antes de production.

---

## Mejores Prácticas de Prompting para DevOps

### Anatomía de un Prompt Efectivo

```
[CONTEXTO] Stack tecnológico, plataforma, restricciones
[OBJETIVO] Qué necesitas lograr
[REQUISITOS] Must-haves vs nice-to-haves
[OUTPUT ESPERADO] Formato específico (script, YAML, JSON, etc.)
[VALIDACIÓN] Cómo verificar que funciona
```

### Ejemplos de Prompts por Caso de Uso

**1. Generar Workflow:**
```
Contexto: FastAPI + PostgreSQL en Railway
Objetivo: CI/CD que ejecute tests y despliegue automáticamente
Requisitos: Coverage 80%+, deploy solo si tests pasan, notificar a Slack
Output: .github/workflows/deploy.yml
Validación: workflow debe pasar en GitHub Actions
```

**2. Debugging:**
```
Contexto: [logs del error]
Objetivo: Entender causa raíz y cómo solucionarlo
Requisitos: Fix que funcione sin cambiar arquitectura
Output: Explicación + código del fix
Validación: [cómo reproduzco el error y verifico el fix]
```

**3. Optimización:**
```
Contexto: Dockerfile actual tarda 8 minutos en build
Objetivo: Reducir a <2 minutos manteniendo misma funcionalidad
Requisitos: Mantener compatibilidad con Railway, imagen <150MB
Output: Dockerfile optimizado con comentarios explicativos
Validación: docker build debe tardar <2min, image size <150MB
```

---

## Checklist de Integración de IA

Usa esta checklist para asegurar que estás aprovechando IA al máximo en esta clase:

### Generación de Código
- [ ] Usé IA para generar workflow de GitHub Actions
- [ ] Usé IA para optimizar Dockerfile
- [ ] Usé IA para generar docker-compose.yml
- [ ] Usé IA para generar scripts de deployment/rollback

### Debugging
- [ ] Usé IA para diagnosticar errores de CI
- [ ] Pedí a IA explicación de errores crípticos
- [ ] Usé IA para optimizar builds lentos

### Monitoring
- [ ] Usé IA para analizar métricas y detectar anomalías
- [ ] Usé IA para Root Cause Analysis de incidentes
- [ ] Implementé alertas inteligentes con IA

### Documentación
- [ ] Usé IA para generar CHANGELOG
- [ ] Usé IA para documentar workflows
- [ ] Usé IA para code review automatizado

### Validación
- [ ] Todos los workflows generados funcionan en GitHub Actions
- [ ] Dockerfile optimizado es más rápido y pequeño que el original
- [ ] Scripts de deployment fueron probados en staging
- [ ] IA detectó al menos 1 problema que no había visto

**Meta**: Al menos 10/14 checkmarks ✅

---

## Recursos para Profundizar

### Herramientas de IA para DevOps

1. **GitHub Copilot CLI**
   - Genera comandos de terminal con lenguaje natural
   - `gh copilot suggest "deploy to railway with health check"`

2. **Claude Code (este entorno)**
   - Agente `docker-infrastructure-guide` para revisar configs
   - Ideal para generar workflows completos

3. **ChatGPT Code Interpreter**
   - Analiza logs grandes (sube archivo de 10MB de logs)
   - Genera gráficos de métricas

### Prompts Reutilizables

Crea tu librería personal de prompts:

```bash
# ~/.devops-prompts/
├── generate-workflow.txt
├── optimize-dockerfile.txt
├── debug-ci.txt
├── analyze-metrics.txt
└── generate-changelog.txt
```

**Ejemplo de template** (`generate-workflow.txt`):
```
Genera un GitHub Actions workflow que:

TRIGGER: [push a main / PRs / schedule]
JOBS:
1. [job name]: [descripción]
2. [job name]: [descripción]

STACK:
- Language: [Python/Node/etc]
- Framework: [FastAPI/Express/etc]
- Tests: [pytest/jest/etc]
- Deploy: [Railway/Fly/AWS]

REQUIREMENTS:
- [requirement 1]
- [requirement 2]

Output: .github/workflows/[name].yml completo y funcional
```

Luego solo completas los placeholders y pasas a IA.

---

## Ejercicio de Autoevaluación

**Escenario realista:**

Tu API en producción está fallando. Error rate subió de 0.5% a 15% en los últimos 10 minutos.

**Tu tarea:**

1. **Diagnóstico (5 minutos con IA)**:
   - Copia logs de Railway
   - Copia métricas del dashboard
   - Pregunta a IA: "¿Cuál es la root cause?"

2. **Mitigación (5 minutos con IA)**:
   - Pregunta a IA: "¿Cómo mitigo AHORA sin rollback?"
   - Ejecuta la solución propuesta

3. **Fix permanente (10 minutos con IA)**:
   - Pregunta a IA: "¿Cómo arreglo esto permanentemente?"
   - Implementa el fix, escribe test que lo valide

4. **Prevención (5 minutos con IA)**:
   - Pregunta a IA: "¿Cómo prevengo que vuelva a pasar?"
   - Implementa monitoreo/alertas sugeridos

**Criterio de éxito:**

- ✅ Diagnosticas root cause en <5 min (sin IA tomaría 30+ min)
- ✅ Mitigación aplicada en <10 min total
- ✅ Fix permanente implementado y testeado
- ✅ Monitoreo preventivo configurado

**Reflexión:**

¿Cuánto tiempo habrías tardado SIN IA? Probablemente 2-3 horas.
CON IA: 25 minutos.

**Eso es el poder de IA como copiloto DevOps.**

---

## Conclusión: De Junior DevOps a Senior con IA

**Antes de usar IA:**
- Lees docs de GitHub Actions por horas
- Copias ejemplos de Stack Overflow sin entenderlos
- Tu pipeline falla en producción

**Después de usar IA:**
- Describes lo que necesitas en lenguaje natural
- IA genera workflow production-ready en 2 minutos
- Tú entiendes y ajustas según tu contexto
- Deploy automatizado funciona desde el día 1

**El multiplicador**: IA te da experiencia equivalente a un Senior DevOps en áreas específicas (workflows, Dockerfiles, debugging). Tú aportas contexto de negocio y decisiones estratégicas.

**Resultado**: "DevOps Team of One" 🚀

---

## Siguiente Paso

**Practica**: `ejercicio_clase7.md`

Implementarás un pipeline completo de CI/CD usando IA como copiloto en cada paso.

---

**¡A automatizar con IA! 🤖⚙️**
