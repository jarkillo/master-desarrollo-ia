# Ejercicios Prácticos - Error Handling en FastAPI

## Ejercicio 1: Custom Exceptions Básicas ⭐

**Objetivo**: Crear tu primera custom exception y usarla en un endpoint.

**Tareas**:
1. Crea una excepción `ProductoNotFoundError` que herede de `BaseAPIException`
2. Úsala en un endpoint `GET /productos/{id}`
3. Verifica que retorna 404 con formato correcto

**Código base**:
```python
# Completa esta clase
class ProductoNotFoundError(BaseAPIException):
    def __init__(self, producto_id: int):
        # TODO: Implementa el constructor
        pass

@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: int):
    producto = db.get_producto(producto_id)
    if not producto:
        # TODO: Lanza la excepción apropiada
        pass
    return producto
```

---

## Ejercicio 2: Global Exception Handler ⭐⭐

**Objetivo**: Implementar un global exception handler para validación.

**Tareas**:
1. Crea un handler para `RequestValidationError`
2. Formatea errores de Pydantic a tu formato estándar
3. Prueba con datos inválidos

**Test esperado**:
```python
def test_validation_error_format():
    response = client.post("/productos", json={"nombre": ""})
    assert response.status_code == 422
    data = response.json()
    assert "details" in data
    assert data["error_code"] == "VALIDATION_ERROR"
```

---

## Ejercicio 3: Logging Estructurado ⭐⭐

**Objetivo**: Integrar logging en error handling.

**Tareas**:
1. Configura logging con formato JSON
2. Log todos los errores con request_id
3. Implementa rotation de logs

**Verificación**:
- Logs contienen `request_id`, `path`, `error_code`
- Archivo `errors.log` se crea automáticamente
- Formato JSON válido en logs

---

## Ejercicio 4: Sistema Completo de Error Handling ⭐⭐⭐

**Objetivo**: Implementar error handling completo para API de e-commerce.

**Requisitos**:
1. **Custom Exceptions** (mínimo 5):
   - `ProductoNotFoundError`
   - `StockInsuficienteError`
   - `PrecioInvalidoError`
   - `PedidoDuplicadoError`
   - `PaymentFailedError`

2. **Global Handlers**:
   - Validation errors (422)
   - Authentication errors (401)
   - Authorization errors (403)
   - Database errors (500)
   - Unhandled exceptions (500)

3. **Error Response Format**:
```python
{
  "status_code": 422,
  "error_code": "STOCK_INSUFICIENTE",
  "message": "No hay stock suficiente del producto",
  "details": [{
    "field": "cantidad",
    "message": "Stock disponible: 5, solicitado: 10",
    "code": "INSUFFICIENT_STOCK"
  }],
  "timestamp": "2025-11-02T10:30:00Z",
  "path": "/pedidos",
  "request_id": "abc-123"
}
```

4. **Middleware**:
   - Request ID tracking
   - Request/response logging
   - Error metrics

5. **Tests** (mínimo 10 tests):
   - Test cada custom exception
   - Test cada handler
   - Test error format
   - Test logging
   - Test request_id

**Acceptance Criteria**:
- ✅ 5+ custom exceptions implementadas
- ✅ Todos los handlers configurados
- ✅ Error response consistente
- ✅ Logging estructurado funcionando
- ✅ Request ID en headers y logs
- ✅ 10+ tests pasando
- ✅ Coverage > 80% en error handling

---

## Soluciones

Ver carpeta `solutions/` para implementaciones completas de cada ejercicio.

## Validación

Ejecuta los tests:
```bash
pytest tests/test_error_handling.py -v
```

Expected output:
```
test_producto_not_found_returns_404 PASSED
test_validation_error_format PASSED
test_logging_includes_request_id PASSED
test_all_exceptions_have_error_codes PASSED
...
10 passed in 2.3s
```
