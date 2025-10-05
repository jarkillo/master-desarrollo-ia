# Clase 4 - Seguridad avanzada y autenticación con JWT: identidad, confianza y tiempo limitado

## 🧩 1. El problema real

Tu API ya tiene una *llave maestra* (la `API_KEY`) y un CI que te protege de errores.

Pero esa llave es como una contraseña universal: si alguien la obtiene, puede hacer cualquier cosa para siempre.

Imagina que lanzas la API en producción y miles de usuarios distintos acceden.

¿Vas a repartir la misma clave a todos?

¿Y si uno la filtra? ¿O si quieres revocar su acceso?

Ahí nace el siguiente reto: **identidad y expiración**.

Cada usuario debe tener su propio token y ese token debe caducar.

Ahí entra **JWT (JSON Web Token)**.

---

## 🧠 2. Concepto

Un **JWT** es como una credencial firmada que tu servidor entrega cuando alguien se identifica correctamente.

Contiene tres partes:

1. **Header** → indica el algoritmo y tipo (`HS256`, `JWT`).
2. **Payload** → datos que tú decides (por ejemplo, `sub: usuario123`, `exp: 1717346400`).
3. **Firma** → una cadena cifrada que demuestra que lo emitiste tú y nadie lo alteró.

Cuando el cliente te hace una petición, manda el token en un header:

`Authorization: Bearer <token>`

Tu API comprueba la firma y la fecha. Si es válida, lo deja pasar.

---

## 🧰 3. Aplicación manual

1. Instala `python-jose`:

```bash
pip install python-jose[cryptography]

# NO TE OLVIDES DE AÑADIR python-jose[cryptography] AL REQUIREMENTS.TXT
```

1. Crea `api/seguridad_jwt.py`:

```python
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os

CLAVE_SECRETA = os.getenv("JWT_SECRET", "supersecreto")
ALGORITMO = "HS256"
DURACION_MINUTOS = 30

def crear_token(datos: dict):
    to_encode = datos.copy()
    exp = datetime.utcnow() + timedelta(minutes=DURACION_MINUTOS)
    to_encode.update({"exp": exp})
    return jwt.encode(to_encode, CLAVE_SECRETA, algorithm=ALGORITMO)

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
        return payload
    except JWTError:
        return None

```

1. Añade un endpoint `/login` que devuelva el token si el usuario y contraseña son correctos (por ahora, hardcodeado o mock).
2. En `tus endpoints`, cambia la dependencia:
    
    usa `verificar_token` en lugar de la API Key.
    

---

## ⚙️ 4. Aplicación con IA

Prompt recomendado:

```
Rol: Ingeniero backend senior en FastAPI.
Contexto: tengo autenticación básica con API_KEY y quiero migrar a JWT.
Objetivo:
- Añadir endpoint /login que devuelva un token con expiración.
- Proteger /tareas usando Authorization Bearer <token>.
Restricciones:
- Mantener estructura modular (api/seguridad_jwt.py separado).
- Añadir tests que validen login y expiración del token.

```

La IA te generará la ruta, el modelo `UsuarioLogin`, y los tests que verifiquen:

- token válido → 200 OK
- token vencido → 401
- token alterado → 401

Vamos a ir pasito a pasito como si se lo preguntaras a la IA

Vamos a migrar **paso a paso** y con tests primero (TDD suave). Yo marco el camino y tú ejecutas cada mini-paso. Vamos con ritmo corto.

# Plan en 4 mini-pasos

1. Tests de login y acceso con token (fallan ahora).
2. Módulo `api/seguridad_jwt.py` con emisión y verificación.
3. Endpoint `/login` y protección de `/tareas` con `Bearer`.
4. Tests de expiración/errores y pequeño refactor.

---

## 1) Escribe los tests (primero)

Crea `tests/test_auth_jwt.py` junto al resto de tests de tu clase actual:

```python
# tests/test_auth_jwt.py
import os
import time
from fastapi.testclient import TestClient
from api import api as api_mod
from api.servicio_tareas import ServicioTareas
from api.repositorio_memoria import RepositorioMemoria

def _cliente():
    # Inyecta repo limpio en cada test
    api_mod.servicio = ServicioTareas(RepositorioMemoria())
    return TestClient(api_mod.app)

def test_login_devuelve_token():
    os.environ["JWT_SECRET"] = "secret-test"
    c = _cliente()
    r = c.post("/login", json={"usuario": "demo", "password": "demo"})
    assert r.status_code == 200
    cuerpo = r.json()
    assert "access_token" in cuerpo
    assert cuerpo["token_type"] == "bearer"

def test_acceso_protegido_con_token():
    os.environ["JWT_SECRET"] = "secret-test"
    c = _cliente()
    token = c.post("/login", json={"usuario": "demo", "password": "demo"}).json()["access_token"]
    r = c.post("/tareas", json={"nombre": "Estudiar JWT"}, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 201

def test_token_invalido_da_401():
    os.environ["JWT_SECRET"] = "secret-test"
    c = _cliente()
    r = c.get("/tareas", headers={"Authorization": "Bearer chorizo"})
    assert r.status_code == 401

def test_token_expirado_da_401(monkeypatch):
    os.environ["JWT_SECRET"] = "secret-test"
    os.environ["JWT_MINUTOS"] = "0"   # forzamos expiración inmediata
    c = _cliente()
    token = c.post("/login", json={"usuario": "demo", "password": "demo"}).json()["access_token"]
    # pequeña espera para vencerlo (cero minutos ⇒ exp en pasado inmediato)
    time.sleep(1)
    r = c.get("/tareas", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401

```

> Estos tests definen el contrato: login da token; /tareas pide Bearer; rechaza tokens malos o vencidos
> 

Ejecuta pytest -v y verás los test fallando.

Genial: los fallos nos confirman exactamente lo que esperábamos (no existe `/login`, el protegido aún usa la API key y la dependencia devuelve 422). Vamos a arreglarlo **en dos micro-pasos**. Tú aplicas el cambio, lo ejecutas, y me dices el resultado. Voy con código mínimo y limpio.

# Paso 2 — Módulo JWT (emisión + verificación)

Crea `api/seguridad_jwt.py`:

```python
# api/seguridad_jwt.py
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import os

from fastapi import Header, HTTPException
from jose import jwt, JWTError

def _config():
    # Leer SIEMPRE del entorno para que los tests puedan setearlo al vuelo
    secret = os.getenv("JWT_SECRET", "dev-secret")
    minutos = int(os.getenv("JWT_MINUTOS", "30"))
    return secret, minutos

def crear_token(claims: Dict[str, Any], minutos: Optional[int] = None) -> str:
    secret, default_min = _config()
    exp_min = default_min if minutos is None else minutos
    to_encode = claims.copy()
    to_encode["exp"] = datetime.now(tz=timezone.utc) + timedelta(minutes=exp_min)
    return jwt.encode(to_encode, secret, algorithm="HS256")

def verificar_jwt(authorization: Optional[str] = Header(None, alias="Authorization")) -> Dict[str, Any]:
    # 401 si no hay cabecera o formato incorrecto
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Token ausente o formato inválido")

    token = authorization.split(" ", 1)[1].strip()
    secret, _ = _config()
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload  # lo puedes inyectar en el endpoint si lo necesitas
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

```

# Paso 3 — Endpoint `/login` y proteger `/tareas`

Edita `api/api.py` (importa y usa la dependencia JWT). Mantén el resto tal cual.

```python
# api/api.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field, constr

from api.servicio_tareas import ServicioTareas
from api.repositorio_memoria import RepositorioMemoria
from api.seguridad_jwt import crear_token, verificar_jwt  # <- NUEVO

app = FastAPI()
servicio = ServicioTareas(RepositorioMemoria())

# ====== Login ======
class LoginRequest(BaseModel):
    usuario: constr(min_length=1)
    password: constr(min_length=1)

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@app.post("/login", response_model=LoginResponse)
def login(cuerpo: LoginRequest):
    # Demo: credenciales fijas. En producción, valida contra tu store de usuarios.
    if cuerpo.usuario == "demo" and cuerpo.password == "demo":
        token = crear_token({"sub": cuerpo.usuario})
        return LoginResponse(access_token=token)
    raise HTTPException(status_code=401, detail="Credenciales inválidas")

# ====== Tareas ======
class CrearTareaRequest(BaseModel):
    nombre: constr(min_length=1, max_length=100)
    # si ya usabas prioridad, mantenla con default válido para no disparar 422:
    # prioridad: str = Field(default="media", pattern="^(alta|media|baja)$")

@app.post("/tareas", status_code=201, dependencies=[Depends(verificar_jwt)])
def crear_tarea(cuerpo: CrearTareaRequest):
    tarea = servicio.crear(cuerpo.nombre)
    return tarea.model_dump()

@app.get("/tareas", dependencies=[Depends(verificar_jwt)])
def listar_tareas():
    return [t.model_dump() for t in servicio.listar()]

```

> Detalles finos:
> 
> - Leemos `JWT_SECRET` y `JWT_MINUTOS` **dentro** de las funciones ⇒ tus tests que setean el entorno funcionan.
> - Para el caso del token inválido, devolvemos **401** (no 422), porque la cabecera existe y el formato es correcto, pero el token no lo es.
> - Mantenemos `CrearTareaRequest` con validación mínima para evitar 422 accidentales.

Recuerda preguntarle a la IA cualquier codigo que no entiendas

Pasa ahora los test y seguiras teniendo algún error:

Eso es lo esperado: ahora **/tareas** está detrás de JWT y esos tres tests fallan por **no mandar Authorization**. Ajustamos los tests para que primero obtengan un token con **/login** y luego llamen a **/tareas** con `Bearer`.

## Parche mínimo a los tests

### `tests/test_crear_tarea.py`

Añade un helper para crear cliente limpio y token, y úsalo en ambos tests:

```python
# al inicio del archivo
import os
from fastapi.testclient import TestClient
from api import api as api_mod
from api.servicio_tareas import ServicioTareas
from api.repositorio_memoria import RepositorioMemoria

def _cliente_y_headers():
    os.environ["JWT_SECRET"] = "secret-test"
    api_mod.servicio = ServicioTareas(RepositorioMemoria())
    c = TestClient(api_mod.app)
    token = c.post("/login", json={"usuario": "demo", "password": "demo"}).json()["access_token"]
    return c, {"Authorization": f"Bearer {token}"}

def test_crear_tarea_minima_devuelve_201_y_cuerpo_esperado():
    c, h = _cliente_y_headers()
    r = c.post("/tareas", json={"nombre": "Estudiar SOLID"}, headers=h)
    assert r.status_code == 201
    cuerpo = r.json()
    assert cuerpo["id"] == 1
    assert cuerpo["nombre"] == "Estudiar SOLID"
    assert cuerpo["completada"] is False

def test_crear_tarea_con_nombre_vacio_devuelve_422():
    c, h = _cliente_y_headers()
    r = c.post("/tareas", json={"nombre": ""}, headers=h)
    assert r.status_code == 422

```

### `tests_integrations/test_integracion_repositorios.py`

Mismo patrón: crear token y mandarlo.

```python
import os, tempfile
from fastapi.testclient import TestClient
from api import api as api_mod
from api.servicio_tareas import ServicioTareas
from api.repositorio_json import RepositorioJSON

def test_crear_tarea_con_repositorio_json_temporal():
    os.environ["JWT_SECRET"] = "secret-test"
    tmp = tempfile.NamedTemporaryFile(delete=False); tmp.close()
    try:
        api_mod.servicio = ServicioTareas(RepositorioJSON(tmp.name))
        c = TestClient(api_mod.app)

        token = c.post("/login", json={"usuario": "demo", "password": "demo"}).json()["access_token"]
        h = {"Authorization": f"Bearer {token}"}

        r = c.post("/tareas", json={"nombre": "Aprender tests con IA"}, headers=h)
        assert r.status_code == 201
        cuerpo = r.json()
        assert cuerpo["id"] == 1
        assert cuerpo["nombre"] == "Aprender tests con IA"
        assert cuerpo["completada"] is False
    finally:
        os.remove(tmp.name)

```

> Nota: seguimos leyendo JWT_SECRET “en tiempo de petición” dentro de seguridad_jwt.py, por eso fijarlo en os.environ antes de crear el TestClient funciona perfecto.
> 

Ahora ya pasarian los test en verde. Pero…

---

## 🧪 5. Mini-proyecto práctico

**Rama:** `feature/jwt-auth`

Pasos:

1. Crea `seguridad_jwt.py` con creación y validación de tokens.
2. Añade endpoint `POST /login` que genere el token.
3. Protege `/tareas` con JWT.
4. Crea tests que:
    - comprueben login correcto/incorrecto,
    - validen acceso con token,
    - fallen si el token expira o es inválido.
5. Actualiza `notes.md` con lo aprendido.

---

## ✅ Checklist de la Clase 4 – Seguridad avanzada

- [ ]  Entiendes la diferencia entre API Key y JWT.
- [ ]  Has creado y verificado JWT firmados y con expiración.
- [ ]  Has migrado tu dependencia de seguridad.
- [ ]  Tus tests validan login, expiración y errores.
- [ ]  Tu CI y auditoría siguen en verde.

---

## 🌱 Qué viene después

En la próxima clase comenzaremos el bloque de **DevSecOps y auditoría continua avanzada**, donde automatizaremos revisiones de vulnerabilidades en dependencias y pipelines de despliegue.