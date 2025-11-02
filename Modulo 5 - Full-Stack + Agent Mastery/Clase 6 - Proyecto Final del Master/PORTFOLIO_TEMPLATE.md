# [Nombre de Tu Proyecto]

> Un [descripción breve en 1 línea] que [propuesta de valor única]

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript)](https://www.typescriptlang.org/)

[Agrega aquí un screenshot principal de tu aplicación]

![App Screenshot](docs/screenshots/main-dashboard.png)

---

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Problema y Solución](#problema-y-solución)
- [Tech Stack](#tech-stack)
- [Arquitectura](#arquitectura)
- [Features](#features)
- [Getting Started](#getting-started)
- [Testing](#testing)
- [Agentes IA Utilizados](#agentes-ia-utilizados)
- [Deployment](#deployment)
- [Roadmap](#roadmap)
- [Contribuir](#contribuir)
- [Licencia](#licencia)
- [Contacto](#contacto)

---

## Descripción

<!-- Instrucciones: Escribe 2-3 párrafos explicando tu proyecto -->

[Tu proyecto] es una aplicación [tipo: SaaS/Marketplace/Dashboard/etc.] construida con tecnologías modernas que permite a [usuarios objetivo] [acción principal].

El proyecto fue desarrollado como proyecto final del Master en Desarrollo Asistido por IA, demostrando:
- Arquitectura limpia y escalable
- Desarrollo full-stack con FastAPI y React
- Orquestación de agentes IA especializados
- Despliegue en producción con CI/CD

**Características destacadas**:
- 🚀 [Característica 1]
- 💎 [Característica 2]
- 🔒 [Característica 3]
- ⚡ [Característica 4]

---

## Problema y Solución

### El Problema 🚨

<!-- Instrucciones: Describe el problema real que resuelve tu app -->

[Descripción del problema en 2-3 frases. Sé específico.]

**Dolores actuales**:
- ❌ [Dolor 1 - ej: Los usuarios pierden X horas por semana en Y]
- ❌ [Dolor 2 - ej: Las soluciones actuales cuestan $X/mes]
- ❌ [Dolor 3 - ej: Falta de integración con herramientas populares]

**Impacto**:
- [Estadística o dato impactante si es posible]
- [Ejemplo: "El 73% de los freelancers no facturan el 20% de su tiempo por mala gestión"]

### La Solución ✨

<!-- Instrucciones: Explica cómo tu app resuelve el problema -->

[Nombre del proyecto] resuelve estos problemas mediante:

1. **[Solución 1]**: [Explicación breve]
2. **[Solución 2]**: [Explicación breve]
3. **[Solución 3]**: [Explicación breve]

**Diferenciadores clave**:
- ✅ [Diferenciador 1 vs competencia]
- ✅ [Diferenciador 2 vs competencia]
- ✅ [Diferenciador 3 vs competencia]

---

## Tech Stack

### Backend

![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red)
![Alembic](https://img.shields.io/badge/Alembic-1.13-lightgrey)

**¿Por qué FastAPI?**
- Performance comparable a NodeJS gracias a async/await
- Type safety nativo con Pydantic
- OpenAPI/Swagger automático
- Ecosistema Python maduro

**¿Por qué PostgreSQL?**
- [Tu justificación - ej: Relaciones complejas, ACID, JSON support]
- [Ver ADR-001](docs/architecture/adr/ADR-001-database-choice.md) para análisis completo

### Frontend

![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript)
![Vite](https://img.shields.io/badge/Vite-5-646CFF?logo=vite)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3-06B6D4?logo=tailwindcss)
![React Query](https://img.shields.io/badge/React_Query-5-FF4154)

**¿Por qué React + TypeScript?**
- Ecosistema maduro con componentes reutilizables
- Type safety end-to-end
- Tooling excelente para debugging
- Facilidad para testing

**State Management**: [Context API / Zustand / Redux - elige uno]

### DevOps & Infrastructure

![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)
![GitHub Actions](https://img.shields.io/badge/CI/CD-GitHub_Actions-2088FF?logo=githubactions)
![Render](https://img.shields.io/badge/Deploy-Render-46E3B7)
![Vercel](https://img.shields.io/badge/Frontend-Vercel-black?logo=vercel)

### Agentes IA

![Claude](https://img.shields.io/badge/Claude-Sonnet_3.5-orange)
![GitHub Copilot](https://img.shields.io/badge/Copilot-Enabled-black?logo=github)

---

## Arquitectura

### Diagrama de Alto Nivel

<!-- Instrucciones: Usa Mermaid o inserta imagen -->

```mermaid
graph TB
    Client[React Client<br/>TypeScript + Vite]
    API[FastAPI<br/>Python 3.12]
    Service[Service Layer<br/>Business Logic]
    Repo[Repository Layer<br/>Data Access]
    DB[(PostgreSQL<br/>Database)]
    Auth[JWT Auth<br/>Middleware]
    Cache[Redis<br/>Cache]

    Client -->|HTTP/REST| API
    API --> Auth
    Auth --> Service
    Service --> Repo
    Service --> Cache
    Repo --> DB

    style Client fill:#61DAFB
    style API fill:#009688
    style Service fill:#FFA500
    style Repo fill:#4169E1
    style DB fill:#336791
```

### Principios Arquitectónicos

✅ **Clean Architecture**: Separación clara de capas (API / Service / Repository)  
✅ **SOLID**: Dependency Inversion, Single Responsibility  
✅ **DRY**: Reutilización mediante abstracciones  
✅ **Security by Design**: JWT en middleware, validación en todos los inputs

### Capas de la Aplicación

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│  (FastAPI Endpoints + React Components) │
├─────────────────────────────────────────┤
│        Business Logic Layer             │
│          (Services + DTOs)              │
├─────────────────────────────────────────┤
│        Data Access Layer                │
│    (Repositories + SQLAlchemy Models)   │
├─────────────────────────────────────────┤
│         Infrastructure                  │
│  (Database, Cache, External APIs)       │
└─────────────────────────────────────────┘
```

Ver [docs/architecture/](docs/architecture/) para diagramas detallados y ADRs.

---

## Features

### 1. Autenticación Segura con JWT 🔐

- Registro de usuarios con validación de email
- Login con access y refresh tokens
- Roles y permisos granulares (Admin, Member, Viewer)
- Rate limiting para prevenir brute force
- Password policy: mínimo 8 caracteres, mayúsculas, números

![Login Screen](docs/screenshots/login.png)

**Tecnologías**: python-jose, bcrypt, Redis (refresh tokens)

---

### 2. [Feature 2 - Ej: Dashboard Interactivo] 📊

<!-- Instrucciones: Describe cada feature con screenshot -->

- [Sub-feature 1]
- [Sub-feature 2]
- [Sub-feature 3]

![Dashboard](docs/screenshots/dashboard.png)

**Tecnologías**: [Librerías usadas]

---

### 3. [Feature 3] 🎯

[Descripción]

![Feature 3](docs/screenshots/feature-3.png)

---

### 4. [Feature 4] ⚡

[Descripción]

![Feature 4](docs/screenshots/feature-4.png)

---

### 5. [Feature 5] 💎

[Descripción]

![Feature 5](docs/screenshots/feature-5.png)

---

## Getting Started

### Prerrequisitos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.12+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **Docker y Docker Compose** (opcional pero recomendado) ([Download](https://www.docker.com/))
- **PostgreSQL 15+** (si no usas Docker)
- **Git** ([Download](https://git-scm.com/))

### Instalación Rápida con Docker (Recomendado)

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/tu-proyecto.git
cd tu-proyecto

# 2. Configurar variables de entorno
cp .env.template .env
# Edita .env con tus valores (ver sección Configuration)

# 3. Levantar todos los servicios con Docker Compose
docker-compose up -d

# 4. Ejecutar migraciones de base de datos
docker-compose exec backend alembic upgrade head

# 5. (Opcional) Cargar datos de prueba
docker-compose exec backend python scripts/seed_data.py

# 6. Abrir en el navegador
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs (Swagger): http://localhost:8000/docs
```

### Instalación Manual (Desarrollo Local)

#### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.template .env
# Edita .env con tus valores

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor de desarrollo
uvicorn app.main:app --reload --port 8000

# El backend estará disponible en http://localhost:8000
# Docs en http://localhost:8000/docs
```

#### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.template .env.local
# Edita .env.local con la URL del backend

# Iniciar servidor de desarrollo
npm run dev

# El frontend estará disponible en http://localhost:3000
```

### Configuration

Variables de entorno requeridas:

#### Backend (`.env`)

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# JWT
JWT_SECRET=your-super-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
JWT_REFRESH_EXPIRATION_DAYS=7

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Redis (opcional, para refresh tokens y caché)
REDIS_URL=redis://localhost:6379/0

# External APIs (si aplica)
# OPENAI_API_KEY=sk-...
# SENDGRID_API_KEY=SG....

# Environment
ENV=development
DEBUG=True
```

#### Frontend (`.env.local`)

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=Tu Proyecto
```

Ver [`.env.template`](.env.template) para todas las opciones disponibles.

### Troubleshooting

**Error: "ModuleNotFoundError: No module named 'app'"**

**Solución**: Asegúrate de estar en el entorno virtual activado.

```bash
# Verificar que estás en el venv
which python  # Debe mostrar ruta del .venv
```

**Error: "Connection refused" al conectar a la base de datos**

**Solución**: Verifica que PostgreSQL está corriendo.

```bash
# Con Docker
docker-compose ps

# Sin Docker (Linux)
sudo systemctl status postgresql
```

**Frontend muestra "Network Error"**

**Solución**: Verifica que:
1. El backend está corriendo en el puerto 8000
2. `VITE_API_BASE_URL` en `.env.local` apunta a `http://localhost:8000`
3. CORS está configurado correctamente en el backend

Ver [docs/SETUP.md](docs/SETUP.md) para más detalles.

---

## Testing

### Ejecutar Tests

#### Backend Tests

```bash
cd backend

# Tests unitarios
pytest

# Tests con reporte de cobertura
pytest --cov=app --cov-report=html --cov-report=term

# Tests de un módulo específico
pytest tests/test_auth.py -v

# Tests con markers
pytest -m "not slow"  # Excluir tests lentos
```

#### Frontend Tests

```bash
cd frontend

# Tests unitarios
npm run test

# Tests en modo watch
npm run test:watch

# Tests con cobertura
npm run test:coverage
```

#### E2E Tests (opcional)

```bash
# Con Playwright
npm run test:e2e

# Con Cypress
npm run cypress:open
```

### Cobertura de Tests

**Backend Coverage**: 87%
- Models: 95%
- Services: 88%
- API Endpoints: 82%
- Repositories: 90%

**Frontend Coverage**: 76%
- Components: 80%
- Hooks: 75%
- Utils: 85%

![Coverage Report](docs/screenshots/coverage.png)

### CI/CD Pipeline

Cada push a `main` ejecuta automáticamente:

1. ✅ **Linting**: Ruff (backend) + ESLint (frontend)
2. ✅ **Type Checking**: mypy (backend) + tsc (frontend)
3. ✅ **Tests**: Pytest + Vitest con reportes de cobertura
4. ✅ **Security Scan**: Bandit (backend) + npm audit (frontend)
5. ✅ **Build**: Docker image build test
6. ✅ **Deploy**: Auto-deploy a staging (Render + Vercel)

Ver [.github/workflows/ci.yml](.github/workflows/ci.yml) para el pipeline completo.

---

## Agentes IA Utilizados

<!-- Instrucciones: Esta sección es CRÍTICA. Documenta cómo usaste agentes IA -->

Este proyecto fue desarrollado con asistencia de **agentes IA especializados**, documentando cada decisión para transparencia y reproducibilidad.

### Equipo de Agentes

| Agente | Rol | Contribución | Documentación |
|--------|-----|--------------|---------------|
| **Backend Architect** | Diseño de arquitectura | Definió estructura de capas, SOLID principles, ADRs | [Ver docs](docs/agents/agents/backend-architect.md) |
| **FastAPI Specialist** | Implementación API | Endpoints RESTful, validación Pydantic, async patterns | [Ver docs](docs/agents/agents/fastapi-specialist.md) |
| **Database Designer** | Modelado de datos | Esquema relacional, migraciones Alembic, índices | [Ver docs](docs/agents/agents/database-designer.md) |
| **Security Auditor** | Revisión de seguridad | JWT, rate limiting, validación, OWASP compliance | [Ver docs](docs/agents/agents/security-auditor.md) |
| **Test Strategist** | Estrategia de testing | Test pyramid, fixtures, mocks, cobertura 80%+ | [Ver docs](docs/agents/agents/test-strategist.md) |
| **Frontend Coach** | React + TypeScript | Componentes, hooks, state management, TypeScript | [Ver docs](docs/agents/agents/frontend-coach.md) |

### Workflow de Desarrollo

```mermaid
graph LR
    A[Diseño Feature] --> B[Backend Architect]
    B --> C[FastAPI Specialist]
    C --> D[Security Auditor]
    D --> E[Test Strategist]
    E --> F[Frontend Coach]
    F --> G[Code Review Manual]
    G --> H{¿Aprobado?}
    H -->|No| C
    H -->|Sí| I[Merge a main]
```

### Ejemplo de Documentación

Para cada feature importante, documenté:

1. **Prompt inicial**: Qué le pedí al agente
2. **Respuesta del agente**: Propuesta de implementación
3. **Iteraciones**: Ajustes y refinamientos
4. **Decisión final**: Qué se implementó y por qué
5. **Validación manual**: Qué revisé como humano

**Ejemplo completo**: [Feature de Autenticación JWT](docs/agents/examples/feature-authentication.md)

### Métricas de Productividad

Comparación de desarrollo con/sin agentes IA:

| Actividad | Sin IA (estimado) | Con IA (real) | Ahorro |
|-----------|-------------------|---------------|--------|
| Diseño de arquitectura | 1 semana | 2 días | 60% |
| Implementación backend | 3 semanas | 1 semana | 67% |
| Tests (80% cobertura) | 1 semana | 2 días | 71% |
| Frontend React + TS | 2 semanas | 5 días | 64% |
| Documentación | 1 semana | 2 días | 71% |
| **TOTAL** | **8 semanas** | **3 semanas** | **62.5%** |

**Nota importante**: El ahorro de tiempo NO significa menor calidad. Los agentes aceleraron la implementación, pero la validación, testing y decisiones arquitectónicas fueron realizadas por mí.

Ver [docs/agents/METRICS.md](docs/agents/METRICS.md) para métricas detalladas.

---

## Deployment

### Aplicación en Producción

- **Frontend**: [https://tu-proyecto.vercel.app](https://tu-proyecto.vercel.app)
- **Backend API**: [https://tu-proyecto-api.render.com](https://tu-proyecto-api.render.com)
- **API Docs**: [https://tu-proyecto-api.render.com/docs](https://tu-proyecto-api.render.com/docs)

### Credenciales de Demo

Para probar la aplicación sin registrarse:

```
Email: demo@tuproyecto.com
Password: Demo1234!
```

### Stack de Deployment

- **Frontend**: Vercel
  - CDN global con edge caching
  - Preview deploys automáticos en cada PR
  - Custom domain con SSL incluido

- **Backend**: Render
  - PostgreSQL incluido (managed database)
  - Health checks automáticos
  - Auto-scale basado en tráfico

- **Database**: Render PostgreSQL
  - Backups diarios automáticos
  - Point-in-time recovery
  - 90 días gratis, luego $7/mes

- **Monitoring**: Sentry + UptimeRobot
  - Error tracking en tiempo real
  - Uptime monitoring 24/7
  - Alertas vía email/Slack

### Estrategia de Deploy

```bash
# Deploy automático en cada push a main
git push origin main

# Preview deploy en cada PR (Vercel)
# Staging deploy antes de producción (Render)
```

### Variables de Entorno en Producción

Configuradas en:
- **Vercel Dashboard**: Settings → Environment Variables
- **Render Dashboard**: Environment → Environment Variables

**Importante**: NUNCA commitear secrets al repositorio.

Ver [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) para documentación completa de deployment.

---

## Roadmap

### Versión Actual: v1.0.0 (Enero 2025)

Features implementadas:
- ✅ Autenticación JWT completa con roles
- ✅ CRUD de [entidad principal]
- ✅ Dashboard con métricas en tiempo real
- ✅ API RESTful documentada (Swagger)
- ✅ Tests con 87% cobertura
- ✅ Despliegue en producción
- ✅ CI/CD con GitHub Actions

### Próximas Versiones

#### v1.1.0 (Q1 2025)
- [ ] Notificaciones en tiempo real (WebSockets)
- [ ] Exportación de reportes (PDF/Excel)
- [ ] Búsqueda avanzada con filtros
- [ ] Dark mode en frontend
- [ ] API rate limiting mejorado

#### v1.2.0 (Q2 2025)
- [ ] API GraphQL (además de REST)
- [ ] Mobile app (React Native)
- [ ] Integración con Slack/Discord
- [ ] AI-powered recommendations

#### v2.0.0 (Q3 2025)
- [ ] Multi-tenancy (modo SaaS)
- [ ] Billing & subscriptions (Stripe)
- [ ] Advanced analytics dashboard
- [ ] Marketplace de plugins/extensions

---

## Contribuir

<!-- Instrucciones: Si quieres que sea open source y aceptar contribuciones -->

Este proyecto actualmente es un portfolio individual, pero acepto:

- 🐛 **Bug reports**: Abre un issue con reproducción detallada
- 💡 **Feature suggestions**: Discusión antes de implementar
- 📖 **Documentación**: Mejoras siempre bienvenidas
- 🌐 **Traducciones**: Ayuda a traducir la app

### Cómo Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'feat: Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para guidelines detallados.

---

## Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2025 [Tu Nombre]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

Puedes usar este código para:
- ✅ Aprendizaje personal
- ✅ Proyectos comerciales
- ✅ Modificar y distribuir
- ⚠️ Sin garantía de ningún tipo

---

## Contacto

**[Tu Nombre]**

- 🌐 Website: [tu-portfolio.com](https://tu-portfolio.com)
- 💼 LinkedIn: [linkedin.com/in/tu-perfil](https://linkedin.com/in/tu-perfil)
- 🐙 GitHub: [@tu-usuario](https://github.com/tu-usuario)
- ✉️ Email: tu.email@example.com
- 🐦 Twitter: [@tu-usuario](https://twitter.com/tu-usuario)

---

## Agradecimientos

- **Master en Desarrollo Asistido por IA** - Por la formación completa
- **FastAPI** - Por el framework increíble
- **React Team** - Por React 18 y las mejoras de performance
- **Anthropic Claude** - Por asistencia en arquitectura y código
- **GitHub Copilot** - Por acelerar el desarrollo

---

**Hecho con** ❤️ **y ayuda de agentes IA especializados**

*Este proyecto es el resultado del Master en Desarrollo Asistido por IA (2024-2025)*

---

## Stats del Proyecto

![GitHub repo size](https://img.shields.io/github/repo-size/tu-usuario/tu-proyecto)
![GitHub stars](https://img.shields.io/github/stars/tu-usuario/tu-proyecto?style=social)
![GitHub forks](https://img.shields.io/github/forks/tu-usuario/tu-proyecto?style=social)
![GitHub issues](https://img.shields.io/github/issues/tu-usuario/tu-proyecto)
![GitHub pull requests](https://img.shields.io/github/issues-pr/tu-usuario/tu-proyecto)

---

**Última actualización**: Enero 2025  
**Versión**: 1.0.0  
**Estado**: ✅ En producción
