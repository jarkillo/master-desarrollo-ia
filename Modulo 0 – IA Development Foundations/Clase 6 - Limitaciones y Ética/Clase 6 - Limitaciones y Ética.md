# Clase 6 - Limitaciones y Ética en IA para Desarrollo

**Duración**: 6 horas
**Objetivo**: Entender las limitaciones fundamentales de IA, cuándo NO usarla, responsabilidad como desarrollador, y principios éticos para desarrollar con IA conscientemente.

---

## Índice

1. [Conceptos Clave](#1-conceptos-clave-45-min)
2. [Limitaciones Técnicas de IA](#2-limitaciones-técnicas-de-ia-15h)
3. [Cuándo NO Usar IA](#3-cuándo-no-usar-ia-1h)
4. [Responsabilidad del Desarrollador](#4-responsabilidad-del-desarrollador-1h)
5. [Ética en Desarrollo con IA](#5-ética-en-desarrollo-con-ia-1h)
6. [Proyecto Final - Código de Conducta IA](#6-proyecto-final---código-de-conducta-ia-45-min)
7. [Evaluación y Cierre del Módulo 0](#7-evaluación-y-cierre-del-módulo-0)

---

## 1. Conceptos Clave (45 min)

### 1.1 La Falacia del "IA Hace Todo" (15 min)

**Mito común**: "Con IA ya no necesito aprender a programar"

**Realidad**: IA es un **asistente experto**, no un **reemplazo del desarrollador**.

**Analogía**: Calculadora

- **Antes de calculadora**: Aprendías aritmética mental
- **Después de calculadora**: Seguías necesitando saber QUÉ calcular, CÓMO interpretar resultados
- **Calculadora NO reemplazó** a matemáticos, ingenieros, contadores

**Lo mismo con IA**:
- **IA NO decide** qué features construir
- **IA NO diseña** arquitectura de sistemas complejos
- **IA NO asume** responsabilidad del código en producción

**TÚ decides**, IA asiste.

---

### 1.2 Espectro de Confiabilidad de IA (15 min)

**No todo lo que genera IA es igualmente confiable**.

**Alta confiabilidad** (puedes confiar más):
- ✅ Sintaxis de código estándar (for loops, funciones básicas)
- ✅ Patrones comunes (CRUD endpoints, validación con Pydantic)
- ✅ Refactoring simple (renombrar variables, extract method)
- ✅ Generación de tests básicos (happy path)

**Media confiabilidad** (revisar cuidadosamente):
- ⚠️ Lógica de negocio específica de tu dominio
- ⚠️ Integración de múltiples sistemas
- ⚠️ Performance optimization
- ⚠️ Código de seguridad (auth, crypto)

**Baja confiabilidad** (NO confiar ciegamente):
- ❌ Arquitectura de sistemas distribuidos
- ❌ Decisiones de infraestructura (qué DB usar, cómo escalar)
- ❌ Edge cases complejos
- ❌ Código crítico para vida/dinero (medicina, finanzas)

**Regla**: Cuanto más crítico o específico, menos confiable es IA sin validación humana.

---

### 1.3 Responsabilidad No Se Delega (15 min)

**Principio fundamental**: Si tu nombre está en el commit, TÚ eres responsable del código.

**Escenario real**:

```python
# IA generó este código
def transferir_dinero(origen, destino, monto):
    origen.saldo -= monto
    destino.saldo += monto
    db.save(origen)
    db.save(destino)
```

**Bug**: No es atómico. Si falla `db.save(destino)`, el dinero desaparece.

**Pregunta**: ¿Quién es responsable del bug?

- ❌ "La IA generó mal código" → NO es excusa
- ✅ "YO no validé el código antes de hacer merge" → Correcto

**Tu responsabilidad**:
1. Entender el código que commit (línea por línea)
2. Validar que funciona (tests, revisión)
3. Anticipar edge cases
4. Documentar decisiones

**IA genera, TÚ validas y asumes responsabilidad**.

---

## 2. Limitaciones Técnicas de IA (1.5h)

### 2.1 Hallucinations (Invención de Código) (20 min)

**Definición**: IA "inventa" APIs, funciones o sintaxis que no existen.

**Ejemplo 1: API inexistente**

**Prompt**:
```
Usa la librería fastapi-magic para generar endpoints automáticamente
```

**IA genera**:
```python
from fastapi_magic import auto_generate_crud

app = auto_generate_crud(Model=Tarea)
```

**Problema**: `fastapi-magic` NO EXISTE. IA inventó la librería.

**Cómo detectar**:
- ❌ NO asumas que la librería existe
- ✅ Verifica en PyPI (https://pypi.org/)
- ✅ Busca documentación oficial

---

**Ejemplo 2: Método inexistente**

**IA genera**:
```python
# IA inventa método que no existe en FastAPI
@app.post("/tareas")
async def crear_tarea(tarea: Tarea):
    return await tarea.save_to_database()  # ❌ Pydantic NO tiene este método
```

**Problema**: Pydantic models NO tienen método `.save_to_database()`.

**Cómo detectar**:
- ✅ Revisa documentación oficial (FastAPI, Pydantic)
- ✅ Prueba el código (ejecutar tests)
- ✅ Si no estás seguro, pregunta a IA: "¿Este método realmente existe en Pydantic?"

---

**Ejercicio**: Detecta la hallucination

**IA generó esto**:

```python
import pytest

@pytest.fixture
def client():
    return TestClient(app)

def test_crear_tarea(client):
    response = client.post("/tareas", json={"nombre": "Test"})
    assert response.status_code == 201
    assert response.json().auto_validate()  # ← ¿Esto existe?
```

**Pregunta**: ¿`response.json().auto_validate()` es válido?

<details>
<summary>Respuesta</summary>

❌ NO. `response.json()` retorna un dict, que NO tiene método `.auto_validate()`.

**Correcto**:
```python
data = response.json()
assert "nombre" in data
assert data["nombre"] == "Test"
```

</details>

---

### 2.2 Contexto Limitado (No Sabe Tu Proyecto Completo) (20 min)

**Limitación**: IA solo ve el código que le muestras en el prompt.

**Problema**:

Tu proyecto tiene:
```python
# config.py
DATABASE_URL = "postgresql://..."

# models.py
class Usuario(BaseModel):
    email: EmailStr
```

**Prompt a IA**:
```
Crea una función que guarde un usuario en la base de datos
```

**IA genera** (sin contexto):
```python
def guardar_usuario(usuario):
    db = connect("sqlite:///db.sqlite")  # ❌ Usa SQLite, tú usas PostgreSQL
    # ...
```

**Problema**: IA no sabe que usas PostgreSQL ni que ya tienes `config.py`.

---

**Solución**: Proveer contexto completo

```
Crea una función que guarde un usuario en la base de datos.

CONTEXTO:
- Usamos PostgreSQL (DATABASE_URL en config.py)
- Modelo Usuario ya existe en models.py:

```python
class Usuario(BaseModel):
    email: EmailStr
    password_hash: str
```

- Usa SQLAlchemy para ORM

Función debe:
- Recibir objeto Usuario
- Guardar en tabla 'usuarios'
- Retornar usuario guardado con ID generado
```

**IA ahora genera** código consistente con tu proyecto.

---

**Ejercicio**: Añade contexto a este prompt

**Prompt malo**:
```
Crea tests para la función login
```

**Tu tarea**: Reescribe incluyendo:
- Qué tecnologías usas (pytest, FastAPI)
- Qué hace la función login (valida email/password, retorna JWT)
- Qué casos testear (credenciales válidas, inválidas, usuario no existe)

**Tiempo**: 10 min

---

### 2.3 No Puede "Probar" Código (Sin Ejecución) (20 min)

**Limitación**: IA no ejecuta el código que genera.

**Consecuencia**: Puede generar código sintácticamente correcto pero con bugs lógicos.

**Ejemplo**:

**IA genera**:
```python
def calcular_promedio(numeros):
    return sum(numeros) / len(numeros)
```

**Parece correcto**, pero:

```python
calcular_promedio([])  # ← ZeroDivisionError!
```

**IA no probó** con lista vacía.

---

**Otro ejemplo**:

**IA genera**:
```python
def es_adulto(edad):
    return edad >= 18
```

**Parece correcto**, pero:

```python
es_adulto(-5)  # ← Retorna False, pero edad negativa es inválida
es_adulto(None)  # ← TypeError!
```

**IA no anticipó** edge cases.

---

**Tu responsabilidad**:
1. Ejecutar el código generado
2. Probar con edge cases (vacío, None, negativos, muy grandes)
3. Añadir validación de inputs

**Código robusto**:
```python
def calcular_promedio(numeros: list[float]) -> float:
    if not numeros:
        raise ValueError("Lista vacía")
    return sum(numeros) / len(numeros)

def es_adulto(edad: int) -> bool:
    if edad < 0:
        raise ValueError("Edad no puede ser negativa")
    return edad >= 18
```

---

**Ejercicio**: Encuentra bugs en código de IA

**IA generó**:

```python
def obtener_usuario(id):
    usuarios = [{"id": 1, "nombre": "Ana"}, {"id": 2, "nombre": "Luis"}]
    return usuarios[id]
```

**Pregunta**: ¿Qué bugs tiene? ¿Qué inputs romperían este código?

<details>
<summary>Respuesta</summary>

Bugs:
1. `usuarios[id]` asume que `id` es índice (0, 1), no el ID real
2. Si `id >= len(usuarios)` → IndexError
3. Si `id < 0` → Retorna desde el final (comportamiento inesperado)
4. Si `id` no es int → TypeError

**Correcto**:
```python
def obtener_usuario(id: int) -> dict:
    usuarios = [{"id": 1, "nombre": "Ana"}, {"id": 2, "nombre": "Luis"}]
    for usuario in usuarios:
        if usuario["id"] == id:
            return usuario
    raise ValueError(f"Usuario {id} no encontrado")
```

</details>

---

### 2.4 Sesgo y Conocimiento Desactualizado (20 min)

**Limitación 1: Conocimiento hasta fecha de corte**

Ejemplo: Claude tiene conocimiento hasta enero 2025.

**Problema**: Si preguntas sobre features de Python 3.13+ o FastAPI 0.120+, puede no saberlo.

**Solución**:
- Especifica versiones en prompts
- Verifica con documentación oficial
- Usa IA para código genérico, documentación para features nuevas

---

**Limitación 2: Sesgo hacia patrones comunes**

**IA tiende a generar** código que vio más veces en training data.

**Ejemplo**: IA genera más frecuentemente Flask que FastAPI (porque Flask es más viejo, más código online).

**Solución**: Especifica explícitamente en prompt
```
Usa FastAPI 0.118 (NO Flask, NO Django)
```

---

**Limitación 3: Puede generar código obsoleto**

**IA puede generar**:
```python
# Pattern obsoleto (Python 3.8)
from typing import List

def procesar(items: List[str]):
    pass
```

**Debería generar** (Python 3.12):
```python
def procesar(items: list[str]):
    pass
```

**Solución**: Especifica versión de Python y pide patterns modernos.

---

### 2.5 Ejercicio: Limitaciones en Acción (10 min)

**Escenario**: Le pediste a IA que genere código para procesar pagos con Stripe.

**IA generó**:
```python
import stripe

stripe.api_key = "sk_test_123456"  # ← Problema 1

def procesar_pago(monto, cliente_email):
    charge = stripe.Charge.create(  # ← Problema 2
        amount=monto,
        currency="usd",
        source="tok_visa",
        description=f"Pago de {cliente_email}"
    )
    return charge
```

**Tu tarea**: Identifica 3+ problemas en este código.

<details>
<summary>Respuesta</summary>

Problemas:
1. **Secret hardcodeado**: `api_key` no debe estar en código, debe ser env var
2. **API obsoleta**: `stripe.Charge` está deprecated, ahora se usa PaymentIntent
3. **Sin manejo de errores**: ¿Qué pasa si falla la llamada?
4. **Token hardcodeado**: `tok_visa` es un token de prueba, no debería estar hardcodeado
5. **Sin validación**: No valida `monto > 0`, `cliente_email` válido

**Cómo detectarlo**:
- Leer documentación de Stripe (detectar API obsoleta)
- Revisar security best practices (detectar secret hardcodeado)
- Ejecutar código con edge cases (detectar falta de validación)

</details>

---

## 3. Cuándo NO Usar IA (1h)

### 3.1 Situaciones Críticas (20 min)

**NO uses IA (o úsala con EXTREMA validación) en**:

#### 1. Código que maneja dinero

**Ejemplo**: Transferencias bancarias, procesamiento de pagos

**Por qué**: Bug = pérdida de dinero real.

**Regla**: SIEMPRE revisa código financiero con:
- Tests exhaustivos (unit, integration, e2e)
- Revisión de código humana
- Auditoría de seguridad
- Validación de edge cases

---

#### 2. Código que afecta vidas

**Ejemplo**: Sistemas médicos, control de dispositivos (autos autónomos, drones)

**Por qué**: Bug = potencial pérdida de vidas.

**Regla**: Usa IA solo como asistente inicial, **NUNCA como implementación final sin validación exhaustiva**.

---

#### 3. Código de seguridad crítico

**Ejemplo**: Auth, crypto, manejo de secretos

**Por qué**: Bug = vulnerabilidad explotable.

**Regla**:
- Usa IA para generar estructura
- Revisa con Security Hardening Mentor
- Valida con herramientas (Bandit, Safety)
- Nunca confíes ciegamente en código crypto generado por IA

**Ejemplo de código peligroso que IA podría generar**:

```python
# IA podría generar esto (INSEGURO)
import hashlib

def hashear_password(password):
    return hashlib.md5(password.encode()).hexdigest()  # ❌ MD5 es inseguro
```

**Correcto** (validado por humano):
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashear_password(password: str) -> str:
    return pwd_context.hash(password)  # ✅ bcrypt es seguro
```

---

#### 4. Decisiones de arquitectura

**Ejemplo**: ¿Microservicios o monolito? ¿PostgreSQL o MongoDB?

**Por qué**: IA no conoce tu contexto completo (equipo, budget, escala, requisitos).

**Regla**: Usa IA para explorar opciones, TÚ decides.

**Prompt correcto**:
```
Compara microservicios vs monolito para [tu contexto].

Contexto:
- Equipo: 3 devs
- Escala: 1000 usuarios
- Budget: Limitado
- Experiencia: Intermedia

Dame pros/contras de cada opción EN MI CONTEXTO ESPECÍFICO.

NO decidas por mí, solo provee información.
```

---

### 3.2 Cuando Estás Aprendiendo (20 min)

**Regla**: Si estás **aprendiendo** un concepto, implementa manualmente primero, IA después.

**Pattern de aprendizaje**:

```
1. Aprende el concepto (manual)
   → Lee documentación, tutoriales
   → Implementa tú mismo

2. Compara con IA
   → Pide a IA que genere implementación
   → Compara con tu solución
   → Identifica diferencias

3. Itera
   → Pregunta POR QUÉ IA hizo X diferente
   → Aprende de las diferencias
```

---

**Ejemplo**:

**Estás aprendiendo decorators en Python**

**MAL approach**:
```bash
claude "Explica decorators y genera un ejemplo"
```
→ Lees, copias, no entiendes profundamente

**BUEN approach**:
```
1. Lee documentación de decorators
2. Implementa tu propio decorador (ej: @timer que mide tiempo de ejecución)
3. Pide a IA: "Revisa mi implementación de decorador @timer. ¿Qué puedo mejorar?"
4. Compara tu código con sugerencias de IA
5. Aprende de las diferencias
```

---

**Ejercicio**: Identifica si usar IA o no

Para cada escenario, decide: ¿Usar IA? ¿Con qué validación?

1. **Escenario**: Generar tests para función simple `sumar(a, b)`
2. **Escenario**: Implementar algoritmo de machine learning para predicción de fraude bancario
3. **Escenario**: Renombrar variable `x` a `usuario_actual` en toda la codebase
4. **Escenario**: Decidir entre Redis vs Memcached para caché
5. **Escenario**: Implementar JWT authentication

<details>
<summary>Respuestas</summary>

1. **Tests para suma**: ✅ Usa IA (bajo riesgo, fácil validar)
2. **ML para fraude**: ❌ NO confíes ciegamente (crítico, afecta dinero, requiere expertise en ML)
3. **Renombrar variable**: ✅ Usa IA o IDE (bajo riesgo, automático)
4. **Redis vs Memcached**: ⚠️ Usa IA para comparar, TÚ decides (depende de contexto)
5. **JWT auth**: ⚠️ Usa IA para estructura, VALIDA EXHAUSTIVAMENTE con Security Mentor (código de seguridad)

</details>

---

### 3.3 Cuando el Problema es Ambiguo (20 min)

**Regla**: Si NO sabes QUÉ quieres, IA no puede ayudarte.

**Ejemplo de ambigüedad**:

**Prompt ambiguo**:
```
Crea una API para mi startup
```

**IA necesita saber**:
- ¿Qué hace tu startup?
- ¿Qué endpoints necesitas?
- ¿Qué datos manejas?
- ¿Qué tecnologías conoces?

**Resultado**: IA genera algo genérico e inútil.

---

**Proceso correcto**:

```
1. DEFINE el problema (tú, sin IA)
   - ¿Qué necesitas construir?
   - ¿Qué requisitos tienes?
   - ¿Qué restricciones existen?

2. ESPECIFICA los detalles (tú, sin IA)
   - Endpoints necesarios
   - Modelos de datos
   - Flujos de usuario

3. USA IA para implementación
   - Con requisitos claros
   - Con restricciones definidas
```

---

**Ejercicio**: Clarifica este problema ambiguo

**Problema ambiguo**:
```
Necesito una base de datos para mi app
```

**Tu tarea**: Convierte esto en un problema específico que IA pueda ayudar a resolver.

**Preguntas a responder**:
- ¿Qué tipo de datos?
- ¿Qué operaciones (leer, escribir, actualizar)?
- ¿Relaciones entre datos?
- ¿Escala esperada?
- ¿Tecnologías permitidas?

**Tiempo**: 10 min

---

## 4. Responsabilidad del Desarrollador (1h)

### 4.1 El Código es Tu Responsabilidad (15 min)

**Principio**: Si commiteas código generado por IA, es TU código.

**Implicaciones**:

1. **Debugging**: Si hay bug, TÚ lo debuggeas (no puedes decir "IA lo generó mal")
2. **Mantenimiento**: Si hay que cambiar el código en 6 meses, TÚ lo mantienes
3. **Explicación**: Si alguien pregunta "¿por qué hiciste esto?", TÚ explicas
4. **Consecuencias**: Si el código causa problemas en producción, TÚ respondes

---

**Checklist antes de commit**:

- [ ] ¿Entiendo CADA LÍNEA del código generado?
- [ ] ¿Probé el código con tests?
- [ ] ¿Revisé edge cases?
- [ ] ¿El código sigue los estándares del proyecto?
- [ ] ¿Puedo explicar POR QUÉ este código es correcto?
- [ ] ¿Documenté decisiones no obvias?

**Si respondiste NO a alguno** → NO hagas commit todavía.

---

### 4.2 Validación de Código Generado (20 min)

**Process de validación**:

```
1. LEER el código línea por línea
   - ¿Qué hace cada línea?
   - ¿Por qué está ahí?

2. EJECUTAR con tests
   - Happy path
   - Edge cases
   - Error cases

3. REVISAR con herramientas
   - Linter (ruff, pylint)
   - Type checker (mypy)
   - Security scanner (bandit)

4. COMPARAR con estándares
   - ¿Sigue SOLID?
   - ¿Sigue patrones del proyecto?
   - ¿Es mantenible?

5. DOCUMENTAR si necesario
   - ¿Por qué este approach?
   - ¿Qué alternativas consideraste?
```

---

**Ejemplo de validación**:

**IA generó**:
```python
def procesar_datos(datos):
    resultado = []
    for item in datos:
        if item > 0:
            resultado.append(item * 2)
    return resultado
```

**Validación paso a paso**:

```
1. LEER:
   - Filtra items > 0
   - Multiplica por 2
   - Retorna lista

2. EJECUTAR:
   - procesar_datos([1, -1, 2]) → [2, 4] ✅
   - procesar_datos([]) → [] ✅
   - procesar_datos([0]) → [] ✅
   - procesar_datos(None) → TypeError ❌

3. REVISAR con type hints:
   ```python
   def procesar_datos(datos: list[int]) -> list[int]:
       # Ahora mypy detectará si pasas None
   ```

4. COMPARAR:
   - Podría ser list comprehension (más Pythonic)
   ```python
   def procesar_datos(datos: list[int]) -> list[int]:
       return [item * 2 for item in datos if item > 0]
   ```

5. DOCUMENTAR:
   ```python
   def procesar_datos(datos: list[int]) -> list[int]:
       """Filtra números positivos y los duplica.

       Args:
           datos: Lista de enteros

       Returns:
           Lista con números positivos duplicados

       Examples:
           >>> procesar_datos([1, -1, 2])
           [2, 4]
       """
       return [item * 2 for item in datos if item > 0]
   ```
```

---

### 4.3 Atribución y Transparencia (15 min)

**Pregunta ética**: ¿Debes decir que IA generó el código?

**Contextos**:

#### 1. En el trabajo (equipo/empresa)

**Recomendación**: Sé transparente si:
- El código es complejo o crítico
- Alguien pregunta
- Es política de la empresa

**En commits**: NO necesitas poner "Generado con IA" en cada commit, pero SÍ asumes responsabilidad.

**Ejemplo**:
```bash
# No necesario:
git commit -m "feat: add login endpoint (generado con Claude)"

# Suficiente:
git commit -m "feat: add login endpoint"

# Pero en code review, si te preguntan:
"Usé IA para generar la estructura inicial, luego validé y ajusté la lógica de auth"
```

---

#### 2. En proyectos académicos

**Recomendación**: Sigue las reglas de tu institución.

**Muchas instituciones permiten** IA como herramienta, similar a Google o Stack Overflow, PERO:
- ✅ Debes entender el código
- ✅ Debes poder explicarlo
- ✅ Debes citar si se pide

**Ejemplo de atribución en proyecto académico**:
```markdown
## Herramientas Utilizadas

- Python 3.12
- FastAPI 0.118
- Claude AI (asistente para generación de tests y refactoring)

Todo el código fue revisado, validado y adaptado por mí.
```

---

#### 3. En proyectos open source

**Recomendación**: Transparencia total si contribuyes a proyecto ajeno.

**Buenas prácticas**:
- Si IA generó parte significativa, menciónalo en PR description
- Asegúrate de que el código sigue guidelines del proyecto
- Responde a code reviews (no puedes decir "pregúntale a IA")

---

### 4.4 Ejercicio: Análisis de Responsabilidad (10 min)

**Escenario**:

Generaste código con IA para procesar pagos. Hiciste commit. Una semana después, un cliente reporta que su pago se procesó 2 veces.

**Preguntas**:
1. ¿De quién es la responsabilidad del bug?
2. ¿Qué deberías haber hecho antes del commit?
3. ¿Cómo manejas la situación ahora?

<details>
<summary>Respuesta</summary>

1. **Responsabilidad**: 100% tuya. Commiteaste el código, asumiste responsabilidad.

2. **Antes de commit**:
   - Tests exhaustivos (casos de duplicación)
   - Revisar si hay transacciones atómicas
   - Validar idempotencia (mismo request no procesar 2 veces)
   - Code review

3. **Ahora**:
   - Investigar root cause (sin culpar a IA)
   - Fix el bug
   - Añadir tests que detecten esta situación
   - Documentar en ADR o postmortem
   - Aprender para próxima vez

**Lección**: IA genera, TÚ validas. Sin validación exhaustiva, NO commitear código crítico.

</details>

---

## 5. Ética en Desarrollo con IA (1h)

### 5.1 Privacidad de Datos (20 min)

**Regla de oro**: NUNCA compartas datos sensibles con IA.

**Datos sensibles incluyen**:
- ❌ Secrets (API keys, passwords, tokens)
- ❌ Información personal identificable (PII): nombres, emails, teléfonos de usuarios reales
- ❌ Datos financieros (tarjetas de crédito, cuentas bancarias)
- ❌ Datos de salud (historiales médicos)
- ❌ Código propietario de clientes/empresas (sin permiso)

---

**Ejemplo de violación de privacidad**:

**MAL** (compartir datos reales):
```bash
claude "Revisa esta query SQL:

SELECT * FROM usuarios WHERE email = 'juan.perez@empresa.com'
AND password = 'secreto123'
```

**Problema**: Compartiste email real y password real con IA.

---

**BIEN** (anonimizar datos):
```bash
claude "Revisa esta query SQL:

SELECT * FROM usuarios WHERE email = '[EMAIL_EJEMPLO]'
AND password = '[PASSWORD_EJEMPLO]'
```

**O mejor aún** (sin datos):
```bash
claude "Revisa esta query SQL:

SELECT * FROM usuarios WHERE email = ? AND password = ?

Uso parámetros para evitar SQL injection. ¿Es correcto?
```

---

**Checklist antes de pegar código en IA**:

- [ ] ¿Contiene API keys? → Reemplazar con `[API_KEY]`
- [ ] ¿Contiene emails reales? → Reemplazar con `[EMAIL]` o `user@example.com`
- [ ] ¿Contiene nombres de usuarios reales? → Usar `Usuario 1`, `Usuario 2`
- [ ] ¿Contiene datos financieros? → Eliminar o reemplazar con dummy data
- [ ] ¿Es código propietario? → Verificar que tienes permiso para compartir

---

### 5.2 Bias y Discriminación (15 min)

**Problema**: IA puede generar código con sesgos implícitos.

**Ejemplo 1: Sesgos de género**

**IA podría generar**:
```python
def generar_saludo(usuario):
    if usuario.profesion == "enfermera":
        pronombre = "ella"
    elif usuario.profesion == "ingeniero":
        pronombre = "él"
    # ...
```

**Problema**: Asume género basado en profesión (sesgo).

**Correcto**:
```python
def generar_saludo(usuario):
    pronombre = usuario.pronombre_preferido  # Usuario especifica su pronombre
    # O simplemente:
    return f"Hola, {usuario.nombre}"  # Sin asumir género
```

---

**Ejemplo 2: Sesgos geográficos**

**IA podría generar**:
```python
def validar_telefono(numero):
    if not numero.startswith("+1"):  # Asume USA
        raise ValueError("Número inválido")
```

**Problema**: Solo acepta números de USA.

**Correcto**:
```python
def validar_telefono(numero):
    # Validar formato internacional
    if not numero.startswith("+"):
        raise ValueError("Número debe incluir código de país (+XX)")
    # Validar con librería especializada
    import phonenumbers
    # ...
```

---

**Tu responsabilidad**:
1. Revisar código generado en busca de assumptions
2. Cuestionar: ¿Este código funciona para TODOS los usuarios?
3. Testear con diversidad (diferentes países, géneros, idiomas)

---

### 5.3 Impacto Ambiental (10 min)

**Realidad**: Entrenar y usar modelos de IA consume mucha energía.

**Implicaciones**:
- Cada request a IA consume recursos
- Generar código innecesariamente tiene impacto ambiental

**Buenas prácticas**:

1. **NO uses IA para cosas triviales que ya sabes hacer**
   ```
   ❌ claude "Cómo sumar dos números en Python"
   ✅ Solo escribir: a + b
   ```

2. **Optimiza prompts** (evita regenerar múltiples veces)
   ```
   ❌ 10 prompts vagos que generan mal código
   ✅ 1 prompt específico que genera código correcto
   ```

3. **Usa caché de conversaciones** (no preguntes lo mismo 2 veces)

4. **Pregunta solo cuando NO sabes** (no por pereza)

---

### 5.4 Derechos de Autor y Licencias (15 min)

**Pregunta**: ¿De quién es el código generado por IA?

**Respuesta legal** (simplificada, consulta abogado para casos reales):
- **Tu prompt**: Es tuyo
- **Código generado**: Generalmente tuyo (si es original)
- **Pero**: IA podría generar código similar a código existente (copyleft issues)

**Problema potencial**: IA entrenada con código open source podría generar código similar.

---

**Ejemplo**:

**IA genera código muy similar a librería GPL**:
```python
# Muy similar a código GPL de [proyecto X]
def algoritmo_especial():
    # ...
```

**Problema**: Si copias código GPL sin seguir la licencia GPL, violación de copyright.

**Solución**:
1. Si IA genera código sospechosamente específico, verifica si existe en proyectos conocidos
2. Si usas código de IA en proyectos comerciales, revisa con abogado
3. Documenta que código fue generado (para traceability)

---

**Buenas prácticas**:

- ✅ Usa IA para generar código nuevo, no para "copiar" código existente
- ✅ Si usas IA para entender código open source, respeta su licencia
- ✅ Si generas código para vender/comercializar, consulta abogado
- ❌ NO asumas que "IA lo generó" es defensa legal

---

## 6. Proyecto Final - Código de Conducta IA (45 min)

### 6.1 Objetivo del Proyecto

Crear tu **Código de Conducta Personal para Usar IA en Desarrollo**.

**Analogía**: Código de ética profesional (como médicos, abogados tienen).

**Propósito**: Definir TUS reglas para usar IA de forma responsable y ética.

---

### 6.2 Estructura del Código de Conducta

**Archivo**: `mi-codigo-conducta-ia.md`

**Secciones requeridas**:

```markdown
# Mi Código de Conducta para Desarrollo con IA

## 1. Principios Fundamentales

[Tus principios core - ej: "IA asiste, yo decido", "Siempre entender antes de commitear"]

## 2. Cuándo Usar IA

**Situaciones donde SÍ usaré IA**:
- [Lista de situaciones]

**Situaciones donde NO usaré IA (o solo con validación exhaustiva)**:
- [Lista de situaciones]

## 3. Proceso de Validación

**Antes de commitear código generado por IA, SIEMPRE**:
- [ ] [Checklist item 1]
- [ ] [Checklist item 2]
- [ ] ...

## 4. Privacidad y Seguridad

**NUNCA compartiré con IA**:
- [Lista de datos sensibles]

**Anonimizaré**:
- [Qué datos y cómo]

## 5. Responsabilidad

**Asumo responsabilidad por**:
- [Qué aspectos del código generado]

**Si hay un bug en código generado por IA**:
- [Cómo manejaré la situación]

## 6. Transparencia

**Seré transparente sobre uso de IA cuando**:
- [Contextos donde revelarás uso de IA]

## 7. Aprendizaje Continuo

**Para evitar dependencia excesiva de IA**:
- [Estrategias de aprendizaje manual]
- [Cuándo implementar sin IA primero]

## 8. Revisión Ética

**Revisaré código de IA en busca de**:
- Sesgos (género, raza, geografía)
- Assumptions problemáticas
- [Otros aspectos éticos]

## 9. Compromiso

Me comprometo a seguir este código de conducta en mi desarrollo con IA.
Si violo algún principio, [qué haré para corregir].

---

**Fecha**: [Fecha de creación]
**Firma**: [Tu nombre]
```

---

### 6.3 Requisitos Mínimos

Tu código de conducta debe incluir:

- [ ] Mínimo 3 principios fundamentales
- [ ] 5+ situaciones donde SÍ usar IA
- [ ] 5+ situaciones donde NO usar IA (o validar exhaustivamente)
- [ ] Checklist de validación con 7+ items
- [ ] Lista de datos sensibles que NUNCA compartirás
- [ ] Compromiso de responsabilidad (qué harás si hay bug)
- [ ] Plan de transparencia (cuándo revelar uso de IA)
- [ ] Estrategia anti-dependencia (cómo seguir aprendiendo manualmente)

---

### 6.4 Ejemplo de Sección

```markdown
## 2. Cuándo Usar IA

**SÍ usaré IA para**:
- Generar boilerplate code (modelos Pydantic, endpoints básicos)
- Refactoring simple (renombrar, extract method)
- Generar tests iniciales (luego los reviso y extiendo)
- Documentación (docstrings, READMEs)
- Explicar conceptos nuevos (como tutor)

**NO usaré IA (o solo con validación exhaustiva) para**:
- Código de seguridad (auth, crypto, manejo de secretos)
- Código que maneja dinero (pagos, transferencias)
- Decisiones de arquitectura (microservicios vs monolito)
- Implementación final de features críticas sin revisión
- Código en proyectos de clientes sin permiso explícito

**Zona gris** (usar IA + validación extra rigurosa):
- Lógica de negocio específica de dominio
- Integración de sistemas complejos
- Performance optimization
```

---

### 6.5 Criterios de Evaluación

| Criterio | Peso | Descripción |
|----------|------|-------------|
| **Completitud** | 25% | Todas las secciones presentes, requisitos mínimos cumplidos |
| **Especificidad** | 25% | Principios y reglas específicas, no genéricas |
| **Realismo** | 20% | Código de conducta que REALMENTE seguirías |
| **Reflexión** | 20% | Demuestra comprensión de limitaciones y ética |
| **Compromiso** | 10% | Incluye compromiso real y consecuencias |

**Total**: 100 puntos (50% de la nota final de Clase 6)

---

## 7. Evaluación y Cierre del Módulo 0

### 7.1 Entregables de Clase 6

1. **Ejercicios de detección de limitaciones** - 20%
2. **Análisis de responsabilidad** (Ejercicio 4.4) - 30%
3. **Código de Conducta IA** (Proyecto Final) - 50%

**Mínimo para aprobar Clase 6**: 70/100

---

### 7.2 Evaluación Final del Módulo 0

**Módulo 0 completo** incluye:
- Clase 1: Fundamentos de IA en Desarrollo
- Clase 2: Git y Cursor con IA
- Clase 3: Documentación y Pensamiento Estructurado
- Clase 4: Tu Primer Agente Custom
- Clase 5: Prompt Engineering Avanzado
- Clase 6: Limitaciones y Ética

**Proyecto Final de Módulo 0** (siguiente entregable):
- Portfolio completo de lo aprendido
- Demuestra dominio de IA como herramienta

---

### 7.3 Autoevaluación Módulo 0

- [ ] ¿Entiendo qué es IA y qué NO es?
- [ ] ¿Puedo usar Claude Code CLI efectivamente?
- [ ] ¿Sé escribir prompts avanzados?
- [ ] ¿Puedo crear agentes educativos especializados?
- [ ] ¿Entiendo las limitaciones de IA?
- [ ] ¿Sé cuándo NO usar IA?
- [ ] ¿Asumo responsabilidad del código generado?
- [ ] ¿Tengo un código de conducta ético para IA?

**Si respondiste SÍ a 7/8+** → Listo para Módulo 1 ✅

**Si respondiste NO a 3+** → Repasa las clases correspondientes

---

### 7.4 Recursos Adicionales

**Ética en IA**:
- "Weapons of Math Destruction" - Cathy O'Neil
- "AI Ethics" - Mark Coeckelbergh
- Guidelines on AI Ethics (UNESCO)

**Limitaciones de LLMs**:
- "On the Dangers of Stochastic Parrots" (Paper)
- OpenAI GPT-4 Technical Report (limitations section)
- Anthropic Claude 2 Model Card

**Responsabilidad en Desarrollo**:
- "The Pragmatic Programmer" - Andy Hunt, Dave Thomas
- "Clean Code" - Robert C. Martin (responsabilidad y profesionalismo)

---

## Resumen de la Clase

En esta clase aprendiste:

1. **Limitaciones de IA**: Hallucinations, contexto limitado, no ejecuta código, conocimiento desactualizado
2. **Cuándo NO usar IA**: Situaciones críticas, cuando aprendes, problemas ambiguos
3. **Responsabilidad**: Código committeado es TU código, validación exhaustiva requerida
4. **Ética**: Privacidad, sesgos, impacto ambiental, derechos de autor
5. **Código de Conducta**: Framework personal para usar IA responsablemente

**Skill clave**: Discernimiento - saber CUÁNDO y CÓMO usar IA, no solo usarla ciegamente.

**Mensaje final**: IA es una herramienta poderosa, pero TÚ eres el desarrollador responsable.

---

## Cierre del Módulo 0

**Has completado Módulo 0: IA Development Foundations** 🎉

**Aprendiste**:
- Fundamentos de IA en desarrollo
- Herramientas (Claude Code, Cursor, Git)
- Documentación profesional
- Crear agentes educativos
- Prompt engineering avanzado
- Limitaciones y ética

**Estás listo para**:
- Módulo 1: Fundamentos + IA Assistant (CLI apps, Python, testing)
- Usar IA como copiloto en proyectos reales
- Desarrollar con conciencia y responsabilidad

**Próximo paso**: Proyecto Final de Módulo 0 (integra todo lo aprendido).

---

**Regla de oro final**:

> "Con gran poder viene gran responsabilidad. IA te da superpoderes de desarrollo - úsalos sabiamente."

**Recuerda**: IA asiste, TÚ decides. IA genera, TÚ validas. IA propone, TÚ eres responsable.

¡Usa IA con cabeza! 🧠🤖
