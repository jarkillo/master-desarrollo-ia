# Ejercicios Prácticos: TDD + IA - Clase 2

## 🎯 Objetivo General

Dominar el workflow **TDD + IA + Agentes Educacionales** implementando funcionalidades reales en la API de Tareas. Cada ejercicio sigue el ciclo:

```
RED (test) → GREEN (implementación) → REFACTOR (agentes) → COMMIT
```

---

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener:

- [x] Entorno virtual activado (`.venv`)
- [x] Dependencias instaladas (`pytest`, `fastapi`, `httpx`)
- [x] Código base de la Clase 2 funcionando
- [x] Todos los tests actuales en verde (`pytest -v`)

---

## 🎯 Ejercicio 1: Implementar PATCH /tareas/{id} (Actualización Parcial)

### Contexto

Actualmente tenemos `PUT /tareas/{id}/completar` que solo cambia el campo `completada`.
Queremos agregar un endpoint más flexible que permita actualizar **cualquier campo** (nombre o completada).

### Historia de Usuario

> Como usuario de la API, quiero poder actualizar el nombre de una tarea existente sin tener que recrearla.

### Paso 1: RED - Escribir el test primero

**Archivo**: `tests/test_actualizar_tarea.py`

**Prompt sugerido para IA**:
```
Rol: QA Engineer Python
Contexto: API FastAPI de tareas con modelo Tarea(id: int, nombre: str, completada: bool)
Objetivo: Genera tests pytest para endpoint PATCH /tareas/{id} que actualice nombre y/o completada
Requisitos:
- Test 1: Actualizar solo nombre (completada no cambia)
- Test 2: Actualizar solo completada (nombre no cambia)
- Test 3: Actualizar ambos campos
- Test 4: PATCH a tarea inexistente devuelve 404
- Test 5: PATCH con nombre vacío devuelve 422
Formato: pytest con TestClient, docstrings claros
```

**Criterio de éxito**:
- pytest falla con `404 Not Found` (endpoint no existe aún)
- Al menos 5 tests implementados

**Entregable**:
```bash
pytest tests/test_actualizar_tarea.py -v
# Resultado esperado: 5 tests FAIL (❌ ROJO)
```

---

### Paso 2: GREEN - Implementación mínima con IA

**Archivo**: `api/api.py`

**Prompt para IA**:
```
Rol: Backend Developer FastAPI
Contexto: API de tareas con estos tests que fallan: [pegar tests del paso 1]
Objetivo: Implementa PATCH /tareas/{id} para hacer pasar los tests
Requisitos:
- Request model con campos opcionales (nombre: str | None, completada: bool | None)
- Solo actualizar campos que vienen en el request (no sobrescribir con None)
- Response: 200 con tarea actualizada, 404 si no existe, 422 si validación falla
- Usar Pydantic para validación
Restricciones: Código MÍNIMO necesario, sin optimizaciones prematuras
```

**Criterio de éxito**:
- `pytest tests/test_actualizar_tarea.py -v` → ✅ VERDE (5/5 passed)
- No se rompieron tests existentes
- Código funciona pero puede no ser óptimo

**Validación**:
```bash
pytest tests/ -v
# Todos los tests (12 originales + 5 nuevos = 17) deben pasar
```

---

### Paso 3: REFACTOR - Mejora con agentes educacionales

#### 3.1 Python Best Practices Coach

**Checklist a revisar**:
- [ ] ¿Tiene type hints completos? (`str | None` para opcionales en Python 3.10+)
- [ ] ¿Docstring explica qué hace y qué devuelve?
- [ ] ¿Usa f-strings para mensajes de error?
- [ ] ¿Request model tiene valores por defecto apropiados?

**Mejora esperada**:
```python
from typing import Optional  # Python 3.9
# O mejor (Python 3.10+):
# nombre: str | None = None

class ActualizarTareaRequest(BaseModel):
    """Modelo para actualización parcial de tarea."""
    nombre: str | None = Field(None, min_length=1)
    completada: bool | None = None

@app.patch("/tareas/{id}", response_model=TareaResponse)
def actualizar_tarea(id: int, cuerpo: ActualizarTareaRequest) -> TareaResponse:
    """Actualiza parcialmente una tarea existente.

    Args:
        id: ID de la tarea a actualizar
        cuerpo: Campos a actualizar (solo los presentes)

    Returns:
        Tarea actualizada con los cambios aplicados

    Raises:
        HTTPException: 404 si tarea no existe, 422 si validación falla
    """
    # Implementación...
```

#### 3.2 FastAPI Design Coach

**Checklist**:
- [ ] Status code correcto (200 para actualización exitosa)
- [ ] Response model explícito (`response_model=TareaResponse`)
- [ ] Manejo de errores con HTTPException
- [ ] Documentación OpenAPI completa (`summary`, `tags`, `responses`)

**Mejora esperada**:
```python
@app.patch(
    "/tareas/{id}",
    response_model=TareaResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar parcialmente una tarea",
    tags=["tareas"],
    responses={
        200: {"description": "Tarea actualizada correctamente"},
        404: {"description": "Tarea no encontrada"},
        422: {"description": "Validación de datos falló"}
    }
)
```

#### 3.3 API Design Reviewer

**Validación**:
- [ ] PATCH vs PUT: ¿Usaste PATCH (parcial) en vez de PUT (completo)? ✅
- [ ] Idempotencia: ¿PATCH repetido con mismo payload produce mismo resultado? ✅
- [ ] Consistencia: ¿Formato de respuesta igual a otros endpoints? ✅

**Re-ejecutar tests**:
```bash
pytest tests/ -v
# Resultado esperado: ✅ VERDE (17/17 passed)
```

---

### Paso 4: Validación final y commit

**Checklist completo**:
- [ ] Todos los tests pasan (`pytest -v`)
- [ ] Type checking sin errores (`mypy api/api.py`)
- [ ] Linting sin warnings (`ruff check api/`)
- [ ] Python Best Practices Coach aprueba
- [ ] FastAPI Design Coach aprueba
- [ ] API Design Reviewer aprueba

**Commit**:
```bash
git add tests/test_actualizar_tarea.py api/api.py
git commit -m "feat(api): agregar endpoint PATCH /tareas/{id} para actualización parcial

- Implementado con TDD (5 tests nuevos)
- Validación con Pydantic
- Refactorizado con agentes educacionales
- Coverage: 17/17 tests passing"
```

---

## 🎯 Ejercicio 2: Code Review con FastAPI Design Coach

### Contexto

Ya implementaste varios endpoints. Ahora vas a **revisar código existente** con el FastAPI Design Coach para detectar mejoras arquitecturales.

### Objetivo

Identificar y aplicar mejoras sugeridas por el agente en los endpoints existentes (POST, GET, PUT, DELETE).

### Paso 1: Lectura del agente

**Archivo a leer**: `.claude/agents/educational/fastapi-design-coach.md`

**Tarea**:
1. Lee **completo** el documento del agente
2. Identifica las secciones:
   - "Anti-patterns to Detect"
   - "RESTful Design Validation"
   - "Pydantic Best Practices"
3. Anota los 5 anti-patterns más comunes

**Entregable**: Documento `review-notes.md` con:
```markdown
# Notas de FastAPI Design Coach

## Anti-patterns detectados en mi código

1. [Descripción del anti-pattern]
   - Ubicación: `api.py` línea X
   - Severidad: Alta/Media/Baja
   - Solución propuesta: ...

2. ...
```

---

### Paso 2: Aplicar mejoras

**Revisar cada endpoint contra checklist del agente**:

#### Endpoint POST /tareas

**Checklist**:
- [ ] Response model con Pydantic (`response_model=TareaResponse`) ✅
- [ ] Status code 201 Created ✅
- [ ] Location header con URL del recurso creado ❌ **¡Mejora identificada!**

**Mejora sugerida**:
```python
from fastapi import Response

@app.post("/tareas", ...)
def crear_tarea(cuerpo: CrearTareaRequest, response: Response) -> TareaResponse:
    # ... código existente ...

    nueva_tarea = TareaResponse(...)
    _tareas.append(nueva_tarea)

    # ✅ Agregar Location header (REST best practice)
    response.headers["Location"] = f"/tareas/{nueva_tarea.id}"

    return nueva_tarea
```

#### Endpoint DELETE /tareas/{id}

**Checklist**:
- [ ] Status code 204 No Content ✅
- [ ] No devuelve body ✅
- [ ] Usa `None` como return type ✅

**Validación**: ✅ Este endpoint ya cumple best practices

---

### Paso 3: Tests para las mejoras

**Si agregaste Location header**, crea test:

```python
def test_crear_tarea_devuelve_location_header():
    """Verifica que POST /tareas devuelve Location header."""
    api_mod._tareas.clear()
    api_mod._contador_id = 0

    cliente = TestClient(api_mod.app)
    respuesta = cliente.post("/tareas", json={"nombre": "Test"})

    assert "location" in respuesta.headers
    assert respuesta.headers["location"] == "/tareas/1"
```

**Criterio de éxito**:
```bash
pytest tests/test_crear_tarea_clase2.py::test_crear_tarea_devuelve_location_header -v
# ✅ PASSED
```

---

### Paso 4: Documentación de learnings

**Archivo**: `learnings.md`

**Contenido esperado**:
```markdown
# Learnings del Code Review con FastAPI Design Coach

## Mejoras aplicadas

### 1. Location header en POST
**Por qué**: REST recomienda devolver la URL del recurso creado en el header `Location`.
**Cómo**: Inyectar `Response` y agregar `response.headers["Location"] = f"/tareas/{id}"`
**Impacto**: Clientes pueden conocer la URL sin parsear el body

### 2. [Otra mejora aplicada]

## Anti-patterns evitados

### 1. Devolver dict en vez de modelo Pydantic
**Por qué es malo**: Sin tipado, sin validación automática
**Cómo evitarlo**: Siempre usar `response_model=MiModelo`

## Referencias
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [REST HTTP Status Codes](https://www.rfc-editor.org/rfc/rfc7231#section-6.3)
```

**Criterio de éxito**: Documento completo con al menos 2 mejoras y 2 anti-patterns

---

## 🎯 Ejercicio 3: Refactoring Guiado - Filtrar Tareas por Estado

### Contexto

El endpoint `GET /tareas` devuelve **todas** las tareas. Los usuarios quieren poder filtrar por estado (`completada=true/false`).

### Historia de Usuario

> Como usuario, quiero poder filtrar las tareas por estado (completadas o pendientes) para ver solo las que me interesan.

---

### Paso 1: Diseño con IA

**Prompt para IA**:
```
Rol: API Architect
Contexto: API REST de tareas. Endpoint actual GET /tareas devuelve todas las tareas
Objetivo: Diseña query parameter para filtrar por estado (completada: true/false/all)
Requisitos:
- GET /tareas → todas las tareas (comportamiento actual)
- GET /tareas?completada=true → solo completadas
- GET /tareas?completada=false → solo pendientes
- Validar que query param es opcional
Pregunta: ¿Qué tipo usar para el query param? (bool, str, Enum)
Formato: Explica pros/contras de cada opción y recomienda una
```

**IA te dará algo como**:
```python
from enum import Enum
from typing import Optional

class EstadoFiltro(str, Enum):
    COMPLETADAS = "true"
    PENDIENTES = "false"
    TODAS = "all"

@app.get("/tareas")
def listar_tareas(completada: Optional[EstadoFiltro] = None):
    ...
```

**Tarea**: Lee la respuesta de la IA y **justifica** por qué recomienda Enum vs bool.

---

### Paso 2: RED - Tests primero

**Archivo**: `tests/test_filtrar_tareas.py`

**Tests a implementar** (escríbelos tú, sin IA):

1. `test_filtrar_tareas_completadas()`
   - Crear 2 tareas, completar una
   - GET /tareas?completada=true
   - Assert: solo devuelve la completada

2. `test_filtrar_tareas_pendientes()`
   - Crear 2 tareas, completar una
   - GET /tareas?completada=false
   - Assert: solo devuelve la pendiente

3. `test_sin_filtro_devuelve_todas()`
   - Crear 2 tareas, completar una
   - GET /tareas (sin query param)
   - Assert: devuelve ambas

**Ejecutar**:
```bash
pytest tests/test_filtrar_tareas.py -v
# ❌ ROJO (feature no existe)
```

---

### Paso 3: GREEN - Implementación

**Modificar**: `api/api.py`

**Implementa tú mismo** (sin IA) la lógica de filtrado:

```python
@app.get("/tareas", response_model=List[TareaResponse])
def listar_tareas(completada: Optional[bool] = None) -> List[TareaResponse]:
    """Lista tareas con filtro opcional por estado.

    Args:
        completada: Filtro opcional (True=solo completadas, False=solo pendientes, None=todas)

    Returns:
        Lista de tareas filtradas
    """
    if completada is None:
        return _tareas

    # ¿Cómo filtrar aquí?
    # Pista: usa list comprehension
```

**Criterio de éxito**:
```bash
pytest tests/test_filtrar_tareas.py -v
# ✅ VERDE (3/3 passed)
```

---

### Paso 4: REFACTOR - Python Best Practices Coach

**Checklist**:
- [ ] ¿Usaste list comprehension para filtrar? (vs loop manual)
- [ ] ¿Type hints completos? (`Optional[bool]`)
- [ ] ¿Docstring explica el parámetro `completada`?

**Mejora esperada**:
```python
# ❌ Antes (loop manual)
resultado = []
for tarea in _tareas:
    if completada is None or tarea.completada == completada:
        resultado.append(tarea)
return resultado

# ✅ Después (list comprehension)
if completada is None:
    return _tareas
return [t for t in _tareas if t.completada == completada]
```

**Re-ejecutar tests**:
```bash
pytest tests/ -v
# ✅ VERDE (20/20 passed - 17 anteriores + 3 nuevos)
```

---

### Paso 5: Documentación OpenAPI

**Validar en Swagger UI**:

1. Levantar servidor:
   ```bash
   uvicorn api.api:app --reload
   ```

2. Abrir navegador: `http://localhost:8000/docs`

3. Verificar que `GET /tareas` muestra:
   - Query parameter `completada` (opcional)
   - Descripción del parámetro
   - Ejemplos de uso

**Screenshot esperado**:
```
GET /tareas
Parameters:
  completada (query, optional): boolean
    Filtro por estado (true=completadas, false=pendientes)
```

---

### Paso 6: Commit final

```bash
git add tests/test_filtrar_tareas.py api/api.py
git commit -m "feat(api): agregar filtro opcional por estado en GET /tareas

- Query param completada: bool | None
- Tests con 100% coverage del filtro
- Refactorizado con list comprehension (Python Best Practices Coach)
- Documentación OpenAPI actualizada
- 20/20 tests passing"
```

---

## ✅ Checklist General de los 3 Ejercicios

Al finalizar los 3 ejercicios, debes tener:

### Código
- [ ] PATCH /tareas/{id} implementado y testeado
- [ ] Location header en POST /tareas
- [ ] Filtro por estado en GET /tareas
- [ ] Todos los tests en verde (`pytest -v`)
- [ ] Type checking sin errores (`mypy api/`)
- [ ] Linting limpio (`ruff check api/`)

### Documentación
- [ ] `review-notes.md` con análisis del FastAPI Design Coach
- [ ] `learnings.md` con aprendizajes del code review
- [ ] Commits descriptivos siguiendo Conventional Commits

### Aprendizajes
- [ ] Comprendes el ciclo TDD (RED → GREEN → REFACTOR)
- [ ] Sabes usar los 3 agentes educacionales
- [ ] Reconoces anti-patterns sin ayuda de IA
- [ ] Puedes explicar por qué cada mejora es importante

---

## 🎓 Criterios de Evaluación

| Criterio | Peso | Descripción |
|----------|------|-------------|
| **Tests** | 30% | Todos los tests pasan, coverage > 80% |
| **Clean Code** | 25% | Type hints, docstrings, código Pythonic |
| **REST Design** | 20% | Status codes, response models, convenciones |
| **Learnings** | 15% | Documentación de aprendizajes clara |
| **Autonomía** | 10% | Resolviste problemas sin copiar/pegar ciegamente |

**Nota mínima**: 7/10 (70%)

---

## 💡 Tips para Éxito

### 1. No copies código de IA sin entender

✅ **Correcto**:
1. IA genera código
2. Lees línea por línea
3. Entiendes qué hace cada parte
4. Validas con tests
5. Aplicas mejoras de agentes

❌ **Incorrecto**:
1. IA genera código
2. Copias y pegas
3. Tests pasan
4. Commit sin revisar

### 2. Usa los agentes como checklist, no como magia

Los agentes no ejecutan código automáticamente. Son **guías educativas**:

1. Lees el agente
2. Identificas patterns en tu código
3. Aplicas mejoras manualmente
4. Re-ejecutas tests

### 3. TDD no es opcional

Siempre:
1. Test primero (RED)
2. Código después (GREEN)
3. Mejora al final (REFACTOR)

Nunca:
1. Código primero
2. Tests después (si hay tiempo)

---

## 🚀 Recursos Adicionales

**Documentación**:
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

**Agentes**:
- [Python Best Practices Coach](../../.claude/agents/educational/python-best-practices-coach.md)
- [FastAPI Design Coach](../../.claude/agents/educational/fastapi-design-coach.md)
- [API Design Reviewer](../../.claude/agents/educational/api-design-reviewer.md)

**Herramientas**:
```bash
# Tests
pytest -v

# Coverage
pytest --cov=api --cov-report=term-missing

# Type checking
mypy api/

# Linting
ruff check api/

# Formatting
ruff format api/
```

---

## 📝 Entregables Finales

Crea una carpeta `entregables/` con:

```
entregables/
├── tests/
│   ├── test_actualizar_tarea.py
│   └── test_filtrar_tareas.py
├── review-notes.md
├── learnings.md
└── screenshots/
    ├── tests-passing.png
    ├── swagger-ui.png
    └── coverage-report.png
```

**Comprime** (`entregables.zip`) y sube al LMS del master.

---

**¡Buena suerte!** Recuerda: el objetivo no es tener código perfecto, sino **entender el proceso** de TDD + IA + Agentes.

**Pregunta clave a responder al final**: *"¿Cómo cambia mi forma de programar cuando combino TDD con IA y agentes educacionales?"*
