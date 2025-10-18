# 📌 Backlog inicial – Mini API de Tareas (Módulo 2)

Este documento recoge las primeras **historias de usuario** y el **backlog técnico** para la API de tareas.

---

## 🧑‍🤝‍🧑 Historias de usuario

1. **Como usuario quiero crear tareas vía API**, para poder gestionarlas desde apps externas.
2. **Como usuario quiero listar mis tareas**, para ver su estado de un vistazo.
3. **Como usuario quiero marcar tareas como completadas**, para llevar control de lo que ya hice.

---

## 📋 Backlog inicial (MVP)

- **Configurar entorno base de FastAPI**
  - Criterios de aceptación:
    - Proyecto inicializado con FastAPI.
    - Endpoint de salud `/health` que devuelve `{status: "ok"}`.

- **Endpoint: Crear tarea**
  - Criterios de aceptación:
    - POST `/tareas` con body `{ "nombre": "texto" }`.
    - Devuelve JSON con `id`, `nombre`, `completada=false`.

- **Endpoint: Listar tareas**
  - Criterios de aceptación:
    - GET `/tareas` devuelve lista de tareas.
    - Incluye estado `completada`.

- **Endpoint: Completar tarea**
  - Criterios de aceptación:
    - PATCH `/tareas/{id}/completar`.
    - Devuelve tarea actualizada con `completada=true`.

- **Tests básicos de integración**
  - Criterios de aceptación:
    - Tests que cubran los 3 endpoints.
    - Ejecutables con `pytest`.

- **ADRs (Architecture Decision Records) iniciales**
  - Criterios de aceptación:
    - Documento ADR explicando por qué usamos FastAPI.
    - Documento ADR sobre cómo persistiremos datos en esta fase (JSON en archivo vs. DB).

---

## ✅ Estado del proyecto

**Completado** (Clase 1):
- ✅ Configurar entorno base de FastAPI
- ✅ Endpoint: Crear tarea (POST /tareas)
- ✅ Endpoint: Listar tareas (GET /tareas)
- ✅ Endpoint: Obtener tarea por ID (GET /tareas/{id})
- ✅ Endpoint: Completar tarea (PATCH /tareas/{id}/completar)
- ✅ Health check (GET /health)
- ✅ Tests básicos con cobertura >70%
- ✅ ADR inicial (docs/adr/001-fastapi.md)

**Pendiente** (Clases 2-3):
- Separar en capas (API, Servicio, Repositorio)
- Aplicar SOLID completo
- Persistencia en JSON
- Inyección de dependencias

---

## 🏗️ Decisiones de Arquitectura

### Almacenamiento en memoria (temporal)

**Decisión**: Usar variables globales `tareas_db` y `contador_id` en `api.py`

**Razón**: Simplicidad para Clase 1 (introducción a FastAPI)

**Consecuencias**:
- ✅ Fácil de entender para principiantes
- ✅ No requiere setup externo
- ❌ Datos se pierden al reiniciar el servidor
- ❌ No es thread-safe (problemas en producción)
- ❌ Mezcla responsabilidades (API + persistencia)

**Próximo paso**: En Clase 2 moveremos esto a `RepositorioMemoria` (patrón Repository)

### Estructura monolítica (api.py único)

**Decisión**: Todo el código en un solo archivo `api.py`

**Razón**: Enfoque pedagógico progresivo (primero funciona, luego se mejora)

**Consecuencias**:
- ✅ Fácil de seguir linealmente
- ✅ Menos archivos = menos confusión inicial
- ❌ Viola Single Responsibility Principle
- ❌ Difícil de testear aisladamente
- ❌ No escala bien

**Próximo paso**: En Clase 2 refactorizaremos aplicando SOLID

---

## 🤖 Prompts de IA utilizados

### Ejercicio 1: IA como Product Owner

```markdown
Rol: Product Owner técnico experimentado en metodologías ágiles.

Contexto: Estoy desarrollando una API REST de tareas con FastAPI. Tengo el MVP definido pero necesito convertirlo en un backlog técnico profesional.

Historias de usuario:
1. Como usuario quiero crear tareas vía API para gestionarlas desde apps externas
2. Como usuario quiero listar mis tareas para ver su estado
3. Como usuario quiero marcar tareas como completadas para llevar control

Tarea: Convierte cada historia en un issue de GitHub con:
- Título en formato: [FEAT] Descripción clara
- Descripción técnica
- Criterios de aceptación (formato Given-When-Then)
- Lista de tareas técnicas (checkboxes)
- Estimación de esfuerzo (S/M/L)

Formato: Markdown, listo para copiar/pegar en GitHub Issues.
```

**Resultado**: 3 issues técnicos con criterios de aceptación claros

---

### Ejercicio 3: Validación con FastAPI Design Coach

```markdown
Revisar el siguiente código FastAPI y proporcionar feedback educativo:

[Código de api/api.py]

Enfócate en:
1. Uso correcto de status codes HTTP
2. Validación Pydantic (¿falta alguna validación importante?)
3. Estructura de responses (¿son consistentes?)
4. Documentación (docstrings y ejemplos en Swagger)
5. Mejores prácticas de FastAPI que no estoy aplicando
```

**Aprendizajes**:
- Status codes correctos: 201 para POST (creación), 200 para GET/PATCH
- HTTP 404 para recursos no encontrados
- HTTP 422 para errores de validación (automático con Pydantic)
- Idempotencia en HTTP: GET/PUT/DELETE son idempotentes, POST no

---

### Ejercicio 4: TDD con IA

**Prompt para generar tests**:
```markdown
Rol: QA Engineer experto en pytest y FastAPI.

Contexto: Estoy aplicando TDD para un endpoint GET /tareas/{tarea_id} que debe:
- Devolver HTTP 200 con la tarea si existe
- Devolver HTTP 404 si no existe

Tarea: Escribe los tests pytest para este endpoint ANTES de implementarlo.

Requisitos:
- Usar TestClient de FastAPI
- 2 tests: caso éxito (200) y caso error (404)
- Nombres descriptivos de tests
- Docstrings explicando qué valida cada test

Formato: Código Python listo para copiar en tests/test_obtener_tarea.py
```

**Ciclo TDD aplicado**:
1. **RED**: Escribir test → Falla (404 porque endpoint no existe)
2. **GREEN**: Implementar código mínimo → Test pasa
3. **REFACTOR**: Revisar con agente educativo → Mejorar código

---

## 📚 Aprendizajes

### Conceptos técnicos

1. **API REST**: Interfaz que permite comunicación entre aplicaciones vía HTTP
2. **Endpoint**: URL específica que realiza una acción (ej: POST /tareas)
3. **Pydantic**: Librería para validación de datos con type hints
4. **FastAPI**: Framework moderno para crear APIs con validación automática
5. **Status Codes HTTP**:
   - 200 OK: Operación exitosa
   - 201 Created: Recurso creado exitosamente
   - 404 Not Found: Recurso no encontrado
   - 422 Unprocessable Entity: Datos inválidos

### Mejores prácticas

1. **TDD**: Escribir tests antes que código
2. **Documentación automática**: Usar docstrings + Pydantic para Swagger
3. **Validación**: Dejar que Pydantic valide (no escribir `if` manuales)
4. **Type hints**: Usar anotaciones de tipos en todas las funciones
5. **ADRs**: Documentar decisiones arquitectónicas importantes

### Anti-patrones detectados

1. ❌ Variables globales para estado (tareas_db, contador_id)
2. ❌ Todo en un solo archivo (viola SRP)
3. ❌ No usar async (FastAPI soporta async nativo)

**Nota**: Estos anti-patrones son intencionales para Clase 1 y se corregirán en Clase 2

---

## 🎯 Próximos pasos (Clase 2)

1. Aplicar **SRP** (Single Responsibility Principle):
   - `api.py` → Solo endpoints HTTP
   - `servicio_tareas.py` → Lógica de negocio
   - `repositorio_memoria.py` → Almacenamiento

2. Implementar **patrón Repository**:
   - Interface `RepositorioTareas` (Protocol)
   - Implementación en memoria
   - Implementación en JSON

3. **Inyección de dependencias**:
   - FastAPI Depends() para inyectar repositorio
   - Facilita testing (mock del repositorio)

4. **Tests mejorados**:
   - Tests de servicio sin API
   - Tests de repositorio sin API ni servicio
   - Mayor cobertura (objetivo: >90%)
