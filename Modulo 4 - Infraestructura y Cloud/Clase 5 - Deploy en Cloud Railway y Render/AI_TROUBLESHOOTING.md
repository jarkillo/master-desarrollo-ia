# 🤖 AI-Assisted Troubleshooting para Deploy en Cloud

**40% de contenido AI** - Cómo usar IA para diagnosticar y resolver problemas de deployment

---

## 📚 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Filosofía de Troubleshooting con IA](#filosofía-de-troubleshooting-con-ia)
3. [Errores Comunes y Cómo usar IA para Resolverlos](#errores-comunes-y-cómo-usar-ia-para-resolverlos)
4. [Prompt Engineering para Troubleshooting](#prompt-engineering-para-troubleshooting)
5. [Casos de Uso Reales](#casos-de-uso-reales)
6. [Herramientas Recomendadas](#herramientas-recomendadas)
7. [Mejores Prácticas](#mejores-prácticas)

---

## 🎯 Introducción

Cuando despliegas una aplicación en producción (Railway, Render, AWS, etc.), es inevitable encontrar errores que no aparecían en desarrollo. La IA puede ser tu **copiloto de debugging** si sabes cómo comunicarte con ella.

**Este documento te enseña:**
- Cómo estructurar prompts efectivos para troubleshooting
- Qué información proporcionar a la IA para diagnósticos precisos
- Patrones de errores comunes en cloud deployments
- Cómo iterar con la IA hasta resolver el problema

---

## 💡 Filosofía de Troubleshooting con IA

### Principio 1: La IA no es mágica, necesita contexto

❌ **Prompt malo:**
```
Mi app no funciona, ayuda.
```

✅ **Prompt bueno:**
```
Desplegué mi FastAPI app en Railway. La app se construye correctamente
pero falla al iniciar con el error:

  ModuleNotFoundError: No module named 'pydantic_settings'

Mi Dockerfile usa python:3.12-slim y mi requirements.txt incluye:
  pydantic-settings==2.7.1

Logs de Railway:
  [build output aquí]
  [runtime error aquí]

¿Qué puede estar causando esto?
```

**Contexto esencial:**
1. **Plataforma**: Railway, Render, AWS, local Docker?
2. **Error exacto**: Copia todo el stack trace o mensaje de error
3. **Logs completos**: Build logs + Runtime logs
4. **Configuración**: Dockerfile, render.yaml, variables de entorno
5. **Qué intentaste**: Cambios que hiciste sin éxito

---

### Principio 2: Itera en conversación, no "one-shot"

El troubleshooting con IA es una **conversación**, no una pregunta única.

**Flujo típico:**

1. **Pregunta inicial**: Describes el problema con contexto
2. **IA responde**: Te hace preguntas aclaratorias o propone hipótesis
3. **Proporcionas más info**: Logs adicionales, configuración
4. **IA diagnostica**: Identifica la causa raíz
5. **Implementas fix**: Aplicas la solución sugerida
6. **Reportas resultado**: Si funciona, ¡genial! Si no, la IA itera

**Ejemplo de iteración:**

```
Usuario: Mi app de FastAPI en Railway no se conecta a PostgreSQL.
         Error: connection refused

IA: ¿Configuraste la variable DATABASE_URL? ¿Qué valor tiene?

Usuario: Sí, use: postgresql://user:pass@localhost:5432/db

IA: ❌ Ahí está el problema. 'localhost' dentro del container de
    Railway no apunta a tu PostgreSQL. Railway proporciona DATABASE_URL
    automáticamente. Usa:

    DATABASE_URL = os.environ["DATABASE_URL"]

    O en Pydantic Settings:
    database_url: str = Field(..., env="DATABASE_URL")

Usuario: ¡Funcionó! Gracias.
```

---

### Principio 3: Aprende patrones, no solo fixes

Cuando la IA te ayuda a resolver un error, **analiza el patrón** para no repetirlo.

**Pregunta de seguimiento efectiva:**

```
Esto funcionó. ¿Puedes explicarme POR QUÉ falló y cuál es el patrón
general que debo recordar para evitarlo en el futuro?
```

---

## 🐛 Errores Comunes y Cómo usar IA para Resolverlos

### Error 1: "ModuleNotFoundError" en producción (funciona en local)

**Síntoma:** La app funciona en tu máquina pero falla en Railway/Render.

**Prompt para IA:**

```
Mi FastAPI app funciona localmente pero en Railway obtengo:

  ModuleNotFoundError: No module named 'api.config'

Estructura de archivos:
  api/
    __init__.py
    config.py
    api.py
    database.py

Dockerfile:
  [pega tu Dockerfile aquí]

¿Qué está mal?
```

**Solución típica (IA te guiará):**
- Falta copiar el directorio `api/` al Dockerfile
- `WORKDIR` mal configurado
- Imports relativos vs absolutos

---

### Error 2: "Address already in use" o puerto incorrecto

**Síntoma:** Railway/Render asigna puertos dinámicamente, tu app usa puerto fijo.

**Prompt para IA:**

```
Mi app FastAPI en Render muestra:

  [ERROR] Failed to bind to address 0.0.0.0:8000

Mi comando de inicio:
  uvicorn api.api:app --host 0.0.0.0 --port 8000

¿Cómo hago que use el puerto dinámico de Render?
```

**Solución (IA te dirá):**
```python
# Usar variable de entorno $PORT
uvicorn api.api:app --host 0.0.0.0 --port $PORT
```

```python
# O en código Python:
import os
port = int(os.environ.get("PORT", 8000))
```

---

### Error 3: Database connection refused (Railway/Render)

**Síntoma:** La app no puede conectarse a PostgreSQL.

**Prompt para IA:**

```
Deploy en Railway con PostgreSQL.

Error:
  sqlalchemy.exc.OperationalError: could not connect to server:
  Connection refused

Variables de entorno en Railway:
  DATABASE_URL = postgresql://postgres:***@[host]/railway
  ENVIRONMENT = prod

database.py:
  [pega tu código de database.py aquí]

¿Qué reviso?
```

**Checklist (IA te guiará):**
1. ¿Railway PostgreSQL está en el mismo proyecto?
2. ¿La variable `DATABASE_URL` está bien configurada?
3. ¿Tu app espera la variable correcta? (`DATABASE_URL` vs `database_url`)
4. ¿El engine de SQLAlchemy tiene `pool_pre_ping=True`?

---

### Error 4: Migrations no se ejecutan automáticamente

**Síntoma:** La app arranca pero las tablas no existen.

**Prompt para IA:**

```
Desplegué en Railway pero obtengo:

  ProgrammingError: relation "tareas" does not exist

Mi app usa Alembic. ¿Cómo ejecuto migrations en Railway automáticamente
al deployar?
```

**Solución (IA te propondrá):**

**Opción 1: Comando de inicio compuesto**
```bash
# railway.toml
startCommand = "alembic upgrade head && uvicorn api.api:app --host 0.0.0.0 --port $PORT"
```

**Opción 2: Script de inicio**
```bash
#!/bin/bash
# start.sh
alembic upgrade head
uvicorn api.api:app --host 0.0.0.0 --port $PORT --workers 2
```

---

### Error 5: "CORS policy blocked" en frontend

**Síntoma:** Tu frontend no puede consumir la API desplegada.

**Prompt para IA:**

```
Frontend en https://mi-app.vercel.app
Backend en https://mi-api.railway.app

Error en navegador:
  Access to XMLHttpRequest blocked by CORS policy

Mi código FastAPI:
  [pega tu configuración de CORS]

¿Qué está mal?
```

**Solución (IA te dirá):**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mi-app.vercel.app"],  # ← Específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📝 Prompt Engineering para Troubleshooting

### Template de Prompt Efectivo

```
# CONTEXTO
- Plataforma: [Railway / Render / AWS / etc.]
- Tecnología: [FastAPI / Django / Flask / etc.]
- Base de datos: [PostgreSQL / MySQL / SQLite / etc.]

# PROBLEMA
[Descripción clara del error o comportamiento inesperado]

# ERROR EXACTO
```
[Pega aquí el stack trace completo o mensaje de error]
```

# CÓDIGO RELEVANTE
```python
[Pega el código relacionado: api.py, database.py, Dockerfile, etc.]
```

# CONFIGURACIÓN
- Variables de entorno: [Lista las relevantes]
- Dockerfile / render.yaml: [Pega la configuración]

# QUÉ INTENTÉ
1. [Acción 1]
2. [Acción 2]
3. [Resultado]

# PREGUNTA ESPECÍFICA
¿[Tu pregunta concreta]?
```

---

### Ejemplos de Prompts Efectivos

#### Ejemplo 1: Debugging de performance

```
Mi API FastAPI en Railway responde lentamente (>5s por request).

Métricas:
- Requests/min: 20
- Database queries por request: ~15 (N+1 problem?)
- RAM usage: 200MB / 512MB available

Código del endpoint lento:
[pega código]

Modelo SQLAlchemy:
[pega modelos]

¿Cómo optimizo esto? ¿Es un problema de queries o de configuración de Railway?
```

#### Ejemplo 2: Environment variables no funcionan

```
Deploy en Render pero mis environment variables no se cargan.

render.yaml:
[pega config]

Código (api/config.py):
[pega Settings class]

Logs de Render:
  [ERROR] ValidationError: 1 validation error for Settings
  database_url
    field required (type=value_error.missing)

Pero SÍ configuré DATABASE_URL en el dashboard de Render.
¿Qué falta?
```

---

## 🔧 Casos de Uso Reales

### Caso 1: App buildea pero no inicia

**Contexto real:**
```
Build exitoso en Railway pero la app no inicia.

Logs:
  ✅ Building...
  ✅ Successfully built image
  ❌ Starting failed

  Error: Health check failed after 5 minutes
```

**Cómo la IA ayudó:**

**Prompt:**
```
Railway build exitoso pero health check falla.

railway.toml:
  healthcheckPath = "/health"
  healthcheckTimeout = 100

api.py:
  @app.get("/health")
  def health():
      check_database_health()  # ← Esto tarda >30s
      return {"status": "ok"}

¿Por qué falla el health check?
```

**Respuesta IA:**
```
El health check falla porque check_database_health() tarda más de 100s
(timeout de Railway).

Solución:
1. Simplifica el health check:
   @app.get("/health")
   def health():
       return {"status": "ok"}  # Sin query pesada

2. Crea un endpoint separado para full health:
   @app.get("/health/full")
   def health_full():
       return check_database_health()
```

**Lección:** Health checks deben ser **ultra-rápidos** (<5s). Checks complejos en endpoints separados.

---

### Caso 2: Secrets expuestos en logs

**Contexto real:**
```
Logs de Railway muestran mi DATABASE_URL completa con contraseña.

Logs:
  INFO: Connecting to postgresql://user:MySecretPass123@host/db
```

**Prompt:**
```
Mi app logea la DATABASE_URL completa en Railway. ¿Cómo evito exponer secrets?

Código:
  logger.info(f"Connecting to {settings.database_url}")
```

**Respuesta IA:**
```
Nunca logees URLs de conexión completas. Sanitiza secrets:

# ❌ MAL
logger.info(f"Connecting to {settings.database_url}")

# ✅ BIEN
db_host = settings.database_url.split("@")[-1]
logger.info(f"Connecting to database at {db_host}")

O usa una función helper:
def sanitize_url(url: str) -> str:
    if "@" in url:
        protocol, rest = url.split("://")
        _, host = rest.split("@")
        return f"{protocol}://***@{host}"
    return url

logger.info(f"Connecting to {sanitize_url(settings.database_url)}")
```

---

## 🛠️ Herramientas Recomendadas

### 1. Claude Code (AI Assistant)

**Uso:** Debugging en tiempo real con contexto de tu codebase.

```
# Ejemplo
claude-code: "analiza mis logs de railway y sugiere fixes"
```

**Ventajas:**
- Acceso a tu código local
- Puede ejecutar comandos y tests
- Itera contigo en tiempo real

---

### 2. ChatGPT / Claude Web

**Uso:** Troubleshooting interactivo con logs largos.

**Tip:** Usa conversaciones largas para iterar, no preguntas aisladas.

---

### 3. GitHub Copilot Chat

**Uso:** Sugerencias inline mientras codeas fixes.

**Ejemplo:**
```python
# Copilot Chat: "Este endpoint es lento, optimiza con eager loading"
@app.get("/tareas")
def listar_tareas(db: Session = Depends(get_db)):
    # Copilot sugiere: .options(joinedload(Tarea.usuario))
    return db.query(TareaModel).options(joinedload(...)).all()
```

---

## ✅ Mejores Prácticas

### 1. Documenta el problema ANTES de preguntar a la IA

**Por qué:** Te obliga a organizar tus pensamientos y recopilar información.

**Plantilla:**
```markdown
## Problema
[Descripción]

## Comportamiento esperado
[Qué debería pasar]

## Comportamiento actual
[Qué pasa realmente]

## Pasos para reproducir
1. [Paso 1]
2. [Paso 2]

## Logs
```
[Logs]
```

## Código relevante
[Links o snippets]
```

---

### 2. Proporciona logs COMPLETOS, no fragmentos

❌ **Fragmento inútil:**
```
Error: Connection refused
```

✅ **Stack trace completo:**
```
Traceback (most recent call last):
  File "api/database.py", line 42, in get_db
    conn = engine.connect()
  File "sqlalchemy/engine/base.py", line 3325, in connect
    return self._connection_cls(self)
  ...
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError)
could not connect to server: Connection refused
    Is the server running on host "localhost" (127.0.0.1) and accepting
    TCP/IP connections on port 5432?
```

---

### 3. Itera, no esperes soluciones mágicas

**Mentalidad correcta:**
```
Intento 1: IA sugiere X → No funciona → Reporto resultado
Intento 2: IA sugiere Y → Funciona parcialmente → Pido refinar
Intento 3: IA sugiere Z → ¡Funciona! → Pido explicación del patrón
```

---

### 4. Aprende de cada solución

**Pregunta de cierre efectiva:**
```
Esto funcionó. Ahora explícame:
1. ¿POR QUÉ falló originalmente?
2. ¿Cuál es el patrón general que debo recordar?
3. ¿Cómo prevengo esto en el futuro?
```

---

### 5. Crea un "Playbook de Errores" personal

Cada vez que resuelves un error con IA, documenta:

```markdown
## Error: [Título]
**Síntoma:** [Qué viste]
**Causa:** [Raíz del problema]
**Solución:** [Fix aplicado]
**Prompt efectivo:** [Prompt que funcionó]
**Lección:** [Qué aprendiste]
```

---

## 🎓 Ejercicio Práctico

### Desafío: Resuelve este error con IA

**Escenario:**
```
Desplegaste tu API en Render. La app arranca pero todos los endpoints
devuelven 500.

Logs de Render:
  INFO: Started server process [1]
  INFO: Waiting for application startup.
  ERROR: Exception in lifespan handler
  Traceback (most recent call last):
    File "api/api.py", line 32, in lifespan
      crear_tablas()
    File "api/database.py", line 57, in crear_tablas
      Base.metadata.create_all(bind=engine)
    File "sqlalchemy/sql/schema.py", line 5347, in create_all
      ...
  sqlalchemy.exc.ProgrammingError: (psycopg2.errors.InsufficientPrivilege)
  permission denied for schema public

Variables de entorno:
  DATABASE_URL = postgresql://render_user:***@dpg-xxx.oregon-postgres.render.com/render_db
  ENVIRONMENT = prod
```

**Tu tarea:**
1. Escribe un prompt efectivo para Claude/ChatGPT
2. Itera con la IA hasta identificar el problema
3. Implementa la solución
4. Documenta el patrón aprendido

**Pista:** El problema está relacionado con permisos de PostgreSQL en Render.

---

## 📚 Recursos Adicionales

- [Railway Docs - Troubleshooting](https://docs.railway.app/guides/troubleshooting)
- [Render Docs - Debugging](https://render.com/docs/troubleshooting)
- [FastAPI Deployment Best Practices](https://fastapi.tiangolo.com/deployment/)
- [PostgreSQL Permission Issues](https://www.postgresql.org/docs/current/ddl-priv.html)

---

## 🎯 Conclusión

**La IA es tu mejor copiloto de troubleshooting si:**
1. ✅ Proporcionas contexto completo
2. ✅ Iteras en conversación
3. ✅ Aprendes patrones, no solo fixes
4. ✅ Documentas soluciones para el futuro

**Recuerda:** No se trata de encontrar la respuesta rápida, sino de **entender el problema profundamente** con ayuda de la IA.

---

**Este documento ES contenido educativo AI-first.** 🤖✨
