# 🧭 Glosario – Clase 7

**Observabilidad** → capacidad de entender el estado interno de tu sistema observando sus outputs (logs, métricas, traces). No solo saber "qué falló", sino "por qué falló" y "en qué contexto".

**Sentry** → plataforma de monitoreo y observabilidad que captura errores en producción, guarda todo el contexto (request, usuario, commit), y te notifica automáticamente. El sistema nervioso de tu aplicación.

**DSN (Data Source Name)** → URL única que Sentry te da para conectar tu app a tu proyecto. Contiene credenciales, por eso **debe estar en .env o GitHub Secrets, NUNCA en código**.

```python
SENTRY_DSN="https://1234567890abcdef.ingest.sentry.io/1234567"
```

**sentry-sdk[fastapi]** → librería oficial de Sentry para Python con integración especializada para FastAPI.

```bash
pip install "sentry-sdk[fastapi]"
```

**traces_sample_rate** → porcentaje de requests que Sentry captura para análisis de rendimiento. `1.0` = 100% (costoso y expone mucho), `0.1` = 10% (recomendado para producción).

```python
traces_sample_rate=0.1  # Solo 10% de traces, pero 100% de errores
```

**Scrubbing** → proceso de filtrar y eliminar datos sensibles (passwords, tokens, PII) **antes** de enviarlos a Sentry. Es tu primera línea de defensa.

```python
def scrub_sensitive_data(data: dict) -> dict:
    # Reemplaza "password", "token", "secret" con "[REDACTED]"
```

**PII (Personally Identifiable Information)** → información que identifica a una persona individual (email, teléfono, dirección, IP en EU, nombre completo). **No debe enviarse a servicios externos** sin consentimiento explícito.

**before_send hook** → función que procesa cada evento antes de enviarlo a Sentry. Aquí implementas tu lógica de scrubbing personalizada.

```python
def before_send(event, hint):
    # Scrub headers, body, query params
    return event  # or None to drop the event
```

**send_default_pii** → flag de Sentry que controla si envía PII automáticamente. **Siempre debe ser `False`** para seguridad.

```python
send_default_pii=False  # No enviar PII por defecto
```

**FastApiIntegration** → integración oficial de Sentry para FastAPI que captura errores y traces automáticamente.

```python
integrations=[
    FastApiIntegration(
        transaction_style="url"  # Agrupa por patrón de URL
    )
]
```

**auto_enable_request_body** → flag peligroso que captura automáticamente el body completo de todos los requests. **Debe estar deshabilitado** (o no incluido) para evitar capturar passwords.

```python
# ❌ NUNCA
auto_enable_request_body=True

# ✅ CORRECTO (omitirlo o False)
# No incluir esta opción
```

**Breadcrumbs** → "migas de pan" que Sentry guarda sobre las acciones previas a un error (logs, queries DB, requests HTTP). Útil para debugging, pero limita el tamaño.

```python
max_breadcrumbs=50  # Límite de breadcrumbs a guardar
```

**Sample rate** → tasa de muestreo. Balance entre:
- 100%: Visibilidad total pero costo alto y más exposición de datos
- 10-30%: Suficiente para detectar patrones, menor costo y exposición

**Context** → información adicional que Sentry adjunta a cada evento (usuario, tags, custom data). Debe ser **mínimo necesario** para debugging.

```python
with sentry_sdk.push_scope() as scope:
    scope.set_context("login_attempt", {
        "username": "demo"  # ✅ OK
        # ❌ NO añadir: password, IP, email
    })
```

**Defense in depth** → principio de seguridad: múltiples capas de protección. En Sentry:
1. `before_send` hook con scrubbing
2. `send_default_pii=False`
3. Deshabilitar `auto_enable_request_body`
4. Filtrar headers sensibles manualmente

**Least privilege** → principio de seguridad: solo enviar la información mínima necesaria para cumplir el objetivo (debugging), nada más.

**Assume breach** → principio de seguridad: asumir que alguien puede comprometer tu cuenta de Sentry, por eso nunca envíes datos que, filtrados, pongan en riesgo a usuarios.

**Blast radius** → radio de impacto de una vulnerabilidad. Minimízalo enviando solo datos no sensibles a Sentry.

**Release tracking** → vincular errores de Sentry con el commit/versión específica que los causó.

```python
release=os.getenv("GIT_COMMIT", "unknown")
```

**Fingerprint** → identificador que Sentry usa para agrupar errores similares. Puedes personalizarlo para agrupar mejor.

```python
with sentry_sdk.configure_scope() as scope:
    scope.fingerprint = ['database', 'connection-timeout']
```

**Alert rules** → reglas configuradas en Sentry para notificarte (Slack, email, Discord) cuando ocurren errores críticos o se supera un umbral.

**Error budget** → porcentaje de requests que pueden fallar sin afectar el SLA (Service Level Agreement). Ej: 99.9% uptime = 0.1% error budget.

**Stack trace** → traza completa de la pila de llamadas cuando ocurre un error. Sentry la captura automáticamente, pero puede exponer rutas del sistema de archivos (considerado PII en algunos casos).

**Data retention policies** → políticas de cuánto tiempo Sentry guarda los datos. Importante para compliance (GDPR, CCPA): eliminar datos sensibles después de 30 días.

**Sentry Security Checklist** → lista de verificación para auditar configuraciones de Sentry:
- 🔴 DSN como secreto
- 🔴 Scrubbing de passwords/tokens
- 🔴 Headers sensibles filtrados
- 🟠 Sample rate < 100%
- 🟠 send_default_pii=False
- 🟡 Release tracking configurado

**Security Hardening Mentor para Sentry** → agente educacional especializado en auditar configuraciones de observabilidad, detectar exposición de PII/secrets, y enseñar principios de seguridad aplicados a monitoring.

**Casos de vulnerabilidad común**:
- ❌ Capturar body de `/login` con passwords
- ❌ Enviar `Authorization` header con JWT tokens
- ❌ Incluir `os.environ` completo (expone JWT_SECRET, DATABASE_URL)
- ❌ Sample rate 100% (costoso y sobreexpone datos)

**Observabilidad segura** → observabilidad que cumple:
1. Nunca loguear información sensible
2. Scrubbing automático antes de enviar
3. Context mínimo necesario
4. DSN como secreto
5. Sample rate adecuado
