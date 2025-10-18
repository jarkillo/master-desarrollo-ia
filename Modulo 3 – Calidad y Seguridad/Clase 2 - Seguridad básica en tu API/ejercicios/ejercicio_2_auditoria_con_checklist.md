# Ejercicio 2: Auditoría paso a paso con checklist

**Duración estimada**: 30 minutos
**Objetivo**: Aprender a auditar código generado por IA de forma sistemática usando un checklist de seguridad.

---

## Parte 1: Código vulnerable para auditar (5 min)

### Contexto

Pediste a la IA que creara un endpoint para actualizar tareas con este prompt débil:

```
Crea un endpoint para actualizar el estado de una tarea
```

### Código generado (vulnerable)

Copia este código en `ejercicios/actualizar_tarea_vulnerable.py`:

```python
from fastapi import FastAPI

app = FastAPI()

# Base de datos simulada
tareas_db = {
    1: {"id": 1, "nombre": "Tarea 1", "user_id": 1, "completada": False},
    2: {"id": 2, "nombre": "Tarea 2", "user_id": 2, "completada": False}
}

@app.put("/tareas/{tarea_id}")
def actualizar_tarea(tarea_id: int, datos: dict):
    """Actualizar tarea - CÓDIGO VULNERABLE"""
    tarea = tareas_db.get(tarea_id)

    if not tarea:
        return {"error": "Tarea no encontrada"}

    # Actualizar todos los campos recibidos
    for campo, valor in datos.items():
        tarea[campo] = valor

    return tarea
```

---

## Parte 2: Aplicar Security Checklist (15 min)

### Instrucciones

Usa el checklist de abajo para auditar el código **línea por línea**.

Para cada item:
- ✅ = Implementado correctamente
- ❌ = No implementado / vulnerable
- ⚠️ = Implementado parcialmente

### Checklist de auditoría de seguridad

#### 1. Validación de entrada (A03: Injection)

- [ ] ¿Usa Pydantic para validar request body?
  - Estado: _____ (✅/❌/⚠️)
  - Problema detectado: ______________________

- [ ] ¿Valida tipos de datos (str, int, bool)?
  - Estado: _____ (✅/❌/⚠️)
  - Problema detectado: ______________________

- [ ] ¿Previene mass assignment (solo campos específicos)?
  - Estado: _____ (✅/❌/⚠️)
  - Problema detectado: ______________________

- [ ] ¿Usa Field() para validación (min_length, max_length)?
  - Estado: _____ (✅/❌/⚠️)
  - Problema detectado: ______________________

#### 2. Control de acceso (A01: Broken Access Control)

- [ ] ¿Requiere autenticación (usa `Depends`)?
  - Estado: _____ (✅/❌/⚠️)
  - Problema detectado: ______________________

- [ ] ¿Valida ownership del recurso?
  - Estado: _____ (✅/❌/⚠️)
  - Problema detectado: ______________________

- [ ] ¿Retorna 403 si usuario no autorizado?
  - Estado: _____ (✅/❌/⚠️)
  - Problema detectado: ______________________

#### 3. Manejo de errores

- [ ] ¿Retorna 404 si recurso no existe (con HTTPException)?
  - Estado: _____ (✅/❌/⚠️)
  - Problema detectado: ______________________

- [ ] ¿Usa HTTPException en vez de retornar dict?
  - Estado: _____ (✅/❌/⚠️)
  - Problema detectado: ______________________

- [ ] ¿Mensajes de error no exponen información sensible?
  - Estado: _____ (✅/❌/⚠️)
  - Problema detectado: ______________________

#### 4. Logging (A09: Security Logging Failures)

- [ ] ¿Registra eventos de actualización?
  - Estado: _____ (✅/❌/⚠️)
  - Problema detectado: ______________________

- [ ] ¿Registra intentos no autorizados?
  - Estado: _____ (✅/❌/⚠️)
  - Problema detectado: ______________________

#### 5. Diseño de API

- [ ] ¿Usa response_model para validar salida?
  - Estado: _____ (✅/❌/⚠️)
  - Problema detectado: ______________________

- [ ] ¿Retorna status code correcto (200)?
  - Estado: _____ (✅/❌/⚠️)
  - Problema detectado: ______________________

### Resultado del checklist

**Total de checks aprobados**: _____ / 14

- **0-5 checks**: Código críticamente vulnerable ⛔
- **6-9 checks**: Código vulnerable ❌
- **10-12 checks**: Código con gaps de seguridad ⚠️
- **13-14 checks**: Código seguro ✅

---

## Parte 3: Implementar correcciones (10 min)

### Instrucciones

Basándote en los problemas detectados, implementa la versión corregida en `ejercicios/actualizar_tarea_seguro.py`.

### Template de código corregido

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)
app = FastAPI()

# Base de datos simulada
tareas_db = {
    1: {"id": 1, "nombre": "Tarea 1", "user_id": 1, "completada": False},
    2: {"id": 2, "nombre": "Tarea 2", "user_id": 2, "completada": False}
}


# TODO 1: Define el modelo Pydantic para validación
class ActualizarTareaRequest(BaseModel):
    # TODO: Agrega campos con validación Field()
    pass


# TODO 2: Define el modelo de respuesta
class TareaResponse(BaseModel):
    # TODO: Define campos de salida
    pass


def obtener_usuario_actual() -> int:
    """Simula autenticación"""
    return 1  # En producción vendría del token


@app.put("/tareas/{tarea_id}", response_model=TareaResponse)
def actualizar_tarea(
    tarea_id: int,
    datos: ActualizarTareaRequest,  # TODO 3: Usar Pydantic
    usuario_actual: int = Depends(obtener_usuario_actual)  # TODO 4: Agregar auth
):
    """Actualizar tarea con validación de ownership y mass assignment protection"""

    # TODO 5: Verificar que tarea existe (404 si no)

    # TODO 6: Validar ownership (403 si no autorizado)

    # TODO 7: Actualizar solo campos permitidos

    # TODO 8: Registrar evento de actualización

    pass
```

---

## Solución completa

<details>
<summary>Haz clic para ver la solución (intenta primero sin mirar)</summary>

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
import logging

logger = logging.getLogger(__name__)
app = FastAPI()

tareas_db = {
    1: {"id": 1, "nombre": "Tarea 1", "user_id": 1, "completada": False},
    2: {"id": 2, "nombre": "Tarea 2", "user_id": 2, "completada": False}
}


class ActualizarTareaRequest(BaseModel):
    """Schema seguro - solo permite campos específicos"""
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    completada: Optional[bool] = None


class TareaResponse(BaseModel):
    id: int
    nombre: str
    user_id: int
    completada: bool


def obtener_usuario_actual() -> int:
    return 1


@app.put("/tareas/{tarea_id}", response_model=TareaResponse)
def actualizar_tarea(
    tarea_id: int,
    datos: ActualizarTareaRequest,
    usuario_actual: int = Depends(obtener_usuario_actual)
):
    """Actualizar tarea con validación de ownership y mass assignment protection"""

    # 1. Verificar que existe
    tarea = tareas_db.get(tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # 2. Validar ownership (A01)
    if tarea["user_id"] != usuario_actual:
        logger.warning(
            f"Intento no autorizado de actualizar tarea {tarea_id} "
            f"por usuario {usuario_actual}",
            extra={
                "event": "actualizacion_no_autorizada",
                "tarea_id": tarea_id,
                "user_id": usuario_actual
            }
        )
        raise HTTPException(status_code=403, detail="Acceso denegado")

    # 3. Actualizar solo campos permitidos (previene mass assignment)
    datos_actualizacion = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizacion.items():
        tarea[campo] = valor

    # 4. Registrar evento
    logger.info(
        f"Tarea {tarea_id} actualizada por usuario {usuario_actual}",
        extra={
            "event": "tarea_actualizada",
            "tarea_id": tarea_id,
            "campos_modificados": list(datos_actualizacion.keys())
        }
    )

    return TareaResponse(**tarea)
```

### Checklist corregido

Ahora el código aprueba **14/14 checks** ✅

</details>

---

## Parte 4: Comparación antes/después (bonus)

Completa esta tabla comparativa:

| Aspecto | Código Vulnerable | Código Corregido |
|---------|-------------------|------------------|
| Validación | `dict` sin validación | Pydantic con `Field()` |
| Autenticación | Sin autenticación | `Depends(obtener_usuario_actual)` |
| Ownership | No valida | Verifica `tarea.user_id == usuario_actual` |
| Mass assignment | Permite cualquier campo | Solo campos específicos |
| Errores | `return {"error": ...}` | `HTTPException` con códigos HTTP |
| Logging | Sin logs | Eventos de seguridad registrados |
| **Vulnerabilidades** | **6 críticas** | **0 vulnerabilidades** |

---

## Reflexión final

**Responde en `ejercicio_2_respuestas.md`**:

1. ¿Cuántos checks aprobó el código vulnerable? _____ / 14

2. ¿Cuál fue la vulnerabilidad más crítica que encontraste?

3. ¿Por qué mass assignment es peligroso?

4. ¿Qué pasaría si un atacante envía `{"user_id": 999}` al endpoint vulnerable?

5. ¿Cómo usarías este checklist en tu workflow diario con IA?

---

## Checklist de completitud

- [ ] Audité el código con el checklist completo (14 items)
- [ ] Identifiqué todas las vulnerabilidades
- [ ] Implementé la versión corregida
- [ ] El código corregido aprueba 14/14 checks
- [ ] Completé la tabla comparativa
- [ ] Respondí las preguntas de reflexión
- [ ] Entiendo por qué cada corrección es necesaria

**¡Excelente trabajo!** Ahora tienes un proceso sistemático para auditar cualquier código generado por IA.
