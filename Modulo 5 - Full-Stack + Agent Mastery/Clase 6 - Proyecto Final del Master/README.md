# Clase 6 - Proyecto Final del Master

## Índice
1. [Introducción](#introducción)
2. [¿Por qué un Proyecto Final?](#por-qué-un-proyecto-final)
3. [Requisitos del Proyecto](#requisitos-del-proyecto)
4. [Estructura del Portfolio](#estructura-del-portfolio)
5. [Guía de Selección de Proyecto](#guía-de-selección-de-proyecto)
6. [Documentación Requerida](#documentación-requerida)
7. [Documentación de Agentes IA](#documentación-de-agentes-ia)
8. [Presentación del Proyecto](#presentación-del-proyecto)
9. [Evaluación](#evaluación)
10. [Timeline Sugerido](#timeline-sugerido)
11. [Ejemplos de Excelencia](#ejemplos-de-excelencia)
12. [Recursos y Herramientas](#recursos-y-herramientas)
13. [Checklist de Entrega](#checklist-de-entrega)
14. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## Introducción

¡Bienvenido a la última clase del Master en Desarrollo Asistido por IA! 🎓

Este es el momento de demostrar todo lo que has aprendido construyendo un **proyecto completo y profesional** que servirá como:

- **Portfolio profesional**: Algo que mostrar en entrevistas técnicas
- **Prueba de concepto**: Demostración de que dominas el stack completo
- **Certificación práctica**: Evidencia tangible de tus habilidades
- **Maestría en IA**: Documentación de cómo orquestas agentes especializados

**Lo que NO es este proyecto**:
- ❌ Un tutorial más
- ❌ Un ejercicio guiado paso a paso
- ❌ Una copia de proyectos anteriores
- ❌ Solo código sin documentación

**Lo que SÍ debe ser**:
- ✅ Un proyecto original y completo
- ✅ Arquitectura limpia y profesional
- ✅ Documentación exhaustiva (código + agentes)
- ✅ Despliegue en producción funcional
- ✅ Presentación clara de tu trabajo

---

## ¿Por qué un Proyecto Final?

### La Brecha entre Saber y Demostrar

Muchos desarrolladores saben programar, pero pocos pueden:
1. **Diseñar** una arquitectura escalable desde cero
2. **Implementar** features complejas de forma profesional
3. **Documentar** decisiones técnicas y arquitectónicas
4. **Desplegar** aplicaciones en producción con confianza
5. **Orquestar** equipos de agentes IA especializados

Este proyecto final te obliga a hacer todo eso.

### El Valor de un Portfolio Técnico

Según estudios de reclutamiento en tech:

- **87%** de recruiters revisan el GitHub antes de una entrevista
- **73%** consideran un proyecto completo más valioso que certificados teóricos
- **91%** valoran documentación clara sobre líneas de código

**Un buen proyecto final puede**:
- Conseguirte entrevistas en empresas top
- Diferenciarte de otros candidatos
- Negociar mejor salario (demuestras senior skills)
- Servir de base para startups o freelancing

### Maestría en Agentes IA: Tu Ventaja Competitiva

La capacidad de **orquestar agentes IA especializados** es una habilidad emergente que muy pocos desarrolladores dominan:

- **Productividad 10x**: Completar en 1 semana lo que antes tomaba 2 meses
- **Calidad profesional**: Agentes especializados en seguridad, testing, arquitectura
- **Escalabilidad individual**: "Un desarrollador con un ejército de agentes"

**Este proyecto debe demostrar** que no solo usas IA para autocompletar código, sino que:
1. Diseñas workflows de agentes especializados
2. Documentas decisiones tomadas por agentes
3. Auditas y validas código generado por IA
4. Mejoras iterativamente tus prompts y agentes

---

## Requisitos del Proyecto

### Requisitos Mínimos (para aprobar)

Tu proyecto **DEBE** incluir:

#### 1. Backend con FastAPI (30% de la nota)
- ✅ Mínimo 8 endpoints RESTful
- ✅ Arquitectura limpia (Repository + Service + API layers)
- ✅ Autenticación JWT
- ✅ Validación con Pydantic
- ✅ Base de datos (SQLAlchemy + Alembic)
- ✅ Tests con cobertura ≥ 80%
- ✅ Manejo de errores profesional

#### 2. Frontend con React (25% de la nota)
- ✅ Mínimo 5 pantallas/vistas
- ✅ Integración completa con el backend
- ✅ Gestión de estado (Context API / Zustand / React Query)
- ✅ TypeScript obligatorio
- ✅ Diseño responsive (mobile + desktop)
- ✅ Formularios con validación
- ✅ Manejo de errores y loading states

#### 3. Infraestructura (15% de la nota)
- ✅ Dockerfile + docker-compose
- ✅ Variables de entorno configurables
- ✅ Despliegue en producción funcional (Render, Railway, Vercel, etc.)
- ✅ CI/CD pipeline (GitHub Actions)
- ✅ Health checks y logging

#### 4. Documentación (20% de la nota)
- ✅ README completo con setup instructions
- ✅ Mínimo 3 ADRs (Architecture Decision Records)
- ✅ Diagramas de arquitectura
- ✅ API documentation (Swagger/OpenAPI)
- ✅ Documentación de agentes IA utilizados

#### 5. Presentación (10% de la nota)
- ✅ Video demo de 5-10 minutos
- ✅ Slides explicando arquitectura y decisiones
- ✅ Demostración en vivo del proyecto desplegado

### Requisitos Avanzados (para destacar)

Si quieres una calificación sobresaliente (9-10), añade:

- 🌟 **Testing avanzado**: E2E tests con Playwright/Cypress
- 🌟 **Observabilidad**: Sentry, logging estructurado, métricas
- 🌟 **Performance**: Caché (Redis), optimizaciones, lazy loading
- 🌟 **Seguridad**: Rate limiting, CORS, sanitización, OWASP compliance
- 🌟 **DevOps**: Multi-stage Docker builds, database backups, monitoring
- 🌟 **UX avanzada**: Animaciones, dark mode, accesibilidad (a11y)
- 🌟 **Features complejas**: WebSockets, file uploads, scheduled tasks
- 🌟 **Orquestación IA**: Uso de 5+ agentes especializados con workflows documentados

---

## Estructura del Portfolio

Tu portfolio **DEBE** incluir estas secciones en el README principal. Ver [PORTFOLIO_TEMPLATE.md](PORTFOLIO_TEMPLATE.md) para template completo copy-paste.

### Secciones Obligatorias

1. **Introducción y Propuesta de Valor**
   - Problema que resuelve
   - Solución propuesta
   - Diferenciadores clave

2. **Tech Stack y Arquitectura**
   - Badges con tecnologías utilizadas
   - Justificación de cada elección
   - Diagrama de arquitectura (Mermaid o imagen)

3. **Features Principales**
   - Lista de funcionalidades con screenshots
   - Descripción de cada feature
   - Valor que aporta al usuario

4. **Getting Started**
   - Prerrequisitos claros
   - Instrucciones de instalación paso a paso
   - Configuración de variables de entorno
   - Troubleshooting de problemas comunes

5. **Testing y CI/CD**
   - Cómo ejecutar tests
   - Reporte de cobertura
   - Pipeline de CI/CD explicado

6. **Documentación de Agentes IA**
   - Tabla con agentes utilizados y sus roles
   - Workflow de desarrollo con agentes
   - Métricas de productividad
   - Ejemplos de features desarrolladas con IA

7. **Deployment**
   - URLs de producción (frontend + backend)
   - Credenciales de demo
   - Stack de deployment explicado

8. **Roadmap**
   - Features actuales
   - Próximas versiones planificadas
   - Cómo contribuir (si es open source)

9. **Licencia y Contacto**
   - Licencia MIT (recomendada)
   - Tus datos de contacto
   - Links a LinkedIn, portfolio personal, etc.

---

## Guía de Selección de Proyecto

### ¿Qué Proyecto Elegir?

La decisión más importante. Usa este framework:

#### Criterio 1: Pasión Personal (40%)

**Pregúntate**:
- ¿Usaría yo esta aplicación?
- ¿Me emociona trabajar en esto 3-4 semanas?
- ¿Aprenderé algo que quiero saber?

**Por qué importa**: Vas a pasar 80+ horas en este proyecto. Si no te apasiona, se notará en la calidad.

#### Criterio 2: Complejidad Técnica (30%)

**Complejidad ideal** (marca mínimo 6):
- [ ] Backend con ≥ 8 endpoints
- [ ] Frontend con ≥ 5 pantallas
- [ ] Autenticación JWT + roles
- [ ] Base de datos relacional (≥ 4 tablas con relaciones)
- [ ] Operaciones CRUD complejas
- [ ] Validaciones de negocio no triviales
- [ ] Integración con API externa
- [ ] File uploads o procesamiento
- [ ] Notificaciones o emails
- [ ] Real-time features

**Señales de alerta**:
- 🚨 **Muy simple**: "Un blog estático con Markdown"
- 🚨 **Muy complejo**: "Un clon de AWS con Kubernetes"

#### Criterio 3: Valor de Portfolio (20%)

**Buenos proyectos**:
- ✅ SaaS B2B: "CRM para freelancers"
- ✅ Marketplace: "Airbnb para espacios de coworking"
- ✅ Dashboard: "Analytics para e-commerce"
- ✅ Herramienta dev: "API testing tool"

**Malos proyectos**:
- ❌ Clones genéricos: "Clon de Twitter"
- ❌ Internos: "Sistema para la empresa de mi tío"
- ❌ Obsoletos: "Aplicación de DVDs"

#### Criterio 4: Viabilidad en 3-4 Semanas (10%)

**MVP scope**:
- Semana 1: Arquitectura + Backend básico + 1 feature核心
- Semana 2: Resto del backend + Frontend básico
- Semana 3: Integración + Features secundarias + Tests
- Semana 4: Polish + Documentación + Deploy + Presentación

### Proceso de Selección

1. Lista 5 ideas que te interesen
2. Califica cada una 1-10 en los 4 criterios
3. Elige la de mayor puntaje
4. Valida con mentor o peers
5. Define MVP vs nice-to-have

Ver [PROJECT_IDEAS.md](PROJECT_IDEAS.md) para 10+ ideas pre-validadas.

---

## Documentación Requerida

### 1. README.md (Obligatorio)

Ver [PORTFOLIO_TEMPLATE.md](PORTFOLIO_TEMPLATE.md) para template completo.

**Longitud mínima**: 800 líneas con screenshots

**Checklist**:
- [ ] Introducción con propuesta de valor
- [ ] Tech stack con badges y justificación
- [ ] Diagrama de arquitectura
- [ ] Features con screenshots
- [ ] Getting Started instructions
- [ ] Testing y CI/CD
- [ ] Documentación de agentes IA
- [ ] Deployment y links
- [ ] Roadmap
- [ ] Licencia y contacto

### 2. Architecture Decision Records (ADRs)

**Formato estándar**:

```markdown
# ADR-001: [Título de la Decisión]

## Estado
Aceptado | Rechazado | Deprecado

## Contexto
[Qué problema estamos resolviendo]
[Qué restricciones tenemos]

## Decisión
[Qué decidimos hacer]

## Consecuencias

### Positivas
- ✅ [Beneficio 1]
- ✅ [Beneficio 2]

### Negativas
- ⚠️ [Trade-off 1]
- ⚠️ [Trade-off 2]

## Alternativas Consideradas

### Opción A
- **Pros**: ...
- **Cons**: ...
- **¿Por qué no?**: ...

## Referencias
- [Link a documentación]
```

**ADRs mínimos requeridos** (3):
1. Elección de base de datos
2. Arquitectura de capas
3. Estrategia de autenticación

**Ubicación**: `docs/architecture/adr/`

### 3. Diagramas de Arquitectura

**Herramientas**: Mermaid, Excalidraw, Draw.io

**Diagramas mínimos** (3):
a) Arquitectura de alto nivel
b) Estructura de capas (Clean Architecture)
c) Flujo de una feature crítica (sequence diagram)

**Ubicación**: `docs/architecture/diagrams/`

### 4. API Documentation (Swagger/OpenAPI)

FastAPI lo genera automáticamente, pero debes:
- Añadir docstrings a todos los endpoints
- Documentar modelos Pydantic con `Field(..., description="...")`
- Ejemplos con `Config.schema_extra`
- Tags para agrupar endpoints
- Documentar todos los status codes

### 5. Setup y Troubleshooting

**Archivo**: `docs/SETUP.md`

Debe incluir:
- Prerrequisitos detallados (versiones específicas)
- Pasos para Windows/Mac/Linux
- Configuración de variables de entorno
- Inicialización de base de datos
- Seeds de datos de prueba
- Problemas comunes y soluciones

---

## Documentación de Agentes IA

**Sección CRÍTICA que te diferencia.**

### Estructura de Documentación

```
docs/
├── agents/
│   ├── README.md                 # Índice de agentes
│   ├── workflows/
│   │   ├── feature-workflow.md   # Workflow para features
│   │   ├── bugfix-workflow.md    # Workflow para bugs
│   │   └── refactor-workflow.md  # Workflow para refactors
│   ├── agents/
│   │   ├── backend-architect.md
│   │   ├── fastapi-specialist.md
│   │   ├── database-designer.md
│   │   ├── security-auditor.md
│   │   ├── test-strategist.md
│   │   └── frontend-coach.md
│   ├── examples/
│   │   ├── feature-authentication.md
│   │   ├── feature-dashboard.md
│   │   └── bugfix-example.md
│   └── METRICS.md                # Métricas globales
```

### Template de Documentación de Agente

```markdown
# [Nombre del Agente]

## Rol y Responsabilidades

**Especialización**: [Área de expertise]
**Responsabilidades**: [Lista de tareas]
**NO hace**: [Límites claros]

## Prompt Base

[Prompt template usado]

## Prompts Utilizados

### Prompt 1: [Nombre]
- **Fecha**: 2025-01-15
- **Contexto**: [Por qué]
- **Prompt**: [Prompt exacto]
- **Decisión**: ✅ Implementado / ⚠️ Modificado / ❌ Rechazado
- **Validación**: [Qué revisaste]

## Métricas

| Métrica | Valor |
|---------|-------|
| Prompts totales | 25 |
| Código generado | ~1,500 líneas |
| Tiempo ahorrado | 15 horas |
```

### Métricas de Agentes

Documenta en `docs/agents/METRICS.md`:

```markdown
# Métricas de Uso de Agentes IA

## Resumen Ejecutivo
- Tiempo total: 3 semanas
- Tiempo estimado sin IA: 8 semanas
- Ahorro: 62.5%
- Líneas generadas: ~8,500
- Tests generados: 147

## Desglose por Agente

[Tabla con métricas por agente]

## ROI

- Tiempo invertido en prompts: ~30 horas
- Tiempo ahorrado: ~81 horas
- ROI: 270%
```

Ver [AGENT_WORKFLOW_GUIDE.md](AGENT_WORKFLOW_GUIDE.md) para guía completa.

---

## Presentación del Proyecto

### 1. Video Demo (Obligatorio)

**Duración**: 5-10 minutos (máximo 12)

**Estructura**:
- Minuto 0-1: Hook y contexto
- Minuto 1-3: Demostración visual (app funcionando)
- Minuto 3-5: Arquitectura técnica
- Minuto 5-7: Código destacado
- Minuto 7-9: Deployment y CI/CD
- Minuto 9-10: Conclusiones

**Herramientas**: Loom, OBS Studio, Zoom

**Tips**:
- ✅ Practica 3 veces antes de grabar
- ✅ Muestra tu cara en esquina
- ✅ Habla claro y con energía
- ❌ No leas un script
- ❌ No uses jerga excesiva

### 2. Slides (Obligatorio)

**Estructura** (15-20 slides):
1. Portada
2. Problema
3. Solución
4-7. Demo Visual (screenshots)
8. Tech Stack
9. Arquitectura
10. ADR Destacado
11. Código Interesante
12-13. Agentes IA
14. Métricas IA
15. Testing y Calidad
16. Deployment
17. Desafíos
18. Aprendizajes
19. Roadmap
20. Contacto

**Herramientas**: Google Slides, Canva, Pitch

### 3. Demo en Vivo (Opcional)

Si decides hacerla:
- Practica 10 veces
- Ten el video como backup
- Reset estado (datos demo listos)
- Narra lo que haces
- No improvises rutas críticas

---

## Evaluación

Tu proyecto será evaluado sobre **100 puntos**.

Ver [RUBRICA_EVALUACION.md](RUBRICA_EVALUACION.md) para rúbrica completa.

### Distribución de Puntos

| Categoría | Puntos | Peso |
|-----------|--------|------|
| Excelencia Técnica | 40 | 40% |
| Orquestación de Agentes IA | 20 | 20% |
| Documentación | 15 | 15% |
| Presentación | 15 | 15% |
| Innovación e Impacto | 10 | 10% |
| **TOTAL** | **100** | **100%** |

### Escala de Calificación

- **90-100**: Sobresaliente (10) - Excepcional
- **80-89**: Notable (8-9) - Muy bueno
- **70-79**: Aprobado (7) - Cumple requisitos
- **60-69**: Suficiente (6) - Cumple mínimos
- **< 60**: Insuficiente - Debe rehacer

### Requisitos Mínimos para Aprobar

Debes cumplir **TODOS**:
- [ ] 8+ endpoints Backend funcionando
- [ ] 5+ pantallas Frontend
- [ ] Tests ≥ 70% cobertura
- [ ] Arquitectura en capas
- [ ] JWT autenticación
- [ ] Desplegado y accesible
- [ ] README completo
- [ ] Mínimo 2 ADRs
- [ ] Documentación básica de agentes
- [ ] Video demo 5-10 min

---

## Timeline Sugerido

### Visión General (3-4 semanas)

```
Semana 1: Diseño y Fundaciones
Semana 2: Implementación Core  
Semana 3: Features Secundarias y Tests
Semana 4: Polish, Documentación y Presentación
```

### Semana 1: Diseño y Fundaciones

**Día 1-2: Planificación**
- [ ] Elegir proyecto
- [ ] Definir MVP
- [ ] Setup repositorio Git
- [ ] Escribir ADR-001

**Día 3-4: Arquitectura**
- [ ] Diseñar arquitectura
- [ ] Diagramas
- [ ] Definir modelos de datos
- [ ] ADRs 002-003

**Día 5: Setup Inicial**
- [ ] Setup backend y frontend
- [ ] Docker Compose
- [ ] GitHub Actions básico
- [ ] Setup deployment accounts

**Entregable**: Arquitectura diseñada, ADRs, setup completo

### Semana 2: Implementación Core

**Día 1-2: Autenticación**
- [ ] Modelos de User
- [ ] Endpoints auth
- [ ] JWT middleware
- [ ] Tests ≥ 10

**Día 3-4: Funcionalidad Core**
- [ ] Modelos principales
- [ ] Migraciones Alembic
- [ ] CRUD endpoints ≥ 8
- [ ] Tests ≥ 20

**Día 5: Deployment Básico**
- [ ] Deploy backend a Render
- [ ] Deploy frontend a Vercel
- [ ] Health check
- [ ] Smoke test

**Entregable**: Backend funcionando, autenticación, desplegado

### Semana 3: Features y Tests

**Día 1-2: Features Adicionales**
- [ ] Feature secundaria 1
- [ ] Feature secundaria 2
- [ ] Integración API externa (si aplica)

**Día 3: Frontend Completo**
- [ ] Componentes React ≥ 10
- [ ] Vistas ≥ 5
- [ ] Integración con backend
- [ ] Manejo de errores

**Día 4: Testing Exhaustivo**
- [ ] Tests integración ≥ 10
- [ ] Cobertura ≥ 80%
- [ ] Security audit
- [ ] Performance testing

**Día 5: CI/CD Completo**
- [ ] GitHub Actions completo
- [ ] Pre-commit hooks
- [ ] Auto-deploy
- [ ] Monitoring (Sentry)

**Entregable**: App completa, tests ≥ 80%, CI/CD

### Semana 4: Polish y Presentación

**Día 1: Polish**
- [ ] Responsive design
- [ ] Loading states
- [ ] Mensajes de error amigables
- [ ] Accesibilidad básica

**Día 2-3: Documentación**
- [ ] README completo
- [ ] ADRs (≥ 3)
- [ ] API docs
- [ ] Docs de agentes IA
- [ ] SETUP.md
- [ ] Ejemplos de features

**Día 4: Video Demo**
- [ ] Escribir script
- [ ] Practicar 3 veces
- [ ] Grabar y editar
- [ ] Subir a YouTube/Loom

**Día 5: Entrega**
- [ ] Crear slides
- [ ] Review final
- [ ] Verificar links
- [ ] Ejecutar checklist
- [ ] **ENTREGAR**

**Entregable**: Proyecto completo, documentación, video, slides

Ver [CHECKLIST.md](CHECKLIST.md) para checklist detallado.

---

## Ejemplos de Excelencia

Ver [ejemplos/PORTFOLIO_EJEMPLO_1.md](ejemplos/PORTFOLIO_EJEMPLO_1.md) para ejemplo completo.

### Características de Proyectos Sobresalientes

**Excelencia Técnica**:
- ✨ Arquitectura limpia y separada
- ✨ Tests exhaustivos (≥ 85%)
- ✨ Security hardening
- ✨ Performance optimizada

**Documentación Excepcional**:
- ✨ README inspirador
- ✨ ADRs bien razonados (≥ 5)
- ✨ Diagramas claros
- ✨ Docs de agentes con ejemplos

**Presentación Impactante**:
- ✨ Video producido profesionalmente
- ✨ Storytelling claro
- ✨ Slides visualmente atractivas

**Innovación**:
- ✨ Solución a problema real
- ✨ Features únicas
- ✨ Uso avanzado de tecnologías

### Anti-Patrones a Evitar

- 🚨 Código sin tests (< 50%)
- 🚨 Secrets hardcodeados
- 🚨 README de 20 líneas
- 🚨 Sin documentación de agentes
- 🚨 Video sin audio o inaudible
- 🚨 Proyecto demasiado simple

---

## Recursos y Herramientas

### Documentación Oficial

**Backend**:
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)

**Frontend**:
- [React Docs](https://react.dev/)
- [TypeScript](https://www.typescriptlang.org/docs/)
- [Vite](https://vitejs.dev/guide/)

**DevOps**:
- [Docker](https://docs.docker.com/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Render](https://render.com/docs)
- [Vercel](https://vercel.com/docs)

### Herramientas

**Diagramas**:
- [Mermaid Live](https://mermaid.live/)
- [Excalidraw](https://excalidraw.com/)
- [Draw.io](https://app.diagrams.net/)

**Screenshots**:
- Cleanshot X (Mac)
- ShareX (Windows)
- Flameshot (Linux)

**Videos**:
- [Loom](https://www.loom.com/)
- [OBS Studio](https://obsproject.com/)

**Slides**:
- [Google Slides](https://slides.google.com/)
- [Canva](https://www.canva.com/presentations/)

### Servicios Deployment (Gratis)

**Backend**:
- Render - PostgreSQL incluido
- Railway - PostgreSQL, Redis
- Fly.io - Edge computing

**Frontend**:
- Vercel - Ideal para React
- Netlify - Similar a Vercel
- Cloudflare Pages - Muy rápido

**Database**:
- Render PostgreSQL (90 días)
- Neon (PostgreSQL serverless)
- PlanetScale (MySQL)

**Monitoring**:
- Sentry (Error tracking)
- UptimeRobot (Uptime monitoring)

---

## Checklist de Entrega

Ver [CHECKLIST.md](CHECKLIST.md) para checklist detallado.

### Checklist Rápido (Pre-Entrega)

#### Código
- [ ] Repositorio público en GitHub
- [ ] README completo con screenshots
- [ ] Código sin secrets hardcodeados
- [ ] `.gitignore` configurado
- [ ] Licencia MIT

#### Documentación
- [ ] Mínimo 3 ADRs
- [ ] Diagramas de arquitectura
- [ ] Documentación de agentes
- [ ] API docs (Swagger)

#### Deployment
- [ ] Backend desplegado y accesible
- [ ] Frontend desplegado y accesible
- [ ] Links funcionan
- [ ] Credenciales demo provistas

#### Presentación
- [ ] Video demo subido
- [ ] Link al video en README
- [ ] Slides en el repo

#### Tests
- [ ] Tests pasan en CI/CD
- [ ] Cobertura ≥ 70%
- [ ] GitHub Actions verde

---

## Preguntas Frecuentes

### ¿Puedo usar otro framework en lugar de FastAPI?

**No**, FastAPI es obligatorio. El master está diseñado alrededor de FastAPI.

**Excepción**: Si tienes razón muy fuerte, consúltalo ANTES de empezar.

### ¿Puedo usar Vue/Svelte en lugar de React?

**Sí, pero no recomendado**. React es el framework cubierto. Si usas otro, debes demostrar mismo nivel de maestría.

### ¿Cuántas líneas de código debería tener?

**No hay mínimo**. Calidad > cantidad.

**Referencia típica**:
- Backend: 2,000-4,000 líneas
- Frontend: 1,500-3,000 líneas
- Total: ~3,500-7,000 líneas

### ¿Qué pasa si no termino en 4 semanas?

**Opción 1**: Reduce scope y entrega MVP funcional
**Opción 2**: Pide extensión (máximo 1 semana)

**Importante**: Mejor MVP bien documentado que proyecto grande incompleto.

### ¿Puedo trabajar en equipo?

Depende de las reglas del master. Si es grupal, documenta contribuciones individuales.

### ¿Debo implementar OAuth social login?

No es obligatorio. Implementa JWT simple primero. Si tienes tiempo, añade OAuth.

**Opción fácil**: Usa Clerk o Auth0.

### ¿Cuántos agentes debo documentar?

- **Mínimo**: 3 agentes (aprobar)
- **Recomendado**: 6 agentes (nota alta)
- **Excelente**: 6+ con ejemplos detallados

### ¿Puedo usar el proyecto en mi portfolio real?

¡Absolutamente! Ese es el objetivo.

**Tips**:
- Pon tu nombre real
- Email profesional
- Personaliza el README
- Añade LinkedIn

---

## Conclusión

Este proyecto final es tu oportunidad de demostrar que:

1. ✅ Dominas el stack completo
2. ✅ Aplicas arquitectura limpia y SOLID
3. ✅ Orquestas agentes IA especializados
4. ✅ Documentas profesionalmente
5. ✅ Despliegas con confianza

**No es solo un ejercicio académico**. Es tu carta de presentación profesional.

**Invierte el tiempo necesario**. 80-100 horas en 3-4 semanas es realista.

**Pide feedback temprano**. Muestra tu progreso.

**Celebra tu logro**. Habrás construido algo real.

---

## Enlaces Importantes

- **Template**: [PORTFOLIO_TEMPLATE.md](PORTFOLIO_TEMPLATE.md)
- **Rúbrica**: [RUBRICA_EVALUACION.md](RUBRICA_EVALUACION.md)
- **Checklist**: [CHECKLIST.md](CHECKLIST.md)
- **Ideas**: [PROJECT_IDEAS.md](PROJECT_IDEAS.md)
- **Agentes**: [AGENT_WORKFLOW_GUIDE.md](AGENT_WORKFLOW_GUIDE.md)
- **Ejemplo**: [ejemplos/PORTFOLIO_EJEMPLO_1.md](ejemplos/PORTFOLIO_EJEMPLO_1.md)

---

**¡Éxito con tu proyecto final!** 🚀

*La perfección es enemiga de lo terminado. Entrega un MVP bien documentado y mejora iterativamente.*

---

**Última actualización**: Enero 2025  
**Versión**: 1.0  
**Autor**: Master en Desarrollo Asistido por IA
