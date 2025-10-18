# Notes - Clase 2: Seguridad básica + OWASP Top 10 + Auditoría con IA

**Fecha**: 2025-01-15
**Módulo**: 3 - Calidad y Seguridad
**Clase**: 2 - Seguridad básica en tu API
**Duración**: 7 horas (1h fundamentos + 3h OWASP + 2h auditoría IA + 1h proyecto final)

---

## Aprendizajes Clave

### 1. La IA genera código funcional, no siempre seguro

**Descubrimiento crítico**: Cuando pides a la IA que genere código sin contexto de seguridad, produce código **funcionalmente correcto** pero **vulnerable**.

**Ejemplo**:
```
Prompt débil: "Crea un endpoint para eliminar una tarea"

IA genera:
@app.delete("/tareas/{id}")
def eliminar(id: int):
    servicio.eliminar(id)  # ✅ Funciona, ❌ Inseguro
    return {"message": "Eliminada"}
```

**Vulnerabilidades generadas**:
- A01: Sin validación de ownership
- A07: Sin autenticación
- A09: Sin audit log
- A04: No usa 204 No Content

**Lección aprendida**: **Siempre** incluir contexto de seguridad en prompts.

---

### 2. OWASP Top 10 para APIs es tu mapa de vulnerabilidades

**Top 5 vulnerabilidades críticas para APIs FastAPI**:

| OWASP | Vulnerabilidad | Frecuencia en código IA | Mitigación |
|-------|----------------|------------------------|------------|
| A01 | Broken Access Control | 90% | Validar ownership |
| A03 | Injection | 70% | Pydantic con Field() |
| A07 | Authentication Failures | 80% | API Keys hasheadas + secrets.compare_digest |
| A08 | Software Integrity | 50% | Safety check + versiones pinneadas |
| A09 | Security Logging | 95% | Logging estructurado de eventos |

**Patrón detectado**: La IA asume autenticación pero **NO ownership**. El 90% de endpoints generados permiten que Usuario A acceda a recursos de Usuario B.

---

### 3. El patrón "Generar → Auditar → Corregir" es esencial

**Workflow de seguridad con IA**:

```
1. Prompt con contexto de seguridad
   ↓
2. IA genera código
   ↓
3. Auditar con SECURITY_CHECKLIST.md
   ↓
4. ¿Checks críticos OK? (10/10)
   ├─ No → Corregir → Volver a paso 3
   └─ Sí → Continuar
   ↓
5. Auditar con agentes especializados
   ↓
6. Corregir vulnerabilidades detectadas
   ↓
7. Re-auditar
   ↓
8. Commit código seguro
```

**Métrica de éxito**: Si código aprueba **<40/50 checks** en primer intento, tu prompt necesita más contexto de seguridad.

---

### 4. Agentes especializados detectan más que un agente genérico

**Experimento realizado**: Audité el mismo código con:
- 1 agente genérico → Detectó 5 vulnerabilidades
- 3 agentes especializados → Detectaron 12 vulnerabilidades

**Agentes especializados usados**:
1. **FastAPI Design Coach**: Anti-patrones de diseño (dict, falta Depends, status codes)
2. **Python Best Practices Coach**: Patrones inseguros (==, no secrets module, type hints)
3. **API Design Reviewer**: Diseño RESTful + OWASP (versionado, paginación, rate limiting)

**Lección**: Usa múltiples agentes especializados para auditoría exhaustiva.

---

## Decisiones de Diseño

### Por qué API Keys hasheadas (A07)

**Decisión**: Almacenar API Keys como `SHA-256(api_key)` en vez de texto plano.

**Alternativas consideradas**:
1. ❌ Texto plano: Si DB se filtra, todas las claves quedan expuestas
2. ❌ Encryption reversible: Requiere gestión de encryption keys, complejidad innecesaria
3. ✅ Hashing (SHA-256): Irreversible, simple, efectivo

**Implementación**:
```python
import hashlib
import secrets

# Generar API Key
api_key = secrets.token_urlsafe(32)  # 43 caracteres, 256 bits

# Almacenar hash
api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()

# Verificar (timing-safe)
if secrets.compare_digest(api_key_hash, stored_hash):
    # ✅ Autenticado
```

**Por qué secrets.compare_digest**:
- `==` es vulnerable a **timing attacks** (retorna inmediatamente al encontrar diferencia)
- `secrets.compare_digest` toma tiempo constante (mismo tiempo si coincide o no)
- Previene que atacante deduzca caracteres correctos midiendo tiempos de respuesta

---

### Por qué 403 vs 404 en ownership (A01)

**Decisión**: Retornar **403 Forbidden** (no 404) cuando usuario intenta acceder a recurso ajeno.

**Escenario**:
```python
# Usuario 2 intenta acceder a tarea de Usuario 1
GET /tareas/123
Authorization: api_key_usuario_2
```

**Opciones**:
1. ❌ Retornar 404: "Tarea no encontrada"
   - Problema: Information disclosure - atacante sabe que tarea existe pero no le pertenece
   - Permite enumeración de recursos

2. ✅ Retornar 403: "Acceso denegado"
   - Claro y directo: "El recurso existe pero no tienes permiso"
   - No expone existencia de recursos ajenos

**Excepción**: Si recurso NO existe → 404 (antes de verificar ownership)

```python
# ✅ Implementación correcta
tarea = servicio.obtener(id)

if not tarea:
    raise HTTPException(404)  # Primero verificar existencia

if tarea.user_id != usuario_actual:
    raise HTTPException(403)  # Luego verificar ownership
```

---

### Por qué Pydantic sobre dict (A03)

**Decisión**: Usar `Pydantic BaseModel` para todos los request bodies (no `dict`).

**Comparación**:

| Aspecto | dict | Pydantic BaseModel |
|---------|------|-------------------|
| Validación de tipos | ❌ Manual | ✅ Automática |
| Valores por defecto | ❌ Manual | ✅ Field(default=...) |
| Límites (min/max) | ❌ Manual | ✅ Field(ge=1, le=100) |
| Mass assignment | ❌ Vulnerable | ✅ Solo campos definidos |
| Documentación | ❌ No auto-generada | ✅ OpenAPI/Swagger |
| Type hints | ❌ No | ✅ Sí |

**Ejemplo de mass assignment**:
```python
# ❌ VULNERABLE con dict
@app.put("/tareas/{id}")
def actualizar(id: int, datos: dict):
    for campo, valor in datos.items():
        tarea[campo] = valor  # ❌ Permite cambiar user_id, permisos, etc.


# ✅ SEGURO con Pydantic
class ActualizarTareaRequest(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=100)
    completada: bool | None = None
    # NO incluye user_id, created_at, etc.

@app.put("/tareas/{id}")
def actualizar(id: int, datos: ActualizarTareaRequest):
    datos_actualizacion = datos.model_dump(exclude_unset=True)
    # ✅ Solo actualiza campos permitidos
```

---

### Por qué logging estructurado (A09)

**Decisión**: Usar formato estructurado con `extra={"event": ...}` en vez de solo mensajes.

**Comparación**:

```python
# ❌ Logging no estructurado
logger.info(f"Usuario {user_id} eliminó tarea {tarea_id}")

# ✅ Logging estructurado
logger.info(
    f"Tarea {tarea_id} eliminada",
    extra={
        "event": "tarea_eliminada",
        "tarea_id": tarea_id,
        "user_id": user_id,
        "timestamp": datetime.now().isoformat()
    }
)
```

**Ventajas del logging estructurado**:
1. **Filtrable**: Buscar todos los eventos "tarea_eliminada"
2. **Agregable**: Contar cuántas eliminaciones por usuario
3. **Alertable**: Trigger si >10 eliminaciones en 1 minuto
4. **Compatible con ELK, Sentry**: Los sistemas de monitoreo entienden JSON
5. **Auditabile**: Compliance (GDPR, SOX, HIPAA) requiere audit trails estructurados

---

## Patrones Anti-pattern → Corrección

### Anti-pattern 1: Comparación insegura de API Keys

```python
# ❌ VULNERABLE a timing attacks
if api_key == stored_key:
    return user_id

# ✅ TIMING-SAFE
if secrets.compare_digest(api_key, stored_key):
    return user_id
```

**Por qué `==` es vulnerable**:
- Compara carácter por carácter
- Retorna inmediatamente al encontrar diferencia
- Atacante mide tiempos:
  - "a" vs "secret" → 0.001ms (falla en primer carácter)
  - "s" vs "secret" → 0.002ms (primer carácter correcto!)
  - Continúa deduciendo caracteres

---

### Anti-pattern 2: Sin validación de límites en paginación

```python
# ❌ VULNERABLE a DoS
@app.get("/tareas")
def listar(limite: int = 10):
    return tareas[:limite]  # Permite limite=999999999 → OOM

# ✅ SEGURO con validación
from fastapi import Query

@app.get("/tareas")
def listar(limite: int = Query(10, ge=1, le=100)):
    return tareas[:limite]  # Máximo 100 resultados
```

---

### Anti-pattern 3: return {"error": ...} en vez de HTTPException

```python
# ❌ ANTI-PATTERN
@app.get("/tareas/{id}")
def obtener(id: int):
    tarea = servicio.obtener(id)
    if not tarea:
        return {"error": "No encontrada"}  # ❌ Status code 200
    return tarea

# ✅ CORRECTO
@app.get("/tareas/{id}")
def obtener(id: int):
    tarea = servicio.obtener(id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea
```

**Por qué HTTPException**:
- Status code correcto (404, no 200)
- OpenAPI/Swagger documenta automáticamente
- Clientes pueden manejar errores con try/catch
- Logs registran status code correcto

---

## Prompts Efectivos Usados

### Prompt 1: Generar endpoint seguro

**Prompt usado**:
```
Crea un endpoint FastAPI DELETE para eliminar una tarea por ID.

Requisitos de seguridad:
- Validar ownership (solo el dueño puede eliminar)
- Retornar 404 si no existe, 403 si no autorizado
- Usar status_code=204 para DELETE exitoso
- Registrar evento de eliminación (audit log)
- Manejar errores con HTTPException
```

**Resultado**: Código generado aprobó 48/50 checks (96%). Solo faltó rate limiting y versionado de API.

---

### Prompt 2: Auditar código vulnerable

**Prompt usado**:
```
Actúa como Security Hardening Mentor. Audita este endpoint para vulnerabilidades OWASP Top 10.

[Código vulnerable]

Proporciona:
1. Lista de vulnerabilidades (código OWASP, severidad)
2. Escenario de ataque
3. Código corregido
```

**Resultado**: Agente detectó 8 vulnerabilidades (vs 3 que detecté manualmente). Incluye mass assignment y timing attacks que no había considerado.

---

## Vulnerabilidades Detectadas en Ejercicios

### Ejercicio 1: Eliminar tarea

**Código generado por IA** (prompt débil):
```python
@app.delete("/tareas/{id}")
def eliminar(id: int):
    servicio.eliminar(id)
    return {"message": "Eliminada"}
```

**Vulnerabilidades detectadas** (4):
1. **A01 (Crítico)**: Sin ownership validation
2. **A07 (Crítico)**: Sin autenticación
3. **A09 (Alto)**: Sin audit log
4. **A04 (Medio)**: No usa 204 No Content

**Código corregido** (aprueba 50/50 checks):
```python
@app.delete("/tareas/{id}", status_code=204)
def eliminar(id: int, usuario: int = Depends(auth)):
    tarea = servicio.obtener(id)
    if not tarea:
        raise HTTPException(404)
    if tarea.user_id != usuario:
        logger.warning("Intento no autorizado", extra={"event": "eliminacion_no_autorizada"})
        raise HTTPException(403)

    servicio.eliminar(id)
    logger.info("Tarea eliminada", extra={"event": "tarea_eliminada", "tarea_id": id})
    return None
```

---

### Ejercicio 2: Actualizar tarea

**Código generado** (mass assignment vulnerable):
```python
@app.put("/tareas/{id}")
def actualizar(id: int, datos: dict):
    for campo, valor in datos.items():
        tarea[campo] = valor  # ❌ Permite cambiar user_id
```

**Vulnerabilidades**: 6 críticas (A01, A03, A07)

**Corrección con Pydantic**:
```python
class ActualizarTareaRequest(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=100)
    completada: bool | None = None

@app.put("/tareas/{id}")
def actualizar(id: int, datos: ActualizarTareaRequest, usuario: int = Depends(auth)):
    # ... validaciones ...
    datos_actualizacion = datos.model_dump(exclude_unset=True)
    # ✅ Solo actualiza campos permitidos
```

---

## Métricas de Aprendizaje

### Antes de la clase

- **Conocimiento OWASP Top 10**: 20% (solo sabía de SQL injection)
- **Uso de Pydantic**: Básico (sin Field())
- **Auditoría de código IA**: 0% (asumía que IA genera código seguro)
- **Logging de seguridad**: 10% (solo print())

### Después de la clase

- **Conocimiento OWASP Top 10**: 80% (puedo identificar y mitigar las 5 críticas)
- **Uso de Pydantic**: Avanzado (Field(), mass assignment prevention)
- **Auditoría de código IA**: 70% (checklist sistemático + agentes)
- **Logging de seguridad**: 75% (formato estructurado, audit logs)

**Velocidad de auditoría**:
- Antes: No auditaba código generado por IA
- Ahora: 5-10 min por endpoint con SECURITY_CHECKLIST.md

---

## Herramientas y Recursos Utilizados

### Herramientas de auditoría

1. **Safety** - Auditoría de dependencias
   ```bash
   safety check --json
   ```
   Detectó 2 vulnerabilidades en versiones antiguas de requests y pydantic.

2. **Bandit** - Análisis estático de seguridad
   ```bash
   bandit -r api/ -ll
   ```
   Detectó uso de `eval()` en un ejemplo vulnerable.

3. **SECURITY_CHECKLIST.md** - Auditoría manual
   - 50 checks en 8 categorías
   - Tiempo: 5-10 min por endpoint
   - Efectividad: Detecta 90%+ de vulnerabilidades comunes

### Agentes educacionales

1. **FastAPI Design Coach**
   - Detectó: dict sin validación, falta Depends, status codes incorrectos
   - Utilidad: ⭐⭐⭐⭐⭐ (5/5)

2. **Python Best Practices Coach**
   - Detectó: == vs secrets.compare_digest, falta type hints, exceptions genéricas
   - Utilidad: ⭐⭐⭐⭐ (4/5)

3. **API Design Reviewer**
   - Detectó: falta versionado, paginación sin límites, CORS inseguro
   - Utilidad: ⭐⭐⭐⭐⭐ (5/5)

**Recomendación**: Usar los 3 agentes en paralelo para auditoría exhaustiva.

---

## Próximos Pasos

### Para Clase 3 (JWT + Autenticación Avanzada)

**Preparación**:
- [ ] Revisar JWT specification (RFC 7519)
- [ ] Estudiar refresh tokens pattern
- [ ] Leer sobre bcrypt para password hashing
- [ ] Entender OAuth 2.0 flows

**Preguntas para Clase 3**:
1. ¿Cuándo usar API Keys vs JWT?
2. ¿Cómo rotar refresh tokens de forma segura?
3. ¿JWT debe incluirse en header o cookie?

---

### Aplicar en proyectos reales

**Plan de acción**:
1. **Semana 1**: Auditar proyecto actual con SECURITY_CHECKLIST.md
2. **Semana 2**: Implementar correcciones de vulnerabilidades críticas
3. **Semana 3**: Agregar logging estructurado de seguridad
4. **Semana 4**: Integrar Safety + Bandit en CI/CD

**Métrica de éxito**: Proyecto aprueba 45/50 checks (90%) en auditoría de seguridad.

---

## Reflexiones Finales

### Cambio de mindset

**Antes**: "La IA genera código correcto, solo debo copiarlo"

**Ahora**: "La IA genera código funcional, yo debo auditarlo y asegurarme que es seguro"

### Lección más importante

**Seguridad NO es una feature que se agrega al final**. Es una **mentalidad** que aplicas desde el primer prompt.

### Quote favorito de la clase

> "No hay código seguro por defecto. Solo código auditado sistemáticamente."

---

**Última actualización**: 2025-01-15
**Mantenido por**: Estudiante del Módulo 3 Clase 2
**Estado**: ✅ Clase completada con éxito
