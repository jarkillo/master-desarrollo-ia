# Clase 2 - Seguridad básica en tu API: puertas cerradas, reglas claras

## 🎬 El contexto

Tu API ya funciona, guarda tareas y pasa los tests.

Pero es como una casa con ventanas abiertas: entra quien quiera, dice lo que le da la gana, y a veces incluso rompe cosas sin darte cuenta.

**Hoy toca poner orden:**

- Vamos a proteger tus rutas con una **llave**.
- A exigir que los datos sean **limpios y válidos**.
- Y a **leer configuración desde fuera del código** (porque meter claves en el `.py` es una receta para el desastre).

No vamos a complicarlo más de lo necesario.

Esto es lo básico que todo backend debería tener desde el día 1.

---

## 🧠 Concepto

### Qué problemas queremos evitar

- Que cualquiera use tu API sin permiso.
- Que envíen datos raros y te rompan el código.
- Que subas a GitHub archivos con claves o rutas privadas.

### Cómo lo resolvemos (sin humo técnico)

- Usamos un archivo `.env` para guardar cosas sensibles (como la clave de acceso).
- Validamos que cada petición venga con una **API Key**.
- Revisamos los datos que nos mandan con Pydantic: si no cumple, se para antes de llegar a tu lógica.
- Adaptamos los tests para que no se rompan con estos cambios.

---

## 🛠️ Aplicación manual (cómo lo haría un dev sin IA)

### 1. Creamos el archivo `.env`

Esto va en la raíz del proyecto (nunca lo subas al repo):

⚠️ PRIMER ERROR TÍPICO

No copies y pegues las credenciales tal cual, son nombres y passwords tipicos que estan en diccionarios de hackers. 

Modifica siempre la clave.

```
API_KEY=miclave123
MODO=dev
```

## 1.2. Añadir .env al archivo .gitignore

Por si acaso, añade siempre el .env al archivo .gitignore, esto evitará que se suba al repo

### 2. Leemos las variables en Python

Instala la librería `python-dotenv` si no la tienes:

```bash
pip install python-dotenv
```

Y al inicio de tu `api.py`, añade:

```python
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
```

Ya puedes usar `API_KEY` dentro del código.

### 3. Creamos una función que valide la clave

```python
from fastapi import Header, HTTPException, Depends

def verificar_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API key inválida")
```

Nota: usamos el header `X-API-Key` por convención.

El `...` significa que **es obligatorio**.

### 4. Protegemos los endpoints

Aplica el `Depends(verificar_api_key)` así:

```python
@app.get("/tareas", dependencies=[Depends(verificar_api_key)])
def listar_tareas():
    return [t.model_dump() for t in servicio.listar()]
```

Haz lo mismo para el `POST`.

### 5. Validación estricta del cuerpo con Pydantic

Queremos evitar que nos manden basura o cosas mal formadas.

```python
from pydantic import BaseModel, Field, constr

class CrearTareaRequest(BaseModel):
    nombre: constr(min_length=1, max_length=100)
    prioridad: str = Field(default="media", pattern="^(alta|media|baja)$")

```

Si te mandan `"prioridad": "urgente"` → 422

Si te mandan un nombre vacío → 422

Todo eso lo hace FastAPI automáticamente gracias a Pydantic.

---

Si has llegado hasta aquí sin preguntarte nada… MAL

¿Recuerdas los principios SOLID?

Ya estamos ensuciando de nuevo nuestro código.

Si hubieses preguntado a la IA, esta te hubiese vuelto a meter el codigo en tu [api.py](http://api.py) y cuando menos te lo esperes no hay quien lo arregle.

## 🔥 Rectificamos: **la API no valida, la API delega**

Meter `verificar_api_key()` en `api.py` **rompe el principio de responsabilidad única (SRP)**.

Ese archivo solo debería **recibir la petición, convertirla a objeto válido y delegar**.

### ¿Dónde debería ir `verificar_api_key`?

✅ En una nueva capa: **`dependencias.py` o `seguridad.py`**, dentro del módulo `api/`.

### ¿Por qué?

- Si lo dejas en `api.py`, ese archivo empieza a mezclar FastAPI, validaciones, lógica de seguridad… y se convierte en una sopa.
- Si mañana cambias el sistema de autenticación (pasas de API key a JWT), **solo cambias esa función**, sin tocar los endpoints.
- Y si quieres testearlo, puedes hacerlo por separado.

---

## 📦 Refactor con arquitectura limpia

### 1. Creamos `api/dependencias.py`

```python
# api/dependencias.py
from fastapi import Header, HTTPException, Depends
import os

API_KEY_ESPERADA = os.getenv("API_KEY")

def verificar_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY_ESPERADA:
        raise HTTPException(status_code=401, detail="API key inválida")

```

💡 Si quieres ir más pro: en vez de `os.getenv`, puedes pasárselo desde fuera al iniciar el servidor, pero por ahora vamos paso a paso.

---

### 2. Lo aplicamos en `api/api.py`, pero sin lógica

```python
from fastapi import Depends
from api.dependencias import verificar_api_key

@app.get("/tareas", dependencies=[Depends(verificar_api_key)])
def listar_tareas():
    return [tarea.model_dump() for tarea in servicio.listar()]

@app.post("/tareas", status_code=201, dependencies=[Depends(verificar_api_key)])
def crear_tarea(cuerpo: CrearTareaRequest):
    tarea = servicio.crear(cuerpo.nombre)
    return tarea.model_dump()

```

Ahora la API **solo orquesta**. No decide seguridad ni reglas.

---

### 🧠 BONUS: ¿Y si mañana quieres cambiar el tipo de autenticación?

Cambias solo `verificar_api_key()` por un `verificar_jwt()`

Tus endpoints siguen igual. Tus tests siguen igual. Tus PRs pesan menos.

---

## 🤖 Aplicación con IA (cómo delegarlo sin perder el control)

Prompt reutilizable:

```
Rol: Ingeniero de seguridad backend.

Contexto: Tengo una API FastAPI con endpoints para crear y listar tareas. Quiero:
- Proteger los endpoints con API Key.
- Leer la clave desde .env.
- Validar que los datos de entrada sean seguros y limpios.

Objetivo: Dame el código mínimo necesario, bien comentado, sin romper los tests actuales y siguiendo las normas SOLID.

```

¿Qué hará la IA?

- Te dará la función `verificar_api_key`.
- Te dirá cómo usar `dotenv`.
- Te pondrá un modelo Pydantic bien tipado.
- Puede que meta un `middleware`, pero para empezar el `Depends()` es más fácil de entender.

⚠️ No copies y pegues todo sin entenderlo. Copia por partes. Y preguntale a la IA lo que no entiendas.

Pasa tus tests. Si se rompen, corrige los headers o los datos.

---

## 📦 Mini-proyecto de esta clase

1. Crea una rama `feature/api-security-basics`.
2. Crea `.env` en la raíz con `API_KEY=loquesea`.
3. Modifica `api/api.py`:
    - Lee `.env`.
    - Añade validación de clave (`x-api-key` en headers).
    - Refuerza los modelos con restricciones reales.
4. Ajusta tus tests para incluir el header (si no lo tienen, fallarán).
5. Documenta en `Modulo3/Clase 2 - Seguridad básica/notes.md`:
    - Qué errores prevenís ahora.
    - Qué partes tuviste que cambiar en los tests.
    - Qué dudas te surgieron al aplicar seguridad.

---

## ✅ Checklist de la clase

- [ ]  `.env` creado y funcionando.
- [ ]  Tu API exige `x-api-key` válida.
- [ ]  Los datos de entrada se validan con Pydantic.
- [ ]  Los tests están actualizados y pasan en verde.
- [ ]  Tu CI sigue funcionando.

---

## Qué viene ahora

En la siguiente clase atacamos lo que ya empieza a sonar más profesional:

- Tokens JWT.
- Autenticación real (por usuario, no solo por clave fija).
- Buenas prácticas OWASP aplicadas a tu API.