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

## 🤖 Aplicación con IA: Tu ingeniero DevOps asistido

En esta clase, la IA será tu **ingeniero de infraestructura asistido**. No se trata de que la IA lo haga todo por ti, sino de que la uses para **generar configuraciones base** que luego **optimizarás con criterio**.

El workflow que seguiremos es:

**IA genera → Tú optimizas → Agent valida → Producción**

### Workflow AI para Infraestructura Docker

#### Fase 1: Generación del Dockerfile base

Usa este prompt para generar un Dockerfile inicial:

```
Rol: Ingeniero DevOps especializado en contenedores.
Contexto: API FastAPI con las siguientes características:
- Framework: FastAPI + Uvicorn
- Python 3.12
- Dependencias en requirements.txt
- Variables de entorno: DATABASE_URL, JWT_SECRET, API_KEY
- Puerto: 8000

Objetivo: Generar un Dockerfile optimizado para producción.

Entrega:
- Dockerfile con multi-stage build
- Non-root user para seguridad
- Health check configurado
- Comentarios explicando cada sección
```

**Ejemplo de output de la IA**:

```dockerfile
# Stage 1: Builder
FROM python:3.12-slim AS builder

WORKDIR /app

# Instalar dependencias primero (mejor cache)
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim

# Non-root user (seguridad)
RUN useradd -m -u 1000 appuser
USER appuser
WORKDIR /home/appuser/app

# Copiar dependencies desde builder
COPY --from=builder /root/.local /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH

# Copiar código
COPY --chown=appuser:appuser . .

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

EXPOSE 8000

CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Fase 2: Optimización con criterio humano

Ahora que tienes el Dockerfile generado por IA, **tú validas y optimizas**:

1. **Verifica el tamaño de la imagen**:
   ```bash
   docker build -t mi-api:test .
   docker images | grep mi-api
   # ¿Es menor a 200MB? ✅ Bien
   # ¿Es mayor a 500MB? ⚠️ Hay que optimizar
   ```

2. **Analiza las capas con Dive** (herramienta de análisis):
   ```bash
   dive mi-api:test
   # Verifica qué capas son más pesadas
   # Identifica archivos innecesarios
   ```

3. **Pregunta a la IA sobre optimizaciones específicas**:
   ```
   He generado este Dockerfile y la imagen pesa 450MB.
   Analiza qué se puede optimizar para reducir el tamaño.
   Considera:
   - ¿Hay dependencias innecesarias en requirements.txt?
   - ¿Se están copiando archivos que no se usan en producción?
   - ¿Hay mejores imágenes base?
   ```

#### Fase 3: Validación con el Docker Infrastructure Guide Agent

Ahora usarás el **Docker Infrastructure Guide** (agente educativo) para validar:

1. **Ejecuta el agent** en tu directorio:
   ```bash
   # Desde Claude Code
   @docker-infrastructure-guide Revisa mi Dockerfile y dame feedback educativo
   ```

2. **El agent validará**:
   - ✅ Multi-stage build implementado
   - ✅ Non-root user configurado
   - ✅ Health check definido
   - ✅ Layer caching optimizado
   - ✅ Imagen base ligera (slim/alpine)
   - ✅ .dockerignore presente

3. **Aprende del feedback**:
   El agent no solo te dice qué está mal, sino **por qué importa** y **cómo mejorarlo**.

   Ejemplo de feedback del agent:
   ```
   ⚠️ Dockerfile: Orden de COPY no optimiza cache

   **Problema detectado**:
   Copias todo el código ANTES de instalar dependencies.
   Esto invalida el cache de Docker en cada cambio de código.

   **Impacto**:
   - Build time aumenta de 30s a 5min en cada cambio
   - CI/CD más lento
   - Experiencia de desarrollo frustrante

   **Solución**:
   COPY requirements.txt primero, luego pip install,
   finalmente COPY el código.

   **Por qué funciona**:
   Docker cachea capas. Si requirements.txt no cambia,
   reutiliza la capa de pip install (90% del build time).
   ```

#### Fase 4: Generación de docker-compose.yml

Una vez que tienes un Dockerfile optimizado, genera el docker-compose:

```
Contexto: Dockerfile optimizado listo.
Necesito un docker-compose.yml para desarrollo local que incluya:
- Mi API (build desde Dockerfile)
- PostgreSQL 15
- Health checks en ambos servicios
- Secrets desde archivo .env (no hardcodeados)
- Volumes nombrados para persistencia
- Resource limits

Genera el docker-compose.yml completo con comentarios educativos.
```

**Luego optimizas** con el Docker Infrastructure Guide:

```bash
@docker-infrastructure-guide Revisa mi docker-compose.yml y valida best practices
```

### Prompts Efectivos para Infraestructura

#### Prompt 1: Generación de .env.template

```
Contexto: API FastAPI con:
- JWT authentication
- PostgreSQL database
- API keys externas (OpenAI, Sentry)
- Configuración de entorno (dev/staging/prod)

Genera un .env.template completo con:
- Todas las variables necesarias
- Comentarios explicando cada variable
- Ejemplos de valores (sin secrets reales)
- Separación por categorías (DB, Auth, External APIs, Config)
```

#### Prompt 2: Script de validación de entorno

```
Crea un script check_env.py que valide:
- Que .env existe (solo en local, no en CI)
- Que todas las variables de .env.template están en .env
- Que no hay secretos hardcodeados en el código
- Compatible con Windows, macOS, Linux

Usa solo librerías estándar de Python (no dependencies externas).
```

#### Prompt 3: Dockerfile para diferentes contextos

```
Genera 3 Dockerfiles optimizados para:

1. Development: Con hot-reload, debugging tools, volúmenes montados
2. CI/CD: Mínimo, solo para ejecutar tests
3. Production: Ultra-optimizado, seguro, mínimo tamaño

Explica las diferencias entre cada uno y cuándo usar cada contexto.
```

### Herramientas AI-Powered para Infraestructura

1. **Dive** (análisis de imágenes Docker):
   ```bash
   dive <imagen>
   # Muestra capas, tamaño, archivos innecesarios
   ```

2. **Hadolint** (linter de Dockerfiles):
   ```bash
   hadolint Dockerfile
   # Detecta anti-patterns automáticamente
   ```

3. **Trivy** (scanner de vulnerabilidades):
   ```bash
   trivy image <imagen>
   # Escanea CVEs en dependencias
   ```

4. **Claude Code + Docker Infrastructure Guide**:
   ```bash
   # Validación educativa con feedback explicativo
   @docker-infrastructure-guide Revisa toda mi configuración Docker
   ```

### Ejercicio Práctico: Genera y Optimiza un Dockerfile

**Objetivo**: Generar un Dockerfile con IA, optimizarlo, y validarlo con el agent.

**Pasos**:

1. **Genera el Dockerfile base** con el prompt de la Fase 1
2. **Construye la imagen** y verifica el tamaño:
   ```bash
   docker build -t mi-api:v1 .
   docker images mi-api:v1
   ```
3. **Si es > 300MB**, pide optimizaciones a la IA:
   ```
   Mi imagen pesa [X]MB. Optimízala para que sea < 200MB.
   Analiza qué se puede eliminar o mejorar.
   ```
4. **Valida con el agent**:
   ```bash
   @docker-infrastructure-guide Revisa mi Dockerfile optimizado
   ```
5. **Documenta** las mejoras conseguidas:
   - Tamaño antes vs después
   - Build time antes vs después
   - Mejoras de seguridad aplicadas

**Meta**: Imagen final < 200MB, build time < 1 minuto, feedback del agent 100% positivo.

---

---

## 🧪 Mini-proyecto de esta clase: Infraestructura AI-Powered

Este mini-proyecto integra **desarrollo manual + asistencia AI + validación con agents**.

### Parte 1: Configuración de Entorno (Manual)

1. **Crea una rama** `feature/infraestructura-ai-clase1`:
   ```bash
   git checkout dev
   git checkout -b feature/infraestructura-ai-clase1
   ```

2. **Prepara `.env.template`** con todas las variables:
   ```bash
   # Base de datos
   DATABASE_URL=your_database_url_here

   # Autenticación
   JWT_SECRET=your_jwt_secret_here
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_MINUTES=30

   # APIs externas
   API_KEY=your_api_key_here

   # Configuración
   MODE=dev
   LOG_LEVEL=INFO
   ```

3. **Crea carpeta `/infra`** con estructura:
   ```
   infra/
   ├── README.md
   ├── .env.template
   └── check_env.py
   ```

### Parte 2: Generación de Dockerfile con IA

4. **Usa el prompt de Fase 1** para generar un Dockerfile inicial:
   - Prompt: "Genera Dockerfile para API FastAPI con Python 3.12..."
   - Guarda el output en `Dockerfile`

5. **Construye y analiza** la imagen:
   ```bash
   docker build -t tareas-api:v1 .
   docker images tareas-api:v1
   # Anota el tamaño inicial
   ```

6. **Si la imagen es > 300MB**, usa el prompt de optimización:
   - Pide a la IA que reduzca el tamaño
   - Reconstruye y compara tamaños

### Parte 3: Validación con Docker Infrastructure Guide

7. **Invoca el agent** para validación:
   ```bash
   @docker-infrastructure-guide Revisa mi Dockerfile y dame feedback
   ```

8. **Aplica mejoras sugeridas** por el agent:
   - Si falta .dockerignore, créalo
   - Si hay problemas de cache, corrige el orden de COPY
   - Si falta health check, añádelo

9. **Vuelve a validar** hasta conseguir feedback 100% positivo

### Parte 4: docker-compose.yml con IA

10. **Genera docker-compose.yml** usando el prompt de Fase 4:
    - Incluye API + PostgreSQL
    - Health checks
    - Volumes nombrados
    - Secrets desde .env

11. **Valida con el agent**:
    ```bash
    @docker-infrastructure-guide Revisa mi docker-compose.yml
    ```

### Parte 5: Integración en CI

12. **Añade validación de entorno** al workflow CI:
    ```yaml
    # .github/workflows/ci_quality.yml
    - name: Validar configuración de entorno
      run: python infra/check_env.py
    ```

### Parte 6: Documentación del Proceso AI

13. **Documenta en `infra/README.md`**:
    ```markdown
    # Infraestructura - Clase 1

    ## 🤖 Proceso AI-Powered

    ### Dockerfile
    - **Generado por**: Claude Code (Prompt de Fase 1)
    - **Tamaño inicial**: [X]MB
    - **Tamaño optimizado**: [Y]MB
    - **Mejoras aplicadas**:
      - Multi-stage build
      - Non-root user
      - Health check
      - Layer caching optimizado

    ### docker-compose.yml
    - **Generado por**: Claude Code (Prompt de Fase 4)
    - **Validado por**: Docker Infrastructure Guide agent
    - **Best practices aplicadas**:
      - Health checks en todos los servicios
      - Secrets desde .env
      - Volumes nombrados
      - Resource limits

    ## 🚀 Cómo levantar el entorno

    1. Copia `.env.template` a `.env` y configura:
       ```bash
       cp infra/.env.template .env
       # Edita .env con tus valores reales
       ```

    2. Levanta los servicios:
       ```bash
       docker-compose up -d
       ```

    3. Verifica health:
       ```bash
       docker-compose ps
       # Todos los servicios deben estar "healthy"
       ```

    ## 📊 Métricas conseguidas

    - Tamaño de imagen: [X]MB → [Y]MB (Z% reducción)
    - Build time: [A]s → [B]s
    - Feedback del agent: ✅ 100% positivo
    ```

14. **Crea `notes.md`** con aprendizajes:
    ```markdown
    # Aprendizajes Clase 1: Infraestructura AI-Powered

    ## ✅ Logros

    1. **Dockerfile optimizado**:
       - Tamaño: [antes] → [después]
       - Multi-stage build implementado
       - Non-root user configurado

    2. **docker-compose.yml profesional**:
       - Health checks ✅
       - Secrets management ✅
       - Volumes persistentes ✅

    3. **Validación con agent**:
       - Aprendí la importancia del layer caching
       - Entendí por qué non-root user es crítico
       - Vi cómo health checks ayudan en producción

    ## 🤖 Uso de IA

    - **Qué delegué a la IA**:
      - Generación del Dockerfile base
      - Estructura de docker-compose.yml
      - Prompts para optimización

    - **Qué validé yo**:
      - Tamaño de imagen (< 200MB)
      - Build time aceptable
      - Feedback del agent

    - **Qué aprendí del agent**:
      - [Aprendizaje 1]
      - [Aprendizaje 2]
      - [Aprendizaje 3]

    ## 🔮 Decisiones para el despliegue (próxima clase)

    - Usaré Railway para desplegar (simple, free tier)
    - PostgreSQL gestionado vs contenedor
    - Variables de entorno: GitHub Secrets → Railway
    ```

### Meta del mini-proyecto

Al finalizar, debes tener:

- ✅ `.env.template` completo y documentado
- ✅ Dockerfile optimizado (< 200MB)
- ✅ docker-compose.yml con best practices
- ✅ .dockerignore configurado
- ✅ CI validando configuración de entorno
- ✅ Feedback 100% positivo del Docker Infrastructure Guide
- ✅ Documentación completa en `infra/README.md`
- ✅ Aprendizajes documentados en `notes.md`

**Tiempo estimado**: 2-3 horas (1h generación AI + 1h optimización + 1h validación y documentación)

---

## ✅ Checklist de la Clase 1 – Infraestructura AI-Powered

### Conceptos Fundamentales
- [ ] Entiendes qué es infraestructura y por qué es necesaria
- [ ] Conoces las 5 capas de infraestructura moderna
- [ ] Comprendes la diferencia entre entornos (local, CI, staging, producción)

### Configuración Manual
- [ ] Tienes un `.env.template` completo y documentado
- [ ] Has creado la carpeta `/infra` con README.md
- [ ] Tu CI valida configuración y variables con `check_env.py`
- [ ] `.env` está en `.gitignore` (nunca commitear secrets)

### Generación con IA
- [ ] Generaste un Dockerfile usando el prompt de Fase 1
- [ ] El Dockerfile incluye multi-stage build
- [ ] Configuraste non-root user (appuser)
- [ ] Añadiste health check al Dockerfile
- [ ] Generaste docker-compose.yml con el prompt de Fase 4
- [ ] docker-compose incluye health checks en todos los servicios
- [ ] Secrets están en `.env`, no hardcodeados

### Optimización
- [ ] Imagen Docker < 200MB
- [ ] Build time < 1 minuto
- [ ] Creaste `.dockerignore` para optimizar cache
- [ ] Layer caching optimizado (COPY requirements.txt antes que código)

### Validación con Agent
- [ ] Ejecutaste Docker Infrastructure Guide en tu Dockerfile
- [ ] Aplicaste mejoras sugeridas por el agent
- [ ] Feedback del agent es 100% positivo
- [ ] Documentaste aprendizajes del agent en `notes.md`

### Documentación del Proceso AI
- [ ] `infra/README.md` documenta el proceso AI-Powered
- [ ] Incluiste métricas (tamaño antes/después, build time)
- [ ] `notes.md` documenta qué delegaste a IA vs qué validaste tú
- [ ] Tienes apuntes para decisiones de despliegue (próxima clase)

### Herramientas
- [ ] Probaste `dive` para analizar capas de imagen
- [ ] (Opcional) Ejecutaste `hadolint` para linting del Dockerfile
- [ ] (Opcional) Escaneaste vulnerabilidades con `trivy`

**Meta final**: Infraestructura base lista, optimizada con IA, validada con agent educativo, y totalmente documentada.

---

En la próxima clase veremos cómo **convertir tu entorno local en uno reproducible**, con Docker o contenedores ligeros.

Tu API dejará de depender de “mi máquina funciona” y empezará a ser **portable y escalable**.