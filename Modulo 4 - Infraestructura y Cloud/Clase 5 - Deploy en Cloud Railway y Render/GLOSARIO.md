# Glosario - Clase 5: Deploy en Cloud

**Términos y conceptos de deployment en cloud (Railway y Render)**

---

## A

### **Alembic**
Sistema de migraciones de base de datos para SQLAlchemy. Permite versionar cambios en el schema de la BD y aplicarlos/revertirlos de forma controlada.

```bash
# Crear migración
alembic revision -m "agregar campo email"

# Aplicar migraciones
alembic upgrade head
```

---

## B

### **Blueprint (Render)**
Archivo YAML (`render.yaml`) que define toda tu infraestructura como código (Infrastructure-as-Code). Incluye servicios, bases de datos, environment variables, etc.

```yaml
services:
  - type: web
    name: mi-api
  - type: pserv
    name: mi-bd
```

---

### **Build Stage (Docker)**
En un Dockerfile multi-stage, la etapa donde se instalan dependencias de build (gcc, compiladores). Estos no se incluyen en la imagen final, reduciendo el tamaño.

```dockerfile
# Stage 1: Builder
FROM python:3.12-slim as builder
RUN apt-get install gcc  # Solo en build

# Stage 2: Runtime
FROM python:3.12-slim
COPY --from=builder ...  # Copia solo lo necesario
```

---

## C

### **CORS (Cross-Origin Resource Sharing)**
Mecanismo de seguridad que permite a un frontend en un dominio (ej: `https://frontend.com`) consumir una API en otro dominio (ej: `https://api.com`).

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Analogía:** Es como un guardia de seguridad que verifica que tu sitio web tenga permiso para hablar con la API.

---

### **Connection Pool**
Conjunto de conexiones reutilizables a la base de datos. En lugar de abrir/cerrar conexión en cada request (lento), se mantienen conexiones activas en un "pool".

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=5,        # 5 conexiones simultáneas
    max_overflow=10     # +10 si se necesitan
)
```

**Analogía:** Como tener 5 cajas abiertas en el supermercado en lugar de abrir/cerrar una por cada cliente.

---

## D

### **DATABASE_URL**
Variable de entorno que contiene la URL de conexión a la base de datos.

```bash
# SQLite (desarrollo)
DATABASE_URL=sqlite:///./tareas.db

# PostgreSQL (producción)
DATABASE_URL=postgresql://user:pass@host:5432/database
```

Railway y Render proporcionan esta variable automáticamente cuando agregas PostgreSQL.

---

### **Deployment**
Proceso de llevar tu aplicación desde tu máquina local a un servidor en internet donde usuarios reales puedan acceder.

**Analogía:** Como llevar tu comida casera a un restaurante para que otros puedan comerla.

---

### **Docker Multi-Stage Build**
Técnica de Dockerfile que usa múltiples `FROM` statements para separar el build del runtime, reduciendo el tamaño de la imagen final.

```dockerfile
# Stage 1: Instalar dependencias (pesado)
FROM python:3.12 as builder
RUN pip install ...

# Stage 2: Runtime (ligero)
FROM python:3.12-slim
COPY --from=builder ~/.local /home/appuser/.local
```

**Ventaja:** Imagen final de ~150MB vs ~1GB sin multi-stage.

---

## E

### **Environment (Entorno)**
Contexto donde corre tu aplicación: `dev` (desarrollo), `staging` (pre-producción), `prod` (producción). Cada uno tiene configuración diferente.

```python
class Settings(BaseSettings):
    environment: Literal["dev", "staging", "prod"] = "dev"
```

---

### **Environment Variables**
Variables configuradas fuera del código que permiten cambiar comportamiento sin modificar código.

```python
# En código
database_url: str = Field(..., env="DATABASE_URL")

# En entorno
DATABASE_URL=postgresql://...
```

**Analogía:** Como los settings de tu celular (brillo, volumen) que cambias sin reprogramar el teléfono.

---

## H

### **Health Check**
Endpoint que verifica que tu aplicación está funcionando correctamente. Usado por load balancers y plataformas cloud.

```python
@app.get("/health")
def health_check():
    # Verifica BD, conexiones, etc.
    return {"status": "healthy"}
```

Railway y Render llaman este endpoint periódicamente. Si falla, reinician tu app.

**Analogía:** Como cuando el doctor te pregunta "¿cómo te sientes?" - un chequeo rápido.

---

### **Healthcheck Timeout**
Tiempo máximo que Railway/Render espera respuesta del health check antes de considerar la app "muerta".

```toml
# railway.toml
healthcheckTimeout = 100  # segundos
```

**Importante:** Health checks deben responder en <5s. Si tu check hace queries pesadas (>30s), el timeout falla.

---

## I

### **Infrastructure-as-Code (IaC)**
Definir tu infraestructura (servidores, BDs, redes) en archivos de configuración en lugar de clicks en una interfaz web.

```yaml
# render.yaml define TODA tu infraestructura
services:
  - type: web
    name: api
  - type: pserv
    name: database
```

**Ventaja:** Reproducible, versionado con Git, fácil de replicar.

---

## L

### **Lifespan Event (FastAPI)**
Función que ejecuta código al iniciar y cerrar la aplicación.

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP: Código antes de recibir requests
    print("Iniciando...")
    yield
    # SHUTDOWN: Código al cerrar app
    print("Cerrando...")

app = FastAPI(lifespan=lifespan)
```

**Uso típico:** Crear tablas, conectar a BD, cargar configuración.

---

### **Logging**
Sistema para registrar eventos de tu aplicación (info, warnings, errors).

```python
import logging

logger = logging.getLogger(__name__)
logger.info("App iniciada")
logger.warning("Tarea no encontrada")
logger.error("Error de BD")
```

**Importante en producción:** Los `print()` no son suficientes. Usa logging con niveles.

---

## M

### **Migration (Migración)**
Cambio versionado en el schema de la base de datos.

```python
# Alembic migration
def upgrade():
    op.add_column('tareas', sa.Column('email', sa.String(100)))

def downgrade():
    op.drop_column('tareas', 'email')
```

**Analogía:** Como las actualizaciones de una app móvil - cada versión tiene cambios específicos y reversibles.

---

## N

### **Non-Root User (Docker)**
Práctica de seguridad: NO correr aplicaciones como usuario `root` en containers.

```dockerfile
# Crear usuario non-root
RUN useradd -m appuser
USER appuser

# Ahora los comandos corren como appuser, no root
```

**Por qué:** Si alguien hackea tu app, no tiene permisos de root en el container.

---

## P

### **Platform-as-a-Service (PaaS)**
Servicio cloud que gestiona servidores, networking, escalado por ti. Solo subes tu código.

**Ejemplos:** Railway, Render, Heroku, Fly.io

**Ventaja vs IaaS (AWS EC2):** No necesitas configurar servidores manualmente.

**Analogía:** PaaS es Uber (solo dices a dónde vas), IaaS es rentar un auto (tú manejas todo).

---

### **PostgreSQL**
Sistema de base de datos relacional open-source, robusto y popular. Usado en producción por su confiabilidad.

**SQLite vs PostgreSQL:**
- SQLite: Archivo local, perfecto para desarrollo
- PostgreSQL: Servidor remoto, perfecto para producción

---

### **Pydantic Settings**
Librería para gestionar configuración de aplicaciones usando Pydantic.

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()  # Lee desde .env o environment variables
```

**Ventaja:** Validación de tipos automática, valores por defecto, fácil testing.

---

## R

### **Railway**
Platform-as-a-Service (PaaS) para deployar aplicaciones. Soporta Docker, PostgreSQL, Redis, etc.

**Características:**
- Deploy automático desde GitHub
- PostgreSQL incluido
- No sleep (vs Render free tier)
- CLI excelente

**Pricing:** $5 crédito/mes gratis, luego pay-as-you-go.

---

### **Render**
Platform-as-a-Service similar a Railway.

**Características:**
- Free tier (con sleep después de 15min)
- Infrastructure-as-Code (render.yaml)
- PostgreSQL incluido
- SSL automático

**Free tier:** App duerme después de 15min inactividad, primer request tarda ~30s.

---

### **Restart Policy**
Política de reinicio cuando tu app falla.

```toml
# railway.toml
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 10
```

**Tipos:**
- `on_failure`: Reinicia si falla
- `always`: Reinicia siempre (incluso si termina exitosamente)
- `never`: No reinicia

---

## S

### **Secret Management**
Gestión segura de información sensible (passwords, API keys, tokens).

**❌ MAL:**
```python
SECRET_KEY = "hardcoded-password-123"  # ¡Nunca hagas esto!
```

**✅ BIEN:**
```python
SECRET_KEY = os.environ["SECRET_KEY"]  # Desde environment variable
```

**Mejores prácticas:**
- Nunca hardcodear secrets en código
- Usar environment variables
- Generar keys fuertes: `openssl rand -hex 32`
- No commitear `.env` a Git

---

### **Sleep (Render Free Tier)**
En Render free tier, tu app "duerme" después de 15 minutos sin actividad. La primera request la "despierta" (tarda ~30s).

**Cómo evitarlo:**
- Upgrade a plan pago
- Usar un servicio de ping (ej: UptimeRobot) para mantenerla despierta
- Usar Railway (no tiene sleep)

---

### **SQLAlchemy Pool Pre-Ping**
Configura SQLAlchemy para verificar conexiones antes de usarlas.

```python
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  # Verifica conexión antes de usar
)
```

**Por qué:** Bases de datos pueden cerrar conexiones inactivas. Pre-ping detecta esto y reconecta automáticamente.

---

## T

### **Troubleshooting**
Proceso de diagnosticar y resolver errores en tu aplicación.

**En Clase 5:** Usamos IA (Claude, ChatGPT) para troubleshooting efectivo:

1. Proporcionas contexto completo (logs, config, error)
2. IA analiza y sugiere diagnóstico
3. Iteras hasta resolver

Ver: [`AI_TROUBLESHOOTING.md`](./AI_TROUBLESHOOTING.md)

---

## U

### **Uvicorn Workers**
Procesos separados de Uvicorn que manejan requests concurrentemente.

```bash
uvicorn api.api:app --workers 2
```

**1 worker:** Maneja 1 request a la vez
**2 workers:** Maneja 2 requests simultáneos

**Regla general:** `workers = (2 * cores) + 1`

En Railway/Render free tier: 2 workers es suficiente.

---

## V

### **Validación de Environment Variables**
Verificar que todas las variables necesarias están configuradas.

```python
# Con Pydantic Settings
class Settings(BaseSettings):
    database_url: str  # Campo requerido
    secret_key: str = "default"  # Campo opcional con default
```

Si falta `database_url`, Pydantic lanza error al iniciar (fail-fast).

---

## W

### **Workers (Uvicorn)**
Ver **Uvicorn Workers**.

---

## Y

### **YAML**
Lenguaje de serialización de datos usado para archivos de configuración.

```yaml
# render.yaml
services:
  - type: web
    name: mi-api
    envVars:
      - key: ENVIRONMENT
        value: prod
```

**Sintaxis:**
- Indentación con espacios (NO tabs)
- Key-value pairs: `key: value`
- Listas: `- item`

---

## Z

### **Zero-Downtime Deployment**
Deploy donde tu app nunca está offline. Railway y Render lo hacen automáticamente:

1. Build nueva versión
2. Start nueva versión
3. Redirect tráfico a nueva versión
4. Shutdown versión vieja

**Analogía:** Como cambiar una llanta mientras el auto sigue andando.

---

## 🤖 AI-Specific Terms

### **Prompt Engineering (para Troubleshooting)**
Arte de formular prompts efectivos para obtener ayuda útil de IA.

**❌ Prompt malo:**
```
Mi app no funciona, ayuda.
```

**✅ Prompt bueno:**
```
Mi FastAPI app en Railway falla con:
  ModuleNotFoundError: No module named 'api.config'

Dockerfile: [pega código]
Estructura: [lista archivos]
Logs: [pega logs]

¿Qué puede estar mal?
```

---

### **Iteración con IA**
Proceso de refinar soluciones mediante conversación con IA, no preguntas aisladas.

```
Usuario: Error X
IA: ¿Configuraste Y?
Usuario: Sí, con valor Z
IA: Ese es el problema, debería ser W
Usuario: ¡Funcionó! ¿Por qué?
IA: [Explica el patrón]
```

---

### **AI Copilot**
IA que te asiste en tiempo real mientras codeas (ej: GitHub Copilot, Claude Code).

**Uso en deployment:** Diagnóstico de errores, sugerencias de config, explicaciones de logs.

---

## 📚 Referencias

- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
