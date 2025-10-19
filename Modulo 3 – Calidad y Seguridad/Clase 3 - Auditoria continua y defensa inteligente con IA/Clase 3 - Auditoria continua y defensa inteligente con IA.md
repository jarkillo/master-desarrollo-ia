# 🎓 Clase 3 – Auditoria continua y defensa inteligente con IA

# 🧩 El punto de partida

Tu API ya:

- Tiene cobertura y linters (el código se defiende solo).
- Está protegida con API Key y validaciones Pydantic.
- Ejecuta CI automático en cada PR.

Pero aún depende **de ti** para darte cuenta si algo huele mal en el código.

Y tú eres humano. Te distraes, tienes sueño, o confías demasiado en el “ya pasaron los tests”.

**Aquí entra el siguiente paso de madurez:**

> Enseñar a la IA a auditar tu proyecto mientras tú duermes.
> 

---

## 🧠 Concepto: calidad como sistema vivo

La seguridad y la calidad no son “filtros” que se aplican al final.

Son **sistemas vivos** que observan, alertan y aprenden.

En un proyecto profesional, nadie revisa línea a línea los PRs.

Se confía en tres guardianes:

1. **Los tests** (aseguran que no rompes lo que ya existía).
2. **El CI/CD** (vigila que el proceso sea reproducible).
3. **Los auditores automáticos** (detectan patrones de riesgo o mala práctica).

Hoy tú vas a construir ese tercer guardián.

---

## ⚙️ Aplicación manual – cómo lo haría un dev senior

### Paso 1. Activar la auditoría de seguridad

Instala una herramienta como **bandit**, que analiza tu código en busca de fallos comunes (inyecciones, uso inseguro de `os.system`, contraseñas en texto plano...).

```bash
pip install bandit
bandit -r api/

```

Te devolverá algo como:

```
>> Issue: [B105:hardcoded_password_string] Possible hardcoded password: 'miclave123'
   Severity: High   Confidence: Medium
   Location: api/dependencias.py:10
```

Bandit no corrige —solo **te avisa**. (Esto puede que no te aparezca porque lo tenemos en un .env)

```sql
[main]  INFO    profile include tests: None
[main]  INFO    profile exclude tests: None
[main]  INFO    cli include tests: None
[main]  INFO    cli exclude tests: None
[main]  INFO    running on Python 3.13.5
Run started:2025-10-05 16:37:50.122060

Test results:
        No issues identified.

Code scanned:
        Total lines of code: 83
        Total lines skipped (#nosec): 0

Run metrics:
        Total issues (by severity):
                Undefined: 0
                Low: 0
                Medium: 0
                High: 0
        Total issues (by confidence):
                Undefined: 0
                Low: 0
                Medium: 0
                High: 0
Files skipped (0):
```

Si todo va bien, te dará esto.

Esto ya te convierte en un desarrollador que no “confía”, sino que **verifica**.

---

### Paso 2. Añadir la auditoría al CI

Dentro de tu `.github/workflows/ci_quality.yml` o en un archivo nuevo:

```yaml
      - name: Auditoría de seguridad
        working-directory: ${{ matrix.class_dir }}
        run: |
            pip install bandit
            bandit -r api/ -ll
```

Esto lanza la revisión automáticamente con cada PR.

Si detecta algo grave, el pipeline fallará.

Y nadie podrá hacer merge hasta arreglarlo. (Siempre que el repositorio este configurado así)

---

## 🤖 Aplicación con IA – cómo delegarlo con cabeza

No se trata de que la IA te diga “tu código es inseguro”.

Se trata de que le **pidas un informe técnico** y **lo traduzcas a acciones concretas**.

Prompt ejemplo:

```
Rol: Auditor de seguridad y calidad de código Python.
Contexto: Proyecto FastAPI con repositorios y CI configurado.
Objetivo: Revisa la carpeta `api/` y los tests.

Entrega:
- Riesgos de seguridad (alta / media / baja).
- Recomendaciones de refactor.
- Código que pueda mejorarse por legibilidad o separación de responsabilidades.
- Mejoras en el pipeline CI.
```

Con eso, la IA generará un informe tipo auditoría.

Luego tú eliges qué implementar o convertir en issues de GitHub.

Y puedes automatizar esa auditoría como *tarea recurrente del pipeline* (por ejemplo, una vez por semana).

---

## 🔒 Validación de Inputs - La primera línea de defensa

Antes de auditar código existente, necesitas prevenir que código inseguro llegue a tu aplicación.

**La validación de inputs es tu primera línea de defensa** contra ataques.

### El problema real

Sin validación robusta, tu API acepta:
- `nombre = ""` - String vacío
- `edad = -5` - Valores negativos
- `email = "no-es-email"` - Formatos inválidos
- `prioridad = 999999` - Valores fuera de rango
- `<script>alert('XSS')</script>` - Inyecciones HTML/JS

**Pydantic te protege**, pero necesitas saber qué validar.

### ¿Dónde entra la IA?

La IA es **excelente identificando edge cases** que no pensaste:

**Prompt para identificar edge cases**:
```
Rol: Security auditor especializado en validación de inputs.
Contexto: Tengo este modelo Pydantic para una API de tareas:

class CrearTareaRequest(BaseModel):
    nombre: str = Field(..., min_length=1)
    prioridad: int = Field(default=1)

Objetivo: Lista todos los edge cases peligrosos que debería validar.

Entrega:
- Edge cases por campo (nombre, prioridad)
- Tipo de ataque que previene cada validación
- Código Pydantic para implementar cada validación
```

**Respuesta esperada de la IA**:

```markdown
## Edge Cases Peligrosos

### Campo: nombre
1. **String vacío o solo espacios**: `nombre = "   "`
   - Ataque: DoS (tareas basura)
   - Validación: `@validator('nombre') def validar_nombre(cls, v): return v.strip()`

2. **String demasiado largo**: `nombre = "A" * 100000`
   - Ataque: DoS (memoria/base de datos)
   - Validación: `Field(..., min_length=1, max_length=200)`

3. **Inyección HTML/XSS**: `nombre = "<script>alert('XSS')</script>"`
   - Ataque: XSS en frontend
   - Validación: Sanitizar HTML con bleach o rechazar caracteres especiales

4. **Unicode malicioso**: `nombre = "\u202E` (Right-to-Left Override)
   - Ataque: Confusión visual
   - Validación: Filtrar caracteres de control Unicode

### Campo: prioridad
1. **Valores negativos**: `prioridad = -1`
   - Validación: `Field(..., ge=1, le=5)`

2. **Valores fuera de rango**: `prioridad = 9999`
   - Validación: `Field(..., ge=1, le=5)`

3. **Overflow de enteros**: `prioridad = 2**63`
   - Validación: Pydantic maneja esto automáticamente
```

---

## 🛡️ Security Hardening Mentor - Audita tus validaciones

Ahora que la IA te ayudó a identificar edge cases, necesitas **validar que tu implementación es segura**.

### ¿Qué es el Security Hardening Mentor?

Es un agente especializado (disponible en `.claude/agents/educational/security-hardening-mentor.md`) que:

1. **Revisa tus validaciones Pydantic** buscando gaps de seguridad
2. **Explica por qué cada gap es peligroso** (no solo dice "esto está mal")
3. **Te muestra código corregido** con explicaciones detalladas
4. **Te enseña a pensar en seguridad** desde el diseño

### Workflow: IA genera → Estudiante audita → Security Mentor valida

**Paso 1**: Usa IA para generar validaciones

**Prompt**:
```
Genera modelo Pydantic completo para una API de tareas con validaciones robustas.

Campos:
- nombre: string (requerido)
- descripcion: string opcional
- prioridad: 1-5
- fecha_limite: fecha futura opcional

Incluye:
- Field validators
- Model validators (validaciones entre campos)
- Sanitización de inputs
```

**Paso 2**: La IA te devuelve código (PERO NO LO USES A CIEGAS)

```python
# Código generado por IA (puede tener vulnerabilidades)
from pydantic import BaseModel, Field, validator
from datetime import datetime

class CrearTareaRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)
    descripcion: str | None = None
    prioridad: int = Field(default=1, ge=1, le=5)
    fecha_limite: datetime | None = None

    @validator('nombre')
    def validar_nombre(cls, v):
        return v.strip()

    @validator('descripcion')
    def validar_descripcion(cls, v):
        if v:
            return v.strip()
        return v
```

**Paso 3**: Audita con Security Hardening Mentor

**Prompt para el Security Mentor**:
```
Revisa este modelo Pydantic para una API de tareas.
Busca: validaciones insuficientes, sanitización faltante, edge cases no manejados.

[pega el código]

Entrega:
- Vulnerabilidades encontradas (con línea específica)
- Por qué es peligroso cada gap
- Código corregido con explicación
```

**Respuesta esperada del Security Mentor**:

```markdown
🔴 CRÍTICO - Validación de nombre insuficiente (línea 10):
   @validator('nombre')
   def validar_nombre(cls, v):
       return v.strip()

   Por qué es peligroso:
   - Acepta nombres solo con espacios: "    " → strip → "" → válido ❌
   - No previene inyección HTML: "<script>alert()</script>"
   - No valida caracteres de control Unicode

   Código corregido:
   @validator('nombre')
   def validar_nombre(cls, v):
       v = v.strip()
       if not v:
           raise ValueError("El nombre no puede estar vacío")
       # Rechazar HTML/scripts
       if '<' in v or '>' in v:
           raise ValueError("El nombre no puede contener HTML")
       return v

⚠️ ALTO - fecha_limite sin validación (línea 8):
   fecha_limite: datetime | None = None

   Por qué es peligroso:
   - Acepta fechas pasadas (tarea con deadline ayer)
   - Acepta fechas muy lejanas (2099 - posible ataque DoS)

   Código corregido:
   @validator('fecha_limite')
   def validar_fecha_limite(cls, v):
       if v and v < datetime.now():
           raise ValueError("La fecha límite debe ser futura")
       if v and (v - datetime.now()).days > 365 * 10:
           raise ValueError("Fecha límite demasiado lejana")
       return v

🟡 MEDIO - descripcion acepta strings enormes (línea 7):
   descripcion: str | None = None

   Sin max_length, acepta 10GB de texto → DoS

   Código corregido:
   descripcion: str | None = Field(None, max_length=2000)
```

**Paso 4**: Corriges vulnerabilidades y aprendes en el proceso

Ahora implementas el código corregido **entendiendo por qué** cada validación es importante.

---

## 🎯 Ejercicios Prácticos - Detecta Vulnerabilidades

### Ejercicio 1: Encuentra el gap de seguridad

```python
from pydantic import BaseModel, Field

class UsuarioRegistro(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)
    email: str
```

**Pregunta**: ¿Qué 4 vulnerabilidades tiene este modelo?

<details>
<summary>Respuesta</summary>

1. **username sin max_length** → DoS con usernames gigantes
2. **password sin validación de complejidad** → Acepta "12345678"
3. **email sin formato** → Acepta "no-es-email"
4. **password en texto plano** → Debería hashearse ANTES de guardarse

**Código corregido**:
```python
from pydantic import BaseModel, Field, EmailStr, validator
import re

class UsuarioRegistro(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    email: EmailStr  # Valida formato email automáticamente

    @validator('username')
    def validar_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError("Username solo puede contener letras, números y _")
        return v

    @validator('password')
    def validar_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError("Password debe tener al menos una mayúscula")
        if not re.search(r'[0-9]', v):
            raise ValueError("Password debe tener al menos un número")
        # NOTA: Hashear password en el servicio, NO aquí
        return v
```

</details>

### Ejercicio 2: Audita con Security Hardening Mentor

Toma el código del Ejercicio 1 (versión incorrecta) y:

1. Pídele al Security Hardening Mentor que lo audite
2. Compara su respuesta con la solución del Ejercicio 1
3. Implementa las correcciones

**Prompt sugerido**:
```
Rol: Security Hardening Mentor
Audita este modelo Pydantic para registro de usuarios.
Busca: validaciones faltantes, formatos sin validar, edge cases peligrosos.

[código del Ejercicio 1]

Entrega:
- Vulnerabilidades por severidad (CRÍTICO/ALTO/MEDIO)
- Por qué es peligroso cada gap
- Código corregido paso a paso
```

---

## ✅ Checklist de Seguridad para Validaciones

Usa esta checklist ANTES de hacer commit de cualquier modelo Pydantic:

### Validaciones Básicas
- [ ] Todos los campos tienen `min_length` y `max_length` apropiados
- [ ] Números tienen `ge` (mayor o igual) y `le` (menor o igual)
- [ ] Fechas tienen validación de rango (no pasadas, no muy lejanas)
- [ ] Emails usan `EmailStr` de Pydantic

### Sanitización
- [ ] Strings se limpian con `.strip()` en validators
- [ ] Se rechazan caracteres HTML (`<`, `>`) si no se espera HTML
- [ ] Se validan formatos con regex (username, teléfono, etc.)

### Edge Cases
- [ ] Strings vacíos rechazados (no solo `None`)
- [ ] Valores negativos manejados (edad, precio, cantidad)
- [ ] Valores enormes (DoS) prevenidos con límites
- [ ] Caracteres Unicode peligrosos filtrados

### Validaciones Entre Campos
- [ ] Model validators para lógica entre campos
- [ ] Ejemplo: `fecha_inicio < fecha_fin`
- [ ] Ejemplo: Tareas urgentes requieren deadline

### Auditoría con IA
- [ ] Security Hardening Mentor revisó el código
- [ ] Todos los gaps CRÍTICOS corregidos
- [ ] Gaps ALTOS documentados en backlog si no se corrigen
- [ ] Tests de edge cases escritos

---

## 🧪 Tests de Validación Generados por IA

Pídale a la IA que genere tests para tus edge cases:

**Prompt**:
```
Genera pytest tests para validar estos edge cases en mi modelo Pydantic:

[lista de edge cases del Security Mentor]

Formato:
- Un test por edge case
- Usa TestClient de FastAPI
- Valida status code 422 (Unprocessable Entity)
- Valida mensaje de error específico
```

**Tests generados**:

```python
# tests/test_validaciones_edge_cases.py
from fastapi.testclient import TestClient
from api.api import app
import pytest

client = TestClient(app)

def test_nombre_vacio_rechazado():
    r = client.post("/tareas", json={"nombre": ""})
    assert r.status_code == 422
    assert "nombre no puede estar vacío" in r.json()["detail"][0]["msg"]

def test_nombre_solo_espacios_rechazado():
    r = client.post("/tareas", json={"nombre": "    "})
    assert r.status_code == 422

def test_nombre_con_html_rechazado():
    r = client.post("/tareas", json={"nombre": "<script>alert()</script>"})
    assert r.status_code == 422

def test_prioridad_negativa_rechazada():
    r = client.post("/tareas", json={"nombre": "Tarea", "prioridad": -1})
    assert r.status_code == 422

def test_prioridad_fuera_de_rango_rechazada():
    r = client.post("/tareas", json={"nombre": "Tarea", "prioridad": 99})
    assert r.status_code == 422

def test_descripcion_muy_larga_rechazada():
    r = client.post("/tareas", json={
        "nombre": "Tarea",
        "descripcion": "A" * 10000
    })
    assert r.status_code == 422
```

---

## 🧩 Mini-proyecto de la clase

1. Crea la rama `feature/auditoria-validacion-continua`.

2. **Validación de Inputs**:
    - Usa IA para identificar edge cases en tus modelos Pydantic
    - Implementa validaciones robustas (Field validators + Model validators)
    - Audita con Security Hardening Mentor
    - Corrige todas las vulnerabilidades CRÍTICAS

3. **Auditoría Automática**:
    - Instala y ejecuta `bandit` localmente
    - Crea un nuevo workflow `.github/workflows/auditoria.yml` que:
        - Corra `bandit` sobre la carpeta `api/`.
        - Falle si detecta vulnerabilidades altas.

4. **Tests de Edge Cases**:
    - Genera tests con IA para validar edge cases
    - Asegura 80%+ de cobertura
    - Tests deben validar status code 422 y mensajes de error

5. **Documentación**:
    - Pídele a la IA el informe de auditoría completo
    - Anótalo en `notes.md` con sección "Validaciones" y "Auditoría"
    - Documenta qué vulnerabilidades encontraste y cómo las corregiste

6. Abre PR con el título **"Auditoría continua + Validaciones de seguridad"**.

---

## ✅ Checklist final

### Validación de Inputs
- [ ]  Todos tus modelos Pydantic tienen validaciones robustas
- [ ]  Usaste IA para identificar edge cases peligrosos
- [ ]  El Security Hardening Mentor auditó tus validaciones
- [ ]  Corregiste todas las vulnerabilidades CRÍTICAS
- [ ]  Implementaste tests para edge cases (strings vacíos, valores negativos, HTML injection)

### Auditoría Automática
- [ ]  Has añadido un análisis de seguridad automático (bandit).
- [ ]  Has generado un informe de auditoría con IA.
- [ ]  Tu pipeline CI avisa si hay código inseguro.
- [ ]  Entiendes cómo combinar pruebas, cobertura y análisis estático.

### Comprensión
- [ ]  Entiendes el workflow: IA genera → Estudiante audita → Security Mentor valida
- [ ]  Sabes cuándo confiar en código generado por IA (nunca a ciegas)
- [ ]  Puedes usar el Security Hardening Mentor para revisar código
- [ ]  Tu código ahora no solo se defiende… **aprende a defenderse.**

---

## 🌱 Qué sigue

En la siguiente clase entraremos ya en **seguridad avanzada**:

JWT, cifrado y tokens temporales.

Pero no antes de tener una base sólida que te diga: *“puedo dormir tranquilo, si algo se rompe, el sistema me lo cuenta antes que el cliente.”*