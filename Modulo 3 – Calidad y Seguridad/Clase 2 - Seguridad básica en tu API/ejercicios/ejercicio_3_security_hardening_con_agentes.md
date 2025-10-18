# Ejercicio 3: Security Hardening con agentes especializados

**Duración estimada**: 40 minutos
**Objetivo**: Usar 3 agentes educacionales especializados para endurecer la seguridad de una API completa.

---

## Contexto del ejercicio

Tienes una API de Tareas funcional generada por IA, pero no has aplicado contexto de seguridad. Usarás 3 agentes especializados para detectar y corregir vulnerabilidades.

**Agentes que usarás**:
1. **FastAPI Design Coach** - Anti-patrones de diseño
2. **Python Best Practices Coach** - Patrones inseguros de Python
3. **API Design Reviewer** - Diseño RESTful + OWASP

---

## Parte 1: Código inicial (API vulnerable)

### Instrucciones

Copia este código en `ejercicios/api_vulnerable.py`:

```python
from fastapi import FastAPI
from typing import List

app = FastAPI()

# Base de datos simulada
tareas = []
usuarios = {"user1": "pass123"}  # API Keys en texto plano


@app.post("/tareas")
def crear_tarea(nombre: str):
    """Crear tarea - sin autenticación"""
    tarea = {
        "id": len(tareas) + 1,
        "nombre": nombre,
        "completada": False
    }
    tareas.append(tarea)
    return tarea


@app.get("/tareas")
def listar_tareas(limite: int = 10):
    """Listar tareas - sin validación de límites"""
    return tareas[:limite]


@app.get("/tareas/{tarea_id}")
def obtener_tarea(tarea_id: int):
    """Obtener tarea - sin ownership validation"""
    for tarea in tareas:
        if tarea["id"] == tarea_id:
            return tarea
    return {"error": "No encontrada"}


@app.put("/tareas/{tarea_id}")
def actualizar_tarea(tarea_id: int, datos: dict):
    """Actualizar tarea - mass assignment vulnerable"""
    for tarea in tareas:
        if tarea["id"] == tarea_id:
            for campo, valor in datos.items():
                tarea[campo] = valor
            return tarea
    return {"error": "No encontrada"}


@app.delete("/tareas/{tarea_id}")
def eliminar_tarea(tarea_id: int):
    """Eliminar tarea - sin auditoría"""
    global tareas
    tareas = [t for t in tareas if t["id"] != tarea_id]
    return {"message": "Eliminada"}


def verificar_api_key(api_key: str) -> bool:
    """Verificar API Key - timing attack vulnerable"""
    for user, key in usuarios.items():
        if api_key == key:  # ❌ Comparación insegura
            return True
    return False
```

---

## Parte 2: Auditoría con FastAPI Design Coach (10 min)

### Prompt para el agente

```
Actúa como FastAPI Design Coach. Revisa esta API de tareas completa.
Identifica anti-patrones de diseño que puedan convertirse en vulnerabilidades.

[Pegar código de api_vulnerable.py]

Enfócate en:
- Validación con Pydantic (¿usa dict o BaseModel?)
- Dependency injection (¿usa Depends?)
- Status codes HTTP correctos (¿usa 200/201/204/403/404/422?)
- Response models consistentes
- Async/await donde aplique

Para cada problema detectado, proporciona:
1. Línea de código problemática
2. ¿Por qué es un anti-patrón?
3. ¿Qué vulnerabilidad puede causar?
4. Código corregido
```

### Tus notas

Anota las detecciones del agente en `ejercicio_3_respuestas.md`:

**Problemas detectados por FastAPI Design Coach**:

1. **Problema**: ______________________
   - **Línea**: ______________________
   - **Riesgo**: ______________________
   - **Corrección**: ______________________

2. **Problema**: ______________________
   - **Línea**: ______________________
   - **Riesgo**: ______________________
   - **Corrección**: ______________________

[Continúa con todos los problemas detectados...]

---

## Parte 3: Auditoría con Python Best Practices Coach (10 min)

### Prompt para el agente

```
Actúa como Python Best Practices Coach. Audita este código FastAPI para patrones inseguros de Python.

[Pegar código de api_vulnerable.py]

Busca específicamente:
- Uso de secrets module para comparaciones criptográficas
- Almacenamiento de credenciales (¿hasheadas o texto plano?)
- Type hints completos
- Manejo seguro de excepciones
- Mutabilidad de estructuras de datos globales
- List comprehensions vs loops manuales

Para cada patrón inseguro, explica:
1. ¿Por qué es inseguro?
2. ¿Qué ataque permite?
3. Alternativa segura con código
```

### Tus notas

**Problemas detectados por Python Best Practices Coach**:

1. **Patrón inseguro**: ______________________
   - **Ataque posible**: ______________________
   - **Corrección**: ______________________

2. **Patrón inseguro**: ______________________
   - **Ataque posible**: ______________________
   - **Corrección**: ______________________

[Continúa...]

---

## Parte 4: Auditoría con API Design Reviewer (10 min)

### Prompt para el agente

```
Actúa como API Design Reviewer. Evalúa esta API REST siguiendo principios RESTful y OWASP Top 10.

[Pegar código de api_vulnerable.py]

Evalúa:
- Diseño de endpoints (¿RESTful? ¿Nombrado correcto?)
- Códigos de estado HTTP (¿200/201/204/403/404 usados correctamente?)
- Versionado de API (¿/v1/tareas?)
- Paginación en listados (¿límites validados?)
- Rate limiting
- Autenticación y autorización
- Documentación (OpenAPI/Swagger)

Clasifica cada problema con:
- Severidad: Crítico/Alto/Medio/Bajo
- Código OWASP (A01, A03, A07, etc.)
- Impacto en producción
```

### Tus notas

**Problemas detectados por API Design Reviewer**:

| Problema | Severidad | OWASP | Impacto |
|----------|-----------|-------|---------|
| | | | |
| | | | |
| | | | |

---

## Parte 5: Consolidar correcciones (10 min)

### Instrucciones

1. Revisa las detecciones de los **3 agentes**

2. Crea una lista priorizada de correcciones:

**Críticas (implementar primero)**:
- [ ] ______________________
- [ ] ______________________

**Altas (implementar después)**:
- [ ] ______________________
- [ ] ______________________

**Medias (implementar si hay tiempo)**:
- [ ] ______________________

3. Implementa las correcciones en `ejercicios/api_hardened.py`

---

## Solución: API hardened completa

<details>
<summary>Haz clic para ver la solución (intenta primero sin mirar)</summary>

```python
from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
import secrets
import hashlib
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="API de Tareas Hardened",
    version="1.0.0",
    description="API segura con OWASP Top 10 mitigado"
)

# Base de datos simulada
tareas_db = []
usuarios_db = {
    "user1": {
        "api_key_hash": hashlib.sha256("secure_key_xyz".encode()).hexdigest()
    }
}


# ===== Modelos Pydantic =====

class CrearTareaRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)


class ActualizarTareaRequest(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    completada: Optional[bool] = None


class TareaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    completada: bool
    user_id: int


# ===== Autenticación =====

def verificar_api_key_seguro(api_key: str) -> int:
    """Verificar API Key con timing-safe comparison"""
    api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()

    for user_id, datos in usuarios_db.items():
        # ✅ Timing-safe comparison
        if secrets.compare_digest(api_key_hash, datos["api_key_hash"]):
            return int(user_id.replace("user", ""))

    logger.warning(
        "Intento de autenticación fallido",
        extra={"event": "auth_failed", "api_key_prefix": api_key[:4]}
    )
    raise HTTPException(status_code=401, detail="API Key inválida")


# ===== Endpoints =====

@app.post("/v1/tareas", response_model=TareaResponse, status_code=201)
def crear_tarea(
    datos: CrearTareaRequest,
    usuario_actual: int = Depends(verificar_api_key_seguro)
):
    """Crear tarea con autenticación y validación"""
    tarea = {
        "id": len(tareas_db) + 1,
        "nombre": datos.nombre,
        "descripcion": datos.descripcion,
        "completada": False,
        "user_id": usuario_actual
    }
    tareas_db.append(tarea)

    logger.info(
        f"Tarea {tarea['id']} creada",
        extra={"event": "tarea_creada", "user_id": usuario_actual}
    )

    return tarea


@app.get("/v1/tareas", response_model=List[TareaResponse])
def listar_tareas(
    usuario_actual: int = Depends(verificar_api_key_seguro),
    limite: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Listar tareas con paginación y ownership"""
    tareas_usuario = [t for t in tareas_db if t["user_id"] == usuario_actual]
    return tareas_usuario[offset:offset + limite]


@app.get("/v1/tareas/{tarea_id}", response_model=TareaResponse)
def obtener_tarea(
    tarea_id: int,
    usuario_actual: int = Depends(verificar_api_key_seguro)
):
    """Obtener tarea con ownership validation"""
    tarea = next((t for t in tareas_db if t["id"] == tarea_id), None)

    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    if tarea["user_id"] != usuario_actual:
        logger.warning(
            f"Acceso no autorizado a tarea {tarea_id}",
            extra={"event": "unauthorized_access", "user_id": usuario_actual}
        )
        raise HTTPException(status_code=403, detail="Acceso denegado")

    return tarea


@app.put("/v1/tareas/{tarea_id}", response_model=TareaResponse)
def actualizar_tarea(
    tarea_id: int,
    datos: ActualizarTareaRequest,
    usuario_actual: int = Depends(verificar_api_key_seguro)
):
    """Actualizar tarea con mass assignment protection"""
    tarea = next((t for t in tareas_db if t["id"] == tarea_id), None)

    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    if tarea["user_id"] != usuario_actual:
        raise HTTPException(status_code=403, detail="Acceso denegado")

    # Solo actualizar campos permitidos
    datos_actualizacion = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizacion.items():
        tarea[campo] = valor

    logger.info(
        f"Tarea {tarea_id} actualizada",
        extra={"event": "tarea_actualizada", "user_id": usuario_actual}
    )

    return tarea


@app.delete("/v1/tareas/{tarea_id}", status_code=204)
def eliminar_tarea(
    tarea_id: int,
    usuario_actual: int = Depends(verificar_api_key_seguro)
):
    """Eliminar tarea con audit log"""
    tarea = next((t for t in tareas_db if t["id"] == tarea_id), None)

    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    if tarea["user_id"] != usuario_actual:
        raise HTTPException(status_code=403, detail="Acceso denegado")

    tareas_db.remove(tarea)

    logger.info(
        f"Tarea {tarea_id} eliminada",
        extra={"event": "tarea_eliminada", "user_id": usuario_actual}
    )

    return None
```

</details>

---

## Comparación antes/después

| Aspecto | Antes (Vulnerable) | Después (Hardened) | Agente que detectó |
|---------|--------------------|--------------------|-------------------|
| Autenticación | Sin autenticación | API Keys hasheadas + timing-safe | Python Coach |
| Validación | `dict` sin validación | Pydantic con `Field()` | FastAPI Coach |
| Ownership | No valida | Validación en todos los endpoints | API Reviewer |
| Paginación | Sin límites | `Query(ge=1, le=100)` | FastAPI Coach |
| Status codes | Genéricos | 200/201/204/403/404 correctos | API Reviewer |
| Logging | Sin logs | Eventos de seguridad | API Reviewer |
| Versionado | Sin versión | `/v1/tareas` | API Reviewer |
| **Vulnerabilidades** | **8+ críticas** | **0 vulnerabilidades** | **Los 3 agentes** |

---

## Reflexión final

**Responde en `ejercicio_3_respuestas.md`**:

1. ¿Qué agente detectó más vulnerabilidades? ¿Por qué?

2. ¿Hubo alguna vulnerabilidad que los 3 agentes detectaron?

3. ¿Cómo integrarías estos agentes en tu workflow de desarrollo?

4. Si tuvieras que priorizar usar solo 1 agente, ¿cuál elegirías y por qué?

5. ¿Qué ventaja tiene usar 3 agentes especializados vs uno genérico?

---

## Checklist de completitud

- [ ] Copié el código vulnerable inicial
- [ ] Audité con FastAPI Design Coach
- [ ] Audité con Python Best Practices Coach
- [ ] Audité con API Design Reviewer
- [ ] Consolidé las detecciones de los 3 agentes
- [ ] Implementé la versión hardened
- [ ] Completé la tabla comparativa
- [ ] Respondí las preguntas de reflexión

**¡Impresionante!** Ahora sabes cómo orquestar múltiples agentes especializados para auditoría de seguridad completa.
