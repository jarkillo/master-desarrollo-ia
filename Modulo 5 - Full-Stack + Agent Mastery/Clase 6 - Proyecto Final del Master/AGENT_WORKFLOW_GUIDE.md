# Guía de Documentación de Agentes IA

## Introducción

Esta guía te enseña **cómo documentar el uso de agentes IA** en tu proyecto final de forma profesional y transparente.

**Por qué es importante**: La documentación de agentes representa el **20% de tu calificación** y es lo que te diferencia de otros desarrolladores.

---

## Estructura de Documentación Recomendada

```
docs/
├── agents/
│   ├── README.md                 # Índice general
│   ├── METRICS.md                # Métricas globales
│   ├── agents/                   # Documentación por agente
│   │   ├── backend-architect.md
│   │   ├── fastapi-specialist.md
│   │   ├── database-designer.md
│   │   ├── security-auditor.md
│   │   ├── test-strategist.md
│   │   └── frontend-coach.md
│   ├── workflows/                # Workflows estándar
│   │   ├── feature-workflow.md
│   │   ├── bugfix-workflow.md
│   │   └── refactor-workflow.md
│   └── examples/                 # Ejemplos completos
│       ├── feature-authentication.md
│       ├── feature-dashboard.md
│       └── bugfix-n-plus-one.md
```

---

## 1. README.md del Índice de Agentes

**Ubicación**: `docs/agents/README.md`

**Contenido mínimo**:

```markdown
# Agentes IA Utilizados en TaskFlow

Este directorio documenta el uso de agentes IA especializados durante el desarrollo de TaskFlow.

## Equipo de Agentes

| Agente | Rol | Archivos |
|--------|-----|----------|
| Backend Architect | Diseño de arquitectura | [Ver docs](agents/backend-architect.md) |
| FastAPI Specialist | Implementación API | [Ver docs](agents/fastapi-specialist.md) |
| Database Designer | Modelado de datos | [Ver docs](agents/database-designer.md) |
| Security Auditor | Revisión de seguridad | [Ver docs](agents/security-auditor.md) |
| Test Strategist | Estrategia de testing | [Ver docs](agents/test-strategist.md) |
| Frontend Coach | React + TypeScript | [Ver docs](agents/frontend-coach.md) |

## Métricas Globales

Ver [METRICS.md](METRICS.md) para métricas completas de productividad.

## Ejemplos de Uso

- [Feature: Autenticación JWT](examples/feature-authentication.md)
- [Feature: Dashboard con métricas](examples/feature-dashboard.md)
- [Bugfix: N+1 Query en proyectos](examples/bugfix-n-plus-one.md)

## Workflow Estándar

Ver [workflows/feature-workflow.md](workflows/feature-workflow.md) para el proceso completo.
```

---

## 2. Documentación por Agente

**Ubicación**: `docs/agents/agents/[nombre-agente].md`

**Template**:

```markdown
# [Nombre del Agente]

## Rol y Responsabilidades

**Especialización**: [Área de expertise]

**Responsabilidades**:
- 🎯 [Responsabilidad 1]
- 🎯 [Responsabilidad 2]
- 🎯 [Responsabilidad 3]

**NO hace** (límites claros):
- ❌ [Lo que NO debe hacer]

## Prompt Base Utilizado

[Prompt template que usaste para este agente]

## Prompts Ejecutados

### Prompt 1: [Nombre de la tarea]

**Fecha**: 2025-01-15  
**Contexto**: [Por qué se necesitó]

**Prompt**:
```
[Prompt exacto]
```

**Respuesta**: Ver [ejemplo completo](../examples/feature-X.md)

**Decisión**:
- ✅ **Implementado**: [Qué se usó tal cual]
- ⚠️ **Modificado**: [Qué se cambió y por qué]
- ❌ **Rechazado**: [Qué se descartó y por qué]

**Validación manual**:
- [x] Código revisado línea por línea
- [x] Tests ejecutados
- [x] Security audit
- [x] Performance check

## Métricas

| Métrica | Valor |
|---------|-------|
| Prompts totales | 25 |
| Código generado (líneas) | ~1,500 |
| Código usado sin cambios | 60% |
| Código modificado | 30% |
| Código rechazado | 10% |
| Tiempo ahorrado | 15 horas |

## Lecciones Aprendidas

1. **Contexto es crítico**: Prompts con más contexto generan mejor código
2. **Iterar es normal**: Rara vez la primera respuesta es perfecta
3. **Validar siempre**: Nunca confiar ciegamente
```

---

## 3. Ejemplo Completo de Feature

**Ubicación**: `docs/agents/examples/feature-authentication.md`

**Estructura**:

```markdown
# Feature: Autenticación JWT

## Metadata

- **Fecha**: 2025-01-15 a 2025-01-17
- **Agentes**: Backend Architect, FastAPI Specialist, Security Auditor
- **Tiempo**: 8 horas (vs 24 horas estimadas sin IA)
- **Archivos**: 8 creados/modificados

## Contexto

**Necesidad**: Sistema de autenticación robusto con JWT, roles y refresh tokens.

**Requisitos**:
- Registro con validación de email
- Login con access + refresh tokens
- Roles: Admin, Member, Viewer
- Rate limiting en login
- Password policy strong

## Fase 1: Diseño con Backend Architect

### Prompt

```
Diseña la arquitectura de autenticación JWT para una aplicación FastAPI.

Contexto:
- Aplicación de gestión de proyectos
- Usuarios con roles (Admin, Member, Viewer)
- PostgreSQL + SQLAlchemy
- Arquitectura limpia (API/Service/Repository)

Requisitos:
- Registro y login
- JWT con access + refresh tokens
- Invalidación de tokens (logout)
- Rate limiting

Propón:
1. Modelos de datos
2. Flujo de autenticación
3. Consideraciones de seguridad
```

### Respuesta (resumen)

[Diagrama de arquitectura propuesto]

**Modelos**:
- `User`: id, email, hashed_password, role, is_active
- `RefreshToken`: id, user_id, token, expires_at, is_revoked

**Flujo**:
1. POST /register → crear user → return tokens
2. POST /login → verificar password → return tokens
3. POST /refresh → validar refresh_token → return new access_token
4. POST /logout → revocar refresh_token

**Seguridad**:
- Bcrypt con 12 rounds mínimo
- Access token: 15 min
- Refresh token: 7 días, almacenado en Redis
- Rate limiting: 5 intentos/minuto

### Decisión

✅ **Implementado**: Modelos y flujo tal como propuso  
⚠️ **Modificado**: Refresh tokens en Redis (no DB) para mejor performance  
❌ **Rechazado**: OAuth social login (fuera de scope MVP)

### Razón de Modificaciones

**Redis para refresh tokens**:
- Performance: O(1) vs query a DB
- TTL automático (no necesito cron job)
- Trade-off: Dependencia adicional (aceptable)

## Fase 2: Implementación con FastAPI Specialist

### Prompt

```
Implementa los endpoints de autenticación siguiendo el diseño.

Tech stack:
- FastAPI con dependency injection
- Pydantic para validación
- python-jose para JWT
- bcrypt para hashing
- Redis para refresh tokens

Endpoints:
1. POST /auth/register
2. POST /auth/login
3. POST /auth/refresh
4. POST /auth/logout

Genera también:
- Schemas Pydantic
- Dependency get_current_user
- Rate limiting middleware
```

### Código Generado (extracto)

```python
# Código generado por el agente...
```

### Validación Manual

**Tests ejecutados**:
- ✅ Registro válido
- ✅ Registro email duplicado (409)
- ✅ Login correcto
- ✅ Login incorrecto (401)
- ✅ Refresh token válido
- ✅ Logout

**Modificaciones**:
- Añadí validación de password strength (agente no lo consideró)
- Mejoré mensajes de error (más descriptivos)

## Fase 3: Auditoría con Security Auditor

### Prompt

```
Audita el código de autenticación.

Busca:
- Vulnerabilidades OWASP Top 10
- Password policy débil
- JWT vulnerabilities
- Falta de rate limiting
- SQL injection
```

### Hallazgos

1. ⚠️ **Password policy muy básica** → Añadida validación de complejidad
2. ⚠️ **Sin logging de intentos fallidos** → Añadido logging
3. ✅ JWT secrets en .env → OK
4. ✅ Rate limiting funciona → OK

## Resultado Final

### Archivos

- `app/models/user.py` (nuevo)
- `app/schemas/auth.py` (nuevo)
- `app/services/auth_service.py` (nuevo)
- `app/api/routes/auth.py` (nuevo)
- `app/core/security.py` (modificado)
- `tests/test_auth.py` (nuevo, 15 tests)

### Estadísticas

| Métrica | Valor |
|---------|-------|
| Líneas generadas | ~600 |
| Líneas modificadas | ~100 |
| Tests generados | 15 |
| Cobertura | 92% |
| **Tiempo real** | **8 horas** |
| Tiempo sin IA | ~24 horas |
| **Ahorro** | **67%** |

### Lecciones

1. **Diseño primero**: Backend Architect antes de código acelera todo
2. **Iterar con contexto**: Segunda iteración con más contexto fue mejor
3. **Security audit crítico**: Detectó 2 issues que no vi
4. **Testing automatizado**: Agente generó tests que no habría pensado
```

---

## 4. METRICS.md - Métricas Globales

**Ubicación**: `docs/agents/METRICS.md`

```markdown
# Métricas de Uso de Agentes IA

## Resumen Ejecutivo

Desarrollo con 6 agentes especializados logró **62.5% de ahorro** vs desarrollo tradicional.

## Estadísticas Globales

| Métrica | Valor |
|---------|-------|
| Tiempo total | 3 semanas |
| Tiempo sin IA (estimado) | 8 semanas |
| Ahorro | 62.5% |
| Líneas generadas | ~8,500 |
| Líneas modificadas | ~2,100 (25%) |
| Líneas rechazadas | ~850 (10%) |
| Tests generados | 147 |
| Prompts totales | 203 |

## Desglose por Agente

### Backend Architect
- Prompts: 23
- Tiempo ahorrado: ~10 horas
- Contribución: Diseño, ADRs

### FastAPI Specialist
- Prompts: 67
- Código generado: ~3,200 líneas
- Tiempo ahorrado: ~25 horas
- Contribución: Endpoints, validación

[... resto de agentes ...]

## ROI

- Tiempo invertido en prompts: 30 horas
- Tiempo ahorrado: 81 horas
- **ROI: 270%**
```

---

## 5. Workflows Estándar

**Ubicación**: `docs/agents/workflows/feature-workflow.md`

```markdown
# Workflow Estándar para Features

## Proceso de 5 Pasos

1. **Diseño** (Backend Architect)
   - Input: Requisitos de la feature
   - Output: Arquitectura, modelos, flujos

2. **Implementación** (Specialist correspondiente)
   - Input: Diseño del paso 1
   - Output: Código funcional

3. **Security Review** (Security Auditor)
   - Input: Código del paso 2
   - Output: Issues + recomendaciones

4. **Testing** (Test Strategist)
   - Input: Código + issues resueltos
   - Output: Tests completos

5. **Validación Manual**
   - Input: Todo lo anterior
   - Output: Código aprobado

## Ejemplo

Ver [examples/feature-authentication.md](../examples/feature-authentication.md)
```

---

## Tips para Documentar Efectivamente

### 1. Documenta en Tiempo Real

❌ **Mal**: Dejar documentación para el final  
✅ **Bien**: Documentar cada agente cuando lo usas

**Por qué**: Recordarás contexto, decisiones, iteraciones.

### 2. Sé Específico con Prompts

❌ **Mal**: "Crea autenticación JWT"  
✅ **Bien**: 
```
Diseña autenticación JWT para FastAPI con:
- Contexto: [tu app]
- Stack: [tecnologías]
- Requisitos: [lista específica]
- Restricciones: [limitaciones]
```

### 3. Documenta Qué NO Usaste

Tan importante como qué usaste es qué rechazaste y **por qué**.

**Ejemplo**:
```
❌ Rechazado: OAuth social login
Razón: Fuera de scope MVP, añade complejidad (Passport.js)
Decisión: Implementar en v1.1
```

### 4. Métricas Reales, No Inventadas

❌ **Mal**: "Ahorré mucho tiempo"  
✅ **Bien**: "Implementación tomó 8 horas vs 24 estimadas (67% ahorro)"

### 5. Atribución Clara

En commits de Git:

```bash
git commit -m "feat(auth): implement JWT authentication

Generated with assistance from FastAPI Specialist agent.
Manual validation and security hardening added.

🤖 Co-Authored-By: AI Agent"
```

---

## Checklist de Documentación de Agentes

### Mínimo (para aprobar)

- [ ] Documentados ≥ 3 agentes
- [ ] 1 ejemplo completo de feature
- [ ] Métricas básicas (tiempo ahorrado)
- [ ] Prompts mencionados

### Recomendado (para nota alta)

- [ ] Documentados 6 agentes
- [ ] 2-3 ejemplos completos
- [ ] METRICS.md con ROI calculado
- [ ] Workflows estándar documentados
- [ ] Decisiones (qué se implementó/modificó/rechazó)
- [ ] Validación manual documentada

### Excelente (para sobresaliente)

- [ ] Todo lo anterior +
- [ ] Iteraciones documentadas
- [ ] Lecciones aprendidas por agente
- [ ] Comparaciones antes/después
- [ ] Diagrams de workflows
- [ ] Atribución en commits Git

---

## Errores Comunes

### Error 1: Documentación Genérica

❌ **Mal**:
```
Usé Claude para generar código.
```

✅ **Bien**:
```
Agente: FastAPI Specialist
Prompt: [prompt específico]
Código generado: 600 líneas
Usado: 60%, Modificado: 30%, Rechazado: 10%
Tiempo ahorrado: 8 horas
```

### Error 2: Sin Validación Manual

❌ **Mal**:
```
El agente generó el código y lo usé.
```

✅ **Bien**:
```
Validación manual:
- [x] Revisé línea por línea
- [x] Ejecuté 15 tests
- [x] Audit de seguridad con Bandit
- [x] Performance: < 200ms response time
```

### Error 3: Sin Contexto de Decisiones

❌ **Mal**:
```
Usé PostgreSQL.
```

✅ **Bien**:
```
Decisión: PostgreSQL vs MongoDB

Prompt al Backend Architect:
[prompt pidiendo comparación]

Respuesta:
- PostgreSQL: ACID, relaciones, JSON support
- MongoDB: Flexible, escalabilidad horizontal

Decisión: PostgreSQL
Razón: Relaciones complejas críticas (users ↔ projects ↔ tasks)
Trade-off: Esquema rígido (aceptable)
Ver: ADR-001
```

---

## Conclusión

La documentación de agentes IA es:
- ✅ **Transparente**: Cualquiera puede reproducir tu proceso
- ✅ **Educativa**: Documenta tu aprendizaje
- ✅ **Profesional**: Demuestra pensamiento crítico
- ✅ **Diferenciadora**: 20% de tu nota

**Invierte tiempo en documentar bien**. Es tan importante como el código.

---

**Última actualización**: Enero 2025  
**Versión**: 1.0
