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