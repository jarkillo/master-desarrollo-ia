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

## 🤖 Aplicación con IA

Prompt reutilizable para tu agente IA o Cursor:

```
Rol: Ingeniero de observabilidad.
Contexto: API FastAPI con CI/CD, JWT y auditorías.
Objetivo:
- Integrar Sentry para registrar errores y rendimiento.
- Configurar secrets y alertas en GitHub Actions.
Entrega:
- Código mínimo para inicializar Sentry.
- YAML modificado con variable SENTRY_DSN.
- Recomendaciones para alertas automáticas.

```

Así la IA te generará el código, actualizará el pipeline y te propondrá alertas o métricas adicionales (por ejemplo, con Grafana o Discord).

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