# Módulo 5 - Clase 5: Agent Orchestration Mastery

**La culminación del master** - Aprende a orquestar un equipo completo de agentes especializados para construir proyectos grandes usando Claude Code best practices.

## 📋 Tabla de Contenidos

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [¿Qué es la Orquestación de Agentes?](#qué-es-la-orquestación-de-agentes)
3. [Agent Team Canvas Framework](#agent-team-canvas-framework)
4. [Claude Code Best Practices](#claude-code-best-practices)
5. [🤖 Construyendo con "Ejército de Agentes" (60% del contenido)](#-construyendo-con-ejército-de-agentes-60-del-contenido)
6. [Proyecto Final: E-commerce Platform](#proyecto-final-e-commerce-platform)
7. [Testing de Sistemas Multi-Agente](#testing-de-sistemas-multi-agente)
8. [Monitoring y Debugging Avanzado](#monitoring-y-debugging-avanzado)
9. [Ejercicios Prácticos](#ejercicios-prácticos)
10. [Recursos Adicionales](#recursos-adicionales)

---

## Descripción del Proyecto

Esta clase final integra **TODO lo aprendido en el master** para construir un proyecto completo usando un equipo orquestado de agentes especializados.

### El Concepto: "Un Desarrollador con un Ejército de Agentes"

Imagina poder construir una aplicación enterprise-grade **tú solo**, coordinando un equipo de 5-10 agentes especializados:

- 🏗️ **Architecture Agent**: Diseña la estructura del proyecto
- 🐍 **Python Best Practices Agent**: Revisa código backend
- ⚡ **FastAPI Design Agent**: Optimiza endpoints y APIs
- ⚛️ **React Integration Agent**: Construye frontend
- 🗄️ **Database ORM Agent**: Optimiza queries y migraciones
- 🚀 **Performance Agent**: Detecta bottlenecks
- 🐳 **Docker Agent**: Configura infraestructura
- 🔒 **Security Agent**: Audita vulnerabilidades

**Resultado**: Aplicación de calidad profesional en **fracción del tiempo** que tomaría solo.

---

## ¿Qué es la Orquestación de Agentes?

### Definición

**Orquestación de agentes** es el arte de coordinar múltiples agentes especializados para trabajar juntos en un proyecto complejo, dividiendo el trabajo en tareas específicas y asignando cada tarea al agente más adecuado.

### Analogía: Orquesta Sinfónica

| Elemento | En Orquesta | En Desarrollo con IA |
|----------|-------------|----------------------|
| **Director** | Coordina músicos | Tú (el desarrollador) |
| **Secciones** | Cuerdas, vientos, percusión | Backend, Frontend, DevOps |
| **Músicos** | Violinistas, trompetistas | Python Agent, React Agent, Docker Agent |
| **Partitura** | Guía musical | Agent Team Canvas (plan del proyecto) |
| **Concierto** | Resultado final | Aplicación funcionando |

**Clave**: El director (tú) no toca todos los instrumentos, pero sabe **cuándo** y **cómo** cada sección debe participar.

### ¿Por Qué Orquestar Agentes?

**Problema sin orquestación**:
```
Tú → Claude Code genérico → Hace "de todo" → Código inconsistente
```

**Solución con orquestación**:
```
Tú (Orchestrator) → Divide proyecto en tareas
                  ↓
    ┌─────────────┼─────────────┐
    ↓             ↓             ↓
Backend Agent  Frontend Agent  DevOps Agent
    ↓             ↓             ↓
Código Python  Código React    Dockerfile
especializado  optimizado      optimizado
```

**Ventajas**:
- ✅ **Especialización**: Cada agente es experto en su dominio
- ✅ **Consistencia**: Patrones específicos por área
- ✅ **Calidad**: Revisión especializada, no genérica
- ✅ **Escalabilidad**: Agrega más agentes según necesites
- ✅ **Aprendizaje**: Los agentes educan mientras construyen

---

## Agent Team Canvas Framework

El **Agent Team Canvas** es un framework para planificar y ejecutar proyectos usando equipos de agentes.

### 1. Project Decomposition (Dividir Proyecto)

**Paso 1**: Divide el proyecto en **capas arquitectónicas**:

```
Proyecto: E-commerce Platform
│
├── Layer 1: Backend API (FastAPI)
│   ├── Authentication & Authorization
│   ├── Product Management
│   ├── Shopping Cart
│   ├── Order Processing
│   └── Payment Integration
│
├── Layer 2: Database (PostgreSQL)
│   ├── Schema Design
│   ├── Migrations (Alembic)
│   ├── Indexes & Optimization
│   └── Seeding Data
│
├── Layer 3: Frontend (React)
│   ├── Authentication UI
│   ├── Product Catalog
│   ├── Shopping Cart UI
│   ├── Checkout Flow
│   └── User Dashboard
│
└── Layer 4: Infrastructure (Docker + Cloud)
    ├── Containerization
    ├── CI/CD Pipeline
    ├── Deployment (Railway/Render)
    └── Monitoring (Sentry)
```

**Paso 2**: Divide cada capa en **tareas atómicas**:

```
Backend API → Authentication
│
├── Task 1: Design JWT auth flow
├── Task 2: Implement user registration endpoint
├── Task 3: Implement login endpoint
├── Task 4: Implement token refresh
├── Task 5: Add password hashing (bcrypt)
├── Task 6: Protected route middleware
└── Task 7: Write unit tests (80% coverage)
```

### 2. Agent Assignment (Asignar Agentes)

**Matriz de Agente → Tarea**:

| Tarea | Agente Principal | Agente Revisor | Criterio de Éxito |
|-------|------------------|----------------|-------------------|
| Design JWT auth flow | Architecture Agent | Security Agent | Diagrama de flujo claro + sin vulnerabilidades |
| Implement registration | Python Best Practices | FastAPI Design | Código Pythonic + validación Pydantic |
| Add password hashing | Security Agent | Python Best Practices | bcrypt con salt rounds ≥12 |
| Write unit tests | Python Best Practices | - | Coverage ≥80% |
| Database schema | Database ORM | Architecture Agent | Normalized + indexes apropiados |
| React auth UI | React Integration | - | TypeScript sin errores + responsive |
| Dockerfile | Docker Infrastructure | Performance Agent | Multi-stage build + <200MB |

**Patrón**: Agente Principal construye → Agente Revisor valida → Tú apruebas.

### 3. Workflow Orchestration

**Workflow Típico**:

```
1. PLANNING PHASE
   ├── Tú: Define high-level requirements
   ├── Architecture Agent: Diseña estructura del proyecto
   └── Output: Project structure + tech stack decisions

2. IMPLEMENTATION PHASE (iterative)
   ├── Loop por cada feature:
   │   ├── Tú: Selecciona siguiente tarea del backlog
   │   ├── Agent Principal: Implementa tarea
   │   ├── Agent Revisor: Revisa implementación
   │   ├── Tú: Apruebas o pide ajustes
   │   └── Commit + push
   └── Hasta completar todas las tareas

3. INTEGRATION PHASE
   ├── Tú: Integra todas las piezas
   ├── Performance Agent: Optimiza bottlenecks
   ├── Security Agent: Audita vulnerabilidades
   └── Output: Aplicación funcionando end-to-end

4. DEPLOYMENT PHASE
   ├── Docker Agent: Configura containers
   ├── Performance Agent: Optimiza build
   ├── Tú: Deploy a producción
   └── Output: App live en Railway/Render/Vercel
```

### 4. Communication Patterns

**Pattern 1: Sequential (Cascada)**
```
Architecture Agent → Python Agent → FastAPI Agent → Testing
```
Uso: Cuando cada paso depende del anterior (ej: diseño → implementación → validación)

**Pattern 2: Parallel (Paralelo)**
```
                    ┌→ Backend Agent
Tú (Orchestrator) ──┼→ Frontend Agent
                    └→ DevOps Agent
```
Uso: Cuando tareas son independientes (ej: backend y frontend pueden construirse simultáneamente)

**Pattern 3: Review Chain (Cadena de Revisión)**
```
Python Agent (implementa) → FastAPI Agent (revisa API design) → Security Agent (revisa vulnerabilities) → Tú (apruebas)
```
Uso: Para código crítico que necesita múltiples revisiones especializadas

**Pattern 4: Iterative Refinement (Refinamiento Iterativo)**
```
Python Agent → Tú revisa → Python Agent (ajusta) → Tú revisa → ✓
```
Uso: Cuando necesitas múltiples rondas de feedback

---

## Claude Code Best Practices

Esta sección integra las mejores prácticas del artículo oficial de Anthropic: [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices).

### 1. Effective Prompting for Code Generation

#### ❌ Prompt Genérico (Evitar)
```
Create a user authentication system
```

#### ✅ Prompt Específico y Contextual
```
Create a JWT-based authentication system for FastAPI with:

Context:
- Python 3.12, FastAPI 0.118.0
- PostgreSQL database with SQLAlchemy
- Existing User model in api/models.py
- JWT_SECRET in environment variables

Requirements:
- POST /auth/register: email, password (min 8 chars) → 201 Created
- POST /auth/login: email, password → 200 OK + JWT token
- GET /auth/me: requires Bearer token → user info
- Password hashing with bcrypt (12 salt rounds)
- Token expiration: 60 minutes
- Pydantic validation for all inputs

Success criteria:
- Unit tests with 80% coverage
- No hardcoded secrets
- Type hints on all functions
- Follows existing code style in api/

Generate step by step:
1. Pydantic models (request/response)
2. Service layer (business logic)
3. API endpoints with dependency injection
4. Unit tests
```

**Principios**:
- ✅ **Context**: Tecnologías, versiones, código existente
- ✅ **Requirements**: Especificaciones detalladas
- ✅ **Constraints**: Limitaciones y estándares
- ✅ **Success Criteria**: Cómo saber que está completo
- ✅ **Step-by-step**: Divide en tareas manejables

### 2. Code Review with Agents

**Patrón de 3 Capas de Revisión**:

```python
# LAYER 1: Python Best Practices Agent
# Revisa: Pythonic code, type hints, docstrings, PEP 8

@app.post("/auth/register")
async def register_user(user_data: UserRegister):
    # Agent detecta: Falta type hint en return
    # Agent sugiere: Agregar -> UserResponse
    pass

# AFTER Layer 1:
@app.post("/auth/register")
async def register_user(user_data: UserRegister) -> UserResponse:
    """Register a new user with email and password."""
    pass
```

```python
# LAYER 2: FastAPI Design Agent
# Revisa: Status codes, validación Pydantic, dependency injection

@app.post("/auth/register")
async def register_user(user_data: UserRegister) -> UserResponse:
    # Agent detecta: Debería retornar 201 Created, no 200 OK
    # Agent detecta: Falta manejo de email duplicado
    pass

# AFTER Layer 2:
@app.post("/auth/register", status_code=201)
async def register_user(
    user_data: UserRegister,
    service: AuthService = Depends(get_auth_service)
) -> UserResponse:
    """Register a new user."""
    try:
        return service.register_user(user_data)
    except EmailAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Email already registered")
```

```python
# LAYER 3: Security Agent
# Revisa: Vulnerabilidades, secrets, injection attacks

@app.post("/auth/register", status_code=201)
async def register_user(
    user_data: UserRegister,
    service: AuthService = Depends(get_auth_service)
) -> UserResponse:
    # Agent detecta: Password mínimo muy corto (8 chars)
    # Agent sugiere: 12 chars mínimo + complexity requirements
    # Agent detecta: No hay rate limiting (brute force attack)
    pass

# AFTER Layer 3:
@app.post("/auth/register", status_code=201)
@limiter.limit("5/minute")  # Rate limiting
async def register_user(
    user_data: UserRegister,  # Pydantic valida: min_length=12, pattern
    service: AuthService = Depends(get_auth_service)
) -> UserResponse:
    """Register a new user with strong password requirements."""
    try:
        return service.register_user(user_data)
    except EmailAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Email already registered")
```

### 3. Iterative Development Pattern

**Cycle**: Red → Green → Refactor → Review

```
1. RED Phase (Tests First)
   ├── Tú: Describe behavior esperado
   ├── Python Agent: Escribe failing tests
   └── Verify: Tests fallan (red)

2. GREEN Phase (Implement)
   ├── Python Agent: Implementa código mínimo
   └── Verify: Tests pasan (green)

3. REFACTOR Phase (Optimize)
   ├── Python Agent: Limpia código
   ├── Performance Agent: Optimiza
   └── Verify: Tests aún pasan

4. REVIEW Phase (Quality)
   ├── FastAPI Agent: Revisa API design
   ├── Security Agent: Revisa vulnerabilities
   └── Tú: Apruebas y hace commit
```

### 4. Context Management

**Problema**: Claude Code tiene límite de contexto. Proyectos grandes exceden el límite.

**Solución**: Fragmenta el contexto por sesión.

**Estrategia 1: Feature-Based Sessions**
```
Session 1: Authentication (solo archivos de auth)
├── api/auth/endpoints.py
├── api/auth/service.py
├── api/auth/models.py
└── tests/test_auth.py

Session 2: Products (solo archivos de products)
├── api/products/endpoints.py
├── api/products/service.py
└── ...
```

**Estrategia 2: Layer-Based Sessions**
```
Session 1: Backend Only
├── Lee: api/**, tests/**
└── Ignora: frontend/

Session 2: Frontend Only
├── Lee: frontend/src/**
└── Ignora: api/
```

**Comando útil**:
```bash
# Lee solo archivos relevantes para la sesión
ls api/auth/*.py | xargs cat
```

### 5. Testing Multi-Agent Systems

Ver sección detallada: [Testing de Sistemas Multi-Agente](#testing-de-sistemas-multi-agente)

---

## 🤖 Construyendo con "Ejército de Agentes" (60% del contenido)

Esta es la sección práctica donde construyes un proyecto real usando equipos de agentes.

### Proyecto: E-commerce Platform con Agentes

Vamos a construir una plataforma de e-commerce **completa** usando orquestación de agentes:

**Features**:
- ✅ Autenticación JWT (usuarios y admins)
- ✅ Catálogo de productos con búsqueda/filtros
- ✅ Carrito de compras (persistente)
- ✅ Checkout y procesamiento de órdenes
- ✅ Panel de administración
- ✅ Integración de pagos (Stripe test mode)
- ✅ Notificaciones por email
- ✅ Dashboard de analytics

**Tech Stack**:
- Backend: FastAPI + PostgreSQL + SQLAlchemy + Alembic
- Frontend: React + TypeScript + TailwindCSS + React Query
- Infraestructura: Docker + Railway/Render + Vercel
- Testing: Pytest + Playwright
- Monitoring: Sentry

### Phase 1: Planning con Architecture Agent

#### Prompt Inicial
```
Actúa como Architecture Agent para un proyecto de e-commerce platform.

Requisitos del proyecto:
- Usuarios pueden registrarse, login, ver productos, agregar a carrito, hacer checkout
- Admins pueden agregar/editar/eliminar productos
- Integración con Stripe para pagos
- Notificaciones por email (SendGrid)
- Dashboard con analytics básicos (ventas, productos más vendidos)

Tecnologías:
- Backend: FastAPI + PostgreSQL + SQLAlchemy + Alembic
- Frontend: React + TypeScript + TailwindCSS
- Deploy: Railway (backend) + Vercel (frontend)

Genera:
1. Estructura completa de directorios (backend y frontend)
2. Modelos de base de datos con relaciones
3. Lista de endpoints de API (método, ruta, descripción)
4. Componentes principales de React
5. Diagrama de flujo de usuario (checkout flow)
6. Plan de implementación en fases

Prioriza: Arquitectura limpia, separación de concerns, escalabilidad
```

**Output del Architecture Agent** (ejemplo):

```
📁 ecommerce-platform/
├── backend/
│   ├── alembic/
│   │   ├── versions/
│   │   └── env.py
│   ├── api/
│   │   ├── auth/
│   │   │   ├── endpoints.py
│   │   │   ├── service.py
│   │   │   └── models.py
│   │   ├── products/
│   │   │   ├── endpoints.py
│   │   │   ├── service.py
│   │   │   └── models.py
│   │   ├── cart/
│   │   │   ├── endpoints.py
│   │   │   ├── service.py
│   │   │   └── models.py
│   │   ├── orders/
│   │   │   ├── endpoints.py
│   │   │   ├── service.py
│   │   │   └── models.py
│   │   ├── payments/
│   │   │   ├── stripe_integration.py
│   │   │   └── service.py
│   │   ├── admin/
│   │   │   └── endpoints.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   └── main.py
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_products.py
│   │   ├── test_cart.py
│   │   └── test_orders.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── auth/
    │   │   │   ├── LoginForm.tsx
    │   │   │   └── RegisterForm.tsx
    │   │   ├── products/
    │   │   │   ├── ProductCard.tsx
    │   │   │   ├── ProductList.tsx
    │   │   │   └── ProductFilters.tsx
    │   │   ├── cart/
    │   │   │   ├── CartItem.tsx
    │   │   │   └── CartSummary.tsx
    │   │   ├── checkout/
    │   │   │   ├── CheckoutForm.tsx
    │   │   │   └── PaymentForm.tsx
    │   │   └── admin/
    │   │       ├── ProductManagement.tsx
    │   │       └── OrdersDashboard.tsx
    │   ├── pages/
    │   │   ├── HomePage.tsx
    │   │   ├── ProductsPage.tsx
    │   │   ├── CartPage.tsx
    │   │   ├── CheckoutPage.tsx
    │   │   └── AdminDashboard.tsx
    │   ├── services/
    │   │   ├── api.ts
    │   │   ├── auth.service.ts
    │   │   ├── products.service.ts
    │   │   └── cart.service.ts
    │   ├── hooks/
    │   │   ├── useAuth.ts
    │   │   └── useCart.ts
    │   ├── types/
    │   │   └── index.ts
    │   └── App.tsx
    ├── package.json
    └── tsconfig.json

Database Models:
1. User (id, email, password_hash, role, created_at)
2. Product (id, name, description, price, stock, category, image_url)
3. Cart (id, user_id, created_at, updated_at)
4. CartItem (id, cart_id, product_id, quantity)
5. Order (id, user_id, total, status, created_at)
6. OrderItem (id, order_id, product_id, quantity, price_at_purchase)
7. Payment (id, order_id, stripe_payment_id, amount, status)

API Endpoints:
Auth:
- POST /auth/register
- POST /auth/login
- GET /auth/me
- POST /auth/refresh

Products:
- GET /products (list with pagination/filters)
- GET /products/{id}
- POST /products (admin only)
- PUT /products/{id} (admin only)
- DELETE /products/{id} (admin only)

Cart:
- GET /cart (get user's cart)
- POST /cart/items (add item)
- PUT /cart/items/{id} (update quantity)
- DELETE /cart/items/{id} (remove item)
- DELETE /cart (clear cart)

Orders:
- POST /orders (create from cart)
- GET /orders (user's orders)
- GET /orders/{id}
- GET /admin/orders (all orders, admin only)

Payments:
- POST /payments/create-intent (Stripe)
- POST /payments/confirm

Implementation Plan:
Phase 1: Database + Auth (2-3 days)
Phase 2: Products CRUD (1-2 days)
Phase 3: Cart functionality (1-2 days)
Phase 4: Orders + Payments (2-3 days)
Phase 5: Admin panel (1-2 days)
Phase 6: Frontend integration (3-4 days)
Phase 7: Testing + Deployment (2-3 days)
```

### Phase 2: Implementation con Agentes Especializados

#### Ejemplo: Implementar Authentication

**Step 1: Setup con Database ORM Agent**

```
Prompt para Database ORM Agent:

Crea el modelo User en SQLAlchemy para e-commerce:

Requirements:
- Campos: id (UUID primary key), email (unique, indexed), password_hash,
  role (enum: 'customer', 'admin'), created_at, updated_at
- Email validation: formato válido, max 255 chars
- Role: default 'customer'
- Timestamps automáticos

Genera también:
1. Alembic migration inicial
2. Función auxiliar para crear admin user (seeding)
3. Tests de modelo (constraints, defaults)
```

**Output**:
```python
# api/models/user.py
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import enum

from api.database import Base

class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.email}>"
```

**Step 2: Implementar con Python Best Practices Agent**

```
Prompt para Python Agent:

Implementa el servicio de autenticación usando el modelo User:

Requirements:
- Función register_user(email, password) → User
  - Valida email format
  - Valida password strength (min 12 chars, uppercase, lowercase, digit)
  - Hash password con bcrypt (12 rounds)
  - Guarda en DB
  - Lanza EmailAlreadyExistsError si duplicado

- Función login_user(email, password) → JWT token
  - Verifica credenciales
  - Genera JWT con user_id y role
  - Token expira en 60 minutos
  - Lanza InvalidCredentialsError si falla

- Función get_current_user(token) → User
  - Decodifica JWT
  - Verifica expiración
  - Retorna User desde DB
  - Lanza TokenExpiredError o InvalidTokenError

Usa type hints, docstrings, y manejo robusto de errores.
```

**Output**: Ver código completo en `ejemplos/auth_service.py`

**Step 3: Revisar con FastAPI Design Agent**

```
Prompt para FastAPI Agent:

Revisa los endpoints de autenticación y sugiere mejoras:

[Pega código de api/auth/endpoints.py]

Criteria:
- ¿Status codes correctos? (201 para register, 200 para login, 401/403 apropiados)
- ¿Pydantic models bien definidos?
- ¿Dependency injection usado correctamente?
- ¿Documentación OpenAPI clara?
- ¿Manejo de errores consistente?
```

**Step 4: Auditar con Security Agent**

```
Prompt para Security Agent:

Audita el sistema de autenticación buscando vulnerabilidades:

[Pega código de auth service y endpoints]

Revisa:
- ¿Password hashing seguro?
- ¿JWT secrets bien manejados?
- ¿Rate limiting en endpoints de auth?
- ¿Timing attacks prevenidos?
- ¿SQL injection prevenido?
- ¿CORS configurado correctamente?
```

### Phase 3: Frontend con React Integration Agent

```
Prompt para React Agent:

Crea el componente LoginForm usando React + TypeScript + TailwindCSS:

Requirements:
- Form con email y password inputs
- Validación client-side (email format, password not empty)
- Submit llama a API POST /auth/login
- Loading state durante request
- Error handling (muestra mensaje de error)
- Success: guarda token en localStorage y redirige a /
- Responsive design con Tailwind
- Accessible (labels, ARIA attributes)

Usa React Hook Form + Zod para validación
```

### Phase 4: Integration Testing

```
Prompt para Python Agent + React Agent:

Crea tests de integración end-to-end para el flujo de autenticación:

Backend (pytest):
1. Test register → login → access protected endpoint (200)
2. Test register con email duplicado → 409
3. Test login con credenciales incorrectas → 401
4. Test access protected endpoint sin token → 401
5. Test access con token expirado → 401

Frontend (Playwright):
1. Test register flow completo
2. Test login flow completo
3. Test error handling (credenciales incorrectas)
4. Test auto-logout si token expira
5. Test protected route redirect si no autenticado
```

### Phase 5: Performance Optimization

```
Prompt para Performance Agent:

Optimiza el sistema de autenticación para manejar 1000 requests/segundo:

Current bottlenecks:
- Cada request protegido hace query a DB para get_current_user
- Password hashing bloquea event loop
- JWT decoding en cada request

Sugiere optimizaciones con código:
1. Caching de user data (Redis o in-memory)
2. Async password hashing
3. JWT decoding optimization
4. Database connection pooling
```

### Phase 6: Deployment con Docker Agent

```
Prompt para Docker Agent:

Crea configuración de Docker para e-commerce platform:

Requirements:
- Multi-stage build para backend (Python)
- Multi-stage build para frontend (Node)
- docker-compose.yml con:
  - Backend service (FastAPI)
  - Frontend service (Nginx serving React build)
  - PostgreSQL service
  - Redis service (caching)
- Health checks para todos los servicios
- Optimización de imagen size (<200MB por service)
- Environment variables desde .env file
- Volume para PostgreSQL data persistence

Genera:
1. backend/Dockerfile
2. frontend/Dockerfile
3. docker-compose.yml
4. .dockerignore files
```

---

## Proyecto Final: E-commerce Platform

Ver carpeta `proyecto-final/` para implementación completa del proyecto con todos los agentes trabajando en coordinación.

**Estructura del proyecto final**:
```
proyecto-final/
├── README.md (instrucciones de setup)
├── AGENTS_WORKFLOW.md (documenta qué agente hizo qué)
├── backend/
│   └── (código completo de backend)
├── frontend/
│   └── (código completo de frontend)
└── docs/
    ├── ARCHITECTURE.md (decisiones de arquitectura)
    ├── API_REFERENCE.md (documentación de API)
    └── DEPLOYMENT.md (guía de deployment)
```

**Métricas del proyecto**:
- **Líneas de código**: ~3000 (backend) + ~2000 (frontend)
- **Test coverage**: >80% backend, >70% frontend
- **Performance**: <100ms response time (p95)
- **Agentes usados**: 7 agentes especializados
- **Tiempo de desarrollo**: ~2 semanas (vs 4-6 semanas solo)

---

## Testing de Sistemas Multi-Agente

### 1. Unit Testing de Código Generado

**Estrategia**: Cada agente debe generar sus propios tests.

```
Regla: "No code without tests"

Python Agent implementa función → Python Agent escribe tests
React Agent crea componente → React Agent escribe tests
```

**Ejemplo**:
```python
# Python Agent implementa
def calculate_cart_total(cart_items: List[CartItem]) -> Decimal:
    return sum(item.product.price * item.quantity for item in cart_items)

# Python Agent también escribe test
def test_calculate_cart_total():
    items = [
        CartItem(product=Product(price=Decimal("10.00")), quantity=2),
        CartItem(product=Product(price=Decimal("5.50")), quantity=1),
    ]
    assert calculate_cart_total(items) == Decimal("25.50")
```

### 2. Integration Testing Between Agents

**Problema**: Backend Agent y Frontend Agent trabajan independientemente. ¿Cómo asegurar que se integran correctamente?

**Solución**: Contract Testing

```typescript
// Frontend Agent define el contrato esperado
interface AuthAPI {
  login(email: string, password: string): Promise<{ token: string }>;
  register(email: string, password: string): Promise<{ user: User }>;
}

// Backend Agent implementa el contrato
@app.post("/auth/login")
def login(credentials: LoginRequest) -> LoginResponse:
    # Debe retornar exactamente { "token": "..." }
    pass
```

**Test de contrato**:
```python
def test_login_response_contract():
    """Verifica que /auth/login retorna el formato esperado por frontend."""
    response = client.post("/auth/login", json={"email": "...", "password": "..."})
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert isinstance(data["token"], str)
    assert len(data["token"]) > 0
```

### 3. End-to-End Testing del Sistema Completo

**Herramienta**: Playwright (frontend) + pytest (backend)

**Ejemplo de test E2E**:
```typescript
// Playwright test escrito por React Agent
test('complete checkout flow', async ({ page }) => {
  // 1. Register
  await page.goto('/register');
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'SecurePass123!');
  await page.click('button[type="submit"]');

  // 2. Browse products
  await expect(page).toHaveURL('/');
  await page.click('text=View Products');

  // 3. Add to cart
  await page.click('button:has-text("Add to Cart")').first();
  await expect(page.locator('.cart-badge')).toHaveText('1');

  // 4. Checkout
  await page.click('text=Cart');
  await page.click('text=Checkout');

  // 5. Payment (test mode)
  await page.fill('input[name="cardNumber"]', '4242424242424242');
  await page.fill('input[name="expiry"]', '12/25');
  await page.fill('input[name="cvc"]', '123');
  await page.click('button:has-text("Pay Now")');

  // 6. Verify success
  await expect(page.locator('.order-success')).toBeVisible();
});
```

### 4. Performance Testing

```
Prompt para Performance Agent:

Crea script de load testing para e-commerce API:

Scenarios:
1. 100 concurrent users browsing products
2. 50 concurrent users adding to cart
3. 10 concurrent users checking out

Tools: locust.io

Métricas a medir:
- Response time (p50, p95, p99)
- Throughput (requests/second)
- Error rate
- Database connection pool usage

Target performance:
- Product listing: <100ms (p95)
- Add to cart: <50ms (p95)
- Checkout: <500ms (p95)
- Error rate: <0.1%
```

---

## Monitoring y Debugging Avanzado

### 1. Sentry para Error Tracking

**Setup con múltiples agentes**:

```
Backend (Python Agent + Security Agent):
- Captura excepciones no manejadas
- Filtra información sensible (passwords, tokens)
- Incluye contexto: user_id, endpoint, request body

Frontend (React Agent):
- Error boundaries
- Promise rejection handling
- Breadcrumbs (user actions antes del error)
```

**Código generado**:
```python
# Backend: api/main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1,
    profiles_sample_rate=0.1,
    before_send=scrub_sensitive_data,  # Security Agent genera esto
)

def scrub_sensitive_data(event, hint):
    """Remove passwords, tokens, credit cards from Sentry events."""
    # Security Agent implementa scrubbing
    pass
```

### 2. Structured Logging

```
Prompt para Python Agent:

Agrega structured logging a todo el backend:

Requirements:
- Use Python logging con formato JSON
- Log levels: DEBUG (development), INFO (production)
- Incluye en cada log: timestamp, level, user_id (si auth), endpoint, duration
- Log de business events: user_registered, product_purchased, payment_failed
- Configurable via environment variable LOG_LEVEL

Ejemplo de log entry:
{
  "timestamp": "2025-10-25T14:30:00Z",
  "level": "INFO",
  "user_id": "abc-123",
  "endpoint": "/orders",
  "method": "POST",
  "status_code": 201,
  "duration_ms": 145,
  "event": "order_created",
  "order_id": "ord-456"
}
```

### 3. Debugging Multi-Agent Issues

**Problema**: Un bug aparece. ¿Qué agente lo causó?

**Solución**: Git Blame + Agent Attribution

```bash
# Ver qué agente escribió el código problemático
git log --pretty=format:"%h %an %s" -- api/auth/service.py

# Ejemplo de commit message:
# feat(auth): implement JWT refresh - Python Best Practices Agent
```

**Strategy**: En cada commit, documenta qué agente generó el código:
```
feat(auth): implement JWT token refresh

Generated by: Python Best Practices Agent
Reviewed by: Security Agent
Approved by: Manuel (human)

Implementation includes:
- Refresh token generation
- Token rotation
- Blacklist for revoked tokens

Tests: 95% coverage
```

### 4. Agent Performance Metrics

**Pregunta**: ¿Qué agentes son más efectivos?

**Métricas a trackear**:

| Agente | Código Generado | Bugs Introducidos | Tests Coverage | Review Time |
|--------|-----------------|-------------------|----------------|-------------|
| Python Agent | 1200 LOC | 3 | 92% | 15 min |
| FastAPI Agent | 800 LOC | 1 | 88% | 10 min |
| React Agent | 1500 LOC | 5 | 75% | 20 min |
| Security Agent | 0 (solo reviews) | -8 (previno bugs) | N/A | 30 min |

**Insight**: Security Agent "previno" 8 bugs encontrando vulnerabilidades antes de merge.

---

## Ejercicios Prácticos

### Ejercicio 1: Mini-Proyecto con 3 Agentes

**Objetivo**: Construir TODO app usando Architecture + Python + React Agents

**Requirements**:
- Backend: FastAPI con endpoints CRUD
- Frontend: React con lista de TODOs
- No database (in-memory)

**Workflow**:
1. Architecture Agent: Diseña estructura
2. Python Agent: Implementa backend + tests
3. React Agent: Implementa frontend
4. Tú: Integras y verifica que funciona

**Success Criteria**:
- 3 agentes usados
- E2E flow funciona (crear, listar, completar TODO)
- Tests >80% coverage

### Ejercicio 2: Refactoring con Agentes

**Objetivo**: Refactoriza código legacy usando Performance + Security Agents

**Código legacy** (proporcionado):
```python
# api/products.py (código "malo" intencionalmente)
@app.get("/products")
def get_products(category: str = None):
    # N+1 query problem
    products = db.query(Product).all()
    result = []
    for p in products:
        if category is None or p.category == category:
            result.append({
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "reviews": [r.text for r in p.reviews]  # N+1!
            })
    return result
```

**Tasks**:
1. Performance Agent: Detecta N+1, sugiere eager loading
2. Security Agent: Detecta SQL injection si category viene de query param sin validación
3. Python Agent: Refactoriza con mejores prácticas
4. FastAPI Agent: Mejora API design (pagination, Pydantic models)

**Success Criteria**:
- Queries optimizadas (1 query en vez de N+1)
- Pydantic validation
- Pagination agregada
- Tests verifican mejoras

### Ejercicio 3: Feature Completo End-to-End

**Objetivo**: Implementar "Product Reviews" feature usando todos los agentes

**Requirements**:
- Usuarios pueden dejar reviews (rating 1-5 + texto)
- Productos muestran rating promedio
- Admin puede moderar reviews (aprobar/rechazar)

**Agents usados**:
- Architecture Agent: Diseña DB schema (Review model)
- Database ORM Agent: Implementa modelo + migration
- Python Agent: Implementa service layer
- FastAPI Agent: Crea endpoints
- React Agent: Crea UI de reviews
- Security Agent: Previene spam/abuse
- Performance Agent: Optimiza queries de rating promedio

**Success Criteria**:
- Feature funcionando E2E
- 6+ agentes usados
- Documentación de workflow (qué agente hizo qué)
- Tests de integración

---

## Recursos Adicionales

### Artículos de Anthropic (Lectura Obligatoria)

1. **[Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)**
   - Prompting efectivo para generación de código
   - Code review patterns
   - Context management

2. **[Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)**
   - Arquitectura de sistemas multi-agente
   - Coordinación entre agentes
   - Caso de estudio real

3. **[Agent Skills Framework](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)**
   - Diseño de agentes especializados
   - Composición de habilidades
   - Best practices

4. **[Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)**
   - Optimización de contexto
   - Fragmentación de tareas
   - Memory management

### Tools y Frameworks

- **[Claude Code](https://claude.ai/code)**: IDE oficial de Anthropic
- **[LangChain](https://python.langchain.com/)**: Framework para apps con LLMs
- **[LangGraph](https://github.com/langchain-ai/langgraph)**: Orquestación de agentes
- **[AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)**: Agentes autónomos
- **[CrewAI](https://github.com/joaomdmoura/crewAI)**: Framework para equipos de agentes

### Libros Recomendados

- **"Building LLM Apps"** by Maxime Labonne
- **"Prompt Engineering Guide"** by DAIR.AI
- **"The Pragmatic Programmer"** (context: cómo dividir proyectos grandes)

### Comunidades

- **Claude Code Discord**: Comunidad oficial de Claude Code
- **r/ClaudeAI** (Reddit): Discusiones y ejemplos
- **LangChain Discord**: Para orquestación de agentes

---

## Glosario

- **Agent Orchestration**: Coordinación de múltiples agentes especializados en un sistema
- **Agent Team Canvas**: Framework para planificar proyectos multi-agente
- **Specialized Agent**: Agente con expertise en un dominio específico (ej: Python, React)
- **Sequential Workflow**: Agentes trabajan uno después del otro (cascada)
- **Parallel Workflow**: Agentes trabajan simultáneamente en tareas independientes
- **Review Chain**: Múltiples agentes revisan código secuencialmente
- **Context Window**: Límite de tokens que un agente puede procesar
- **Contract Testing**: Verificar que componentes se integran según contrato definido
- **Agent Attribution**: Documentar qué agente generó qué código (git blame)
- **Multi-Agent System**: Sistema donde múltiples agentes colaboran
- **Orchestrator**: Entidad (humano o agente) que coordina otros agentes
- **Task Decomposition**: Dividir proyecto grande en tareas pequeñas
- **Agent Handoff**: Transferir tarea de un agente a otro

---

## Reflexión Final: Lecciones Aprendidas

Al completar esta clase, deberías poder responder:

1. **¿Cuándo usar múltiples agentes vs uno genérico?**
   - Múltiples: Proyectos grandes, expertise específico necesario
   - Uno: Tareas simples, prototipos rápidos

2. **¿Cuál es el rol del humano en orquestación?**
   - Definir visión y prioridades
   - Asignar tareas a agentes apropiados
   - Revisar y aprobar outputs críticos
   - Resolver conflictos entre agentes

3. **¿Qué aprendiste sobre tu propio workflow de desarrollo?**
   - Dividir proyectos grandes es crucial
   - Especialización mejora calidad
   - Testing es fundamental incluso con agentes

4. **¿Cómo cambió tu velocidad de desarrollo?**
   - Mide: Tiempo antes vs después de usar agentes
   - Objetivo: 2-3x más rápido con igual o mejor calidad

5. **¿Qué agentes fueron más valiosos para ti?**
   - Identifica tus agentes MVP
   - Crea más agentes en áreas donde necesitas ayuda

---

**Siguiente paso**: ¡Construye tu propio proyecto con tu ejército de agentes!

**Clase anterior**: [Módulo 5 - Clase 4: Despliegue Full-Stack](../Clase%204%20-%20Despliegue%20Full-Stack/README.md)

---

**🎓 Has completado el Master en Desarrollo con IA**

Ahora eres capaz de:
- ✅ Construir aplicaciones full-stack con FastAPI + React
- ✅ Implementar arquitectura limpia y SOLID
- ✅ Integrar seguridad (JWT, bcrypt, auditorías)
- ✅ Desplegar a producción (Docker, Railway, Vercel)
- ✅ **Orquestar equipos de agentes especializados**
- ✅ Ser **"un desarrollador con un ejército de agentes"**

**¡Felicidades! 🎉**
