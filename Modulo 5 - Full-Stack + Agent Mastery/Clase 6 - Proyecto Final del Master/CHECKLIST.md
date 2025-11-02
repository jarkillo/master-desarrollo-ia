# Checklist Completo - Proyecto Final

## Cómo Usar Este Checklist

- [ ] Imprime este documento o tenlo abierto durante todo el proyecto
- [ ] Marca cada item cuando lo completes
- [ ] Revisa el checklist al final de cada semana
- [ ] Ejecuta el "Checklist Pre-Entrega" 24 horas antes de entregar

---

## Fase 1: Planificación (Semana 1, Días 1-2)

### Selección de Proyecto

- [ ] He listado 5 ideas de proyectos que me interesan
- [ ] He calificado cada idea según el framework (Pasión/Complejidad/Portfolio/Viabilidad)
- [ ] He elegido el proyecto con mayor puntaje
- [ ] He validado la idea con un mentor o peer
- [ ] He definido el MVP (features core vs nice-to-have)

### Setup Inicial de Repositorio

- [ ] Repositorio Git creado (público en GitHub)
- [ ] .gitignore configurado (Python, Node, .env, etc.)
- [ ] README inicial creado con descripción básica
- [ ] Licencia MIT añadida
- [ ] Estructura de carpetas creada:
  - [ ] `/backend`
  - [ ] `/frontend`
  - [ ] `/docs`
  - [ ] `/docs/architecture/adr`
  - [ ] `/docs/architecture/diagrams`
  - [ ] `/docs/agents`

### Tablero de Tareas

- [ ] Tablero creado (Trello/Linear/GitHub Projects)
- [ ] Columnas creadas: To Do / In Progress / Done
- [ ] Features del MVP añadidas como tareas
- [ ] Tareas priorizadas por importancia

---

## Fase 2: Arquitectura (Semana 1, Días 3-4)

### Diseño con Backend Architect

- [ ] He usado un agente "Backend Architect" para diseñar la arquitectura
- [ ] Arquitectura en capas definida (API / Service / Repository)
- [ ] Diagrama de arquitectura de alto nivel creado
- [ ] Diagrama de capas creado

### Modelado de Datos

- [ ] He usado un agente "Database Designer"
- [ ] Entidades principales identificadas (≥ 4 tablas)
- [ ] Relaciones entre entidades definidas
- [ ] Diagrama ER creado
- [ ] Índices necesarios identificados

### ADRs Iniciales

- [ ] ADR-001: Elección de base de datos (PostgreSQL vs otros) escrito
- [ ] ADR-002: Arquitectura en capas justificada
- [ ] ADR-003: Estrategia de autenticación (JWT) documentada
- [ ] Todos los ADRs siguen el formato estándar
- [ ] ADRs en `docs/architecture/adr/`

---

## Fase 3: Setup Técnico (Semana 1, Día 5)

### Backend Setup

- [ ] Carpeta `/backend` creada
- [ ] Virtual environment creado (`.venv`)
- [ ] `requirements.txt` creado con dependencias:
  - [ ] FastAPI
  - [ ] Uvicorn
  - [ ] SQLAlchemy
  - [ ] Alembic
  - [ ] Pydantic
  - [ ] python-jose (JWT)
  - [ ] bcrypt
  - [ ] pytest + pytest-cov
  - [ ] httpx (para tests)
- [ ] Estructura de carpetas backend:
  - [ ] `/app/api/routes`
  - [ ] `/app/services`
  - [ ] `/app/repositories`
  - [ ] `/app/models`
  - [ ] `/app/schemas`
  - [ ] `/app/core` (config, security)
  - [ ] `/tests`
- [ ] `app/main.py` creado con app básica de FastAPI
- [ ] Servidor corre exitosamente (`uvicorn app.main:app --reload`)

### Frontend Setup

- [ ] Carpeta `/frontend` creada
- [ ] Proyecto Vite + React + TypeScript creado
- [ ] Dependencias instaladas:
  - [ ] React 18
  - [ ] React Router
  - [ ] TailwindCSS (o librería de UI elegida)
  - [ ] React Query (opcional)
  - [ ] Axios o similar para HTTP
- [ ] Estructura de carpetas frontend:
  - [ ] `/src/components`
  - [ ] `/src/pages`
  - [ ] `/src/services` (API client)
  - [ ] `/src/hooks`
  - [ ] `/src/types`
  - [ ] `/src/utils`
- [ ] TypeScript configurado correctamente (`tsconfig.json`)
- [ ] Servidor dev corre exitosamente (`npm run dev`)

### Docker y CI/CD

- [ ] `Dockerfile` para backend creado
- [ ] `Dockerfile` para frontend creado
- [ ] `docker-compose.yml` creado con:
  - [ ] Servicio backend
  - [ ] Servicio frontend
  - [ ] Servicio postgres
  - [ ] Volúmenes para persistencia de datos
- [ ] `docker-compose up` funciona correctamente
- [ ] `.github/workflows/ci.yml` creado con workflow básico:
  - [ ] Checkout código
  - [ ] Setup Python y Node
  - [ ] Instalar dependencias
  - [ ] Ejecutar linting (ruff, eslint)
  - [ ] Ejecutar tests

### Deployment Accounts

- [ ] Cuenta de Render creada (para backend)
- [ ] Cuenta de Vercel creada (para frontend)
- [ ] PostgreSQL en Render provisionado (o alternativa elegida)

---

## Fase 4: Autenticación (Semana 2, Días 1-2)

### Backend: Modelos y Lógica

- [ ] Modelo `User` creado en SQLAlchemy:
  - [ ] id (UUID)
  - [ ] email (unique)
  - [ ] hashed_password
  - [ ] full_name
  - [ ] is_active
  - [ ] role (Enum: admin, member, viewer)
  - [ ] created_at
- [ ] Modelo `RefreshToken` creado (opcional pero recomendado)
- [ ] Migración de Alembic generada y aplicada
- [ ] `AuthService` creado con métodos:
  - [ ] `register_user()`
  - [ ] `authenticate_user()`
  - [ ] `create_access_token()`
  - [ ] `create_refresh_token()`
  - [ ] `verify_token()`
- [ ] Password hashing con bcrypt (≥ 12 rounds)
- [ ] Password validation implementada (min 8 chars, mayúsculas, números)

### Backend: Endpoints de Auth

- [ ] `POST /auth/register` creado
- [ ] `POST /auth/login` creado
- [ ] `POST /auth/refresh` creado (refresh token)
- [ ] `POST /auth/logout` creado (invalidar tokens)
- [ ] Schemas Pydantic creados:
  - [ ] `UserRegister`
  - [ ] `UserLogin`
  - [ ] `TokenResponse`
  - [ ] `UserResponse`
- [ ] Validación completa en todos los schemas
- [ ] Middleware `get_current_user` creado para proteger rutas
- [ ] Rate limiting implementado en `/auth/login`

### Tests de Autenticación

- [ ] Test: Registro de usuario válido
- [ ] Test: Registro con email duplicado (debe fallar)
- [ ] Test: Login con credenciales correctas
- [ ] Test: Login con credenciales incorrectas
- [ ] Test: Acceso a ruta protegida con token válido
- [ ] Test: Acceso a ruta protegida sin token (debe fallar)
- [ ] Test: Refresh token válido
- [ ] Test: Refresh token expirado (debe fallar)
- [ ] Test: Logout (invalidar tokens)
- [ ] Test: Password policy validación
- [ ] Cobertura de tests de auth ≥ 85%

### Documentación de Agentes

- [ ] Agente "Backend Architect" usado para diseño documentado
- [ ] Agente "FastAPI Specialist" usado para implementación documentado
- [ ] Agente "Security Auditor" usado para revisión documentado
- [ ] Ejemplo completo en `docs/agents/examples/feature-authentication.md`

---

## Fase 5: Funcionalidad Core (Semana 2, Días 3-4)

### Modelos de Datos

- [ ] Todas las entidades principales creadas (≥ 4 tablas)
- [ ] Relaciones entre modelos definidas (ForeignKey, relationships)
- [ ] Índices añadidos donde necesario
- [ ] Migraciones generadas y aplicadas
- [ ] Datos de seed creados (`scripts/seed_data.py`)

### Servicios y Repositorios

- [ ] `RepositoryBase` creado con métodos genéricos
- [ ] Repositorios concretos para cada entidad:
  - [ ] `get_by_id()`
  - [ ] `get_all()`
  - [ ] `create()`
  - [ ] `update()`
  - [ ] `delete()`
  - [ ] Métodos de búsqueda personalizados
- [ ] Servicios para cada entidad con lógica de negocio
- [ ] Validaciones de negocio implementadas

### Endpoints CRUD

- [ ] Endpoints creados para entidad principal 1:
  - [ ] `GET /entity` (listar con paginación)
  - [ ] `GET /entity/{id}` (obtener por ID)
  - [ ] `POST /entity` (crear)
  - [ ] `PUT /entity/{id}` (actualizar)
  - [ ] `DELETE /entity/{id}` (eliminar)
- [ ] Endpoints creados para entidad principal 2 (similar)
- [ ] Endpoints creados para entidad principal 3 (similar)
- [ ] Total de endpoints ≥ 8 (sin contar auth)
- [ ] Todos los endpoints protegidos con JWT
- [ ] Validación con Pydantic en todos los inputs
- [ ] Status codes HTTP correctos en todas las respuestas
- [ ] Manejo de errores consistente

### Tests Backend

- [ ] Tests unitarios para servicios
- [ ] Tests de integración para repositorios
- [ ] Tests de endpoints (happy path)
- [ ] Tests de endpoints (casos de error)
- [ ] Tests de validación Pydantic
- [ ] Tests de casos edge
- [ ] Cobertura total backend ≥ 80%

---

## Fase 6: Deployment Básico (Semana 2, Día 5)

### Backend Deployment

- [ ] Proyecto backend desplegado en Render
- [ ] Base de datos PostgreSQL conectada
- [ ] Variables de entorno configuradas en Render
- [ ] Migraciones ejecutadas en producción
- [ ] Health check endpoint creado (`GET /health`)
- [ ] URL de backend funciona: `https://tu-proyecto-api.render.com`
- [ ] Swagger funciona: `https://tu-proyecto-api.render.com/docs`

### Frontend Deployment (básico)

- [ ] Proyecto frontend desplegado en Vercel
- [ ] Variable `VITE_API_BASE_URL` apunta al backend en Render
- [ ] CORS configurado en backend para permitir frontend
- [ ] URL de frontend funciona: `https://tu-proyecto.vercel.app`

### Smoke Tests

- [ ] Backend responde en producción
- [ ] Frontend carga en producción
- [ ] Frontend puede llamar al backend (sin CORS errors)
- [ ] Registro de usuario funciona end-to-end

---

## Fase 7: Features Secundarias (Semana 3, Días 1-2)

### Features Adicionales Backend

- [ ] Feature secundaria 1 implementada
- [ ] Feature secundaria 2 implementada
- [ ] Integración con API externa (si aplica)
- [ ] File uploads implementados (si aplica)
- [ ] Notificaciones por email (si aplica)
- [ ] Tests para features secundarias

### Documentación de Agentes

- [ ] Agentes utilizados documentados para cada feature
- [ ] Prompts documentados
- [ ] Decisiones y modificaciones registradas

---

## Fase 8: Frontend Completo (Semana 3, Día 3)

### Componentes y Páginas

- [ ] Layout principal creado (Header, Footer, Sidebar)
- [ ] Componentes reutilizables creados (≥ 10):
  - [ ] Button
  - [ ] Input/Form components
  - [ ] Card
  - [ ] Modal
  - [ ] Loading spinner
  - [ ] Error message
  - [ ] (otros según tu proyecto)
- [ ] Páginas principales creadas (≥ 5):
  - [ ] Landing/Home
  - [ ] Login
  - [ ] Register
  - [ ] Dashboard
  - [ ] [Página específica 1]
  - [ ] [Página específica 2]
  - [ ] (otras según tu proyecto)
- [ ] Navegación con React Router configurada
- [ ] Rutas protegidas implementadas (requieren auth)

### Integración con Backend

- [ ] API client creado (`/src/services/api.ts`)
- [ ] Interceptor para añadir JWT a requests
- [ ] Manejo de errores 401 (redirect a login)
- [ ] Todas las páginas integradas con backend
- [ ] Estado de auth sincronizado (Context o Zustand)

### Formularios y Validación

- [ ] Formularios con validación en cliente
- [ ] Feedback visual en inputs (error states)
- [ ] Loading states durante submit
- [ ] Mensajes de éxito después de acciones
- [ ] Manejo de errores del servidor mostrados al usuario

### UX y Diseño

- [ ] Diseño responsive (mobile, tablet, desktop)
- [ ] Loading skeletons o spinners en carga de datos
- [ ] Estados vacíos manejados (empty states)
- [ ] Confirmaciones para acciones destructivas (delete)
- [ ] Animaciones sutiles (transiciones)
- [ ] Paleta de colores consistente
- [ ] Tipografía legible

### Documentación de Agentes

- [ ] Agente "Frontend Coach" usado y documentado
- [ ] Decisiones de state management documentadas
- [ ] Componentes complejos documentados

---

## Fase 9: Testing Exhaustivo (Semana 3, Día 4)

### Tests Backend

- [ ] Todos los endpoints tienen tests
- [ ] Casos edge testeados
- [ ] Tests de seguridad (inyección SQL, XSS simulado)
- [ ] Tests de performance básicos
- [ ] Cobertura backend ≥ 85%

### Tests Frontend

- [ ] Tests unitarios de componentes
- [ ] Tests de integración de páginas
- [ ] Tests de hooks personalizados
- [ ] Tests de utils
- [ ] Cobertura frontend ≥ 75%

### Tests E2E (opcional pero suma puntos)

- [ ] Playwright o Cypress configurado
- [ ] Test: Registro + Login + Acción principal
- [ ] Test: CRUD completo de entidad principal
- [ ] Test: Logout
- [ ] Tests E2E pasan en CI/CD

### Security Audit

- [ ] Bandit ejecutado en backend (sin issues críticos)
- [ ] npm audit ejecutado en frontend (vulnerabilidades resueltas)
- [ ] Secrets no hardcodeados (verificado con grep)
- [ ] OWASP Top 10 considerado:
  - [ ] Inyección SQL prevenida (ORM)
  - [ ] XSS prevenido (React escapa por defecto)
  - [ ] CSRF no aplica (API stateless)
  - [ ] Autenticación robusta (JWT)
  - [ ] Rate limiting en endpoints críticos

### Performance Testing

- [ ] Endpoints principales responden en < 500ms
- [ ] Frontend carga en < 3 segundos
- [ ] Lighthouse score ≥ 80 (Performance)
- [ ] Consultas N+1 identificadas y resueltas

---

## Fase 10: CI/CD Completo (Semana 3, Día 5)

### GitHub Actions

- [ ] Workflow completo en `.github/workflows/ci.yml`:
  - [ ] Checkout código
  - [ ] Setup Python 3.12
  - [ ] Setup Node 18
  - [ ] Install dependencies (backend + frontend)
  - [ ] Lint backend (ruff)
  - [ ] Lint frontend (eslint)
  - [ ] Type check backend (mypy)
  - [ ] Type check frontend (tsc --noEmit)
  - [ ] Run tests backend (pytest con cobertura)
  - [ ] Run tests frontend (vitest con cobertura)
  - [ ] Security scan (bandit)
  - [ ] Build Docker image (test)
  - [ ] Deploy a staging (opcional)
- [ ] Workflow ejecuta en cada push a main
- [ ] Workflow ejecuta en cada PR
- [ ] Badge de CI/CD en README

### Pre-commit Hooks

- [ ] Pre-commit hooks configurados (opcional pero recomendado):
  - [ ] Black o Ruff format
  - [ ] ESLint
  - [ ] Tests rápidos
- [ ] `.pre-commit-config.yaml` creado

### Monitoring

- [ ] Sentry configurado (o alternativa)
- [ ] Error tracking funcionando
- [ ] Alertas configuradas
- [ ] Uptime Robot monitoreando (https://uptimerobot.com/)

---

## Fase 11: Polish de la Aplicación (Semana 4, Día 1)

### UX Refinements

- [ ] Todos los botones tienen estados (hover, active, disabled)
- [ ] Loading states consistentes
- [ ] Error messages user-friendly (no stack traces)
- [ ] Success feedback después de acciones
- [ ] Tooltips en iconos (si aplica)
- [ ] Placeholders en inputs
- [ ] Confirmaciones para acciones destructivas

### Responsive Design

- [ ] Probado en Chrome DevTools (mobile, tablet, desktop)
- [ ] Probado en dispositivo móvil real
- [ ] Menú colapsable en mobile
- [ ] Tablas con scroll horizontal en mobile (si aplica)
- [ ] Modals adaptados a pantalla pequeña

### Accesibilidad (a11y)

- [ ] Alt text en imágenes
- [ ] Labels en inputs (no solo placeholders)
- [ ] Navegación con teclado funciona
- [ ] Contraste de colores adecuado
- [ ] ARIA labels donde necesario

### Dark Mode (opcional pero suma)

- [ ] Dark mode implementado
- [ ] Toggle funcional
- [ ] Colores adaptados
- [ ] Preferencia guardada en localStorage

### Performance

- [ ] Imágenes optimizadas (formato WebP, comprimidas)
- [ ] Lazy loading de imágenes
- [ ] Code splitting implementado (React.lazy)
- [ ] Bundle size optimizado
- [ ] Lighthouse score ≥ 85

---

## Fase 12: Documentación Exhaustiva (Semana 4, Días 2-3)

### README Principal

- [ ] README completo con todas las secciones (usar PORTFOLIO_TEMPLATE.md)
- [ ] Screenshots de alta calidad de todas las features principales
- [ ] Badges profesionales (Python, FastAPI, React, TypeScript, etc.)
- [ ] Propuesta de valor clara en introducción
- [ ] Tech stack con justificación (por qué cada tecnología)
- [ ] Diagrama de arquitectura insertado
- [ ] Features listadas con screenshots
- [ ] Getting Started detallado y probado
- [ ] Sección de Testing completa
- [ ] Sección de Agentes IA con tabla y workflow
- [ ] Links de deployment funcionando
- [ ] Roadmap con próximas versiones
- [ ] Información de contacto
- [ ] README ≥ 800 líneas

### ADRs Completos

- [ ] Mínimo 3 ADRs (obligatorio)
- [ ] Recomendado 5 ADRs:
  - [ ] ADR-001: Elección de base de datos
  - [ ] ADR-002: Arquitectura en capas
  - [ ] ADR-003: Estrategia de autenticación
  - [ ] ADR-004: Frontend framework
  - [ ] ADR-005: State management
  - [ ] (otros según tu proyecto)
- [ ] Todos los ADRs en `docs/architecture/adr/`
- [ ] Formato estándar usado en todos

### Diagramas

- [ ] Diagrama de arquitectura de alto nivel
- [ ] Diagrama de capas (Clean Architecture)
- [ ] Diagrama de flujo de autenticación (sequence diagram)
- [ ] Diagrama ER de base de datos (opcional)
- [ ] Todos en `docs/architecture/diagrams/`

### API Documentation

- [ ] Swagger/OpenAPI funciona en `/docs`
- [ ] Todos los endpoints documentados con docstrings
- [ ] Modelos Pydantic con `Field(..., description="")`
- [ ] Ejemplos en `Config.schema_extra`
- [ ] Tags agrupan endpoints lógicamente
- [ ] Todos los status codes documentados
- [ ] README tiene link a Swagger en producción

### Documentación de Agentes IA

- [ ] `docs/agents/README.md` creado (índice de agentes)
- [ ] Mínimo 3 agentes documentados (obligatorio):
  - [ ] Backend Architect
  - [ ] FastAPI Specialist
  - [ ] Security Auditor
- [ ] Recomendado 6 agentes:
  - [ ] Backend Architect
  - [ ] FastAPI Specialist
  - [ ] Database Designer
  - [ ] Security Auditor
  - [ ] Test Strategist
  - [ ] Frontend Coach
- [ ] Cada agente en `docs/agents/agents/[nombre].md`
- [ ] Template seguido para cada agente (rol, prompts, métricas)
- [ ] Mínimo 2 ejemplos completos en `docs/agents/examples/`:
  - [ ] Ejemplo 1: Feature importante (ej: autenticación)
  - [ ] Ejemplo 2: Otra feature o bugfix
- [ ] `docs/agents/METRICS.md` creado con:
  - [ ] Resumen ejecutivo
  - [ ] Estadísticas globales
  - [ ] Desglose por agente
  - [ ] ROI calculado
  - [ ] Comparación con/sin IA

### SETUP.md

- [ ] `docs/SETUP.md` creado
- [ ] Prerrequisitos listados con versiones
- [ ] Instrucciones paso a paso para Windows/Mac/Linux
- [ ] Variables de entorno explicadas
- [ ] Sección de Troubleshooting con problemas comunes

### DEPLOYMENT.md

- [ ] `docs/DEPLOYMENT.md` creado
- [ ] Stack de deployment explicado
- [ ] Pasos para desplegar backend en Render
- [ ] Pasos para desplegar frontend en Vercel
- [ ] Configuración de variables de entorno
- [ ] Configuración de PostgreSQL
- [ ] Configuración de CI/CD auto-deploy

---

## Fase 13: Video Demo (Semana 4, Día 4)

### Preparación

- [ ] Script del video escrito con estructura:
  - Minuto 0-1: Hook y contexto
  - Minuto 1-3: Demo visual
  - Minuto 3-5: Arquitectura técnica
  - Minuto 5-7: Código destacado
  - Minuto 7-9: Deployment y CI/CD
  - Minuto 9-10: Conclusiones
- [ ] Script practicado 3 veces en voz alta
- [ ] Setup de grabación preparado:
  - [ ] Micrófono funcionando
  - [ ] OBS/Loom/Zoom configurado
  - [ ] Tabs cerrados (solo los necesarios)
  - [ ] Notificaciones desactivadas
  - [ ] Browser limpio (sin extensiones visibles)

### Grabación

- [ ] Video grabado en una sola toma (o editado profesionalmente)
- [ ] Audio claro y sin ruido de fondo
- [ ] Duración 5-10 minutos
- [ ] Aplicación funcionando demostrada
- [ ] Arquitectura explicada con diagrama
- [ ] Snippet de código mostrado
- [ ] Deployment mostrado (URL real)
- [ ] Cara visible (opcional pero suma)

### Post-Producción

- [ ] Video editado (quitar pausas largas, silencios)
- [ ] Música de fondo añadida (opcional, muy sutil)
- [ ] Transiciones suaves entre secciones
- [ ] Video exportado en 1080p
- [ ] Video subido a YouTube (unlisted o public)
- [ ] Link del video añadido al README

---

## Fase 14: Slides (Semana 4, Día 4-5)

### Creación de Slides

- [ ] 15-20 slides creados
- [ ] Plantilla consistente usada
- [ ] Contenido:
  - [ ] Slide 1: Portada con nombre del proyecto
  - [ ] Slide 2: Problema que resuelve
  - [ ] Slide 3: Solución propuesta
  - [ ] Slides 4-7: Screenshots de features
  - [ ] Slide 8: Tech stack con logos
  - [ ] Slide 9: Diagrama de arquitectura
  - [ ] Slide 10: ADR destacado
  - [ ] Slide 11: Código interesante
  - [ ] Slides 12-13: Agentes IA y workflow
  - [ ] Slide 14: Métricas de IA
  - [ ] Slide 15: Testing y calidad
  - [ ] Slide 16: Deployment
  - [ ] Slide 17: Desafíos superados
  - [ ] Slide 18: Aprendizajes
  - [ ] Slide 19: Roadmap
  - [ ] Slide 20: Contacto y agradecimientos
- [ ] Diseño limpio (no sobrecargado)
- [ ] Imágenes de alta calidad
- [ ] Texto mínimo (bullets, no párrafos)
- [ ] Contraste alto (legible)

### Export

- [ ] Slides exportadas a PDF
- [ ] Slides subidas al repositorio (`docs/slides.pdf`)
- [ ] Fuente editable también subida (`.pptx` o link a Google Slides)

---

## Fase 15: Entrega Final (Semana 4, Día 5)

### Checklist Pre-Entrega (24 horas antes)

#### Código

- [ ] Todo el código commiteado y pusheado
- [ ] No hay código comentado innecesariamente
- [ ] No hay TODOs en el código
- [ ] No hay prints de debugging
- [ ] `.gitignore` está completo
- [ ] `.env` NO está en Git (solo `.env.template`)
- [ ] Secrets NO están hardcodeados

#### Tests

- [ ] Todos los tests pasan localmente
- [ ] Cobertura backend ≥ 80%
- [ ] Cobertura frontend ≥ 70% (recomendado 75%)
- [ ] CI/CD en GitHub Actions está verde
- [ ] No hay warnings críticos en tests

#### Deployment

- [ ] Backend desplegado y funciona:
  - [ ] URL accesible: _______________
  - [ ] `/docs` funciona
  - [ ] `/health` responde 200 OK
  - [ ] Endpoints principales probados
- [ ] Frontend desplegado y funciona:
  - [ ] URL accesible: _______________
  - [ ] Todas las páginas cargan
  - [ ] Puede comunicarse con backend
  - [ ] Login y registro funcionan
- [ ] Base de datos en producción con datos de demo
- [ ] Credenciales de demo creadas y funcionan

#### Documentación

- [ ] README completo y verificado:
  - [ ] Todos los screenshots presentes
  - [ ] Todos los links funcionan
  - [ ] Getting Started probado por otra persona
  - [ ] ≥ 800 líneas
- [ ] ADRs completos (≥ 3)
- [ ] Diagramas presentes (≥ 3)
- [ ] API docs verificadas (Swagger funciona)
- [ ] Documentación de agentes completa:
  - [ ] ≥ 3 agentes documentados
  - [ ] ≥ 2 ejemplos completos
  - [ ] METRICS.md con datos reales

#### Presentación

- [ ] Video demo:
  - [ ] Subido a YouTube
  - [ ] Link en README funciona
  - [ ] 5-10 minutos de duración
  - [ ] Audio claro
- [ ] Slides:
  - [ ] PDF en repo (`docs/slides.pdf`)
  - [ ] 15-20 slides
  - [ ] Contenido completo

#### Calidad

- [ ] Linter pasado (Ruff, ESLint)
- [ ] Type checker pasado (mypy, tsc)
- [ ] Security scan pasado (Bandit, npm audit)
- [ ] No hay errores en consola del browser
- [ ] Performance aceptable (Lighthouse ≥ 80)

### Auto-Evaluación con Rúbrica

- [ ] He revisado RUBRICA_EVALUACION.md
- [ ] Estimo mi puntuación: _____ / 100
- [ ] Identifico áreas débiles y las he mejorado
- [ ] Estimo que aprobaré (≥ 60 puntos)

### Entrega

- [ ] Link del repositorio GitHub copiado
- [ ] Link del video demo copiado
- [ ] Link de deployment (frontend) copiado
- [ ] Link de deployment (backend) copiado
- [ ] Credenciales de demo anotadas
- [ ] Formulario de entrega completado (si aplica)
- [ ] **ENTREGADO**

---

## Post-Entrega

### Celebración

- [ ] ¡He completado el proyecto final!
- [ ] He compartido mi proyecto en LinkedIn
- [ ] He pedido feedback a peers
- [ ] He actualizado mi CV con este proyecto
- [ ] He guardado este proyecto en mi portfolio

### Mejoras Continuas

- [ ] He anotado ideas para v1.1
- [ ] He respondido a issues de GitHub (si hay)
- [ ] He considerado hacer el proyecto open source
- [ ] He aplicado los learnings a futuros proyectos

---

## Resumen de Requisitos Mínimos

Para asegurarte de que apruebas, verifica que cumples **TODOS** estos mínimos:

### Técnico ✅
- [ ] Backend con ≥ 8 endpoints funcionando
- [ ] Frontend con ≥ 5 pantallas
- [ ] Autenticación JWT funcional
- [ ] Base de datos con ≥ 4 tablas relacionadas
- [ ] Tests con cobertura backend ≥ 70%, frontend ≥ 50%
- [ ] Arquitectura en capas identificable

### Deployment ✅
- [ ] Backend desplegado y accesible públicamente
- [ ] Frontend desplegado y accesible públicamente
- [ ] Links funcionando en README
- [ ] Credenciales de demo provistas

### Documentación ✅
- [ ] README ≥ 500 líneas con screenshots
- [ ] ≥ 2 ADRs con formato correcto
- [ ] ≥ 1 diagrama de arquitectura
- [ ] Getting Started que funciona (probado)

### Agentes IA ✅
- [ ] Documentación de ≥ 3 agentes
- [ ] ≥ 1 ejemplo completo de feature con agente
- [ ] Métricas básicas de uso de IA

### Presentación ✅
- [ ] Video demo de 5-10 minutos funcionando
- [ ] Slides con ≥ 10 slides
- [ ] Demo funcional mostrada

---

## Notas Finales

**Frecuencia de revisión**:
- [ ] Revisa este checklist diariamente
- [ ] Al final de cada semana, verifica que completaste la fase correspondiente
- [ ] 48 horas antes de entregar, ejecuta el "Checklist Pre-Entrega"

**Gestión de tiempo**:
- Si vas atrasado, prioriza features core sobre nice-to-have
- La documentación es tan importante como el código
- Deja al menos 3 días para documentación y presentación

**Pide ayuda si**:
- Estás bloqueado más de 4 horas en un problema
- No entiendes un requisito
- Dudes de tu arquitectura

---

**¡Éxito con tu proyecto final!** 🚀

*Este checklist es tu guía paso a paso. Síguelo y aprobarás con nota alta.*

---

**Última actualización**: Enero 2025  
**Versión**: 1.0
