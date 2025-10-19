# Clase 1 - El código que se defiende solo

Antes de comenzar, si estás siguiendo el repo con carpetas con clase, toca añadir al CI la siguiente ruta para que se hagan los test

```sql
  - "Módulo 3 – Calidad y Seguridad/Clase 1 - El codigo que se defiende solo”
```

## 🧠 ¿Qué estamos haciendo aquí?

Hasta ahora has hecho:

- Un CLI que gestiona tareas.
- Una API limpia, separada por capas.
- Tests que confirman que lo básico funciona.
- Y un CI que los lanza solos cada vez que haces push.

Todo bonito… **pero frágil**.

Hoy vamos a enseñarle a tu código a **defenderse solo**:

- A gritar si alguien borra algo sin querer.
- A frenar PRs con errores.
- A detectar código mal escrito o con partes sin testear.

---

## 🧩 El problema real

Imagina esto:

Alguien (puedes ser tú dentro de dos semanas) sube un cambio y se carga la parte que marca las tareas como completadas.

Los tests no se enteran.

El CI dice que todo está ok.

La API sigue funcionando… pero rota.

**¿Por qué?**

Porque nadie comprobó si esa parte del código seguía presente.

No tenías cobertura. No tenías una alarma.

Hoy vas a poner esas alarmas.

---

## 🔧 ¿Qué vamos a hacer exactamente?

### Paso 1: Medir lo que no estás probando

Esto es como hacerle un chequeo a tu app.

Corre esto:

```bash
pip install pytest-cov
pytest --cov=api --cov-report=term-missing

```

Y verás algo así:

```
====================== tests coverage ==============
coverage: platform win32, python 3.13.5-final-0 

Name                         Stmts   Miss  Cover   Missing
----------------------------------------------------------
api\__init__.py                  0      0   100%
api\api.py                      17      1    94%   28
api\repositorio_base.py          2      0   100%
api\repositorio_json.py         22      2    91%   15-16
api\repositorio_memoria.py      12      1    92%   17
api\servicio_tareas.py          16      1    94%   23
----------------------------------------------------------
TOTAL                           69      5    93%
================= 3 passed in 0.78s =============
```

Esto te dice qué archivos están cubiertos por tus tests y qué líneas se están quedando sin comprobar.

¿Mola? ¿te pensabas que ibas a tener que irte acordando de revisar todo como un campeón?

Pues ahora ya sabes como comprobar las funciones que no están testeadas

Espero que te haya gustado el truquito 

---

### Paso 2: Escribir tests nuevos

Ahora que sabes qué zonas están “desnudas”, escribe tests que:

- Prueben errores (ej. crear tarea sin nombre, que devuelva 422).
- Prueben con datos raros.
- Comprueben que al cambiar de repositorio, todo sigue funcionando igual.

💡 *Haz tests que confirmen que “el código no se ha ido de vacaciones sin avisar”*.

---

### Paso 3: Configurar el CI para que te frene si algo falla

Esto es clave.

Modifica tu pipeline `.github/workflows/ci.yml` para que:

- Corra los tests **con cobertura**.
- Falle si la cobertura está por debajo del 80%.
- Pase un linter (`flake8`, `ruff`) para que el código no sea una selva.

Así, si alguien hace un PR que borra una función o sube una chapuza, **GitHub no lo deja pasar**.

---

### Paso 4: Pedírselo a la IA (pero con cabeza)

Aquí no queremos que la IA lo haga todo. Queremos que te dé ideas y te revise lo que hiciste.

Pídeselo así:

```
Rol: Auditor de calidad Python.
Contexto: Tengo una API con FastAPI, tests unitarios y CI básico.
Objetivo: Revísame los riesgos de calidad y seguridad.

Entrega: lista con
- puntos débiles (tests, seguridad, estructura),
- acciones prioritarias (alta / media / baja),
- posibles mejoras automatizables en el pipeline CI.
```

Y verás cómo te suelta cosas que puedes convertir en issues o tareas para mejorar la calidad.

---

## 🔒 IA genera código inseguro - aprende a detectarlo

Hasta ahora hablamos de calidad: cobertura, linters, tests. Pero hay algo más crítico: **seguridad**.

La IA es rápida, eficiente y muy buena generando código funcional. **Pero no siempre genera código seguro.**

### El problema real

La IA te puede generar:
- **SQL injection**: Concatenando strings en queries
- **Secretos hardcoded**: API keys directamente en el código
- **Validación insuficiente**: Aceptando cualquier input sin filtros
- **Dependencias vulnerables**: Usando versiones antiguas con CVEs conocidos
- **Logging de datos sensibles**: Imprimiendo passwords en logs

**¿Por qué?** Porque la IA aprende de código público (que no siempre es seguro) y prioriza "que funcione" sobre "que sea seguro".

### Ejemplo 1: SQL Injection

**❌ Código inseguro que la IA puede generar:**

```python
# NUNCA hagas esto
def buscar_usuario(nombre: str):
    query = f"SELECT * FROM usuarios WHERE nombre = '{nombre}'"
    cursor.execute(query)
    return cursor.fetchall()
```

**Problema**: Si `nombre = "'; DROP TABLE usuarios; --"`, tu base de datos desaparece.

**✅ Código seguro:**

```python
def buscar_usuario(nombre: str):
    query = "SELECT * FROM usuarios WHERE nombre = ?"
    cursor.execute(query, (nombre,))
    return cursor.fetchall()
```

**Cómo detectarlo**:
- ❌ F-strings o concatenación en queries SQL
- ✅ Parámetros preparados o ORMs (SQLAlchemy)

### Ejemplo 2: Secretos hardcoded

**❌ Código inseguro:**

```python
# api/api.py
JWT_SECRET = "mi-secreto-super-seguro-123"
DATABASE_URL = "postgresql://admin:password123@localhost/prod"
```

**Problema**: Esto queda en git, visible para todos. Un atacante lo lee y compromete tu sistema.

**✅ Código seguro:**

```python
import os
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")
DATABASE_URL = os.getenv("DATABASE_URL")

if not JWT_SECRET:
    raise ValueError("JWT_SECRET no está configurado")
```

**Cómo detectarlo**:
- ❌ Strings con `secret`, `password`, `key`, `token` asignados directamente
- ✅ Variables de entorno con `.env` (nunca en git)
- ✅ Validación que falla si no están configuradas

### Ejemplo 3: Validación insuficiente

**❌ Código inseguro:**

```python
@app.post("/tareas")
def crear_tarea(nombre: str):
    # Acepta cualquier cosa, incluso strings vacíos o HTML malicioso
    tarea = servicio.crear(nombre)
    return tarea
```

**Problema**: Acepta `nombre = ""`, `nombre = "<script>alert('XSS')</script>"`, etc.

**✅ Código seguro:**

```python
from pydantic import BaseModel, Field, validator

class CrearTareaRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)

    @validator('nombre')
    def validar_nombre(cls, v):
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        # Opcional: sanitizar HTML
        return v.strip()

@app.post("/tareas")
def crear_tarea(cuerpo: CrearTareaRequest):
    tarea = servicio.crear(cuerpo.nombre)
    return tarea
```

**Cómo detectarlo**:
- ❌ Endpoints que aceptan `str`, `int`, etc. directamente sin validación
- ✅ Pydantic con `Field(..., min_length=1)` y validadores personalizados

### Ejemplo 4: Dependencias vulnerables

**❌ Dependencias sin actualizar:**

```txt
# requirements.txt
fastapi==0.68.0  # Tiene CVE-2021-32677
pydantic==1.8.0  # Versión antigua con bugs de validación
```

**Cómo detectarlo**:
- Ejecuta `pip list --outdated`
- Usa `safety check` (escanea CVEs conocidos)
- Configura Dependabot en GitHub

**✅ Mantén dependencias actualizadas:**

```bash
pip install --upgrade fastapi pydantic
pip freeze > requirements.txt
```

---

## 🛡️ Security Hardening Mentor - Tu auditor de seguridad IA

Ahora que conoces los problemas, necesitas herramientas para detectarlos **antes** de que lleguen a producción.

### ¿Qué es el Security Hardening Mentor?

Es un agente especializado (disponible en `.claude/agents/educational/`) que:

1. **Revisa tu código buscando anti-patrones de seguridad**
2. **Explica por qué son peligrosos** (no solo dice "esto está mal")
3. **Te muestra el código correcto** (con ejemplos before/after)
4. **Te enseña a pensar en seguridad** desde el diseño

### ¿Cuándo usarlo?

- **Antes de hacer commit**: Revisa tus cambios
- **Después de que la IA genere código**: Audítalo antes de usarlo
- **Antes de un PR**: Valida que no introduces vulnerabilidades
- **Cuando aprendes algo nuevo**: Pídele que revise tu implementación

### Ejemplo de uso

**Prompt para el Security Hardening Mentor:**

```
Revisa este código de autenticación JWT que generé con IA.
Busca: secretos hardcoded, validación insuficiente, manejo inseguro de tokens.

[código aquí]

Entrega:
- Anti-patrones detectados (con línea específica)
- Por qué es peligroso cada uno
- Código corregido con explicación
```

**Respuesta esperada:**

```
🔴 CRÍTICO - Secreto hardcoded (línea 5):
   JWT_SECRET = "abc123"

   Por qué es peligroso:
   - Queda visible en git (historial completo)
   - Cualquiera con acceso al repo puede falsificar tokens
   - Imposible rotar sin cambiar código

   Código corregido:
   import os
   JWT_SECRET = os.getenv("JWT_SECRET")
   if not JWT_SECRET:
       raise ValueError("JWT_SECRET requerido en .env")

⚠️ ALTO - Validación insuficiente de token (línea 12):
   [...]
```

### Flujo de trabajo recomendado

1. **IA genera código** → `git add .`
2. **Security Hardening Mentor revisa** → Detecta problemas
3. **Corriges vulnerabilidades** → Aprendes en el proceso
4. **Commit seguro** → `git commit -m "feat: ..."`

**No uses la IA a ciegas. Audita siempre.**

---

## 🎯 Ejercicios de detección de vulnerabilidades

### Ejercicio 1: Encuentra el problema

```python
# api/auth.py
@app.post("/login")
def login(username: str, password: str):
    user = db.query(f"SELECT * FROM users WHERE username='{username}'")
    if user and user.password == password:
        return {"token": "abc123"}
    return {"error": "Invalid credentials"}
```

**Pregunta**: ¿Qué 3 vulnerabilidades encuentras aquí?

<details>
<summary>Respuesta</summary>

1. **SQL Injection** - Concatenación de strings en query
2. **Password en texto plano** - Debería estar hasheado (bcrypt)
3. **Token estático** - `"abc123"` siempre igual, no es JWT

</details>

### Ejercicio 2: Validación insuficiente

```python
@app.post("/tareas")
def crear_tarea(nombre: str, prioridad: int):
    tarea = servicio.crear(nombre, prioridad)
    return tarea
```

**Pregunta**: ¿Qué puede salir mal?

<details>
<summary>Respuesta</summary>

- `nombre = ""` - String vacío
- `nombre = "A" * 10000` - DoS con strings gigantes
- `prioridad = -999` o `999999` - Valores fuera de rango esperado
- Sin Pydantic, FastAPI acepta cualquier cosa

**Solución**: Usar `CrearTareaRequest(BaseModel)` con validación.

</details>

### Ejercicio 3: Busca el secreto

```python
# api/config.py
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
API_KEY = "sk-1234567890abcdef"
JWT_SECRET = os.getenv("JWT_SECRET")
```

**Pregunta**: ¿Qué línea es insegura?

<details>
<summary>Respuesta</summary>

**Línea 5**: `API_KEY = "sk-1234567890abcdef"`

Debería ser:
```python
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY requerida en .env")
```

</details>

### Ejercicio 4: Audita con herramientas

Ejecuta esto en tu proyecto:

```bash
# Busca secretos hardcoded
pip install detect-secrets
detect-secrets scan api/ > secrets.json

# Busca vulnerabilidades de seguridad
pip install bandit
bandit -r api/ -ll

# Busca dependencias vulnerables
pip install safety
safety check
```

**Tarea**: Documenta en `notes.md` qué encontraste y cómo lo corregiste.

---

## 🧪 Mini-proyecto (entregable de esta clase)

Haz lo siguiente:

1. Crea rama `feature/quality-coverage-security`.
2. Añade el nuevo workflow `ci_quality.yml` con cobertura y linter.
3. Mejora tus tests para cubrir mínimo un 80% del código.
4. **NUEVO**: Ejecuta herramientas de seguridad:
   - `bandit -r api/ -ll` (busca vulnerabilidades)
   - `safety check` (escanea dependencias)
   - `detect-secrets scan api/` (busca secretos hardcoded)
5. **NUEVO**: Audita el código con Security Hardening Mentor:
   - Revisa código de autenticación (si existe)
   - Valida que no hay secretos hardcoded
   - Comprueba validación de inputs con Pydantic
6. Haz push y abre un PR.
7. En `notes.md`, apunta:
    - Qué partes no estaban cubiertas (cobertura).
    - **Qué vulnerabilidades encontraste** (bandit, safety, detect-secrets).
    - Qué aprendiste de la auditoría IA con Security Hardening Mentor.
    - Qué tareas dejarías abiertas para reforzar la seguridad.
    - **Cómo corregiste las vulnerabilidades** (código before/after).

---

## ✅ Qué debe quedarte claro

- Tu código ahora tiene una red que **grita si algo se rompe**.
- La cobertura no es "nota", es una **alarma de seguridad**.
- **NUEVO**: La IA genera código funcional, pero **no siempre seguro** - audita siempre.
- **NUEVO**: Conoces los **anti-patrones de seguridad comunes** (SQL injection, secretos hardcoded, validación insuficiente).
- **NUEVO**: Sabes usar el **Security Hardening Mentor** para auditar código antes de hacer commit.
- No todo lo debe escribir la IA, pero sí puede **auditarte** como un mini revisor.
- Tu CI ya no solo lanza tests, **te protege de ti mismo**.

---

Y esto…

No es postureo DevOps.

Es simplemente **programar sin miedo**.

Listo para que tu API empiece a vivir sola sin que se caiga a pedazos.

Cuando tengas tu rama y tu PR, pasamos a **seguridad real**: JWT, `.env`, validaciones y filtros contra ataques.

## 🧹 Extra: Que el código no huela

Hasta ahora hablamos de cobertura (¿estás probando lo que importa?), pero hay otra pata de la calidad: **la legibilidad**.

Ahí entran los **linters**: herramientas que te dicen *“esto está raro”* antes de que se vuelva un problema.

### Vamos con `flake8` (el clásico):

### 🧪 Paso 1 – Instálalo

```bash
pip install flake8

```

### 🧪 Paso 2 – Ejecuta sobre tu carpeta `api`

```bash
flake8 api/

```

Te va a decir cosas como:

```
api/api.py:5:1: F401 'api.repositorio_memoria.RepositorioMemoria' imported but unused
api/repositorio_json.py:3:12: E401 multiple imports on one line
api/repositorio_json.py:34:80: E501 line too long (88 > 79 characters)

```

Traducción:

- Estás importando cosas que no usas → bórralas.
- Hay líneas que ocupan medio monitor → divídelas.
- Hay funciones con nombre `t()` o variables `x` → cámbialas por algo que se entienda.

Y esto tambien puedes meterle el resultado a la IA para que lo arregle (revisalo siempre)

### ⚠️ Importante

No lo haces **para que el linter esté contento**. Lo haces **para que el código no dé asco en dos semanas**.

Un código sin naming claro, con funciones kilométricas y sin estructura es como un piso lleno de cables, comida vieja y gatos imaginarios: puede funcionar, pero nadie quiere vivir ahí.

---

### Bonus: ¿Y si prefieres algo más moderno?

Instala `ruff`, un linter ultra rápido que además te arregla cosas solo.

```bash
pip install ruff
```

```bash
ruff check api/
```

Y si quieres que arregle lo que pueda automáticamente:

```bash
ruff check api/ --fix
```

---

Y esto te acaba de ahorrar unos cuantos tokens o peticiones de cursor.

Creo que con estos dos truquitos, tu codigo va a hacerse mucho mas legible ahora, y no te volveras tan loco al intentar entender lo que esta haciendo la IA.

### ¿Y qué hace la IA aquí?

Prompt directo al grano:

```
Rol: Revisor de código Python.
Contexto: Tengo esta carpeta `api/` con varios archivos. Quiero asegurarme de que el código sea legible, mantenible y sin código muerto.
Objetivo: Señálame variables poco claras, funciones demasiado largas, imports innecesarios o lógica repetida.
Entrega: Lista de sugerencias, ordenadas por prioridad.
```

Te dará sugerencias útiles para refactorizar… pero ahora **tú ya entiendes por qué son importantes**.

Y puede que te encuentre cosas que flake, ruff o pytest no han encontrado

---

## ✅ ¿Qué dejas hecho?

- Linter instalado (`flake8` o `ruff`).
- Código revisado y limpiado.
- Rama con cambios (`feature/quality-coverage`).
- PR que activa el nuevo pipeline CI (tests + cobertura + linter).
- `notes.md` con lo que descubriste al mirar tu propio código con lupa.

---

Ya está. Con esta limpieza, tu repo respira.

Y con la cobertura y los tests nuevos, se defiende.

Ahora sí: pasamos de “funciona” a “esto lo puede tocar otro humano sin llorar”.

## Nota:

En mi caso he reducido las rutas de los test a solo la ultima clase para evitar acumular errores de clases anteriores que no se van a modificar, y seguirán teniendo baja calidad.

En nuestro caso, va fallar el test de calidad por tener flake8 añadido, podriamos arreglar la linea que indica y tener todos los test en verde. O desactivar flake8 para esta clase y evitar que pase el test