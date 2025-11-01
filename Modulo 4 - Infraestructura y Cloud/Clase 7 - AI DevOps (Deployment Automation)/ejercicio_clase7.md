# Ejercicio Práctico: CI/CD Completo con IA

## Objetivo

Implementar un pipeline de CI/CD completo para tu API de tareas usando GitHub Actions y Railway, con **IA como copiloto en cada paso**.

**Duración estimada**: 2-3 horas (60% implementación, 40% usando IA)

---

## Contexto

Tienes una API de tareas (FastAPI) que funciona localmente. Necesitas:

1. **CI** (Continuous Integration): Tests automáticos en cada push/PR
2. **CD** (Continuous Deployment): Deploy automático a Railway cuando tests pasan
3. **Monitoring**: Health checks y alertas básicas
4. **Rollback**: Script de rollback automático si algo falla

**Stack:**
- FastAPI + PostgreSQL
- GitHub para código
- GitHub Actions para CI/CD
- Railway para hosting

---

## Fase 1: Setup Inicial (15 minutos)

### 1.1 Preparar Repositorio

**Código base**: Usa tu API de la Clase 6 (o cualquier clase del Módulo 4).

```bash
# Asegúrate de tener estos archivos:
.
├── api/
│   ├── api.py
│   ├── servicio_tareas.py
│   └── repositorio_json.py
├── tests/
│   └── test_*.py
├── requirements.txt
├── Dockerfile
└── README.md
```

**Checklist:**
- [ ] API funciona localmente (`uvicorn api.api:app --reload`)
- [ ] Tests pasan (`pytest`)
- [ ] Dockerfile existe y construye (`docker build -t api-tareas .`)
- [ ] Git repository inicializado con remote en GitHub

---

### 1.2 Crear Cuenta Railway

1. Ve a [railway.app](https://railway.app)
2. Login with GitHub
3. Crear nuevo proyecto: "api-tareas-prod"
4. Obtener RAILWAY_TOKEN:
   ```bash
   # Instalar Railway CLI
   npm i -g @railway/cli

   # Login
   railway login

   # Obtener token
   railway whoami
   ```

5. Guardar token en GitHub Secrets:
   - GitHub repo → Settings → Secrets and variables → Actions
   - New repository secret
   - Name: `RAILWAY_TOKEN`
   - Value: `[tu token]`

---

## Fase 2: CI con GitHub Actions (45 minutos)

### 2.1 Generar Workflow con IA

**Prompt para Claude/ChatGPT:**

```
Genera un workflow de GitHub Actions para mi API FastAPI con estos requisitos:

CONTEXTO:
- Python 3.12
- FastAPI con tests en pytest
- Linting con ruff
- Dependencias en requirements.txt
- Tests en directorio tests/

WORKFLOW DEBE:
1. Ejecutarse en:
   - Push a main
   - Pull requests a main

2. Jobs (en orden):
   a) lint: Ejecutar ruff check
   b) test: Ejecutar pytest con coverage mínimo 80%
   c) build: Construir Docker image (solo si lint y test pasan)

3. Optimizaciones:
   - Usar cache de pip para acelerar instalación
   - Usar últimas versiones de actions (@v4, @v5)
   - Jobs lint y test deben correr en paralelo
   - Job build solo corre si los anteriores pasan

4. Matriz de versiones Python:
   - Probar con Python 3.11 y 3.12

Output: Archivo .github/workflows/ci.yml completo con comentarios explicativos
```

**📝 IMPORTANTE**: Usa exactamente este prompt. La IA generará un workflow production-ready.

---

### 2.2 Implementar Workflow

1. Crear directorio:
   ```bash
   mkdir -p .github/workflows
   ```

2. Copiar output de IA a `.github/workflows/ci.yml`

3. Revisar y ajustar si es necesario:
   - ¿Paths correctos? (`tests/` vs `test/`)
   - ¿Comando de ruff correcto? (`ruff check .` vs `ruff check api/`)
   - ¿Coverage threshold? (`--cov-fail-under=80`)

4. Commit y push:
   ```bash
   git add .github/workflows/ci.yml
   git commit -m "feat: add CI workflow with linting, tests, and build"
   git push origin main
   ```

5. **Verificar**:
   - Ve a GitHub → Actions tab
   - Deberías ver el workflow ejecutándose
   - Espera a que termine (1-3 minutos)

**Checkpoint**: ✅ Workflow pasa con todos los jobs en verde

---

### 2.3 Debugging con IA (si workflow falla)

**Si el workflow falla:**

1. Click en el job que falló
2. Copiar logs del step con error
3. Preguntar a IA:

```
Mi GitHub Actions workflow está fallando. Ayuda a diagnosticar:

ERROR:
[pegar mensaje de error]

LOGS:
[pegar logs completos del step]

WORKFLOW ci.yml:
[pegar tu archivo workflow]

¿Cuál es el problema y cómo lo soluciono?
```

4. Implementar fix sugerido
5. Commit y push de nuevo
6. Repetir hasta que pase ✅

---

## Fase 3: CD con Deployment Automático (30 minutos)

### 3.1 Añadir Job de Deploy

**Prompt para IA:**

```
Añade un job de deploy a mi workflow de GitHub Actions:

WORKFLOW ACTUAL:
[pegar tu ci.yml]

NUEVO JOB:
- Nombre: "deploy"
- Debe correr SOLO si:
  * Jobs lint y test pasan
  * Push es a branch main (NO en PRs)
- Steps:
  1. Checkout code
  2. Deploy a Railway usando railway CLI
  3. Verificar deploy exitoso (health check en /health)

CONTEXTO:
- RAILWAY_TOKEN está en GitHub secrets
- API tiene endpoint /health que retorna 200 si está OK
- Railway project: "api-tareas-prod"
- Comando deploy: railway up --detach

Output: Job "deploy" completo para añadir a ci.yml
```

**Implementar:**

1. Copiar job generado por IA
2. Añadirlo a `.github/workflows/ci.yml` después del job `build`
3. Commit y push:
   ```bash
   git add .github/workflows/ci.yml
   git commit -m "feat: add automated deployment to Railway"
   git push origin main
   ```

4. **Verificar**:
   - GitHub Actions ejecuta workflow
   - Job "deploy" corre SOLO en push a main (no en PRs)
   - Deploy exitoso ✅
   - API responde en URL de Railway

---

### 3.2 Añadir Health Check

**Si tu API no tiene endpoint /health:**

**Prompt para IA:**

```
Añade un endpoint /health a mi FastAPI:

DEBE RETORNAR:
- Status 200 si todo OK
- JSON con:
  {
    "status": "healthy",
    "timestamp": "2024-11-01T12:00:00Z",
    "version": "1.0.0"
  }

CONTEXTO:
- FastAPI app en api/api.py
- Debe ser un endpoint simple (no queries a DB)

Output: Código Python para añadir a api.py
```

**Implementar:**

1. Añadir endpoint a `api/api.py`
2. Test manual:
   ```bash
   curl http://localhost:8000/health
   # Debe retornar: {"status":"healthy",...}
   ```
3. Commit:
   ```bash
   git add api/api.py
   git commit -m "feat: add health check endpoint"
   git push origin main
   ```

---

## Fase 4: Optimización de Dockerfile (20 minutos)

### 4.1 Analizar Dockerfile Actual

**Construir y medir:**

```bash
# Build y medir tiempo
time docker build -t api-tareas .

# Verificar tamaño
docker images | grep api-tareas
```

**Anota:**
- Build time: _____ segundos
- Image size: _____ MB

---

### 4.2 Optimizar con IA

**Prompt:**

```
Optimiza este Dockerfile para CI/CD:

DOCKERFILE ACTUAL:
[pegar tu Dockerfile]

OBJETIVOS:
- Builds rápidos (usar cache de capas efectivo)
- Imagen pequeña (<150MB si es posible)
- Multi-stage build
- Non-root user (seguridad)
- Health check incluido

CONTEXTO:
- Se construye en cada push a main (builds frecuentes)
- Base: Python 3.12
- App: FastAPI con uvicorn
- Dependencias: requirements.txt (~20 paquetes)

Output: Dockerfile optimizado con comentarios explicativos sobre cada optimización
```

**Implementar:**

1. Reemplazar Dockerfile con versión optimizada
2. Reconstruir y medir:
   ```bash
   time docker build -t api-tareas-optimized .
   docker images | grep api-tareas-optimized
   ```

3. **Comparar**:
   - Build time: Antes ___s → Después ___s (mejora: __%)
   - Image size: Antes ___MB → Después ___MB (mejora: __%)

4. **Checkpoint**: ✅ Build al menos 30% más rápido O imagen al menos 30% más pequeña

5. Commit:
   ```bash
   git add Dockerfile
   git commit -m "perf: optimize Dockerfile for faster builds and smaller image"
   git push origin main
   ```

---

## Fase 5: Monitoring y Alertas (30 minutos)

### 5.1 Configurar Uptime Monitoring

**Opción 1: UptimeRobot (Gratis)**

1. Crear cuenta en [uptimerobot.com](https://uptimerobot.com)
2. Add New Monitor:
   - Type: HTTP(s)
   - URL: `https://tu-api.railway.app/health`
   - Interval: 5 minutes
   - Alert contacts: Tu email

**Opción 2: Railway Health Checks**

Railway lo hace automáticamente si tienes HEALTHCHECK en Dockerfile.

---

### 5.2 Añadir Notificaciones a Slack (Opcional pero recomendado)

**Crear Webhook de Slack:**

1. Ir a [api.slack.com/messaging/webhooks](https://api.slack.com/messaging/webhooks)
2. Crear nuevo webhook para tu workspace
3. Copiar webhook URL
4. Añadir a GitHub Secrets: `SLACK_WEBHOOK`

**Modificar workflow para notificar:**

**Prompt para IA:**

```
Añade notificaciones a Slack en mi workflow de GitHub Actions:

WORKFLOW ACTUAL:
[pegar ci.yml]

NOTIFICAR:
- ✅ Deploy exitoso a production
- ❌ Tests fallaron
- ❌ Deploy falló

USAR:
- Slack webhook en secret SLACK_WEBHOOK
- Mensajes concisos con emojis
- Incluir link al workflow run

Output: Steps para añadir al workflow
```

**Implementar** output de IA y probar.

---

## Fase 6: Script de Rollback (20 minutos)

### 6.1 Generar Script con IA

**Prompt:**

```
Genera un script de rollback para mi API en Railway:

REQUISITOS:
1. Detectar última versión estable (git tag v*.*.*)
2. Checkout a esa versión
3. Deploy a Railway
4. Verificar con health check (/health)
5. Notificar resultado (echo en consola)

CONTEXTO:
- Repository usa tags: v1.0.0, v1.1.0, v1.2.0, etc.
- Railway project: api-tareas-prod
- Health check: curl https://tu-api.railway.app/health
- RAILWAY_TOKEN en variable de entorno

Output: Script bash (rollback.sh) production-ready con error handling
```

---

### 6.2 Implementar y Probar

1. Guardar output como `scripts/rollback.sh`
2. Dar permisos de ejecución:
   ```bash
   chmod +x scripts/rollback.sh
   ```

3. **Simular incidente**:
   ```bash
   # 1. Crear tag actual (versión estable)
   git tag v1.0.0
   git push origin v1.0.0

   # 2. Hacer cambio que "rompe" la API
   echo "# Bug introducido" >> api/api.py
   git add api/api.py
   git commit -m "fix: intentando arreglar algo (introduce bug)"
   git push origin main

   # 3. Tag nueva versión (con bug)
   git tag v1.1.0
   git push origin v1.1.0

   # 4. Ejecutar rollback
   export RAILWAY_TOKEN="tu_token"
   ./scripts/rollback.sh

   # 5. Verificar que volvió a v1.0.0
   git describe --tags
   # Debe mostrar: v1.0.0
   ```

4. **Checkpoint**: ✅ Script hace rollback exitosamente a versión anterior

---

## Fase 7: Documentación con IA (15 minutos)

### 7.1 Generar DEPLOYMENT.md

**Prompt:**

```
Genera documentación completa de deployment para mi API:

CONTEXTO:
- API FastAPI desplegada en Railway
- CI/CD con GitHub Actions
- Tests automáticos antes de deploy
- Health checks configurados
- Script de rollback disponible

DOCUMENTACIÓN DEBE INCLUIR:
1. Arquitectura del pipeline (diagrama ASCII)
2. Cómo hacer deploy manual
3. Cómo funciona el deploy automático
4. Cómo hacer rollback si algo falla
5. Troubleshooting común
6. Variables de entorno necesarias

AUDIENCIA: Desarrolladores del equipo que nunca han usado Railway

Output: DEPLOYMENT.md completo en español, tono profesional
```

**Implementar:**

1. Guardar output como `DEPLOYMENT.md`
2. Revisar y añadir detalles específicos de tu setup
3. Commit:
   ```bash
   git add DEPLOYMENT.md scripts/rollback.sh
   git commit -m "docs: add deployment documentation and rollback script"
   git push origin main
   ```

---

## Entregables Finales

Al terminar el ejercicio, debes tener:

### Archivos Nuevos

```
.
├── .github/
│   └── workflows/
│       └── ci.yml              # Workflow de CI/CD
├── api/
│   └── api.py                  # (modificado con /health)
├── scripts/
│   └── rollback.sh             # Script de rollback
├── Dockerfile                  # (optimizado)
├── DEPLOYMENT.md               # Documentación
└── README.md                   # (actualizado)
```

### Checklist de Validación

- [ ] **CI configurado**: Workflow ejecuta lint + tests en cada push/PR
- [ ] **CD configurado**: Deploy automático a Railway en push a main
- [ ] **Tests pasan**: Coverage ≥80%, todos los tests en verde
- [ ] **Dockerfile optimizado**: Build más rápido y/o imagen más pequeña
- [ ] **Health check**: Endpoint /health responde 200
- [ ] **Monitoring**: UptimeRobot o equivalente configurado
- [ ] **Rollback funcional**: Script hace rollback a versión anterior
- [ ] **Documentación**: DEPLOYMENT.md explica proceso completo
- [ ] **Usaste IA**: Al menos 5 prompts a IA durante el ejercicio

### Demo

**Graba un video corto (2-3 minutos) mostrando:**

1. Hacer un cambio en código
2. Push a GitHub
3. GitHub Actions ejecuta tests automáticamente
4. Deploy automático a Railway
5. Health check responde OK
6. Ejecutar rollback script

**Sube a**: Unlisted YouTube video y comparte link

---

## Reflexión Post-Ejercicio

**Responde estas preguntas:**

1. **Sin IA, ¿cuánto habrías tardado en este ejercicio?**
   - Estimación: ___ horas

2. **Con IA, ¿cuánto tardaste?**
   - Real: ___ horas
   - Ahorro: ___ horas (__%)

3. **¿Qué fue lo más útil que generó la IA?**
   - Ejemplo: "El workflow de GitHub Actions completo"

4. **¿Qué tuviste que ajustar manualmente?**
   - Ejemplo: "Paths de directorios, nombres de secrets"

5. **¿Qué aprendiste que no sabías antes?**
   - Ejemplo: "Multi-stage Docker builds, cache de pip en CI"

6. **¿Usarías este pipeline en un proyecto real?**
   - [ ] Sí, tal cual está
   - [ ] Sí, con algunas mejoras
   - [ ] No, necesita más trabajo

---

## Bonus: Desafíos Adicionales

Si terminaste rápido y quieres más:

### Desafío 1: Canary Deployment

**Implementar deploy canario:**
- 10% de tráfico a nueva versión
- Monitorear métricas por 5 minutos
- Si OK, aumentar a 100%

**Prompt para IA:**
```
¿Cómo implemento canary deployment en Railway?
Necesito: 10% tráfico a v2, 90% a v1, luego aumentar gradualmente.
```

---

### Desafío 2: Análisis de Métricas con IA

**Crear script que analiza métricas:**

```python
# scripts/analyze_metrics.py
import anthropic
import requests

# Fetch métricas de Railway API
metrics = fetch_metrics()

# Preguntar a IA si hay anomalías
response = analyze_with_claude(metrics)

print(response)
```

**Prompt para IA:**
```
Genera script Python que:
1. Obtiene métricas de Railway API (requests/seg, error rate, latency)
2. Las envía a Claude API
3. Claude analiza y detecta anomalías
4. Imprime reporte

Output: Script completo con manejo de errores
```

---

### Desafío 3: Auto-Scaling Based on Metrics

**Implementar auto-scaling:**
- Monitorear CPU usage cada 5 minutos
- Si CPU >80% por 3 mediciones consecutivas → escalar a más replicas
- Si CPU <30% por 10 minutos → bajar replicas

**Prompt para IA:**
```
¿Cómo implemento auto-scaling en Railway basado en CPU?
Railway API permite scaling via CLI: railway scale --replicas N
```

---

## Conclusión

**Has implementado un pipeline DevOps completo:**

✅ CI: Tests automáticos antes de cada merge
✅ CD: Deploy automático a producción
✅ Monitoring: Health checks y alertas
✅ Rollback: Script de emergencia para revertir
✅ Documentación: Proceso explicado para el equipo

**Y lo más importante**: Lo hiciste en 2-3 horas con ayuda de IA, en vez de 2-3 días leyendo documentación.

**Eso es el poder de AI DevOps.**

---

**Siguiente**: Clase 8 - Proyecto Final del Módulo 4 (integración de todo lo aprendido)

---

## Recursos

**GitHub Actions:**
- [Docs oficiales](https://docs.github.com/actions)
- [Marketplace de Actions](https://github.com/marketplace?type=actions)

**Railway:**
- [Docs de Railway](https://docs.railway.app)
- [Railway CLI](https://docs.railway.app/develop/cli)

**Prompts útiles** (guárdalos para reutilizar):
```
# Para workflows
"Genera GitHub Actions workflow que [objetivo]. Stack: [tecnologías]. Debe [requisitos]."

# Para debugging
"Mi workflow falla con: [error]. Logs: [logs]. ¿Cuál es el problema?"

# Para optimización
"Optimiza este Dockerfile: [contenido]. Objetivo: builds rápidos, imagen pequeña."
```

---

**¡Éxito con tu pipeline! 🚀**
