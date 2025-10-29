# Workflow AI - Clase 7: Observabilidad y Alertas con Sentry

## 🎯 Objetivo

Usar IA para **configurar observabilidad inteligente** con Sentry y **analizar errores en producción** para priorizar fixes.

---

## 🤖 Agentes Recomendados

### 1. Performance Optimizer
- **Analizar performance traces**: Endpoints lentos
- **Detectar N+1 queries**: Database bottlenecks

### 2. Security Hardening Mentor
- **Error handling seguro**: No exponer stack traces
- **PII en logs**: Detectar datos sensibles

---

## 🚀 Workflow: Sentry + IA

### Paso 1: Configuración Segura de Sentry

**Prompt**:
```
Configura Sentry en FastAPI de forma segura.

Requisitos:
1. Integración FastAPI oficial
2. Capturar exceptions automáticamente
3. Performance monitoring (traces, spans)
4. NO capturar datos sensibles (passwords, tokens)
5. Environment tags (dev, staging, prod)
6. Release tracking (git commit SHA)

Configuración:
[PEGA sentry_sdk initialization]

¿Qué filtros de PII (Personally Identifiable Info) debo agregar?
Muestra código completo con before_send hook.
```

**Código seguro**:
```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

def before_send(event, hint):
    """Filtrar datos sensibles antes de enviar a Sentry."""
    # Remover passwords
    if 'request' in event:
        if 'data' in event['request']:
            data = event['request']['data']
            if isinstance(data, dict):
                data.pop('password', None)
                data.pop('token', None)

    # Sanitizar headers
    if 'headers' in event.get('request', {}):
        headers = event['request']['headers']
        headers.pop('Authorization', None)

    return event

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1,  # 10% de requests
    environment=os.getenv("ENVIRONMENT", "dev"),
    release=os.getenv("GIT_SHA"),
    before_send=before_send
)
```

---

### Paso 2: Análisis de Errores con IA

**Prompt para analizar Sentry issues**:
```
Tengo estos errores en Sentry (últimas 24h):

1. ValueError: Invalid task ID
   - Count: 450
   - Users affected: 23
   - Stack trace: [PEGA TRACE]

2. HTTPException 404
   - Count: 1200
   - Users affected: 87
   - Endpoint: GET /tareas/{id}

3. asyncpg.PostgresError: connection timeout
   - Count: 15
   - Users affected: 8

Analiza:
1. ¿Cuál priorizar primero? (impacto vs frecuencia)
2. Root cause probable de cada error
3. Fix sugerido con código
4. ¿Cómo prevenirlo en el futuro?
```

---

### Paso 3: Performance Analysis

**Prompt**:
```
Sentry performance traces muestran:

Endpoint: GET /tareas
- P50: 250ms
- P95: 1200ms ⚠️
- P99: 3500ms 🚨

Spans:
1. Database query: 45ms (P50), 980ms (P95)
2. JSON serialization: 5ms
3. Validation: 2ms

Analiza:
1. ¿Por qué el P95 es 5x el P50?
2. ¿Problema de N+1 queries?
3. Optimizaciones sugeridas
4. Tests de performance para CI
```

---

### Paso 4: Alertas Inteligentes

**Prompt para configurar alertas**:
```
Configura alertas Sentry inteligentes:

1. Critical (página inmediata):
   - Error rate > 5% últimos 5 min
   - Apdex score < 0.7
   - Database connections exhausted

2. High (notificación inmediata):
   - Nuevo tipo de error (first seen)
   - P95 latency > 2s
   - 500 errors en endpoint crítico

3. Medium (resumen diario):
   - Error count increase >50%
   - User feedback negativo

4. Low (resumen semanal):
   - Deprecation warnings
   - Performance degradation <20%

¿Cómo configurar estas alertas en Sentry?
¿Integración con Slack/PagerDuty?
```

---

## ✅ Checklist Observabilidad

```markdown
Sentry Config:
- [ ] DSN en variable de entorno
- [ ] before_send hook filtra PII
- [ ] Environment tags (dev/staging/prod)
- [ ] Release tracking con git SHA
- [ ] Sample rate apropiado (10-20%)

Monitoring:
- [ ] Performance tracing habilitado
- [ ] Database queries tracked
- [ ] Alertas configuradas por severidad
- [ ] Dashboard de health en Sentry

Privacy:
- [ ] No passwords en eventos
- [ ] No tokens en eventos
- [ ] Authorization headers filtrados
- [ ] User IDs anonimizados si GDPR
```

---

## 💡 AI-Powered Error Triage

**Weekly Error Review con IA**:

```
Revisa errores Sentry de esta semana:

[EXPORTAR JSON de Sentry]

Genera reporte:
1. Top 5 errores por impacto (frecuencia × users affected)
2. Errores críticos de seguridad (si existen)
3. Performance regressions detectadas
4. Recomendaciones priorizadas con código

Formato: Markdown con links a Sentry issues
```

---

**Tiempo**: 2 horas | **Agentes**: Performance Optimizer, Security Hardening Mentor
