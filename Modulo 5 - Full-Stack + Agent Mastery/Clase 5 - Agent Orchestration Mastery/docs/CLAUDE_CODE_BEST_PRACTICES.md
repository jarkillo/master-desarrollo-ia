# Claude Code Best Practices

Esta guía documenta las mejores prácticas para usar **Claude Code** en proyectos reales, basado en el artículo oficial de Anthropic: [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices).

## 📋 Tabla de Contenidos

1. [Effective Prompting](#effective-prompting)
2. [Context Management](#context-management)
3. [Code Review Patterns](#code-review-patterns)
4. [Iterative Development](#iterative-development)
5. [Testing Strategies](#testing-strategies)
6. [Error Handling](#error-handling)
7. [Performance Optimization](#performance-optimization)
8. [Security Considerations](#security-considerations)

---

## Effective Prompting

### Principio: Ser Específico y Contextual

Claude Code genera mejor código cuando entiendes **exactamente** qué necesitas.

#### ❌ Prompt Vago

```
Create a user system
```

**Problemas**:
- ¿Qué es un "user system"? (Auth, perfil, roles?)
- ¿Qué tech stack?
- ¿Qué features específicas?
- ¿Qué estándares de código seguir?

**Resultado**: Código genérico que probablemente necesita reescritura.

#### ✅ Prompt Específico y Contextual

```
Create a JWT-based authentication system for FastAPI.

CONTEXT:
- Existing codebase: FastAPI 0.118.0 + SQLAlchemy 2.0 + PostgreSQL
- User model already exists in api/models/user.py with fields: id, email, password_hash, role
- JWT_SECRET is in environment variable
- We use bcrypt for password hashing (12 salt rounds)
- Existing code style: type hints, Pydantic validation, dependency injection

REQUIREMENTS:
1. POST /auth/register endpoint
   - Input: email (valid format, max 255 chars), password (min 12 chars)
   - Output: 201 Created + {user_id, email, role}
   - Validation: email unique, password strength (uppercase, lowercase, digit)
   - Errors: 409 if email exists, 422 for validation errors

2. POST /auth/login endpoint
   - Input: email, password
   - Output: 200 OK + {access_token, token_type: "bearer"}
   - Validation: credentials correct
   - Errors: 401 for invalid credentials

3. GET /auth/me endpoint (protected)
   - Requires: Authorization header with Bearer token
   - Output: 200 OK + {id, email, role}
   - Errors: 401 if no token or invalid, 403 if token expired

4. Dependency: get_current_user(token) → User
   - Validates JWT
   - Returns User from DB
   - Raises HTTPException if invalid

CONSTRAINTS:
- No hardcoded secrets
- Follow existing project structure (api/auth/ directory)
- Use existing dependencies.py pattern for DI
- Write unit tests with pytest (target: 85%+ coverage)
- Follow PEP 8 and existing code style

SUCCESS CRITERIA:
- All endpoints work as specified
- Tests pass with >85% coverage
- No security vulnerabilities (SQL injection, timing attacks)
- Type hints on all functions
- Proper error messages (helpful for frontend)
```

### Estructura de un Buen Prompt

**Template**:

```
[ACCIÓN: Qué quieres que haga Claude]

CONTEXT:
- [Tech stack con versiones]
- [Código existente relevante]
- [Patrones/convenciones del proyecto]
- [Environment setup]

REQUIREMENTS:
1. [Requirement específico con detalles]
2. [Requirement específico con detalles]
...

CONSTRAINTS:
- [Limitaciones técnicas]
- [Estándares de código]
- [Performance requirements]
- [Security requirements]

SUCCESS CRITERIA:
- [Cómo saber que está completo]
- [Métricas de calidad]
```

### Ejemplos de Prompts Efectivos

#### Ejemplo 1: Database Model

```
Create SQLAlchemy model for Product in e-commerce app.

CONTEXT:
- SQLAlchemy 2.0 with async engine
- PostgreSQL 15
- Existing Base in api/database.py
- Using UUIDs for primary keys (uuid.uuid4)
- Alembic for migrations

REQUIREMENTS:
- Fields:
  * id: UUID primary key
  * name: String(255), not null, indexed
  * description: Text, nullable
  * price: Numeric(10,2), not null, check constraint (price > 0)
  * stock: Integer, not null, default 0, check constraint (stock >= 0)
  * category_id: UUID, foreign key to categories.id
  * image_url: String(512), nullable
  * created_at, updated_at: DateTime with auto-timestamps
- Relationships:
  * Many-to-one with Category
  * One-to-many with OrderItems
- Indexes:
  * (name, category_id) compound index for filtering
- Validation:
  * Prices must be positive
  * Stock can't be negative

CONSTRAINTS:
- Use declarative base
- Add __repr__ for debugging
- Include type hints
- Generate Alembic migration

SUCCESS CRITERIA:
- Model can be imported without errors
- Constraints enforced at DB level
- Alembic migration runs successfully
- Can create/query products with relationships
```

#### Ejemplo 2: React Component

```
Create ProductCard component for e-commerce frontend.

CONTEXT:
- React 18 + TypeScript 5
- TailwindCSS for styling
- Existing types in src/types/product.ts
- Using React Query for data fetching
- Component library: Headless UI

REQUIREMENTS:
- Props:
  * product: Product type (id, name, price, imageUrl, stock)
  * onAddToCart: (productId: string) => Promise<void>
- UI:
  * Product image (fallback if missing)
  * Product name (truncate after 2 lines)
  * Price (formatted as currency: $10.99)
  * Stock indicator (green if >10, yellow if 1-10, red if 0)
  * "Add to Cart" button (disabled if out of stock)
- Interactions:
  * Hover effect on card
  * Loading state while adding to cart
  * Success feedback (brief animation)
  * Error handling (toast notification)
- Accessibility:
  * Alt text for images
  * Aria labels for buttons
  * Keyboard navigation support

CONSTRAINTS:
- Mobile-first responsive design
- Follow existing Tailwind config
- Use existing toast utility (src/utils/toast.ts)
- TypeScript strict mode
- No external image libraries

SUCCESS CRITERIA:
- Component renders without TypeScript errors
- Responsive on mobile/tablet/desktop
- Accessible (WCAG AA)
- Loading and error states work
- Can add product to cart successfully
```

---

## Context Management

### Problema: Context Window Limits

Claude Code tiene un límite de contexto. Proyectos grandes pueden excederlo.

**Límite**: ~200k tokens input (varía según plan)

**Cálculo aproximado**:
- 1 línea de código Python ≈ 15-20 tokens
- Archivo mediano (200 líneas) ≈ 3000-4000 tokens
- Proyecto grande (50 archivos) ≈ 150k-200k tokens

**Problema**: Si intentas "leer todo el proyecto" de una vez, excedes el límite.

### Solución 1: Context Fragmentation

**Divide el proyecto en contextos manejables:**

#### Por Feature
```
Session 1: Authentication Feature
├── Lee: api/auth/*.py, tests/test_auth.py
└── Ignora: api/products/*, api/cart/*, frontend/*

Session 2: Products Feature
├── Lee: api/products/*.py, tests/test_products.py
└── Ignora: api/auth/*, api/cart/*, frontend/*
```

**Ventaja**: Contexto enfocado → mejor código generado

#### Por Layer
```
Session 1: Backend Only
├── Lee: api/**, tests/**, alembic/**
└── Ignora: frontend/**

Session 2: Frontend Only
├── Lee: frontend/src/**
└── Ignora: api/**, tests/**
```

**Ventaja**: No mezclas backend y frontend concerns

### Solución 2: Progressive Context Loading

En vez de "leer todo", carga contexto progresivamente:

```
Step 1: Lee solo la estructura (ls -R)
Step 2: Identifica archivos relevantes para la tarea
Step 3: Lee solo esos archivos específicos
Step 4: Genera código
Step 5: Si necesitas más contexto, lee archivos adicionales
```

**Comando útil**:
```bash
# Ver solo estructura de directorios
ls -R api/ | grep -E "\.py$" | head -20

# Leer solo archivos relevantes
cat api/auth/service.py api/models/user.py
```

### Solución 3: Context Summarization

Para proyectos muy grandes, resume contexto crítico:

```
Prompt:
Resume la arquitectura del proyecto en 500 palabras o menos:

[Pega output de ls -R]

Include:
- Tech stack principal
- Estructura de directorios clave
- Patrones arquitectónicos (Clean Architecture, MVC, etc)
- Convenciones de código (naming, testing, etc)
- Decisiones técnicas importantes
```

**Usa el resumen** en prompts subsecuentes en vez de pegar todo el código.

### Best Practice: Session Planning

**Antes de iniciar sesión**:

1. **Define el objetivo**: ¿Qué feature/bug vas a trabajar?
2. **Identifica archivos relevantes**: ¿Qué código necesitas leer?
3. **Carga contexto mínimo**: Solo lo necesario para la tarea
4. **Trabaja enfocado**: Completa la tarea
5. **Next session**: Repite para siguiente feature

**Ejemplo de plan de sesión**:
```
Session Goal: Implement password reset flow

Files to Read:
- api/auth/service.py (existing auth logic)
- api/models/user.py (User model)
- api/dependencies.py (DI patterns)

Context Needed:
- How JWT tokens are generated (line 45-60 of service.py)
- Email sending utility (if exists)
- Environment variables pattern

Tasks:
1. Create PasswordResetToken model
2. POST /auth/forgot-password endpoint (send email)
3. POST /auth/reset-password endpoint (with token)
4. Write unit tests

Estimated Context: ~15k tokens (safe)
```

---

## Code Review Patterns

### Pattern 1: Layered Review

**Concepto**: Revisar código en múltiples capas, cada una con foco específico.

```
Code → Layer 1 (Syntax) → Layer 2 (Design) → Layer 3 (Security) → Production
```

#### Layer 1: Syntax & Style

**Qué revisar**:
- Type hints presentes
- Docstrings en funciones públicas
- PEP 8 compliance
- Naming conventions
- Code formatting

**Agente sugerido**: Python Best Practices Agent

**Prompt**:
```
Review this code for Python best practices:

[Pega código]

Check:
- Type hints on all functions
- Docstrings (Google style)
- PEP 8 compliance
- Pythonic patterns (list comprehensions, f-strings, etc)
- No anti-patterns (mutable defaults, etc)

Provide specific line-by-line feedback.
```

#### Layer 2: Design & Architecture

**Qué revisar**:
- API design (RESTful, status codes correctos)
- Separation of concerns
- Dependency injection
- Error handling patterns
- Pydantic validation

**Agente sugerido**: FastAPI Design Agent

**Prompt**:
```
Review this FastAPI endpoint for API design:

[Pega código]

Check:
- Correct HTTP methods and status codes
- Pydantic models well-defined
- Dependency injection used appropriately
- Response models consistent
- Error handling (HTTPException with detail)
- OpenAPI documentation clear

Suggest improvements.
```

#### Layer 3: Security

**Qué revisar**:
- SQL injection prevention
- Password hashing
- JWT token handling
- Secrets management
- Input validation
- Rate limiting

**Agente sugerido**: Security Agent

**Prompt**:
```
Security audit of this authentication code:

[Pega código]

Look for:
- SQL injection vulnerabilities
- Weak password hashing (bcrypt with <10 rounds)
- Hardcoded secrets
- Timing attacks
- Missing input validation
- No rate limiting on sensitive endpoints
- Insecure JWT configuration

Provide severity ratings (Critical, High, Medium, Low).
```

### Pattern 2: Pair Review

**Concepto**: Dos agentes revisan simultáneamente, cada uno con expertise diferente.

```
Prompt:
I need TWO reviews of this code:

1. Python Best Practices Agent:
   - Review for Pythonic code, type hints, docstrings, PEP 8

2. FastAPI Design Agent:
   - Review for API design, status codes, Pydantic validation

[Pega código]

Provide two separate review sections.
```

**Ventaja**: Coverage más completo en una sesión.

### Pattern 3: Incremental Review

**Concepto**: Revisar después de cada cambio pequeño, no al final.

```
❌ Mal (batch review):
Day 1-5: Escribes 1000 líneas de código
Day 6: Pides review → Encuentran 50 issues → Re-trabajo masivo

✅ Bien (incremental review):
Day 1: Implementas endpoint de register → Review → Fix issues
Day 2: Implementas endpoint de login → Review → Fix issues
Day 3: Implementas endpoint de me → Review → Fix issues
```

**Ventaja**: Menos re-trabajo, aprendes más rápido.

### Pattern 4: Checklist-Driven Review

**Concepto**: Usa checklists para review consistente.

**Backend Checklist**:
```markdown
- [ ] Type hints en todas las funciones públicas
- [ ] Docstrings en funciones públicas (Google style)
- [ ] Pydantic validation para todos los inputs
- [ ] Status codes correctos (201 Created, 404 Not Found, etc)
- [ ] Error handling robusto (custom exceptions)
- [ ] No secrets hardcodeados (usar env vars)
- [ ] SQL queries optimizadas (no N+1 problems)
- [ ] Tests con ≥80% coverage
- [ ] Logging apropiado (INFO level en producción)
- [ ] Security: password hashing, input sanitization
```

**Prompt**:
```
Review this code against the following checklist:

[Pega checklist]

Code:
[Pega código]

For each item, indicate:
- ✅ Pass
- ⚠️ Warning (works but could be better)
- ❌ Fail (must fix)

Provide specific feedback for warnings and failures.
```

---

## Iterative Development

### Cycle: Red → Green → Refactor → Review

**Inspirado en TDD**, pero con agentes de IA:

```
1. RED: Write failing tests
   ├── Tú: Describes behavior esperado
   ├── Agent: Escribe tests que fallan
   └── Verify: pytest muestra red

2. GREEN: Implement minimum code to pass
   ├── Agent: Implementa código simple
   └── Verify: pytest muestra green

3. REFACTOR: Improve code quality
   ├── Agent: Limpia código, optimiza
   └── Verify: tests aún pasan (green)

4. REVIEW: Quality gates
   ├── Agent(s): Review código
   ├── Tú: Apruebas o pides cambios
   └── Commit: git commit con mensaje descriptivo
```

### Ejemplo Completo: Implementar Product Search

#### Step 1: RED (Tests Primero)

**Prompt**:
```
Write pytest tests for product search functionality (TDD).

Requirements:
- Function: search_products(query: str, category: str | None, max_price: float | None) → List[Product]
- Behavior:
  * If query matches product name (case-insensitive), return it
  * If category specified, filter by category
  * If max_price specified, filter by price <= max_price
  * Return empty list if no matches
  * Raise ValueError if query is empty string

Write comprehensive tests covering:
- Happy path (finds products)
- Edge cases (empty results, None filters)
- Error cases (empty query)
- Combinations (query + category + max_price)

Tests should FAIL now (function doesn't exist yet).
```

**Output**:
```python
# tests/test_product_search.py
import pytest
from api.products.service import search_products

def test_search_products_by_name():
    """Search finds products matching name."""
    results = search_products(query="laptop")
    assert len(results) > 0
    assert all("laptop" in p.name.lower() for p in results)

def test_search_products_by_category():
    """Search filters by category."""
    results = search_products(query="", category="electronics")
    assert all(p.category == "electronics" for p in results)

def test_search_products_with_max_price():
    """Search filters by max price."""
    results = search_products(query="", max_price=100.0)
    assert all(p.price <= 100.0 for p in results)

def test_search_products_empty_query_raises_error():
    """Empty query raises ValueError."""
    with pytest.raises(ValueError, match="Query cannot be empty"):
        search_products(query="")

# ... más tests
```

**Run tests**: `pytest tests/test_product_search.py -v`
**Expected**: 🔴 All tests FAIL (function doesn't exist)

#### Step 2: GREEN (Implementación Mínima)

**Prompt**:
```
Implement search_products function to make these tests pass:

[Pega tests]

Implement MINIMUM code necesario. No optimización aún.

Context:
- SQLAlchemy 2.0 with Product model (api/models/product.py)
- Fields: id, name, description, price, stock, category
- Database session available via get_db() dependency
```

**Output**:
```python
# api/products/service.py
from sqlalchemy.orm import Session
from api.models.product import Product

def search_products(
    query: str,
    category: str | None = None,
    max_price: float | None = None,
    db: Session = None
) -> list[Product]:
    """Search products by name, category, and price."""
    if query == "":
        raise ValueError("Query cannot be empty")

    # Start with base query
    db_query = db.query(Product)

    # Filter by name (case-insensitive)
    if query:
        db_query = db_query.filter(Product.name.ilike(f"%{query}%"))

    # Filter by category
    if category:
        db_query = db_query.filter(Product.category == category)

    # Filter by max price
    if max_price:
        db_query = db_query.filter(Product.price <= max_price)

    return db_query.all()
```

**Run tests**: `pytest tests/test_product_search.py -v`
**Expected**: ✅ All tests PASS

#### Step 3: REFACTOR (Mejorar Código)

**Prompt**:
```
Refactor search_products for better code quality:

[Pega código actual]

Improvements:
- Add type hints
- Add docstring (Google style)
- Extract magic strings to constants
- Add logging
- Optimize query (use indexes)
- Consider using full-text search for better performance

Ensure tests still pass after refactoring.
```

**Output**:
```python
# api/products/service.py
import logging
from sqlalchemy.orm import Session
from sqlalchemy import or_
from api.models.product import Product

logger = logging.getLogger(__name__)

# Constants
MIN_QUERY_LENGTH = 1
MAX_RESULTS = 100

def search_products(
    query: str,
    category: str | None = None,
    max_price: float | None = None,
    db: Session = None
) -> list[Product]:
    """
    Search products by name, category, and price.

    Args:
        query: Search term for product name (case-insensitive)
        category: Optional category filter
        max_price: Optional maximum price filter
        db: Database session

    Returns:
        List of matching Product objects (max 100 results)

    Raises:
        ValueError: If query is empty string

    Example:
        >>> search_products("laptop", category="electronics", max_price=500.0)
        [Product(name="Gaming Laptop", price=499.99), ...]
    """
    if query == "":
        raise ValueError("Query cannot be empty")

    logger.info(f"Searching products: query={query}, category={category}, max_price={max_price}")

    # Base query with index hint
    db_query = db.query(Product)

    # Full-text search on name and description
    if query:
        search_pattern = f"%{query}%"
        db_query = db_query.filter(
            or_(
                Product.name.ilike(search_pattern),
                Product.description.ilike(search_pattern)
            )
        )

    # Apply filters
    if category:
        db_query = db_query.filter(Product.category == category)

    if max_price:
        db_query = db_query.filter(Product.price <= max_price)

    # Limit results and execute
    results = db_query.limit(MAX_RESULTS).all()

    logger.info(f"Found {len(results)} products")
    return results
```

**Run tests**: `pytest tests/test_product_search.py -v`
**Expected**: ✅ All tests STILL PASS

#### Step 4: REVIEW (Quality Gate)

**Prompt 1** (Python Best Practices):
```
Review this refactored code for Python best practices:

[Pega código refactorizado]

Check:
- Type hints complete
- Docstring follows Google style
- Pythonic code
- Logging appropriate
- Constants used correctly
```

**Prompt 2** (Performance):
```
Performance review of search function:

[Pega código]

Check:
- N+1 query problems
- Missing indexes
- Inefficient filters
- Unnecessary database calls

Suggest optimizations if needed.
```

**Tú revisas outputs** → Apruebas o pides ajustes → Commit

```bash
git add api/products/service.py tests/test_product_search.py
git commit -m "feat(products): implement product search with filters

- Search by name/description (case-insensitive)
- Filter by category and max_price
- Full-text search capability
- Tests: 95% coverage
- Reviewed by: Python BP Agent + Performance Agent"
```

---

## Testing Strategies

### Strategy 1: Test-Driven Development (TDD)

**Siempre escribe tests ANTES de implementar.**

**Beneficios**:
- Clarifica requirements
- Previene over-engineering
- Garantiza test coverage
- Facilita refactoring

**Prompt Template**:
```
Write pytest tests for [FEATURE] following TDD:

Requirements:
[Lista de requirements específicos]

Test cases to cover:
1. Happy path
2. Edge cases
3. Error cases
4. Boundary conditions

Tests should be:
- Descriptive names (test_should_do_X_when_Y)
- Arrange-Act-Assert pattern
- Independent (can run in any order)
- Fast (<100ms each)

DO NOT implement the function yet, only tests.
```

### Strategy 2: Pyramid Testing

**Balance de tests por nivel:**

```
        /\
       /  \   E2E (10%)
      /    \
     /------\  Integration (20%)
    /        \
   /----------\ Unit (70%)
```

**Unit Tests (70%)**:
- Funciones puras
- Service layer
- Utility functions
- Veloces (<1s total)
- Sin dependencias externas (mock DB, API calls)

**Integration Tests (20%)**:
- API endpoints con database real (test DB)
- File I/O
- External service mocks
- Más lentos (5-10s total)

**E2E Tests (10%)**:
- User flows completos
- Frontend + Backend + Database
- Browser automation (Playwright)
- Los más lentos (30-60s)

**Regla**: Si un bug se puede detectar con unit test, NO escribas E2E test.

### Strategy 3: Contract Testing

**Para sistemas con múltiples componentes (backend + frontend):**

**Problema**: Backend cambia API → Frontend se rompe

**Solución**: Define API contract explícitamente

```typescript
// frontend/src/types/api-contracts.ts
/**
 * API Contract: POST /auth/login
 * Backend MUST return this exact shape.
 */
export interface LoginResponse {
  access_token: string;
  token_type: "bearer";
  expires_in: number;
}

// Contract test (backend)
def test_login_response_contract():
    """Ensure /auth/login matches frontend contract."""
    response = client.post("/auth/login", json={"email": "...", "password": "..."})
    data = response.json()

    # Contract assertions
    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert data["token_type"] == "bearer"
    assert "expires_in" in data
    assert isinstance(data["expires_in"], int)
```

**Ventaja**: Si backend rompe contrato, test falla inmediatamente.

### Strategy 4: Property-Based Testing

**Para funciones con muchos edge cases:**

**Problema**: Es imposible testear todos los inputs manualmente.

**Solución**: Usa `hypothesis` para generar inputs aleatorios.

```python
from hypothesis import given, strategies as st

@given(st.text(min_size=1), st.floats(min_value=0, allow_nan=False))
def test_calculate_discount_never_negative(price, discount_rate):
    """Discount calculation should never return negative price."""
    result = calculate_discount(price, discount_rate)
    assert result >= 0

# Hypothesis generará cientos de combinaciones de price y discount_rate
# y verificará que la propiedad "result >= 0" siempre se cumpla
```

**Cuándo usar**:
- Funciones matemáticas
- Parsers
- Validadores
- Algoritmos complejos

---

## Error Handling

### Principle: Fail Fast, Fail Clearly

**Mal**:
```python
def create_order(user_id, items):
    try:
        # ... lógica compleja
        return order
    except Exception:
        return None  # ❌ Silencia TODOS los errores
```

**Bien**:
```python
class InsufficientStockError(Exception):
    """Raised when product stock is insufficient for order."""
    pass

class InvalidPaymentError(Exception):
    """Raised when payment processing fails."""
    pass

def create_order(user_id: str, items: list[OrderItem]) -> Order:
    """
    Create order for user.

    Raises:
        InsufficientStockError: If any item out of stock
        InvalidPaymentError: If payment fails
        ValueError: If items list is empty
    """
    if not items:
        raise ValueError("Cannot create order with no items")

    # Check stock
    for item in items:
        if item.product.stock < item.quantity:
            raise InsufficientStockError(
                f"Insufficient stock for {item.product.name}: "
                f"requested {item.quantity}, available {item.product.stock}"
            )

    # Process payment
    try:
        payment = process_payment(user_id, calculate_total(items))
    except PaymentGatewayError as e:
        raise InvalidPaymentError(f"Payment failed: {str(e)}") from e

    # Create order
    order = Order(user_id=user_id, items=items, payment_id=payment.id)
    db.add(order)
    db.commit()

    return order
```

### Custom Exceptions Hierarchy

```python
# api/exceptions.py

class APIException(Exception):
    """Base exception for all API errors."""
    pass

class ValidationError(APIException):
    """Input validation failed."""
    pass

class AuthenticationError(APIException):
    """Authentication failed (wrong credentials)."""
    pass

class AuthorizationError(APIException):
    """User not authorized for this action."""
    pass

class ResourceNotFoundError(APIException):
    """Requested resource does not exist."""
    pass

class BusinessLogicError(APIException):
    """Business rule violated."""
    pass
```

**Uso en FastAPI**:
```python
from fastapi import HTTPException, status

@app.exception_handler(ValidationError)
def validation_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc)}
    )

@app.exception_handler(AuthenticationError)
def auth_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)},
        headers={"WWW-Authenticate": "Bearer"}
    )
```

---

## Performance Optimization

### When to Optimize

**Regla de oro**: No optimices prematuramente.

```
1. Make it work (funcionalidad)
2. Make it right (código limpio, tests)
3. Make it fast (solo si es necesario)
```

**Cuándo optimizar**:
- ✅ Tienes métricas que muestran problema (response time >500ms)
- ✅ El bottleneck está identificado (profiling)
- ✅ La optimización no sacrifica legibilidad

**Cuándo NO optimizar**:
- ❌ "Creo que esto podría ser más rápido" (sin datos)
- ❌ Sacrifica legibilidad para ganar 5ms
- ❌ El código aún no funciona correctamente

### Profiling First

**Antes de optimizar, mide:**

```python
# api/profiling.py
import cProfile
import pstats
from pstats import SortKey

def profile_endpoint(func):
    """Decorator to profile function execution."""
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()

        result = func(*args, **kwargs)

        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats(SortKey.CUMULATIVE)
        stats.print_stats(10)  # Top 10 slowest functions

        return result
    return wrapper

# Usage
@profile_endpoint
def slow_function():
    # ... código
    pass
```

**Identifica bottleneck** → Optimiza solo esa parte → Mide de nuevo

### Common Optimizations

#### 1. Database Queries: N+1 Problem

**Problema**:
```python
# ❌ N+1 queries (1 + N)
def get_orders_with_items():
    orders = db.query(Order).all()  # 1 query
    for order in orders:
        print(order.items)  # N queries (uno por cada order)
    return orders
```

**Solución**:
```python
# ✅ 1 query con JOIN
def get_orders_with_items():
    orders = db.query(Order).options(joinedload(Order.items)).all()
    for order in orders:
        print(order.items)  # No query, ya cargado
    return orders
```

**Prompt para detectar**:
```
Audit this code for N+1 query problems:

[Pega código con queries]

Look for:
- Loops that access relationships (order.items, product.category)
- Multiple queries in loops
- Missing eager loading (joinedload, selectinload)

Suggest fixes with SQLAlchemy eager loading.
```

#### 2. Caching con Redis

```python
import redis
from functools import lru_cache

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_product(product_id: str) -> Product:
    """Get product with Redis caching."""
    # Try cache first
    cached = redis_client.get(f"product:{product_id}")
    if cached:
        return Product.parse_raw(cached)

    # Query database
    product = db.query(Product).filter(Product.id == product_id).first()

    # Store in cache (TTL: 5 minutes)
    redis_client.setex(
        f"product:{product_id}",
        300,
        product.json()
    )

    return product
```

#### 3. Async donde Tenga Sentido

```python
# ❌ Sync (bloqueante)
def send_notification_email(user_email: str):
    smtp.send(user_email, "Welcome!")  # Bloquea por 2-3 segundos
    return {"status": "sent"}

# ✅ Async (no bloqueante)
import asyncio

async def send_notification_email(user_email: str):
    await asyncio.to_thread(smtp.send, user_email, "Welcome!")
    return {"status": "sent"}

# En FastAPI endpoint
@app.post("/users")
async def create_user(user: UserCreate):
    db_user = create_user_in_db(user)

    # Send email asíncrono (no bloquea respuesta)
    asyncio.create_task(send_notification_email(db_user.email))

    return db_user  # Responde inmediatamente
```

---

## Security Considerations

Ver también: Security Agent en `.claude/agents/educational/`

### Checklist de Seguridad

**Authentication**:
- [ ] Passwords hasheados con bcrypt (min 12 salt rounds)
- [ ] JWT secrets en environment variables (min 256 bits)
- [ ] Token expiration configurado (típicamente 60 min)
- [ ] Rate limiting en /login y /register (5 requests/min)
- [ ] Account lockout después de N intentos fallidos

**Input Validation**:
- [ ] Pydantic validation para TODOS los inputs
- [ ] Email format validation
- [ ] String length limits (prevenir DoS)
- [ ] Sanitización de inputs (HTML, SQL)
- [ ] File upload validation (type, size, content)

**SQL Injection Prevention**:
- [ ] NUNCA usar f-strings o % formatting para queries
- [ ] Usar SQLAlchemy ORM (automático)
- [ ] Si usas raw SQL, usar parámetros bound

```python
# ❌ VULNERABLE a SQL injection
query = f"SELECT * FROM users WHERE email = '{email}'"
db.execute(query)

# ✅ SAFE (parameterized)
query = "SELECT * FROM users WHERE email = :email"
db.execute(query, {"email": email})
```

**CORS**:
- [ ] No usar `allow_origins=["*"]` en producción
- [ ] Especificar origins exactos
- [ ] `allow_credentials=True` solo si necesario

**Secrets Management**:
- [ ] NUNCA commits secrets a Git
- [ ] Usar `.env` files (en `.gitignore`)
- [ ] Production secrets en plataforma (Railway, Render)
- [ ] Rotar secrets regularmente

**Prompt para Security Audit**:
```
Perform security audit of this code:

[Pega código]

Check for:
1. SQL injection vulnerabilities
2. Weak password hashing
3. Hardcoded secrets
4. Missing input validation
5. CORS misconfigurations
6. Missing rate limiting
7. Information leakage in error messages
8. Timing attacks

Provide:
- Severity (Critical, High, Medium, Low)
- Exploit scenario
- Fix recommendation
```

---

## Recursos Adicionales

- **[Claude Code Docs](https://docs.claude.com/claude-code)**: Documentación oficial
- **[Anthropic Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)**: Artículo original
- **[Fast API Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)**: Guía de FastAPI
- **[SQLAlchemy Performance](https://docs.sqlalchemy.org/en/20/orm/queryguide/performance.html)**: Optimización de queries

---

**Siguiente**: [Agent Team Canvas Framework](./AGENT_TEAM_CANVAS.md)
