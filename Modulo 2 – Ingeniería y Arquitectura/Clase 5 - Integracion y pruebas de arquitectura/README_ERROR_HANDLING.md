# Error Handling Profesional - Guía Rápida

## 📂 Archivos Creados

- **ERROR_HANDLING.md**: Contenido teórico completo (~2 horas)
- **EJERCICIOS_ERROR_HANDLING.md**: 4 ejercicios progresivos
- **api/error_handling/exceptions.py**: Implementación de custom exceptions

## 🚀 Quick Start

### 1. Leer Material Teórico

```bash
cat ERROR_HANDLING.md
```

**Contenido**:
- ¿Por qué error handling profesional?
- Custom exception classes (jerarquía completa)
- Error response format estandarizado
- Global exception handlers
- Logging estructurado
- Middleware de request ID
- Best practices y anti-patrones

### 2. Revisar Implementación

```bash
cat api/error_handling/exceptions.py
```

**Incluye**:
- `BaseAPIException`: Clase base con error_code y context
- `ResourceNotFoundError`, `TareaNotFoundError`
- `InvalidDataError`, `BusinessRuleViolationError`
- `DatabaseError`, `AuthenticationError`, `AuthorizationError`

### 3. Hacer Ejercicios

```bash
cat EJERCICIOS_ERROR_HANDLING.md
```

**Progresión**:
1. ⭐ Custom Exceptions Básicas (30 min)
2. ⭐⭐ Global Exception Handler (45 min)
3. ⭐⭐ Logging Estructurado (45 min)
4. ⭐⭐⭐ Sistema Completo (2-3 horas)

## 🎯 Objetivos de Aprendizaje

Después de este contenido, podrás:

✅ Crear custom exceptions específicas para tu dominio
✅ Implementar global exception handlers en FastAPI
✅ Diseñar error responses estandarizados y consistentes
✅ Integrar logging estructurado con request IDs
✅ Testear error handling correctamente
✅ Aplicar best practices de manejo de errores

## 📊 Error Response Format

```json
{
  "status_code": 404,
  "error_code": "RESOURCE_NOT_FOUND",
  "message": "Tarea no encontrada",
  "details": [{
    "field": "tarea_id",
    "message": "Tarea con ID 123 no existe"
  }],
  "timestamp": "2025-11-02T10:30:00Z",
  "path": "/tareas/123",
  "request_id": "abc-123-def"
}
```

## 🔑 Conceptos Clave

### Custom Exceptions

```python
# Específico y con contexto
raise TareaNotFoundError(tarea_id=123)

# En vez de genérico
raise HTTPException(404, "Not found")
```

### Global Handlers

```python
@app.exception_handler(BaseAPIException)
async def custom_exception_handler(request, exc):
    # Log + formato estandarizado + request_id
    return JSONResponse(status_code=exc.status_code, content=...)
```

### Logging

```python
logger.error(
    f"[{request_id}] {exc.error_code}: {exc.detail}",
    extra={"request_id": request_id, "context": exc.context}
)
```

## 🛠️ Implementación Sugerida

### Paso 1: Custom Exceptions

Copia `api/error_handling/exceptions.py` y adáptalo a tu dominio.

### Paso 2: Error Schemas

Crea Pydantic schemas para error responses (ver ERROR_HANDLING.md sección 3).

### Paso 3: Exception Handlers

Implementa handlers globales (ver ERROR_HANDLING.md sección 4).

### Paso 4: Logging

Configura logging estructurado (ver ERROR_HANDLING.md sección 5).

### Paso 5: Tests

Escribe tests para cada excepción y handler (ver ERROR_HANDLING.md sección 8).

## 📚 Recursos Adicionales

- [FastAPI Exception Handling](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [Python Logging](https://docs.python.org/3/howto/logging.html)

## ✅ Checklist

- [ ] Leí ERROR_HANDLING.md completo
- [ ] Revisé exceptions.py
- [ ] Completé Ejercicio 1 (Custom Exceptions)
- [ ] Completé Ejercicio 2 (Global Handlers)
- [ ] Completé Ejercicio 3 (Logging)
- [ ] Completé Ejercicio 4 (Sistema Completo)
- [ ] Todos mis tests pasan
- [ ] Implementé error handling en mi proyecto

---

**💡 Tip**: El error handling profesional es lo que diferencia una API amateur de una de producción. Invierte tiempo en diseñarlo bien desde el principio.
