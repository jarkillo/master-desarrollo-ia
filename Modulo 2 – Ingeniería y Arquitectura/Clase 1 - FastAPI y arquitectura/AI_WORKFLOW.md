# Workflow de Agentes Educacionales - Clase 1 (FastAPI Intro)

## 🎯 Objetivo

Aprender a usar agentes de IA para **diseñar y construir tu primera API REST** con FastAPI de manera profesional desde el inicio. Este workflow te guía desde el diseño hasta la implementación con asistencia inteligente.

---

## 📊 Agentes Disponibles para Esta Clase

### 1. FastAPI Design Coach

**Ubicación**: `.claude/agents/educational/fastapi-design-coach.md`

**Cuándo usar**:
- ANTES de escribir tu primer endpoint
- Al diseñar la estructura de la API
- Cuando implementas modelos Pydantic
- Al decidir códigos de estado HTTP

**Qué valida**:
- ✅ Endpoints RESTful correctamente nombrados
- ✅ Modelos Pydantic con validaciones completas
- ✅ HTTP status codes apropiados (200, 201, 404, 422)
- ✅ Response models consistentes
- ✅ Dependency injection desde el inicio

**Ejemplo de uso**:

```python
# ❌ Diseño incorrecto (antes del coach)
@app.get("/get_all_tasks")
def get_tasks():
    return {"data": tareas}

# ✅ Diseño correcto (después del coach)
from fastapi import FastAPI, status
from pydantic import BaseModel, Field
from typing import List

class TareaResponse(BaseModel):
    id: int
    nombre: str = Field(..., min_length=1)
    completada: bool

@app.get("/tareas", response_model=List[TareaResponse], status_code=status.HTTP_200_OK)
def listar_tareas() -> List[TareaResponse]:
    """Devuelve todas las tareas del sistema."""
    return tareas
```

**Pasos para usar el agente**:

1. **Diseña tu API en papel** (endpoints, métodos HTTP, recursos):
   ```
   GET  /tareas         → Listar todas
   POST /tareas         → Crear nueva
   GET  /tareas/{id}    → Obtener por ID
   PUT  /tareas/{id}    → Actualizar
   DELETE /tareas/{id}  → Eliminar
   ```

2. **Antes de codificar**, consulta al FastAPI Design Coach:
   - Lee la sección "RESTful Endpoint Patterns"
   - Verifica que tus URLs sigan las convenciones REST
   - Revisa los códigos de estado apropiados para cada operación

3. **Escribe modelos Pydantic primero**:
   ```python
   from pydantic import BaseModel, Field

   class TareaCreate(BaseModel):
       nombre: str = Field(..., min_length=3, max_length=100)

   class TareaResponse(BaseModel):
       id: int
       nombre: str
       completada: bool
   ```

4. **Implementa endpoints** siguiendo las recomendaciones del coach

5. **Valida** con el checklist:
   - [ ] ¿Los endpoints usan nombres RESTful?
   - [ ] ¿Cada endpoint tiene `response_model`?
   - [ ] ¿Los códigos HTTP son correctos?
   - [ ] ¿Las validaciones Pydantic están completas?

---

### 2. API Design Reviewer

**Ubicación**: `.claude/agents/educational/api-design-reviewer.md`

**Cuándo usar**:
- Después de implementar todos los endpoints
- Antes de escribir tests
- Al revisar APIs existentes de compañeros

**Qué valida**:
- ✅ Consistencia en formato de respuestas
- ✅ Uso correcto de métodos HTTP (GET, POST, PUT, DELETE)
- ✅ Status codes semánticamente correctos
- ✅ Nombres de recursos en plural
- ✅ Estructura de URLs jerárquica

**Ejemplo de revisión**:

```python
# ❌ Problemas detectados por el reviewer
@app.post("/create-task")  # 🚨 Verbo en URL
def create(data: dict):    # 🚨 dict sin validación
    return {"ok": True}     # 🚨 Respuesta inconsistente

@app.get("/task/{id}")     # 🚨 Recurso en singular
def get_task(id: str):     # 🚨 ID debería ser int
    return tarea            # 🚨 Sin response_model

# ✅ Corregido después de la revisión
@app.post("/tareas", status_code=status.HTTP_201_CREATED, response_model=TareaResponse)
def crear_tarea(tarea: TareaCreate) -> TareaResponse:
    """Crea una nueva tarea en el sistema."""
    nueva_tarea = {...}
    return nueva_tarea

@app.get("/tareas/{id}", response_model=TareaResponse)
def obtener_tarea(id: int) -> TareaResponse:
    """Obtiene una tarea específica por su ID."""
    return tarea
```

**Checklist de revisión**:

```markdown
# Revisión API - Clase 1

## Endpoints RESTful ✅/❌
- [ ] Todos los recursos en plural (/tareas, no /tarea)
- [ ] Sin verbos en URLs (/tareas, no /crear-tarea)
- [ ] Métodos HTTP correctos (POST para crear, GET para leer)

## Modelos Pydantic ✅/❌
- [ ] Todos los endpoints tienen request/response models
- [ ] Validaciones Field() en campos requeridos
- [ ] Type hints completos

## HTTP Status Codes ✅/❌
- [ ] GET exitoso → 200
- [ ] POST exitoso → 201
- [ ] Not Found → 404
- [ ] Validación falla → 422 (auto en FastAPI)

## Documentación ✅/❌
- [ ] Docstrings en cada endpoint
- [ ] OpenAPI docs accesibles en /docs
```

---

### 3. Python Best Practices Coach

**Ubicación**: `.claude/agents/educational/python-best-practices-coach.md`

**Cuándo usar**:
- Al escribir funciones auxiliares
- Al estructurar el código del archivo api.py
- Después de implementar lógica de negocio

**Qué valida**:
- ✅ Type hints completos (FastAPI los requiere)
- ✅ Nombres descriptivos (snake_case)
- ✅ Funciones pequeñas y enfocadas
- ✅ Sin lógica duplicada
- ✅ Uso de comprehensions donde apropiado

**Ejemplo**:

```python
# ❌ No Pythonic
def buscar(nombre):
    resultado = []
    for t in tareas:
        if nombre.lower() in t["nombre"].lower():
            resultado.append(t)
    return resultado

# ✅ Pythonic (después del coach)
def buscar_tareas_por_nombre(nombre: str) -> List[TareaResponse]:
    """Busca tareas que contengan el nombre especificado (case-insensitive)."""
    return [
        tarea for tarea in tareas
        if nombre.lower() in tarea.nombre.lower()
    ]
```

---

## 🚀 Workflow Completo: Tu Primera API

### Fase 1: Diseño (con FastAPI Design Coach)

**Paso 1: Definir recursos y operaciones**

Usa este prompt con tu asistente IA:

```
Voy a crear mi primera API REST con FastAPI para un gestor de tareas.

Operaciones CRUD:
- Crear tarea (nombre requerido, min 3 caracteres)
- Listar todas las tareas
- Obtener tarea por ID
- Actualizar tarea (nombre y/o estado completada)
- Eliminar tarea por ID

Ayúdame a diseñar:
1. Los endpoints RESTful (URLs + métodos HTTP)
2. Modelos Pydantic necesarios (Request/Response)
3. Códigos de estado HTTP para cada operación

Muéstrame solo el diseño, sin implementación aún.
```

**Paso 2: Validar diseño con el coach**

Antes de codificar, revisa con FastAPI Design Coach:
- ¿Los endpoints siguen convenciones REST?
- ¿Los modelos Pydantic tienen validaciones?
- ¿Los códigos HTTP son semánticos?

---

### Fase 2: Implementación (con asistencia IA)

**Paso 3: Crear estructura base**

```
Implementa la estructura base de mi API FastAPI:

1. Archivo api.py con:
   - from fastapi import FastAPI, status, HTTPException
   - app = FastAPI(title="Gestor de Tareas", version="1.0.0")
   - Almacenamiento en memoria: tareas = []

2. Modelos Pydantic:
   - TareaBase(BaseModel): campos comunes
   - TareaCreate(TareaBase): para POST
   - TareaUpdate(BaseModel): para PUT (campos opcionales)
   - TareaResponse(TareaBase): para respuestas (con id)

3. Variable para proximo_id: int = 1

Muestra solo la estructura, sin endpoints aún.
```

**Paso 4: Implementar endpoints uno por uno**

Para cada endpoint, usa este prompt:

```
Implementa el endpoint [OPERACIÓN] siguiendo este diseño:

Endpoint: [MÉTODO] [URL]
Request body: [Modelo]
Response: [Modelo]
Status code éxito: [Código]
Errores posibles:
- 404 si no existe
- 422 si validación falla (automático en FastAPI)

Requisitos:
- Docstring completo
- Type hints en parámetros y retorno
- response_model explícito
- Manejo de errores con HTTPException
- Validaciones robustas

Endpoint: _______________
```

**Ejemplo**: Implementar GET /tareas/{id}

```python
@app.get("/tareas/{id}", response_model=TareaResponse, status_code=status.HTTP_200_OK)
def obtener_tarea(id: int) -> TareaResponse:
    """
    Obtiene una tarea específica por su ID.

    Args:
        id: Identificador único de la tarea

    Returns:
        TareaResponse con los datos de la tarea

    Raises:
        HTTPException 404 si la tarea no existe
    """
    tarea = next((t for t in tareas if t["id"] == id), None)
    if tarea is None:
        raise HTTPException(status_code=404, detail=f"Tarea {id} no encontrada")
    return tarea
```

---

### Fase 3: Validación (con API Design Reviewer)

**Paso 5: Revisión completa**

Después de implementar todos los endpoints:

1. **Ejecuta la API**:
   ```bash
   uvicorn api:app --reload
   ```

2. **Abre la documentación**:
   ```
   http://localhost:8000/docs
   ```

3. **Prueba cada endpoint** desde la UI de Swagger

4. **Revisa con API Design Reviewer**:
   - Lee el agente: `.claude/agents/educational/api-design-reviewer.md`
   - Aplica el checklist de "API Design Review Process"
   - Busca inconsistencias en:
     - Nombres de endpoints
     - Formatos de respuesta
     - Códigos de estado
     - Validaciones

---

## 🧪 Testing con Asistencia IA

**Prompt para generar tests**:

```
Necesito tests para mi API FastAPI usando TestClient.

API implementada:
[PEGA TU CÓDIGO]

Requisitos de tests:
1. test_crear_tarea_exitosa:
   - POST /tareas con datos válidos
   - Assert status 201
   - Assert respuesta tiene id, nombre, completada

2. test_crear_tarea_nombre_corto:
   - POST /tareas con nombre de 2 caracteres
   - Assert status 422 (validación falla)

3. test_listar_tareas_vacia:
   - GET /tareas con lista vacía
   - Assert status 200
   - Assert respuesta = []

4. test_obtener_tarea_inexistente:
   - GET /tareas/999
   - Assert status 404

Usa:
- from fastapi.testclient import TestClient
- pytest con fixtures para resetear estado
- Nombres descriptivos de tests

Muestra el código completo de tests.
```

---

## 📋 Entregables de Esta Clase

Al finalizar debes tener:

1. ✅ `api.py` - API FastAPI completa con 5 endpoints CRUD
2. ✅ `test_api.py` - Tests para todos los endpoints
3. ✅ `DISENO_API.md` - Documento de diseño con:
   - Tabla de endpoints
   - Modelos Pydantic
   - Decisiones de diseño
4. ✅ `VALIDACION_AGENTES.md` - Checklist completado con:
   - Revisión FastAPI Design Coach
   - Revisión API Design Reviewer
   - Revisión Python Best Practices Coach

---

## 🎯 Criterios de Éxito

Has completado esta clase exitosamente si:

1. ✅ Tu API tiene 5 endpoints CRUD funcionando
2. ✅ Todos los endpoints siguen convenciones REST
3. ✅ Usas modelos Pydantic con validaciones
4. ✅ Los códigos HTTP son semánticamente correctos
5. ✅ La documentación OpenAPI funciona en /docs
6. ✅ Tienes tests con >80% coverage
7. ✅ Aplicaste los 3 agentes educacionales

---

## 💡 Mejores Prácticas Aprendidas

**Diseño API**:
- 🎯 Diseñar ANTES de implementar
- 🎯 Usar modelos Pydantic para validación automática
- 🎯 Códigos HTTP semánticos (no siempre 200)
- 🎯 Documentación automática con OpenAPI

**Desarrollo con IA**:
- 🎯 Implementar endpoint por endpoint (no todo de golpe)
- 🎯 Validar con agentes educacionales después de cada paso
- 🎯 Probar inmediatamente en /docs
- 🎯 Escribir tests antes de seguir

---

## 🔗 Recursos Adicionales

- 📘 **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/
- 🎓 **REST API Best Practices**: https://restfulapi.net/
- 📚 **Pydantic Docs**: https://docs.pydantic.dev/
- 🤖 **Agentes Usados**:
  - FastAPI Design Coach
  - API Design Reviewer
  - Python Best Practices Coach

---

**Tiempo estimado**: 3 horas

**Siguiente clase**: Clase 2 - Principios SOLID (con AI_WORKFLOW ya existente)
