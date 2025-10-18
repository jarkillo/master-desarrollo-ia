# Clase 1 - Ciclo de vida del software y backlog ágil

En el **Módulo 1** la trama fue clara:

- **Clase 1**: aprendiste a pensar como dev → descomponer problemas, usar la terminal, y montar un CLI mínimo con `sys.argv`.
- **Clase 2**: le diste persistencia → tu CLI ya guardaba datos en JSON, con funciones bien separadas. La IA te mostró `argparse` y modularidad.
- **Clase 3**: apareció la disciplina → Clean Code y los primeros tests unitarios (`unittest`). Descubriste que refactorizar sin red de seguridad es un salto al vacío.
- **Clase 4 (bonus)**: probaste a escalar tu CLI con nuevas features (prioridades). Aquí los tests se convirtieron en alarma y guía. Viste el primer principio **SOLID** (SRP: Single Responsibility Principle).

Esa historia termina con tu CLI convertido en un pequeño **motor fiable**: tiene lógica separada, tests que lo protegen y ya no es un juguete que se rompe al primer soplido.

Ahora viene el **Módulo 2**: imagina que tu jefe te dice:

*"El CLI está guay… pero necesitamos una API para que el equipo de frontend pueda usarlo en una app web."*

Aquí empieza la nueva aventura: pasar de un **script individual** a un **servicio de software con arquitectura**.

Eso significa pensar en:

- **El ciclo de vida del software** (no solo escribir código, sino gestionarlo con backlog, sprints y entregas).
- **Principios SOLID completos** (no solo SRP).
- **Arquitecturas**: cuándo un monolito es suficiente, cuándo separar en módulos o microservicios, y cómo documentar decisiones (ADRs).

Mini-spoiler: igual que tu CLI empezó con `sys.argv` y terminó con tests y capas, ahora tu API empezará con un endpoint mínimo y terminará con una **mini-arquitectura limpia**.

---

Antes de seguir, una nota:

La mayoría de cursos de “IA para devs” empiezan con lo llamativo: prompts mágicos, agentes encadenados, autogpt’s que hacen café mientras tú ves Netflix. Suena espectacular… hasta que pruebas a usarlos en un proyecto real y el castillo se te cae encima porque no entiendes qué está pasando bajo el capó.

Aquí hicimos justo lo contrario: primero construiste **músculo de dev**. Aprendiste a pensar en problemas como ordenadores, a escribir un CLI que guarda cosas, a refactorizar y a testear. Puede sonar “más básico” que tener un ejército de agentes en cinco minutos, pero la diferencia es brutal: **tú sabes lo que está pasando**.

Ahora la IA se vuelve mucho más poderosa. Porque no vas a usarla como un generador de líneas mágicas, sino como un **equipo de juniors** que te ayudan siguiendo tus reglas:

- Un agente puede ser tu tester, que genera y ejecuta tests automáticamente.
- Otro agente puede actuar como arquitecto, sugiriendo cómo dividir módulos y dejando ADRs documentados.
- Incluso puedes tener un PM virtual que convierte historias de usuario en issues de GitHub.

Ese es el hype real: no es que la IA te quite trabajo, es que te multiplica, pero solo si tienes los fundamentos para dirigirla. Y justo eso es lo que estamos haciendo: te has ganado el derecho a que la IA trabaje contigo como **copiloto disciplinado**, no como mago impredecible.

Así que ahora sí: pasamos del **CLI de juguete** a una **API de verdad**, con backlog ágil, SOLID aplicado y agentes que te acompañan en el camino.

---

## Comencemos:

Genial, arrancamos **Clase 1 del Módulo 2 – Ciclo de vida del software y backlog ágil**.

## Concepto

Hasta ahora trabajabas casi en “modo artesano”: abres tu editor, picas código, haces commits y PRs. Eso está bien para un CLI pequeño, pero cuando construyes una API (aunque sea mini) ya necesitas **organizar el trabajo como un equipo**.

Ahí entra el **ciclo de vida del software**. Suena pomposo, pero en realidad es una coreografía simple:

1. **Backlog** → la lista de todo lo que queremos hacer (features, bugs, mejoras).
2. **Sprint** → elegir un subconjunto de ese backlog y comprometerte a completarlo en un período (1–2 semanas).
3. **Entrega** → al final del sprint, el producto tiene que “respirar”: algo que funcione, aunque sea pequeñito.
4. **Feedback** → revisas, corriges, ajustas prioridades, y arrancas otro sprint.

Con esto, no vas a estar meses programando en una cueva hasta enseñar algo: siempre tendrás un prototipo funcionando, listo para mostrar y probar.

## Aplicación manual

Vamos a simular el **primer backlog** para tu mini-API de tareas.

Historias de usuario (en formato clásico “Como… quiero… para…”):

- Como usuario quiero crear tareas vía API para gestionarlas desde apps externas.
- Como usuario quiero listar mis tareas para ver el estado.
- Como usuario quiero marcar tareas como completadas para llevar control.

Ese es tu **MVP (Minimum Viable Product)**: 3 endpoints básicos.

El backlog inicial también puede incluir cosas técnicas, como:

- Configurar un entorno de FastAPI.
- Documentar decisiones de arquitectura (ADRs).
- Preparar tests básicos de integración.

## Aplicación con IA

Aquí es donde la IA brilla. Puedes tratarla como un **Product Owner junior** que traduce tus historias en backlog técnico. Ejemplo de prompt:

```
Rol: Product Owner técnico.

Contexto: Tengo un mini-proyecto para una API REST de tareas con FastAPI.
Objetivo: Convierte estas historias de usuario en un backlog con issues de GitHub (cada issue con título, descripción y criterios de aceptación).

Historias:
- Como usuario quiero crear tareas vía API.
- Como usuario quiero listar mis tareas.
- Como usuario quiero marcar tareas como completadas.

Formato: Markdown con lista de issues.
```

La IA te devolverá algo parecido a un tablero inicial. Luego podrás pegarlo en GitHub Projects, Jira o Notion, y empezar a jugar como si fuese un proyecto real.

## Ejercicio práctico

1. Crea una rama `feature/backlog-api`.
2. Añade un archivo `Modulo2/api/notes.md`.
3. Dentro escribe las **3 historias de usuario** y el **backlog inicial** (puedes pedirle a la IA que lo expanda con criterios de aceptación).
4. Haz commit y PR. Ese será tu punto de partida para el módulo 2.

### Checklist rápida

- Entendiste qué es backlog y sprint.
- Tienes tus 3 historias de usuario como base del mini-proyecto.
- Tienes un `notes.md` con la primera versión del backlog.

---

## Parte 2: Del CLI a la API - Introducción a FastAPI (2h)

Ahora que tienes tu backlog definido, es momento de **pasar de la teoría a la práctica**.

En el Módulo 1 construiste un CLI que funcionaba en tu terminal. Pero imagina que quieres que tu sistema de tareas sea accesible desde:
- Una app móvil
- Una página web
- Otro servicio backend
- Un script de automatización

Todas esas aplicaciones necesitan **hablar con tu sistema**, y la forma moderna de hacerlo es mediante una **API REST**.

### ¿Qué es una API REST? (15 min)

**API** = Application Programming Interface (Interfaz de Programación de Aplicaciones)
**REST** = Representational State Transfer (un estilo de diseño para APIs web)

**Analogía del mostrador de restaurante:**

- **Tu CLI** = Cocina interna del restaurante (solo los empleados pueden usarlo)
- **Tu API** = Mostrador donde cualquiera puede pedir comida
- **Los endpoints** = Los platos del menú (crear tarea, listar tareas, etc.)
- **HTTP** = El idioma que usa el cliente para hacer el pedido

Cuando haces `POST /tareas` con `{"nombre": "Estudiar FastAPI"}`, es como decir:
> "Hola mostrador, quiero crear (POST) una tarea nueva con este nombre"

Y la API responde:
> "Vale, creada. Aquí está tu comprobante (JSON con id, nombre, completada)"

### Por qué FastAPI (15 min)

Hay muchos frameworks para crear APIs en Python:
- **Flask**: Simple, minimalista, muy popular
- **Django REST Framework**: Completo, pesado, ideal para proyectos grandes
- **FastAPI**: Moderno, rápido, con validación automática

Elegimos **FastAPI** porque:

1. **Validación automática con Pydantic**: defines qué esperas y FastAPI lo valida por ti
2. **Documentación automática**: Swagger UI generado sin escribir una línea extra
3. **Type hints**: usa las anotaciones de tipos de Python 3.6+
4. **Rápido**: rendimiento comparable a Node.js y Go
5. **Async nativo**: aunque empezaremos sin async, está listo cuando lo necesites

### Instalación desde cero (30 min)

#### Paso 1: Crear entorno virtual

Siempre trabaja en un entorno virtual para aislar las dependencias de tu proyecto:

```bash
# Navega a la carpeta de la clase
cd "Modulo 2 – Ingeniería y Arquitectura/Clase 1 - Ciclo de vida del sofware y backlog agil"

# Crea el entorno virtual
python -m venv .venv

# Activa el entorno virtual
# Windows:
.venv\Scripts\activate

# Linux/Mac:
source .venv/bin/activate
```

Tu terminal debería mostrar `(.venv)` al principio, indicando que el entorno está activo.

#### Paso 2: Instalar dependencias

```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar FastAPI y uvicorn (servidor ASGI)
pip install fastapi uvicorn

# Instalar herramientas para testing
pip install pytest httpx

# Instalar Pydantic (ya viene con FastAPI pero lo hacemos explícito)
pip install pydantic

# Guardar dependencias en archivo
pip freeze > requirements.txt
```

🧠 **Pausa de comprensión:**

- `fastapi`: El framework de la API
- `uvicorn`: El servidor que ejecuta tu API (como `python script.py` ejecuta un script)
- `pytest`: Framework de testing (ya lo conoces del Módulo 1)
- `httpx`: Cliente HTTP para testear APIs (como requests pero async-compatible)
- `pydantic`: Validación de datos con type hints

### Tu primer endpoint: Hello World (30 min)

Vamos a crear el endpoint más simple posible para verificar que todo funciona.

Crea el archivo `api/api.py`:

```python
# api/api.py
from fastapi import FastAPI

# Crear la aplicación FastAPI
app = FastAPI(
    title="API de Tareas",
    description="Una API simple para gestionar tareas",
    version="1.0.0"
)

# Endpoint de salud (health check)
@app.get("/health")
def health_check():
    """
    Endpoint para verificar que la API está funcionando.

    Útil para monitoreo y deployment.
    """
    return {"status": "ok", "message": "API de Tareas funcionando correctamente"}
```

#### Ejecutar el servidor

```bash
# Desde la carpeta de la clase
uvicorn api.api:app --reload
```

Deberías ver algo como:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Ahora abre tu navegador en `http://127.0.0.1:8000/health` y verás:

```json
{
  "status": "ok",
  "message": "API de Tareas funcionando correctamente"
}
```

🎉 **¡Tu primera API REST está viva!**

#### Explorar la documentación automática

FastAPI genera documentación interactiva automáticamente. Abre:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

En Swagger UI puedes:
- Ver todos tus endpoints
- Probar cada endpoint directamente desde el navegador
- Ver los modelos de datos (Request/Response)

Esto es **gratis**, no escribiste ni una línea de documentación.

### Request y Response con Pydantic (45 min)

Ahora vamos a crear un endpoint real: **crear una tarea**.

#### Paso 1: Definir el modelo de datos

Los modelos Pydantic son como contratos: definen qué campos esperas y qué tipos tienen.

Añade al archivo `api/api.py`:

```python
from pydantic import BaseModel, Field
from typing import Optional

# Modelo para la request (lo que el cliente envía)
class CrearTareaRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200,
                        description="Nombre de la tarea")
    descripcion: Optional[str] = Field(None, max_length=500,
                                       description="Descripción opcional de la tarea")

    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Estudiar FastAPI",
                "descripcion": "Completar el tutorial básico y hacer ejercicios"
            }
        }

# Modelo para la response (lo que la API devuelve)
class TareaResponse(BaseModel):
    id: int = Field(..., description="ID único de la tarea")
    nombre: str = Field(..., description="Nombre de la tarea")
    descripcion: Optional[str] = Field(None, description="Descripción de la tarea")
    completada: bool = Field(False, description="Estado de la tarea")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Estudiar FastAPI",
                "descripcion": "Completar el tutorial básico y hacer ejercicios",
                "completada": False
            }
        }
```

🧠 **Pausa de comprensión:**

- `Field(...)`: El `...` significa "requerido" (no puede ser None)
- `min_length=1`: Valida que el nombre no esté vacío
- `Optional[str]`: Puede ser string o None
- `Config.json_schema_extra`: Ejemplo que aparece en la documentación automática

#### Paso 2: Crear el endpoint

Ahora añade el endpoint que usa estos modelos:

```python
# Almacenamiento temporal en memoria (lo mejoraremos en Clase 2)
tareas_db = []
contador_id = 0

@app.post("/tareas", response_model=TareaResponse, status_code=201)
def crear_tarea(tarea: CrearTareaRequest):
    """
    Crea una nueva tarea.

    - **nombre**: Nombre de la tarea (requerido, 1-200 caracteres)
    - **descripcion**: Descripción opcional (máximo 500 caracteres)

    Devuelve la tarea creada con su ID asignado.
    """
    global contador_id
    contador_id += 1

    nueva_tarea = TareaResponse(
        id=contador_id,
        nombre=tarea.nombre,
        descripcion=tarea.descripcion,
        completada=False
    )

    tareas_db.append(nueva_tarea.model_dump())
    return nueva_tarea
```

🧠 **Pausa de comprensión:**

- `@app.post("/tareas")`: Este endpoint acepta peticiones POST a `/tareas`
- `response_model=TareaResponse`: FastAPI valida que la respuesta cumpla este modelo
- `status_code=201`: HTTP 201 = "Created" (estándar para creación exitosa)
- `tarea: CrearTareaRequest`: FastAPI automáticamente:
  - Lee el JSON del body de la petición
  - Lo valida contra el modelo
  - Si falla, devuelve HTTP 422 con detalles del error
  - Si pasa, lo convierte en un objeto Python

#### Paso 3: Añadir endpoint para listar tareas

```python
@app.get("/tareas", response_model=list[TareaResponse])
def listar_tareas():
    """
    Lista todas las tareas creadas.

    Devuelve un array de tareas (puede estar vacío si no hay ninguna).
    """
    return tareas_db
```

### Probar la API (10 min)

#### Opción 1: Desde Swagger UI

1. Ve a `http://127.0.0.1:8000/docs`
2. Expande `POST /tareas`
3. Click en "Try it out"
4. Edita el JSON de ejemplo:
   ```json
   {
     "nombre": "Aprender FastAPI",
     "descripcion": "Completar la Clase 1 del Módulo 2"
   }
   ```
5. Click en "Execute"
6. Verás la respuesta con HTTP 201 y tu tarea con id=1

#### Opción 2: Desde la terminal con curl

```bash
# Crear una tarea
curl -X POST "http://127.0.0.1:8000/tareas" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Aprender FastAPI", "descripcion": "Clase 1 completa"}'

# Listar tareas
curl http://127.0.0.1:8000/tareas
```

#### Opción 3: Con Python (usando httpx)

```python
import httpx

# Crear tarea
response = httpx.post(
    "http://127.0.0.1:8000/tareas",
    json={"nombre": "Aprender FastAPI", "descripcion": "Muy útil"}
)
print(response.status_code)  # 201
print(response.json())  # {"id": 1, "nombre": "...", ...}

# Listar tareas
response = httpx.get("http://127.0.0.1:8000/tareas")
print(response.json())  # [{"id": 1, ...}, ...]
```

### Validación automática en acción (10 min)

Prueba a enviar datos inválidos para ver cómo FastAPI los rechaza:

```bash
# Nombre vacío (viola min_length=1)
curl -X POST "http://127.0.0.1:8000/tareas" \
  -H "Content-Type: application/json" \
  -d '{"nombre": ""}'
```

Respuesta:
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "nombre"],
      "msg": "String should have at least 1 character",
      "input": "",
      "ctx": {"min_length": 1}
    }
  ]
}
```

FastAPI automáticamente:
- Detectó que `nombre` está vacío
- Devolvió HTTP 422 (Unprocessable Entity)
- Explicó exactamente qué está mal

**Esto es Pydantic trabajando para ti**, no tuviste que escribir ni un `if` para validar.

### Comparación: CLI vs API

| CLI (Módulo 1) | API (Módulo 2) |
|----------------|----------------|
| `python tareas.py agregar "Estudiar"` | `POST /tareas {"nombre": "Estudiar"}` |
| Solo accesible desde terminal | Accesible desde cualquier cliente HTTP |
| Entrada: argumentos de línea de comandos | Entrada: JSON en petición HTTP |
| Salida: print en terminal | Salida: JSON en respuesta HTTP |
| Usuario: tú | Usuario: cualquier aplicación |

### ✅ Checklist Parte 2

- [ ] Entiendes qué es una API REST y por qué es útil
- [ ] Instalaste FastAPI y uvicorn en un entorno virtual
- [ ] Creaste el endpoint `/health` y lo probaste en el navegador
- [ ] Exploraste la documentación automática en `/docs`
- [ ] Creaste modelos Pydantic para Request y Response
- [ ] Implementaste `POST /tareas` con validación automática
- [ ] Implementaste `GET /tareas` para listar
- [ ] Probaste la validación automática con datos inválidos
- [ ] Comprendes la diferencia entre CLI y API

---

## Parte 3: Aplicación con IA - 5 Ejercicios Prácticos (1.5h)

Ahora es el momento de **integrar la IA** en tu flujo de desarrollo. No como magia que escribe código por ti, sino como un **equipo de especialistas** que te ayudan a diseñar, validar y mejorar tu trabajo.

En el Módulo 0 aprendiste los fundamentos de la IA. Ahora los aplicamos a un proyecto real.

### 🤖 Ejercicio 1: IA como Product Owner (20 min)

**Objetivo**: Convertir tus historias de usuario en un backlog técnico estructurado.

#### Contexto

Tienes 3 historias de usuario básicas:
1. Como usuario quiero crear tareas vía API
2. Como usuario quiero listar mis tareas
3. Como usuario quiero marcar tareas como completadas

Un Product Owner experimentado las expandiría en issues técnicos con:
- Título claro
- Descripción detallada
- Criterios de aceptación medibles
- Tareas técnicas (subtareas)

#### Prompt para Claude Code / ChatGPT

```markdown
Rol: Product Owner técnico experimentado en metodologías ágiles.

Contexto: Estoy desarrollando una API REST de tareas con FastAPI. Tengo el MVP definido pero necesito convertirlo en un backlog técnico profesional.

Historias de usuario:
1. Como usuario quiero crear tareas vía API para gestionarlas desde apps externas
2. Como usuario quiero listar mis tareas para ver su estado
3. Como usuario quiero marcar tareas como completadas para llevar control

Tarea: Convierte cada historia en un issue de GitHub con:
- Título en formato: [FEAT] Descripción clara
- Descripción técnica
- Criterios de aceptación (formato Given-When-Then)
- Lista de tareas técnicas (checkboxes)
- Estimación de esfuerzo (S/M/L)

Formato: Markdown, listo para copiar/pegar en GitHub Issues.
```

#### Resultado esperado

La IA te devolverá 3 issues estructurados. Ejemplo:

```markdown
## Issue 1: [FEAT] Endpoint para crear tareas

### Descripción
Implementar endpoint POST /tareas que permita crear nuevas tareas con validación de entrada.

### Criterios de aceptación
- [ ] Given que envío POST /tareas con JSON válido
      When el nombre tiene 1-200 caracteres
      Then responde HTTP 201 con la tarea creada (id, nombre, completada=false)

- [ ] Given que envío POST /tareas con nombre vacío
      When valido la entrada
      Then responde HTTP 422 con detalles del error

### Tareas técnicas
- [ ] Crear modelo Pydantic CrearTareaRequest
- [ ] Crear modelo Pydantic TareaResponse
- [ ] Implementar endpoint POST /tareas
- [ ] Añadir validación min_length=1
- [ ] Escribir tests (mínimo 2: caso válido + caso inválido)
- [ ] Documentar en Swagger

### Estimación
M (Medium - 2-4 horas)
```

#### 📝 Acción

Copia estos issues en `api/notes.md` bajo una sección "Backlog Técnico".

---

### 🤖 Ejercicio 2: Setup de proyecto con IA (15 min)

**Objetivo**: Usar IA para generar la estructura de carpetas y archivos iniciales.

#### Prompt

```markdown
Rol: Senior Python Developer especializado en FastAPI.

Contexto: Inicio un proyecto de API REST con FastAPI para gestión de tareas. Necesito la estructura de carpetas profesional siguiendo buenas prácticas.

Requisitos:
- Separación de capas (API, lógica, datos)
- Tests unitarios y de integración separados
- Configuración de entorno virtual
- .gitignore apropiado para Python

Tarea: Genera la estructura de carpetas y el contenido de:
1. Estructura completa de directorios
2. .gitignore para Python/FastAPI
3. README.md básico con instrucciones de setup
4. requirements.txt con versiones específicas

Formato: Lista de comandos bash para crear todo + contenido de archivos.
```

#### Resultado esperado

```bash
# Estructura de carpetas
mkdir -p api tests tests_integrations docs

# Crear __init__.py
touch api/__init__.py tests/__init__.py tests_integrations/__init__.py

# .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual Environment
.venv/
venv/
ENV/

# FastAPI / Testing
.pytest_cache/
.coverage
htmlcov/

# IDEs
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Environment variables
.env
.env.local
EOF

# requirements.txt con versiones específicas
cat > requirements.txt << 'EOF'
fastapi==0.115.0
uvicorn[standard]==0.32.0
pydantic==2.10.3
pytest==8.4.2
httpx==0.27.2
pytest-cov==6.0.0
EOF
```

#### 📝 Acción

Ejecuta los comandos generados y verifica que la estructura se creó correctamente.

---

### 🤖 Ejercicio 3: Validación con FastAPI Design Coach (20 min)

**Objetivo**: Usar un agente educativo para revisar tu código y aprender mejores prácticas.

#### Contexto

Ahora tienes código FastAPI básico funcionando. Es momento de que un "senior" lo revise.

El agente **FastAPI Design Coach** (`.claude/agents/educational/fastapi-design-coach.md`) está diseñado para:
- Detectar anti-patrones en APIs REST
- Sugerir mejoras en Pydantic models
- Validar status codes HTTP
- Enseñar buenas prácticas de FastAPI

#### Cómo invocar al agente (en Claude Code CLI)

```bash
# Desde la terminal de Claude Code
/agent fastapi-design-coach

# O directamente en conversación:
"Usa el agente FastAPI Design Coach para revisar mi archivo api/api.py"
```

#### Prompt para el agente

```markdown
Revisar el siguiente código FastAPI y proporcionar feedback educativo:

[Pegar el contenido de api/api.py]

Enfócate en:
1. Uso correcto de status codes HTTP
2. Validación Pydantic (¿falta alguna validación importante?)
3. Estructura de responses (¿son consistentes?)
4. Documentación (docstrings y ejemplos en Swagger)
5. Mejores prácticas de FastAPI que no estoy aplicando
```

#### Resultado esperado

El agente te responderá con algo como:

```markdown
## Revisión FastAPI Design Coach

### ✅ Lo que está bien:
- Status code 201 para POST /tareas (correcto para creación)
- Uso de Pydantic models para request/response
- Documentación automática configurada

### ⚠️ Oportunidades de mejora:

1. **Falta validación de descripción en GET**
   ```python
   # Actual:
   descripcion: Optional[str] = Field(None, ...)

   # Mejor:
   descripcion: Optional[str] = Field(
       None,
       max_length=500,
       description="Descripción de la tarea"
   )
   ```
   **Por qué**: Siempre limita el tamaño de campos de texto para evitar abusos.

2. **Almacenamiento global no es thread-safe**
   ```python
   # Actual:
   tareas_db = []
   contador_id = 0

   # Mejor (para Clase 2):
   # Usar un repositorio con lock o una clase singleton
   ```
   **Por qué**: Variables globales causan problemas en entornos multi-thread.

3. **Falta endpoint para obtener tarea por ID**
   ```python
   @app.get("/tareas/{tarea_id}", response_model=TareaResponse)
   def obtener_tarea(tarea_id: int):
       # Implementar búsqueda por ID
       pass
   ```
   **Por qué**: En REST, deberías poder obtener un recurso específico.

### 📚 Concepto a aprender:
**Idempotencia en HTTP**: POST no es idempotente (crear 2 veces = 2 recursos).
GET, PUT, DELETE sí lo son. Esto afecta diseño de APIs.
```

#### 📝 Acción

1. Lee el feedback del agente
2. Implementa las mejoras sugeridas
3. Anota los conceptos nuevos en `api/notes.md` bajo "Aprendizajes"

---

### 🤖 Ejercicio 4: TDD Básico con IA (25 min)

**Objetivo**: Aplicar Test-Driven Development con ayuda de IA.

**TDD** = Escribir el test ANTES que el código (ciclo RED → GREEN → REFACTOR)

#### Fase RED: Escribir el test (con ayuda de IA)

**Prompt:**

```markdown
Rol: QA Engineer experto en pytest y FastAPI.

Contexto: Estoy aplicando TDD para un endpoint GET /tareas/{tarea_id} que debe:
- Devolver HTTP 200 con la tarea si existe
- Devolver HTTP 404 si no existe

Tarea: Escribe los tests pytest para este endpoint ANTES de implementarlo.

Requisitos:
- Usar TestClient de FastAPI
- 2 tests: caso éxito (200) y caso error (404)
- Nombres descriptivos de tests
- Docstrings explicando qué valida cada test

Formato: Código Python listo para copiar en tests/test_obtener_tarea.py
```

#### Resultado de la IA

```python
# tests/test_obtener_tarea.py
from fastapi.testclient import TestClient
from api.api import app

client = TestClient(app)

def test_obtener_tarea_existente_devuelve_200_y_tarea():
    """
    Given: Existe una tarea con id=1
    When: Hago GET /tareas/1
    Then: Responde HTTP 200 con la tarea completa
    """
    # Arrange: Crear una tarea primero
    response_crear = client.post("/tareas", json={"nombre": "Test tarea"})
    tarea_id = response_crear.json()["id"]

    # Act: Obtener la tarea
    response = client.get(f"/tareas/{tarea_id}")

    # Assert
    assert response.status_code == 200
    tarea = response.json()
    assert tarea["id"] == tarea_id
    assert tarea["nombre"] == "Test tarea"
    assert tarea["completada"] is False


def test_obtener_tarea_inexistente_devuelve_404():
    """
    Given: No existe tarea con id=9999
    When: Hago GET /tareas/9999
    Then: Responde HTTP 404 con mensaje de error
    """
    # Act
    response = client.get("/tareas/9999")

    # Assert
    assert response.status_code == 404
    assert "detail" in response.json()
```

#### Ejecutar el test (debe FALLAR)

```bash
pytest tests/test_obtener_tarea.py -v
```

Resultado esperado:
```
FAILED tests/test_obtener_tarea.py::test_obtener_tarea_existente_devuelve_200_y_tarea
  404 != 200  # El endpoint no existe todavía
```

🎯 **Estás en fase RED** (test falla como esperado)

#### Fase GREEN: Implementar el código mínimo

Ahora pide a la IA:

```markdown
Implementa el endpoint GET /tareas/{tarea_id} que haga pasar estos tests:
[Pegar el código de los tests]

Requisitos:
- Buscar en tareas_db por id
- Devolver 200 si existe
- Devolver 404 si no existe (usar HTTPException de FastAPI)
```

La IA generará:

```python
from fastapi import HTTPException

@app.get("/tareas/{tarea_id}", response_model=TareaResponse)
def obtener_tarea(tarea_id: int):
    """
    Obtiene una tarea específica por su ID.

    - **tarea_id**: ID de la tarea a buscar

    Devuelve HTTP 404 si la tarea no existe.
    """
    for tarea in tareas_db:
        if tarea["id"] == tarea_id:
            return tarea

    raise HTTPException(status_code=404, detail=f"Tarea con id={tarea_id} no encontrada")
```

Ejecuta los tests de nuevo:

```bash
pytest tests/test_obtener_tarea.py -v
```

```
PASSED tests/test_obtener_tarea.py::test_obtener_tarea_existente_devuelve_200_y_tarea
PASSED tests/test_obtener_tarea.py::test_obtener_tarea_inexistente_devuelve_404
```

🎯 **Estás en fase GREEN** (tests pasan)

#### Fase REFACTOR: Mejorar con agentes

Ahora usa el **API Design Reviewer** para validar:

```markdown
/agent api-design-reviewer

Revisa este endpoint GET /tareas/{tarea_id}:
[Pegar el código]

¿Sigue buenas prácticas REST? ¿El status code es correcto? ¿Falta algo?
```

#### 📝 Acción

1. Implementa el ciclo completo TDD (RED-GREEN-REFACTOR)
2. Documenta el proceso en `api/notes.md`
3. Anota qué aprendiste sobre TDD con IA

---

### 🤖 Ejercicio 5: Documentación con IA (10 min)

**Objetivo**: Generar documentación de decisiones de arquitectura (ADR).

#### ¿Qué es un ADR?

**ADR** = Architecture Decision Record

Es un documento breve que explica:
1. **Contexto**: ¿Por qué necesitamos decidir esto?
2. **Decisión**: ¿Qué elegimos?
3. **Consecuencias**: ¿Qué implica esta decisión?

#### Prompt para generar ADR

```markdown
Rol: Arquitecto de software senior.

Contexto: He decidido usar FastAPI (en lugar de Flask o Django) para una API de tareas educativa.

Tarea: Escribe un ADR (Architecture Decision Record) documentando esta decisión.

Formato ADR estándar:
# ADR-001: [Título]
## Estado: Aceptado
## Contexto
## Decisión
## Consecuencias (positivas y negativas)
## Alternativas consideradas
```

#### Resultado esperado

```markdown
# ADR-001: Uso de FastAPI como framework para API REST

## Estado
Aceptado

## Contexto
Necesitamos construir una API REST para gestión de tareas con:
- Validación automática de entrada/salida
- Documentación interactiva para aprendizaje
- Rendimiento aceptable para escalar
- Código moderno con type hints (Python 3.9+)

## Decisión
Usar **FastAPI** como framework web principal.

## Consecuencias

### Positivas
- Validación automática con Pydantic (menos código boilerplate)
- Swagger UI generado automáticamente (útil para enseñar)
- Type hints nativos mejoran IDE support y detección de errores
- Performance comparable a Node.js/Go (si escalamos)
- Async/await nativo para futuro (aunque empezamos sin async)

### Negativas
- Menos maduro que Flask (menos ejemplos legacy)
- Requiere Python 3.7+ (no es problema en 2025)
- Curva de aprendizaje ligeramente mayor que Flask (pero mejor ROI)

## Alternativas consideradas

1. **Flask + marshmallow**
   - Pro: Más ejemplos, más maduro
   - Con: Validación manual, documentación manual

2. **Django REST Framework**
   - Pro: Muy completo, admin incluido
   - Con: Demasiado pesado para MVP, más complejo

## Referencias
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Pydantic v2](https://docs.pydantic.dev/)
```

#### 📝 Acción

1. Guarda este ADR en `docs/adr/001-fastapi.md`
2. Crea ADRs adicionales para otras decisiones (almacenamiento en memoria, estructura de proyecto, etc.)

---

### ✅ Checklist Parte 3

- [ ] Usaste IA como Product Owner para crear backlog técnico
- [ ] Generaste estructura de proyecto con prompts a IA
- [ ] Revisaste tu código con FastAPI Design Coach
- [ ] Aplicaste ciclo TDD (RED-GREEN-REFACTOR) con ayuda de IA
- [ ] Generaste ADRs para documentar decisiones arquitectónicas
- [ ] Comprendes cómo la IA actúa como "equipo de especialistas"
- [ ] Guardaste todos los prompts usados en `api/notes.md` para referencia futura

---

## Parte 4: Proyecto Final de Clase (1h)

Es momento de consolidar todo lo aprendido en un **proyecto funcional completo**.

Al final de esta parte tendrás:
- Una mini-API REST funcional con 3-4 endpoints
- Tests automatizados que validan el comportamiento
- Documentación generada automáticamente
- Backlog técnico documentado
- Estructura preparada para escalar en la Clase 2

### 🎯 Especificación del Proyecto

**Nombre**: Mini API de Tareas v1.0

**Endpoints requeridos**:

1. `GET /health` - Health check (ya lo tienes)
2. `POST /tareas` - Crear tarea (ya lo tienes)
3. `GET /tareas` - Listar todas las tareas (ya lo tienes)
4. `GET /tareas/{tarea_id}` - Obtener tarea por ID (ejercicio 4)
5. `PATCH /tareas/{tarea_id}/completar` - Marcar tarea como completada (NUEVO)

**Criterios de aceptación**:
- Todos los endpoints funcionando
- Validación Pydantic en todos los endpoints
- Mínimo 6 tests (2 por endpoint principal)
- Cobertura de tests > 70%
- Documentación Swagger completa
- Sin errores de linting (ruff)

### Paso 1: Implementar endpoint PATCH /completar (20 min)

Este es el último endpoint que falta para completar el MVP.

#### Con TDD (escribe el test primero)

```python
# tests/test_completar_tarea.py
from fastapi.testclient import TestClient
from api.api import app

client = TestClient(app)

def test_completar_tarea_existente_devuelve_200():
    """
    Given: Existe una tarea sin completar
    When: Hago PATCH /tareas/{id}/completar
    Then: Responde 200 y la tarea tiene completada=True
    """
    # Arrange: Crear tarea
    response_crear = client.post("/tareas", json={"nombre": "Tarea a completar"})
    tarea_id = response_crear.json()["id"]

    # Act: Completar la tarea
    response = client.patch(f"/tareas/{tarea_id}/completar")

    # Assert
    assert response.status_code == 200
    tarea = response.json()
    assert tarea["id"] == tarea_id
    assert tarea["completada"] is True


def test_completar_tarea_inexistente_devuelve_404():
    """
    Given: No existe tarea con id=9999
    When: Intento completarla
    Then: Responde 404
    """
    response = client.patch("/tareas/9999/completar")
    assert response.status_code == 404
```

Ejecuta el test (debe fallar - fase RED):

```bash
pytest tests/test_completar_tarea.py -v
```

#### Implementación (fase GREEN)

Añade el endpoint a `api/api.py`:

```python
@app.patch("/tareas/{tarea_id}/completar", response_model=TareaResponse)
def completar_tarea(tarea_id: int):
    """
    Marca una tarea como completada.

    - **tarea_id**: ID de la tarea a completar

    Devuelve HTTP 404 si la tarea no existe.
    """
    for tarea in tareas_db:
        if tarea["id"] == tarea_id:
            tarea["completada"] = True
            return tarea

    raise HTTPException(status_code=404, detail=f"Tarea con id={tarea_id} no encontrada")
```

Ejecuta el test de nuevo (debe pasar - fase GREEN):

```bash
pytest tests/test_completar_tarea.py -v
```

### Paso 2: Ejecutar todos los tests (10 min)

Ahora que tienes todos los endpoints, ejecuta la suite completa de tests:

```bash
# Ejecutar todos los tests con verbose
pytest -v

# Ejecutar con cobertura
pytest --cov=api --cov-report=term-missing

# Ejecutar solo si quieres ver HTML de cobertura
pytest --cov=api --cov-report=html
# Luego abre htmlcov/index.html en el navegador
```

**Objetivo**: Cobertura > 70%

Si tienes menos cobertura, identifica qué líneas no están cubiertas y añade tests para ellas.

### Paso 3: Validar con linting (5 min)

Asegúrate de que el código sigue las convenciones de Python:

```bash
# Instalar ruff si no lo tienes
pip install ruff

# Ejecutar linting
ruff check api/

# Autofix automático (para algunos errores)
ruff check api/ --fix
```

Si hay errores, corrígelos antes de continuar.

### Paso 4: Documentar el proyecto (15 min)

Crea un `README.md` en la carpeta de la clase:

```markdown
# Mini API de Tareas - Clase 1 Módulo 2

API REST simple para gestión de tareas, construida con FastAPI como introducción al desarrollo backend moderno.

## Características

- CRUD completo de tareas (Crear, Listar, Obtener, Completar)
- Validación automática con Pydantic
- Documentación interactiva con Swagger UI
- Tests automatizados con pytest
- Almacenamiento en memoria (se mejorará en Clase 2)

## Requisitos

- Python 3.9+
- pip

## Instalación

### 1. Crear entorno virtual

\`\`\`bash
python -m venv .venv

# Activar (Windows)
.venv\\Scripts\\activate

# Activar (Linux/Mac)
source .venv/bin/activate
\`\`\`

### 2. Instalar dependencias

\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Uso

### Ejecutar el servidor

\`\`\`bash
uvicorn api.api:app --reload
\`\`\`

El servidor estará disponible en `http://127.0.0.1:8000`

### Documentación interactiva

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Endpoints

| Método | Endpoint | Descripción | Status Codes |
|--------|----------|-------------|--------------|
| GET | `/health` | Health check | 200 |
| POST | `/tareas` | Crear tarea | 201, 422 |
| GET | `/tareas` | Listar tareas | 200 |
| GET | `/tareas/{id}` | Obtener tarea por ID | 200, 404 |
| PATCH | `/tareas/{id}/completar` | Completar tarea | 200, 404 |

## Ejemplos de uso

### Crear una tarea

\`\`\`bash
curl -X POST "http://127.0.0.1:8000/tareas" \\
  -H "Content-Type: application/json" \\
  -d '{"nombre": "Aprender FastAPI", "descripcion": "Completar Clase 1"}'
\`\`\`

### Listar tareas

\`\`\`bash
curl http://127.0.0.1:8000/tareas
\`\`\`

### Completar una tarea

\`\`\`bash
curl -X PATCH "http://127.0.0.1:8000/tareas/1/completar"
\`\`\`

## Testing

### Ejecutar tests

\`\`\`bash
pytest -v
\`\`\`

### Con cobertura

\`\`\`bash
pytest --cov=api --cov-report=term-missing
\`\`\`

## Estructura del Proyecto

\`\`\`
├── api/
│   ├── __init__.py
│   ├── api.py              # Endpoints de la API
│   └── notes.md            # Backlog y notas del proyecto
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # Configuración de pytest
│   ├── test_health.py
│   ├── test_crear_tarea_clase1.py
│   ├── test_obtener_tarea.py
│   └── test_completar_tarea.py
├── docs/
│   └── adr/
│       └── 001-fastapi.md  # Architecture Decision Records
├── requirements.txt
├── .gitignore
└── README.md
\`\`\`

## Próximos pasos (Clase 2)

- Aplicar principios SOLID en profundidad
- Separar en capas (API, Servicio, Repositorio)
- Implementar persistencia en JSON
- Añadir inyección de dependencias

## Licencia

Proyecto educativo - Módulo 2 del Master en IA para Desarrollo
\`\`\`

### Paso 5: Crear PR y preparar para revisión (10 min)

#### Commit con conventional commits

```bash
git add .
git commit -m "feat(m2-clase1): completar Clase 1 con FastAPI + IA integration

- Añadir Parte 2: Introducción a FastAPI (2h de contenido)
- Añadir Parte 3: 5 ejercicios prácticos con IA (1.5h)
- Añadir Parte 4: Proyecto final completo (1h)
- Implementar endpoints: health, crear, listar, obtener, completar
- Añadir tests con >70% cobertura
- Documentar backlog técnico y ADRs
- Integrar agentes educativos (FastAPI Coach, API Reviewer)

Closes JAR-201"
```

#### Crear Pull Request

```bash
# Hacer push de la rama
git push origin feature/jar-201-completar-clase-1

# Crear PR con gh CLI
gh pr create --base dev \\
  --title "feat(M2-C1): Completar Clase 1 - Introducción a FastAPI + IA" \\
  --body "## Resumen

Completa la Clase 1 del Módulo 2 con contenido de 6 horas incluyendo:

### Parte 1: Ciclo de vida y backlog ágil (1.5h)
- ✅ Mantiene contenido original
- ✅ Expande con ejercicios reflexivos

### Parte 2: Introducción a FastAPI (2h)
- ✅ Instalación desde cero
- ✅ Endpoint Hello World (/health)
- ✅ Request/Response con Pydantic
- ✅ Validación automática
- ✅ Documentación Swagger

### Parte 3: Aplicación con IA (1.5h)
- ✅ Ejercicio 1: IA como Product Owner
- ✅ Ejercicio 2: Setup de proyecto con IA
- ✅ Ejercicio 3: Validación con FastAPI Design Coach
- ✅ Ejercicio 4: TDD básico con IA
- ✅ Ejercicio 5: Documentación con ADRs

### Parte 4: Proyecto final (1h)
- ✅ Mini-API funcional con 5 endpoints
- ✅ Tests automatizados (cobertura >70%)
- ✅ README.md completo
- ✅ Estructura preparada para Clase 2

## Criterios de aceptación (JAR-201)

- [x] Archivo .md completo similar a Clase 2
- [x] 6 horas de contenido estructurado
- [x] Ejercicios con soluciones (5 ejercicios)
- [x] 40% AI integration
- [x] Instalación FastAPI desde cero
- [x] Primer endpoint Hello World
- [x] Request/Response models con Pydantic
- [x] Proyecto final de clase

## Testing

\`\`\`bash
cd \"Modulo 2 – Ingeniería y Arquitectura/Clase 1 - Ciclo de vida del sofware y backlog agil\"
pytest --cov=api --cov-report=term-missing
ruff check api/
\`\`\`

## Integración con agentes

Usa los siguientes agentes durante la revisión:
- \`.claude/agents/educational/fastapi-design-coach.md\`
- \`.claude/agents/educational/api-design-reviewer.md\`
- \`.claude/agents/educational/python-best-practices-coach.md\`

## Notas

- No rompe la secuencia pedagógica (Clase 2 sigue construyendo sobre esto)
- Mantiene backlog ágil que conecta con Clase 4
- Introduce FastAPI prácticamente sin profundizar en arquitectura (eso es Clase 2-3)

Closes #JAR-201"
```

### ✅ Checklist Parte 4

- [ ] Implementaste endpoint PATCH /completar con TDD
- [ ] Ejecutaste todos los tests con >70% cobertura
- [ ] Validaste código con ruff (sin errores)
- [ ] Creaste README.md completo con ejemplos
- [ ] Hiciste commit siguiendo conventional commits
- [ ] Creaste PR apuntando a dev
- [ ] PR incluye descripción detallada con checklist de criterios de aceptación
- [ ] Comprendes el flujo completo de desarrollo (Backlog → Código → Tests → Docs → PR)

---

## 🎓 Resumen Final de la Clase

### Lo que aprendiste (6 horas de contenido)

**Parte 1 - Gestión (1.5h)**:
- Ciclo de vida del software (backlog, sprints, entregas)
- Historias de usuario en formato profesional
- MVP (Minimum Viable Product)

**Parte 2 - FastAPI Práctico (2h)**:
- Qué es una API REST y por qué es importante
- Instalación de FastAPI desde cero
- Endpoint Hello World y documentación automática
- Request/Response con Pydantic
- Validación automática de entrada

**Parte 3 - IA como equipo (1.5h)**:
- IA como Product Owner (generar backlog técnico)
- IA para setup de proyectos
- Agentes educativos para revisión de código
- TDD con ayuda de IA (RED-GREEN-REFACTOR)
- Documentación con ADRs

**Parte 4 - Proyecto completo (1h)**:
- Mini-API funcional con 5 endpoints
- Suite de tests automatizados
- Linting y cobertura de código
- Documentación profesional
- Flujo completo de desarrollo con Git

### Habilidades desbloqueadas

✅ Entiendes la diferencia entre CLI y API
✅ Sabes instalar y configurar un entorno Python profesional
✅ Puedes crear endpoints REST con FastAPI
✅ Aplicas validación automática con Pydantic
✅ Usas IA como equipo de especialistas (no como magia)
✅ Sigues TDD básico (test primero, luego código)
✅ Documentas decisiones con ADRs
✅ Creas PRs profesionales con conventional commits

### Conexión con Clase 2

En la próxima clase aplicarás **SOLID en profundidad**:
- Single Responsibility Principle (SRP) → separar capas
- Open/Closed Principle (OCP) → extensible sin modificar
- Dependency Inversion (DIP) → inyectar repositorios

Tu código actual tiene todo mezclado en `api.py`. En Clase 2 lo separarás en:
- `api.py` → Solo endpoints HTTP
- `servicio_tareas.py` → Lógica de negocio
- `repositorio_*.py` → Persistencia (memoria/JSON)

Esa separación hará que tu código sea **testeable, mantenible y escalable**.

### ✅ Checklist Final de la Clase

- [ ] Completaste las 4 partes (6 horas de contenido)
- [ ] Tienes una mini-API funcional corriendo en tu máquina
- [ ] Exploraste Swagger UI en `/docs`
- [ ] Ejecutaste tests con >70% cobertura
- [ ] Aplicaste al menos 3 de los 5 ejercicios con IA
- [ ] Documentaste tu backlog técnico en `api/notes.md`
- [ ] Creaste tu PR siguiendo el flujo Git profesional
- [ ] Comprendes que la IA es un equipo, no un mago
- [ ] Estás listo para la Clase 2 (arquitectura en capas)

---

¡Felicidades! Has completado la Clase 1 del Módulo 2.

Pasaste de entender **qué es un backlog** a tener una **API REST funcional** con tests, documentación y flujo profesional de desarrollo.

En la Clase 2 elevarás la calidad de este código aplicando principios SOLID y arquitectura limpia. Nos vemos allí.