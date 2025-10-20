# Linear Issues - Master Plan

**Proyecto**: Master Desarrollo con IA
**Fecha**: 2025-01-18
**Estado**: Pendiente de creación en Linear

Este documento lista TODAS las issues necesarias para completar el Master, organizadas por módulo, prioridad y tipo.

---

## Resumen Ejecutivo

**Total de issues**: 42
- **Críticas** (P0): 8 issues
- **Altas** (P1): 18 issues
- **Medias** (P2): 12 issues
- **Bajas** (P3): 4 issues

**Por tipo**:
- Content Creation: 28 issues
- AI Integration: 10 issues
- Bug Fix: 3 issues
- Documentation: 1 issue

**Por módulo**:
- Módulo 1: 4 issues
- Módulo 2: 6 issues
- Módulo 3: 7 issues
- Módulo 4: 8 issues
- Módulo 5: 6 issues
- AI Dev Academy Game: 4 issues
- Fixes & Improvements: 7 issues

---

## Labels a Crear en Linear

```
Módulos:
- module-0 (verde)
- module-1 (azul)
- module-2 (violeta)
- module-3 (naranja)
- module-4 (rojo)
- module-5 (rosa)

Tipo:
- content-creation (amarillo)
- ai-integration (cyan)
- bug-fix (rojo)
- documentation (gris)
- game (morado)

Prioridad:
- P0-critical (rojo oscuro)
- P1-high (naranja)
- P2-medium (amarillo)
- P3-low (verde)

Estimación:
- 1-2h
- 3-4h
- 5-8h
- 1-2d
- 3-5d
- 1w+
```

---

## MÓDULO 1 - Fundamentos + IA Assistant (4 issues)

### M1-1: Integrar AI Assistant en Clase 1 (Introducción a Python)
**Prioridad**: P1 (Alta)
**Labels**: `module-1`, `ai-integration`
**Estimación**: 3-4h

**Descripción**:
Añadir 40% de contenido AI a Clase 1 de Módulo 1.

**Tareas**:
- [ ] Sección: "Python Manual vs AI-Assisted" (30 min)
- [ ] Ejercicio: Generar función con Claude Code, luego implementar manualmente
- [ ] Sección: "Debugging con IA" (20 min)
- [ ] Ejercicio: IA detecta bugs en código, estudiante los corrige
- [ ] Sección: "Refactoring asistido" (20 min)
- [ ] Proyecto integrado: CLI app con y sin IA

**Acceptance Criteria**:
- 40% del contenido menciona/usa AI
- Ejercicios comparativos (manual vs IA)
- Estudiante aprende cuándo usar IA vs manual

---

### M1-2: Integrar AI Assistant en Clase 2 (Testing con Pytest)
**Prioridad**: P1 (Alta)
**Labels**: `module-1`, `ai-integration`
**Estimación**: 3-4h

**Descripción**:
Añadir AI integration a testing workflow.

**Tareas**:
- [ ] Sección: "Generar tests con IA" (30 min)
- [ ] Usar Test Coverage Strategist agent
- [ ] Ejercicio: IA genera tests, estudiante valida
- [ ] Sección: "Edge cases con IA" (20 min)
- [ ] Proyecto: Alcanzar 80% coverage con asistencia de IA

**Acceptance Criteria**:
- Test Coverage Strategist agent integrado
- Workflow: Manual → IA → Validación
- 80%+ coverage en proyecto

---

### M1-3: Integrar AI en Clase 3 (Estructura de Proyectos)
**Prioridad**: P2 (Media)
**Labels**: `module-1`, `ai-integration`
**Estimación**: 2-3h

**Tareas**:
- [ ] Sección: "IA para diseñar estructura de carpetas"
- [ ] Usar Clean Architecture Enforcer
- [ ] Ejercicio: IA sugiere estructura, estudiante decide

---

### M1-4: Integrar AI en Clase 4 (Proyecto Final Módulo 1)
**Prioridad**: P2 (Media)
**Labels**: `module-1`, `ai-integration`
**Estimación**: 2-3h

**Tareas**:
- [ ] Workflow de proyecto con agentes
- [ ] Documentar qué partes usaron IA
- [ ] Validación de código generado

---

## MÓDULO 2 - Arquitectura + Agent Orchestration (6 issues)

### M2-1: Completar Clase 1 (Introducción a FastAPI)
**Prioridad**: P0 (Crítica)
**Labels**: `module-2`, `content-creation`
**Estimación**: 5-8h

**Descripción**:
Clase 1 solo tiene notas (outline). Crear contenido completo similar a otras clases.

**Tareas**:
- [ ] Crear contenido completo (~6 horas material)
- [ ] Instalación FastAPI desde cero
- [ ] Primer endpoint Hello World
- [ ] Request/Response models con Pydantic
- [ ] Ejercicios prácticos (mínimo 5)
- [ ] Proyecto final de clase
- [ ] Integrar 40% AI content desde el inicio

**Acceptance Criteria**:
- Archivo .md completo (similar a Clase 2)
- 6 horas de contenido estructurado
- Ejercicios con soluciones
- 40% AI integration

---

### M2-2: Integrar AI en Clase 2 (CRUD con FastAPI)
**Prioridad**: P1 (Alta)
**Labels**: `module-2`, `ai-integration`
**Estimación**: 3-4h

**Tareas**:
- [ ] Sección: Generar CRUD endpoints con IA
- [ ] Usar Clean Architecture Enforcer
- [ ] Workflow: Diseño → IA genera → Validación

---

### M2-3: Integrar AI en Clase 3 (Validación con Pydantic)
**Prioridad**: P1 (Alta)
**Labels**: `module-2`, `ai-integration`
**Estimación**: 3-4h

**Tareas**:
- [ ] IA genera Pydantic models
- [ ] Estudiante valida validaciones
- [ ] Edge cases con IA

---

### M2-4: Integrar AI en Clase 4 (Repository Pattern)
**Prioridad**: P1 (Alta)
**Labels**: `module-2`, `ai-integration`
**Estimación**: 3-4h

**Tareas**:
- [ ] Clean Architecture Enforcer guía separación
- [ ] IA genera interfaces/protocols
- [ ] Estudiante implementa concrete classes

---

### M2-5: Integrar AI en Clase 5 (Testing de APIs)
**Prioridad**: P1 (Alta)
**Labels**: `module-2`, `ai-integration`
**Estimación**: 3-4h

**Tareas**:
- [ ] Test Coverage Strategist para API tests
- [ ] IA genera integration tests
- [ ] Estudiante valida y extiende

---

### M2-6: Integrar AI en Clase 6 (Proyecto Final Módulo 2)
**Prioridad**: P2 (Media)
**Labels**: `module-2`, `ai-integration`
**Estimación**: 2-3h

**Tareas**:
- [ ] Orquestación multi-agente
- [ ] Workflow completo documentado
- [ ] Validación de arquitectura

---

## MÓDULO 3 - Seguridad + IA con Criterio (7 issues)

### M3-1: Integrar AI en Clase 1 (Introducción a Seguridad)
**Prioridad**: P1 (Alta)
**Labels**: `module-3`, `ai-integration`
**Estimación**: 3-4h

**Tareas**:
- [ ] Sección: "IA genera código inseguro - aprende a detectarlo"
- [ ] Security Hardening Mentor introducción
- [ ] Ejercicios de detección de vulnerabilidades

---

### M3-2: Integrar AI en Clase 2 (OWASP Top 10)
**Prioridad**: P0 (Crítica)
**Labels**: `module-3`, `ai-integration`, `security`
**Estimación**: 4-5h

**Descripción**:
CRÍTICO: Enseñar a auditar código generado por IA.

**Tareas**:
- [ ] Security Hardening Mentor en cada vulnerabilidad OWASP
- [ ] Ejercicio: IA genera código vulnerable, estudiante detecta
- [ ] Pattern: Vulnerable → IA explica → Fix → Prevención

**Acceptance Criteria**:
- Security Mentor integrado en 10 secciones OWASP
- Ejercicios prácticos de detección
- Checklist de auditoría de código IA

---

### M3-3 a M3-7: Integrar AI en Clases 3-7
**Prioridad**: P1 (Alta) cada una
**Labels**: `module-3`, `ai-integration`
**Estimación**: 3-4h cada una

**Clases**:
- M3-3: Clase 3 (Validación de Inputs)
- M3-4: Clase 4 (JWT Authentication)
- M3-5: Clase 5 (HTTPS y Secrets)
- M3-6: Clase 6 (Testing de Seguridad)
- M3-7: Clase 7 (Observability con Sentry)

**Tareas comunes**:
- [ ] Security Hardening Mentor en cada clase
- [ ] IA genera código, estudiante audita
- [ ] Checklist de seguridad

---

## MÓDULO 4 - Infraestructura + AI DevOps (8 issues)

### M4-1: Integrar AI en Clase 1 (Introducción a Docker)
**Prioridad**: P2 (Media)
**Labels**: `module-4`, `ai-integration`
**Estimación**: 2-3h

**Tareas**:
- [ ] IA genera Dockerfiles
- [ ] Estudiante optimiza
- [ ] Best practices con IA

---

### M4-2: Integrar AI en Clase 2 (Tu API en un contenedor)
**Prioridad**: P2 (Media)
**Labels**: `module-4`, `ai-integration`
**Estimación**: 2-3h

**Tareas**:
- [ ] IA genera docker-compose
- [ ] Troubleshooting con IA
- [ ] Multi-stage builds

---

### M4-3: Crear Clase 3 (Base de Datos con SQLAlchemy)
**Prioridad**: P0 (Crítica)
**Labels**: `module-4`, `content-creation`
**Estimación**: 1-2 días

**Descripción**:
Clase completamente faltante. Crítica para proyecto real.

**Tareas**:
- [ ] Introducción a SQLAlchemy 2.0
- [ ] Modelos ORM (declarative base)
- [ ] Relaciones (one-to-many, many-to-many)
- [ ] Queries con ORM
- [ ] Integración con FastAPI
- [ ] Session management
- [ ] Ejercicios prácticos (5+)
- [ ] Proyecto: Migrar Repository de JSON a DB
- [ ] AI Integration (40%): IA genera models, estudiante valida

**Acceptance Criteria**:
- 6 horas de contenido
- SQLAlchemy 2.0 syntax
- Integración completa con FastAPI
- 40% AI content

---

### M4-4: Crear Clase 4 (Migraciones con Alembic)
**Prioridad**: P0 (Crítica)
**Labels**: `module-4`, `content-creation`
**Estimación**: 1-2 días

**Descripción**:
Migraciones de BD son esenciales para producción.

**Tareas**:
- [ ] Setup Alembic
- [ ] Crear primera migración
- [ ] Migrations workflow (upgrade/downgrade)
- [ ] Migrations en producción
- [ ] Rollback strategies
- [ ] Ejercicios: Modificar schema con migrations
- [ ] AI Integration: IA genera migrations, estudiante valida

**Acceptance Criteria**:
- Alembic completamente explicado
- Workflow producción-ready
- 40% AI integration

---

### M4-5: Crear Clase 5 (Deploy en Cloud - Railway/Render)
**Prioridad**: P1 (Alta)
**Labels**: `module-4`, `content-creation`
**Estimación**: 1-2 días

**Tareas**:
- [ ] Preparar app para producción
- [ ] Environment variables
- [ ] Deploy a Railway
- [ ] Deploy a Render (alternativa)
- [ ] PostgreSQL en cloud
- [ ] CI/CD básico
- [ ] Monitoring
- [ ] AI Integration: IA genera configs, estudiante deploya

---

### M4-6: Crear Clase 6 (LangChain para Agentes)
**Prioridad**: P2 (Media)
**Labels**: `module-4`, `content-creation`, `ai-integration`
**Estimación**: 1-2 días

**Descripción**:
Introducción a frameworks de agentes.

**Tareas**:
- [ ] Introducción a LangChain
- [ ] Chains básicos
- [ ] Agents y Tools
- [ ] Memory en agentes
- [ ] RAG básico
- [ ] Proyecto: Agente que asiste desarrollo
- [ ] 50%+ AI content (es clase sobre AI)

---

### M4-7: Crear Clase 7 (AI DevOps - Deployment Automation)
**Prioridad**: P2 (Media)
**Labels**: `module-4`, `content-creation`, `ai-integration`
**Estimación**: 1-2 días

**Tareas**:
- [ ] GitHub Actions con IA
- [ ] IA genera workflows
- [ ] Auto-deployment con validación IA
- [ ] Monitoring con IA
- [ ] 50% AI content

---

### M4-8: Crear Clase 8 (Proyecto Final Módulo 4)
**Prioridad**: P1 (Alta)
**Labels**: `module-4`, `content-creation`
**Estimación**: 3-5h

**Tareas**:
- [ ] API completa con DB
- [ ] Migrations
- [ ] Deployed en cloud
- [ ] CI/CD funcional
- [ ] Documentado con agentes usados

---

## MÓDULO 5 - Full-Stack + Agent Mastery (6 issues)

### M5-1: Crear Clase 1 (Introducción a React + FastAPI)
**Prioridad**: P1 (Alta)
**Labels**: `module-5`, `content-creation`
**Estimación**: 1-2 días

**Tareas**:
- [ ] Setup React + Vite
- [ ] Conectar con FastAPI backend
- [ ] CORS configuration
- [ ] Primer componente + API call
- [ ] State management (Zustand/Context)
- [ ] AI: IA genera componentes React, estudiante integra

---

### M5-2: Crear Clase 2 (Full-Stack CRUD)
**Prioridad**: P1 (Alta)
**Labels**: `module-5`, `content-creation`
**Estimación**: 1-2 días

**Tareas**:
- [ ] CRUD completo frontend
- [ ] Forms con validación
- [ ] Error handling
- [ ] Loading states
- [ ] AI: IA genera boilerplate, estudiante customiza

---

### M5-3: Crear Clase 3 (Autenticación Full-Stack)
**Prioridad**: P1 (Alta)
**Labels**: `module-5`, `content-creation`
**Estimación**: 1-2 días

**Tareas**:
- [ ] Login/Logout frontend
- [ ] JWT storage (localStorage vs httpOnly cookies)
- [ ] Protected routes
- [ ] Auth context
- [ ] Security Hardening Mentor validation

---

### M5-4: Crear Clase 4 (Despliegue Full-Stack)
**Prioridad**: P1 (Alta)
**Labels**: `module-5`, `content-creation`
**Estimación**: 1-2 días

**Tareas**:
- [ ] Build frontend (Vite)
- [ ] Deploy frontend (Vercel/Netlify)
- [ ] Deploy backend (Railway/Render)
- [ ] Environment variables
- [ ] Production checklist

---

### M5-5: Crear Clase 5 (Agent Orchestration Mastery)
**Prioridad**: P0 (Crítica)
**Labels**: `module-5`, `content-creation`, `ai-integration`
**Estimación**: 2-3 días

**Descripción**:
**Culminación del master** - Orquestar equipo de agentes para proyecto grande.

**Tareas**:
- [ ] Agent Team Canvas (framework)
- [ ] Dividir proyecto en sub-tareas
- [ ] Asignar agente a cada tarea
- [ ] Workflow multi-agente
- [ ] Validación y integración
- [ ] Proyecto: Aplicación completa con agentes
- [ ] 60%+ AI content

**Acceptance Criteria**:
- Framework de orquestación claro
- Proyecto grande completado con agentes
- Documentación de workflow
- "Ejército de agentes" en acción

---

### M5-6: Crear Clase 6 (Proyecto Final - Master Project)
**Prioridad**: P0 (Crítica)
**Labels**: `module-5`, `content-creation`
**Estimación**: 3-5 días

**Descripción**:
Proyecto integrador final del master.

**Tareas**:
- [ ] Definir proyecto (e-commerce, SaaS, etc.)
- [ ] Requisitos completos
- [ ] Arquitectura completa
- [ ] Full-stack con todos los módulos integrados
- [ ] Team de agentes documentado
- [ ] Deployment en producción
- [ ] Presentación final

**Acceptance Criteria**:
- Proyecto producción-ready
- Todos los conceptos del master integrados
- Documentación completa (ADRs, arquitectura, agentes)
- Video demo

---

## AI DEV ACADEMY GAME (4 issues)

### GAME-1: Completar Backend FastAPI
**Prioridad**: P2 (Media)
**Labels**: `game`, `content-creation`
**Estimación**: 5-8h

**Tareas**:
- [ ] Completar routes (player, progress, achievements, minigames)
- [ ] Implementar XP service
- [ ] Content loader (parsear módulos existentes)
- [ ] Achievement checker
- [ ] Tests básicos

---

### GAME-2: Crear Frontend React
**Prioridad**: P2 (Media)
**Labels**: `game`, `content-creation`
**Estimación**: 1-2 días

**Tareas**:
- [ ] Setup Vite + React + TypeScript
- [ ] Dashboard component
- [ ] Workspace visualization
- [ ] Module selector
- [ ] Class viewer
- [ ] Progress bars y stats
- [ ] Achievement popups

---

### GAME-3: Implementar Bug Hunt Mini-Game
**Prioridad**: P3 (Baja)
**Labels**: `game`, `content-creation`
**Estimación**: 5-8h

**Tareas**:
- [ ] Generador de código con bugs
- [ ] UI de selección de bugs
- [ ] Timer y scoring
- [ ] Leaderboard
- [ ] XP rewards

---

### GAME-4: Deploy Juego en Producción
**Prioridad**: P3 (Baja)
**Labels**: `game`, `content-creation`
**Estimación**: 3-4h

**Tareas**:
- [ ] Deploy backend a Railway
- [ ] Deploy frontend a Vercel
- [ ] Configurar CORS producción
- [ ] Testing end-to-end

---

## FIXES & IMPROVEMENTS (7 issues)

### FIX-1: Renombrar Tests de Módulos 3-4
**Prioridad**: P2 (Media)
**Labels**: `bug-fix`
**Estimación**: 1-2h

**Descripción**:
Tests están mal nombrados (`test_crear_tarea_clase7.py` en todas las clases).

**Tareas**:
- [ ] Renombrar a `test_crear_tarea_clase{X}_mod{Y}.py`
- [ ] Actualizar imports si necesario
- [ ] Verificar tests siguen pasando

---

### FIX-2: Actualizar CI Matrix
**Prioridad**: P1 (Alta)
**Labels**: `bug-fix`
**Estimación**: 1-2h

**Descripción**:
CI solo testea 1-2 clases. Añadir todas las clases implementadas.

**Tareas**:
- [ ] Listar todas las clases con tests
- [ ] Actualizar `.github/workflows/ci.yml` matrix
- [ ] Actualizar `.github/workflows/ci_quality.yml` matrix
- [ ] Verificar workflows pasan

---

### FIX-3: Añadir Glossaries Faltantes
**Prioridad**: P3 (Baja)
**Labels**: `documentation`
**Estimación**: 2-3h

**Tareas**:
- [ ] Crear glossary Módulo 3 Clase 1
- [ ] Crear glossary Módulo 3 Clase 7
- [ ] Crear glossary Módulo 4 Clase 1
- [ ] Añadir `.md` extension a 4 glossaries sin extensión

---

### FIX-4: Añadir Async/Await Teaching
**Prioridad**: P2 (Media)
**Labels**: `module-2`, `content-creation`
**Estimación**: 5-8h

**Descripción**:
Gap crítico: FastAPI es async pero no enseñamos async/await.

**Tareas**:
- [ ] Crear Módulo 2 Clase 3.5 "Async Python"
- [ ] Conceptos: event loop, coroutines, async/await
- [ ] Comparación sync vs async
- [ ] Async en FastAPI
- [ ] Ejercicios prácticos
- [ ] 40% AI integration

---

### FIX-5: Añadir Error Handling Patterns
**Prioridad**: P2 (Media)
**Labels**: `module-2`, `content-creation`
**Estimación**: 3-4h

**Tareas**:
- [ ] Custom exceptions
- [ ] HTTPException handlers
- [ ] Global exception handlers
- [ ] Error responses structure
- [ ] Logging de errores
- [ ] Integrar en Módulo 2 Clase 4 o 5

---

### FIX-6: Crear Module-Level READMEs
**Prioridad**: P3 (Baja)
**Labels**: `documentation`
**Estimación**: 2-3h

**Tareas**:
- [ ] README para Módulo 1
- [ ] README para Módulo 2
- [ ] README para Módulo 3
- [ ] Overview, objetivos, estructura

---

### FIX-7: Actualizar CLAUDE.md con Estado Final
**Prioridad**: P3 (Baja)
**Labels**: `documentation`
**Estimación**: 1h

**Tareas**:
- [ ] Actualizar completion status después de completar módulos
- [ ] Remover "gaps" section cuando se completen
- [ ] Añadir "how to run game" section

---

## Roadmap de Implementación

### Sprint 1 (1-2 semanas): Críticos
```
P0 Issues (8 total):
- M2-1: Completar Clase 1 FastAPI
- M3-2: Integrar Security Mentor en OWASP
- M4-3: Crear Clase 3 SQLAlchemy
- M4-4: Crear Clase 4 Alembic
- M5-5: Agent Orchestration Mastery
- M5-6: Proyecto Final Master
```

### Sprint 2 (2-3 semanas): AI Integration Alta Prioridad
```
P1 Issues (18 total):
- Todas las integraciones AI de Módulos 1-3
- M4-5: Deploy en Cloud
- M4-8: Proyecto Final Módulo 4
- M5-1 a M5-4: Clases Full-Stack
- FIX-2: Update CI
```

### Sprint 3 (1-2 semanas): Media Prioridad + Game
```
P2 Issues (12 total):
- Integraciones AI restantes
- M4-1, M4-2, M4-6, M4-7
- GAME-1, GAME-2
- FIX-1, FIX-4, FIX-5
```

### Sprint 4 (1 semana): Low Priority + Polish
```
P3 Issues (4 total):
- GAME-3, GAME-4
- FIX-3, FIX-6, FIX-7
```

---

## Siguiente Paso

**Usar linear-project-manager agent** para crear todas estas issues en Linear con:
- Title apropiado
- Description completa
- Labels correctos
- Priority asignada
- Estimate incluido
- Linked al proyecto "Master desarrollo con IA"

**Comando**:
```
@linear-project-manager

Crea todas las issues listadas en LINEAR_ISSUES_MASTER_PLAN.md en el proyecto "Master desarrollo con IA".

Para cada issue:
1. Usar title del header (ej: "M1-1: Integrar AI Assistant en Clase 1")
2. Description = toda la sección (Descripción, Tareas, Acceptance Criteria)
3. Asignar labels según especificado
4. Asignar priority (P0, P1, P2, P3)
5. Asignar estimate
6. Vincular al proyecto correcto

Confirma después de crear cada batch de 5 issues.
```
