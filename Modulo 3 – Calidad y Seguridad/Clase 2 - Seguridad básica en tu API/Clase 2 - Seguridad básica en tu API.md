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
## ⚠️ ⚠️  Error en los Test ⚠️ ⚠️

Si acabas de hacer el PR te habras dado cuenta de que los test no han pasado:

Vale, el fallo es justo el que esperabas en una clase de seguridad: **422 porque falta la cabecera requerida**. En FastAPI, cuando una dependencia exige un header y no lo mandas, la validación de entrada falla → **422 Unprocessable Entity** (si la cabecera llega pero es incorrecta, entonces sería **401**).

Vamos a arreglarlo en dos frentes:

# 1) Asegurar que la dependencia lee la API key “en tiempo de petición”

Para que los tests puedan fijar `API_KEY` al vuelo, lee el valor del entorno **dentro** de la función (no al importar el módulo).

```python
# api/dependencias.py
import os
from fastapi import Header, HTTPException

def verificar_api_key(x_api_key: str = Header(..., alias="x-api-key")):
    esperada = os.getenv("API_KEY")  # leer en cada petición
    if not esperada or x_api_key != esperada:
        raise HTTPException(status_code=401, detail="API key inválida")

```

Notas:

- Uso `alias="x-api-key"` para que no haya dudas con el nombre exacto del header.
- Si `API_KEY` no está en el entorno y la exigimos, devolverá 401 (correcto: no hay clave de servidor configurada).

# 2) Ajustar los tests para enviar el header y preparar el entorno

Añade la API key al entorno **antes** de crear el `TestClient`, y mándala en cada petición.

**tests/test_crear_tarea_clase7.py**

```python
import os
from fastapi.testclient import TestClient
from api import api as api_mod
from api.servicio_tareas import ServicioTareas
from api.repositorio_memoria import RepositorioMemoria

def test_crear_tarea_minima_devuelve_201_y_cuerpo_esperado():
    os.environ["API_KEY"] = "test-key"     # 1) fijar clave
    api_mod.servicio = ServicioTareas(RepositorioMemoria())
    cliente = TestClient(api_mod.app)

    r = cliente.post(
        "/tareas",
        json={"nombre": "Estudiar SOLID"},
        headers={"x-api-key": "test-key"}  # 2) mandar cabecera
    )
    assert r.status_code == 201
    cuerpo = r.json()
    assert cuerpo["id"] == 1
    assert cuerpo["nombre"] == "Estudiar SOLID"
    assert cuerpo["completada"] is False

```

**tests_integrations/test_integracion_repositorios_clase7.py**

```python
import os, tempfile
from fastapi.testclient import TestClient
from api import api as api_mod
from api.servicio_tareas import ServicioTareas
from api.repositorio_json import RepositorioJSON

def test_crear_tarea_con_repositorio_json_temporal():
    os.environ["API_KEY"] = "test-key"
    tmp = tempfile.NamedTemporaryFile(delete=False); tmp.close()
    try:
        api_mod.servicio = ServicioTareas(RepositorioJSON(tmp.name))
        cliente = TestClient(api_mod.app)

        r = cliente.post(
            "/tareas",
            json={"nombre": "Aprender tests con IA"},
            headers={"x-api-key": "test-key"}
        )

        assert r.status_code == 201
        cuerpo = r.json()
        assert cuerpo["id"] == 1
        assert cuerpo["nombre"] == "Aprender tests con IA"
        assert cuerpo["completada"] is False
    finally:
        os.remove(tmp.name)

```

# 3) Revisa el modelo de entrada

Si en esta clase metiste validación extra con Pydantic (por ejemplo, `prioridad` con patrón) y **la hiciste obligatoria**, también disparará 422. Deja **valor por defecto**:

```python
# api/api.py (o donde definas los modelos)
from pydantic import BaseModel, Field, constr

class CrearTareaRequest(BaseModel):
    nombre: constr(min_length=1, max_length=100)
    prioridad: str = Field(default="media", pattern="^(alta|media|baja)$")

```

## Añadir la clave en github

**Si metes tu clave directamente en el YAML del workflow, la estás exponiendo en tu repo.**

Aunque esté dentro del `.github/workflows`, ese archivo es público si tu repo lo es.

Y aunque fuera privado, sigue siendo **una mala práctica**, porque las claves deben rotar y estar fuera del control de versiones.

Así que lo correcto es: **nunca pongas la clave real en el YAML ni en el codigo.**

---

## 🧭 Cómo se hace bien

### 🧱usar “secrets” de GitHub

GitHub tiene una sección en cada repositorio llamada **Settings → Secrets and variables → Actions**.

Ahí puedes crear una variable segura, por ejemplo:

```
Name: API_KEY
Value: miclaveultrasecreta123

```

Y luego, en tu workflow (`.github/workflows/ci.yml`) añade:

```yaml
env:
  API_KEY: ${{ secrets.API_KEY }}
```

Eso hace que la clave se inyecte **solo en el entorno del pipeline**, pero no se vea en los logs, ni se pueda leer desde el YAML.

GitHub la cifra internamente.

Perfecto para producción o proyectos reales.

---

Y en GitHub → Settings → Secrets → Actions → "New repository secret"

pones `API_KEY = test-key` o el valor que uses en tus pruebas.

---

## Parte 2: OWASP Top 10 para APIs - Vulnerabilidades Críticas (3h)

Ahora que tienes seguridad básica, es momento de conocer las **vulnerabilidades más peligrosas** que atacan a las APIs en producción.

OWASP (Open Web Application Security Project) publica cada año el Top 10 de vulnerabilidades web. Aquí nos enfocaremos en las **5 más relevantes para APIs FastAPI**.

### 🎯 Por qué esto es crítico para desarrollo asistido por IA

**La IA puede generar código vulnerable sin saberlo**. Y si no sabes detectarlo, terminas desplegando software inseguro.

Esta sección te enseña:
1. Cómo reconocer código vulnerable (generado por IA o por humanos)
2. Cómo usar agentes de seguridad para detectar problemas
3. Cómo corregir y prevenir cada vulnerabilidad

---

### 🔴 A01: Broken Access Control (Control de Acceso Roto)

**¿Qué es?** Endpoints o recursos accesibles sin validar permisos.

#### Código Vulnerable (típico de IA sin contexto de seguridad)

```python
# ❌ VULNERABLE: Cualquiera puede ver/editar tareas de otros usuarios
@app.get("/tareas/{user_id}")
def obtener_tareas_usuario(user_id: int):
    # No valida si el usuario autenticado puede ver estas tareas
    return servicio.listar_por_usuario(user_id)

@app.delete("/tareas/{tarea_id}")
def eliminar_tarea(tarea_id: int):
    # No valida ownership - cualquiera puede borrar tareas de otros
    servicio.eliminar(tarea_id)
    return {"mensaje": "Tarea eliminada"}
```

#### 🧠 ¿Por qué es peligroso?

- Usuario A puede leer/modificar/borrar tareas de Usuario B
- No hay verificación de **ownership** (propiedad)
- En APIs reales: pérdida de datos, violación de privacidad, manipulación

#### Prompt para que IA explique el riesgo

```markdown
Rol: Security Analyst experto en APIs

Contexto: Tengo este endpoint en FastAPI que permite acceder a tareas de usuarios:

[Pegar código vulnerable]

Pregunta: ¿Qué vulnerabilidad de seguridad tiene este código? Explica el riesgo con un ejemplo de ataque real.
```

**Respuesta esperada de IA**:
> Este código tiene **Broken Access Control (OWASP A01)**. Un atacante puede iterar user_id (1, 2, 3...) y acceder a tareas privadas de otros usuarios. Ejemplo: `GET /tareas/999` devuelve las tareas del usuario 999 sin validar si el solicitante tiene permiso.

#### ✅ Fix paso a paso

```python
# ✅ SEGURO: Validar ownership antes de permitir acceso
from fastapi import Depends, HTTPException

def obtener_usuario_actual(x_api_key: str = Header(...)):
    # En Clase 4 usaremos JWT, por ahora simulamos
    usuario_id = validar_y_extraer_usuario(x_api_key)
    if not usuario_id:
        raise HTTPException(status_code=401, detail="No autenticado")
    return usuario_id

@app.get("/tareas/{user_id}")
def obtener_tareas_usuario(
    user_id: int,
    usuario_actual: int = Depends(obtener_usuario_actual)
):
    # Validar que solo puedes ver tus propias tareas
    if user_id != usuario_actual:
        raise HTTPException(status_code=403, detail="Acceso denegado")

    return servicio.listar_por_usuario(user_id)
```

#### 🛡️ Prevención con agentes

**Usa FastAPI Design Coach para detectar**:

```markdown
/agent fastapi-design-coach

Revisa estos endpoints y detecta si hay problemas de control de acceso:

[Pegar código]

Enfócate en:
- Endpoints que acceden a recursos de usuarios específicos
- Validación de ownership
- Status codes (401 vs 403)
```

**Checklist de prevención**:
- [ ] Todo endpoint con `{user_id}` valida ownership
- [ ] Usar HTTP 403 (Forbidden) cuando el usuario no tiene permiso
- [ ] Usar HTTP 401 (Unauthorized) cuando no está autenticado
- [ ] Nunca confiar en parámetros del cliente para decisiones de acceso

---

### 🔴 A03: Injection (Inyección de código)

**¿Qué es?** Ejecutar código malicioso insertado en inputs no validados.

#### Código Vulnerable

```python
# ❌ VULNERABLE: SQL Injection simulado (f-strings peligrosos)
@app.get("/buscar")
def buscar_tareas(q: str):
    # Si usaras SQL raw (nunca lo hagas):
    query = f"SELECT * FROM tareas WHERE nombre LIKE '%{q}%'"
    # Atacante envía: q="'; DROP TABLE tareas; --"
    # Resultado: Tu tabla se borra

    # Incluso sin SQL, f-strings con datos externos son peligrosos
    resultado = eval(f"buscar_en_sistema('{q}')")  # ← NUNCA USAR eval()
    return resultado
```

#### 🧠 Riesgo

- **SQL Injection**: Borrar/modificar base de datos
- **Command Injection**: Ejecutar comandos del sistema
- **Code Injection**: Ejecutar código Python arbitrario

#### Prompt para generar código vulnerable (educativo)

```markdown
Rol: Ethical Hacker educativo

Tarea: Genera un ejemplo de endpoint FastAPI vulnerable a inyección de código.
Requisitos:
- Usa f-strings o eval() incorrectamente
- Incluye un comentario explicando el ataque
- Formato: código Python con docstrings educativos
```

#### ✅ Fix con Pydantic + Validación

```python
from pydantic import BaseModel, Field, constr

class BusquedaRequest(BaseModel):
    q: constr(min_length=1, max_length=50, pattern="^[a-zA-Z0-9 ]+$")
    # Solo permite letras, números y espacios
    # Bloquea caracteres especiales SQL (', ", --, ;)

@app.post("/buscar")
def buscar_tareas(busqueda: BusquedaRequest):
    # Pydantic ya validó que q es seguro
    # Usar ORM (SQLAlchemy) en lugar de SQL raw
    return servicio.buscar(busqueda.q)  # ORM escapa automáticamente
```

#### 🛡️ Prevención

1. **NUNCA usar**:
   - `eval()`, `exec()`, `compile()`
   - f-strings con datos de usuario en SQL
   - Concatenación de strings para queries

2. **SIEMPRE usar**:
   - Pydantic para validación
   - ORMs (SQLAlchemy) que escapan automáticamente
   - Prepared statements si usas SQL raw

3. **Validar con Python Best Practices Coach**:

```markdown
/agent python-best-practices-coach

Revisa este código y detecta usos peligrosos de eval, exec o f-strings con datos externos:

[Pegar código]
```

---

### 🔴 A07: Identification and Authentication Failures (Fallos de Autenticación)

**¿Qué es?** Sistemas de autenticación débiles o mal implementados.

#### Código Vulnerable

```python
# ❌ VULNERABLE: API Keys débiles, sin rotación, hardcodeadas
API_KEYS = {
    "admin": "123456",  # ← Clave débil
    "user1": "password",  # ← Clave predecible
}

def verificar_api_key_debil(x_api_key: str = Header(...)):
    # Comparación insegura (vulnerable a timing attacks)
    for user, key in API_KEYS.items():
        if x_api_key == key:
            return user
    raise HTTPException(status_code=401)

# Claves en código fuente (nunca rotadas, expuestas en Git)
```

#### 🧠 Problemas

1. **Claves débiles**: Fáciles de adivinar con brute force
2. **Hardcoded**: Si se filtran en Git, están comprometidas para siempre
3. **Sin rotación**: Mismas claves por años
4. **Timing attacks**: Comparación insegura revela información

#### ✅ Fix

```python
import secrets
from fastapi import Header, HTTPException

# Leer de .env (rotación manual) o usar JWT (Clase 4)
API_KEYS_VALIDOS = os.getenv("API_KEYS", "").split(",")

def verificar_api_key_segura(x_api_key: str = Header(...)):
    # Comparación segura (constant-time)
    for key_valida in API_KEYS_VALIDOS:
        if secrets.compare_digest(x_api_key, key_valida):
            return True
    raise HTTPException(status_code=401, detail="API key inválida")

# Generar claves seguras:
# secrets.token_urlsafe(32)  # Genera: "A2B3C4..."
```

#### 🛡️ Mejores prácticas

- [ ] Usar claves de al menos 32 caracteres aleatorios
- [ ] Guardar en `.env`, nunca en código
- [ ] Rotar claves cada 90 días
- [ ] Usar `secrets.compare_digest()` para comparar
- [ ] Prepararse para JWT (Clase 4 - autenticación moderna)

#### Prompt para Security Hardening Mentor

```markdown
Revisa mi sistema de autenticación y detecta debilidades:

[Pegar código de verificar_api_key]

Enfócate en:
- Fortaleza de las claves
- Almacenamiento seguro
- Comparación segura (timing attacks)
- Estrategia de rotación
```

---

### 🔴 A08: Software and Data Integrity Failures (Fallos de Integridad)

**¿Qué es?** Usar dependencias sin verificar, sin versiones específicas, con vulnerabilidades conocidas.

#### Código Vulnerable

```python
# requirements.txt INSEGURO
fastapi  # ← Sin versión específica (puede cambiar en producción)
requests  # ← Puede tener vulnerabilidades
pydantic
```

#### 🧠 Riesgo

- Instalas `fastapi` hoy (0.100.0) y funciona
- En 6 meses instalas en otro servidor → descarga 0.150.0 (breaking changes)
- O peor: una dependencia tiene vulnerabilidad crítica (CVE) y no lo sabes

#### ✅ Fix con versiones específicas

```bash
# ✅ SEGURO: Versiones específicas
fastapi==0.115.0
pydantic==2.10.3
requests==2.31.0

# Generar con pip freeze (después de testear)
pip freeze > requirements.txt
```

#### Auditoría con Safety

```bash
# Instalar Safety
pip install safety

# Escanear vulnerabilidades conocidas
safety check

# Ejemplo de output si detecta algo:
# requests==2.25.0 (vulnerable a CVE-2021-12345)
# Recomendación: Actualizar a requests>=2.31.0
```

#### 🛡️ Prevención con IA

**Prompt para auditar dependencies**:

```markdown
Rol: DevSecOps Engineer

Contexto: Tengo este requirements.txt:

[Pegar contenido]

Tareas:
1. Detectar dependencias sin versión específica
2. Verificar si hay versiones con vulnerabilidades conocidas
3. Sugerir versiones seguras actualizadas
4. Generar requirements.txt mejorado
```

**Integración en CI/CD** (`.github/workflows/ci_quality.yml`):

```yaml
- name: Security audit with Safety
  run: |
    pip install safety
    safety check --json
```

---

### 🔴 A09: Security Logging and Monitoring Failures (Sin Logs/Monitoreo)

**¿Qué es?** No registrar eventos de seguridad, sin alertas de ataques.

#### Código Vulnerable

```python
# ❌ VULNERABLE: Sin logging de eventos de seguridad
@app.post("/login")
def login(username: str, password: str):
    if not validar_credenciales(username, password):
        # Fallo silencioso - atacante puede intentar miles de veces
        raise HTTPException(status_code=401)
    return {"token": generar_token(username)}

# Sin logs de:
# - Intentos de login fallidos
# - Accesos denegados (403)
# - Errores de validación (422)
# - Requests sospechosos
```

#### 🧠 Riesgo

- **Brute force attacks** no detectados (miles de intentos)
- **Data breaches** descubiertos meses después
- **Sin evidencia** para análisis forense
- **Imposible detectar** patrones de ataque

#### ✅ Fix con logging estructurado

```python
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.post("/login")
def login(username: str, password: str, request: Request):
    ip_cliente = request.client.host

    if not validar_credenciales(username, password):
        # Registrar fallo de autenticación
        logger.warning(
            f"Login fallido: usuario={username}, ip={ip_cliente}"
        )
        raise HTTPException(status_code=401)

    # Registrar login exitoso
    logger.info(f"Login exitoso: usuario={username}, ip={ip_cliente}")
    return {"token": generar_token(username)}

# Logs de acceso denegado
@app.middleware("http")
async def log_security_events(request: Request, call_next):
    response = await call_next(request)

    if response.status_code in [401, 403]:
        logger.warning(
            f"Acceso denegado: {request.method} {request.url.path}, "
            f"status={response.status_code}, ip={request.client.host}"
        )

    return response
```

#### 🛡️ Integración con Sentry (Preview Clase 7)

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastAPIIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[FastAPIIntegration()],
    traces_sample_rate=1.0,
)

# Ahora Sentry captura automáticamente:
# - Excepciones no manejadas
# - Requests lentos
# - Errores 500
# - Contexto completo (user, IP, headers)
```

#### Checklist de logging

- [ ] Registrar intentos de autenticación (exitosos y fallidos)
- [ ] Registrar accesos denegados (401, 403)
- [ ] Registrar errores de validación (422)
- [ ] Incluir: timestamp, IP, user_id, acción
- [ ] NUNCA loguear: passwords, tokens, API keys
- [ ] Enviar logs críticos a sistema externo (Sentry, CloudWatch)

---

### ✅ Checklist Parte 2: OWASP Top 10

- [ ] Comprendes las 5 vulnerabilidades críticas para APIs
- [ ] Sabes detectar Broken Access Control en código
- [ ] Entiendes cómo prevenir Injection con Pydantic
- [ ] Implementas autenticación segura (API Keys fuertes)
- [ ] Auditas dependencias con Safety
- [ ] Implementas logging de eventos de seguridad
- [ ] Has usado agentes para detectar vulnerabilidades
- [ ] Conoces el patrón: Vulnerable → Explica → Fix → Prevención

---

## Parte 3: Ejercicios prácticos con IA (1.5-2h)

**Objetivo**: Aprender a **auditar código generado por IA** para detectar vulnerabilidades de seguridad. La IA puede generar código vulnerable si no le das el contexto de seguridad adecuado.

### Ejercicio 1: Detectar vulnerabilidades generadas por IA (30 min)

**Contexto**: Pides a la IA que implemente un endpoint sin darle contexto de seguridad. Luego auditas el código.

#### Paso 1: Genera código sin contexto de seguridad

**Prompt débil (sin seguridad)**:
```
Crea un endpoint FastAPI para eliminar una tarea por ID
```

**Código generado por IA** (típicamente vulnerable):
```python
# ejemplos_vulnerables/eliminar_tarea_inseguro.py
@app.delete("/tareas/{tarea_id}")
def eliminar_tarea(tarea_id: int):
    """Eliminar tarea - CÓDIGO VULNERABLE GENERADO POR IA"""
    servicio.eliminar(tarea_id)
    return {"message": "Tarea eliminada"}
```

#### Paso 2: Audita con Security Hardening Mentor

**Prompt de auditoría**:
```
Actúa como Security Hardening Mentor. Audita este endpoint de FastAPI para eliminar tareas.
Identifica vulnerabilidades de seguridad siguiendo OWASP Top 10.

Código:
[pegar código generado]

Proporciona:
1. Lista de vulnerabilidades encontradas
2. Nivel de severidad (Crítico/Alto/Medio/Bajo)
3. Explicación del riesgo
4. Código corregido
```

**Vulnerabilidades detectadas**:
1. **A01: Broken Access Control** (CRÍTICO)
   - No valida ownership de la tarea
   - Cualquier usuario puede eliminar tareas de otros

2. **A09: Security Logging Failures** (ALTO)
   - No registra eventos de eliminación (audit trail)
   - Imposible investigar eliminaciones no autorizadas

3. **A04: Insecure Design** (MEDIO)
   - No retorna 404 si tarea no existe
   - No usa 204 No Content (código correcto para DELETE exitoso)

#### Paso 3: Código seguro corregido

```python
# api/endpoints_seguros.py
import logging
from fastapi import Depends, HTTPException

logger = logging.getLogger(__name__)

@app.delete("/tareas/{tarea_id}", status_code=204)
def eliminar_tarea(
    tarea_id: int,
    usuario_actual: int = Depends(obtener_usuario_actual)
):
    """Eliminar tarea con validación de ownership y auditoría"""

    # 1. Verificar que tarea existe
    tarea = servicio.obtener_por_id(tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # 2. Verificar ownership (A01: Broken Access Control)
    if tarea.user_id != usuario_actual:
        logger.warning(
            f"Intento no autorizado de eliminar tarea {tarea_id} "
            f"por usuario {usuario_actual}"
        )
        raise HTTPException(status_code=403, detail="Acceso denegado")

    # 3. Eliminar tarea
    servicio.eliminar(tarea_id)

    # 4. Auditoría (A09: Security Logging)
    logger.info(
        f"Tarea {tarea_id} eliminada por usuario {usuario_actual}",
        extra={
            "event": "tarea_eliminada",
            "tarea_id": tarea_id,
            "user_id": usuario_actual
        }
    )

    # 5. 204 No Content (no retornar cuerpo en DELETE)
    return None
```

#### Reflexión del ejercicio

**¿Qué aprendiste?**
- La IA genera código funcional pero **no siempre seguro**
- Necesitas **dar contexto de seguridad en tus prompts**
- El patrón "generar → auditar → corregir" es esencial
- Los agentes educacionales detectan patrones peligrosos

**Prompt mejorado** (con contexto de seguridad):
```
Crea un endpoint FastAPI para eliminar una tarea por ID.

Requisitos de seguridad:
- Validar ownership (solo el dueño puede eliminar)
- Retornar 404 si no existe, 403 si no autorizado
- Usar status_code=204 para DELETE exitoso
- Registrar evento de eliminación (audit log)
- Manejar errores con HTTPException
```

---

### Ejercicio 2: Auditoría paso a paso con checklist (30 min)

**Contexto**: Usas un checklist sistemático para auditar código generado por IA.

#### Paso 1: Código generado por IA

**Prompt débil**:
```
Crea un endpoint para actualizar el estado de una tarea
```

**Código generado**:
```python
# ejemplos_vulnerables/actualizar_tarea_inseguro.py
@app.put("/tareas/{tarea_id}")
def actualizar_tarea(tarea_id: int, datos: dict):
    """Actualizar tarea - VULNERABLE"""
    tarea = servicio.obtener_por_id(tarea_id)

    for campo, valor in datos.items():
        setattr(tarea, campo, valor)  # Mass assignment vulnerability

    servicio.guardar(tarea)
    return tarea
```

#### Paso 2: Aplica el Security Checklist

Usa el checklist `SECURITY_CHECKLIST.md` (lo crearemos después):

**Checklist de auditoría**:

```markdown
## 1. Validación de entrada
- [ ] ¿Usa Pydantic para validar request body? ❌ (usa `dict`)
- [ ] ¿Valida tipos de datos? ❌
- [ ] ¿Previene mass assignment? ❌ (usa `setattr` con cualquier campo)

## 2. Control de acceso (A01)
- [ ] ¿Valida ownership del recurso? ❌
- [ ] ¿Retorna 403 si no autorizado? ❌

## 3. Manejo de errores
- [ ] ¿Retorna 404 si recurso no existe? ⚠️ (retorna None sin validar)
- [ ] ¿Usa HTTPException correctamente? ❌

## 4. Inyección (A03)
- [ ] ¿Evita SQL injection? ✅ (usa ORM)
- [ ] ¿Evita eval() o exec()? ✅

## 5. Autenticación (A07)
- [ ] ¿Requiere autenticación? ❌ (no usa `Depends`)

## 6. Logging (A09)
- [ ] ¿Registra eventos de seguridad? ❌
```

**Resultado**: 2/11 checks aprobados → **CÓDIGO VULNERABLE**

#### Paso 3: Código corregido

```python
# api/endpoints_seguros.py
from pydantic import BaseModel, Field

class ActualizarTareaRequest(BaseModel):
    """Schema seguro - solo permite campos específicos"""
    nombre: str = Field(None, min_length=1, max_length=100)
    descripcion: str = Field(None, max_length=500)
    completada: bool = None

@app.put("/tareas/{tarea_id}", response_model=TareaResponse)
def actualizar_tarea(
    tarea_id: int,
    datos: ActualizarTareaRequest,  # Pydantic valida
    usuario_actual: int = Depends(obtener_usuario_actual)
):
    """Actualizar tarea con validación de ownership y mass assignment protection"""

    # 1. Verificar que existe
    tarea = servicio.obtener_por_id(tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # 2. Validar ownership
    if tarea.user_id != usuario_actual:
        logger.warning(
            f"Intento no autorizado de actualizar tarea {tarea_id} "
            f"por usuario {usuario_actual}"
        )
        raise HTTPException(status_code=403, detail="Acceso denegado")

    # 3. Actualizar solo campos permitidos (previene mass assignment)
    datos_actualizacion = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizacion.items():
        setattr(tarea, campo, valor)

    # 4. Guardar y auditar
    servicio.guardar(tarea)
    logger.info(
        f"Tarea {tarea_id} actualizada por usuario {usuario_actual}",
        extra={"event": "tarea_actualizada", "tarea_id": tarea_id}
    )

    return tarea
```

**Checklist corregido**: 11/11 checks aprobados ✅

---

### Ejercicio 3: Security Hardening con agentes (40 min)

**Contexto**: Usas 3 agentes especializados para endurecer la seguridad de tu API completa.

#### Paso 1: Revisión inicial con FastAPI Design Coach

**Prompt**:
```
Actúa como FastAPI Design Coach. Revisa esta API de tareas completa.
Identifica anti-patrones de diseño que puedan convertirse en vulnerabilidades.

[Pegar código de api.py completo]

Enfócate en:
- Validación con Pydantic
- Dependency injection
- Status codes HTTP correctos
- Async/await donde aplique
```

**Detecciones típicas**:
- Falta validación de límites en paginación
- No usa async/await (puede causar blocking I/O)
- Falta rate limiting
- No usa Response models consistentemente

#### Paso 2: Revisión de seguridad con Python Best Practices Coach

**Prompt**:
```
Actúa como Python Best Practices Coach. Audita este código FastAPI para patrones inseguros.

[Pegar código]

Busca:
- Uso de secrets module para comparaciones
- Manejo seguro de excepciones
- Type hints completos
- Validación de entrada/salida
```

**Detecciones típicas**:
- Usa `==` en vez de `secrets.compare_digest` para API keys
- Falta type hints en algunas funciones
- Excepciones genéricas exponen stack traces
- Secrets hardcodeados en código

#### Paso 3: Revisión de arquitectura con API Design Reviewer

**Prompt**:
```
Actúa como API Design Reviewer. Evalúa esta API REST siguiendo principios RESTful y OWASP.

[Pegar código]

Evalúa:
- Diseño de endpoints (RESTful)
- Códigos de estado HTTP
- Versionado de API
- Rate limiting
- Documentación (OpenAPI/Swagger)
```

**Detecciones típicas**:
- Falta versionado (`/v1/tareas`)
- No documenta límites de rate limiting
- Falta paginación en listados
- Códigos de estado inconsistentes

#### Paso 4: Implementa las correcciones

**Ejemplo de correcciones aplicadas**:

```python
# api/api_hardened.py
from fastapi import FastAPI, Depends, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import secrets

app = FastAPI(
    title="API de Tareas - Hardened",
    version="1.0.0",
    description="API segura con OWASP Top 10 mitigado"
)

# Rate limiting middleware
@app.on_event("startup")
async def startup():
    await FastAPILimiter.init("redis://localhost")

# CORS seguro (no usar "*" en producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://miapp.com"],  # Específico
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Endpoint con rate limiting y versionado
@app.get(
    "/v1/tareas",
    response_model=ListaTareasResponse,
    dependencies=[Depends(RateLimiter(times=100, seconds=60))]
)
async def listar_tareas(  # Async para no bloquear
    usuario_actual: int = Depends(obtener_usuario_actual),
    limite: int = Query(10, ge=1, le=100),  # Validación de límites
    offset: int = Query(0, ge=0)
):
    """Listar tareas con paginación y rate limiting"""
    tareas = await servicio.listar_por_usuario(
        usuario_actual,
        limite=limite,
        offset=offset
    )

    return {
        "tareas": tareas,
        "total": len(tareas),
        "limite": limite,
        "offset": offset
    }

# Autenticación segura con secrets.compare_digest
def verificar_api_key(api_key: str = Depends(obtener_api_key)) -> int:
    """Verificar API Key resistente a timing attacks"""
    usuario = repositorio_usuarios.obtener_por_api_key_hash(
        hashlib.sha256(api_key.encode()).hexdigest()
    )

    if not usuario:
        raise HTTPException(status_code=401, detail="API Key inválida")

    # Timing-safe comparison
    if not secrets.compare_digest(
        usuario.api_key_hash,
        hashlib.sha256(api_key.encode()).hexdigest()
    ):
        raise HTTPException(status_code=401, detail="API Key inválida")

    return usuario.id
```

#### Reflexión del ejercicio

**Antes del hardening**:
- 8+ vulnerabilidades detectadas por agentes
- Sin rate limiting, sin versionado, sin async
- Timing attacks posibles en autenticación

**Después del hardening**:
- 0 vulnerabilidades críticas/altas
- Rate limiting implementado
- API versionada (`/v1/`)
- Async/await para operaciones I/O
- Autenticación resistente a timing attacks

---

### Ejercicio 4: Crear tu checklist de auditoría de código IA (20 min)

**Contexto**: Creas un checklist reutilizable para auditar cualquier código generado por IA.

#### Paso 1: Usa agentes para generar el checklist

**Prompt para Security Hardening Mentor**:
```
Actúa como Security Hardening Mentor. Crea un checklist exhaustivo para auditar código FastAPI generado por IA.

El checklist debe cubrir:
1. OWASP Top 10 para APIs
2. Validación de entrada/salida
3. Autenticación y autorización
4. Logging y monitoreo
5. Manejo de errores
6. Configuración segura

Formato: Markdown con checkboxes, dividido por categorías, con ejemplos de qué buscar.
```

#### Paso 2: Personaliza el checklist

El agente generará un checklist base. Tú lo personalizas para tu proyecto:

```markdown
# Security Audit Checklist - Código Generado por IA

## Categoría 1: Validación de Entrada (A03 Injection)

### Validación con Pydantic
- [ ] Todos los request bodies usan modelos Pydantic (no `dict`)
- [ ] Campos tienen validación con `Field` (min_length, max_length, ge, le)
- [ ] No se usa `eval()`, `exec()`, `compile()`
- [ ] Queries SQL usan ORM o prepared statements (no f-strings)

**Ejemplo de qué buscar**:
```python
# ❌ VULNERABLE
datos: dict  # Sin validación

# ✅ SEGURO
class CrearTareaRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
```

## Categoría 2: Control de Acceso (A01 Broken Access Control)

### Validación de Ownership
- [ ] Endpoints protegidos usan `Depends(obtener_usuario_actual)`
- [ ] Se valida ownership antes de modificar recursos
- [ ] Retorna 403 Forbidden (no 404) si no autorizado
- [ ] No se expone información de otros usuarios

**Ejemplo**:
```python
# ❌ VULNERABLE
@app.delete("/tareas/{id}")
def eliminar(id: int):
    servicio.eliminar(id)  # Cualquiera puede eliminar

# ✅ SEGURO
@app.delete("/tareas/{id}")
def eliminar(id: int, user: int = Depends(auth)):
    tarea = servicio.obtener(id)
    if tarea.user_id != user:
        raise HTTPException(403)
    servicio.eliminar(id)
```

[... continúa con las 10 categorías OWASP ...]
```

#### Paso 3: Usa el checklist en tu workflow

**Workflow de desarrollo con IA**:

1. **Generar código** con prompt (incluir contexto de seguridad)
2. **Auditar** con `SECURITY_CHECKLIST.md`
3. **Corregir vulnerabilidades** detectadas
4. **Re-auditar** con agentes (FastAPI Design Coach, Security Hardening)
5. **Commit** solo si pasa auditoría

**Ejemplo de prompt con contexto de seguridad**:
```
Crea un endpoint FastAPI para [funcionalidad].

Requisitos de seguridad:
- Usar Pydantic para validación estricta
- Validar ownership del recurso
- Retornar códigos HTTP correctos (200/201/204/403/404)
- Registrar eventos de seguridad con logging
- Usar `Depends` para autenticación
- Prevenir mass assignment
```

#### Reflexión del ejercicio

**¿Qué lograste?**
- Tienes un checklist reutilizable para cualquier proyecto
- Puedes auditar código IA de forma sistemática
- Reduces el "copiar-pegar" inseguro
- Workflow: Generar → Auditar → Corregir → Re-auditar

**¿Cómo mejora tu productividad?**
- La IA genera código rápido → Tú auditas con checklist → Código seguro en menos tiempo
- Aprendes patrones seguros/inseguros a identificar
- Puedes pedir a la IA que "implemente siguiendo SECURITY_CHECKLIST.md"

---

## Resumen de la Parte 3

**Has aprendido a**:
1. **Detectar vulnerabilidades** en código generado por IA
2. **Auditar sistemáticamente** con checklists
3. **Usar agentes especializados** para hardening (FastAPI Coach, Python Practices, API Reviewer)
4. **Crear tu propio checklist** de auditoría

**Workflow de seguridad con IA**:
```
Prompt con contexto → Generar código → Auditar con checklist →
Usar agentes → Corregir vulnerabilidades → Re-auditar → Commit seguro
```

**Checklist de aprendizaje**:
- [ ] Sabes que la IA genera código funcional pero no siempre seguro
- [ ] Aprendiste a dar contexto de seguridad en prompts
- [ ] Puedes auditar código con checklist sistemático
- [ ] Usas agentes educacionales para hardening
- [ ] Tienes un workflow: Generar → Auditar → Corregir → Re-auditar
- [ ] Creaste tu `SECURITY_CHECKLIST.md` reutilizable

---

## Parte 4: Proyecto final seguro (1h)

**Objetivo**: Construir una API de Tareas **completamente segura** aplicando todo lo aprendido: API Keys, OWASP Top 10, auditoría con IA, y prevención de vulnerabilidades.

### Especificaciones del proyecto

Implementa una API de Tareas con **5 endpoints seguros**:

1. **POST /v1/tareas** - Crear tarea (requiere autenticación)
2. **GET /v1/tareas** - Listar tareas del usuario autenticado (con paginación)
3. **GET /v1/tareas/{id}** - Obtener tarea específica (validar ownership)
4. **PUT /v1/tareas/{id}** - Actualizar tarea (validar ownership, prevenir mass assignment)
5. **DELETE /v1/tareas/{id}** - Eliminar tarea (validar ownership, audit log)

### Requisitos de seguridad (checklist del proyecto)

**Debes implementar**:

#### 1. Autenticación (A07: Authentication Failures)
- [ ] API Keys almacenadas hasheadas (SHA-256)
- [ ] Validación con `secrets.compare_digest` (resistente a timing attacks)
- [ ] API Keys de 32+ caracteres generadas con `secrets.token_urlsafe`
- [ ] Endpoint protegido con `Depends(obtener_usuario_actual)`

#### 2. Control de Acceso (A01: Broken Access Control)
- [ ] Validación de ownership en GET/PUT/DELETE
- [ ] Retornar 403 si usuario intenta acceder a recursos de otros
- [ ] Retornar 404 si recurso no existe
- [ ] No exponer información de otros usuarios

#### 3. Validación de Entrada (A03: Injection)
- [ ] Todos los request bodies usan modelos Pydantic
- [ ] Validación con `Field` (min_length, max_length, ge, le)
- [ ] No se usa `eval()`, `exec()`, `__import__()`
- [ ] Queries usan ORM (no SQL raw con f-strings)

#### 4. Seguridad de Dependencias (A08: Software/Data Integrity Failures)
- [ ] `requirements.txt` con versiones pinneadas
- [ ] Auditado con `safety check` sin vulnerabilidades críticas/altas
- [ ] Usa dependencias actualizadas (FastAPI 0.115+, Pydantic 2.10+)

#### 5. Logging y Monitoreo (A09: Security Logging Failures)
- [ ] Logs de autenticación fallida
- [ ] Logs de intentos no autorizados (403)
- [ ] Logs de eventos críticos (creación, actualización, eliminación)
- [ ] Formato estructurado con `extra={"event": "nombre_evento"}`

#### 6. Configuración Segura (A05: Security Misconfiguration)
- [ ] Secretos en `.env` (no hardcodeados)
- [ ] `.env` en `.gitignore`
- [ ] `.env.template` con valores de ejemplo
- [ ] Validación de variables de entorno al inicio

#### 7. Manejo de Errores
- [ ] No exponer stack traces en producción
- [ ] Mensajes de error genéricos ("Acceso denegado", no "Usuario 123 no es dueño")
- [ ] HTTPException con status codes correctos

#### 8. Diseño de API (REST + OWASP)
- [ ] Versionado de API (`/v1/`)
- [ ] Status codes correctos (200, 201, 204, 403, 404, 422)
- [ ] Paginación en listados (`limite`, `offset`)
- [ ] Documentación automática (Swagger en `/docs`)

### Paso 1: Genera la estructura con IA

**Prompt inicial** (con contexto de seguridad):

```
Crea la estructura base de una API FastAPI de Tareas siguiendo estas especificaciones:

Endpoints:
- POST /v1/tareas - Crear tarea
- GET /v1/tareas - Listar tareas (con paginación)
- GET /v1/tareas/{id} - Obtener tarea
- PUT /v1/tareas/{id} - Actualizar tarea
- DELETE /v1/tareas/{id} - Eliminar tarea

Requisitos de seguridad (OWASP Top 10):
1. Autenticación con API Keys (hasheadas, timing-safe comparison)
2. Validación de ownership en todos los endpoints (403 si no autorizado)
3. Validación con Pydantic (min_length, max_length)
4. Prevención de mass assignment (solo campos específicos)
5. Logging de eventos de seguridad (auth, 403, CRUD)
6. Secretos en .env
7. Paginación con validación (limite entre 1-100)
8. Status codes correctos (200/201/204/403/404/422)

Estructura:
- api/api.py (endpoints)
- api/seguridad.py (autenticación, API Keys)
- api/modelos.py (Pydantic models)
- api/servicio.py (lógica de negocio)
- .env.template
- requirements.txt

Genera el código completo con comentarios explicando cada mitigación OWASP.
```

### Paso 2: Audita el código generado

**Usa el Security Checklist** (`SECURITY_CHECKLIST.md`):

1. **Revisión manual** con el checklist de 8 categorías
2. **Auditoría con FastAPI Design Coach**:
   ```
   Actúa como FastAPI Design Coach. Audita esta API completa.
   Busca anti-patrones de diseño y validación.
   ```

3. **Auditoría con Python Best Practices Coach**:
   ```
   Actúa como Python Best Practices Coach. Audita para patrones inseguros.
   Busca: secrets.compare_digest, type hints, manejo de excepciones.
   ```

4. **Auditoría con API Design Reviewer**:
   ```
   Actúa como API Design Reviewer. Evalúa diseño RESTful y OWASP.
   Verifica: status codes, versionado, paginación, documentación.
   ```

### Paso 3: Implementa correcciones

**Ejemplo de código esperado** (con todas las mitigaciones):

```python
# api/api.py
from fastapi import FastAPI, Depends, HTTPException, Query
from api.modelos import (
    CrearTareaRequest, ActualizarTareaRequest, TareaResponse, ListaTareasResponse
)
from api.seguridad import obtener_usuario_actual
from api.servicio import ServicioTareas
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="API de Tareas Segura",
    version="1.0.0",
    description="API con OWASP Top 10 mitigado"
)

servicio = ServicioTareas()

@app.post("/v1/tareas", response_model=TareaResponse, status_code=201)
def crear_tarea(
    datos: CrearTareaRequest,
    usuario_actual: int = Depends(obtener_usuario_actual)
):
    """Crear tarea con autenticación y validación (A07, A03)"""
    tarea = servicio.crear(datos, user_id=usuario_actual)

    logger.info(
        f"Tarea {tarea.id} creada por usuario {usuario_actual}",
        extra={"event": "tarea_creada", "tarea_id": tarea.id, "user_id": usuario_actual}
    )

    return tarea

@app.get("/v1/tareas", response_model=ListaTareasResponse)
def listar_tareas(
    usuario_actual: int = Depends(obtener_usuario_actual),
    limite: int = Query(10, ge=1, le=100),  # A03: Validación de límites
    offset: int = Query(0, ge=0)
):
    """Listar tareas con paginación (A03, A01)"""
    # A01: Solo retorna tareas del usuario autenticado
    tareas = servicio.listar_por_usuario(
        usuario_actual,
        limite=limite,
        offset=offset
    )

    return {
        "tareas": tareas,
        "total": len(tareas),
        "limite": limite,
        "offset": offset
    }

@app.get("/v1/tareas/{tarea_id}", response_model=TareaResponse)
def obtener_tarea(
    tarea_id: int,
    usuario_actual: int = Depends(obtener_usuario_actual)
):
    """Obtener tarea con validación de ownership (A01)"""
    tarea = servicio.obtener_por_id(tarea_id)

    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # A01: Validar ownership
    if tarea.user_id != usuario_actual:
        logger.warning(
            f"Intento no autorizado de acceder a tarea {tarea_id} por usuario {usuario_actual}",
            extra={"event": "acceso_no_autorizado", "tarea_id": tarea_id, "user_id": usuario_actual}
        )
        raise HTTPException(status_code=403, detail="Acceso denegado")

    return tarea

@app.put("/v1/tareas/{tarea_id}", response_model=TareaResponse)
def actualizar_tarea(
    tarea_id: int,
    datos: ActualizarTareaRequest,  # A03: Validación con Pydantic
    usuario_actual: int = Depends(obtener_usuario_actual)
):
    """Actualizar tarea con ownership y mass assignment protection (A01, A03)"""
    tarea = servicio.obtener_por_id(tarea_id)

    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # A01: Validar ownership
    if tarea.user_id != usuario_actual:
        logger.warning(
            f"Intento no autorizado de actualizar tarea {tarea_id}",
            extra={"event": "actualizacion_no_autorizada", "tarea_id": tarea_id}
        )
        raise HTTPException(status_code=403, detail="Acceso denegado")

    # A03: Solo actualizar campos permitidos (previene mass assignment)
    datos_actualizacion = datos.model_dump(exclude_unset=True)
    tarea_actualizada = servicio.actualizar(tarea_id, datos_actualizacion)

    logger.info(
        f"Tarea {tarea_id} actualizada",
        extra={"event": "tarea_actualizada", "tarea_id": tarea_id}
    )

    return tarea_actualizada

@app.delete("/v1/tareas/{tarea_id}", status_code=204)
def eliminar_tarea(
    tarea_id: int,
    usuario_actual: int = Depends(obtener_usuario_actual)
):
    """Eliminar tarea con ownership y audit log (A01, A09)"""
    tarea = servicio.obtener_por_id(tarea_id)

    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # A01: Validar ownership
    if tarea.user_id != usuario_actual:
        logger.warning(
            f"Intento no autorizado de eliminar tarea {tarea_id}",
            extra={"event": "eliminacion_no_autorizada", "tarea_id": tarea_id}
        )
        raise HTTPException(status_code=403, detail="Acceso denegado")

    servicio.eliminar(tarea_id)

    # A09: Audit log para eliminaciones
    logger.info(
        f"Tarea {tarea_id} eliminada",
        extra={"event": "tarea_eliminada", "tarea_id": tarea_id, "user_id": usuario_actual}
    )

    return None  # 204 No Content
```

### Paso 4: Testing de seguridad

Crea tests que **validen las mitigaciones OWASP**:

```python
# tests/test_seguridad.py
def test_acceso_sin_autenticacion_devuelve_401():
    """A07: Endpoints requieren autenticación"""
    response = client.get("/v1/tareas")
    assert response.status_code == 401

def test_acceso_tarea_ajena_devuelve_403():
    """A01: No se puede acceder a tareas de otros usuarios"""
    # Usuario 1 crea tarea
    response = client.post(
        "/v1/tareas",
        json={"nombre": "Tarea de usuario 1"},
        headers={"X-API-Key": "api_key_usuario_1"}
    )
    tarea_id = response.json()["id"]

    # Usuario 2 intenta acceder (debe retornar 403)
    response = client.get(
        f"/v1/tareas/{tarea_id}",
        headers={"X-API-Key": "api_key_usuario_2"}
    )
    assert response.status_code == 403

def test_validacion_pydantic_rechaza_datos_invalidos():
    """A03: Validación de entrada con Pydantic"""
    response = client.post(
        "/v1/tareas",
        json={"nombre": ""},  # Nombre vacío (invalido)
        headers={"X-API-Key": "api_key_valida"}
    )
    assert response.status_code == 422  # Validation error

def test_paginacion_rechaza_limites_invalidos():
    """A03: Validación de límites en paginación"""
    response = client.get(
        "/v1/tareas?limite=1000",  # Excede límite máximo (100)
        headers={"X-API-Key": "api_key_valida"}
    )
    assert response.status_code == 422

def test_logging_registra_eventos_criticos(caplog):
    """A09: Eventos de seguridad se registran"""
    # Intentar acceder a tarea ajena
    client.get(
        "/v1/tareas/123",
        headers={"X-API-Key": "api_key_usuario_2"}
    )

    # Verificar que se registró el evento
    assert "acceso_no_autorizado" in caplog.text
```

### Paso 5: Documentación y README

Crea un `README.md` profesional:

```markdown
# API de Tareas Segura

API RESTful con FastAPI implementando **OWASP Top 10** mitigaciones.

## Seguridad implementada

### A01: Broken Access Control ✅
- Validación de ownership en todos los endpoints
- Retorna 403 si usuario intenta acceder a recursos ajenos

### A03: Injection ✅
- Validación con Pydantic (min_length, max_length)
- No se usa eval(), exec()
- Queries usan ORM

### A07: Authentication Failures ✅
- API Keys hasheadas con SHA-256
- Comparación timing-safe con `secrets.compare_digest`
- API Keys de 32+ caracteres

### A08: Software/Data Integrity Failures ✅
- Dependencias auditadas con Safety
- Versiones pinneadas en `requirements.txt`

### A09: Security Logging Failures ✅
- Logs de autenticación fallida
- Logs de intentos no autorizados (403)
- Logs de eventos críticos (CRUD)

## Instalación

```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
cp .env.template .env
# Editar .env con tus valores
```

## Uso

```bash
# Ejecutar API
uvicorn api.api:app --reload

# Auditoría de seguridad
safety check
bandit -r api/ -ll

# Tests
pytest --cov=api --cov-report=term-missing
```

## Endpoints

- **POST /v1/tareas** - Crear tarea (requiere autenticación)
- **GET /v1/tareas** - Listar tareas (paginación: ?limite=10&offset=0)
- **GET /v1/tareas/{id}** - Obtener tarea (valida ownership)
- **PUT /v1/tareas/{id}** - Actualizar tarea
- **DELETE /v1/tareas/{id}** - Eliminar tarea

## Testing con curl

```bash
# Crear tarea
curl -X POST http://localhost:8000/v1/tareas \
  -H "X-API-Key: tu_api_key_aqui" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Completar proyecto seguro", "descripcion": "Implementar OWASP Top 10"}'

# Listar tareas
curl http://localhost:8000/v1/tareas?limite=10 \
  -H "X-API-Key: tu_api_key_aqui"
```
```

### Checklist de completitud del proyecto

**Antes de enviar el proyecto, verifica**:

#### Código
- [ ] 5 endpoints implementados y funcionando
- [ ] Todas las mitigaciones OWASP implementadas (8/8)
- [ ] Tests de seguridad pasando (5+ tests de vulnerabilidades)
- [ ] Cobertura de tests >80%

#### Seguridad
- [ ] `safety check` sin vulnerabilidades críticas/altas
- [ ] `bandit -r api/ -ll` sin issues de severidad alta
- [ ] `.env` en `.gitignore`
- [ ] No hay secretos hardcodeados en código

#### Documentación
- [ ] README.md completo con seguridad implementada
- [ ] `.env.template` con variables necesarias
- [ ] Comentarios en código explicando mitigaciones OWASP
- [ ] Swagger docs funcionando (`/docs`)

#### Auditoría con IA
- [ ] Código auditado con `SECURITY_CHECKLIST.md`
- [ ] Revisado por 3 agentes (FastAPI Coach, Python Practices, API Reviewer)
- [ ] Vulnerabilidades detectadas y corregidas
- [ ] Prompts usados documentados en `notes.md`

---

## Resumen de la Clase 2

**Has aprendido**:

### Parte 1: Fundamentos de seguridad (1h)
- Autenticación con API Keys
- Variables de entorno con `.env`
- Validación de entrada con Pydantic

### Parte 2: OWASP Top 10 para APIs (3h)
- **A01: Broken Access Control** → Validación de ownership
- **A03: Injection** → Validación con Pydantic, evitar eval()
- **A07: Authentication Failures** → API Keys fuertes, timing-safe comparison
- **A08: Software/Data Integrity** → Auditoría con Safety, versiones pinneadas
- **A09: Security Logging** → Logs de eventos de seguridad, Sentry

### Parte 3: Auditoría de código IA (2h)
- Detectar vulnerabilidades en código generado por IA
- Auditar sistemáticamente con checklists
- Usar agentes especializados para hardening
- Crear checklist reutilizable

### Parte 4: Proyecto final (1h)
- API completa con OWASP Top 10 mitigado
- Tests de seguridad
- Documentación profesional
- Auditoría con IA

**Total**: 7 horas de contenido de seguridad + IA

### Habilidades adquiridas

**Técnicas**:
- [ ] Implementas autenticación con API Keys seguras
- [ ] Validas ownership para prevenir Broken Access Control
- [ ] Usas Pydantic para prevenir Injection
- [ ] Auditas dependencias con Safety
- [ ] Implementas logging de seguridad con Python logging
- [ ] Creas tests de seguridad

**Con IA**:
- [ ] Sabes que la IA genera código funcional pero no siempre seguro
- [ ] Das contexto de seguridad en tus prompts
- [ ] Auditas código IA con checklist sistemático
- [ ] Usas agentes educacionales para hardening
- [ ] Tienes un workflow: Generar → Auditar → Corregir → Re-auditar

**Profesionales**:
- [ ] Conoces OWASP Top 10 para APIs
- [ ] Puedes auditar código para vulnerabilidades
- [ ] Implementas seguridad desde el diseño (not bolted on)
- [ ] Documentas seguridad en README
- [ ] Eres un desarrollador consciente de seguridad

### Próximos pasos

**Clase 3 del Módulo 3**: Autenticación avanzada con JWT
- Tokens JWT (JSON Web Tokens)
- Refresh tokens
- Password hashing con bcrypt
- OAuth 2.0 flows

**Para profundizar**:
- OWASP API Security Top 10 completo: https://owasp.org/API-Security/
- FastAPI Security docs: https://fastapi.tiangolo.com/tutorial/security/
- Python Cryptography: https://cryptography.io/
- Sentry para FastAPI: https://docs.sentry.io/platforms/python/guides/fastapi/

---

## Recursos de la clase

**Archivos de referencia**:
- `ejemplos_vulnerables/` - Código vulnerable típico de IA
- `ejercicios/` - 4 ejercicios prácticos con soluciones
- `SECURITY_CHECKLIST.md` - Checklist de auditoría reutilizable
- `prompts_seguridad.md` - Prompts reutilizables para seguridad
- `notes.md` - Aprendizajes y decisiones de la clase

**Agentes educacionales usados**:
- Security Hardening Mentor (detección de vulnerabilidades)
- FastAPI Design Coach (anti-patrones de diseño)
- Python Best Practices Coach (patrones inseguros de Python)
- API Design Reviewer (diseño RESTful + OWASP)

---

**¡Felicidades!** Has completado la Clase 2: Seguridad básica + OWASP Top 10 + Auditoría con IA. Ahora sabes cómo construir APIs seguras y auditar código generado por IA sistemáticamente.