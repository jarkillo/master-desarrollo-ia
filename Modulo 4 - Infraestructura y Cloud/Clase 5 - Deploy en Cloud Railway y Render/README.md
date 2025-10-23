# Clase 5: Deploy en Cloud (Railway y Render)

**Módulo 4 - Infraestructura y Cloud**

---

## 📋 Tabla de Contenidos

1. [Objetivos de Aprendizaje](#objetivos-de-aprendizaje)
2. [Qué Aprendimos Antes](#qué-aprendimos-antes)
3. [Qué Vamos a Aprender Ahora](#qué-vamos-a-aprender-ahora)
4. [Arquitectura de la Aplicación](#arquitectura-de-la-aplicación)
5. [Deploy en Railway](#deploy-en-railway)
6. [Deploy en Render](#deploy-en-render)
7. [Environment Variables](#environment-variables)
8. [Troubleshooting con IA](#troubleshooting-con-ia)
9. [Testing](#testing)
10. [Recursos Adicionales](#recursos-adicionales)

---

## 🎯 Objetivos de Aprendizaje

Al completar esta clase, serás capaz de:

- ✅ Preparar una aplicación FastAPI para producción
- ✅ Configurar environment variables para diferentes entornos (dev/prod)
- ✅ Desplegar en Railway y Render
- ✅ Conectar a PostgreSQL en cloud
- ✅ Usar Docker en producción
- ✅ Implementar health checks
- ✅ **Usar IA para troubleshooting de deployment** (40% AI content)

---

## 📚 Qué Aprendimos Antes

### Clase 1: Del código local al entorno vivo
- Conceptos de deployment
- Diferencias local vs cloud

### Clase 2: Tu API en un contenedor
- Docker basics
- Dockerfile
- Contenedores

### Clase 3: Base de Datos con SQLAlchemy
- SQLAlchemy 2.0
- Modelos ORM
- Sesiones de BD

### Clase 4: Migraciones con Alembic
- Alembic migrations
- Versionado de schema
- Migraciones reversibles

---

## 🚀 Qué Vamos a Aprender Ahora

### 1. Configuración Dinámica (Pydantic Settings)

**Problema en Clase 4:**
```python
# ❌ Configuración hardcodeada
DATABASE_URL = "sqlite:///./tareas.db"
```

**Solución Clase 5:**
```python
# ✅ Configuración dinámica con environment variables
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./tareas.db"
    environment: Literal["dev", "staging", "prod"] = "dev"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
```

**Ventajas:**
- Mismo código para dev/staging/prod
- Configuración via environment variables
- Validación automática de tipos
- Valores por defecto seguros

---

### 2. Multi-Database Support (SQLite → PostgreSQL)

**Desarrollo (SQLite):**
```python
DATABASE_URL=sqlite:///./tareas.db
```

**Producción (PostgreSQL):**
```python
DATABASE_URL=postgresql://user:pass@host:port/database
```

**Código adapta automáticamente:**
```python
def get_engine_config():
    if settings.database_url.startswith("sqlite"):
        return {"poolclass": NullPool}  # SQLite
    else:
        return {
            "poolclass": QueuePool,  # PostgreSQL
            "pool_size": 5,
            "pool_pre_ping": True
        }
```

---

### 3. Health Checks para Cloud Platforms

**Railway y Render necesitan saber si tu app está viva:**

```python
@app.get("/health")
def health_check():
    """
    Health check completo: API + Base de datos.

    Retorna:
    - 200 OK: Todo funciona
    - 503 Service Unavailable: BD desconectada
    """
    db_health = check_database_health()

    if db_health["status"] == "error":
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": db_health}
        )

    return {"status": "healthy", "database": db_health}
```

---

### 4. CORS para Frontend Separado

Si tienes un frontend en otro dominio:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tu-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### 5. Logging en Producción

```python
import logging

logging.basicConfig(
    level=settings.log_level,  # INFO en prod, DEBUG en dev
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# En endpoints:
logger.info(f"Creando tarea: {tarea_data.nombre}")
logger.warning(f"Tarea {id} no encontrada")
logger.error(f"Error de base de datos: {str(e)}")
```

---

## 🏗️ Arquitectura de la Aplicación

```
Clase 5/
├── api/
│   ├── config.py           # ⭐ NUEVO: Pydantic Settings
│   ├── database.py         # ⭐ ADAPTADO: Multi-DB support
│   ├── api.py              # ⭐ MEJORADO: Health checks, CORS, logging
│   ├── models.py           # (Sin cambios)
│   ├── servicio_tareas.py  # (Sin cambios)
│   ├── repositorio_db.py   # (Sin cambios)
│   └── dependencias.py     # (Sin cambios)
│
├── infra/
│   └── .env.template       # Template de variables de entorno
│
├── Dockerfile              # ⭐ Multi-stage build optimizado
├── railway.toml            # ⭐ Config para Railway
├── render.yaml             # ⭐ Infrastructure-as-Code para Render
├── requirements.txt        # + pydantic-settings, psycopg2
│
├── AI_TROUBLESHOOTING.md   # ⭐ 40% AI content
├── README.md
└── GLOSARIO.md
```

---

## 🚂 Deploy en Railway

### Paso 1: Crear Cuenta en Railway

1. Ve a [railway.app](https://railway.app)
2. Sign up con GitHub
3. Verifica tu email

---

### Paso 2: Crear Nuevo Proyecto

1. Click en "New Project"
2. Selecciona "Deploy from GitHub repo"
3. Autoriza Railway a acceder a tu repositorio
4. Selecciona tu repo

---

### Paso 3: Agregar PostgreSQL

1. En tu proyecto, click "New Service"
2. Selecciona "Database" → "PostgreSQL"
3. Railway crea automáticamente la BD y expone `DATABASE_URL`

---

### Paso 4: Configurar Variables de Entorno

En el dashboard de Railway, ve a "Variables" y agrega:

```bash
ENVIRONMENT=prod
LOG_LEVEL=INFO
SECRET_KEY=tu-clave-secreta-generada-con-openssl-rand-hex-32
CORS_ORIGINS=["https://tu-frontend.com"]
```

**⚠️ Railway proporciona `DATABASE_URL` automáticamente, NO la agregues manualmente.**

---

### Paso 5: Deploy Automático

Railway detecta automáticamente:
- `Dockerfile` → Usa Docker build
- `railway.toml` → Lee configuración

**railway.toml** (ya incluido):
```toml
[build]
builder = "dockerfile"

[deploy]
startCommand = "uvicorn api.api:app --host 0.0.0.0 --port $PORT --workers 2"
healthcheckPath = "/health"
restartPolicyType = "on_failure"
```

¡Tu app se despliega automáticamente! 🎉

---

### Paso 6: Ejecutar Migraciones (si usas Alembic)

Si tu app usa Alembic, necesitas ejecutar migrations manualmente la primera vez:

**Opción 1: Desde Railway CLI**
```bash
railway login
railway link
railway run alembic upgrade head
```

**Opción 2: En el startCommand**
```toml
startCommand = "alembic upgrade head && uvicorn api.api:app --host 0.0.0.0 --port $PORT"
```

---

### Paso 7: Verificar Deployment

1. Railway te da una URL: `https://tu-app.up.railway.app`
2. Ve a `https://tu-app.up.railway.app/health`
3. Deberías ver:
   ```json
   {
     "status": "healthy",
     "api": "ok",
     "database": {"status": "ok"},
     "environment": "prod"
   }
   ```

---

## 🎨 Deploy en Render

### Paso 1: Crear Cuenta en Render

1. Ve a [render.com](https://render.com)
2. Sign up con GitHub
3. Verifica tu email

---

### Paso 2: Crear Blueprint (Infrastructure-as-Code)

Render usa `render.yaml` para definir TODA tu infraestructura:

**render.yaml** (ya incluido):
```yaml
services:
  # PostgreSQL Database
  - type: pserv
    name: tareas-db
    env: docker
    plan: free
    databaseName: tareas_db

  # Web Service
  - type: web
    name: tareas-api
    env: docker
    plan: free
    dockerfilePath: ./Dockerfile
    healthCheckPath: /health

    envVars:
      - key: ENVIRONMENT
        value: prod

      - key: DATABASE_URL
        fromDatabase:
          name: tareas-db
          property: connectionString

      - key: SECRET_KEY
        generateValue: true
```

---

### Paso 3: Deploy desde GitHub

1. En Render, click "New" → "Blueprint"
2. Conecta tu repositorio de GitHub
3. Render detecta `render.yaml` automáticamente
4. Click "Apply"

Render crea:
- PostgreSQL database
- Web service
- Conecta automáticamente con `DATABASE_URL`

---

### Paso 4: Verificar Deployment

1. Render te da una URL: `https://tu-app.onrender.com`
2. Ve a `https://tu-app.onrender.com/health`

**⚠️ IMPORTANTE:** Render free tier pone tu app en sleep después de 15min de inactividad. La primera request puede tardar ~30s.

---

### Paso 5: Ejecutar Migraciones

**En render.yaml**, agrega un Build Command:

```yaml
buildCommand: "pip install -r requirements.txt && alembic upgrade head"
```

O crea un script:

**start.sh:**
```bash
#!/bin/bash
alembic upgrade head
uvicorn api.api:app --host 0.0.0.0 --port $PORT --workers 2
```

**render.yaml:**
```yaml
startCommand: "bash start.sh"
```

---

## 🔐 Environment Variables

### Development (.env local)

```bash
ENVIRONMENT=dev
DATABASE_URL=sqlite:///./tareas.db
LOG_LEVEL=DEBUG
CORS_ORIGINS=["*"]
SECRET_KEY=dev-secret-not-for-production
```

### Production (Railway/Render)

```bash
ENVIRONMENT=prod
DATABASE_URL=postgresql://user:pass@host/database  # Auto-provisto
LOG_LEVEL=INFO
CORS_ORIGINS=["https://tu-frontend.com"]
SECRET_KEY=<generar con openssl rand -hex 32>
```

### Generar SECRET_KEY Segura

```bash
openssl rand -hex 32
# Output: a1b2c3d4e5f6...
```

---

## 🤖 Troubleshooting con IA (40% AI Content)

**Ver documento completo:** [`AI_TROUBLESHOOTING.md`](./AI_TROUBLESHOOTING.md)

### Errores Comunes y Cómo Pedir Ayuda a la IA

#### Error 1: "ModuleNotFoundError"

**Prompt efectivo:**
```
Mi FastAPI app funciona localmente pero en Railway obtengo:

  ModuleNotFoundError: No module named 'api.config'

Dockerfile:
  [pega tu Dockerfile]

Estructura de archivos:
  api/
    config.py
    api.py

¿Qué falta?
```

---

#### Error 2: Database Connection Refused

**Prompt efectivo:**
```
Deploy en Railway con PostgreSQL.

Error:
  sqlalchemy.exc.OperationalError: could not connect to server

Variables de entorno:
  DATABASE_URL = postgresql://...

database.py:
  [pega código]

¿Qué reviso?
```

---

#### Error 3: Health Check Failed

**Prompt efectivo:**
```
Railway build exitoso pero health check falla.

Logs:
  ✅ Building...
  ❌ Health check failed after 5 minutes

railway.toml:
  healthcheckPath = "/health"

api.py:
  @app.get("/health")
  def health():
      check_database_health()  # Tarda >30s

¿Por qué falla?
```

**Solución (IA te dirá):** Health checks deben ser ultra-rápidos (<5s). Mueve queries pesadas a `/health/full`.

---

### Template de Prompt para Troubleshooting

```markdown
# CONTEXTO
- Plataforma: Railway / Render
- Tecnología: FastAPI + SQLAlchemy + PostgreSQL
- Database: PostgreSQL 15

# PROBLEMA
[Descripción del error]

# ERROR EXACTO
```
[Stack trace completo]
```

# CÓDIGO RELEVANTE
```python
[Pega código: api.py, database.py, Dockerfile]
```

# CONFIGURACIÓN
- Variables de entorno: [Lista]
- railway.toml / render.yaml: [Pega config]

# QUÉ INTENTÉ
1. [Acción 1]
2. [Acción 2]

# PREGUNTA
¿[Tu pregunta específica]?
```

---

## 🧪 Testing

### Ejecutar Tests Localmente

```bash
# Activar entorno virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Tests unitarios
pytest tests/ -v

# Tests de integración
pytest tests_integrations/ -v

# Todos los tests con coverage
pytest --cov=api --cov-report=term-missing --cov-fail-under=80
```

---

### Tests Específicos de Clase 5

```python
# test_api_clase5.py

def test_root_endpoint(client):
    """Health check básico"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_health_check_endpoint(client):
    """Health check completo (API + BD)"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["database"]["status"] == "ok"

def test_cors_headers_present(client):
    """CORS headers configurados"""
    response = client.get("/tareas", headers={"Origin": "https://example.com"})
    assert "access-control-allow-origin" in response.headers
```

---

## 📦 Docker Local Testing

Antes de deployar, prueba localmente con Docker:

```bash
# Build image
docker build -t tareas-api-clase5 .

# Run container
docker run -p 8000:8000 -e ENVIRONMENT=dev tareas-api-clase5

# Test
curl http://localhost:8000/health
```

---

## 🔧 Comparación: Railway vs Render

| Feature | Railway | Render |
|---------|---------|--------|
| **Free tier** | $5 crédito/mes | Free con limitaciones |
| **Sleep** | No | Sí (15min inactividad) |
| **PostgreSQL** | Sí (incluido) | Sí (incluido) |
| **Config** | railway.toml | render.yaml (IaC) |
| **CLI** | Excelente | Limitado |
| **Logs** | Tiempo real | Tiempo real |
| **Deployment** | Push to GitHub | Push to GitHub |
| **Custom domains** | Sí | Sí |
| **Environment vars** | Dashboard + CLI | Dashboard + render.yaml |

**Recomendación:**
- **Railway**: Mejor DX, no sleep, excelente CLI
- **Render**: Más generous free tier, IaC completo

---

## 📚 Recursos Adicionales

### Documentación Oficial

- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

### Troubleshooting con IA

- [AI_TROUBLESHOOTING.md](./AI_TROUBLESHOOTING.md) - Guía completa (40% AI content)
- [Claude Code](https://claude.ai/code) - AI assistant para debugging
- [GitHub Copilot](https://github.com/features/copilot) - Sugerencias inline

### Seguridad

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Security Best Practices](https://cheatsheetseries.owasp.org/)

---

## 🎓 Ejercicios Propuestos

### Ejercicio 1: Deploy Completo

1. Despliega la app en Railway
2. Conecta PostgreSQL
3. Configura environment variables
4. Ejecuta migrations
5. Verifica health checks
6. Consume la API desde Postman/curl

### Ejercicio 2: Troubleshoot con IA

1. Introduce un error intencional (ej: quita `DATABASE_URL`)
2. Deploy y observa el error
3. Usa Claude/ChatGPT para diagnosticar
4. Documenta el proceso en tu "Playbook de Errores"

### Ejercicio 3: Frontend + Backend

1. Crea un simple frontend (HTML/JS o React)
2. Despliega frontend en Vercel/Netlify
3. Configura CORS correctamente
4. Consume tu API desplegada en Railway

---

## ✅ Checklist de Deployment

Antes de considerar el deployment completo, verifica:

- [ ] App funciona localmente con Docker
- [ ] Tests pasan (pytest con coverage >80%)
- [ ] Health checks funcionan (`/` y `/health`)
- [ ] Environment variables configuradas
- [ ] PostgreSQL conectado
- [ ] Migrations ejecutadas
- [ ] CORS configurado si tienes frontend
- [ ] Logs no exponen secrets
- [ ] SECRET_KEY es fuerte (no "change-me")
- [ ] API responde en la URL pública
- [ ] Documentación API accesible (si no es prod)

---

## 🎯 Conclusión

**Has aprendido:**

✅ Configuración dinámica con Pydantic Settings
✅ Multi-database support (SQLite → PostgreSQL)
✅ Docker multi-stage builds optimizados
✅ Health checks para cloud platforms
✅ CORS para frontends separados
✅ Logging apropiado para producción
✅ Deploy en Railway y Render
✅ **Troubleshooting con IA (40% AI content)**

**Próxima clase:**
- **Clase 6**: CI/CD con GitHub Actions
- **Clase 7**: Monitoring y Observabilidad con Sentry
- **Clase 8**: Escalabilidad y Performance

---

**¿Dudas? ¿Errores? ¡Usa IA para troubleshooting!** Revisa [`AI_TROUBLESHOOTING.md`](./AI_TROUBLESHOOTING.md) para aprender cómo.
