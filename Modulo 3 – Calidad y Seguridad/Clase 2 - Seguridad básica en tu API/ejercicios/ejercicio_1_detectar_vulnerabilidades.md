# Ejercicio 1: Detectar vulnerabilidades generadas por IA

**Duración estimada**: 30 minutos
**Objetivo**: Aprender a identificar vulnerabilidades en código generado por IA sin contexto de seguridad.

---

## Parte 1: Generar código vulnerable con IA (10 min)

### Instrucciones

1. Usa un prompt **deliberadamente débil** (sin contexto de seguridad):

```
Crea un endpoint FastAPI para eliminar una tarea por ID.
```

2. Copia el código generado por la IA

3. Pégalo en `ejercicios/eliminar_tarea_generado.py`

### Pregunta de reflexión

¿La IA te preguntó sobre seguridad? ¿Mencionó autenticación o autorización? ¿Por qué sí o por qué no?

---

## Parte 2: Auditar con Security Hardening Mentor (10 min)

### Instrucciones

1. Usa este prompt con el código generado:

```
Actúa como Security Hardening Mentor. Audita este endpoint de FastAPI para eliminar tareas.
Identifica vulnerabilidades de seguridad siguiendo OWASP Top 10.

Código:
[pegar código generado en Parte 1]

Proporciona:
1. Lista de vulnerabilidades encontradas con código OWASP (A01, A03, etc.)
2. Nivel de severidad (Crítico/Alto/Medio/Bajo)
3. Explicación del riesgo
4. Escenario de ataque específico
5. Código corregido
```

2. Anota las vulnerabilidades detectadas en `ejercicio_1_respuestas.md`

### Checklist de vulnerabilidades comunes

Compara con esta lista (no mires hasta intentar primero):

- [ ] **A01: Broken Access Control** - No valida ownership
- [ ] **A09: Security Logging** - No registra eliminaciones
- [ ] **A04: Insecure Design** - No usa 204 No Content
- [ ] **Manejo de errores** - No retorna 404 si no existe

¿Cuántas detectaste tú vs el agente?

---

## Parte 3: Implementar corrección (10 min)

### Instrucciones

1. Toma el código corregido sugerido por el agente

2. Implementa la versión segura en `ejercicios/eliminar_tarea_seguro.py`

3. Asegúrate de incluir:
   - ✅ Autenticación con `Depends(obtener_usuario_actual)`
   - ✅ Validación de ownership (403 si no autorizado)
   - ✅ Retorna 404 si tarea no existe
   - ✅ Status code 204 No Content
   - ✅ Logging de evento de eliminación

### Código de referencia

```python
# ejercicios/eliminar_tarea_seguro.py
from fastapi import FastAPI, HTTPException, Depends
import logging

logger = logging.getLogger(__name__)
app = FastAPI()

# Base de datos simulada
tareas_db = {
    1: {"id": 1, "nombre": "Tarea 1", "user_id": 1},
    2: {"id": 2, "nombre": "Tarea 2", "user_id": 2}
}

def obtener_usuario_actual() -> int:
    """Simula autenticación - en producción vendría del token"""
    return 1  # Usuario autenticado


@app.delete("/tareas/{tarea_id}", status_code=204)
def eliminar_tarea(
    tarea_id: int,
    usuario_actual: int = Depends(obtener_usuario_actual)
):
    """
    Eliminar tarea con validación de ownership y auditoría.

    Mitigaciones OWASP implementadas:
    - A01: Validación de ownership
    - A09: Logging de eventos críticos
    - A04: Diseño seguro con códigos HTTP correctos
    """

    # TODO: Implementa las validaciones aquí

    pass  # Reemplaza con tu código
```

---

## Solución completa

<details>
<summary>Haz clic para ver la solución (intenta primero sin mirar)</summary>

```python
@app.delete("/tareas/{tarea_id}", status_code=204)
def eliminar_tarea(
    tarea_id: int,
    usuario_actual: int = Depends(obtener_usuario_actual)
):
    """Eliminar tarea con validación de ownership y auditoría"""

    # 1. Verificar que tarea existe
    tarea = tareas_db.get(tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # 2. Verificar ownership (A01: Broken Access Control)
    if tarea["user_id"] != usuario_actual:
        logger.warning(
            f"Intento no autorizado de eliminar tarea {tarea_id} "
            f"por usuario {usuario_actual}",
            extra={
                "event": "eliminacion_no_autorizada",
                "tarea_id": tarea_id,
                "user_id": usuario_actual
            }
        )
        raise HTTPException(status_code=403, detail="Acceso denegado")

    # 3. Eliminar tarea
    nombre_tarea = tarea["nombre"]
    del tareas_db[tarea_id]

    # 4. Auditoría (A09: Security Logging)
    logger.info(
        f"Tarea {tarea_id} '{nombre_tarea}' eliminada por usuario {usuario_actual}",
        extra={
            "event": "tarea_eliminada",
            "tarea_id": tarea_id,
            "user_id": usuario_actual,
            "tarea_nombre": nombre_tarea
        }
    )

    # 5. 204 No Content (no retornar cuerpo en DELETE)
    return None
```

</details>

---

## Reflexión final

**Responde estas preguntas** (anótalas en `ejercicio_1_respuestas.md`):

1. ¿Qué vulnerabilidades detectaste tú solo antes de usar el agente?
2. ¿Qué vulnerabilidades detectó el agente que tú no viste?
3. ¿Por qué la IA genera código vulnerable si no le das contexto de seguridad?
4. ¿Cómo mejorarías el prompt inicial para generar código seguro desde el principio?

### Prompt mejorado (para la próxima)

```
Crea un endpoint FastAPI para eliminar una tarea por ID.

Requisitos de seguridad:
- Validar ownership (solo el dueño puede eliminar)
- Retornar 404 si no existe, 403 si no autorizado
- Usar status_code=204 para DELETE exitoso
- Registrar evento de eliminación (audit log)
- Manejar errores con HTTPException

Implementa siguiendo OWASP Top 10 (A01 Broken Access Control, A09 Logging).
```

---

## Checklist de completitud

Marca cuando hayas completado cada parte:

- [ ] Generé código con prompt débil (sin seguridad)
- [ ] Audité con Security Hardening Mentor
- [ ] Identifiqué las 4 vulnerabilidades principales
- [ ] Implementé la versión corregida
- [ ] Probé que funciona correctamente
- [ ] Respondí las preguntas de reflexión
- [ ] Creé un prompt mejorado con contexto de seguridad

**¡Felicidades!** Has completado el Ejercicio 1. Ahora sabes cómo detectar y corregir vulnerabilidades en código generado por IA.
