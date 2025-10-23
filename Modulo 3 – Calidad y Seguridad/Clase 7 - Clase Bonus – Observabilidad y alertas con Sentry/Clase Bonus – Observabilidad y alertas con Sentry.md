# 🎯 Clase Bonus – Observabilidad y alertas con Sentry: cuando tu API te habla

# 🧩 El problema

Tu API ya pasó por todas las fases:

- se defiende sola con tests y linters,
- protege sus puertas con claves y tokens,
- y revisa su propio código con auditorías automáticas.

Pero hay un escenario inevitable:

un **error real en producción**.

Una ruta que nadie probó, una conexión caída, un bug que aparece solo con cierto dato.

¿Cómo te enteras **antes de que lo descubra tu usuario**?

Ahí entra **Sentry**, el sistema nervioso de tu aplicación.

---

## 🧠 Concepto

**Sentry** es una plataforma de *observabilidad y monitoreo de errores*.

Actúa como un “sensor” que escucha todo lo que pasa dentro de tu aplicación, y cuando algo falla:

- captura la excepción completa,
- guarda el contexto (endpoint, usuario, request, commit),
- y te notifica automáticamente por Slack, Discord o email.

> Ya no tienes que revisar logs manualmente: los errores te encuentran a ti.
> 

---

## ⚙️ Aplicación manual – Cómo integrarlo en tu API

### 1. Crea una cuenta gratuita en sentry.io

Crea un nuevo proyecto → elige **Python / FastAPI**

Sentry te dará un **DSN** (una URL de conexión como esta):

```
https://1234567890abcdef.ingest.sentry.io/1234567
```

Guárdala **como secret** en GitHub:

```
Name: SENTRY_DSN
Value: https://1234567890abcdef.ingest.sentry.io/1234567
```

---

### 2. Instala la librería en tu entorno

```bash
pip install "sentry-sdk[fastapi]"

```

---

### 3. Inicializa Sentry en tu app

Edita `api/api.py` y añade esto **antes de crear el FastAPI()**:

```python
import sentry_sdk
import os

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,   # captura errores y rendimiento
)

```

Listo.

Cada error no controlado se enviará automáticamente a tu panel de Sentry con todos los detalles.

---

### 4. Prueba que funciona

Lanza tu API y crea una ruta que falle a propósito:

```python
@app.get("/error")
def generar_error():
    raise ValueError("Error intencional para probar Sentry")

```

Haz una petición a `/error`

y verás el registro aparecer en tu dashboard de Sentry en segundos.

---

## 🤖 Aplicación con IA – Security Hardening para Observabilidad

La integración de Sentry es **crítica para detectar errores**, pero también puede convertirse en una **vulnerabilidad de seguridad** si no se configura correctamente. La IA puede generar código funcional pero inseguro que exponga información sensible.

### 🎯 Concepto: Observabilidad Segura

La observabilidad (logs, métricas, traces) debe cumplir estos principios:

1. **Nunca loguees información sensible**: Passwords, tokens, API keys, PII, números de tarjeta
2. **Scrubbing automático**: Sentry debe filtrar campos sensibles antes de enviar
3. **Context mínimo necesario**: Solo envía la información necesaria para debugging
4. **DSN como secreto**: El DSN es una URL con credenciales, nunca en código
5. **Sample rate adecuado**: No enviar 100% del tráfico a Sentry (costo y exposición)

**Diferencia con logging tradicional**:
- **Logs locales**: Se quedan en tu servidor (controlados)
- **Sentry**: Se envía a un servidor externo (terceros)
- **Riesgo**: Si logueas passwords, van a los servidores de Sentry

---

### 🧪 Ejercicio Práctico: IA genera código Sentry inseguro, tú auditas

Este ejercicio te enseña a **auditar configuraciones de observabilidad** que la IA puede generar.

#### **Paso 1: Genera configuración Sentry con IA**

Usa este prompt con tu asistente IA:

```
Integra Sentry en una API FastAPI con estas características:
- Captura todos los errores automáticamente
- Incluye información del usuario autenticado en cada error
- Captura el body de las requests para debugging
- Añade contexto de headers y variables de entorno

Genera el código de inicialización de Sentry con el máximo detalle posible.
```

**⚠️ IMPORTANTE**: Este prompt está diseñado para que la IA genere código con vulnerabilidades de seguridad (exposición de datos sensibles).

#### **Paso 2: Audita el código generado**

La IA probablemente generó algo así:

```python
# ❌ CONFIGURACIÓN INSEGURA DE SENTRY (generada por IA)
import sentry_sdk
import os
from sentry_sdk.integrations.fastapi import FastApiIntegration
from fastapi import Request

def before_send(event, hint):
    # ⚠️ Añade información que puede ser sensible
    if 'request' in event:
        request = event['request']

        # ⚠️ Captura TODOS los headers (incluye Authorization, API keys)
        event['request']['headers'] = dict(request.get('headers', {}))

        # ⚠️ Captura el body completo (puede tener passwords)
        event['request']['data'] = request.get('data', {})

    # ⚠️ Añade TODAS las variables de entorno
    event['contexts']['environment'] = dict(os.environ)

    return event


sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),  # ✅ OK: DSN desde env var

    # ⚠️ Captura 100% del tráfico (costoso y expone mucha información)
    traces_sample_rate=1.0,

    integrations=[
        FastApiIntegration(
            # ⚠️ Captura automáticamente todos los requests
            auto_enable_request_body=True,
        )
    ],

    # ⚠️ Envía información del entorno
    environment=os.getenv("MODE", "production"),

    # ⚠️ Hook inseguro que expone datos sensibles
    before_send=before_send,
)


# En los endpoints
@app.post("/login")
async def login(request: Request, cuerpo: LoginRequest):
    # ⚠️ Si este endpoint falla, Sentry capturará el password del body
    usuario = authenticate(cuerpo.usuario, cuerpo.password)

    if not usuario:
        # ⚠️ El contexto incluirá el password en el body
        sentry_sdk.capture_message("Login failed", level="warning")
        raise HTTPException(status_code=401)

    return {"token": generate_token(usuario)}
```

#### **Paso 3: Identifica las vulnerabilidades**

Usa el **Sentry Security Checklist** (abajo) para auditar:

| ⚠️ Vulnerabilidad | Ubicación | Severidad | Impacto |
|------------------|-----------|-----------|---------|
| **Exposición de passwords** | `before_send` captura `request.data` sin filtrar | 🔴 Crítica | Los passwords de login se envían a Sentry en texto plano |
| **Exposición de tokens** | Captura todos los headers (incluye `Authorization`) | 🔴 Crítica | JWT tokens y API keys visibles en Sentry |
| **Exposición de secrets** | `event['contexts']['environment']` incluye TODO `os.environ` | 🔴 Crítica | `JWT_SECRET`, `API_KEY`, etc. enviadas a Sentry |
| **Sample rate 100%** | `traces_sample_rate=1.0` | 🟠 Alta | Costo elevado y exposición innecesaria de datos |
| **Body capturado automáticamente** | `auto_enable_request_body=True` | 🟠 Alta | Todos los POST/PUT/PATCH envían su body a Sentry |

#### **Paso 4: Corrige con Security Hardening Mentor**

Usa este prompt para que la IA te enseñe a corregir:

```
Actúa como Security Hardening Mentor especializado en Observabilidad.

Tengo esta configuración de Sentry [pega el código inseguro].

Para cada vulnerabilidad:
1. Explica POR QUÉ es peligrosa (ejemplo: qué información se filtra)
2. Muestra un ataque real (cómo un atacante explotaría esto)
3. Dame el código corregido con scrubbing y filtros
4. Enséñame el principio de seguridad (ej: "principle of least privilege")

Incluye configuración de:
- Scrubbing de campos sensibles
- Sample rate adecuado
- Filtros de PII
- Manejo seguro de contexto

Usa un tono educativo, no condescendiente.
```

**Código corregido** (que la IA debe generar):

```python
# ✅ CONFIGURACIÓN SEGURA DE SENTRY
import sentry_sdk
import os
import re
from sentry_sdk.integrations.fastapi import FastApiIntegration
from fastapi import Request

# ✅ Lista de campos sensibles que NUNCA deben enviarse
SENSITIVE_FIELDS = [
    'password', 'secret', 'token', 'api_key', 'authorization',
    'credit_card', 'ssn', 'dni', 'access_token', 'refresh_token',
    'jwt_secret', 'database_url', 'private_key'
]

def scrub_sensitive_data(data: dict) -> dict:
    """
    Remove sensitive fields from data before sending to Sentry.

    Uses a blocklist approach: any key matching SENSITIVE_FIELDS
    (case-insensitive, partial match) is replaced with [REDACTED].
    """
    if not isinstance(data, dict):
        return data

    scrubbed = {}
    for key, value in data.items():
        key_lower = key.lower()

        # ✅ Check if key contains any sensitive pattern
        is_sensitive = any(pattern in key_lower for pattern in SENSITIVE_FIELDS)

        if is_sensitive:
            scrubbed[key] = "[REDACTED]"  # Replace with placeholder
        elif isinstance(value, dict):
            scrubbed[key] = scrub_sensitive_data(value)  # Recursive
        elif isinstance(value, list):
            scrubbed[key] = [scrub_sensitive_data(item) if isinstance(item, dict) else item for item in value]
        else:
            scrubbed[key] = value

    return scrubbed


def before_send(event, hint):
    """
    Custom event processor to sanitize data before sending to Sentry.

    Security measures:
    1. Remove sensitive headers (Authorization, API keys)
    2. Scrub request body for passwords/secrets
    3. Never send environment variables
    4. Redact URL parameters with sensitive data
    """
    if 'request' in event:
        # ✅ HEADERS: Remove Authorization and sensitive headers
        if 'headers' in event['request']:
            headers = dict(event['request']['headers'])

            # Remove sensitive headers entirely
            sensitive_headers = ['authorization', 'x-api-key', 'cookie', 'x-csrf-token']
            for header in sensitive_headers:
                headers.pop(header, None)
                headers.pop(header.upper(), None)
                headers.pop(header.title(), None)

            event['request']['headers'] = headers

        # ✅ BODY: Scrub sensitive fields from request data
        if 'data' in event['request']:
            event['request']['data'] = scrub_sensitive_data(event['request']['data'])

        # ✅ URL: Redact sensitive query parameters
        if 'query_string' in event['request']:
            query = event['request']['query_string']
            # Example: ?token=abc123 -> ?token=[REDACTED]
            for field in SENSITIVE_FIELDS:
                query = re.sub(
                    f"{field}=[^&]*",
                    f"{field}=[REDACTED]",
                    query,
                    flags=re.IGNORECASE
                )
            event['request']['query_string'] = query

    # ✅ USER CONTEXT: Only include non-sensitive user info
    if 'user' in event:
        # Keep: user ID, username
        # Remove: email (PII), IP address (PII in EU)
        allowed_fields = {'id', 'username'}
        event['user'] = {k: v for k, v in event['user'].items() if k in allowed_fields}

    # ✅ CONTEXTS: Never send environment variables
    if 'contexts' in event:
        event['contexts'].pop('environment', None)  # Remove if accidentally added

    return event


# ✅ Initialize Sentry with security best practices
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),

    # ✅ Sample rate: Only 10% of successful transactions (reduce cost and exposure)
    # Always capture errors (100%), but not all traces
    traces_sample_rate=0.1,  # 10% of traces

    # ✅ Environment from env var (safe: only "dev", "staging", "production")
    environment=os.getenv("MODE", "production"),

    # ✅ Release tracking (helps identify which version has bugs)
    release=os.getenv("GIT_COMMIT", "unknown"),

    integrations=[
        FastApiIntegration(
            # ✅ DO NOT auto-capture request bodies (too risky)
            transaction_style="url",  # Use URL patterns for grouping
        )
    ],

    # ✅ Custom before_send hook to scrub sensitive data
    before_send=before_send,

    # ✅ Built-in PII scrubbing (Sentry feature)
    # This is a fallback, but always implement custom scrubbing too
    send_default_pii=False,  # Don't send PII by default

    # ✅ Max breadcrumbs (limit memory usage)
    max_breadcrumbs=50,
)


# ✅ Manually capture context when needed (explicit is better than implicit)
@app.post("/login")
async def login(cuerpo: LoginRequest):
    try:
        usuario = authenticate(cuerpo.usuario, cuerpo.password)

        if not usuario:
            # ✅ Capture event manually WITHOUT sensitive data
            with sentry_sdk.push_scope() as scope:
                # Add safe context
                scope.set_context("login_attempt", {
                    "username": cuerpo.usuario,  # OK: username not sensitive
                    # ❌ DON'T add: password, IP address, etc.
                })
                scope.set_level("warning")
                sentry_sdk.capture_message("Login failed - invalid credentials")

            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        return {"token": generate_token(usuario)}

    except Exception as e:
        # ✅ Sentry auto-captures exceptions, scrubbing applied
        raise
```

**Lecciones aprendidas**:

1. **Scrubbing is mandatory**: Never trust auto-capture features, always filter
2. **Blocklist approach**: Maintain a list of sensitive field patterns
3. **Sample rate trade-off**: 100% traces = high cost + more exposure, 10% is often enough
4. **Explicit context > Implicit**: Manually add context to avoid accidents
5. **Defense in depth**: Multiple layers (before_send + send_default_pii=False + manual scrubbing)

---

### 📋 Sentry Security Checklist

Usa esta checklist al auditar código de observabilidad generado por IA:

#### **🔴 Críticas (bloquean despliegue)**

- [ ] **DSN como secreto**: ¿El `SENTRY_DSN` está en `.env` o GitHub Secrets (NO en código)?
- [ ] **Scrubbing de passwords**: ¿El `before_send` filtra campos con "password", "secret", "token"?
- [ ] **No envía env vars**: ¿Se evita enviar `os.environ` completo a Sentry?
- [ ] **Headers sensibles filtrados**: ¿Se remueve `Authorization`, `X-API-Key`, `Cookie`?
- [ ] **Body de login no capturado**: ¿Los endpoints `/login`, `/register` NO envían el body a Sentry?

#### **🟠 Altas (corregir antes de merge)**

- [ ] **Sample rate < 100%**: ¿`traces_sample_rate` está en 0.1-0.3 (no 1.0)?
- [ ] **PII scrubbing habilitado**: ¿`send_default_pii=False` configurado?
- [ ] **URL parameters scrubbed**: ¿Query strings con tokens son redactadas?
- [ ] **User context mínimo**: ¿Solo se envía `user.id` y `user.username` (no email, IP)?
- [ ] **Request body deshabilitado**: ¿`auto_enable_request_body=False` en FastApiIntegration?

#### **🟡 Medias (mejorar en refactor)**

- [ ] **Filtrado por entorno**: ¿Sentry solo está activo en staging/production (no dev local)?
- [ ] **Release tracking**: ¿Se configura `release=` con el commit hash para trazabilidad?
- [ ] **Custom grouping**: ¿Se usa `fingerprint` para agrupar errores similares?
- [ ] **Breadcrumbs limitados**: ¿`max_breadcrumbs` configurado (default 100 puede ser excesivo)?
- [ ] **Documentación**: ¿README explica qué información se envía a Sentry?

#### **🟢 Extras (producción profesional)**

- [ ] **Alert rules configuradas**: ¿Sentry notifica a Slack/Discord cuando hay errores críticos?
- [ ] **Error budget**: ¿Se monitorean las tasas de error (ej: < 1% de requests)?
- [ ] **Performance monitoring**: ¿Se capturan métricas de endpoints lentos?
- [ ] **Issue ownership**: ¿Los errores se asignan automáticamente a equipos responsables?
- [ ] **Data retention policies**: ¿Se elimina data sensible después de 30 días?

---

### 🎓 Prompt Avanzado: Security Hardening Mentor para Sentry

Usa este prompt para crear tu mentor de seguridad especializado en observabilidad:

```
Actúa como Security Hardening Mentor especializado en Observabilidad y Monitoring.

Capacidades:
1. DETECCIÓN: Identificar exposición de PII, secrets, y datos sensibles en logs/traces
2. EDUCACIÓN: Explicar por qué cierta información NO debe enviarse a servicios externos
3. CORRECCIÓN: Proporcionar código de scrubbing y filtrado robusto
4. PRINCIPIOS: Enseñar "defense in depth", "least privilege", "assume breach"
5. CONTEXTO: Adaptar a Sentry, DataDog, New Relic, CloudWatch, etc.

Formato de respuesta para cada vulnerabilidad:
---
🔴 VULNERABILIDAD DETECTADA: [Nombre]
📍 Ubicación: [Línea/configuración]
⚠️ Severidad: [Crítica/Alta/Media]
💥 Impacto: [Qué información se filtra]
🛠️ Ejemplo de ataque: [Cómo un atacante explotaría esto]
✅ Solución: [Código de scrubbing/filtrado con explicaciones]
📚 Principio: [Concepto de seguridad subyacente]
🧪 Cómo testear: [Comando/script para verificar que el scrubbing funciona]
---

Casos especiales a revisar:
- Captura automática de request bodies en endpoints de autenticación
- Headers con tokens JWT, API keys, cookies de sesión
- Variables de entorno con secrets (DATABASE_URL, JWT_SECRET, etc.)
- URL parameters con tokens de reseteo de contraseña
- Contexto de usuario con PII (email, teléfono, dirección IP en EU)
- Stack traces que exponen rutas del sistema de archivos

Tono: Educativo, alentador, técnicamente preciso. Enfatizar que observabilidad es crítica
para debugging PERO debe hacerse de forma segura. No es paranoia, es profesionalismo.

Código de Sentry a auditar:
[Pega aquí el código de inicialización de Sentry]
```

---

### 🔧 Mejoras del Pipeline CI/CD con Sentry

**Prompt para integrar Sentry en CI/CD**:

```
Rol: Ingeniero DevSecOps especializado en observabilidad.
Contexto: Proyecto FastAPI con CI/CD, JWT, auditorías, y ahora Sentry para monitoring.
Objetivo: Integrar Sentry en el pipeline de CI/CD para:
1. Validar que el SENTRY_DSN está configurado como secret (no hardcoded)
2. Verificar que el código incluye scrubbing de datos sensibles (test automático)
3. Crear un job de CI que testee el before_send hook con datos sensibles (debe redactarlos)
4. Configurar notificaciones: errores críticos en Sentry → alerta en Slack/Discord
5. Generar reporte de Sentry en cada PR (errores nuevos introducidos)

Entrega:
- YAML actualizado con job de validación de Sentry
- Script de test para verificar scrubbing (ej: test_sentry_scrubbing.py)
- Configuración de alertas (Sentry → Slack webhook)
- Documentación de debugging con Sentry
```

**Validación de Sentry en CI** (ejemplo):

```yaml
# .github/workflows/ci_quality.yml
- name: Validar configuración de Sentry
  run: |
    # ✅ Verificar que SENTRY_DSN no está hardcoded
    if grep -r "sentry.io" --include="*.py" --exclude-dir=".venv"; then
      echo "❌ SENTRY_DSN encontrado hardcoded en código"
      exit 1
    fi

    # ✅ Verificar que existe scrubbing de datos sensibles
    if ! grep -q "scrub_sensitive_data\|before_send" api/api.py; then
      echo "⚠️  Advertencia: No se encontró función de scrubbing en api.py"
    fi

    # ✅ Ejecutar tests de scrubbing
    pytest tests/test_sentry_scrubbing.py -v
```

**Test de scrubbing** (tests/test_sentry_scrubbing.py):

```python
import pytest
from api.api import scrub_sensitive_data, before_send

def test_scrubbing_passwords():
    """Verify passwords are redacted."""
    data = {
        "username": "demo",
        "password": "super_secret_123",
        "email": "demo@example.com"
    }

    scrubbed = scrub_sensitive_data(data)

    assert scrubbed["username"] == "demo"
    assert scrubbed["password"] == "[REDACTED]"
    assert scrubbed["email"] == "demo@example.com"


def test_scrubbing_tokens():
    """Verify JWT tokens are redacted."""
    data = {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh_token": "abc123def456"
    }

    scrubbed = scrub_sensitive_data(data)

    assert scrubbed["access_token"] == "[REDACTED]"
    assert scrubbed["refresh_token"] == "[REDACTED]"


def test_before_send_removes_auth_header():
    """Verify Authorization header is removed in before_send."""
    event = {
        'request': {
            'headers': {
                'Authorization': 'Bearer eyJhbGc...',
                'Content-Type': 'application/json',
                'X-API-Key': 'secret_key_123'
            }
        }
    }

    processed = before_send(event, {})

    assert 'Authorization' not in processed['request']['headers']
    assert 'X-API-Key' not in processed['request']['headers']
    assert 'Content-Type' in processed['request']['headers']  # Non-sensitive OK
```

---

### 🚨 Caso Real: Sentry Data Breach (Educativo)

**Escenario**: Un desarrollador configuró Sentry con `auto_enable_request_body=True` y sin scrubbing.

**Qué pasó**:
1. Un endpoint `/reset-password` acepta `{email, new_password}`
2. Si el endpoint falla (ej: email no existe), Sentry captura el error
3. El request body **con la nueva contraseña** se envía a Sentry
4. Un atacante con acceso al proyecto de Sentry puede ver todos los passwords intentados

**Lección**:
- **Observabilidad es poder**: Todo lo que envías a Sentry puede ser visto por quien tenga acceso
- **Assume breach**: Asume que alguien puede comprometer tu cuenta de Sentry
- **Minimize blast radius**: Solo envía lo mínimo necesario para debugging

---

### 📊 Métricas de Observabilidad Segura

Mide si tu observabilidad es segura:

| Métrica | Objetivo | Cómo medir |
|---------|----------|------------|
| **Eventos con PII** | 0 por semana | Buscar en Sentry: "email", "password", "token" en eventos |
| **Sample rate** | 10-30% | Verificar `traces_sample_rate` en config |
| **Alertas configuradas** | ≥ 3 (critical errors, high error rate, new issue types) | Panel de Sentry → Alerts |
| **Tiempo de detección** | < 5 minutos | Crear error, medir tiempo hasta notificación Slack |
| **False positives** | < 5% de alertas | Revisar alertas que no requirieron acción |

---

## 🧪 Mini-proyecto

1. Crea la rama `feature/observabilidad-sentry`.
2. Añade `sentry-sdk` al proyecto y configura `SENTRY_DSN` como secret.
3. Crea una ruta `/error` para testearlo.
4. Verifica que Sentry recibe el fallo.
5. Documenta en `notes.md`:
    - Qué información viste en el dashboard.
    - Cómo ayuda eso a depurar más rápido.
    - Qué alertas o integraciones extra añadirías.

---

## ✅ Checklist de la clase

- [ ]  Sentry instalado y configurado.
- [ ]  Variable `SENTRY_DSN` añadida como secret.
- [ ]  Ruta `/error` comprobada y visible en Sentry.
- [ ]  Integración opcional de alertas (Slack, Discord, email).
- [ ]  notes.md con evidencias y reflexiones.

---

## 🌱 Qué aporta esta clase

Con Sentry, tu API ya **no solo se defiende y audita**, sino que **informa y aprende**.

Cierra el ciclo del módulo 3:

> “Si algo se rompe, lo sabrás antes que el usuario… y con todos los datos para arreglarlo.”
>