# Workflow de Agentes Educacionales - Clase 2

## 🎯 Objetivo

Aprender a usar agentes especializados para validar y mejorar código CRUD con FastAPI. Este workflow transforma código "que funciona" en código **profesional, mantenible y Pythonic**.

---

## 📊 Agentes Disponibles

### 1. Python Best Practices Coach

**Ubicación**: `.claude/agents/educational/python-best-practices-coach.md`

**Cuándo usar**:
- Después de escribir código Python (antes de commit)
- Cuando recibes código generado por IA
- Al refactorizar código existente

**Qué valida**:
- ✅ Type hints (PEP 484) completos
- ✅ List/dict comprehensions vs loops manuales
- ✅ f-strings vs concatenación antigua
- ✅ Pathlib vs os.path
- ✅ Dataclasses/Pydantic vs dicts para datos estructurados
- ✅ Context managers (`with` statements)

**Ejemplo de uso**:

```python
# Código inicial (funciona pero no es Pythonic)
@app.get("/tareas")
def listar_tareas():
    return []
```

**Después de aplicar Python Best Practices Coach**:
```python
from typing import List
from pydantic import BaseModel

class TareaResponse(BaseModel):
    id: int
    nombre: str
    completada: bool

@app.get("/tareas", response_model=List[TareaResponse])
def listar_tareas() -> List[TareaResponse]:
    """Devuelve la lista de todas las tareas.

    Returns:
        Lista de tareas con id, nombre y estado de completitud
    """
    return []
```

**Cómo revisar con el agente**:

1. Abre el archivo del agente: `.claude/agents/educational/python-best-practices-coach.md`
2. Lee la sección "Pattern Recognition"
3. Busca en tu código los anti-patterns listados:
   - ¿Falta type hints? → Ver "Pattern 2"
   - ¿Concatenas strings? → Ver "Pattern 3"
   - ¿Usas loops manuales con append? → Ver "Pattern 1"
4. Aplica las soluciones Pythonic sugeridas
5. Re-ejecuta tests: `pytest -v`

**Red flags que detecta**:
- ❌ Funciones sin type annotations
- ❌ `"texto " + variable + " más texto"` (usa f-strings)
- ❌ `resultado = []; for x in items: resultado.append(...)` (usa comprehension)
- ❌ `import os; os.path.join(...)` (usa Pathlib)

---

### 2. FastAPI Design Coach

**Ubicación**: `.claude/agents/educational/fastapi-design-coach.md`

**Cuándo usar**:
- Al implementar nuevos endpoints
- Después de generar código con IA
- Al revisar arquitectura de la API

**Qué valida**:
- ✅ RESTful design (verbos HTTP correctos)
- ✅ Response models con Pydantic
- ✅ Status codes apropiados (200, 201, 204, 404, 422)
- ✅ Dependency injection patterns
- ✅ Async/await cuando aplica
- ✅ Validación de entrada con Pydantic

**Ejemplo de uso**:

```python
# ❌ Anti-pattern detectado por el agente
@app.get("/tareas/{id}")
def get_tarea(id: int):
    # ¿Qué pasa si no existe? → Falta manejo de 404
    tarea = encontrar_tarea(id)
    return {"id": tarea.id, "nombre": tarea.nombre}  # ❌ Dict sin tipar
```

**Después de FastAPI Design Coach**:
```python
from fastapi import HTTPException, status

@app.get(
    "/tareas/{id}",
    response_model=TareaResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener una tarea específica",
    responses={
        200: {"description": "Tarea encontrada"},
        404: {"description": "Tarea no encontrada"}
    }
)
def obtener_tarea(id: int) -> TareaResponse:
    """Devuelve una tarea específica por su ID.

    Args:
        id: ID de la tarea a buscar

    Returns:
        Tarea encontrada con todos sus datos

    Raises:
        HTTPException: 404 si la tarea no existe
    """
    tarea = encontrar_tarea(id)
    if tarea is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con id {id} no encontrada"
        )
    return tarea
```

**Cómo revisar**:

1. Lee `.claude/agents/educational/fastapi-design-coach.md`
2. Valida contra checklist del agente:
   - [ ] Response model explícito (`response_model=...`)
   - [ ] Status code correcto (GET → 200, POST → 201, DELETE → 204)
   - [ ] Manejo de errores con HTTPException
   - [ ] Documentación con docstrings
   - [ ] Nombres RESTful (`/tareas` no `/getTareas`)
3. Aplica feedback
4. Re-ejecuta tests

**Red flags**:
- ❌ Devolver `dict` en vez de modelo Pydantic
- ❌ No manejar casos de error (404, 422)
- ❌ Status codes incorrectos (200 para creación en vez de 201)
- ❌ Nombres no-RESTful (`/createTask` vs `/tareas`)

---

### 3. API Design Reviewer

**Ubicación**: `.claude/agents/educational/api-design-reviewer.md`

**Cuándo usar**:
- Al diseñar nuevos endpoints (antes de implementar)
- Al revisar la estructura completa de la API
- Antes de crear Pull Request

**Qué valida**:
- ✅ Convenciones REST completas
- ✅ HTTP semantics correctos
- ✅ Consistencia en formatos de respuesta
- ✅ Paginación y filtrado (cuando aplica)
- ✅ Versionado de API
- ✅ Documentación OpenAPI/Swagger completa

**Ejemplo de revisión**:

```python
# API Review Checklist

## Convenciones REST
- [x] GET /tareas → Listar (200)
- [x] POST /tareas → Crear (201)
- [x] GET /tareas/{id} → Obtener uno (200/404)
- [x] PUT /tareas/{id} → Actualizar completo (200/404)
- [x] PATCH /tareas/{id} → Actualizar parcial (200/404)
- [x] DELETE /tareas/{id} → Eliminar (204/404)

## Status Codes
- [x] 200 OK - GET exitoso
- [x] 201 Created - POST exitoso (con Location header)
- [x] 204 No Content - DELETE exitoso
- [x] 404 Not Found - Recurso no existe
- [x] 422 Unprocessable Entity - Validación falló

## Respuestas Consistentes
- [x] Formato JSON uniforme
- [x] Nombres de campos consistentes (snake_case o camelCase)
- [x] Mensajes de error informativos
```

**Cómo usar**:

1. Abre `.claude/agents/educational/api-design-reviewer.md`
2. Revisa sección "RESTful Principles Checklist"
3. Compara tus endpoints contra la tabla de convenciones
4. Valida status codes
5. Verifica consistencia de respuestas

---

## 🔄 Workflow Completo (Paso a Paso)

### Escenario: Implementar endpoint GET /tareas

#### FASE 1: RED (Test primero)

**Paso 1.1**: Escribir el test

```python
# tests/test_listar_tareas.py
from fastapi.testclient import TestClient
from api.api import app

def test_listar_tareas_vacia_devuelve_lista_vacia():
    cliente = TestClient(app)
    respuesta = cliente.get("/tareas")
    assert respuesta.status_code == 200
    assert respuesta.json() == []
```

**Paso 1.2**: Ejecutar test
```bash
pytest tests/test_listar_tareas.py -v
```

**Resultado esperado**: ❌ ROJO (404 Not Found - endpoint no existe)

---

#### FASE 2: GREEN (Implementación mínima)

**Paso 2.1**: Implementar código mínimo

```python
# api/api.py
@app.get("/tareas")
def listar_tareas():
    return []
```

**Paso 2.2**: Ejecutar test
```bash
pytest tests/test_listar_tareas.py -v
```

**Resultado esperado**: ✅ VERDE

---

#### FASE 3: REFACTOR (Agentes educacionales)

**Paso 3.1**: Python Best Practices Coach

Revisa checklist:
- [ ] ¿Tiene type hints?
- [ ] ¿Tiene docstring?
- [ ] ¿Response model definido?

**Aplicar mejoras**:
```python
from typing import List

@app.get("/tareas")
def listar_tareas() -> List:
    """Devuelve lista de todas las tareas."""
    return []
```

**Paso 3.2**: FastAPI Design Coach

Revisa checklist:
- [ ] ¿Response model con Pydantic?
- [ ] ¿Status code explícito?
- [ ] ¿Documentación completa?

**Aplicar mejoras**:
```python
from typing import List
from pydantic import BaseModel

class TareaResponse(BaseModel):
    id: int
    nombre: str
    completada: bool

@app.get(
    "/tareas",
    response_model=List[TareaResponse],
    status_code=200,
    summary="Listar todas las tareas",
    tags=["tareas"]
)
def listar_tareas() -> List[TareaResponse]:
    """Devuelve la lista completa de tareas.

    Returns:
        Lista de tareas (puede estar vacía)
    """
    return []
```

**Paso 3.3**: API Design Reviewer

Valida:
- [x] Endpoint RESTful (`/tareas` no `/getTareas`)
- [x] Status code correcto (200)
- [x] Response model explícito
- [x] Documentación presente

**Paso 3.4**: Re-ejecutar tests
```bash
pytest tests/ -v
```

**Resultado**: ✅ VERDE (mismo comportamiento, mejor código)

---

## 🎯 Checklist de Validación por Agente

### Python Best Practices Coach

Antes de hacer commit, valida:

- [ ] **Type hints completos**
  ```python
  def funcion(param: str) -> int:  # ✅
  def funcion(param):  # ❌
  ```

- [ ] **Docstrings en funciones públicas**
  ```python
  def funcion():
      """Descripción clara de qué hace."""  # ✅
  ```

- [ ] **f-strings para formateo**
  ```python
  f"Hola {nombre}"  # ✅
  "Hola " + nombre  # ❌
  ```

- [ ] **Comprehensions para transformaciones simples**
  ```python
  [x * 2 for x in lista]  # ✅
  resultado = []
  for x in lista:
      resultado.append(x * 2)  # ❌
  ```

### FastAPI Design Coach

- [ ] **Response models con Pydantic**
  ```python
  @app.get("/tareas", response_model=List[TareaResponse])  # ✅
  @app.get("/tareas")  # ❌ Sin tipar
  ```

- [ ] **Status codes explícitos**
  ```python
  @app.post("/tareas", status_code=201)  # ✅ Creación
  @app.delete("/tareas/{id}", status_code=204)  # ✅ Eliminación
  ```

- [ ] **Manejo de errores con HTTPException**
  ```python
  if not tarea:
      raise HTTPException(status_code=404, detail="No encontrada")  # ✅
  ```

- [ ] **Validación de entrada con Pydantic**
  ```python
  class CrearTareaRequest(BaseModel):
      nombre: str = Field(..., min_length=1)  # ✅ Validación
  ```

### API Design Reviewer

- [ ] **Endpoints RESTful**
  - GET /tareas → Listar
  - POST /tareas → Crear
  - GET /tareas/{id} → Obtener
  - PUT /tareas/{id} → Actualizar
  - DELETE /tareas/{id} → Eliminar

- [ ] **Status codes correctos**
  - 200: OK (GET, PUT exitosos)
  - 201: Created (POST exitoso)
  - 204: No Content (DELETE exitoso)
  - 404: Not Found (recurso no existe)
  - 422: Validation Error (datos inválidos)

- [ ] **Respuestas consistentes**
  - Mismo formato JSON en todos los endpoints
  - Mensajes de error informativos
  - Campos con nombres consistentes

---

## 🚦 Workflow Visual

```
┌───────────────────────────────────────────────────────────┐
│  1. ESCRIBIR TEST (RED)                                   │
│  ┌─────────────────────────────────────────────────┐      │
│  │ • Escribir test pytest                          │      │
│  │ • pytest -v → ❌ ROJO                           │      │
│  └─────────────────────────────────────────────────┘      │
└───────────────────────────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────┐
│  2. IMPLEMENTACIÓN MÍNIMA (GREEN)                         │
│  ┌─────────────────────────────────────────────────┐      │
│  │ • Código mínimo para pasar test                 │      │
│  │ • pytest -v → ✅ VERDE                          │      │
│  └─────────────────────────────────────────────────┘      │
└───────────────────────────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────┐
│  3. REFACTOR CON AGENTES                                  │
│  ┌─────────────────────────────────────────────────┐      │
│  │ A. Python Best Practices Coach                  │      │
│  │    • Type hints                                 │      │
│  │    • Docstrings                                 │      │
│  │    • f-strings                                  │      │
│  │    • Comprehensions                             │      │
│  ├─────────────────────────────────────────────────┤      │
│  │ B. FastAPI Design Coach                         │      │
│  │    • Response models                            │      │
│  │    • Status codes                               │      │
│  │    • HTTPException                              │      │
│  │    • Validation                                 │      │
│  ├─────────────────────────────────────────────────┤      │
│  │ C. API Design Reviewer                          │      │
│  │    • RESTful conventions                        │      │
│  │    • Consistency                                │      │
│  │    • Documentation                              │      │
│  ├─────────────────────────────────────────────────┤      │
│  │ D. Re-ejecutar tests                            │      │
│  │    • pytest -v → ✅ VERDE (refactored)         │      │
│  └─────────────────────────────────────────────────┘      │
└───────────────────────────────────────────────────────────┘
                        │
                        ▼
                     COMMIT
```

---

## 💡 Tips de Uso

### Cuándo usar cada agente

**Python Best Practices Coach** → Siempre
- Cada vez que escribes código Python
- Antes de cada commit
- Al revisar código generado por IA

**FastAPI Design Coach** → Endpoints y arquitectura
- Al implementar nuevos endpoints
- Al refactorizar estructura API
- Después de agregar validaciones

**API Design Reviewer** → Diseño global
- Al completar un conjunto de endpoints
- Antes de crear Pull Request
- Al revisar consistencia de toda la API

### Orden recomendado

1. **Primero**: Python Best Practices Coach (fundamentos)
2. **Segundo**: FastAPI Design Coach (arquitectura API)
3. **Tercero**: API Design Reviewer (visión global)

### Automatización

```bash
# Script de validación completa
#!/bin/bash

echo "🔍 Validando código..."

# 1. Tests
pytest -v || exit 1

# 2. Type checking
mypy api/ || exit 1

# 3. Linting
ruff check api/ || exit 1

# 4. Coverage
pytest --cov=api --cov-fail-under=80 || exit 1

echo "✅ Todas las validaciones pasaron"
```

---

## 📚 Recursos Adicionales

**Agentes educacionales**:
- [Python Best Practices Coach](../../.claude/agents/educational/python-best-practices-coach.md)
- [FastAPI Design Coach](../../.claude/agents/educational/fastapi-design-coach.md)
- [API Design Reviewer](../../.claude/agents/educational/api-design-reviewer.md)

**Documentación oficial**:
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [PEP 484 Type Hints](https://peps.python.org/pep-0484/)

---

## ✅ Checklist Final

Antes de hacer commit, valida:

- [ ] Todos los tests pasan (`pytest -v`)
- [ ] Type checking sin errores (`mypy api/`)
- [ ] Linting sin warnings (`ruff check api/`)
- [ ] Coverage > 80% (`pytest --cov`)
- [ ] Python Best Practices Coach aprueba
- [ ] FastAPI Design Coach aprueba
- [ ] API Design Reviewer aprueba
- [ ] Documentación actualizada

---

**Recuerda**: Los agentes son **guías educativas**, no reglas estrictas. Entiende el **por qué** detrás de cada recomendación antes de aplicarla ciegamente.
