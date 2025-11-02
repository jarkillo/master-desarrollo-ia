# Glosario - Clase 7: AI DevOps (Deployment Automation)

## Términos de DevOps

### CI/CD
**Continuous Integration / Continuous Deployment**

- **CI (Continuous Integration)**: Práctica de integrar cambios de código frecuentemente (varios commits por día) con tests automáticos para detectar errores temprano.
- **CD (Continuous Deployment)**: Extensión de CI donde código que pasa tests se despliega automáticamente a producción sin intervención manual.

**Analogía**: Una fábrica con inspección de calidad automatizada en cada paso.

**Ejemplo**:
```
Developer commit → Tests automáticos → Build → Deploy a producción
```

---

### GitHub Actions
**Sistema de CI/CD integrado en GitHub**

Permite ejecutar código en respuesta a eventos (push, PR, tags, schedule).

**Componentes**:
- **Workflow**: Archivo YAML que define el proceso
- **Job**: Conjunto de steps que se ejecutan juntos
- **Step**: Comando individual (bash, action reutilizable)
- **Runner**: Máquina donde se ejecuta (ubuntu, windows, macos)

**Ejemplo**:
```yaml
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: pytest
```

---

### Pipeline
**Secuencia automatizada de pasos desde código hasta producción**

Serie de stages (build, test, deploy) que código debe pasar.

**Analogía**: Tubería donde código fluye y pasa por filtros (tests, quality gates).

**Ejemplo**:
```
Code → Lint → Test → Build → Deploy Staging → Deploy Production
```

---

### Deployment Strategies

#### Blue-Green Deployment
**Dos ambientes idénticos: uno activo (blue), otro standby (green)**

**Proceso**:
1. Blue recibe 100% tráfico (producción actual)
2. Deploy nueva versión a Green
3. Validar Green
4. Switch tráfico: Green = 100%
5. Blue queda como rollback

**Ventaja**: Rollback instantáneo (switch de vuelta a Blue)

---

#### Canary Deployment
**Deploy gradual, empezando con pequeño % de usuarios**

**Proceso**:
1. Deploy nueva versión a subset de servidores (5-10%)
2. Monitorear métricas (error rate, latency)
3. Si OK, aumentar gradualmente (25% → 50% → 100%)
4. Si falla, rollback afecta solo a subset pequeño

**Ventaja**: Detecta problemas con impacto mínimo

**Origen del nombre**: Los mineros llevaban canarios a las minas. Si el canario moría (gas tóxico), sabían que debían evacuar. Similar: un pequeño grupo de usuarios "prueba" nueva versión.

---

#### Rolling Deployment
**Actualización gradual de instancias, una por una**

**Proceso**:
1. Tienes N instancias corriendo v1.0
2. Bajas instancia 1, actualizas a v2.0, subes
3. Repites con instancia 2, 3, ..., N
4. Al final, todas están en v2.0

**Ventaja**: Sin downtime

---

### Rollback
**Revertir a versión anterior cuando deployment falla**

Proceso de volver a estado conocido estable.

**Estrategias**:
- **Git-based**: Checkout de tag anterior + redeploy
- **Blue-Green**: Switch tráfico de vuelta
- **Snapshot**: Restaurar snapshot de infraestructura

**Ejemplo**:
```bash
git checkout v1.0.0  # Versión estable
railway up           # Redeploy
```

---

### Infrastructure as Code (IaC)
**Gestión de infraestructura mediante archivos de código versionados**

En vez de crear servidores manualmente (clicks en consola), defines infraestructura en archivos.

**Herramientas**:
- Terraform (multi-cloud)
- Pulumi (IaC con Python/TypeScript)
- CloudFormation (AWS)
- docker-compose (contenedores)

**Ventajas**:
- Reproducible
- Versionado (Git)
- Revisable (code review)
- Automatizable

**Ejemplo (docker-compose.yml)**:
```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
  db:
    image: postgres:15
    volumes:
      - db_data:/var/lib/postgresql/data
```

---

## Términos de Monitoring & Observability

### Observability
**Capacidad de entender estado interno de un sistema basado en outputs externos**

**Los 3 pilares**:

1. **Logs**: Registros de eventos
   ```
   2024-11-01 12:00:00 INFO User 123 logged in
   2024-11-01 12:00:05 ERROR Payment failed: insufficient funds
   ```

2. **Metrics**: Mediciones numéricas
   ```
   requests_per_second: 450
   error_rate: 0.2%
   response_time_p95: 120ms
   ```

3. **Traces**: Rastreo de requests a través de servicios
   ```
   Request ID 789
   → API Gateway (5ms)
   → Auth Service (50ms)
   → Database (2000ms) ← BOTTLENECK
   Total: 2055ms
   ```

---

### Health Check
**Endpoint que indica si servicio está funcionando correctamente**

Típicamente endpoint `/health` que retorna 200 OK si todo está bien.

**Ejemplo**:
```python
@app.get("/health")
def health():
    return {"status": "healthy"}
```

**Uso**:
- Docker: HEALTHCHECK en Dockerfile
- Kubernetes: liveness/readiness probes
- Load balancers: Detectar instancias no saludables

---

### Uptime
**Porcentaje de tiempo que servicio está disponible**

**Cálculo**:
```
Uptime = (Tiempo online / Tiempo total) × 100%
```

**Estándares**:
- 99% (two nines): ~7.2 horas downtime/mes
- 99.9% (three nines): ~43 minutos downtime/mes
- 99.99% (four nines): ~4 minutos downtime/mes
- 99.999% (five nines): ~26 segundos downtime/mes

**Herramienta**: UptimeRobot, Pingdom

---

### SLA (Service Level Agreement)
**Acuerdo formal de nivel de servicio garantizado**

Contrato que especifica uptime esperado y compensación si no se cumple.

**Ejemplo**:
```
SLA: 99.9% uptime mensual
- Si uptime < 99.9%: 10% crédito
- Si uptime < 99%: 25% crédito
```

---

### Anomaly Detection
**Identificación automática de comportamiento inusual en métricas**

Usar IA/ML para detectar patrones que se desvían de baseline histórico.

**Ejemplo**:
```
Baseline: 200-300 req/seg
Actual: 2000 req/seg ← ANOMALÍA (posible DDoS)
```

---

## Términos de GitHub Actions

### Workflow
**Archivo YAML que define proceso automatizado**

Se guarda en `.github/workflows/nombre.yml`

**Ejemplo**:
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest
```

---

### Job
**Conjunto de steps que se ejecutan en mismo runner**

Jobs corren en paralelo por defecto, a menos que uses `needs`.

**Ejemplo**:
```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [...]

  test:
    runs-on: ubuntu-latest
    needs: lint  # Espera a que lint termine
    steps: [...]
```

---

### Step
**Acción individual dentro de un job**

Puede ser comando bash (`run`) o action reutilizable (`uses`).

**Ejemplo**:
```yaml
steps:
  - name: Checkout code
    uses: actions/checkout@v4

  - name: Run tests
    run: pytest
```

---

### Action
**Componente reutilizable para workflows**

Marketplace de GitHub tiene miles de actions predefinidas.

**Ejemplo**:
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: 'pip'
```

---

### Runner
**Máquina donde se ejecuta el workflow**

**Opciones**:
- `ubuntu-latest` (más común, gratis)
- `windows-latest`
- `macos-latest`
- Self-hosted (tu propio servidor)

---

### Secret
**Variable de entorno sensible almacenada encriptada**

Para API keys, tokens, passwords.

**Configurar**: GitHub repo → Settings → Secrets and variables → Actions

**Usar**:
```yaml
steps:
  - name: Deploy
    env:
      API_KEY: ${{ secrets.API_KEY }}
    run: ./deploy.sh
```

---

### Matrix
**Ejecutar job con múltiples configuraciones**

**Ejemplo** (probar con Python 3.11 y 3.12):
```yaml
jobs:
  test:
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
```

---

### Cache
**Almacenar archivos entre ejecuciones para acelerar builds**

**Ejemplo** (cache de pip):
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: 'pip'  # Cachea dependencias de pip
```

**Resultado**: Instalación de dependencias 5-10x más rápida.

---

## Términos de Docker

### Multi-stage Build
**Dockerfile con múltiples etapas, usando solo output de última etapa**

**Propósito**: Imagen final pequeña (sin compiladores, headers, etc.)

**Ejemplo**:
```dockerfile
# Stage 1: Build
FROM python:3.12 AS builder
RUN pip install --user -r requirements.txt

# Stage 2: Production (imagen final)
FROM python:3.12-slim
COPY --from=builder /root/.local /usr/local
```

**Resultado**: Imagen 60-70% más pequeña

---

### Layer Caching
**Docker reutiliza capas (layers) no modificadas**

Cada comando en Dockerfile crea una capa. Si capa no cambió, Docker usa cache.

**Optimización**:
```dockerfile
# ❌ MALO: invalida cache si CUALQUIER archivo cambia
COPY . .
RUN pip install -r requirements.txt

# ✅ BUENO: cache se invalida solo si requirements.txt cambia
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

---

### Health Check (Docker)
**Comando que Docker ejecuta periódicamente para verificar que container está OK**

**Sintaxis**:
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

**Estados**:
- `starting`: Aún no ha pasado primer check
- `healthy`: Checks pasando
- `unhealthy`: 3+ checks fallidos consecutivos

---

### Image Size
**Tamaño de imagen Docker en MB/GB**

**Objetivo**: Más pequeña posible para:
- Builds rápidos
- Deploy rápido
- Menor consumo de storage

**Optimizaciones**:
- Usar base image slim (`python:3.12-slim` vs `python:3.12`)
- Multi-stage build
- `--no-cache-dir` en pip
- Cleanup de caches (`rm -rf /var/lib/apt/lists/*`)

**Benchmark**:
- Sin optimizar: 400-600MB
- Optimizado: 100-150MB

---

## Términos de Railway

### Railway
**Plataforma de deployment simplificada (PaaS)**

Deploy con `railway up`, sin configurar infraestructura.

**Features**:
- Auto-scaling
- PostgreSQL managed
- Logs centralizados
- Metrics dashboards

---

### Railway CLI
**Herramienta de línea de comandos para Railway**

**Instalación**:
```bash
npm i -g @railway/cli
```

**Comandos clave**:
- `railway login`: Autenticar
- `railway up`: Deploy
- `railway logs`: Ver logs
- `railway whoami`: Obtener token

---

### RAILWAY_TOKEN
**Token de autenticación para Railway CLI**

Usado en CI/CD para deploy automático.

**Obtener**:
```bash
railway login
railway whoami
```

**Usar en GitHub Actions**:
```yaml
env:
  RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
run: railway up
```

---

## Términos de Seguridad en CI/CD

### Secrets Management
**Manejo seguro de credenciales en pipelines**

**Mejores prácticas**:
- ✅ Usar GitHub Secrets (encriptados)
- ✅ Variables de entorno (no hardcoded)
- ❌ NUNCA commitear secrets en código
- ❌ NUNCA imprimir secrets en logs

**Ejemplo**:
```yaml
# ✅ CORRECTO
env:
  API_KEY: ${{ secrets.API_KEY }}

# ❌ INCORRECTO
env:
  API_KEY: "sk-1234567890abcdef"  # Hardcoded!
```

---

### Least Privilege
**Dar mínimos permisos necesarios**

**Ejemplo**:
- Token de GitHub: Solo permisos de `repo:write`, no `admin`
- Usuario Docker: No root (`USER appuser`)

---

### Supply Chain Security
**Seguridad de dependencias y herramientas**

**Riesgos**:
- Dependencias con vulnerabilidades
- Actions maliciosos
- Base images comprometidas

**Mitigaciones**:
- Pin versions de actions (`uses: actions/checkout@v4` no `@main`)
- Scan de vulnerabilidades (Dependabot, Safety)
- Usar images oficiales verificadas

---

## Términos de Métricas

### SLI (Service Level Indicator)
**Métrica cuantitativa de un aspecto del servicio**

**Ejemplos**:
- Uptime: % de tiempo servicio disponible
- Latency: Tiempo de respuesta p95
- Error rate: % de requests con error

---

### SLO (Service Level Objective)
**Objetivo interno de SLI**

**Ejemplo**:
```
SLI: Error rate
SLO: Error rate < 0.5%
```

Si se viola SLO → Alerta al equipo

---

### Error Budget
**Cantidad de errores "permitidos" según SLO**

**Cálculo**:
```
SLO: 99.9% uptime
Error budget: 100% - 99.9% = 0.1%
En 30 días: 0.1% × 30 días = 43 minutos de downtime permitido
```

Si se agota error budget → Freeze de features, solo bug fixes.

---

## Términos de IA en DevOps

### AI-Assisted DevOps (AIOps)
**Uso de IA para automatizar operaciones de DevOps**

**Casos de uso**:
- Generar workflows automáticamente
- Detectar anomalías en métricas
- Root Cause Analysis de incidentes
- Auto-remediation de problemas

---

### Root Cause Analysis (RCA)
**Proceso de identificar causa raíz de un incidente**

**Con IA**:
1. Copiar logs + métricas
2. Preguntar a IA: "¿Cuál es la causa raíz?"
3. IA analiza patrones → Identifica causa
4. IA sugiere fix

**Resultado**: RCA en minutos vs horas manualmente

---

### Auto-remediation
**Corrección automática de problemas sin intervención humana**

**Ejemplo con IA**:
```
Detección: Error rate subió a 15%
IA analiza: "Database connection pool agotado"
IA sugiere: "Aumentar pool a 50 conexiones"
Auto-remediation: Ejecuta comando automáticamente
```

---

## Términos de Testing en CI/CD

### Smoke Test
**Test básico que verifica funcionalidad crítica**

**Analogía**: Encender máquina y verificar que no sale humo.

**Ejemplo**:
```bash
# Después de deploy
curl https://api.com/health  # ¿Responde?
curl https://api.com/tasks   # ¿Endpoint funciona?
```

---

### Integration Test
**Test que verifica interacción entre componentes**

**Ejemplo**:
```python
def test_crear_tarea_integración():
    # Test completo: API → Service → Repository → DB
    response = client.post("/tasks", json={"titulo": "Test"})
    assert response.status_code == 201
    assert db.query(Task).count() == 1
```

---

### End-to-End Test (E2E)
**Test que simula flujo completo de usuario**

**Ejemplo** (con Playwright):
```python
# Usuario completa flujo: login → crear tarea → listar → logout
page.goto("https://app.com/login")
page.fill("#username", "test@example.com")
page.fill("#password", "password")
page.click("#login-button")
page.click("#new-task")
# ... etc
```

---

## Acrónimos Comunes

- **CI/CD**: Continuous Integration / Continuous Deployment
- **SLA**: Service Level Agreement
- **SLI**: Service Level Indicator
- **SLO**: Service Level Objective
- **IaC**: Infrastructure as Code
- **YAML**: YAML Ain't Markup Language (formato de configuración)
- **API**: Application Programming Interface
- **RCA**: Root Cause Analysis
- **AIOps**: Artificial Intelligence for IT Operations
- **PaaS**: Platform as a Service (Railway, Heroku, Fly.io)
- **SaaS**: Software as a Service
- **IaaS**: Infrastructure as a Service (AWS, GCP, Azure)

---

## Comandos Clave

```bash
# GitHub Actions (local testing con act)
act                           # Ejecutar workflow localmente
act -l                        # Listar workflows disponibles
act -n                        # Dry run (no ejecutar, solo mostrar)

# Railway CLI
railway login                 # Autenticar
railway up                    # Deploy
railway logs                  # Ver logs
railway open                  # Abrir app en browser
railway whoami                # Mostrar usuario y token

# Docker
docker build -t app .         # Build imagen
docker run -p 8000:8000 app   # Correr container
docker ps                     # Listar containers corriendo
docker images                 # Listar imágenes
docker system prune -a        # Limpiar espacio (borra todo!)

# Git (para rollbacks)
git tag -l "v*"               # Listar tags
git checkout v1.0.0           # Checkout de tag específico
git describe --tags           # Mostrar tag actual

# Health checks
curl -f http://localhost:8000/health   # Verificar health check
```

---

## Recursos

**Documentación oficial**:
- [GitHub Actions Docs](https://docs.github.com/actions)
- [Railway Docs](https://docs.railway.app)
- [Docker Docs](https://docs.docker.com)

**Herramientas mencionadas**:
- [UptimeRobot](https://uptimerobot.com) - Monitoring gratuito
- [act](https://github.com/nektos/act) - Ejecutar GitHub Actions localmente
- [yamllint](https://yamllint.readthedocs.io/) - Validar sintaxis YAML

---

**Este glosario cubre los términos clave de la Clase 7. Para términos de módulos anteriores, ver glosarios de clases previas.**
