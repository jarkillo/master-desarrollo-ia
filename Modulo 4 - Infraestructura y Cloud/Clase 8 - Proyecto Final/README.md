# 🚀 Proyecto Final - Módulo 4: API de Tareas con PostgreSQL

**Módulo 4 - Infraestructura y Cloud | Clase 8**

Proyecto integrador que combina todos los conceptos del módulo: FastAPI, SQLAlchemy, Alembic, Docker, PostgreSQL, autenticación JWT, y deployment en cloud.

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Stack Tecnológico](#-stack-tecnológico)
- [Quick Start](#-quick-start)
- [Desarrollo Local](#-desarrollo-local)
- [Tests](#-tests)
- [Deployment](#-deployment)
- [API Documentation](#-api-documentation)

---

## ✨ Características

### Funcionalidades Core

- ✅ **Autenticación JWT** - Registro y login de usuarios
- ✅ **CRUD completo de tareas** - Crear, leer, actualizar, eliminar
- ✅ **Filtros avanzados** - Por completada, prioridad, búsqueda de texto
- ✅ **Paginación** - Listados con page/page_size
- ✅ **Soft delete** - Papelera de reciclaje para tareas eliminadas
- ✅ **Relaciones 1:N** - Un usuario tiene muchas tareas

### Infraestructura

- ✅ **PostgreSQL** - Base de datos relacional en producción
- ✅ **SQLite** - Base de datos para desarrollo y tests
- ✅ **Alembic** - Migraciones de schema versionadas
- ✅ **Docker** - Contenedorización para despliegue
- ✅ **docker-compose** - PostgreSQL local para desarrollo
- ✅ **Pydantic Settings** - Configuración multi-entorno (dev/staging/prod)

### Calidad y Testing

- ✅ **Tests unitarios** - Coverage 80%+
- ✅ **Tests de integración** - Repositorios con BD real
- ✅ **Linting** - Ruff para código limpio
- ✅ **Security** - Bandit para auditoría de seguridad

---

## 🏗️ Arquitectura

### Capas de la Aplicación

```
┌─────────────────────────────────────┐
│   API Layer (FastAPI)               │  ← Endpoints REST
│   - Validación con Pydantic         │
│   - Autenticación JWT               │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│   Service Layer                     │  ← Lógica de negocio
│   - ServicioUsuarios                │
│   - ServicioTareas                  │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│   Repository Layer (Protocol)       │  ← Abstracción de datos
│   - RepositorioUsuarios             │
│   - RepositorioTareas               │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│   Database Layer                    │  ← Persistencia
│   - PostgreSQL (producción)         │
│   - SQLite (desarrollo/tests)       │
└─────────────────────────────────────┘
```

### Modelos de Datos

**Usuario:**
- `id` (PK), `email` (unique), `nombre`, `password_hash`
- `activo` (soft delete), `creado_en`, `actualizado_en`

**Tarea:**
- `id` (PK), `titulo`, `descripcion`, `completada`, `prioridad` (1-3)
- `usuario_id` (FK), `eliminada` (soft delete)
- `creado_en`, `actualizado_en`

---

## 🛠️ Stack Tecnológico

**Backend:**
- FastAPI 0.118.0 (web framework)
- SQLAlchemy 2.0 (ORM)
- Alembic 1.14.0 (migrations)
- Pydantic 2.11.10 (validation)
- python-jose (JWT)
- passlib (password hashing)

**Database:**
- PostgreSQL 15+ (producción)
- SQLite (desarrollo/tests)

**Infraestructura:**
- Docker + docker-compose
- Uvicorn (ASGI server)
- Railway / Render (cloud deployment)

**Testing & Quality:**
- Pytest + pytest-cov
- httpx (API testing)
- Ruff (linting)
- Bandit (security audit)

---

## 🚀 Quick Start

### 1. Clonar y Setup

```bash
# Navegar al directorio del proyecto
cd "Modulo 4 - Infraestructura y Cloud/Clase 8 - Proyecto Final"

# Activar entorno virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Copiar template de variables de entorno
cp .env.template .env

# Editar .env y configurar JWT_SECRET
# JWT_SECRET=your-secret-key-here
```

### 2. Ejecutar con SQLite (desarrollo rápido)

```bash
# Crear migración inicial
alembic revision --autogenerate -m "Initial migration"

# Aplicar migración
alembic upgrade head

# Iniciar servidor
uvicorn api.api:app --reload
```

### 3. Acceder a la API

- **API**: http://localhost:8000
- **Documentación interactiva**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/health

---

## 💻 Desarrollo Local

### Opción 1: SQLite (más simple)

```bash
# .env
DATABASE_URL=sqlite:///./tareas.db
```

### Opción 2: PostgreSQL con Docker (recomendado)

```bash
# Iniciar PostgreSQL con docker-compose
docker-compose up -d

# .env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tareas_db

# Aplicar migraciones
alembic upgrade head

# Iniciar API
uvicorn api.api:app --reload
```

### Comandos de Alembic

```bash
# Crear migración automática (detecta cambios en modelos)
alembic revision --autogenerate -m "Descripción del cambio"

# Aplicar migraciones pendientes
alembic upgrade head

# Rollback a versión anterior
alembic downgrade -1

# Ver historial de migraciones
alembic history

# Ver estado actual
alembic current
```

---

## 🧪 Tests

### Ejecutar todos los tests

```bash
pytest
```

### Tests con coverage

```bash
pytest --cov=api --cov-report=term-missing --cov-fail-under=80
```

### Tests específicos

```bash
# Solo tests de autenticación
pytest tests/test_auth.py -v

# Solo tests de CRUD de tareas
pytest tests/test_tareas_crud.py -v

# Tests de integración
pytest tests_integrations/ -v
```

### Estructura de Tests

```
tests/
├── conftest.py              # Fixtures compartidos
├── test_auth.py             # Tests de autenticación
├── test_tareas_crud.py      # Tests de CRUD de tareas
└── test_health.py           # Tests de health check

tests_integrations/
├── test_repositorio_usuarios.py
└── test_repositorio_tareas.py
```

---

## 🐳 Deployment

### Build de Docker

```bash
# Build de imagen
docker build -t api-tareas:latest .

# Ejecutar contenedor
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://..." \
  -e JWT_SECRET="..." \
  -e ENVIRONMENT="prod" \
  api-tareas:latest
```

### Railway

1. Crear proyecto en Railway
2. Agregar PostgreSQL addon
3. Configurar variables de entorno:
   - `DATABASE_URL` (automático desde PostgreSQL)
   - `JWT_SECRET` (generar secreto seguro)
   - `ENVIRONMENT=prod`
4. Deploy automático desde Git o con Railway CLI:

```bash
railway up
```

Ver `railway.toml` para configuración.

### Render

1. Crear nuevo Web Service desde GitHub
2. Agregar PostgreSQL database
3. Configurar variables de entorno (ver `render.yaml`)
4. Deploy automático

Ver `render.yaml` para blueprint completo.

### Migraciones en Producción

```bash
# Railway/Render ejecutan esto automáticamente en startup:
alembic upgrade head && uvicorn api.api:app --host 0.0.0.0 --port $PORT
```

---

## 📚 API Documentation

### Autenticación

#### `POST /auth/register`
Registra un nuevo usuario.

**Request:**
```json
{
  "email": "user@example.com",
  "nombre": "Usuario Ejemplo",
  "password": "password123"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "email": "user@example.com",
  "nombre": "Usuario Ejemplo",
  "activo": true,
  "creado_en": "2025-01-01T00:00:00Z",
  "actualizado_en": "2025-01-01T00:00:00Z"
}
```

#### `POST /auth/login`
Autentica un usuario y devuelve JWT token.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

#### `GET /auth/me`
Obtiene información del usuario autenticado.

**Headers:** `Authorization: Bearer {token}`

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "nombre": "Usuario Ejemplo",
  "activo": true,
  "creado_en": "2025-01-01T00:00:00Z",
  "actualizado_en": "2025-01-01T00:00:00Z"
}
```

### Tareas

#### `POST /tareas`
Crea una nueva tarea.

**Headers:** `Authorization: Bearer {token}`

**Request:**
```json
{
  "titulo": "Comprar leche",
  "descripcion": "En el supermercado",
  "prioridad": 2,
  "completada": false
}
```

**Response:** `201 Created`

#### `GET /tareas`
Lista tareas con filtros y paginación.

**Headers:** `Authorization: Bearer {token}`

**Query params:**
- `page` (int): Número de página (default: 1)
- `page_size` (int): Tamaño de página (default: 10)
- `completada` (bool): Filtrar por completada
- `prioridad` (int): Filtrar por prioridad (1-3)
- `q` (string): Buscar en título

**Ejemplos:**
```bash
GET /tareas?page=1&page_size=10
GET /tareas?completada=true
GET /tareas?prioridad=3
GET /tareas?q=comprar
```

**Response:** `200 OK`
```json
{
  "items": [...],
  "total": 25,
  "page": 1,
  "page_size": 10,
  "total_pages": 3
}
```

#### `GET /tareas/{id}`
Obtiene una tarea por ID.

**Response:** `200 OK` o `404 Not Found`

#### `PUT /tareas/{id}`
Actualiza una tarea (PATCH semántico - solo campos enviados).

**Request:**
```json
{
  "completada": true,
  "prioridad": 1
}
```

**Response:** `200 OK`

#### `DELETE /tareas/{id}`
Elimina una tarea (soft delete).

**Response:** `204 No Content`

#### `GET /tareas/papelera/listar`
Lista tareas eliminadas.

**Response:** `200 OK` (estructura igual que listar tareas)

#### `POST /tareas/{id}/restaurar`
Restaura una tarea eliminada.

**Response:** `200 OK`

### Health Check

#### `GET /health`
Verifica el estado de la aplicación.

**Response:** `200 OK`
```json
{
  "status": "ok",
  "environment": "dev",
  "database": "connected",
  "timestamp": "2025-01-01T00:00:00Z"
}
```

---

## 📁 Estructura del Proyecto

```
Clase 8 - Proyecto Final/
├── api/
│   ├── __init__.py
│   ├── api.py                      # FastAPI app + endpoints
│   ├── models.py                   # SQLAlchemy models
│   ├── schemas.py                  # Pydantic schemas
│   ├── database.py                 # Database config
│   ├── config.py                   # Pydantic Settings
│   ├── seguridad_jwt.py            # JWT auth
│   ├── dependencias.py             # Dependency injection
│   ├── repositorio_base.py         # Repository protocols
│   ├── repositorio_usuarios.py     # User repository
│   ├── repositorio_tareas.py       # Task repository
│   ├── servicio_usuarios.py        # User service
│   └── servicio_tareas.py          # Task service
├── alembic/
│   ├── versions/                   # Migration files
│   ├── env.py                      # Alembic config
│   └── script.py.mako              # Migration template
├── tests/
│   ├── conftest.py                 # Test fixtures
│   ├── test_auth.py
│   ├── test_tareas_crud.py
│   └── test_health.py
├── tests_integrations/
│   └── test_repositorio_*.py
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API_SPEC.md
│   └── DEPLOYMENT.md
├── .env                            # Environment variables
├── .env.template                   # Template de variables
├── .gitignore
├── alembic.ini                     # Alembic configuration
├── docker-compose.yml              # PostgreSQL local
├── Dockerfile                      # Production image
├── railway.toml                    # Railway config
├── render.yaml                     # Render config
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## 🔐 Seguridad

### Buenas Prácticas Implementadas

✅ **Password hashing** con bcrypt
✅ **JWT tokens** con expiración configurable
✅ **Secrets en variables de entorno** (nunca en código)
✅ **SQL injection protection** (SQLAlchemy ORM)
✅ **CORS configurado** para entornos específicos
✅ **Container security** (usuario no-root en Docker)
✅ **Dependency scanning** (Bandit, Safety)

### Variables de Entorno Críticas

```bash
# ⚠️ NUNCA commitear estos valores reales
JWT_SECRET=<generar-secreto-seguro-256-bits>
DATABASE_URL=<url-con-credenciales>

# Generar JWT_SECRET seguro:
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 🤖 Integración con IA (40%)

Este proyecto incluye contenido educativo sobre cómo usar IA durante el desarrollo.

Ver documentación completa en:
- `docs/AI_INTEGRATION.md` - Prompts efectivos para cada fase
- `docs/AI_TROUBLESHOOTING.md` - Debugging con IA
- `.claude/agents/educational/` - Agentes especializados para review

### Ejemplos de Uso de IA

**Generación de modelos ORM:**
```
Crea un modelo SQLAlchemy 2.0 para [entidad] con:
- Type hints completos (Mapped[])
- Timestamps automáticos
- Índices optimizados
- Relaciones [tipo de relación]
```

**Optimización de queries:**
```
Esta query hace N+1. Optimízala con eager loading.
[código de la query]
```

**Generación de tests:**
```
Genera tests pytest para [funcionalidad] que cubran:
- Happy path
- Edge cases
- Error handling
```

---

## 📖 Recursos

**Documentación Oficial:**
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)

**Deployment:**
- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)

---

## 📝 Licencia

Este proyecto es parte del programa educativo "Master en Desarrollo con IA".
Uso exclusivamente educativo.

---

## 👤 Autor

Desarrollado como proyecto final del Módulo 4 - Infraestructura y Cloud.

**Conceptos aplicados:**
- Clean Architecture (SOLID principles)
- Repository Pattern
- Dependency Injection
- Test-Driven Development (TDD)
- Twelve-Factor App methodology
- DevOps practices (CI/CD, containers, cloud)

---

¿Preguntas o problemas? Consulta la documentación en `/docs` o abre un issue.
