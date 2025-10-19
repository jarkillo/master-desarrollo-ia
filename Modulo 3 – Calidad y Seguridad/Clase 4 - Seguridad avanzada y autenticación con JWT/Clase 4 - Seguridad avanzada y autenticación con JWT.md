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

## 🤖 4.5. Security Hardening Mentor: IA genera, tú auditas

### El problema con "código que funciona"

Tu código JWT funciona. Los tests pasan. Puedes hacer login, crear tareas, y la autenticación protege tus endpoints.

**Pero, ¿es código profesional?**

Aquí es donde entra el **Security Hardening Mentor**: un flujo pedagógico donde la IA genera código funcional y **tú aprendes a auditarlo** con criterio de seguridad.

### 🎯 Cómo funciona

1. **IA genera** → Código funcional (como el que implementaste arriba)
2. **Agentes revisan** → Encuentran anti-patrones y vulnerabilidades
3. **Tú aprendes** → Entiendes *por qué* algo es problemático y *cómo* mejorarlo
4. **Iteras** → Aplicas las mejoras hasta que los agentes aprueban

Este no es un "code review" tradicional. Es **aprendizaje activo** donde cada issue te enseña un principio de seguridad.

---

### 🔍 Auditoría con 3 agentes educacionales

Vamos a revisar el código JWT que generaste con **tres agentes especializados** de `.claude/agents/educational/`:

#### 1. **Python Best Practices Coach**
**Qué busca**: Pythonic code, type hints, modern syntax (Python 3.10+), secrets management

**Prompt para Claude Code**:
```
Actúa como Python Best Practices Coach.

Revisa api/seguridad_jwt.py y api/api.py enfocándote en:
- Type hints completos (usa sintaxis moderna: dict[str, any], str | None)
- Secrets management (JWT_SECRET debe ser obligatorio y validado)
- Constantes HTTP (usa fastapi.status en lugar de números)
- Manejo de errores específicos (ExpiredSignatureError vs JWTError)

Para cada issue:
1. Identifica el anti-patrón
2. Explica POR QUÉ es problemático
3. Muestra la solución correcta
4. Enseña el principio subyacente
```

**Qué aprenderás**:
- ❌ `Optional[str]` → ✅ `str | None` (sintaxis Python 3.10+)
- ❌ `Dict[str, Any]` → ✅ `dict[str, any]` (built-in genéricos)
- ❌ `status_code=401` → ✅ `status_code=status.HTTP_401_UNAUTHORIZED`
- ❌ JWT_SECRET con default débil → ✅ Fail-fast sin secret válido

---

#### 2. **FastAPI Design Coach**
**Qué busca**: Dependency injection, response models, async patterns, Pydantic validation

**Prompt para Claude Code**:
```
Actúa como FastAPI Design Coach.

Revisa los endpoints /login y /tareas enfocándote en:
- Response models en todos los endpoints (no solo request)
- Dependency injection avanzada (inyectar payload del JWT, no solo validar)
- Rate limiting en /login (prevenir brute-force)
- Manejo de errores con HTTPException correcto

Para cada issue:
1. Identifica el anti-patrón
2. Explica POR QUÉ es problemático
3. Muestra la solución correcta
4. Enseña el principio de diseño FastAPI
```

**Qué aprenderás**:
- ❌ `dependencies=[Depends(verificar_jwt)]` (descarta el payload)
- ✅ `usuario: dict = Depends(verificar_jwt)` (inyecta para auditoría)
- ❌ `return tarea.model_dump()` (sin response_model)
- ✅ `response_model=TareaResponse` (contrato de API completo)
- ❌ Endpoint /login sin rate limiting
- ✅ `@limiter.limit("5/minute")` (previene brute-force)

---

#### 3. **API Design Reviewer**
**Qué busca**: RESTful principles, HTTP semantics, status codes, headers (RFC compliance)

**Prompt para Claude Code**:
```
Actúa como API Design Reviewer.

Revisa el diseño completo de la API JWT enfocándote en:
- Status codes HTTP correctos (200, 201, 401, 422)
- WWW-Authenticate header en respuestas 401 (RFC 7235)
- Location header en respuestas 201 (RFC 7231)
- Formato de errores consistente (no solo {"detail": "..."})

Para cada issue:
1. Identifica el problema de diseño
2. Explica POR QUÉ viola estándares HTTP/REST
3. Muestra la solución correcta según RFC
4. Enseña el principio de diseño de APIs
```

**Qué aprenderás**:
- ❌ `raise HTTPException(status_code=401, detail="...")`
- ✅ `headers={"WWW-Authenticate": "Bearer"}` (RFC 7235 requirement)
- ❌ Respuesta 201 sin Location header
- ✅ `response.headers["Location"] = f"/tareas/{tarea.id}"`
- ❌ Errores con formato inconsistente
- ✅ `ErrorResponse` model estándar (RFC 7807 inspired)

---

### 📋 Checklist de Seguridad JWT (de los agentes)

Usa este checklist **después** de que la IA genere tu código JWT:

#### ⚠️ **Nivel 1: Crítico (Seguridad)**
- [ ] **JWT_SECRET** es obligatorio (fail-fast si no existe)
- [ ] **JWT_SECRET** tiene ≥32 caracteres (nunca "dev-secret" en producción)
- [ ] **Passwords hasheados** con bcrypt (nunca texto plano, ni en demos)
- [ ] **WWW-Authenticate header** en todas las respuestas 401
- [ ] **Rate limiting** en /login (máximo 5-10 intentos/minuto)
- [ ] **Timing-safe comparison** para passwords (bcrypt.checkpw, no `==`)
- [ ] **Validar issuer/audience** en JWT (defense in depth)

#### 🟡 **Nivel 2: Importante (Calidad)**
- [ ] **Type hints completos** en todas las funciones (Python 3.10+ syntax)
- [ ] **Response models** en todos los endpoints (no solo request)
- [ ] **Inyectar payload del JWT** en handlers (para auditoría, no solo validar)
- [ ] **Manejo de errores específicos** (ExpiredSignatureError vs JWTError genérico)
- [ ] **Location header** en respuestas 201 (apunta al recurso creado)
- [ ] **Constantes HTTP** en lugar de números mágicos (status.HTTP_401_UNAUTHORIZED)

#### 🟢 **Nivel 3: Profesional (Mejores prácticas)**
- [ ] **Claims adicionales en JWT** (roles, email, issued_at)
- [ ] **Formato de errores estándar** (ErrorResponse model, no solo detail)
- [ ] **Security headers** (X-Content-Type-Options, X-Frame-Options, HSTS)
- [ ] **OpenAPI metadata completa** (title, description, examples, error responses)
- [ ] **Dependency factories** para roles (`requiere_roles(["admin"])`)
- [ ] **Logs de seguridad** (intentos fallidos de login, tokens inválidos)

---

### 🎓 Ejercicio práctico: Audita tu código

**Paso 1**: Implementa el código JWT básico (secciones 1-4 de esta clase)

**Paso 2**: Usa los 3 agentes para revisarlo
```bash
# En Claude Code, ejecuta cada prompt de agente por separado
# Guarda el reporte de cada uno en docs/auditorias/
```

**Paso 3**: Para cada issue que encuentren los agentes:
1. **Entiende** por qué es un problema (lee la explicación "Explain Why")
2. **Aplica** la solución (copia el código "Show Better")
3. **Aprende** el principio (memoriza "Teach Principle")
4. **Verifica** que los tests sigan pasando

**Paso 4**: Re-ejecuta los agentes hasta que no haya issues críticos

**Paso 5**: Compara "código antes" vs "código después"
```bash
git diff HEAD~1 api/seguridad_jwt.py
# ¿Qué cambió? ¿Por qué es más seguro?
```

---

### 💡 Ejemplo de iteración con agentes

**Código inicial (generado por IA)**:
```python
# ❌ Anti-patrón detectado por Python Best Practices Coach
def crear_token(claims: Dict[str, Any], minutos: Optional[int] = None) -> str:
    secret = os.getenv("JWT_SECRET", "dev-secret")  # ❌ Default débil
    # ...
```

**Agente reporta**:
> **Issue #2: Secrets Management**
>
> **Problema**: JWT_SECRET con default débil permite que la aplicación arranque sin configuración segura (silent failure).
>
> **Por qué es crítico**: En producción, si olvidas configurar JWT_SECRET, todos los tokens serán firmados con "dev-secret", permitiendo a un atacante generar tokens válidos.
>
> **Solución**: Usar pydantic-settings para fail-fast.

**Código refactorizado (tras aprender)**:
```python
# ✅ Mejor práctica aprendida
from pydantic_settings import BaseSettings

class SecurityConfig(BaseSettings):
    jwt_secret: str = Field(..., min_length=32)  # ✅ Obligatorio, ≥32 chars

    @field_validator("jwt_secret")
    @classmethod
    def validate_secret_strength(cls, v: str) -> str:
        weak = {"dev-secret", "secret", "password"}
        if v.lower() in weak:
            raise ValueError(f"JWT_SECRET '{v}' es débil. Genera uno con secrets.token_urlsafe(64)")
        return v

# Fail-fast en startup
config = SecurityConfig()  # Crash si JWT_SECRET no está configurado
```

**Resultado**: Aprendiste defense-in-depth y fail-fast patterns, no solo "cómo usar pydantic-settings".

---

### 🚨 Errores comunes al auditar (evítalos)

**❌ Error #1: "Funciona, no lo toques"**
- **Problema**: Código funcional ≠ código seguro
- **Aprendizaje**: Timing attacks, secrets débiles, y lack of rate limiting son invisibles en tests funcionales

**❌ Error #2: "Es solo una demo, no importa"**
- **Problema**: Demos con malas prácticas se copian a producción
- **Aprendizaje**: Siempre hashea passwords, incluso en demos. Normaliza buenas prácticas.

**❌ Error #3: "La IA dijo que está bien"**
- **Problema**: LLMs generan código funcional, no necesariamente seguro
- **Aprendizaje**: **Tú** eres el guardia de seguridad. Los agentes son tus herramientas de aprendizaje.

**❌ Error #4: "Aplicaré las mejoras después"**
- **Problema**: "Después" nunca llega. Deuda técnica crece.
- **Aprendizaje**: Refactoriza **antes** de mergear. Código en main debe ser profesional.

---

### 🎯 Meta-aprendizaje: Por qué este flujo importa

**Antes** (desarrollo tradicional):
1. Escribes código → Funciona → Mergeas
2. Semanas después: Auditoría de seguridad encuentra 15 vulnerabilidades
3. Sprint completo arreglando lo que pudiste prevenir

**Ahora** (con Security Hardening Mentor):
1. IA genera código funcional → **Agentes auditan** → Encuentran 6 issues
2. Aprendes **por qué** cada issue es problemático → Refactorizas
3. Re-auditas → 0 issues críticos → Mergeas con confianza

**La diferencia**: Aprendizaje **proactivo** vs reactivo. Prevención vs corrección tardía.

---

### 📚 Recursos para profundizar

**Agentes educacionales** (`.claude/agents/educational/`):
- `python-best-practices-coach.md` - Pythonic code, type hints, modern syntax
- `fastapi-design-coach.md` - DI avanzado, response models, async patterns
- `api-design-reviewer.md` - RESTful principles, HTTP semantics, RFC compliance

**RFCs de seguridad**:
- [RFC 7235 - HTTP Authentication](https://datatracker.ietf.org/doc/html/rfc7235) (WWW-Authenticate header)
- [RFC 6750 - OAuth 2.0 Bearer Token](https://datatracker.ietf.org/doc/html/rfc6750)
- [RFC 7519 - JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)
- [RFC 7807 - Problem Details for HTTP APIs](https://datatracker.ietf.org/doc/html/rfc7807)

**Herramientas de auditoría**:
- `bandit` - Security linter para Python
- `safety` - Dependency vulnerability scanner
- `ruff` - Modern Python linter (incluye security rules)
- OWASP ZAP - Web application security scanner

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

## ✅ Checklist de la Clase 4 – Seguridad avanzada y JWT

### 🎯 Fundamentos JWT
- [ ] Entiendes la diferencia entre API Key (estática, sin expiración) y JWT (temporal, con claims)
- [ ] Sabes qué son los tres componentes de un JWT (Header, Payload, Signature)
- [ ] Has creado y verificado JWT firmados con python-jose
- [ ] Has configurado expiración de tokens (configurable con JWT_MINUTOS)

### 🔒 Seguridad Crítica (de agentes)
- [ ] **JWT_SECRET** es obligatorio y ≥32 caracteres (fail-fast con pydantic-settings)
- [ ] **Nunca usas defaults débiles** ("dev-secret", "secret", "password")
- [ ] **WWW-Authenticate header** presente en todas las respuestas 401 (RFC 7235)
- [ ] **Rate limiting** implementado en /login (5-10 intentos/minuto)
- [ ] **Passwords hasheados** con bcrypt (nunca texto plano, ni en demos)
- [ ] **Timing-safe comparison** para validar passwords (bcrypt.checkpw)
- [ ] **Claims validados**: issuer (iss), audience (aud), expiration (exp), issued_at (iat)

### 🧰 Calidad y Buenas Prácticas
- [ ] **Type hints completos** con sintaxis moderna (`dict[str, any]`, `str | None`)
- [ ] **Response models** definidos en todos los endpoints (no solo request models)
- [ ] **Constantes HTTP** en lugar de números mágicos (`status.HTTP_401_UNAUTHORIZED`)
- [ ] **Manejo de errores específico** (ExpiredSignatureError vs JWTError genérico)
- [ ] **Dependency injection avanzada** (inyectas payload del JWT para auditoría)
- [ ] **Location header** en respuestas 201 Created (apunta al recurso creado)

### 🤖 Auditoría con IA
- [ ] Has usado **Python Best Practices Coach** para revisar tu código
- [ ] Has usado **FastAPI Design Coach** para mejorar el diseño de endpoints
- [ ] Has usado **API Design Reviewer** para validar cumplimiento de RFCs
- [ ] Has iterado con los agentes hasta eliminar issues críticos
- [ ] Entiendes el flujo "IA genera → Agentes auditan → Tú aprendes → Iteras"

### 🧪 Testing y CI/CD
- [ ] Tests validan login exitoso y credenciales inválidas
- [ ] Tests validan acceso con token válido a endpoints protegidos
- [ ] Tests validan rechazo de tokens inválidos, expirados o ausentes
- [ ] Tests verifican formato correcto de respuestas (access_token, token_type)
- [ ] Tu CI y auditoría de seguridad (bandit, safety) siguen en verde
- [ ] Coverage ≥80% (incluye casos de error y expiración)

### 📚 Meta-aprendizaje
- [ ] Entiendes que "funciona" ≠ "es seguro"
- [ ] Sabes usar agentes educacionales como herramienta de aprendizaje
- [ ] Has refactorizado código "antes de mergear", no "después"
- [ ] Reconoces la diferencia entre aprendizaje proactivo vs reactivo

---

## 🌱 Qué viene después

En la próxima clase comenzaremos el bloque de **DevSecOps y auditoría continua avanzada**, donde automatizaremos revisiones de vulnerabilidades en dependencias y pipelines de despliegue.