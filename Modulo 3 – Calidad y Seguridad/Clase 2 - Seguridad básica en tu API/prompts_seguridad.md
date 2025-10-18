# Prompts de Seguridad Reutilizables

**Propósito**: Colección de prompts reutilizables para generar código seguro con IA.
**Proyecto**: API de Tareas - Módulo 3 Clase 2
**Última actualización**: 2025-01-15

---

## Índice de prompts

1. [Prompt Base para Endpoints Seguros](#prompt-base-endpoints-seguros)
2. [Prompt para Autenticación con API Keys](#prompt-autenticacion-api-keys)
3. [Prompt para Endpoints con Ownership](#prompt-endpoints-con-ownership)
4. [Prompt para Auditoría de Código](#prompt-auditoria-codigo)
5. [Prompt para Corrección de Vulnerabilidades](#prompt-correccion-vulnerabilidades)
6. [Prompt para Tests de Seguridad](#prompt-tests-seguridad)
7. [Prompt para Agentes Educacionales](#prompt-agentes-educacionales)

---

## Prompt Base para Endpoints Seguros

**Cuándo usar**: Al generar cualquier endpoint FastAPI desde cero.

### Prompt

```
Crea un endpoint FastAPI para [FUNCIONALIDAD].

Requisitos de seguridad (OWASP Top 10):
1. **Autenticación (A07)**: Requiere autenticación con Depends(obtener_usuario_actual)
2. **Control de acceso (A01)**: Valida ownership del recurso (tarea.user_id == usuario_actual)
3. **Validación de entrada (A03)**:
   - Usa Pydantic BaseModel (no dict)
   - Campos con Field(min_length, max_length, ge, le)
   - Previene mass assignment (solo campos específicos)
4. **Logging (A09)**:
   - Registra intentos no autorizados (403)
   - Registra eventos críticos (creación, modificación, eliminación)
   - Formato estructurado con extra={"event": "nombre"}
5. **Manejo de errores**:
   - HTTPException para todos los errores
   - Status codes correctos (200/201/204/403/404/422)
   - Mensajes genéricos (no exponen detalles internos)

Estructura del código:
- Modelos Pydantic separados (Request, Response)
- Comentarios explicando cada mitigación OWASP
- Type hints completos
- Logging con Python logging module
```

### Ejemplo de uso

```
Crea un endpoint FastAPI para eliminar una tarea por ID.

[Copiar requisitos de seguridad de arriba]
```

---

## Prompt para Autenticación con API Keys

**Cuándo usar**: Al implementar autenticación con API Keys.

### Prompt

```
Implementa autenticación con API Keys para FastAPI siguiendo estas especificaciones de seguridad:

**Generación de API Keys (A07)**:
- Usa secrets.token_urlsafe(32) para generar claves (256 bits mínimo)
- API Keys de 43+ caracteres (output de token_urlsafe(32))
- Criptográficamente seguras

**Almacenamiento (A08)**:
- Almacena API Keys hasheadas con SHA-256
- NUNCA almacenar en texto plano
- Schema: {"user_id": int, "api_key_hash": str, "created_at": datetime}

**Validación (A07)**:
- Usa secrets.compare_digest() para comparación timing-safe
- NO usar == (vulnerable a timing attacks)
- Hashear API Key recibida antes de comparar

**Logging (A09)**:
- Registra intentos fallidos de autenticación
- Solo registra primeros 4 caracteres de API Key
- Formato: extra={"event": "auth_failed", "api_key_prefix": api_key[:4]}

**Estructura**:
1. Función generar_api_key() → str
2. Función hashear_api_key(api_key: str) → str
3. Dependency obtener_usuario_actual(api_key: str = Header(...)) → int
4. Schema Pydantic para User con api_key_hash

Incluye comentarios explicando por qué cada mitigación es importante.
```

---

## Prompt para Endpoints con Ownership

**Cuándo usar**: Al crear endpoints GET/PUT/DELETE que requieren validación de ownership.

### Prompt

```
Crea un endpoint FastAPI [GET/PUT/DELETE] para [RECURSO] con validación de ownership.

**Control de acceso (A01)**:
1. Requiere autenticación con Depends(obtener_usuario_actual)
2. Verifica que recurso existe (retornar 404 si no)
3. Valida ownership: recurso.user_id == usuario_actual
4. Retorna 403 Forbidden si no autorizado (NO 404 para evitar information disclosure)
5. Filtra listados por user_id (no retornar recursos de otros usuarios)

**Logging (A09)**:
1. Registra intentos no autorizados con logger.warning
2. Incluye contexto: recurso_id, user_id, tipo de operación
3. Formato estructurado: extra={"event": "unauthorized_access", ...}

**Manejo de errores**:
1. HTTPException(404) si recurso no existe
2. HTTPException(403) si no autorizado
3. Mensajes genéricos: "Acceso denegado" (no "Usuario X no es dueño de recurso Y")

**Códigos de estado**:
- GET: 200 OK (éxito), 403 (no autorizado), 404 (no existe)
- PUT: 200 OK (éxito), 403, 404
- DELETE: 204 No Content (éxito), 403, 404

Incluye ejemplos de código vulnerable vs seguro en comentarios.
```

### Ejemplo de uso

```
Crea un endpoint FastAPI DELETE para eliminar una tarea por ID con validación de ownership.

[Copiar requisitos de arriba]
```

---

## Prompt para Auditoría de Código

**Cuándo usar**: Al auditar código generado por IA para detectar vulnerabilidades.

### Prompt para Security Hardening Mentor

```
Actúa como Security Hardening Mentor. Audita este código FastAPI para vulnerabilidades de seguridad siguiendo OWASP Top 10.

Código a auditar:
[PEGAR CÓDIGO AQUÍ]

Para cada vulnerabilidad detectada, proporciona:

1. **Clasificación**:
   - Código OWASP (A01, A03, A07, A08, A09, etc.)
   - Severidad (Crítico/Alto/Medio/Bajo)
   - Línea de código problemática

2. **Análisis**:
   - ¿Qué vulnerabilidad es?
   - ¿Por qué es peligrosa?
   - Escenario de ataque específico (paso a paso)
   - Impacto si se explota

3. **Corrección**:
   - Código corregido
   - Explicación de la mitigación
   - Mejores prácticas relacionadas

Enfócate especialmente en:
- A01: Broken Access Control (ownership)
- A03: Injection (Pydantic, eval, SQL)
- A07: Authentication Failures (API Keys, timing attacks)
- A08: Software Integrity (dependencias, pickle)
- A09: Security Logging (audit logs)

Ordena las vulnerabilidades por severidad (Crítico → Bajo).
```

---

## Prompt para Corrección de Vulnerabilidades

**Cuándo usar**: Al corregir código vulnerable detectado en auditoría.

### Prompt

```
Corrige las siguientes vulnerabilidades en este código FastAPI:

**Código vulnerable**:
[PEGAR CÓDIGO VULNERABLE]

**Vulnerabilidades detectadas**:
1. [Vulnerabilidad 1 - A0X]
2. [Vulnerabilidad 2 - A0Y]
3. [...]

**Requisitos para la corrección**:

1. **Implementar mitigaciones OWASP**:
   - A01: Validar ownership en todos los endpoints
   - A03: Usar Pydantic con Field() para validación
   - A07: API Keys hasheadas + secrets.compare_digest
   - A09: Logging de eventos de seguridad

2. **Estructura del código corregido**:
   - Modelos Pydantic separados (Request, Response)
   - Type hints completos
   - Comentarios explicando cada corrección
   - Before/After comparison en comentarios

3. **Formato de respuesta**:
   - Código completo corregido
   - Explicación de cada cambio
   - Checklist de vulnerabilidades mitigadas

4. **Validación**:
   - El código debe aprobar SECURITY_CHECKLIST.md (50 checks)
   - Checks críticos deben estar 10/10
   - Sin uso de eval(), pickle, dict sin validación

Proporciona el código corregido con todos los imports necesarios.
```

---

## Prompt para Tests de Seguridad

**Cuándo usar**: Al escribir tests para validar mitigaciones de seguridad.

### Prompt

```
Crea tests de seguridad para este endpoint FastAPI:

[PEGAR CÓDIGO DEL ENDPOINT]

**Tests requeridos (OWASP Top 10)**:

1. **A07: Autenticación**:
   - test_acceso_sin_autenticacion_devuelve_401()
   - test_api_key_invalida_devuelve_401()

2. **A01: Control de Acceso**:
   - test_acceso_recurso_ajeno_devuelve_403()
   - test_listar_solo_retorna_recursos_propios()

3. **A03: Validación de Entrada**:
   - test_pydantic_rechaza_datos_invalidos()
   - test_validacion_rechaza_valores_fuera_de_rango()
   - test_mass_assignment_no_permite_modificar_campos_restringidos()

4. **A09: Logging**:
   - test_intento_no_autorizado_se_registra(caplog)
   - test_eliminacion_se_registra_en_audit_log(caplog)

**Estructura de los tests**:
- Usa pytest con TestClient
- Patrón Given-When-Then en docstrings
- Fixtures para crear datos de prueba
- Validar status codes específicos (401/403/404/422)
- Validar estructura de respuesta
- Validar logs con caplog

**Formato de salida**:
```python
# tests/test_seguridad_[endpoint].py
import pytest
from fastapi.testclient import TestClient

def test_nombre_descriptivo():
    \"\"\"
    Given: [Condición inicial]
    When: [Acción]
    Then: [Resultado esperado]
    \"\"\"
    # Arrange
    ...
    # Act
    ...
    # Assert
    assert ...
```

Genera tests exhaustivos que validen TODAS las mitigaciones de seguridad.
```

---

## Prompt para Agentes Educacionales

**Cuándo usar**: Al solicitar ayuda de agentes especializados para revisión de código.

### Prompt para FastAPI Design Coach

```
Actúa como FastAPI Design Coach. Revisa este código FastAPI para anti-patrones de diseño que puedan convertirse en vulnerabilidades.

[PEGAR CÓDIGO]

Enfócate en:
1. **Validación con Pydantic**:
   - ¿Usa BaseModel o dict?
   - ¿Campos tienen Field() con validación?
   - ¿Previene mass assignment?

2. **Dependency Injection**:
   - ¿Usa Depends() para autenticación?
   - ¿Dependencies están bien estructuradas?

3. **Status Codes HTTP**:
   - ¿Usa 200/201/204/403/404/422 correctamente?
   - ¿DELETE retorna 204 No Content?

4. **Response Models**:
   - ¿Usa response_model consistentemente?
   - ¿Valida salida además de entrada?

5. **Async/Await**:
   - ¿Endpoints I/O-bound son async?
   - ¿Evita blocking calls?

Para cada anti-patrón detectado:
- Línea de código problemática
- ¿Por qué es un anti-patrón?
- ¿Qué vulnerabilidad puede causar?
- Código corregido
```

### Prompt para Python Best Practices Coach

```
Actúa como Python Best Practices Coach. Audita este código FastAPI para patrones inseguros de Python.

[PEGAR CÓDIGO]

Busca:
1. **Criptografía**:
   - ¿Usa secrets module (no random)?
   - ¿secrets.compare_digest para comparaciones?
   - ¿Hashea secrets antes de almacenar?

2. **Manejo de Excepciones**:
   - ¿Excepciones específicas vs genéricas?
   - ¿No expone stack traces?

3. **Type Hints**:
   - ¿Type hints completos?
   - ¿Return types especificados?

4. **Estructuras de Datos**:
   - ¿Evita mutabilidad de globales?
   - ¿List comprehensions vs loops?

5. **Validación**:
   - ¿No usa eval(), exec(), pickle?

Para cada patrón inseguro:
- ¿Por qué es inseguro?
- ¿Qué ataque permite?
- Alternativa segura con código
```

### Prompt para API Design Reviewer

```
Actúa como API Design Reviewer. Evalúa este código FastAPI siguiendo principios RESTful y OWASP Top 10.

[PEGAR CÓDIGO]

Evalúa:
1. **Diseño RESTful**:
   - ¿Endpoints siguen REST conventions?
   - ¿Nombres de recursos plurales y descriptivos?
   - ¿Versionado de API (/v1/)?

2. **Status Codes**:
   - ¿200/201/204/403/404/422 usados correctamente?
   - ¿Consistencia entre endpoints?

3. **Paginación**:
   - ¿Listados tienen paginación?
   - ¿Límites validados (ge=1, le=100)?

4. **Seguridad**:
   - ¿Rate limiting?
   - ¿CORS configurado correctamente?
   - ¿Autenticación/Autorización?

5. **Documentación**:
   - ¿OpenAPI/Swagger actualizado?
   - ¿Descripciones de endpoints?

Clasifica cada problema:
- Severidad: Crítico/Alto/Medio/Bajo
- Código OWASP (si aplica)
- Impacto en producción
```

---

## Plantilla de Prompt Completo

**Usa esta plantilla para generar endpoints complejos con todas las mitigaciones de seguridad:**

```
Crea un endpoint FastAPI [MÉTODO HTTP] para [FUNCIONALIDAD].

=== ESPECIFICACIONES TÉCNICAS ===

**Endpoint**: [MÉTODO] /v1/[recurso]/{id}
**Autenticación**: Requerida (API Keys)
**Ownership**: Validar que usuario es dueño del recurso

=== REQUISITOS DE SEGURIDAD (OWASP TOP 10) ===

**A01: Broken Access Control**:
- Validar ownership: recurso.user_id == usuario_actual
- Retornar 403 si no autorizado, 404 si no existe
- Filtrar listados por user_id

**A03: Injection**:
- Pydantic BaseModel para validación (no dict)
- Field() con min_length, max_length, ge, le
- Prevenir mass assignment (solo campos específicos)
- Queries usan ORM (no f-strings)

**A07: Authentication Failures**:
- Depends(obtener_usuario_actual) para autenticación
- API Keys hasheadas + secrets.compare_digest

**A08: Software/Data Integrity**:
- No usar pickle
- Validar integridad de datos
- Dependencies auditadas con Safety

**A09: Security Logging**:
- Logging de intentos no autorizados
- Logging de eventos críticos (CRUD)
- Formato estructurado: extra={"event": ...}

=== ESTRUCTURA DEL CÓDIGO ===

1. **Modelos Pydantic**:
   - [Nombre]Request con validación Field()
   - [Nombre]Response para salida

2. **Endpoint**:
   - Type hints completos
   - response_model definido
   - status_code correcto
   - Comentarios explicando mitigaciones OWASP

3. **Manejo de errores**:
   - HTTPException para todos los errores
   - Mensajes genéricos (no exponen detalles)

4. **Logging**:
   - logger.warning para intentos no autorizados
   - logger.info para eventos exitosos

=== EJEMPLO DE SALIDA ESPERADO ===

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

class [Nombre]Request(BaseModel):
    # ... con Field()

class [Nombre]Response(BaseModel):
    # ...

@app.[método]("/v1/[recurso]/{id}", response_model=[Nombre]Response, status_code=[código])
def [nombre_funcion](
    id: int,
    datos: [Nombre]Request = None,  # Si aplica
    usuario_actual: int = Depends(obtener_usuario_actual)
):
    \"\"\"Docstring con explicación\"\"\"

    # 1. Verificar que recurso existe (A01)
    # 2. Validar ownership (A01)
    # 3. Realizar operación
    # 4. Logging (A09)
    # 5. Retornar respuesta

    pass
```

Genera el código completo con todos los imports necesarios y comentarios explicativos.
```

---

## Checklist de Uso de Prompts

Antes de generar código con IA, asegúrate de:

- [ ] Especificar requisitos de seguridad OWASP explícitamente
- [ ] Mencionar uso de Pydantic con Field()
- [ ] Requerir Depends() para autenticación
- [ ] Solicitar validación de ownership
- [ ] Pedir logging de eventos de seguridad
- [ ] Especificar status codes correctos
- [ ] Solicitar comentarios explicando mitigaciones
- [ ] Pedir ejemplos de código vulnerable vs seguro

---

**Última actualización**: 2025-01-15
**Mantenido por**: Estudiante del Módulo 3 Clase 2
**Uso**: Copiar y personalizar según necesidad
