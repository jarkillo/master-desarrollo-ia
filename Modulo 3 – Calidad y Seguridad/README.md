# Módulo 3 - Calidad y Seguridad

## Overview

Este módulo introduce **seguridad de aplicaciones** y **auditoría de código**, transformando APIs funcionales en sistemas resistentes a ataques. Los estudiantes aprenderán a detectar vulnerabilidades OWASP Top 10, implementar autenticación JWT, configurar pipelines seguros, y **auditar críticamente código generado por IA**.

**Visión del módulo**: Construir sistemas que se defienden solos, aplicando seguridad por diseño y usando IA con criterio para detectar vulnerabilidades.

## Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

1. **Detectar vulnerabilidades**: Identificar y mitigar OWASP Top 10 en APIs
2. **Implementar autenticación**: JWT, tokens de acceso/refresh, protección de endpoints
3. **Aplicar validación robusta**: Pydantic avanzado, sanitización de entrada
4. **Configurar pipelines seguros**: CI/CD con análisis de seguridad (Bandit, Safety, Gitleaks)
5. **Auditar código de IA**: Revisar críticamente código generado por asistentes
6. **Implementar observabilidad**: Sentry para monitoreo de errores en producción
7. **Usar IA para seguridad**: Agentes especializados en auditoría y detección de vulnerabilidades

## Prerrequisitos

- Completar Módulo 2 (o equivalente)
- Arquitectura limpia (API → Service → Repository)
- FastAPI intermedio
- Testing con pytest
- CI/CD básico con GitHub Actions

## Estructura del Módulo

### Clase 1 - El Código que se Defiende Solo
**Duración**: 4h | **Tipo**: Validación + Defensa

**Contenido**:
- Validación de entrada con Pydantic (Field, validators, custom validators)
- Sanitización de datos
- Manejo robusto de errores (HTTPException personalizado)
- Principio de "fail secure" (fallar de forma segura)

**Proyecto**: API con validación defensiva
- Validaciones exhaustivas de todos los campos
- Mensajes de error seguros (sin revelar información sensible)
- Logging de intentos de entrada inválida

**Artefactos**:
- `Glosario - Clase 1.md` - ⚠️ **PENDIENTE** (según CLAUDE.md)

### Clase 2 - Seguridad Básica en tu API
**Duración**: 4h | **Tipo**: OWASP + Vulnerabilidades

**Contenido**:
- OWASP Top 10 2021 para APIs
- A01: Broken Access Control
- A03: Injection
- A07: Authentication Failures
- A08: Software Integrity Failures
- A09: Security Logging Failures
- Introducción a dependency injection segura

**Proyecto**: API resistente a vulnerabilidades comunes
- `api/dependencias.py` - Dependency Injection segura
- Ejemplos de código vulnerable vs seguro
- Checklist de seguridad

**Artefactos**:
- `Clase 2 - Seguridad básica en tu API.md` - Material teórico
- `SECURITY_CHECKLIST.md` - Checklist de auditoría
- `ejemplos_vulnerables/` - Código vulnerable para aprender
- `ejercicios/` - Ejercicios de detección y corrección

**Ejercicios destacados**:
- `ejercicio_1_detectar_vulnerabilidades.md` - Caza de bugs
- `ejercicio_2_auditoria_con_checklist.md` - Auditoría sistemática
- `ejercicio_3_security_hardening_con_agentes.md` - Hardening con IA

### Clase 3 - Auditoría Continua y Defensa Inteligente con IA
**Duración**: 4h | **Tipo**: Auditoría + IA

**Contenido**:
- Herramientas de auditoría (Bandit, Safety)
- Análisis estático de código
- Detección de secretos (Gitleaks)
- Uso de agentes IA para revisión de seguridad
- Auditoría crítica de código generado por IA

**Proyecto**: API con auditoría continua
- Pipeline de seguridad automatizado
- Detección de vulnerabilidades antes del merge
- Prompts para revisión de seguridad con IA

**Artefactos**:
- `Glosario - Clase 3.md` - Términos de auditoría

### Clase 4 - Seguridad Avanzada y Autenticación con JWT
**Duración**: 5h | **Tipo**: Autenticación + Autorización

**Contenido**:
- JSON Web Tokens (JWT): estructura, claims, firma
- Access tokens y refresh tokens
- Protección de endpoints con dependencias
- Gestión segura de secretos (variables de entorno)
- Rotación de tokens

**Proyecto**: API con autenticación completa
- `api/seguridad_jwt.py` - Módulo de autenticación
- Login, registro, protección de endpoints
- Middleware de autenticación

**Artefactos**:
- `Glosario - Clase 4.md` - Términos de autenticación
- `tests/test_auth_jwt.py` - Tests de autenticación

**Funcionalidades implementadas**:
- `POST /token` - Login con JWT
- `GET /usuarios/me` - Endpoint protegido
- Validación de tokens en cada request

### Clase 5 - Defensa Activa y Pipelines Seguros
**Duración**: 4h | **Tipo**: CI/CD Seguro

**Contenido**:
- Pre-commit hooks con validación de seguridad
- Pre-push hooks (linting + tests + security)
- GitHub Actions para auditoría continua
- Secrets management en CI/CD
- Análisis de dependencias vulnerables

**Proyecto**: Pipeline de seguridad completo
- `.githooks/pre-push` - Validación local completa
- `scripts/pre-pr-check.sh` - Validación pre-PR
- CI/CD con Bandit, Safety, Gitleaks

**Funcionalidades**:
- Bloqueo automático de commits con secretos
- Tests de seguridad en cada PR
- Reporte de vulnerabilidades de dependencias

### Clase 6 - Defensa Completa y CI/CD Inteligente
**Duración**: 4h | **Tipo**: Integración Total

**Contenido**:
- Pipeline completo de calidad + seguridad
- Integración de todas las herramientas (Ruff, pytest, Bandit, Safety, Gitleaks)
- Cobertura de tests de seguridad
- Branch protection y políticas de merge
- Revisión de PRs con agentes IA

**Proyecto**: API production-ready con seguridad completa
- Pipeline de CI/CD robusto
- Tests de autenticación completos
- Validación de seguridad automática

**Artefactos**:
- `Glosario - Clase 6.md` - Términos de CI/CD seguro

### Clase 7 - Clase Bonus: Observabilidad y Alertas con Sentry
**Duración**: 3h | **Tipo**: Monitoreo + Producción

**Contenido**:
- Integración de Sentry con FastAPI
- Captura de errores y excepciones
- Contexto de usuario en errores
- Alertas en tiempo real
- Performance monitoring básico

**Proyecto**: API con observabilidad completa
- Sentry SDK integrado
- Tracking de errores en producción
- Alertas configuradas

**Artefactos**:
- `Glosario - Clase 7.md` - ⚠️ **PENDIENTE** (según CLAUDE.md)

## Arquitectura de Referencia

A partir de Clase 2, se añade la capa de seguridad:

```
api/
├── __init__.py
├── api.py                    # Endpoints + protección
├── servicio_tareas.py        # Lógica de negocio
├── repositorio_base.py       # Protocol
├── repositorio_memoria.py    # Implementación memoria
├── repositorio_json.py       # Implementación JSON
├── dependencias.py           # Dependency Injection (Clase 2+)
└── seguridad_jwt.py          # Autenticación JWT (Clase 4+)

tests/
├── conftest.py
├── test_crear_tarea_clase7.py  ⚠️ Nombre incorrecto (ver Problemas Conocidos)
└── test_auth_jwt.py            # Tests de autenticación (Clase 4+)

tests_integrations/
├── conftest.py
└── test_integracion_*.py
```

### Flujo de Seguridad

```
Cliente HTTP
    ↓
[JWT Validation] ← Dependencia de autenticación
    ↓
API Layer (validación Pydantic)
    ↓
Service Layer (lógica + reglas de negocio)
    ↓
Repository Layer (persistencia segura)
    ↓
[Sentry Monitoring] ← Observabilidad (Clase 7)
```

## Tecnologías Utilizadas

**Seguridad**:
- **python-jose[cryptography]**: Manejo de JWT
- **Bandit**: Auditoría de seguridad
- **Safety**: Análisis de dependencias vulnerables
- **Gitleaks**: Detección de secretos

**Observabilidad**:
- **sentry-sdk[fastapi]**: Monitoreo de errores (Clase 7)

**Validación**:
- **Pydantic 2.11.10**: Validación avanzada con Field, validators

**Testing**:
- **pytest 8.4.2**: Tests de seguridad

**CI/CD**:
- **GitHub Actions**: Pipelines de seguridad
- **Git hooks**: Validación local

## Cómo Ejecutar los Proyectos

### Configuración inicial

```bash
# Activar entorno virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Instalar dependencias (incluye herramientas de seguridad)
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.template .env
# Editar .env con tus secretos:
# JWT_SECRET=tu_clave_secreta_segura_minimo_32_caracteres
# MODE=dev
```

### Ejecutar la API (con autenticación)

```bash
# Navegar a una clase (ej. Clase 4+)
cd "Modulo 3 – Calidad y Seguridad/Clase 4 - Seguridad avanzada y autenticación con JWT"

# Ejecutar servidor
uvicorn api.api:app --reload

# Probar autenticación:
# 1. Obtener token: POST http://localhost:8000/token
# 2. Usar token en endpoints protegidos
```

### Ejecutar tests de seguridad

```bash
# Tests unitarios (incluye auth)
pytest tests/ -v

# Solo tests de autenticación
pytest tests/test_auth_jwt.py -v

# Auditoría de seguridad
bandit -r api/ -ll

# Análisis de dependencias
safety check

# Detección de secretos
gitleaks detect --source . --verbose

# Validación completa (pre-PR)
bash scripts/pre-pr-check.sh
```

### Probar vulnerabilidades (entorno de aprendizaje)

```bash
# Clase 2 - Ejemplos vulnerables (NO ejecutar en producción)
cd "Modulo 3 – Calidad y Seguridad/Clase 2 - Seguridad básica en tu API/ejemplos_vulnerables"

# Revisar código vulnerable para aprender
cat a01_broken_access_control.py
cat a03_injection.py
cat a07_authentication_failures.py
```

## Progresión del Aprendizaje

**Estrategia: "Construir para defender, defender para aprender"**

1. **Clase 1**: Validación defensiva → Tu API rechaza entrada maliciosa
2. **Clase 2**: Vulnerabilidades OWASP → Reconoces ataques comunes
3. **Clase 3**: Auditoría automática → Detectas vulnerabilidades antes del merge
4. **Clase 4**: Autenticación JWT → Proteges endpoints críticos
5. **Clase 5**: Pipeline seguro → Calidad + seguridad continua
6. **Clase 6**: Integración completa → Sistema production-ready
7. **Clase 7**: Observabilidad → Monitoreo en producción

## Uso de IA en Este Módulo

### 🔐 Auditoría Crítica de Código de IA

**⚠️ IMPORTANTE**: Este módulo enfatiza la **revisión crítica** de código generado por IA:

- ❌ **NO confíes ciegamente** en código generado
- ✅ **VALIDA** cada línea con Bandit, Safety
- ✅ **COMPRENDE** qué hace el código antes de usarlo
- ✅ **PRUEBA** exhaustivamente con tests de seguridad

### Agentes Especializados

Usa estos agentes educativos (`.claude/agents/educational/`):

- **FastAPI Design Coach**: Validación de endpoints seguros
- **API Design Reviewer**: Verificación de respuestas HTTP correctas

### Prompts de Seguridad

**Auditoría de código**:
```
"Revisa este endpoint buscando vulnerabilidades OWASP Top 10.
Específicamente verifica: Broken Access Control, Injection,
Authentication Failures."
```

**Generación segura**:
```
"Genera un endpoint POST /tareas con:
- Validación Pydantic exhaustiva (título 1-200 chars)
- Autenticación JWT requerida
- Manejo de errores sin revelar información sensible
- Logging seguro de operaciones"
```

**Revisión de dependencias**:
```
"Analiza requirements.txt y verifica si hay vulnerabilidades conocidas
en las dependencias. Sugiere actualizaciones seguras."
```

## Ejercicios Prácticos

### Clase 2 - Ejercicios de Seguridad

**Ejercicio 1**: Detectar vulnerabilidades
- Código vulnerable proporcionado
- Tarea: Identificar 5 vulnerabilidades OWASP
- Usar agentes IA para validación

**Ejercicio 2**: Auditoría con checklist
- API de ejemplo con múltiples issues
- Aplicar `SECURITY_CHECKLIST.md`
- Documentar hallazgos

**Ejercicio 3**: Security hardening con agentes
- API sin protección
- Usar agentes para refactorizar
- Validar con Bandit + tests

## Problemas Conocidos

⚠️ Según `CLAUDE.md`, hay inconsistencias conocidas:

### Naming Issues

**Tests incorrectamente nombrados**: Todas las clases usan `test_crear_tarea_clase7.py` en lugar del número correcto:

```
Modulo 3/Clase 1/tests/test_crear_tarea_clase7.py  ❌ Debería ser clase1
Modulo 3/Clase 2/tests/test_crear_tarea_clase7.py  ❌ Debería ser clase2
Modulo 3/Clase 3/tests/test_crear_tarea_clase7.py  ❌ Debería ser clase3
...
```

**Solución propuesta**: Renombrar a `test_crear_tarea_clase{X}_mod3.py` para claridad.

### Documentación Incompleta

- **Glosario Clase 1**: Falta crear
- **Glosario Clase 7**: Falta crear

### CI/CD

- No todas las clases de este módulo están en la matriz de CI/CD
- Ver `.github/workflows/ci.yml` y `ci_quality.yml`

Estas inconsistencias están documentadas en `docs/reviews/REVIEW_COMPLETENESS.md`.

## Próximos Pasos

Después de completar este módulo:

➡️ **Módulo 4 - Infraestructura + AI DevOps**: Aprenderás Docker, bases de datos (SQLAlchemy), Alembic (migraciones), y despliegue en cloud.

⚠️ **Nota**: Módulo 4 está solo 25% completo (clases 1-2 implementadas, clases 3-8 pendientes).

## Recursos Adicionales

### Documentación Oficial

- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **JWT Best Practices**: https://tools.ietf.org/html/rfc8725
- **FastAPI Security**: https://fastapi.tiangolo.com/tutorial/security/
- **Pydantic Validation**: https://docs.pydantic.dev/latest/

### Herramientas de Seguridad

- **Bandit**: https://bandit.readthedocs.io/
- **Safety**: https://pyup.io/safety/
- **Gitleaks**: https://github.com/gitleaks/gitleaks
- **Sentry**: https://docs.sentry.io/platforms/python/guides/fastapi/

### Checklists y Guías

- `SECURITY_CHECKLIST.md` (Clase 2) - Auditoría sistemática
- `scripts/pre-pr-check.sh` - Validación completa local

## Contribuciones

Si encuentras vulnerabilidades o mejoras de seguridad:

1. ⚠️ **NO publiques vulnerabilidades reales** en issues públicos
2. Contacta en privado si es crítico
3. Para mejoras de documentación/código, abre un PR

---

**¿Listo para construir software seguro?** Comienza en [Clase 1 - El codigo que se defiende solo](./Clase%201%20-%20El%20codigo%20que%20se%20defiende%20solo/) 🔒

**Recuerda**: La seguridad no es un feature, es un requisito fundamental. 🛡️
