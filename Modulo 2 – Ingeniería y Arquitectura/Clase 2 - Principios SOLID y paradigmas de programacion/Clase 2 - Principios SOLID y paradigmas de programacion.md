# 🎓 Clase 2 - Principios SOLID y paradigmas de programación
*(Módulo 2 – Ingeniería y Arquitectura)*

---

## 🎬 Escena 1 – Del taller al laboratorio

En el módulo anterior, tu CLI ya funcionaba.

Guardaba tareas, tenía tests, incluso aplicaste Clean Code y SRP sin darte cuenta.

Ahora empieza una nueva etapa:

> “Necesitamos una API para que otros programas usen tu sistema de tareas.”
> 

Y tú piensas: *“¿API? ¿endpoint? ¿FastAPI? ¿esto no era un curso de IA?”*

Sí, pero aquí **no escribimos APIs mágicas**: las diseñamos **como ingenieros**.

Y eso significa: entender principios, diseñar bien, probar antes de tocar.

Por eso hoy haremos **tu primer endpoint con TDD** y aprenderás **por qué cada línea existe**, no solo qué escribir.

---

## 🧩 Escena 2 – Las reglas que te salvarán del caos (SOLID en versión humana)

No te las aprendas de memoria todavía. Solo quiero que las **sientas**.

| Principio | Traducción humana |
| --- | --- |
| **S**ingle Responsibility | Cada parte del código debe tener un motivo único para cambiar. |
| **O**pen/Closed | Puedes extender sin romper. |
| **L**iskov Substitution | Si algo se comporta como un pato, debería reemplazar al pato sin romper nada. |
| **I**nterface Segregation | Mejor interfaces pequeñas que una gigante que obligue a implementarlo todo. |
| **D**ependency Inversion | No dependas de detalles, sino de abstracciones. |

Hoy verás el primero en acción: **SRP**, el principio de una sola responsabilidad.

---

## ⚙️ Escena 3 – Entendiendo el problema antes del código

Queremos esta historia de usuario:

> Cuando un usuario envía POST /tareas con {"nombre": "Estudiar SOLID"},
> 
> 
> el servidor responde **201** (creado) y un JSON con:
> 
> ```json
> { "id": 1, "nombre": "Estudiar SOLID", "completada": false }
> ```
> 
> Si el nombre va vacío, responde **422** (error de validación).
> 

Esa historia **es nuestro test**.

---

## 🧪 Escena 4 – Escribiendo el test primero (TDD: el contrato)

Crea la carpeta `Clase2/tests/test_crear_tarea.py` y escribe:

```python
from fastapi.testclient import TestClient
from api.api import app  # aún no existe, lo haremos después

cliente_http = TestClient(app)

def test_crear_tarea_minima_devuelve_201_y_cuerpo_esperado():
    cuerpo_peticion = {"nombre": "Estudiar SOLID"}
    respuesta = cliente_http.post("/tareas", json=cuerpo_peticion)
    assert respuesta.status_code == 201

    cuerpo_respuesta = respuesta.json()
    assert cuerpo_respuesta["id"] == 1
    assert cuerpo_respuesta["nombre"] == "Estudiar SOLID"
    assert cuerpo_respuesta["completada"] is False

def test_crear_tarea_con_nombre_vacio_devuelve_422():
    respuesta = cliente_http.post("/tareas", json={"nombre": ""})
    assert respuesta.status_code == 422

```

---

### 🧠 Pausa de comprensión

**¿Qué estás haciendo aquí?**

- `TestClient(app)` crea un **servidor fantasma**: no hay nada corriendo aún, pero simula peticiones HTTP.
- `respuesta = cliente_http.post(...)` es como decir *“mando una carta al servidor y espero su respuesta”*.
- `assert respuesta.status_code == 201` significa *“la historia solo se cumple si el servidor contesta ‘creado’”*.

Así que este test no prueba el código: **prueba la historia**.

Cuando lo ejecutes con:

```bash
pytest -q
```

fallará con un error tipo:

```
ModuleNotFoundError: No module named 'api'
```

Perfecto. Estás en la fase **Red** del ciclo TDD: nada funciona aún.

---

## 🧰 Escena 5 – Preparando el entorno

Antes de tocar nada, crea tu entorno limpio.

```bash
python -m venv .venv
.venv\Scripts\activate  # (Windows)
# o
source .venv/bin/activate  # (mac/Linux)
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn pytest httpx
pip freeze > requirements.txt

```

🧩 **Traducción mental**

“Estoy creando un laboratorio cerrado para mis experimentos.

Todo lo que instale vive aquí, no en mi ordenador global.”

---

## 🔨 Escena 6 – Construyendo el código mínimo

Crea tu estructura:

```
Clase2/
 ├─ api/
 │   ├─ __init__.py
 │   └─ api.py
 └─ tests/
     ├─ conftest.py
     └─ test_crear_tarea.py
```

`__init__.py` puede estar vacío. Solo dice:

> “Esta carpeta contiene código Python importable.”
> 

Y ahora el esqueleto de la API:

```python
# api/api.py
from fastapi import FastAPI
from pydantic import BaseModel

class CrearTareaRequest(BaseModel):
    nombre: str  # sin validación todavía

app = FastAPI()

@app.post("/tareas", status_code=201)
def crear_tarea(cuerpo: CrearTareaRequest):
    return {
        "id": 1,
        "nombre": cuerpo.nombre,
        "completada": False,
    }

```

---

### 🧠 Pausa de comprensión

- `FastAPI()` crea tu servidor.
- `@app.post("/tareas")` significa *“cuando alguien haga POST a /tareas, ejecuta esta función”*.
- `BaseModel` (de Pydantic) define **qué campos esperas** en el cuerpo de la petición.

Por ahora, el código **siempre devuelve id=1**, da igual cuántas veces lo llames.

Y eso está bien: **TDD no busca belleza, busca cumplir el contrato**.

---

### 🔗 Arreglando el import (el error feo de antes)

A veces `pytest` no sabe dónde está `api/`.

Crea `tests/conftest.py` con esto:

```python
import sys
from pathlib import Path

raiz_proyecto = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(raiz_proyecto))
```

Ahora vuelve a ejecutar:

```bash
pytest -q
```

Uno de tus tests pasará ✅, el otro fallará ❌.

### 🧠 Pausa de comprensión

`conftest.py` solo le dice a Python **“oye, sube un nivel y mira ahí”** para encontrar tu carpeta `api/`.

- `import sys` → te deja tocar la configuración interna de Python.
- `from pathlib import Path` → sirve para manejar rutas sin volverte loco con las barras.
- `Path(__file__).resolve().parents[1]` → coge la ruta del archivo actual (`tests/conftest.py`) y sube una carpeta.
- `sys.path.insert(0, str(raiz_proyecto))` → añade esa carpeta al radar de búsqueda de Python.

Sin eso, Python solo mira dentro de `tests/` y te suelta el error “No module named api”.

Con eso, ya sabe mirar hacia la raíz del proyecto y encuentra tu `api/api.py`.

---

## 🧠 Escena 7 – Validando el nombre (segunda iteración TDD)

Queremos que si el nombre va vacío, la API devuelva **422**.

Edita tu modelo:

```python
from pydantic import BaseModel, Field

class CrearTareaRequest(BaseModel):
    nombre: str = Field(..., min_length=1)
```

Ejecuta otra vez:

```bash
pytest -q
```

🎉 Ambos tests verdes.

---

### 📖 Qué aprendiste aquí (sin darte cuenta)

| Línea | Qué significa en lenguaje humano |
| --- | --- |
| `status_code=201` | “Confirmo que creé algo nuevo.” |
| `Field(..., min_length=1)` | “El nombre no puede ir vacío.” |
| `pytest -q` | “Comprueba si mis promesas se cumplen.” |
| `return {...}` | “Devuelvo lo que prometí: id, nombre, completada.” |

---

## 💬 Escena 8 – ¿Qué estamos realmente testeando?

No estás probando si FastAPI funciona.

Estás comprobando **tu contrato con el mundo exterior**:

1. Si alguien envía un JSON correcto → respondes 201.
2. Si alguien envía un JSON inválido → respondes 422.

Tus tests son como **las reglas de un juego**.

Y tu código solo gana si las cumple todas.

---

## 🧭 Escena 9 – Primer principio SOLID en acción (SRP)

- Tu test tiene una **única responsabilidad**: verificar el contrato.
- Tu endpoint tiene una **única responsabilidad**: crear una tarea.
- Tu modelo tiene una **única responsabilidad**: validar datos.

Eso es **SRP**. No hace falta decirlo, lo estás aplicando sin darte cuenta.

---

## 🧠 Escena 10 – Comprensión activa

**Haz este ejercicio:**

1. Lee tu función `crear_tarea`.
2. Explícala sin usar la palabra “función”.
    
    Ejemplo:
    
    > “Cuando alguien me manda una tarea, la reviso, le pongo un número, y se la devuelvo con sello de recibido.”
    > 

Eso es entender código de verdad.

---

## 🤖 Escena 11 – Aplicación con IA (como compañero de laboratorio)

Una vez que entiendes lo que hace tu código, ahora sí puedes pedir ayuda inteligente.

Prompt:

```
Rol: Arquitecto Python senior.
Contexto: Tengo una API FastAPI con POST /tareas y tests que pasan.
Objetivo: Enséñame cómo separar la lógica de negocio de la capa API (repositorio simulado), sin romper los tests.
```

La IA te devolverá código más modular:

`RepositorioDeTareas`, `servicio.crear_tarea()`, etc.

Pero esta vez tú sabrás **qué hace cada pieza** y por qué existe.

---

## 🤖 Escena 12 – Workflow TDD + IA: el círculo virtuoso

### El ciclo completo: RED → GREEN → REFACTOR con IA

Hasta ahora usaste IA para generar código aislado. Ahora aprenderás el **workflow profesional** que combina TDD con IA de forma disciplinada.

Este es el proceso que usarás en cada funcionalidad nueva:

---

### 📍 Paso 1: RED – Escribir el test primero (TÚ defines el contrato)

**Quién lo hace**: Tú (o IA bajo tu supervisión)
**Por qué importa**: El test **es la especificación**. Define qué debe hacer el código.

**Prompt para IA** (si necesitas ayuda):
```
Rol: QA Engineer Python
Contexto: API FastAPI con endpoint POST /tareas ya funcionando
Objetivo: Genera test pytest para endpoint GET /tareas que devuelva lista vacía inicialmente
Restricciones:
- Usar TestClient de FastAPI
- Assert status_code 200
- Assert response JSON es lista vacía []
```

**IA genera**:
```python
def test_listar_tareas_vacia_devuelve_lista_vacia():
    cliente = TestClient(app)
    respuesta = cliente.get("/tareas")
    assert respuesta.status_code == 200
    assert respuesta.json() == []
```

**TÚ validas**:
- ✅ ¿El test cumple la historia de usuario?
- ✅ ¿Los asserts son claros y completos?
- ✅ ¿El test falla por la razón correcta? (endpoint no existe aún)

**Ejecuta**: `pytest -v`
**Resultado esperado**: ❌ ROJO (test falla, endpoint no existe)

---

### 📍 Paso 2: GREEN – Implementación mínima (IA genera, TÚ validas)

**Prompt para IA**:
```
Rol: Backend Developer Python
Contexto: Tengo este test que falla: [pegar test completo]
Objetivo: Implementa el código MÍNIMO para hacer pasar este test
Restricciones:
- Solo agregar endpoint GET /tareas
- Devolver lista vacía hardcodeada (por ahora)
- No romper código existente
```

**IA genera**:
```python
@app.get("/tareas")
def listar_tareas():
    return []
```

**TÚ validas**:
1. Ejecutar `pytest -v`
2. ✅ ¿El test pasó a VERDE?
3. ✅ ¿No rompió otros tests?
4. ✅ ¿El código es el MÍNIMO necesario?

---

### 📍 Paso 3: REFACTOR – Mejora con agentes educacionales

Aquí es donde separas código que "funciona" de código **profesional**.

#### 3A. Python Best Practices Coach

**Qué detecta**:
- Type hints faltantes
- Oportunidades para comprehensions
- Anti-patterns (concatenación, loops innecesarios)

**Cómo usar**:
1. Lee tu código implementado
2. Busca patterns del agente (`.claude/agents/educational/python-best-practices-coach.md`)
3. Aplica feedback

**Ejemplo de mejora**:
```python
# ❌ Antes (sin type hints)
@app.get("/tareas")
def listar_tareas():
    return []

# ✅ Después (con type hints)
from typing import List
from pydantic import BaseModel

class TareaResponse(BaseModel):
    id: int
    nombre: str
    completada: bool

@app.get("/tareas", response_model=List[TareaResponse])
def listar_tareas() -> List[TareaResponse]:
    return []
```

#### 3B. FastAPI Design Coach

**Qué valida**:
- RESTful design correcto
- Status codes apropiados
- Response models con Pydantic
- Async/await cuando aplica

**Red flags típicas que detecta**:
```python
# ❌ Anti-pattern: Retornar dict en vez de modelo
@app.get("/tareas")
def listar_tareas():
    return [{"id": 1, "nombre": "Tarea"}]  # ❌ No tipado

# ✅ Correcto: Response model explícito
@app.get("/tareas", response_model=List[TareaResponse])
def listar_tareas() -> List[TareaResponse]:
    # FastAPI serializa automáticamente
    return [TareaResponse(id=1, nombre="Tarea", completada=False)]
```

#### 3C. API Design Reviewer

**Qué revisa**:
- Convenciones REST (GET, POST, PUT, DELETE)
- Nombres de endpoints (`/tareas` vs `/get-tareas`)
- Estructura de respuestas consistente
- Error handling apropiado

**Después del refactor**: Re-ejecuta tests
```bash
pytest -v
```
**Resultado**: ✅ VERDE (mismo comportamiento, mejor código)

---

### 🎯 Prompts efectivos para endpoints CRUD

#### Prompt template para GET (listar)
```
Rol: Backend Developer FastAPI
Contexto: API de tareas con modelo Tarea(id, nombre, completada)
Objetivo: Implementa GET /tareas que devuelva todas las tareas
Requisitos:
- Response model: List[TareaResponse]
- Status code: 200
- Inicialmente devolver lista vacía (memoria)
Restricciones: Solo código necesario, sin BD aún
```

#### Prompt template para GET (obtener uno)
```
Rol: Backend Developer FastAPI
Contexto: API de tareas ya tiene POST /tareas y GET /tareas
Objetivo: Implementa GET /tareas/{id} que devuelva una tarea específica
Requisitos:
- Path parameter: id (int)
- Response: 200 si existe, 404 si no existe
- Usar HTTPException para 404
```

#### Prompt template para PUT (actualizar)
```
Rol: Backend Developer FastAPI
Objetivo: Implementa PUT /tareas/{id}/completar que marque tarea como completada
Requisitos:
- Solo cambiar campo 'completada' a True
- Response: 200 con tarea actualizada, 404 si no existe
- Validar que id existe antes de actualizar
```

#### Prompt template para DELETE
```
Rol: Backend Developer FastAPI
Objetivo: Implementa DELETE /tareas/{id} que elimine una tarea
Requisitos:
- Response: 204 (No Content) si se eliminó
- Response: 404 si no existe
- No devolver body en 204
```

---

### 🔍 Validación del código generado por IA

**Checklist antes de aceptar código IA**:

#### Tests
- [ ] ¿Los tests pasan en verde?
- [ ] ¿Los tests validan el comportamiento correcto?
- [ ] ¿No hay tests comentados o skip?

#### Type hints
- [ ] ¿Funciones tienen type annotations?
- [ ] ¿Request/Response models están definidos con Pydantic?
- [ ] ¿mypy pasa sin errores? (`mypy api/api.py`)

#### REST compliance
- [ ] ¿Status codes son correctos? (200, 201, 204, 404, 422)
- [ ] ¿Nombres de endpoints siguen convención? (`/tareas` no `/getTareas`)
- [ ] ¿Response models son consistentes?

#### Clean Code
- [ ] ¿Código es legible? (nombres claros, no magia)
- [ ] ¿No hay duplicación innecesaria?
- [ ] ¿Sigue Single Responsibility?

---

### 🚨 Red flags típicas del código IA

**Red flag #1**: Código "mágico" sin explicación
```python
# ❌ IA a veces genera esto
@app.get("/tareas")
def get_tasks():  # ❌ Nombre inconsistente
    return db.query(Task).all()  # ❌ ¿De dónde sale db?
```

**Solución**: Pide a la IA que explique de dónde vienen las dependencias.

**Red flag #2**: Tests que no fallan
```python
# ❌ Test que siempre pasa (inútil)
def test_crear_tarea():
    assert True  # ❌ No valida nada real
```

**Solución**: Valida que el test falle cuando DEBE fallar.

**Red flag #3**: Código que "funciona" pero no es mantenible
```python
# ❌ Hardcoded values
@app.get("/tareas/{id}")
def get_task(id: int):
    if id == 1:
        return {"id": 1, "nombre": "Tarea 1"}
    elif id == 2:
        return {"id": 2, "nombre": "Tarea 2"}
    # ...
```

**Solución**: Usa repositorio, no hardcodes.

---

### 🎓 Cómo usar agentes educacionales (paso a paso)

**Escenario**: Acabas de implementar GET /tareas con IA

**Paso 1**: Lee el código generado línea por línea
**Paso 2**: Abre `.claude/agents/educational/python-best-practices-coach.md`
**Paso 3**: Compara tu código con los patterns del agente:
- ¿Falta type hints? → Agrega
- ¿Usa loops manuales? → Refactoriza a comprehension
- ¿Concatena strings? → Cambia a f-strings

**Paso 4**: Abre `.claude/agents/educational/fastapi-design-coach.md`
**Paso 5**: Valida diseño API:
- ¿Response model explícito?
- ¿Status codes correctos?
- ¿Async donde aplica?

**Paso 6**: Ejecuta tests nuevamente
**Paso 7**: Commit solo si TODO pasa

---

### 📊 Workflow visual resumido

```
┌─────────────────────────────────────────────┐
│  FASE RED (Test primero)                    │
│  ┌─────────────────────────────────────┐    │
│  │ 1. Escribe test (tú o IA)           │    │
│  │ 2. Valida que test es correcto      │    │
│  │ 3. pytest → ❌ ROJO (esperado)      │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────┐
│  FASE GREEN (Implementación mínima)         │
│  ┌─────────────────────────────────────┐    │
│  │ 1. IA genera código mínimo          │    │
│  │ 2. TÚ validas código                │    │
│  │ 3. pytest → ✅ VERDE               │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────┐
│  FASE REFACTOR (Mejora con agentes)         │
│  ┌─────────────────────────────────────┐    │
│  │ 1. Python Best Practices Coach      │    │
│  │ 2. FastAPI Design Coach             │    │
│  │ 3. API Design Reviewer              │    │
│  │ 4. pytest → ✅ VERDE (refactored)  │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
           │
           ▼
        COMMIT
```

---

### 💡 Lección clave

**La IA es tu junior developer**, no tu arquitecto.

- ✅ **IA genera código** → TÚ validas diseño
- ✅ **IA propone tests** → TÚ validas cobertura
- ✅ **IA sugiere refactors** → TÚ decides si aplicar

**No inviertas la relación**. Tú eres el arquitecto, la IA es la herramienta.

---

## ✅ Escena final – Checklist

- [x]  Entiendes qué es SOLID (y aplicaste SRP).
- [x]  Sabes qué prueba un test HTTP.
- [x]  Tienes tu entorno virtual limpio.
- [x]  Creaste un endpoint real y lo probaste con TDD.
- [x]  Aprendiste a leer código como historia, no como receta.

---

## 🎯 Resultado del PR

- Rama: `feature/api-tdd-crear-endpoint`.
- Archivos:
    - `api/api.py` (endpoint funcional).
    - `tests/test_crear_tarea.py` (dos tests claros).
    - `tests/conftest.py` (arreglo de import).
- Ambos tests en verde.
- `requirements.txt` generado.

---

Esta clase no te enseñó a “hacer APIs”.

Te enseñó **a pensar como un ingeniero**: cada línea tiene un propósito, cada error es una pista, cada test es una historia.

Lo importante es que ahora sabes, que cuando pidas a la IA un codigo, debes:

1. Pedir las historias a la IA
2. pedirle los test
3. Recordarle usar SOLID y SRP
4. Documentar en [notes.md](http://notes.md) para poder dar contexto en el futuro a la IA o a ti mismo
5. Sabes que tienes que hacer entornos virtuales
6. Sabes escalar de un CLI a una API
7. Aunque no sepas el codigo de memoria, ya puedes pedirle a la IA las cosas con mayor contexto en menos palabras.

No necesitas hacer un curso de prompt engineering, solo debes saber el lenguaje y lo que tienes que pedirle.