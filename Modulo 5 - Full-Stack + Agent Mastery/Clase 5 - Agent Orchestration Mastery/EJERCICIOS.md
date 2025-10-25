# Ejercicios Prácticos: Agent Orchestration Mastery

Estos ejercicios te preparan gradualmente para el proyecto final, introduciendo conceptos de orquestación de agentes de forma progresiva.

## 📋 Tabla de Contenidos

1. [Ejercicio 1: TODO App con 3 Agentes (Básico)](#ejercicio-1-todo-app-con-3-agentes)
2. [Ejercicio 2: Refactoring con Agentes (Intermedio)](#ejercicio-2-refactoring-con-agentes)
3. [Ejercicio 3: Product Reviews Feature (Avanzado)](#ejercicio-3-product-reviews-feature)
4. [Ejercicio 4: Performance Optimization Challenge](#ejercicio-4-performance-optimization-challenge)
5. [Ejercicio 5: Security Audit Sprint](#ejercicio-5-security-audit-sprint)

---

## Ejercicio 1: TODO App con 3 Agentes

**Nivel**: Básico
**Tiempo estimado**: 4-6 horas
**Agentes**: Architecture, Python Best Practices, React Integration

### Objetivo

Construir una TODO app simple usando 3 agentes especializados, aprendiendo el workflow básico de orquestación.

### Requirements

**Backend (FastAPI)**:
- POST /todos - Crear TODO
- GET /todos - Listar TODOs
- PUT /todos/{id} - Actualizar TODO (marcar completado)
- DELETE /todos/{id} - Eliminar TODO
- In-memory storage (no database)

**Frontend (React)**:
- Lista de TODOs
- Form para crear TODO
- Checkbox para marcar completado
- Botón para eliminar

### Workflow

**Step 1: Planning (30 min)**

Prompt para Architecture Agent:
```
Diseña arquitectura simple para TODO app:

Backend: FastAPI (in-memory storage)
Frontend: React + TypeScript

Genera:
1. Estructura de directorios (backend y frontend)
2. Pydantic models para TODO (id, title, completed)
3. Lista de 4 endpoints REST
4. React components principales (TodoList, TodoForm, TodoItem)

Mantén simple - no database, no auth.
```

Documenta output en mini-canvas (1 página):
- Features: CRUD de TODOs
- Agents: Architecture, Python BP, React Integration
- Tasks: 6-8 tasks principales

**Step 2: Backend Implementation (1.5-2 hours)**

Prompt para Python Best Practices Agent:
```
Implementa backend de TODO app en FastAPI.

CONTEXT:
- Python 3.12, FastAPI 0.118.0
- In-memory storage (global dict)
- UUID for TODO ids

REQUIREMENTS:
[Pega output de Architecture Agent sobre endpoints]

CONSTRAINTS:
- Type hints en todas las funciones
- Pydantic models para request/response
- Docstrings estilo Google
- Unit tests con pytest (≥80% coverage)
- Error handling (404 si TODO no existe)

Generate:
1. api/main.py con endpoints
2. api/models.py con Pydantic models
3. api/storage.py con in-memory CRUD
4. tests/test_todos.py con tests comprehensivos
```

**Step 3: Frontend Implementation (1.5-2 hours)**

Prompt para React Integration Agent:
```
Implementa frontend de TODO app en React + TypeScript.

CONTEXT:
- React 18, TypeScript 5
- TailwindCSS for styling
- No state management library (useState es suficiente)
- API en http://localhost:8000

REQUIREMENTS:
[Pega output de Architecture Agent sobre components]

UI Features:
- Input para nuevo TODO + botón "Add"
- Lista de TODOs con checkbox y botón delete
- Loading state durante requests
- Error handling (toast notifications)

CONSTRAINTS:
- TypeScript strict mode
- Responsive design
- Accessible (labels, aria-attributes)
- No external libraries (excepto axios para API calls)

Generate:
1. src/components/TodoList.tsx
2. src/components/TodoForm.tsx
3. src/components/TodoItem.tsx
4. src/services/api.ts (axios wrapper)
5. src/App.tsx (integra components)
```

**Step 4: Integration & Testing (30-45 min)**

1. Run backend: `uvicorn api.main:app --reload`
2. Run frontend: `npm run dev`
3. Test E2E flow manualmente:
   - Create TODO
   - Mark as completed
   - Delete TODO
4. Run tests: `pytest --cov`

**Step 5: Mini Lessons Learned (15 min)**

Documenta en 1 página:
- ¿Qué agente fue más útil?
- ¿Cuánto código generaron vs cuánto ajustaste?
- ¿Qué aprendiste sobre prompting?
- ¿Harías algo diferente next time?

### Success Criteria

- [ ] App funciona E2E (crear, completar, eliminar)
- [ ] Backend tests ≥80% coverage
- [ ] Frontend compila sin TypeScript errors
- [ ] 3 agentes usados y documentados
- [ ] Mini lessons learned completado

---

## Ejercicio 2: Refactoring con Agentes

**Nivel**: Intermedio
**Tiempo estimado**: 3-4 horas
**Agentes**: Performance, Security, Python Best Practices, FastAPI Design

### Objetivo

Tomar código legacy "malo" (proporcionado) y refactorizarlo usando múltiples agentes, aprendiendo el workflow de review chains.

### Código Legacy Proporcionado

```python
# api/products.py (CÓDIGO "MALO" INTENCIONALMENTE)

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Fake database
products_db = [
    {"id": 1, "name": "Laptop", "price": 999, "category": "electronics"},
    {"id": 2, "name": "Mouse", "price": 25, "category": "electronics"},
    # ... más productos
]

class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str

@app.get("/products")
def get_products(category: str = None, min_price: float = None, max_price: float = None):
    """Get products with filters."""
    results = []
    for p in products_db:  # O(n) - no optimizado
        if category and p["category"] != category:
            continue
        if min_price and p["price"] < min_price:
            continue
        if max_price and p["price"] > max_price:
            continue

        # N+1 problem simulado (cada producto hace query a reviews)
        reviews = get_reviews(p["id"])  # Función separada
        p["reviews"] = reviews
        results.append(p)

    return results

def get_reviews(product_id):
    # Simula query a database (muy lento)
    import time
    time.sleep(0.1)  # 100ms por producto!
    return [{"text": "Great product!", "rating": 5}]
```

**Problemas en el código**:
- No usa Pydantic validation para filters
- No pagination (devuelve todos los productos)
- N+1 problem (get_reviews en loop)
- No type hints
- No error handling
- SQL injection vulnerable si `category` viniera de query string sin validar
- No logging
- Performance terrible (100ms * N productos)

### Workflow

**Step 1: Performance Agent Audit (30 min)**

```
Prompt:
Audita este código para problemas de performance:

[Pega código legacy]

Identifica:
1. N+1 query problems
2. Operaciones O(n) innecesarias
3. Blocking operations (time.sleep)
4. Missing pagination
5. Inefficient data structures

Sugiere optimizaciones específicas con código.
```

**Step 2: Security Agent Audit (30 min)**

```
Prompt:
Security audit de este endpoint:

[Pega código legacy]

Busca:
1. SQL injection vulnerabilities
2. Missing input validation
3. Information leakage
4. DoS attack vectors (ej: devolver millones de productos)
5. Missing rate limiting

Provide severity (Critical, High, Medium, Low) y fixes.
```

**Step 3: Python Best Practices Agent Refactor (1-1.5 hours)**

```
Prompt:
Refactoriza este código siguiendo Python best practices:

[Pega código legacy + outputs de Performance & Security agents]

Requirements:
- Fix ALL performance issues (N+1, pagination, etc)
- Fix ALL security issues (validation, sanitization)
- Add type hints
- Add docstrings
- Add error handling
- Add logging
- Write unit tests (≥85% coverage)

Context:
- Usar SQLAlchemy ORM (no raw queries)
- Pydantic for validation
- FastAPI dependency injection
```

**Step 4: FastAPI Design Agent Review (30 min)**

```
Prompt:
Review este endpoint refactorizado para API design:

[Pega código refactorizado]

Check:
- Correct HTTP status codes
- Pydantic models well-structured
- Pagination following REST standards
- Error responses consistent
- OpenAPI documentation clear

Suggest improvements.
```

**Step 5: Before/After Comparison (30 min)**

Crea documento comparando:

| Métrica | Before | After | Improvement |
|---------|--------|-------|-------------|
| Response time (10 products) | 1000ms | 50ms | 20x faster |
| Type safety | None | Full | ✅ |
| Test coverage | 0% | 88% | ✅ |
| Security vulnerabilities | 3 High | 0 | ✅ |
| Lines of code | 35 | 120 | Trade-off OK |

**Step 6: Lessons Learned (15 min)**

Documenta:
- ¿Qué issues fueron más críticos?
- ¿Qué agente fue más valuable?
- ¿Cómo cambió tu código después de 4 reviews?
- ¿Aprendiste algo nuevo sobre performance/security?

### Success Criteria

- [ ] 4 agentes usados (Performance, Security, Python BP, FastAPI Design)
- [ ] Todos los performance issues fixed
- [ ] Todos los security issues fixed
- [ ] Tests ≥85% coverage
- [ ] Before/After comparison documentado
- [ ] Lessons learned completado

---

## Ejercicio 3: Product Reviews Feature

**Nivel**: Avanzado
**Tiempo estimado**: 8-12 horas
**Agentes**: Architecture, Database ORM, Python BP, FastAPI Design, React Integration, Security, Performance

### Objetivo

Implementar feature completo end-to-end usando 6-7 agentes, practicando workflow real de proyecto.

### Requirements

**Backend**:
- Users can leave reviews on products (rating 1-5 + text comment)
- Products show average rating
- Admin can moderate reviews (approve/reject)
- List reviews with pagination
- Filter reviews by rating

**Frontend**:
- Product detail page shows reviews
- Form to submit review (authenticated users only)
- Star rating component
- Admin panel to moderate reviews
- Loading and error states

### Database Schema

```sql
CREATE TABLE reviews (
    id UUID PRIMARY KEY,
    product_id UUID REFERENCES products(id),
    user_id UUID REFERENCES users(id),
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    comment TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending', -- pending, approved, rejected
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Actualizar products table
ALTER TABLE products ADD COLUMN average_rating DECIMAL(2,1);
ALTER TABLE products ADD COLUMN review_count INTEGER DEFAULT 0;
```

### Workflow (Similar a Proyecto Final)

**Phase 1: Planning con Mini-Canvas**
1. Crea Agent Team Canvas (usa template)
2. Architecture Agent: diseña feature
3. Agent Assignment Matrix con 15-20 tasks

**Phase 2: Implementation**
1. Database ORM Agent: Review model + migration
2. Python BP Agent: Review service (CRUD)
3. FastAPI Design Agent: Review endpoints
4. React Integration Agent: Review components
5. Security Agent: Review security (spam prevention, abuse)
6. Performance Agent: Optimize rating calculation

**Phase 3: Integration**
1. Integration tests (API)
2. E2E tests (Playwright)
3. Performance testing

### Special Challenges

**Challenge 1: Optimized Average Rating**

Problema: Calcular average rating haciendo query a todas las reviews es lento (O(n)).

Solución: Usar triggers de PostgreSQL o mantener counter en products table.

Prompt para Database ORM Agent:
```
Optimiza el cálculo de average_rating para productos.

Current approach (slow):
- Cada vez que se pide product, query todas sus reviews y calcula average

Better approach:
- Mantener average_rating y review_count en products table
- Actualizar automáticamente cuando review se crea/actualiza/elimina

Implementa usando:
1. PostgreSQL trigger, O
2. SQLAlchemy event listeners

Include Alembic migration.
```

**Challenge 2: Spam Prevention**

Prompt para Security Agent:
```
Implementa protección contra spam de reviews.

Requirements:
- User puede dejar solo 1 review por producto
- Rate limiting: 5 reviews/hour por user
- Admin puede flagear users como spammers
- Validación: comment min 10 chars, max 500 chars
- Detect abusive language (simple keyword filter)

Generate:
1. Database constraints (unique user_id + product_id)
2. Rate limiting middleware
3. Content validation
4. Tests
```

### Success Criteria

- [ ] Feature completo E2E (crear, listar, moderar reviews)
- [ ] 6+ agentes usados
- [ ] Agent Team Canvas completo
- [ ] Average rating optimizado (≤10ms calculation)
- [ ] Security measures implemented (spam prevention)
- [ ] Tests ≥80% coverage
- [ ] Lessons learned detallado

---

## Ejercicio 4: Performance Optimization Challenge

**Nivel**: Avanzado
**Tiempo estimado**: 4-6 horas
**Agente Principal**: Performance Optimizer

### Objetivo

Optimizar aplicación lenta usando profiling y técnicas avanzadas.

### Scenario

Te dan una API de e-commerce que es MUY lenta:

- `/products` → 2.5 seconds
- `/cart` → 1.2 seconds
- `/checkout` → 4.8 seconds

**Tu meta**: Reducir a <100ms (p95)

### Código Proporcionado

```python
# api/products.py (LENTO)

@app.get("/products")
def list_products():
    # N+1 problem
    products = db.query(Product).all()  # 1 query
    for p in products:
        p.category_name = p.category.name  # N queries
        p.reviews_count = len(p.reviews)  # N queries
        p.avg_rating = sum(r.rating for r in p.reviews) / len(p.reviews) if p.reviews else 0  # N queries

    # Serialization muy lenta
    return [ProductSchema.from_orm(p).dict() for p in products]  # O(n) Pydantic serialization
```

### Tasks

**Task 1: Profiling (30 min)**

Use cProfile para identificar bottlenecks:

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Run slow endpoint
list_products()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

Documenta los top 5 slowest functions.

**Task 2: Database Optimization (1-1.5 hours)**

Prompt para Performance Agent:
```
Optimiza este endpoint que toma 2.5 segundos:

[Pega código]

Profiling muestra:
1. db.query(Product).all() - 50ms
2. p.category.name (in loop) - 1200ms (N+1)
3. len(p.reviews) (in loop) - 800ms (N+1)
4. Pydantic serialization - 450ms

Optimizations needed:
- Eager loading (joinedload/selectinload)
- Denormalization (cache review_count, avg_rating)
- Batch serialization
- Database indexes

Provide optimized code + Alembic migration if needed.
```

**Task 3: Caching (1 hour)**

Add Redis caching para product catalog:

```python
from redis import Redis
redis_client = Redis(host='localhost', port=6379)

@app.get("/products")
async def list_products():
    # Try cache
    cached = redis_client.get("products:all")
    if cached:
        return json.loads(cached)

    # Query DB (optimized)
    products = db.query(Product).options(
        joinedload(Product.category),
        selectinload(Product.reviews)
    ).all()

    result = [ProductSchema.from_orm(p).dict() for p in products]

    # Cache for 5 minutes
    redis_client.setex("products:all", 300, json.dumps(result))

    return result
```

**Task 4: Async donde Sea Apropiado (1 hour)**

Convert blocking I/O to async:

```python
# Before (blocking)
def send_order_confirmation_email(order_id):
    email_service.send(...)  # Blocks for 2 seconds!

# After (async)
import asyncio

async def send_order_confirmation_email(order_id):
    await asyncio.to_thread(email_service.send, ...)

@app.post("/checkout")
async def checkout():
    order = create_order(...)

    # Send email asynchronously (don't wait)
    asyncio.create_task(send_order_confirmation_email(order.id))

    return order  # Return immediately
```

**Task 5: Load Testing (30-45 min)**

Use locust.io para verificar mejoras:

```python
# locustfile.py
from locust import HttpUser, task, between

class EcommerceUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def view_products(self):
        self.client.get("/products")

    @task(1)
    def view_cart(self):
        self.client.get("/cart")
```

Run: `locust -f locustfile.py --host=http://localhost:8000`

Target: 100 RPS with p95 <100ms

### Success Criteria

- [ ] `/products` optimizado: 2.5s → <50ms
- [ ] `/cart` optimizado: 1.2s → <30ms
- [ ] `/checkout` optimizado: 4.8s → <80ms
- [ ] Load testing muestra 100+ RPS
- [ ] Documented optimizations (before/after)
- [ ] Profiling data included

---

## Ejercicio 5: Security Audit Sprint

**Nivel**: Avanzado
**Tiempo estimado**: 3-4 horas
**Agente Principal**: Security Agent

### Objetivo

Auditar aplicación vulnerable y fix todas las security issues encontradas.

### Vulnerable Code Proporcionado

```python
# api/auth.py (VULNERABLE!)

import hashlib

users_db = {}

@app.post("/register")
def register(email: str, password: str):
    # ❌ Password stored in plaintext!
    users_db[email] = password
    return {"message": "User created"}

@app.post("/login")
def login(email: str, password: str):
    # ❌ Timing attack vulnerable!
    if email in users_db and users_db[email] == password:
        # ❌ Weak token (just email!)
        token = email
        return {"token": token}
    return {"error": "Invalid credentials"}

@app.get("/users/{user_id}")
def get_user(user_id: str, token: str):
    # ❌ No authorization check!
    # Anyone can get anyone's data
    return users_db.get(user_id)

@app.get("/search")
def search_users(query: str):
    # ❌ SQL injection vulnerable!
    sql = f"SELECT * FROM users WHERE name LIKE '%{query}%'"
    return db.execute(sql).fetchall()
```

### Tasks

**Task 1: Security Audit (45 min)**

Prompt para Security Agent:
```
Complete security audit de este código de autenticación:

[Pega código vulnerable]

Identifica TODAS las vulnerabilidades:
1. Authentication/Authorization issues
2. Cryptographic issues
3. Injection attacks
4. Information leakage
5. Missing security headers
6. Any other security issues

For each:
- Severity (Critical, High, Medium, Low)
- Exploit scenario
- Fix recommendation with code
```

**Task 2: Fix All Issues (1.5-2 hours)**

Work through each vulnerability:

1. **Plaintext passwords** → bcrypt hashing
2. **Weak tokens** → JWT with secrets
3. **Timing attacks** → constant-time comparison
4. **No authorization** → token validation + role-based access
5. **SQL injection** → parameterized queries / ORM
6. **Missing rate limiting** → SlowAPI middleware
7. **No CORS config** → Proper CORS setup
8. **Missing security headers** → Add headers middleware

**Task 3: Write Security Tests (1 hour)**

```python
# tests/test_security.py

def test_passwords_are_hashed():
    """Passwords must be hashed, not stored plaintext."""
    register_user("test@example.com", "SecurePass123!")

    user = db.query(User).filter_by(email="test@example.com").first()
    assert user.password_hash != "SecurePass123!"
    assert user.password_hash.startswith("$2b$")  # bcrypt hash

def test_cannot_access_other_users_data():
    """Users should not access other users' data."""
    user1_token = login_as("user1@example.com")
    user2_id = get_user_id("user2@example.com")

    response = client.get(
        f"/users/{user2_id}",
        headers={"Authorization": f"Bearer {user1_token}"}
    )

    assert response.status_code == 403  # Forbidden

def test_sql_injection_prevented():
    """SQL injection should be prevented."""
    malicious_query = "'; DROP TABLE users; --"

    response = client.get(f"/search?query={malicious_query}")

    # Should not crash, should escape properly
    assert response.status_code == 200
    # Users table should still exist
    assert db.query(User).count() > 0
```

**Task 4: Document Fixes (30 min)**

Create security report:

```markdown
# Security Audit Report

## Vulnerabilities Found: 7

### Critical (3)

1. **Plaintext Password Storage**
   - Severity: Critical
   - Impact: All passwords compromised if DB leaked
   - Fix: bcrypt with 12 salt rounds
   - Status: ✅ Fixed

2. **SQL Injection in Search**
   - Severity: Critical
   - Impact: Attacker can drop tables, steal data
   - Fix: Used SQLAlchemy ORM (parameterized)
   - Status: ✅ Fixed

[... resto de vulnerabilities]

## Summary

- Vulnerabilities Fixed: 7/7
- Security Tests Added: 12
- Code Review: Security Agent approved
```

### Success Criteria

- [ ] All 7+ vulnerabilities identified
- [ ] All vulnerabilities fixed
- [ ] Security tests written (≥12 tests)
- [ ] Security Agent audit pasa (0 Critical/High issues)
- [ ] Security report documentado

---

## 🎯 Progression Path

Recomendamos hacer ejercicios en orden:

```
Ejercicio 1 (Básico)
  ↓ Aprendes: Workflow básico, 3 agentes
Ejercicio 2 (Intermedio)
  ↓ Aprendes: Review chains, refactoring
Ejercicio 3 (Avanzado)
  ↓ Aprendes: Feature completo E2E, 7 agentes
Ejercicio 4 (Performance)
  ↓ Aprendes: Profiling, optimization
Ejercicio 5 (Security)
  ↓ Aprendes: Security audit, vulnerability fixing
    ↓
Proyecto Final (Master Level)
  → Combina TODO lo aprendido
```

## 📚 Recursos

- [Agent Team Canvas Template](./ejemplos/AGENT_CANVAS_TEMPLATE.md)
- [Claude Code Best Practices](./docs/CLAUDE_CODE_BEST_PRACTICES.md)
- [Educational Agents](../../.claude/agents/educational/)

---

**¡A practicar! 🚀 Cada ejercicio te acerca más al "desarrollador con ejército de agentes".**
