# Security Audit Checklist - Código Generado por IA

**Proyecto**: API de Tareas - Módulo 3 Clase 2
**Tecnologías**: FastAPI 0.115+, Pydantic 2.10+, Python 3.12
**Última actualización**: 2025-01-15
**Versión**: 1.0

---

## 📋 Instrucciones de uso

1. **Genera código con IA** (incluir contexto de seguridad en prompt)
2. **Audita con este checklist** (5-10 min por endpoint)
3. **Marca** ✅ si aprueba, ❌ si falla, ⚠️ si parcial
4. **Si <40/50 checks**, NO commit hasta corregir
5. **Re-audita** con agentes especializados (FastAPI Coach, Python Coach, API Reviewer)

---

## ⚠️ Checks Críticos (bloquean commit si fallan)

Estos 10 checks **DEBEN** pasar siempre. Si **cualquiera** falla → 🚫 **NO COMMIT**

1. [ ] Endpoints requieren autenticación (`Depends(obtener_usuario_actual)`)
2. [ ] Validación de ownership en GET/PUT/DELETE (`tarea.user_id == usuario_actual`)
3. [ ] Pydantic BaseModel para validación de entrada (no `dict`)
4. [ ] API Keys almacenadas hasheadas (SHA-256 mínimo)
5. [ ] `secrets.compare_digest` para comparaciones (no `==`)
6. [ ] Logging de eventos críticos (creación, actualización, eliminación)
7. [ ] `HTTPException` para errores (no `return {"error": ...}`)
8. [ ] Status codes HTTP correctos (200/201/204/403/404/422)
9. [ ] No usa `eval()`, `exec()`, `pickle.load()`, `compile()`
10. [ ] `safety check` sin vulnerabilidades críticas/altas

---

## 1️⃣ Categoría 1: Validación de Entrada (A03: Injection)

**Severidad**: Alta | **Checks**: 8 | **OWASP**: A03

- [ ] Request bodies usan `Pydantic BaseModel` (no `dict`)
- [ ] Campos tienen `Field()` con `min_length`, `max_length`, `ge`, `le`
- [ ] Query params usan `Query()` con validación (`ge=1, le=100`)
- [ ] No usa `eval()`, `exec()`, `compile()`, `__import__()`
- [ ] Queries SQL usan ORM (SQLAlchemy) - no f-strings
- [ ] No deserializa con `pickle.load()` (usar JSON + Pydantic)
- [ ] Valida tipos de datos explícitamente (`int`, `str`, `bool`)
- [ ] Previene mass assignment (solo campos específicos en schema)

**Ejemplo de código seguro**:
```python
# ✅ SEGURO
from pydantic import BaseModel, Field

class CrearTareaRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: str | None = Field(None, max_length=500)

@app.post("/tareas")
def crear_tarea(datos: CrearTareaRequest): pass
```

**Código vulnerable a evitar**:
```python
# ❌ VULNERABLE
@app.post("/tareas")
def crear_tarea(datos: dict):  # No valida tipos ni contenido
    pass
```

---

## 2️⃣ Categoría 2: Control de Acceso (A01: Broken Access Control)

**Severidad**: Crítica | **Checks**: 6 | **OWASP**: A01

- [ ] Endpoints protegidos usan `Depends(obtener_usuario_actual)`
- [ ] Valida ownership en GET/PUT/DELETE (`tarea.user_id == usuario_actual`)
- [ ] Retorna **403 Forbidden** si no autorizado (no 404)
- [ ] Retorna **404 Not Found** si recurso no existe
- [ ] No expone información de otros usuarios (filtrar por `user_id`)
- [ ] Listados filtran por `user_id` (no retornan todo)

**Ejemplo de código seguro**:
```python
# ✅ SEGURO
@app.get("/tareas/{tarea_id}")
def obtener_tarea(
    tarea_id: int,
    usuario_actual: int = Depends(obtener_usuario_actual)
):
    tarea = servicio.obtener(tarea_id)

    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # Validar ownership
    if tarea.user_id != usuario_actual:
        raise HTTPException(status_code=403, detail="Acceso denegado")

    return tarea
```

**Código vulnerable a evitar**:
```python
# ❌ VULNERABLE
@app.get("/tareas/{tarea_id}")
def obtener_tarea(tarea_id: int):  # Sin autenticación ni ownership
    return servicio.obtener(tarea_id)
```

---

## 3️⃣ Categoría 3: Autenticación (A07: Authentication Failures)

**Severidad**: Crítica | **Checks**: 7 | **OWASP**: A07

- [ ] API Keys almacenadas hasheadas (SHA-256 mínimo)
- [ ] Comparación con `secrets.compare_digest()` (no `==`)
- [ ] API Keys generadas con `secrets.token_urlsafe(32)` (32+ bytes)
- [ ] API Keys de 32+ caracteres (256 bits mínimo)
- [ ] Secrets en `.env` (no hardcodeados en código)
- [ ] API Keys con expiración (recomendado: 30-90 días)
- [ ] Logging de intentos de autenticación fallidos

**Ejemplo de código seguro**:
```python
# ✅ SEGURO
import secrets
import hashlib

def verificar_api_key(api_key: str = Depends(obtener_api_key_header)) -> int:
    # Hashear API Key recibida
    api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()

    # Obtener hash almacenado del usuario
    usuario = repositorio.obtener_por_api_key_hash(api_key_hash)

    if not usuario:
        logger.warning("Intento de autenticación fallido")
        raise HTTPException(status_code=401, detail="API Key inválida")

    # Timing-safe comparison
    if not secrets.compare_digest(api_key_hash, usuario.api_key_hash):
        raise HTTPException(status_code=401, detail="API Key inválida")

    return usuario.id
```

**Código vulnerable a evitar**:
```python
# ❌ VULNERABLE
API_KEYS = {"user1": "abc123"}  # Texto plano, clave débil

def verificar_api_key(api_key: str) -> int:
    if api_key == "abc123":  # ❌ Comparación insegura, vulnerable a timing attacks
        return 1
    raise HTTPException(401)
```

---

## 4️⃣ Categoría 4: Logging y Monitoreo (A09: Security Logging Failures)

**Severidad**: Alta | **Checks**: 6 | **OWASP**: A09

- [ ] Logging de autenticación fallida (con `logger.warning`)
- [ ] Logging de accesos no autorizados - 403 (con contexto)
- [ ] Logging de eventos críticos (creación, actualización, eliminación)
- [ ] Formato estructurado con `extra={"event": "nombre", ...}`
- [ ] No registra información sensible (passwords, API Keys completas)
- [ ] Logs van a sistema centralizado (Sentry, ELK, CloudWatch)

**Ejemplo de código seguro**:
```python
# ✅ SEGURO
import logging

logger = logging.getLogger(__name__)

@app.delete("/tareas/{tarea_id}", status_code=204)
def eliminar_tarea(tarea_id: int, usuario_actual: int = Depends(auth)):
    tarea = servicio.obtener(tarea_id)

    if tarea.user_id != usuario_actual:
        # Logging de intento no autorizado
        logger.warning(
            f"Intento no autorizado de eliminar tarea {tarea_id}",
            extra={
                "event": "eliminacion_no_autorizada",
                "tarea_id": tarea_id,
                "user_id": usuario_actual
            }
        )
        raise HTTPException(403)

    servicio.eliminar(tarea_id)

    # Audit log de eliminación
    logger.info(
        f"Tarea {tarea_id} eliminada",
        extra={
            "event": "tarea_eliminada",
            "tarea_id": tarea_id,
            "user_id": usuario_actual
        }
    )

    return None
```

**Código vulnerable a evitar**:
```python
# ❌ VULNERABLE
@app.delete("/tareas/{tarea_id}")
def eliminar_tarea(tarea_id: int):
    servicio.eliminar(tarea_id)  # Sin logging - imposible auditar
    return {"message": "Eliminada"}
```

---

## 5️⃣ Categoría 5: Manejo de Errores

**Severidad**: Media | **Checks**: 5

- [ ] Usa `HTTPException` (no `return {"error": ...}`)
- [ ] Status codes HTTP correctos (200/201/204/403/404/422)
- [ ] Mensajes de error genéricos (no exponen stack traces)
- [ ] No expone información sensible en errores
- [ ] Sentry/Monitoring captura excepciones en producción

**Ejemplo de código seguro**:
```python
# ✅ SEGURO
from fastapi import HTTPException

@app.get("/tareas/{tarea_id}")
def obtener_tarea(tarea_id: int, usuario_actual: int = Depends(auth)):
    tarea = servicio.obtener(tarea_id)

    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    if tarea.user_id != usuario_actual:
        # Mensaje genérico - no expone detalles
        raise HTTPException(status_code=403, detail="Acceso denegado")

    return tarea
```

**Código vulnerable a evitar**:
```python
# ❌ VULNERABLE
@app.get("/tareas/{tarea_id}")
def obtener_tarea(tarea_id: int):
    tarea = servicio.obtener(tarea_id)
    if not tarea:
        return {"error": "No encontrada"}  # ❌ No usa HTTPException

    return tarea
```

---

## 6️⃣ Categoría 6: Integridad de Software (A08: Software/Data Integrity Failures)

**Severidad**: Alta | **Checks**: 5 | **OWASP**: A08

- [ ] `requirements.txt` con versiones pinneadas (`fastapi==0.115.0`)
- [ ] `safety check` sin vulnerabilidades críticas/altas
- [ ] Dependencias actualizadas (últimos 6 meses)
- [ ] No instala paquetes desde fuentes no confiables
- [ ] Builds reproducibles (mismo `requirements.txt` → mismo resultado)

**Ejemplo de requirements.txt seguro**:
```txt
# ✅ SEGURO - Versiones pinneadas y auditadas
# Auditado con `safety check` el 2025-01-15

fastapi==0.115.0
uvicorn[standard]==0.32.0
pydantic==2.10.3
python-dotenv==1.0.1
sqlalchemy==2.0.36
```

**Requirements vulnerable a evitar**:
```txt
# ❌ VULNERABLE
fastapi  # Sin versión - puede instalar versión vulnerable
uvicorn
pydantic
```

---

## 7️⃣ Categoría 7: Diseño de API (REST + Seguridad)

**Severidad**: Media | **Checks**: 7

- [ ] Versionado de API (`/v1/tareas`, `/v2/tareas`)
- [ ] Paginación en listados (`limite`, `offset` con validación)
- [ ] Validación de límites (`Query(ge=1, le=100)`)
- [ ] `response_model` para validar salida
- [ ] Rate limiting implementado (recomendado: 100 req/min)
- [ ] CORS configurado correctamente (no `allow_origins=["*"]` en producción)
- [ ] Documentación OpenAPI/Swagger actualizada y accesible

**Ejemplo de código seguro**:
```python
# ✅ SEGURO
from fastapi import Query

@app.get("/v1/tareas", response_model=ListaTareasResponse)
def listar_tareas(
    usuario_actual: int = Depends(auth),
    limite: int = Query(10, ge=1, le=100),  # Validación de límites
    offset: int = Query(0, ge=0)
):
    tareas = servicio.listar_por_usuario(
        usuario_actual,
        limite=limite,
        offset=offset
    )

    return {
        "tareas": tareas,
        "total": len(tareas),
        "limite": limite,
        "offset": offset
    }
```

**Código vulnerable a evitar**:
```python
# ❌ VULNERABLE
@app.get("/tareas")
def listar_tareas(limite: int = 10):  # Sin validación de límite máximo
    return servicio.listar()[:limite]  # Permite limite=9999999 → DoS
```

---

## 8️⃣ Categoría 8: Configuración Segura (A05: Security Misconfiguration)

**Severidad**: Alta | **Checks**: 6 | **OWASP**: A05

- [ ] Secrets en `.env` (no hardcodeados en código)
- [ ] `.env` en `.gitignore` (no commitear secrets)
- [ ] `.env.template` con valores de ejemplo (sin secrets reales)
- [ ] Validación de variables de entorno al inicio (con `python-dotenv`)
- [ ] `DEBUG=False` en producción
- [ ] No expone stack traces en producción (Sentry captura errores)

**Ejemplo de configuración segura**:
```python
# ✅ SEGURO
# .env
JWT_SECRET=generated_with_secrets_token_hex_32
DATABASE_URL=postgresql://user:pass@localhost/db
MODE=production
DEBUG=false

# api/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwt_secret: str
    database_url: str
    mode: str = "production"
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()  # Valida que todas las variables existan
```

**Configuración vulnerable a evitar**:
```python
# ❌ VULNERABLE
JWT_SECRET = "secret123"  # Hardcodeado en código
DEBUG = True  # Debug en producción expone stack traces
```

---

## 📊 Sistema de Scoring

**Total de checks**: 50

### Clasificación de seguridad

Marca todos los checks completados y calcula tu porcentaje:

- **40-50 checks (80-100%)**: ✅ **Código seguro** - OK para commit
- **30-39 checks (60-79%)**: ⚠️ **Gaps de seguridad** - Corregir antes de commit
- **20-29 checks (40-59%)**: ❌ **Código vulnerable** - NO commit
- **0-19 checks (<40%)**: ⛔ **Críticamente vulnerable** - Reescribir con contexto de seguridad

### Checks aprobados

**Total**: _____ / 50
**Porcentaje**: _____ %
**Clasificación**: _______________

---

## 🚨 Acciones Recomendadas

Basándote en tu resultado:

### ✅ Seguro (40-50 checks)

1. OK para commit
2. Auditar con agentes para validación adicional (FastAPI Design Coach, Python Best Practices Coach)
3. Ejecutar tests de seguridad (`pytest tests/test_seguridad.py`)
4. Crear PR para revisión

### ⚠️ Gaps (30-39 checks)

1. Corregir gaps antes de commit
2. Usar agentes especializados para identificar problemas restantes
3. Re-auditar con este checklist después de correcciones
4. Documentar decisiones en `notes.md`

### ❌ Vulnerable (20-29 checks)

1. **NO commit** hasta corregir
2. Usar prompt mejorado con contexto de seguridad
3. Re-generar código con IA incluyendo requisitos de seguridad
4. Seguir workflow: Prompt → Generar → Auditar → Corregir

### ⛔ Críticamente vulnerable (<20 checks)

1. **Reescribir completamente**
2. Revisar prompt usado - falta contexto de seguridad
3. Consultar `prompts_seguridad.md` para ejemplos de prompts seguros
4. Seguir patrón: Generar con contexto → Auditar → Corregir → Re-auditar

---

## 🔄 Workflow Recomendado

```
1. Prompt con contexto de seguridad (usar prompts_seguridad.md)
   ↓
2. IA genera código
   ↓
3. Auditar con SECURITY_CHECKLIST.md (este archivo)
   ↓
4. ¿Checks críticos OK? (10/10)
   ├─ No → Corregir vulnerabilidades → Volver a paso 3
   └─ Sí → Continuar
   ↓
5. Auditar con agentes especializados
   - FastAPI Design Coach
   - Python Best Practices Coach
   - API Design Reviewer
   ↓
6. ¿Agentes detectaron vulnerabilidades?
   ├─ Sí → Corregir → Volver a paso 3
   └─ No → Continuar
   ↓
7. Ejecutar tests de seguridad
   ↓
8. Commit código seguro
```

---

## 📝 Notas de auditoría

**Fecha de auditoría**: _____________
**Auditado por**: _____________
**Archivo auditado**: _____________

**Vulnerabilidades encontradas**:

1. _______________________________________
   - **Severidad**: Crítica / Alta / Media / Baja
   - **OWASP**: _______
   - **Corrección aplicada**: Sí / No

2. _______________________________________

3. _______________________________________

**Agentes usados**:
- [ ] FastAPI Design Coach
- [ ] Python Best Practices Coach
- [ ] API Design Reviewer

**Herramientas de seguridad**:
- [ ] `safety check` ejecutado (sin vulnerabilidades críticas)
- [ ] `bandit -r api/ -ll` ejecutado (sin issues altos)
- [ ] Tests de seguridad pasando

---

## 📚 Referencias

- [OWASP API Security Top 10](https://owasp.org/API-Security/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Python secrets module](https://docs.python.org/3/library/secrets.html)
- [Pydantic Field validation](https://docs.pydantic.dev/latest/concepts/fields/)

---

**Última actualización**: 2025-01-15
**Versión**: 1.0
**Mantenido por**: Estudiante del Módulo 3 Clase 2
