# Clase 7: AI DevOps - Deployment Automation

## Objetivo

Aprender a usar **IA como copiloto de DevOps** para automatizar workflows de deployment, generar pipelines de CI/CD, y gestionar infraestructura como código con asistencia inteligente.

**Al finalizar esta clase serás capaz de:**

- Usar IA para generar y optimizar GitHub Actions workflows
- Automatizar deployment con validación asistida por IA
- Implementar monitoring y alertas con ayuda de IA
- Aplicar mejores prácticas de DevOps guiadas por IA

---

## Contexto Pedagógico

### ¿Por qué DevOps con IA?

**El problema tradicional:**

Eres un desarrollador solo. Necesitas:
- Configurar CI/CD pipelines complejos
- Escribir scripts de deployment para múltiples entornos
- Configurar monitoring, logs, alertas
- Mantener infraestructura como código (IaC)
- Responder a incidentes en producción

**Sin IA**: Pasas **semanas** leyendo documentación de GitHub Actions, Docker, Kubernetes, Terraform. Copias ejemplos de Stack Overflow que no entiendes. Tu pipeline falla en producción.

**Con IA como copiloto DevOps**: Le describes lo que necesitas en lenguaje natural, la IA genera el workflow completo, tú revisas y ajustas. De **semanas a minutos**.

### La Visión: "DevOps Team of One"

```
Tú (Developer) + IA (DevOps Expert) = Full Stack + DevOps capabilities
```

**Esta clase completa la transformación:**

- **Módulo 1-2**: Desarrollaste APIs con IA
- **Módulo 3**: Las aseguraste con IA
- **Módulo 4 Clase 1-6**: Las containerizaste, conectaste a DB, desplegaste en cloud
- **Módulo 4 Clase 7 (esta)**: Automatizas TODO el ciclo de vida con IA

Después de esta clase: **serás un "DevOps Team of One"** - capaz de llevar código desde tu laptop hasta producción sin ayuda externa.

---

## Conceptos Clave

### 1. CI/CD (Continuous Integration / Continuous Deployment)

**Analogía**: Una fábrica con inspección de calidad automatizada

```
Código nuevo → Tests automáticos → Build → Deploy automático → Monitor
     ↓              ↓                 ↓           ↓              ↓
   Commit      ✅ Pasan tests?    📦 Build    🚀 Deploy      📊 Logs
```

**CI (Continuous Integration)**:
- Cada commit dispara tests automáticos
- Se detectan errores inmediatamente
- Se previenen bugs en producción

**CD (Continuous Deployment)**:
- Si tests pasan, se despliega automáticamente
- Deploy sin intervención manual
- Releases frecuentes y seguros

### 2. GitHub Actions - El Motor de CI/CD

**¿Qué es?**
Una herramienta que ejecuta código en respuesta a eventos de Git (commits, PRs, tags).

**Componentes clave:**

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:  # Evento que dispara el workflow
  push:
    branches: [main]

jobs:  # Tareas a ejecutar
  deploy:
    runs-on: ubuntu-latest  # Máquina donde corre
    steps:  # Pasos secuenciales
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run tests
        run: pytest

      - name: Deploy
        run: ./deploy.sh
```

**Analogía**: Un robot que vigila tu repositorio y ejecuta tareas cuando algo cambia.

### 3. Deployment Strategies

**3.1 Blue-Green Deployment**

```
Production:    [Blue v1.0] <-- 100% traffic
Staging:       [Green v2.0] (ready)

# Después de validar:
Production:    [Green v2.0] <-- 100% traffic  ✅
Old version:   [Blue v1.0] (standby for rollback)
```

**Ventajas**: Rollback instantáneo si algo falla

**3.2 Canary Deployment**

```
Production:
  [v1.0] <-- 95% traffic
  [v2.0] <-- 5% traffic (test users)

# Si métricas OK, aumentar gradualmente:
  [v1.0] <-- 50% traffic
  [v2.0] <-- 50% traffic

# Finalmente:
  [v2.0] <-- 100% traffic ✅
```

**Ventajas**: Detecta problemas con impacto mínimo

**3.3 Rolling Deployment**

```
Instances: [A] [B] [C] [D]  (todas v1.0)

Step 1:    [A v2.0] [B] [C] [D]
Step 2:    [A v2.0] [B v2.0] [C] [D]
Step 3:    [A v2.0] [B v2.0] [C v2.0] [D]
Step 4:    [A v2.0] [B v2.0] [C v2.0] [D v2.0] ✅
```

**Ventajas**: Sin downtime, reemplazo gradual

### 4. Infrastructure as Code (IaC)

**Concepto**: La infraestructura se define en archivos de código versionados.

**Sin IaC** (manual):
```bash
# En AWS Console, hacer clic en:
1. Create EC2 instance
2. Configure security groups
3. Attach EBS volume
4. Configure load balancer
# ... 20 pasos más, CADA VEZ que necesites recrear
```

**Con IaC** (automatizado):
```yaml
# infra/aws.yml
ec2_instance:
  type: t3.medium
  ami: ubuntu-22.04
  security_groups: [web-server]
  volumes: [50GB]
load_balancer:
  type: application
  targets: [ec2_instance]
```

Ejecutas: `terraform apply` → Todo se crea automáticamente y de forma reproducible.

### 5. Monitoring & Observability

**Los 3 pilares:**

**1. Logs**: ¿Qué está pasando?
```python
logger.info("User 123 logged in")
logger.error("Payment failed: insufficient funds")
```

**2. Metrics**: ¿Cómo está el sistema?
```
requests_per_second: 450
error_rate: 0.2%
response_time_p95: 120ms
```

**3. Traces**: ¿Dónde está el problema?
```
Request → API Gateway → Auth Service → Database
                                          ↑ 2000ms delay! 🔴
```

**Analogía**:
- Logs = diario de eventos
- Metrics = panel de instrumentos del coche
- Traces = GPS que muestra cada paso del viaje

---

## IA como Copiloto DevOps

### Casos de Uso Reales

**1. Generar GitHub Actions Workflows**

**Prompt efectivo:**
```
Genera un workflow de GitHub Actions que:
- Se ejecute en push a main y en PRs
- Corra tests con pytest y coverage 80%+
- Haga linting con ruff
- Solo despliegue si tests pasan
- Despliege a Railway usando variable de entorno RAILWAY_TOKEN
- Notifique a Slack en caso de fallo

Usa las últimas versiones de actions y mejores prácticas de seguridad.
```

**IA genera**:
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Lint with ruff
        run: ruff check .

      - name: Run tests with coverage
        run: pytest --cov --cov-report=term-missing --cov-fail-under=80

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Railway
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: |
          npm i -g @railway/cli
          railway up

      - name: Notify Slack on failure
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK }}
          payload: |
            {
              "text": "❌ Deployment failed on ${{ github.repository }}"
            }
```

**Valor agregado de IA:**
- Conoce las últimas versiones de actions (`@v4`, `@v5`)
- Usa cache para pip (acelera builds)
- Implementa dependencias entre jobs (`needs: test`)
- Añade condicionales (`if: github.ref == 'refs/heads/main'`)
- Maneja secrets de forma segura
- Notificaciones solo en fallos

**Tú solo**: Habrías tardado **horas** buscando en docs y Stack Overflow.

---

**2. Debugging de Pipelines que Fallan**

**Escenario**: Tu workflow de GitHub Actions falla con error críptico:

```
Error: Process completed with exit code 1.
```

**Prompt efectivo:**
```
Mi GitHub Actions workflow está fallando con "exit code 1" en el step de tests.

Logs del step:
[pegar logs aquí]

workflow.yml:
[pegar workflow aquí]

requirements.txt:
[pegar dependencias aquí]

¿Cuál es el problema y cómo lo soluciono?
```

**IA analiza y responde:**
```
El problema está en línea 23 del workflow:

  run: pytest --cov --cov-report=term-missing

El error indica que pytest no encuentra los módulos de tu API.
Esto ocurre porque no instalaste el paquete en modo editable.

Solución: Añade antes del step de tests:

  - name: Install package
    run: pip install -e .

Esto añade el directorio actual al PYTHONPATH, permitiendo
que pytest importe los módulos de `api/`.

Alternativamente, si no tienes setup.py, añade PYTHONPATH
manualmente:

  - name: Run tests
    env:
      PYTHONPATH: ${{ github.workspace }}
    run: pytest --cov
```

**Valor agregado**: Diagnostica el problema raíz (PYTHONPATH), no solo el síntoma.

---

**3. Optimización de Dockerfiles para CI**

**Prompt efectivo:**
```
Optimiza este Dockerfile para CI/CD. Necesito:
- Builds rápidos (usar cache de capas)
- Imagen pequeña (<100MB si es posible)
- Multi-stage build
- No root user
- Health check

Dockerfile actual:
[pegar Dockerfile aquí]
```

**IA genera Dockerfile optimizado**:
```dockerfile
# Stage 1: Build dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

# Install dependencies in separate layer (cached if requirements.txt no cambia)
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Production image
FROM python:3.12-slim

# Create non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy only installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .

# Make sure scripts in .local are usable
ENV PATH=/home/appuser/.local/bin:$PATH

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Mejoras aplicadas por IA:**
1. Multi-stage build → Imagen 60% más pequeña
2. Cache de `pip install` → Builds 5x más rápidos
3. Non-root user → Seguridad
4. Health check → Detecta crashes automáticamente
5. `--no-cache-dir` → Ahorra 20MB

---

**4. Generar Scripts de Rollback**

**Prompt efectivo:**
```
Genera un script de rollback para mi API desplegada en Railway.
Debe:
- Detectar la última versión estable (tag git)
- Hacer rollback a esa versión
- Verificar que el rollback funcionó (health check)
- Notificar resultado

Contexto: Uso Railway, FastAPI, y GitHub para versiones.
```

**IA genera `rollback.sh`**:
```bash
#!/bin/bash
set -e

echo "🔄 Starting rollback..."

# Get last stable tag (assumes semantic versioning)
LAST_STABLE=$(git tag -l "v*" | sort -V | tail -n 2 | head -n 1)

if [ -z "$LAST_STABLE" ]; then
  echo "❌ No previous stable version found"
  exit 1
fi

echo "📌 Rolling back to $LAST_STABLE"

# Checkout last stable version
git checkout "$LAST_STABLE"

# Deploy to Railway
railway up --detach

# Wait for deployment
echo "⏳ Waiting for deployment..."
sleep 30

# Health check
HEALTH_URL="https://your-api.railway.app/health"
if curl -f "$HEALTH_URL" > /dev/null 2>&1; then
  echo "✅ Rollback successful! Running $LAST_STABLE"

  # Notify Slack
  curl -X POST "$SLACK_WEBHOOK" \
    -H 'Content-Type: application/json' \
    -d "{\"text\": \"✅ Rollback to $LAST_STABLE successful\"}"
else
  echo "❌ Rollback failed! Health check not passing"
  exit 1
fi
```

**Valor agregado**: Script production-ready con manejo de errores, verificación, y notificaciones.

---

### Prompt Engineering para DevOps

**Anatomía de un Prompt Efectivo para DevOps:**

```
[CONTEXTO] Describe tu stack tecnológico
[OBJETIVO] Qué necesitas lograr
[RESTRICCIONES] Limitaciones (presupuesto, tiempo, seguridad)
[OUTPUT ESPERADO] Formato deseado
[VALIDACIÓN] Cómo verificar que funciona
```

**Ejemplo real:**

```
[CONTEXTO]
- FastAPI API con PostgreSQL
- Desplegada en Railway
- GitHub Actions para CI/CD
- 100 requests/minuto promedio

[OBJETIVO]
Implementar blue-green deployment para evitar downtime durante deploys

[RESTRICCIONES]
- Presupuesto: <$20/mes extra
- Railway permite múltiples servicios
- No puedo usar Kubernetes (demasiado complejo)

[OUTPUT ESPERADO]
- Diagrama de arquitectura
- Script de deployment
- Workflow de GitHub Actions
- Rollback strategy

[VALIDACIÓN]
- Debe haber 0 segundos de downtime durante deploy
- Rollback debe tomar <30 segundos
```

**IA generará**: Solución completa adaptada a tus restricciones (Railway, presupuesto, complejidad).

---

## Workflows Reales con IA

### Workflow 1: De Feature a Producción

```
1. Desarrollas feature en rama local
   ↓
2. Git push → GitHub Actions
   ├─ IA ejecuta: Linting (ruff)
   ├─ IA ejecuta: Tests (pytest + coverage)
   ├─ IA ejecuta: Security scan (bandit)
   └─ Si falla: IA sugiere fix en comentario del PR
   ↓
3. Merge a main → Deploy automático
   ├─ Build Docker image
   ├─ Push a container registry
   ├─ Deploy to staging
   ├─ Run smoke tests
   ├─ Deploy to production (canary 10%)
   ├─ Monitor métricas (5 minutos)
   └─ Si OK: Aumentar a 100%
   ↓
4. Monitoring post-deploy
   ├─ Logs → Aggregate en ELK/Datadog
   ├─ Metrics → Dashboard en Grafana
   └─ Alertas → Slack/PagerDuty si error rate > 1%
```

**Rol de IA en cada paso:**

1. **Desarrollo**: Copiloto de código (GitHub Copilot)
2. **CI**: IA ejecuta validaciones y sugiere fixes
3. **Deploy**: IA decide estrategia (blue-green vs canary)
4. **Monitoring**: IA detecta anomalías y sugiere causas

---

### Workflow 2: Respuesta a Incidentes

**Escenario**: Producción se cae a las 3 AM. Error rate sube a 80%.

**Sin IA:**
```
1. Despertarte con alerta de PagerDuty
2. Revisar logs manualmente (1 hora)
3. Buscar en Stack Overflow (30 min)
4. Intentar fix (30 min)
5. Deploy fix (15 min)
Total: 2+ horas de downtime
```

**Con IA:**
```
1. Alerta automática con logs agregados
2. Copiar logs y preguntar a IA:
   "¿Cuál es la causa root de estos errores?"
3. IA analiza → "Database connection pool agotado"
4. Preguntar: "¿Cómo aumento el pool en Railway?"
5. IA genera: Comando + configuración
6. Ejecutar comando → Problema resuelto
Total: 15 minutos de downtime
```

**Ahorro**: 1h 45min + menos estrés

---

## Monitoreo Inteligente con IA

### 1. Detección de Anomalías

**Problema**: ¿Cómo saber si 450 req/seg es normal o un ataque DDoS?

**Solución con IA**:
```python
# prompts/detect_anomaly.py
import anthropic

def analyze_metrics(metrics: dict) -> str:
    """Usa Claude para detectar anomalías en métricas."""

    prompt = f"""
    Analiza estas métricas de los últimos 30 minutos:

    {metrics}

    Comparado con baseline histórico:
    - Requests/seg promedio: 200-300
    - Error rate promedio: 0.1-0.5%
    - Response time p95: 50-150ms

    ¿Hay alguna anomalía? ¿Requiere acción inmediata?
    Responde en formato JSON:
    {{
      "anomaly_detected": true/false,
      "severity": "low/medium/high/critical",
      "description": "...",
      "recommended_action": "..."
    }}
    """

    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text
```

**Uso en workflow:**
```yaml
# .github/workflows/monitor.yml
name: Continuous Monitoring

on:
  schedule:
    - cron: '*/15 * * * *'  # Every 15 minutes

jobs:
  check-health:
    runs-on: ubuntu-latest
    steps:
      - name: Fetch metrics
        run: |
          curl https://api.production.com/metrics > metrics.json

      - name: Analyze with AI
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python prompts/detect_anomaly.py metrics.json

      - name: Alert if critical
        if: contains(steps.analyze.outputs.result, 'critical')
        run: |
          # Send alert to Slack/PagerDuty
```

---

### 2. Root Cause Analysis Automático

**Cuando algo falla, IA analiza logs para encontrar la causa:**

```python
# scripts/rca.py
"""Root Cause Analysis con IA"""

def analyze_incident(error_logs: str, metrics: dict) -> dict:
    prompt = f"""
    Ocurrió un incidente en producción. Analiza:

    LOGS (últimos 100 errores):
    {error_logs}

    MÉTRICAS en el momento del incidente:
    {metrics}

    Provee:
    1. Causa raíz probable (la más específica)
    2. Cómo llegaste a esa conclusión
    3. Steps para mitigar inmediatamente
    4. Steps para prevenir recurrencia

    Formato: JSON estructurado
    """

    # ... (llamada a Claude API)
```

**Resultado**:
```json
{
  "root_cause": "Database connection pool exhausted due to N+1 query in /users endpoint",
  "evidence": [
    "Log shows 1000+ queries to DB in 1 second",
    "All errors are 'connection timeout'",
    "CPU spike coincides with /users endpoint spike"
  ],
  "immediate_mitigation": [
    "Restart API instances to reset connection pool",
    "Rate limit /users endpoint temporarily"
  ],
  "long_term_fix": [
    "Add eager loading to User query (use .join())",
    "Implement query result caching",
    "Add database connection pool monitoring"
  ]
}
```

**Valor**: Lo que tomaría 1 hora de investigación manual → 30 segundos.

---

## Mejores Prácticas de DevOps con IA

### 1. Versionado Semántico Automático

**Usa IA para determinar el tipo de cambio:**

```yaml
# .github/workflows/release.yml
name: Semantic Release

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Fetch all history

      - name: Analyze commits with AI
        id: version
        run: |
          # Get commits since last tag
          COMMITS=$(git log $(git describe --tags --abbrev=0)..HEAD --oneline)

          # Ask AI to categorize
          python << EOF
          import anthropic

          commits = """$COMMITS"""

          prompt = f"""
          Analiza estos commits y determina el tipo de release según Semantic Versioning:

          {commits}

          Responde solo: MAJOR, MINOR, o PATCH

          Reglas:
          - MAJOR: Breaking changes (API incompatible)
          - MINOR: New features (backward compatible)
          - PATCH: Bug fixes
          """

          # ... (call API, output version bump)
          EOF

      - name: Create release
        run: |
          # Bump version based on AI decision
          npm version ${{ steps.version.outputs.bump }}
          git push --tags
```

---

### 2. Documentación Auto-Generada

**Genera CHANGELOG automáticamente:**

```yaml
- name: Generate CHANGELOG with AI
  run: |
    python << EOF
    import anthropic

    commits = """$(git log --oneline --since="1 month ago")"""

    prompt = f"""
    Genera un CHANGELOG.md profesional agrupando estos commits:

    {commits}

    Agrupa por categorías:
    - 🚀 Features
    - 🐛 Bug Fixes
    - 📚 Documentation
    - ⚡ Performance
    - 🔒 Security

    Escribe en español, tono profesional, bullets concisos.
    """
    # ... (write to CHANGELOG.md)
    EOF
```

---

### 3. Infrastructure as Code Review

**IA revisa tus archivos Terraform/Docker:**

```bash
# Pre-commit hook con IA
# .git/hooks/pre-commit

#!/bin/bash

# Detectar cambios en infra/
CHANGED=$(git diff --cached --name-only | grep "^infra/")

if [ -n "$CHANGED" ]; then
  echo "🔍 Reviewing infrastructure changes with AI..."

  python << EOF
import anthropic

files_changed = """$CHANGED"""

for file in files_changed.split('\n'):
    content = open(file).read()

    prompt = f"""
    Revisa este archivo de infraestructura:

    {file}:
    {content}

    Busca:
    - Configuraciones inseguras (puertos abiertos, credenciales hardcoded)
    - Anti-patterns (recursos sin tags, no root user check)
    - Costos innecesarios (instancias oversized)

    Si encuentras problemas: explícalos y sugiere fix.
    Si está OK: di "✅ LGTM"
    """

    # ... (call API, print review)
EOF
fi
```

**Resultado**: Cada cambio de infra es revisado por IA antes del commit.

---

## Arquitectura de Referencia

### Stack Completo con IA DevOps

```
┌─────────────────────────────────────────────────────────┐
│                    DEVELOPER                            │
│  (Tú + GitHub Copilot)                                  │
└──────────────────┬──────────────────────────────────────┘
                   │ git push
                   ▼
┌─────────────────────────────────────────────────────────┐
│                 GITHUB ACTIONS                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ Linting  │→ │  Tests   │→ │ Security │             │
│  │ (Ruff)   │  │ (Pytest) │  │ (Bandit) │             │
│  └──────────┘  └──────────┘  └──────────┘             │
│                      ↓                                  │
│            ✅ All checks pass                           │
└──────────────────┬──────────────────────────────────────┘
                   │ Auto deploy
                   ▼
┌─────────────────────────────────────────────────────────┐
│              CONTAINER REGISTRY                         │
│  (GitHub Container Registry / Docker Hub)               │
│  📦 your-api:v2.1.0                                     │
└──────────────────┬──────────────────────────────────────┘
                   │
          ┌────────┴────────┐
          ▼                 ▼
┌──────────────────┐  ┌──────────────────┐
│   STAGING        │  │   PRODUCTION     │
│  (Railway/Fly)   │  │  (Railway/Fly)   │
│  🧪 Test env     │  │  🚀 Live users   │
└────────┬─────────┘  └────────┬─────────┘
         │                     │
         └──────────┬──────────┘
                    │ Logs/Metrics
                    ▼
┌─────────────────────────────────────────────────────────┐
│              MONITORING & OBSERVABILITY                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │  Logs    │  │ Metrics  │  │  Traces  │             │
│  │ (Datadog)│  │(Prometheus│  │ (Jaeger) │             │
│  └──────────┘  └──────────┘  └──────────┘             │
│                      ↓                                  │
│             🤖 AI Anomaly Detection                     │
│                      ↓                                  │
│             🚨 Alerts (Slack/PagerDuty)                 │
└─────────────────────────────────────────────────────────┘
```

**Flujo completo:**

1. **Desarrollas** con GitHub Copilot → Código de calidad
2. **Push** → GitHub Actions ejecuta validaciones
3. **Tests pass** → Auto-deploy a staging
4. **Smoke tests OK** → Deploy a production (canary)
5. **IA monitorea** métricas → Alerta si anomalías
6. **Incident?** → IA hace Root Cause Analysis → Sugiere fix

**Resultado**: Ciclo completo automatizado, IA en cada paso crítico.

---

## Ejercicio Práctico

Ver: `ejercicio_clase7.md`

**Objetivo**: Configurar CI/CD completo con GitHub Actions y deployment automático a Railway, usando IA para generar workflows.

---

## Recursos Adicionales

### Herramientas Clave

**CI/CD:**
- [GitHub Actions](https://docs.github.com/actions)
- [GitLab CI](https://docs.gitlab.com/ee/ci/)
- [CircleCI](https://circleci.com/docs/)

**Deployment Platforms:**
- [Railway](https://railway.app/) - Recomendado para este curso
- [Fly.io](https://fly.io/)
- [Render](https://render.com/)

**Monitoring:**
- [Datadog](https://www.datadoghq.com/) - Observability completa
- [Sentry](https://sentry.io/) - Error tracking (ya visto en M3)
- [Prometheus + Grafana](https://prometheus.io/) - Open source

**Infrastructure as Code:**
- [Terraform](https://www.terraform.io/)
- [Pulumi](https://www.pulumi.com/) - IaC con Python

### Lecturas Recomendadas

**DevOps Fundamentals:**
- [The Phoenix Project](https://itrevolution.com/product/the-phoenix-project/) - Novela sobre DevOps
- [Accelerate](https://itrevolution.com/product/accelerate/) - Métricas de DevOps

**GitHub Actions:**
- [GitHub Actions Official Docs](https://docs.github.com/en/actions)
- [Awesome Actions](https://github.com/sdras/awesome-actions) - Lista curada

**AI + DevOps:**
- [AIOps: Artificial Intelligence for IT Operations](https://www.gartner.com/en/information-technology/glossary/aiops-artificial-intelligence-operations)
- [GitHub Copilot for CLI](https://githubnext.com/projects/copilot-cli)

### Prompts Útiles

```
# Para generar workflows
"Genera un GitHub Actions workflow que [describe objetivo]. Stack: [tecnologías]. Debe incluir [requirements]."

# Para debugging
"Mi workflow falla con este error: [error]. Logs: [logs]. workflow.yml: [archivo]. ¿Cuál es el problema?"

# Para optimización
"Optimiza este Dockerfile para CI/CD: [Dockerfile]. Necesito builds rápidos y imagen pequeña."

# Para monitoring
"Analiza estas métricas: [datos]. ¿Hay anomalías? ¿Requiere acción?"

# Para infrastructure
"Genera un archivo docker-compose.yml para: API FastAPI + PostgreSQL + Redis. Incluye health checks y volúmenes persistentes."
```

---

## Siguientes Pasos

**Después de esta clase:**

1. **Módulo 4 Clase 8**: Proyecto final integrador (API completa con todo lo aprendido)
2. **Módulo 5**: Full-Stack (React + FastAPI) con deployment automatizado

**Habilidades adquiridas:**

✅ Configurar CI/CD con GitHub Actions
✅ Automatizar deployment a cloud platforms
✅ Implementar monitoring y alertas
✅ Usar IA para generar y optimizar workflows
✅ Responder a incidentes con asistencia de IA
✅ **SER UN "DevOps Team of One"**

---

## Glosario

Ver: `glosario_clase7.md`

---

## Conclusión

**Antes de esta clase**: Sabías programar APIs y desplegarlas manualmente.

**Después de esta clase**: Eres un **DevOps Team of One** - capaz de automatizar todo el ciclo de vida de una aplicación, desde commit hasta producción, con asistencia de IA en cada paso crítico.

**La magia**: IA te da **superpoderes de automatización**. Lo que un equipo DevOps de 3 personas hacía en 1 semana, tú lo haces en 1 día.

**Siguiente nivel**: Módulo 5 - Aplicar todo lo aprendido en proyectos Full-Stack completos.

---

**¡A automatizar con IA! 🚀**
