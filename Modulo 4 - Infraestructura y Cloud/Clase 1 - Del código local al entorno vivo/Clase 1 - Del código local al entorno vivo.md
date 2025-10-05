# Clase 1 - Del código local al entorno vivo

Hasta ahora, tu código:

- se defiende solo (tests, cobertura, linters),
- se protege (API Key y JWT),
- se audita (Bandit, Safety, Gitleaks),
- y se monitorea (Sentry).

Pero todo eso vive en un entorno controlado: tu máquina y GitHub Actions.

Hoy, empezamos la fase donde el código **cobra vida propia en la nube**.

## 🧩 Historia: el código quiere salir de casa

Imagina tu API como un joven programador recién graduado: ha aprendido a cuidarse, a revisar su trabajo y a proteger sus secretos.

Pero ahora quiere independizarse.

Necesita un lugar donde vivir (un servidor o contenedor), una nevera donde guardar sus datos (una base de datos), y vecinos con los que hablar (otras APIs, el frontend, etc.).

Ese es el **salto a infraestructura**.

Y justo aquí empieza la Clase 1:

**“Del código local al entorno vivo: entender la infraestructura moderna”**.

---

## 🧠 Concepto

Infraestructura es todo lo que **hace posible que tu aplicación funcione cuando tú no estás mirando**.

Desde los servidores y contenedores, hasta los pipelines que la despliegan automáticamente.

Vamos a romperlo en capas comprensibles:

1. **Infraestructura física o virtual:** máquinas reales o servicios cloud (AWS, Render, Railway).
2. **Infraestructura como código (IaC):** archivos que describen esa máquina (por ejemplo, Docker o Terraform).
3. **Pipeline CI/CD:** el sistema que toma tu repo, ejecuta tests, construye tu app y la lanza.
4. **Entorno y configuración:** variables `.env`, secretos, y conexiones seguras a servicios externos.
5. **Monitoreo y logs:** lo que te cuenta si el entorno está sano.

Tu objetivo en este módulo no será “aprender Docker” o “hacer un despliegue mágico”, sino **entender cómo se conectan las piezas** para poder hacerlo tú o delegarlo a la IA con criterio.

---

## ⚙️ Aplicación manual – cómo lo haría un dev

1. Creas un entorno virtual o contenedor donde se ejecuta tu API.
2. Añades una base de datos (SQLite, PostgreSQL, Mongo…).
3. Configuras las variables de entorno (`DATABASE_URL`, `API_KEY`, `JWT_SECRET`).
4. Haces que el pipeline (GitHub Actions) ejecute los tests, y si todo va bien, **haga deploy automático**.

En esta primera clase **no desplegaremos todavía**, sino que prepararemos el terreno:

- limpiar tu proyecto,
- asegurar que los `.env` estén bien definidos,
- y dejar claro qué partes del código dependen del entorno.

## 📂 Estructura de carpetas

```
Modulo 4 – Infraestructura y Cloud/
│
├── Clase 1 - Del código local al entorno vivo.md
└── infra/
    ├── README.md
    ├── .env.template
    └── check_env.py

```

Añade un pequeño script de validación (`infra/check_env.py` )

```python
# infra/check_env.py
import re, sys, os

TEMPLATE_PATH = os.path.join("infra", ".env.template")
ENV_PATH = ".env"
EN_CI = os.getenv("GITHUB_ACTIONS") == "true"

if not os.path.exists(TEMPLATE_PATH):
    print("❌ No se encontró infra/.env.template")
    sys.exit(1)

if not os.path.exists(ENV_PATH):
    if EN_CI:
        print("ℹ️  CI: no hay .env; se omite la validación de valores (solo se valida en local).")
        sys.exit(0)
    else:
        print("⚠️  No hay archivo .env, créalo a partir del template.")
        sys.exit(1)

with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    variables = re.findall(r"^([A-Z_]+)=", f.read(), re.MULTILINE)

with open(ENV_PATH, "r", encoding="utf-8") as f:
    contenido_env = f.read()

missing = [var for var in variables if var not in contenido_env]

if missing:
    print("❌ Faltan variables en .env:", ", ".join(missing))
    sys.exit(1)

print("✅ Variables sincronizadas correctamente")


```

Este script puede ejecutarse igual en **Windows, macOS o Linux**, y también desde **GitHub Actions**, sin permisos especiales.

1. En tu workflow de CI añade una etapa para lanzarlo:

```yaml
- name: Validar variables de entorno
  run: python infra/check_env.py
```

1. Revisa tu código y apunta qué partes dependen de variables de entorno (por ejemplo, claves o rutas de DB).

---

## 🤖 Aplicación con IA

A partir de aquí, la IA será tu **ingeniero de infraestructura asistido**.

Usa este prompt base para explorar configuraciones:

```
Rol: Ingeniero DevOps.
Contexto: API FastAPI con tests y CI configurado.
Objetivo: Preparar el entorno para despliegue en la nube.

Entrega:
- Archivos .env y ejemplo .env.template.
- Estructura recomendada de carpetas (infra/, scripts/).
- YAML inicial para pipeline de despliegue.

```

La IA puede generarte una plantilla inicial de infraestructura (`infra/docker-compose.yml`, `infra/requirements.txt`, `infra/env.example`) y explicarte cómo conectarla al pipeline.

---

## 🧪 Mini-proyecto de esta clase

1. Crea una rama `feature/infraestructura-base`.
2. Prepara un archivo `.env.template` con todas las variables que usará tu proyecto (API_KEY, JWT_SECRET, DATABASE_URL...).
3. Crea una carpeta `/infra` con un `README.md` que explique cómo levantar el entorno.
4. Añade en tu workflow CI una etapa que valide que `.env` y `.env.template` están sincronizados.
5. Documenta en `notes.md`:
    - qué variables definiste,
    - qué dependencias cambiarán en cloud,
    - y qué decisiones dejarás a la IA en el despliegue.

---

## ✅ Checklist de la Clase 1 – Infraestructura base

- [ ]  Entiendes qué es infraestructura y por qué es necesaria.
- [ ]  Tienes un `.env.template` claro y limpio.
- [ ]  Has creado la carpeta `/infra`.
- [ ]  Tu CI valida configuración y variables.
- [ ]  Tienes apuntes listos para el despliegue del módulo 4.

---

En la próxima clase veremos cómo **convertir tu entorno local en uno reproducible**, con Docker o contenedores ligeros.

Tu API dejará de depender de “mi máquina funciona” y empezará a ser **portable y escalable**.