# Clase 5 - Prompt Engineering Avanzado

**Duración**: 6 horas
**Objetivo**: Dominar técnicas avanzadas de prompt engineering para obtener código de mayor calidad, dividir tareas complejas, y orquestar múltiples agentes trabajando juntos.

---

## Índice

1. [Conceptos Clave](#1-conceptos-clave-45-min)
2. [Anatomía de un Prompt Efectivo](#2-anatomía-de-un-prompt-efectivo-1h)
3. [Técnicas Avanzadas](#3-técnicas-avanzadas-15h)
4. [Orquestación de Agentes](#4-orquestación-de-agentes-1h)
5. [Debugging de Prompts](#5-debugging-de-prompts-45-min)
6. [Proyecto Final - Prompt Library](#6-proyecto-final---prompt-library-1h)
7. [Evaluación y Entregables](#7-evaluación-y-entregables)

---

## 1. Conceptos Clave (45 min)

### 1.1 ¿Por Qué Prompt Engineering? (15 min)

**Realidad**: Misma IA, prompts diferentes = resultados completamente diferentes.

**Experimento**:

**Prompt malo**:
```
Crea una API
```

**Output de IA**:
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello"

if __name__ == '__main__':
    app.run()
```

**Problema**: ¿Es esto lo que querías? Tal vez querías FastAPI, validación con Pydantic, tests incluidos.

---

**Prompt bueno**:
```
Crea una API REST con FastAPI para gestionar tareas.

Requisitos:
- Endpoint POST /tareas (crear tarea con nombre y prioridad)
- Validación: nombre no vacío, prioridad en [alta, media, baja]
- Usar Pydantic para request/response models
- Incluir docstrings en endpoints
- Incluir tests con pytest usando TestClient

Arquitectura:
- Separación en capas (API → Servicio → Repositorio)
- Repositorio en memoria por ahora

Output esperado:
- api.py con endpoints
- servicio_tareas.py con lógica
- repositorio_memoria.py con almacenamiento
- test_api.py con tests

Python 3.12, FastAPI 0.118
```

**Output de IA**: Código completo, estructurado, con tests, siguiendo los requisitos exactos.

**Diferencia**: Especificidad.

---

### 1.2 Principios de Prompt Engineering (15 min)

**Principio 1: Especificidad > Generalidad**

❌ "Mejora este código"
✅ "Refactoriza esta función para que siga Single Responsibility Principle. Extrae la validación a una función separada llamada validar_entrada()"

---

**Principio 2: Contexto es Rey**

❌ "¿Cómo testeo esto?"
✅ "Tengo una función crear_usuario(email, password) que hashea passwords con bcrypt y guarda en DB. ¿Cómo testearla usando pytest y mocks para la DB?"

---

**Principio 3: Formato de Output Claro**

❌ "Explica SOLID"
✅ "Explica los 5 principios SOLID usando esta estructura para cada uno:
- Nombre
- Definición en 1 línea
- Ejemplo de violación en Python
- Ejemplo correcto en Python
- Por qué importa"

---

**Principio 4: Restricciones Explícitas**

❌ "Crea tests"
✅ "Crea tests usando pytest. RESTRICCIONES:
- NO uses fixtures complejos
- NO uses parametrize (aún no lo sé usar)
- SÍ usa TestClient de FastAPI
- SÍ incluye tests de happy path y error cases"

---

### 1.3 Niveles de Prompt Engineering (15 min)

**Nivel 1: Básico** (Clase 1)
```
Rol + Objetivo + Restricciones

Ejemplo:
"Eres un experto en Python. Crea una función que sume dos números. NO uses librerías externas."
```

**Nivel 2: Intermedio** (Clase 1-2)
```
Rol + Contexto + Objetivo + Restricciones + Formato de Output

Ejemplo:
"Eres un experto en Python. Estoy aprendiendo testing. Crea tests para una función saludar(nombre) que retorna 'Hola, {nombre}'. Usa pytest. Incluye test de happy path y edge case (nombre vacío). Formato: un archivo test_saludar.py completo."
```

**Nivel 3: Avanzado** (Esta clase)
```
Rol + Contexto + Objetivo + Restricciones + Formato de Output + Ejemplos + Chain of Thought + Validación

Ejemplo:
[Ver sección 2]
```

---

## 2. Anatomía de un Prompt Efectivo (1h)

### 2.1 Estructura Completa (20 min)

**Template de prompt avanzado**:

```
[1. ROL Y EXPERTISE]
Eres un [especialista en X] con [N años de experiencia en Y].

[2. CONTEXTO]
Estoy trabajando en [descripción del proyecto].
Tecnologías: [lista]
Nivel de experiencia: [principiante/intermedio/avanzado]

[3. SITUACIÓN ACTUAL]
Tengo [problema/código/situación].
[Pegar código si aplica]

[4. OBJETIVO]
Necesito [qué quieres lograr].

[5. RESTRICCIONES]
DEBES:
- [Restricción obligatoria 1]
- [Restricción obligatoria 2]

NO DEBES:
- [Restricción de prohibición 1]
- [Restricción de prohibición 2]

[6. FORMATO DE OUTPUT]
Proporciona la respuesta en este formato:
1. [Sección 1]
2. [Sección 2]
3. [Código completo]

[7. EJEMPLOS] (opcional)
Ejemplo de output esperado:
[Ejemplo]

[8. VALIDACIÓN] (opcional)
Asegúrate de que:
- [Criterio de validación 1]
- [Criterio de validación 2]
```

---

### 2.2 Ejemplo Completo de Prompt Avanzado (20 min)

**Situación**: Necesitas crear una función de retry logic para llamadas a API externa.

**Prompt avanzado**:

```
[ROL]
Eres un experto en Python y reliability engineering, especializado en manejo de errores y retry patterns.

[CONTEXTO]
Estoy construyendo una aplicación FastAPI que consume una API externa (Yurest API).
La API a veces falla con timeouts o errores 503 (servicio no disponible).
Tecnologías: Python 3.12, FastAPI 0.118, httpx para HTTP requests
Nivel: Intermedio (sé excepciones básicas, no conozco retry libraries)

[SITUACIÓN ACTUAL]
Tengo este código que llama a la API:

```python
import httpx

def obtener_productos():
    response = httpx.get("https://yurest-api.com/productos")
    response.raise_for_status()
    return response.json()
```

Problema: Si la API falla, mi aplicación crashea. Quiero retry automático.

[OBJETIVO]
Implementar retry logic con exponential backoff para manejar fallos transitorios.

[RESTRICCIONES]
DEBES:
- Usar decorador para que sea reutilizable
- Máximo 3 reintentos
- Exponential backoff (1s, 2s, 4s)
- Loggear cada reintento
- Solo reintentar en errores transitorios (timeout, 503, 502)

NO DEBES:
- NO usar librerías externas (como tenacity o backoff)
- NO reintentar en errores 4xx (esos son errores de cliente)
- NO bloquear indefinidamente

[FORMATO DE OUTPUT]
1. Explicación breve del patrón (2-3 líneas)
2. Código del decorador completo con docstrings
3. Ejemplo de uso con mi función obtener_productos()
4. Explicación de por qué exponential backoff es mejor que intervalo fijo

[EJEMPLOS]
Output esperado debe ser similar a:

```python
@retry(max_attempts=3)
def obtener_productos():
    # ...
```

[VALIDACIÓN]
Asegúrate de que:
- El código funciona sin dependencias externas
- Incluye type hints
- Los logs muestren qué intento es (1/3, 2/3, 3/3)
- Después de 3 intentos, raise la excepción original
```

---

**Output esperado de IA**:

```markdown
## Retry Pattern con Exponential Backoff

Este patrón reintenta operaciones fallidas con delays crecientes (1s, 2s, 4s), dando tiempo al servicio externo para recuperarse.

### Decorador de Retry

```python
import time
import logging
from functools import wraps
from typing import Callable, Any

logger = logging.getLogger(__name__)

def retry(max_attempts: int = 3, base_delay: float = 1.0):
    """
    Decorador que reintenta una función en caso de errores transitorios.

    Args:
        max_attempts: Número máximo de intentos (default: 3)
        base_delay: Delay inicial en segundos (se duplica en cada intento)

    Raises:
        La excepción original después de max_attempts intentos
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except (httpx.TimeoutException, httpx.HTTPStatusError) as e:
                    # Solo reintentar en errores transitorios
                    if isinstance(e, httpx.HTTPStatusError):
                        if e.response.status_code not in [502, 503]:
                            # Error de cliente (4xx) o permanente
                            raise

                    if attempt == max_attempts:
                        logger.error(f"{func.__name__} falló después de {max_attempts} intentos")
                        raise

                    delay = base_delay * (2 ** (attempt - 1))
                    logger.warning(
                        f"{func.__name__} falló (intento {attempt}/{max_attempts}). "
                        f"Reintentando en {delay}s... Error: {e}"
                    )
                    time.sleep(delay)

            return None  # No debería llegar aquí
        return wrapper
    return decorator
```

### Uso

```python
import httpx

@retry(max_attempts=3, base_delay=1.0)
def obtener_productos():
    """Obtiene productos desde Yurest API con retry automático."""
    response = httpx.get("https://yurest-api.com/productos", timeout=5.0)
    response.raise_for_status()
    return response.json()

# Si falla:
# Intento 1: Falla, espera 1s
# Intento 2: Falla, espera 2s
# Intento 3: Falla, espera 4s
# Intento 4: Raise exception
```

### Por Qué Exponential Backoff

**Intervalo fijo** (1s, 1s, 1s):
- ❌ Si el servicio está caído, bombardeas con requests inútiles
- ❌ No da tiempo al servicio a recuperarse

**Exponential backoff** (1s, 2s, 4s):
- ✅ Da tiempo creciente para que el servicio se recupere
- ✅ Reduce carga en el servidor
- ✅ Pattern estándar en sistemas distribuidos (usado por AWS, Google Cloud)
```

---

### 2.3 Ejercicio: Mejora Este Prompt (20 min)

**Prompt malo**:
```
Crea un script que lea un CSV y lo guarde en JSON
```

**Tu tarea**: Reescribe usando la estructura de prompt avanzado.

**Pistas**:
- Rol: ¿Especialista en qué?
- Contexto: ¿Qué tipo de CSV? ¿Qué columnas? ¿Qué hacer con errores?
- Objetivo: ¿Solo convertir? ¿Validar datos?
- Restricciones: ¿Librerías permitidas? ¿Encoding del CSV?
- Formato de output: ¿Solo código? ¿Con tests?

**Tiempo**: 15 min reescribir + 5 min comparar con ejemplo

<details>
<summary>Ejemplo de mejora</summary>

```
[ROL]
Eres un experto en Python y procesamiento de datos, especializado en ETL (Extract, Transform, Load).

[CONTEXTO]
Estoy construyendo un pipeline de datos que procesa archivos CSV de ventas.
CSV tiene columnas: fecha, producto, cantidad, precio
Tecnologías: Python 3.12, pandas (permitido), pytest
Nivel: Intermedio

[SITUACIÓN ACTUAL]
Tengo archivos CSV como este:

```csv
fecha,producto,cantidad,precio
2025-01-15,Pan,10,2.5
2025-01-16,Leche,5,3.0
```

Necesito convertirlos a JSON para enviar a una API.

[OBJETIVO]
Crear un script que lea CSV, valide datos, y genere JSON.

[RESTRICCIONES]
DEBES:
- Validar que las columnas existan
- Convertir fecha a formato ISO (YYYY-MM-DD)
- Validar que cantidad y precio sean números > 0
- Manejar errores (CSV mal formado, datos inválidos)

NO DEBES:
- NO crashear si hay una fila con error (skipearla y loggear)
- NO modificar el CSV original

[FORMATO DE OUTPUT]
1. Función procesar_csv(ruta_csv: str) -> list[dict]
2. Función guardar_json(datos: list[dict], ruta_json: str) -> None
3. Script main que usa ambas
4. Tests con pytest

[VALIDACIÓN]
- El código debe funcionar con pandas
- Incluir docstrings
- JSON resultante debe ser válido
```

</details>

---

## 3. Técnicas Avanzadas (1.5h)

### 3.1 Chain of Thought (Cadena de Razonamiento) (20 min)

**Concepto**: Pedir a IA que "piense en voz alta" antes de dar respuesta.

**Sin Chain of Thought**:
```
¿Este código tiene bugs?

```python
def dividir(a, b):
    return a / b
```
```

**IA responde**: "Sí, falla si b es 0"

---

**Con Chain of Thought**:
```
Analiza este código en busca de bugs. Razona paso a paso:

1. ¿Qué hace la función?
2. ¿Qué inputs espera?
3. ¿Qué edge cases existen?
4. ¿Qué pasa en cada edge case?
5. ¿Cómo arreglarlo?

```python
def dividir(a, b):
    return a / b
```
```

**IA responde**:
```
1. ¿Qué hace? Divide 'a' entre 'b'
2. ¿Qué inputs? Números (int o float)
3. Edge cases:
   - b = 0 (división por cero)
   - a = 0 (válido, retorna 0)
   - Inputs negativos (válido, retorna negativo)
4. ¿Qué pasa?
   - b = 0 → ZeroDivisionError (crash)
5. Fix: Validar b != 0

```python
def dividir(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return a / b
```
```

**Beneficio**: Análisis más profundo, no solo respuesta superficial.

---

**Ejercicio**:

Usa Chain of Thought para este código:

```python
def obtener_usuario(id):
    usuarios = [{"id": 1, "nombre": "Ana"}, {"id": 2, "nombre": "Luis"}]
    return usuarios[id]
```

**Prompt**:
```
Analiza este código paso a paso:
1. ¿Qué hace?
2. ¿Qué edge cases existen?
3. ¿Qué bugs tiene?
4. ¿Cómo arreglarlo?

[Código aquí]
```

**Tiempo**: 10 min

---

### 3.2 Few-Shot Learning (Ejemplos Incluidos) (25 min)

**Concepto**: Proveer ejemplos de input/output esperado.

**Sin ejemplos** (Zero-shot):
```
Genera docstrings para esta función:

def calcular_descuento(precio, porcentaje):
    return precio * (1 - porcentaje / 100)
```

**IA genera** (formato inconsistente):
```python
# Esta función calcula el descuento
def calcular_descuento(precio, porcentaje):
    return precio * (1 - porcentaje / 100)
```

---

**Con ejemplos** (Few-shot):
```
Genera docstrings en formato Google para esta función.

EJEMPLO de formato Google:

```python
def sumar(a: int, b: int) -> int:
    """Suma dos números enteros.

    Args:
        a (int): Primer número
        b (int): Segundo número

    Returns:
        int: Suma de a y b

    Examples:
        >>> sumar(2, 3)
        5
    """
    return a + b
```

Ahora genera docstring para:

```python
def calcular_descuento(precio, porcentaje):
    return precio * (1 - porcentaje / 100)
```
```

**IA genera** (formato correcto):
```python
def calcular_descuento(precio: float, porcentaje: float) -> float:
    """Calcula el precio con descuento aplicado.

    Args:
        precio (float): Precio original del producto
        porcentaje (float): Porcentaje de descuento (0-100)

    Returns:
        float: Precio final después de aplicar descuento

    Examples:
        >>> calcular_descuento(100, 10)
        90.0
        >>> calcular_descuento(50, 20)
        40.0
    """
    return precio * (1 - porcentaje / 100)
```

**Beneficio**: Formato consistente, output predecible.

---

**Ejercicio**: Usa Few-Shot para generar commits

```
Genera commits siguiendo Conventional Commits.

EJEMPLOS:

Cambio: Añadí función validar_email()
Commit: feat(validacion): add email validation function

Cambio: Corregí bug en login (tokens expiraban inmediatamente)
Commit: fix(auth): correct token expiration time

Cambio: Actualicé README con instrucciones de instalación
Commit: docs(readme): add installation instructions

Ahora genera commit para:
Cambio: Refactoriqué la función crear_tarea() para separar validación de lógica de guardado
```

**Tiempo**: 10 min

---

### 3.3 Divide and Conquer (Dividir Tareas Complejas) (25 min)

**Problema**: Tareas grandes generan código de baja calidad.

**Tarea compleja** (mal abordada):
```
Crea una API completa de e-commerce con productos, carrito, checkout, y autenticación
```

**IA genera**: Código mezclado, sin tests, difícil de mantener.

---

**Divide and Conquer** (bien abordado):

**Paso 1**: Arquitectura
```
Diseña la arquitectura de una API de e-commerce.

Incluye:
- Entidades principales (Usuario, Producto, Carrito, Orden)
- Endpoints necesarios
- Separación en capas (API → Servicio → Repositorio)

NO generes código, solo estructura.
```

**Paso 2**: Implementar entidad por entidad
```
Implementa SOLO la entidad Producto.

Incluye:
- Modelo Pydantic (ProductoCreate, ProductoResponse)
- Servicio (crear, listar, obtener, actualizar)
- Repositorio en memoria
- Endpoints (POST, GET, PUT)
- Tests

Tecnologías: FastAPI, Pydantic, pytest
```

**Paso 3**: Repetir para cada entidad

**Paso 4**: Integración
```
Integra las entidades Producto y Carrito.

- Añadir producto al carrito debe validar que producto existe
- Calcular total del carrito
```

**Beneficio**: Cada paso genera código de alta calidad, incremental, testeable.

---

**Ejercicio**: Divide esta tarea compleja

**Tarea**:
```
Crea un sistema de notificaciones que envíe emails y SMS cuando:
- Usuario se registra
- Usuario hace una compra
- Usuario recupera password
```

**Tu trabajo**: Divide en 4-5 pasos incrementales.

**Tiempo**: 15 min

<details>
<summary>Ejemplo de división</summary>

1. Diseñar interfaz de NotificacionService (qué métodos necesita)
2. Implementar EmailSender (sin enviar real, mock)
3. Implementar SMSSender (sin enviar real, mock)
4. Implementar NotificacionService que usa ambos
5. Integrar con eventos (registro, compra, recuperar password)
6. Tests unitarios para cada componente
7. (Opcional) Reemplazar mocks con servicios reales (SendGrid, Twilio)

</details>

---

### 3.4 Constraining Output (Restringir Formato) (20 min)

**Problema**: IA genera código en formato inesperado.

**Sin restricciones**:
```
Genera tests para la función saludar(nombre)
```

**IA podría generar**:
- Unittest (tú querías pytest)
- Sin fixtures (tú los necesitas)
- En formato que no conoces

---

**Con restricciones de formato**:
```
Genera tests para la función saludar(nombre).

FORMATO REQUERIDO:

```python
import pytest

def test_nombre_descriptivo():
    # Arrange
    input_value = ...

    # Act
    result = funcion(input_value)

    # Assert
    assert result == expected
```

RESTRICCIONES:
- Usa pytest (NO unittest)
- Patrón Arrange-Act-Assert
- Nombres de tests descriptivos (test_saludar_con_nombre_valido)
- Mínimo 3 tests (happy path, edge case, error case)

Función a testear:

```python
def saludar(nombre: str) -> str:
    if not nombre:
        raise ValueError("Nombre vacío")
    return f"Hola, {nombre}"
```
```

**IA genera exactamente** en el formato esperado.

---

**Ejercicio**: Restringe formato para generación de README

```
Genera README.md para un proyecto de API de tareas.

FORMATO REQUERIDO:
# [Nombre]
Descripción breve (1 línea)

## Características
- [ ] Feature 1
- [ ] Feature 2

## Instalación
```bash
# Comandos aquí
```

## Uso
[Ejemplo de código]

## Tecnologías
| Tech | Versión |
|------|---------|
| ... | ... |
```

**Tiempo**: 10 min

---

## 4. Orquestación de Agentes (1h)

### 4.1 Workflow Multi-Agente (20 min)

**Concepto**: Usar múltiples agentes especializados en secuencia.

**Escenario**: Implementar endpoint de autenticación

**Workflow**:

```
1. Diseño de Arquitectura
   → Agente: Clean Architecture Enforcer
   → Input: "Diseña estructura de capas para auth (API → Servicio → Repositorio)"
   → Output: Estructura de archivos, responsabilidades

2. Implementación
   → Tú: Escribes código siguiendo la estructura

3. Revisión de Seguridad
   → Agente: Security Hardening Mentor
   → Input: "Revisa este código de auth en busca de vulnerabilidades"
   → Output: Lista de issues (passwords sin hashear, JWT sin expiración, etc.)

4. Corrección
   → Tú: Arreglas issues

5. Tests
   → Agente: Test Coverage Strategist
   → Input: "Qué tests necesito para auth completo?"
   → Output: Plan de tests (happy path, credenciales inválidas, token expirado, etc.)

6. Implementación de Tests
   → Tú: Escribes tests

7. Commit
   → Agente: Git Commit Helper
   → Input: "Genera commit message para esta feature de auth"
   → Output: feat(auth): add JWT authentication with bcrypt password hashing
```

**Beneficio**: Cada agente aporta su expertise en su fase.

---

### 4.2 Ejemplo Práctico: Crear Feature Completa (25 min)

**Feature**: Endpoint POST /usuarios (registro)

**Paso 1: Prompt para Arquitectura**

```
@clean-architecture-enforcer

Diseña la estructura de archivos y capas para implementar registro de usuarios.

Requisitos:
- Endpoint POST /usuarios
- Validar email (formato correcto, único)
- Hashear password con bcrypt
- Guardar usuario en repositorio

Proporciona:
- Estructura de archivos (api/, servicio_, repositorio_)
- Responsabilidades de cada capa
- Flujo de datos (request → response)

NO generes código todavía, solo arquitectura.
```

**Output esperado**: Estructura clara de capas.

---

**Paso 2: Implementación Manual**

Tú escribes el código siguiendo la arquitectura.

---

**Paso 3: Prompt para Seguridad**

```
@security-hardening-mentor

Revisa este código de registro de usuarios en busca de vulnerabilidades.

```python
# api/api.py
@app.post("/usuarios")
def crear_usuario(email: str, password: str):
    usuario = servicio.crear(email, password)
    return usuario

# servicio_usuarios.py
class ServicioUsuarios:
    def crear(self, email, password):
        usuario = {"email": email, "password": password}
        self._repo.guardar(usuario)
        return usuario
```

Busca:
- OWASP Top 10 issues
- Password handling
- Input validation
- Secrets management
```

**Output esperado**: Lista de vulnerabilidades (password en plain text, sin validación, etc.)

---

**Paso 4: Corrección de Issues**

Tú arreglas los problemas detectados.

---

**Paso 5: Prompt para Tests**

```
@test-coverage-strategist

Necesito tests para registro de usuarios. Qué debería testear?

Función:

```python
def crear_usuario(email: str, password: str) -> Usuario:
    validar_email(email)
    verificar_email_unico(email)
    password_hash = hashear_password(password)
    usuario = Usuario(email=email, password_hash=password_hash)
    repositorio.guardar(usuario)
    return usuario
```

Dame:
- Lista priorizada de tests (críticos primero)
- Qué mockear y por qué
- Edge cases a cubrir
```

**Output esperado**: Plan de tests detallado.

---

**Paso 6: Implementación de Tests**

Tú escribes tests siguiendo el plan.

---

**Paso 7: Prompt para Commit**

```
@git-commit-helper

Genera commit message para estos cambios:

- Añadí endpoint POST /usuarios
- Email validation con regex
- Password hashing con bcrypt
- Tests completos (95% coverage)
- Manejo de errores (email duplicado, email inválido)

Archivos cambiados:
- api/api.py (nuevo endpoint)
- servicio_usuarios.py (nueva clase)
- repositorio_usuarios.py (nueva clase)
- tests/test_crear_usuario.py (nuevos tests)
```

**Output esperado**: `feat(auth): add user registration with email validation and password hashing`

---

### 4.3 Ejercicio: Orquesta Agentes para Feature (15 min)

**Feature**: Implementar "Marcar tarea como completada" (PUT /tareas/{id}/completar)

**Tu tarea**: Diseña workflow de 5-7 pasos usando agentes.

**Agentes disponibles**:
- Clean Architecture Enforcer
- Security Hardening Mentor
- Test Coverage Strategist
- Git Commit Helper

**Tiempo**: 15 min

**Entregable**: Lista de pasos con agente asignado a cada uno.

---

## 5. Debugging de Prompts (45 min)

### 5.1 Problema: Output de Baja Calidad (15 min)

**Síntomas**:
- IA genera código que no compila
- IA no sigue instrucciones
- IA genera código muy genérico

**Diagnóstico**:

**Problema 1**: Prompt demasiado vago

Ejemplo:
```
Crea una API
```

**Solución**: Añadir especificidad
```
Crea una API REST con FastAPI para [dominio].
Endpoints: [listar]
Tecnologías: [especificar versiones]
```

---

**Problema 2**: Restricciones contradictorias

Ejemplo:
```
Crea código simple y básico, pero que use arquitectura avanzada con DDD, CQRS, y Event Sourcing
```

**Solución**: Eliminar contradicción
```
Crea código con arquitectura de 3 capas (API → Servicio → Repositorio).
NO uses patrones avanzados (DDD, CQRS).
```

---

**Problema 3**: Contexto insuficiente

Ejemplo:
```
¿Cómo testeo esto? [sin mostrar código]
```

**Solución**: Proveer contexto completo
```
Tengo esta función [código]. Usa [tecnologías]. ¿Cómo testearla?
```

---

### 5.2 Iterar Prompts (20 min)

**Pattern**: Prompt inicial → Output malo → Refinar prompt → Output mejor

**Iteración 1**:
```
Crea tests para crear_tarea()
```

**Output**: Tests genéricos sin estructura.

---

**Iteración 2** (añadir restricciones):
```
Crea tests para crear_tarea() usando pytest.

Restricciones:
- Patrón Arrange-Act-Assert
- Nombres descriptivos
```

**Output**: Mejor, pero sin edge cases.

---

**Iteración 3** (añadir ejemplos):
```
Crea tests para crear_tarea() usando pytest.

Ejemplo de formato:

```python
def test_crear_tarea_con_nombre_valido():
    # Arrange
    nombre = "Comprar pan"
    prioridad = "alta"

    # Act
    tarea = crear_tarea(nombre, prioridad)

    # Assert
    assert tarea["nombre"] == nombre
    assert tarea["prioridad"] == prioridad
```

Incluye tests para:
- Happy path
- Nombre vacío (debe raise ValueError)
- Prioridad inválida (debe raise ValueError)
```

**Output**: Tests completos y correctos.

---

**Ejercicio**: Itera este prompt

**Iteración 1**:
```
Explica SOLID
```

(Prueba con IA, ve qué output da)

**Tu trabajo**: Itera 2 veces para obtener:
- Explicación concisa de cada principio
- Ejemplo de violación en Python
- Ejemplo correcto en Python

**Tiempo**: 15 min

---

### 5.3 Debugging Checklist (10 min)

**Si IA no da buen output, verifica**:

- [ ] **Rol definido**: ¿Le dijiste en qué es experto?
- [ ] **Contexto completo**: ¿Sabe tu nivel, tecnologías, problema?
- [ ] **Objetivo claro**: ¿Sabe QUÉ quieres lograr?
- [ ] **Restricciones explícitas**: ¿Sabe qué NO hacer?
- [ ] **Formato de output**: ¿Sabe cómo estructurar respuesta?
- [ ] **Ejemplos**: ¿Le mostraste output esperado?
- [ ] **Sin contradicciones**: ¿Tus restricciones son consistentes?

**Si falla en 2+ checks** → Refina el prompt.

---

## 6. Proyecto Final - Prompt Library (1h)

### 6.1 Objetivo del Proyecto

Crear una **biblioteca de prompts reutilizables** para tareas comunes de desarrollo.

**Analogía**: Biblioteca de snippets de código, pero para prompts.

---

### 6.2 Estructura de la Library

**Archivo**: `prompts-library.md`

**Categorías**:
1. Generación de Código
2. Refactoring
3. Testing
4. Documentación
5. Debugging
6. Arquitectura
7. Seguridad

---

### 6.3 Template de Prompt en Library

```markdown
### [Nombre del Prompt]

**Categoría**: [Generación/Refactoring/Testing/etc.]

**Cuándo usar**: [Descripción de cuándo este prompt es útil]

**Prompt**:
```
[Prompt completo con placeholders]
```

**Placeholders**:
- `[TECNOLOGIA]`: Reemplazar con framework/librería
- `[CODIGO]`: Pegar código aquí
- `[REQUISITOS]`: Listar requisitos específicos

**Ejemplo de uso**:
```
[Prompt con placeholders reemplazados]
```

**Output esperado**:
[Descripción breve del output]
```

---

### 6.4 Requisitos del Proyecto (30 min de implementación)

**Crea `prompts-library.md` con mínimo 10 prompts** (2 por categoría mínimo).

**Prompts requeridos**:

1. **Generación de Código**: Crear endpoint REST completo
2. **Generación de Código**: Crear función con docstrings y type hints
3. **Refactoring**: Extraer método (Extract Method pattern)
4. **Refactoring**: Simplificar función compleja
5. **Testing**: Generar tests unitarios con pytest
6. **Testing**: Generar tests de integración
7. **Documentación**: Generar README completo
8. **Documentación**: Generar ADR (Architecture Decision Record)
9. **Debugging**: Analizar código en busca de bugs
10. **Arquitectura**: Diseñar estructura de capas

---

### 6.5 Ejemplo de Prompt en Library

```markdown
### Crear Endpoint REST Completo

**Categoría**: Generación de Código

**Cuándo usar**: Necesitas implementar un endpoint nuevo con validación, lógica de negocio, y tests.

**Prompt**:
```
Crea un endpoint [METODO] [RUTA] con [TECNOLOGIA].

Requisitos:
- Request model: [CAMPOS_REQUEST]
- Response model: [CAMPOS_RESPONSE]
- Validación: [REGLAS_VALIDACION]
- Lógica de negocio: [DESCRIPCION_LOGICA]

Arquitectura:
- Separación en capas (API → Servicio → Repositorio)
- Repositorio: [TIPO_REPOSITORIO]

Incluye:
- Pydantic models con validación
- Docstrings en endpoint
- Manejo de errores (HTTPException)
- Tests con pytest y TestClient

Tecnologías: [TECNOLOGIA] [VERSION], Python [VERSION]
```

**Placeholders**:
- `[METODO]`: POST, GET, PUT, DELETE
- `[RUTA]`: /tareas, /usuarios, etc.
- `[TECNOLOGIA]`: FastAPI, Flask, Django
- `[CAMPOS_REQUEST]`: Lista de campos del request body
- `[CAMPOS_RESPONSE]`: Lista de campos del response
- `[REGLAS_VALIDACION]`: Validaciones específicas
- `[DESCRIPCION_LOGICA]`: Qué hace el endpoint
- `[TIPO_REPOSITORIO]`: En memoria, JSON, DB

**Ejemplo de uso**:
```
Crea un endpoint POST /tareas con FastAPI.

Requisitos:
- Request model: nombre (str, 1-100 chars), prioridad (alta/media/baja)
- Response model: id, nombre, prioridad, completada
- Validación: nombre no vacío, prioridad válida
- Lógica de negocio: Crear tarea y guardar en repositorio

Arquitectura:
- Separación en capas (API → Servicio → Repositorio)
- Repositorio: En memoria

Incluye:
- Pydantic models con validación
- Docstrings en endpoint
- Manejo de errores (HTTPException)
- Tests con pytest y TestClient

Tecnologías: FastAPI 0.118, Python 3.12
```

**Output esperado**:
- `api.py` con endpoint completo
- `servicio_tareas.py` con lógica
- `repositorio_memoria.py` con almacenamiento
- `test_crear_tarea.py` con tests
```

---

### 6.6 Criterios de Evaluación (30 min)

| Criterio | Peso | Descripción |
|----------|------|-------------|
| **Completitud** | 30% | 10+ prompts, todas las categorías cubiertas |
| **Calidad de Prompts** | 30% | Prompts específicos, con restricciones claras |
| **Ejemplos** | 20% | Cada prompt tiene ejemplo de uso completo |
| **Utilidad** | 10% | Prompts son realmente útiles para desarrollo |
| **Formato** | 10% | Markdown correcto, bien organizado |

**Total**: 100 puntos

---

## 7. Evaluación y Entregables

### 7.1 Entregables de la Clase

1. **Ejercicio de mejora de prompt** (Ejercicio 2.3) - 10%
2. **División de tarea compleja** (Ejercicio 3.3) - 15%
3. **Workflow multi-agente** (Ejercicio 4.3) - 25%
4. **Prompt Library completa** (Proyecto Final) - 50%

**Mínimo para aprobar**: 70/100

---

### 7.2 Autoevaluación

- [ ] ¿Puedo escribir un prompt avanzado con todas las secciones?
- [ ] ¿Entiendo cuándo usar Chain of Thought vs Few-Shot?
- [ ] ¿Puedo dividir tareas complejas en pasos manejables?
- [ ] ¿Sé cómo orquestar múltiples agentes para una feature?
- [ ] ¿Puedo diagnosticar por qué un prompt da mal output?
- [ ] ¿Puedo iterar prompts para mejorar resultados?

**Si respondiste NO a 2+ preguntas**: Repasa las secciones correspondientes.

---

### 7.3 Recursos Adicionales

**Guías de Prompt Engineering**:
- OpenAI Prompt Engineering Guide
- Anthropic Prompt Engineering Tutorial
- Prompt Engineering Guide (GitHub)

**Ejemplos de Prompts**:
- Awesome ChatGPT Prompts (GitHub)
- FlowGPT Prompt Library

**Papers**:
- "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
- "Large Language Models are Zero-Shot Reasoners"

---

## Resumen de la Clase

En esta clase aprendiste:

1. **Principios de Prompt Engineering**: Especificidad, contexto, formato, restricciones
2. **Anatomía de prompt avanzado**: 8 secciones (rol, contexto, objetivo, restricciones, formato, ejemplos, validación)
3. **Técnicas avanzadas**: Chain of Thought, Few-Shot, Divide and Conquer, Constraining Output
4. **Orquestación de agentes**: Workflow multi-agente para features complejas
5. **Debugging de prompts**: Diagnosticar por qué falla, iterar para mejorar
6. **Prompt Library**: Crear biblioteca reutilizable de prompts

**Skill clave**: Obtener output de alta calidad de IA mediante prompts bien estructurados.

**Próxima clase**: Clase 6 - Limitaciones y Ética (cuándo NO usar IA, edge cases, responsabilidad).

---

**Regla de oro del Prompt Engineering**: La calidad del output es directamente proporcional a la especificidad del input.

Prompt vago → Output genérico
Prompt específico → Output útil

¡Itera tus prompts como iteras tu código!
