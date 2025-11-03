# Clase 8 - Proyecto Final: Sistema de Tareas en Producción

## 🎬 El problema

Has aprendido muchísimo en este módulo:

> "Ya sé FastAPI, SQLAlchemy, Alembic, Docker y deployment..."
> "¿Pero cómo junto TODO esto en un proyecto profesional?"
> "¿Cómo lo llevo a producción de verdad?"

¿Por qué ocurre?

Porque has visto **piezas individuales**, pero falta la **orquestación completa**:
- SQLAlchemy sin autenticación real
- Docker sin configuración multi-entorno
- Deployment sin estrategia de migraciones
- Tests sin CI/CD pipeline

Para solucionar esto necesitas un **proyecto integrador** que une todos los conceptos en una aplicación de producción.

---

## 🧠 Concepto

Piensa en este proyecto final como **construir una casa completa**:

### Analogía: De habitaciones a casa completa

Imagina que en las clases anteriores aprendiste a:
- **Clase 1-2**: Cómo hacer paredes (Docker, contenedores)
- **Clase 3**: Cómo instalar tuberías (SQLAlchemy, base de datos)
- **Clase 4**: Cómo renovar tuberías sin romper nada (Alembic, migraciones)
- **Clase 5**: Cómo conectar servicios públicos (deployment en cloud)

Pero... ¿dónde está la **casa completa**?

**Este proyecto final ES la casa**:
- **Cimientos** = Modelos de datos bien diseñados
- **Estructura** = Arquitectura en capas limpia
- **Instalaciones** = Autenticación, permisos, seguridad
- **Conexiones** = API REST con validación completa
- **Mantenimiento** = CI/CD, tests automáticos
- **Servicios** = PostgreSQL, JWT, paginación
- **Inspección** = Health checks, logs, monitoreo

Y lo mejor: **lista para vivir** (deployada en producción).

---

## 📚 Fundamentos: Arquitectura del Proyecto

### ¿Qué construiremos?

Una **API de gestión de tareas profesional** con:

**Funcionalidades de negocio:**
- ✅ Registro y autenticación de usuarios (JWT)
- ✅ CRUD completo de tareas
- ✅ Relación 1:N (un usuario → muchas tareas)
- ✅ Filtros avanzados (completada, prioridad, búsqueda)
- ✅ Paginación (manejo de grandes volúmenes)
- ✅ Soft delete con papelera de reciclaje

**Infraestructura:**
- ✅ PostgreSQL en producción, SQLite en desarrollo
- ✅ Migraciones automáticas con Alembic
- ✅ Configuración multi-entorno (dev/staging/prod)
- ✅ Docker con multi-stage build
- ✅ CI/CD con GitHub Actions
- ✅ Deployment en Railway y Render

**Calidad:**
- ✅ Tests con 80%+ coverage
- ✅ Linting automático (Ruff)
- ✅ Security audit (Bandit)
- ✅ Type hints completos

### Arquitectura en Capas

```
┌───────────────────────────────────────┐
│  API Layer (FastAPI)                  │  ← Tu "recepcionista"
│  - Endpoints REST                     │    Recibe requests, valida formato
│  - Validación Pydantic                │
│  - Autenticación JWT                  │
└──────────────┬────────────────────────┘
               │
┌──────────────▼────────────────────────┐
│  Service Layer                        │  ← Tu "gerente"
│  - Lógica de negocio                  │    Toma decisiones de negocio
│  - Orquestación                       │
└──────────────┬────────────────────────┘
               │
┌──────────────▼────────────────────────┐
│  Repository Layer (Protocol)          │  ← Tu "archivista"
│  - Abstracción de persistencia        │    Sabe DÓNDE guardar (no QUÉ)
└──────────────┬────────────────────────┘
               │
┌──────────────▼────────────────────────┐
│  Database Layer                       │  ← Tu "bodega"
│  - PostgreSQL (producción)            │    Almacenamiento físico
│  - SQLite (desarrollo)                │
└───────────────────────────────────────┘
```

**Analogía: Hotel bien organizado**

| Capa | Rol en el hotel | Responsabilidad |
|------|----------------|-----------------|
| **API** | Recepcionista | Atiende clientes, valida identidad, registra solicitudes |
| **Service** | Gerente | Decide qué hacer con cada solicitud según reglas del negocio |
| **Repository** | Archivista | Busca y guarda información en el archivo |
| **Database** | Bodega | Almacena físicamente los documentos |

**¿Por qué en capas?**

1. **Separación de responsabilidades**: Cada capa hace UNA cosa
2. **Testeabilidad**: Puedes testear cada capa por separado
3. **Mantenibilidad**: Cambiar una capa no afecta las demás
4. **Escalabilidad**: Cada capa puede escalar independientemente

---

## 🛠️ Aplicación manual: Paso a paso

### Paso 1: Setup inicial del proyecto

```bash
# Navegar al directorio
cd "Modulo 4 - Infraestructura y Cloud/Clase 8 - Proyecto Final"

# Activar entorno virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

**requirements.txt explicado:**

```txt
# Web Framework
fastapi==0.118.0         # API REST moderna
uvicorn[standard]==0.37.0  # Servidor ASGI

# Database
sqlalchemy==2.0.35       # ORM para hablar con BD
alembic==1.14.0          # Migraciones de schema
psycopg2-binary==2.9.10  # Driver de PostgreSQL

# Validation
pydantic==2.11.10        # Validación de datos
pydantic-settings==2.7.1 # Config multi-entorno

# Security
python-jose[cryptography]  # JWT tokens
passlib[bcrypt]           # Password hashing

# Testing
pytest==8.4.2            # Framework de tests
pytest-cov==6.0.0        # Coverage reports
```

---

### Paso 2: Configuración multi-entorno

**api/config.py:**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./tareas.db"

    # Environment
    environment: Literal["dev", "staging", "prod"] = "dev"

    # JWT
    jwt_secret: str  # ⚠️ REQUERIDO (no tiene default)
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60

    # Carga desde .env automáticamente
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
```

**¿Por qué Pydantic Settings?**

**Sin Pydantic Settings** (el problema):
```python
# ❌ Hardcoded, no portable
DATABASE_URL = "sqlite:///./tareas.db"
JWT_SECRET = "mi-secreto-123"  # ⚠️ Secreto en código!

# ❌ Sin validación
PORT = os.getenv("PORT")  # Puede ser None, puede ser "abc"
```

**Con Pydantic Settings** (la solución):
```python
# ✅ Type-safe, validado, con defaults
settings = Settings()

# ✅ Funciona en dev (SQLite) y prod (PostgreSQL)
# Sin cambiar código, solo .env

# ✅ Error claro si falta JWT_SECRET
# ValidationError: field required (JWT_SECRET)
```

**.env (desarrollo):**
```env
DATABASE_URL=sqlite:///./tareas.db
JWT_SECRET=dev-secret-key-12345
ENVIRONMENT=dev
```

**.env (producción - Railway/Render):**
```env
DATABASE_URL=postgresql://user:pass@host:5432/db
JWT_SECRET=<generar-secreto-seguro-256-bits>
ENVIRONMENT=prod
```

---

### Paso 3: Modelos de datos con relaciones

**api/models.py:**

```python
from sqlalchemy.orm import Mapped, mapped_column, relationship

class UsuarioModel(Base):
    """Un usuario del sistema."""
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(200))
    password_hash: Mapped[str] = mapped_column(String(255))

    # Soft delete
    activo: Mapped[bool] = mapped_column(default=True)

    # Timestamps automáticos
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relación: Un usuario tiene muchas tareas
    tareas: Mapped[List["TareaModel"]] = relationship(
        back_populates="usuario",
        cascade="all, delete-orphan"
    )


class TareaModel(Base):
    """Una tarea asignada a un usuario."""
    __tablename__ = "tareas"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200))
    descripcion: Mapped[Optional[str]] = mapped_column(String(1000))
    completada: Mapped[bool] = mapped_column(default=False)
    prioridad: Mapped[int] = mapped_column(default=2)  # 1-3
    eliminada: Mapped[bool] = mapped_column(default=False)

    # Foreign Key
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE")
    )

    # Relación inversa
    usuario: Mapped["UsuarioModel"] = relationship(back_populates="tareas")

    # Índices compuestos para optimizar queries
    __table_args__ = (
        Index("idx_usuario_completada", "usuario_id", "completada"),
        Index("idx_usuario_eliminada", "usuario_id", "eliminada"),
    )
```

**Decisiones de diseño explicadas:**

1. **`cascade="all, delete-orphan"`**: Si elimino un usuario, se eliminan sus tareas
2. **`ondelete="CASCADE"`**: A nivel de BD también (doble seguridad)
3. **Índices compuestos**: Queries como "tareas completadas del usuario X" son O(log n) en lugar de O(n)
4. **Soft delete** (`eliminada`): No borrar físicamente, marcar como eliminada
5. **Timestamps automáticos**: `server_default=func.now()` lo hace la BD (no Python)

---

### Paso 4: Repository Pattern (desacoplamiento)

**¿Por qué Repository Pattern?**

**Sin Repository** (Service habla directamente con SQLAlchemy):
```python
# ❌ Service depende de SQLAlchemy
class ServicioTareas:
    def listar(self, usuario_id):
        return db.query(TareaModel).filter(...).all()
        # ⚠️ Si cambio de ORM, debo cambiar Service
        # ⚠️ No puedo testear sin BD real
```

**Con Repository** (Service habla con abstracción):
```python
# ✅ Service depende de Protocol (abstracción)
class ServicioTareas:
    def __init__(self, repositorio: RepositorioTareas):
        self._repo = repositorio

    def listar(self, usuario_id):
        return self._repo.listar(usuario_id=usuario_id)
        # ✅ Puedo cambiar de ORM sin tocar Service
        # ✅ Puedo testear con RepositorioMemoria
```

**api/repositorio_base.py (Protocol):**

```python
from typing import Protocol

class RepositorioTareas(Protocol):
    """Contrato que debe cumplir cualquier repositorio de tareas."""

    def crear(self, titulo: str, usuario_id: int, ...) -> TareaModel:
        ...

    def listar(self, usuario_id: int, ...) -> List[TareaModel]:
        ...

    def obtener_por_id(self, tarea_id: int, usuario_id: int) -> Optional[TareaModel]:
        ...
```

**api/repositorio_tareas.py (Implementación SQLAlchemy):**

```python
class RepositorioTareasDB:
    """Implementación con SQLAlchemy."""

    def __init__(self, session: Session):
        self._session = session

    def crear(self, titulo: str, usuario_id: int, ...) -> TareaModel:
        tarea = TareaModel(titulo=titulo, usuario_id=usuario_id, ...)
        self._session.add(tarea)
        self._session.commit()
        self._session.refresh(tarea)
        return tarea

    def listar(
        self,
        usuario_id: int,
        completada: Optional[bool] = None,
        prioridad: Optional[int] = None,
        limite: int = 10,
        offset: int = 0
    ) -> List[TareaModel]:
        query = self._session.query(TareaModel).filter(
            TareaModel.usuario_id == usuario_id,
            TareaModel.eliminada == False
        )

        # Filtros opcionales
        if completada is not None:
            query = query.filter(TareaModel.completada == completada)
        if prioridad is not None:
            query = query.filter(TareaModel.prioridad == prioridad)

        # Paginación y orden
        return query.order_by(
            TareaModel.prioridad.desc(),
            TareaModel.creado_en.desc()
        ).limit(limite).offset(offset).all()
```

**Beneficios:**
- ✅ Puedes crear `RepositorioMemoria` para tests
- ✅ Puedes cambiar de ORM sin romper nada
- ✅ Cada query está documentada en un método
- ✅ Facilita el testing (mock del repositorio)

---

### Paso 5: Autenticación JWT profesional

**api/seguridad_jwt.py:**

```python
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash con bcrypt (lento a propósito = seguro)."""
    return pwd_context.hash(password)

def verificar_password(password_plano: str, password_hash: str) -> bool:
    """Verifica password sin revelar el hash."""
    return pwd_context.verify(password_plano, password_hash)

def crear_access_token(email: str, user_id: int) -> str:
    """Crea JWT token con expiración."""
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expiration_minutes)
    to_encode = {"sub": email, "user_id": user_id, "exp": expire}

    return jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )

def obtener_usuario_actual(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> UsuarioModel:
    """Dependency que valida JWT y devuelve usuario."""
    token = credentials.credentials
    payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])

    email = payload.get("sub")
    usuario = db.query(UsuarioModel).filter(UsuarioModel.email == email).first()

    if not usuario or not usuario.activo:
        raise HTTPException(status_code=401, detail="No autorizado")

    return usuario
```

**Uso en endpoints:**

```python
@app.get("/tareas")
def listar_tareas(
    usuario: UsuarioModel = Depends(obtener_usuario_actual),  # ⬅ Protección JWT
    servicio: ServicioTareas = Depends(get_servicio_tareas)
):
    return servicio.listar(usuario_id=usuario.id)
```

**¿Qué hace `Depends(obtener_usuario_actual)`?**

1. Lee header `Authorization: Bearer <token>`
2. Decodifica el JWT
3. Busca usuario en BD
4. Verifica que esté activo
5. Lo inyecta en el endpoint

Si falla cualquier paso → 401 Unauthorized

---

### Paso 6: API completa con FastAPI

**Endpoints implementados:**

```python
# Autenticación
POST   /auth/register    # Crear cuenta
POST   /auth/login       # Obtener token
GET    /auth/me          # Info del usuario actual (protegido)

# Tareas
GET    /tareas                    # Listar con filtros (protegido)
GET    /tareas/{id}               # Obtener una (protegido)
POST   /tareas                    # Crear (protegido)
PUT    /tareas/{id}               # Actualizar (protegido)
DELETE /tareas/{id}               # Eliminar (protegido)
GET    /tareas/papelera/listar    # Ver eliminadas (protegido)
POST   /tareas/{id}/restaurar     # Restaurar (protegido)

# Health
GET    /health           # Health check (público)
GET    /                 # Info de la API (público)
```

**Ejemplo de endpoint completo:**

```python
@app.get("/tareas", response_model=TareaListResponse)
def listar_tareas(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    completada: Optional[bool] = Query(None),
    prioridad: Optional[int] = Query(None, ge=1, le=3),
    q: Optional[str] = Query(None, max_length=200),
    usuario: UsuarioModel = Depends(obtener_usuario_actual),
    servicio: ServicioTareas = Depends(get_servicio_tareas)
):
    """
    Lista tareas con filtros y paginación.

    Query params:
    - page: Número de página (default: 1)
    - page_size: Items por página (default: 10, max: 100)
    - completada: Filtrar por completada (true/false)
    - prioridad: Filtrar por prioridad (1=Baja, 2=Media, 3=Alta)
    - q: Buscar en título (case-insensitive)
    """
    pagination = PaginationParams(page=page, page_size=page_size)
    return servicio.listar(
        usuario_id=usuario.id,
        pagination=pagination,
        completada=completada,
        prioridad=prioridad,
        q=q
    )
```

**Validaciones automáticas de Pydantic:**
- ✅ `page >= 1`
- ✅ `page_size` entre 1 y 100
- ✅ `prioridad` entre 1 y 3
- ✅ `q` máximo 200 caracteres
- ✅ Si falta JWT → 401
- ✅ Si formato inválido → 422

---

### Paso 7: Migraciones con Alembic

**Configurar Alembic:**

```bash
# Ya está configurado, solo genera la primera migración
alembic revision --autogenerate -m "Initial migration"

# Aplica a la BD
alembic upgrade head
```

**Workflow de migraciones:**

```bash
# 1. Modificas models.py (agregar campo, tabla, etc)

# 2. Generas migración automática
alembic revision --autogenerate -m "Add priority field"

# 3. Revisas el archivo generado en alembic/versions/
# Verifica que el SQL es correcto

# 4. Aplicas migración
alembic upgrade head

# 5. Si algo sale mal, rollback
alembic downgrade -1
```

**En producción:**

```bash
# Railway/Render ejecutan esto en startup:
alembic upgrade head && uvicorn api.api:app --host 0.0.0.0 --port $PORT
```

---

### Paso 8: Docker multi-stage

**Dockerfile explicado:**

```dockerfile
# ========= STAGE 1: Builder =========
FROM python:3.12-slim as builder

# Instalar dependencias de build (gcc para psycopg2)
RUN apt-get update && apt-get install -y gcc libpq-dev

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# ========= STAGE 2: Runtime =========
FROM python:3.12-slim

# Solo librerías de runtime (no gcc)
RUN apt-get update && apt-get install -y libpq5

# Copiar dependencias desde builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copiar código
COPY ./api ./api
COPY ./alembic ./alembic
COPY alembic.ini .

# Usuario no-root (seguridad)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

**¿Por qué multi-stage?**

**Single-stage** (imagen grande):
```
Builder dependencies: 500MB (gcc, build-tools)
+ Runtime: 200MB
= 700MB de imagen final ❌
```

**Multi-stage** (imagen optimizada):
```
Stage 1 (builder): 500MB → Descartada
Stage 2 (runtime): 200MB → Esta es la final ✅
```

**Resultado:** Imagen 3x más pequeña, más rápida de descargar y desplegar.

---

### Paso 9: Testing con pytest

**tests/conftest.py (fixtures):**

```python
@pytest.fixture
def test_db():
    """BD SQLite en memoria para cada test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(bind=engine)
    db = TestingSessionLocal()

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    """Cliente de FastAPI con BD de testing."""
    app.dependency_overrides[get_db] = lambda: test_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers(usuario_test):
    """Headers con JWT válido."""
    token = crear_access_token(usuario_test.email, usuario_test.id)
    return {"Authorization": f"Bearer {token}"}
```

**Test de ejemplo:**

```python
def test_crear_tarea_exitoso(client, auth_headers):
    response = client.post(
        "/tareas",
        headers=auth_headers,
        json={
            "titulo": "Comprar leche",
            "prioridad": 2
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == "Comprar leche"
    assert data["prioridad"] == 2
    assert "id" in data
```

**Ejecutar tests:**

```bash
# Todos los tests
pytest

# Con coverage
pytest --cov=api --cov-report=term-missing --cov-fail-under=80

# Solo auth
pytest tests/test_auth.py -v
```

---

### Paso 10: CI/CD con GitHub Actions

**`.github/workflows/ci.yml`:**

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - run: pip install -r requirements.txt

      - name: Run tests
        run: pytest --cov=api --cov-fail-under=80

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install ruff
      - run: ruff check api/

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install bandit
      - run: bandit -r api/ -ll
```

**Se ejecuta automáticamente en:**
- ✅ Push a `main`, `dev`
- ✅ Pull Requests

**Si falla CI:**
- ❌ No se puede hacer merge
- ❌ Debes arreglar antes de continuar

---

### Paso 11: Deployment en Railway

**Configuración en Railway:**

1. Conectar repo de GitHub
2. Agregar PostgreSQL addon (automático)
3. Configurar variables:
   - `JWT_SECRET` (generar seguro)
   - `ENVIRONMENT=prod`
   - `DATABASE_URL` (automático desde PostgreSQL)

4. Deploy automático en cada push a `main`

**railway.toml:**

```toml
[build]
builder = "DOCKERFILE"

[deploy]
startCommand = "alembic upgrade head && uvicorn api.api:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
restartPolicyType = "ON_FAILURE"
```

**Verifica deployment:**

```bash
# Desde tu terminal
curl https://tu-app.railway.app/health

# O visita
https://tu-app.railway.app/docs
```

---

## 🤖 Aplicación con IA (40% del contenido)

### Prompt para diseñar modelos ORM

```
Rol: Database architect especializado en SQLAlchemy 2.0.

Contexto: Estoy diseñando una API de gestión de tareas con:
- Usuarios autenticados (email, password)
- Tareas asignadas a usuarios (1:N)
- Soft delete (no borrar físicamente)
- Necesito optimizar queries frecuentes

Objetivo: Diseña los modelos ORM con:
- SQLAlchemy 2.0 syntax (Mapped[], mapped_column)
- Type hints completos
- Relaciones bidireccionales
- Timestamps automáticos
- Índices compuestos para queries frecuentes:
  * "Tareas completadas del usuario X"
  * "Tareas no eliminadas del usuario X"
  * "Buscar tareas por prioridad"

Restricciones:
- Compatible con PostgreSQL y SQLite
- Seguir convenciones de naming (snake_case)
- Cascade rules correctas

Entrega:
- Código de los modelos
- Explicación de cada índice (por qué mejora performance)
- Queries SQL resultantes
```

**Qué genera la IA:**
- ✅ Modelos completos con type hints
- ✅ Índices compuestos optimizados
- ✅ Explicación de decisiones de diseño

**Qué DEBES validar tú:**
- ⚠️ Los índices realmente mejoran TUS queries (no todas)
- ⚠️ Los cascades no borran datos importantes
- ⚠️ Los tipos de columnas (String(100) vs Text)

---

### Prompt para implementar paginación

```
Rol: Backend developer especializado en APIs REST.

Contexto: Tengo este endpoint que devuelve TODAS las tareas:

[pegar código del endpoint sin paginación]

Problema: Si un usuario tiene 10,000 tareas, la API se cuelga.

Objetivo: Implementa paginación con:
- Query params: ?page=1&page_size=10
- Validación: page >= 1, page_size entre 1 y 100
- Response con metadata:
  {
    "items": [...],
    "total": 1000,
    "page": 1,
    "page_size": 10,
    "total_pages": 100
  }
- Mantener filtros existentes (completada, prioridad)

Restricciones:
- Usar SQLAlchemy .limit() y .offset()
- No romper tests existentes
- Defaults razonables (page=1, page_size=10)

Entrega:
- Código del endpoint actualizado
- Schema de Pydantic para la response
- Ejemplo de uso con curl
```

---

### Prompt para debugging de deployment

```
Tengo este error al desplegar en Railway:

[pegar logs del error]

Mi setup:
- PostgreSQL addon conectado
- Variables: DATABASE_URL, JWT_SECRET, ENVIRONMENT=prod
- Dockerfile multi-stage
- Alembic configurado

¿Cuáles son las 3 causas más probables?
¿Qué debo verificar primero?
¿Cómo puedo reproducir el error localmente?
```

**La IA es excelente para:**
- ✅ Interpretar stack traces
- ✅ Sugerir causas probables
- ✅ Proponer pasos de debugging

**Tú debes:**
- ⚠️ Verificar las variables de entorno (la causa #1)
- ⚠️ Comprobar los logs completos (no solo el error final)
- ⚠️ Reproducir localmente antes de redeploy

---

### Prompt para optimizar Docker

```
Mi imagen Docker es muy grande (800MB) y tarda mucho en subir.

Dockerfile actual:
[pegar Dockerfile]

¿Cómo puedo reducir el tamaño de la imagen?
¿Qué layers están causando el peso?
¿Debería usar multi-stage build?

Restricciones:
- Debo incluir PostgreSQL client (psycopg2)
- Quiero mantener la seguridad (non-root user)
- No sacrificar funcionalidad
```

---

### Prompt para generar tests

```
Rol: QA engineer especializado en pytest.

Contexto: Tengo este endpoint de restaurar tarea eliminada:

[pegar código del endpoint]

Objetivo: Genera tests que cubran:
- Happy path: restaurar tarea eliminada exitosamente
- Edge case: intentar restaurar tarea no eliminada
- Edge case: intentar restaurar tarea de otro usuario
- Error handling: tarea no existe

Restricciones:
- Usar fixtures de conftest.py
- Assertions claras (qué se está verificando)
- Nombres descriptivos de tests

Entrega:
- Código de tests
- Comentarios explicando qué valida cada uno
```

---

### IA como pair programmer

**Workflow recomendado:**

1. **Diseño** → Pide a IA que diseñe la arquitectura
2. **Implementación** → Escribe código tú (o genera y ENTIENDE)
3. **Review** → Pide a IA que revise tu código
4. **Tests** → Genera tests y MODIFÍCALOS para entenderlos
5. **Debugging** → Usa IA para interpretar errores

**Ejemplo de iteración:**

```
Tú: Genera el repositorio de tareas con SQLAlchemy
IA: [genera código]

Tú: El método listar() no tiene paginación
IA: [agrega paginación]

Tú: Ahora agrégale filtros por completada y prioridad
IA: [agrega filtros]

Tú: Los tests para este repositorio
IA: [genera tests]

Tú: [revisas tests, los modificas, los ejecutas]
```

**Regla de oro:** Si no entiendes el código que generó la IA, NO LO USES.

---

## 🧪 Ejercicios prácticos

### Ejercicio 1: Agregar campo "fecha_limite"

**Objetivo**: Agregar fecha límite a las tareas.

**Pasos**:
1. Modificar `TareaModel` agregando `fecha_limite: Mapped[Optional[datetime]]`
2. Generar migración con Alembic
3. Actualizar `TareaCreate` y `TareaUpdate` schemas
4. Agregar filtro `vencidas=true` (tareas con fecha_limite < hoy)
5. Escribir tests

**Prompt IA**:
```
Necesito agregar un campo "fecha_limite" opcional a las tareas.
¿Cómo modifico el modelo ORM?
¿Cómo genero la migración de Alembic?
¿Qué validaciones debo agregar en Pydantic?
```

---

### Ejercicio 2: Endpoint de estadísticas

**Objetivo**: Crear `GET /estadisticas` que devuelva:
```json
{
  "total_tareas": 50,
  "completadas": 30,
  "pendientes": 20,
  "por_prioridad": {
    "alta": 10,
    "media": 25,
    "baja": 15
  }
}
```

**Pasos**:
1. Crear método `estadisticas(usuario_id)` en el repositorio
2. Usar `.count()` y `.group_by()` de SQLAlchemy
3. Crear schema `EstadisticasResponse`
4. Agregar endpoint protegido
5. Escribir tests

**Prompt IA**:
```
Necesito un endpoint que devuelva estadísticas de tareas del usuario.
¿Cómo hago una query con GROUP BY en SQLAlchemy?
¿Cómo optimizo para que sea una sola query a la BD?
```

---

### Ejercicio 3: Notificaciones por email

**Objetivo**: Enviar email cuando se crea una tarea de prioridad alta.

**Pasos**:
1. Instalar `python-decouple` y `aiosmtplib`
2. Configurar SMTP en `config.py`
3. Crear `servicio_emails.py` con `enviar_email(destinatario, asunto, cuerpo)`
4. En `ServicioTareas.crear()`, si `prioridad == 3`, enviar email
5. Escribir tests con mock de email

**Prompt IA**:
```
¿Cómo envío emails desde FastAPI de forma asíncrona?
¿Debería usar background tasks de FastAPI?
¿Cómo mockeo el envío de email en tests?
```

---

### Ejercicio 4: Rate limiting

**Objetivo**: Limitar a 10 requests por minuto por usuario.

**Pasos**:
1. Instalar `slowapi`
2. Configurar rate limiter basado en usuario (no IP)
3. Aplicar a endpoints de creación/actualización
4. Devolver 429 Too Many Requests si excede límite
5. Agregar header `X-RateLimit-Remaining`

**Prompt IA**:
```
¿Cómo implemento rate limiting por usuario en FastAPI?
¿Debería usar Redis o in-memory?
¿Cómo teseo que el rate limiting funciona?
```

---

## 📦 Proyecto final: Extensión avanzada

### Objetivo

Extiende el proyecto base con UNA de estas funcionalidades:

**Opción A: Sistema de etiquetas (tags)**
- Muchos-a-muchos entre Tareas y Etiquetas
- Crear, listar, eliminar etiquetas
- Filtrar tareas por etiqueta
- Endpoints: `POST /etiquetas`, `GET /tareas?etiqueta=urgente`

**Opción B: Comentarios en tareas**
- Relación 1:N (Tarea → Comentarios)
- CRUD de comentarios
- Solo el dueño de la tarea puede comentar
- Endpoints: `POST /tareas/{id}/comentarios`, `GET /tareas/{id}/comentarios`

**Opción C: Compartir tareas entre usuarios**
- Tabla intermedia: `tareas_compartidas` (usuario_id, tarea_id, permisos)
- Permisos: `read`, `write`
- Endpoints: `POST /tareas/{id}/compartir`, `GET /tareas/compartidas`

### Requisitos

1. **Diseño de BD**: Diagrama ER de las nuevas entidades
2. **Migraciones**: Alembic para agregar tablas/campos
3. **Tests**: Coverage ≥ 80% de la nueva funcionalidad
4. **Documentación**: README actualizado con nuevos endpoints
5. **CI/CD**: Tests de la nueva funcionalidad en pipeline

### Entrega

- Branch `feature/nombre-funcionalidad`
- Pull Request a `dev` con:
  - Código implementado
  - Tests pasando
  - CI verde
  - README actualizado

---

## ✅ Checklist de la Clase 8

### Fundamentos (obligatorio)

- [ ] Entiendes arquitectura en capas (API → Service → Repository → DB)
- [ ] Implementaste modelos ORM con relaciones 1:N
- [ ] Configuraste multi-entorno con Pydantic Settings
- [ ] Implementaste autenticación JWT completa
- [ ] Creaste repository pattern con Protocols
- [ ] Implementaste 15+ endpoints REST
- [ ] Agregaste filtros, paginación y búsqueda
- [ ] Configuraste Alembic para migraciones
- [ ] Creaste Dockerfile multi-stage
- [ ] Escribiste tests con 80%+ coverage
- [ ] Configuraste CI/CD con GitHub Actions
- [ ] Desplegaste en Railway o Render

### Conceptos avanzados (opcional)

- [ ] Implementaste soft delete con papelera
- [ ] Agregaste índices compuestos optimizados
- [ ] Usaste eager loading para evitar N+1
- [ ] Implementaste rate limiting
- [ ] Agregaste logging estructurado
- [ ] Configuraste monitoreo (Sentry)

### Integración con IA (40%)

- [ ] Usaste IA para diseñar modelos ORM
- [ ] Generaste tests con IA (y los entendiste)
- [ ] IA te ayudó con debugging de deployment
- [ ] Optimizaste Docker con sugerencias de IA
- [ ] Documentaste qué prompts funcionaron mejor

---

## 🎯 Conceptos clave para recordar

1. **Arquitectura en capas = separación de responsabilidades**: Cada capa hace UNA cosa bien
2. **Repository Pattern = desacoplamiento**: Service no conoce SQLAlchemy
3. **Pydantic Settings = configuración type-safe**: Dev y prod con el mismo código
4. **JWT = autenticación stateless**: No necesitas sesiones en servidor
5. **Migraciones = cambios de schema versionados**: Nunca perder datos en producción
6. **Docker multi-stage = imágenes pequeñas**: 3x más rápido de desplegar
7. **CI/CD = calidad automática**: Tests en cada commit, no solo antes de deploy
8. **Índices compuestos = queries rápidas**: O(log n) en lugar de O(n)

---

## 🚀 Próximos pasos

Has completado el **Módulo 4 - Infraestructura y Cloud**. Ahora sabes:
- ✅ Crear APIs profesionales con FastAPI
- ✅ Diseñar bases de datos relacionales
- ✅ Gestionar migraciones con Alembic
- ✅ Dockerizar aplicaciones
- ✅ Desplegar en cloud (Railway, Render)
- ✅ Implementar CI/CD
- ✅ Usar IA como assistant de desarrollo

**Módulo 5 - Full-Stack + Agent Mastery**:
- Frontend con React + TypeScript
- Orquestación de agentes especializados
- Proyectos completos de principio a fin
- "Un desarrollador solo con un ejército de agentes"

---

## 📖 Recursos adicionales

**Documentación oficial**:
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [SQLAlchemy 2.0 Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [Alembic Cookbook](https://alembic.sqlalchemy.org/en/latest/cookbook.html)
- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)

**Arquitectura**:
- [Clean Architecture in Python](https://www.youtube.com/watch?v=DJtef410XaM)
- [Repository Pattern Explained](https://www.cosmicpython.com/book/chapter_02_repository.html)
- [Twelve-Factor App](https://12factor.net/)

**Seguridad**:
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [JWT Best Practices](https://curity.io/resources/learn/jwt-best-practices/)

**Deployment**:
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Database Migration Strategies](https://www.braintreepayments.com/blog/safe-database-migration-patterns/)

---

¿Preguntas o problemas? Consulta:
- `README.md` para guías técnicas
- `docs/CI_CD.md` para CI/CD
- `docs/AI_INTEGRATION.md` para prompts efectivos
- `GLOSARIO.md` para términos técnicos

**¡Felicitaciones por completar el Módulo 4!** 🎉
