# 🔧 AI-Assisted Troubleshooting

Guía práctica para resolver problemas comunes usando IA como asistente.

---

## 📋 Índice de Problemas

1. [Errores de Deployment](#-errores-de-deployment)
2. [Problemas de Base de Datos](#-problemas-de-base-de-datos)
3. [Errores de Autenticación](#-errores-de-autenticación)
4. [Performance Issues](#-performance-issues)
5. [Errores de Docker](#-errores-de-docker)
6. [Problemas de Tests](#-problemas-de-tests)

---

## 🚀 Errores de Deployment

### Problema 1: "Application failed to start"

**Síntomas:**
```
Build exitoso
Container starts
Application crashes immediately
Logs: ModuleNotFoundError: No module named 'api'
```

**Prompt para IA:**
```
Mi aplicación falla al iniciar en Railway con este error:
[pegar logs completos]

Dockerfile:
[pegar Dockerfile]

Estructura del proyecto:
[pegar árbol de directorios]

¿Qué puede estar causando ModuleNotFoundError?
```

**IA sugerirá verificar:**
1. **WORKDIR en Dockerfile** - ¿Está configurado correctamente?
2. **COPY paths** - ¿Copias `./api` correctamente?
3. **PYTHONPATH** - ¿Necesitas agregarlo?

**Solución común:**
```dockerfile
# ❌ MAL
COPY . .
CMD ["uvicorn", "api:app"]

# ✅ BIEN
WORKDIR /app
COPY ./api ./api
CMD ["uvicorn", "api.api:app"]
```

---

### Problema 2: "Database connection refused"

**Síntomas:**
```
App starts
Crash on first request
psycopg2.OperationalError: could not connect to server
```

**Prompt para IA:**
```
Railway/Render configurado con PostgreSQL addon.
DATABASE_URL está configurada en las variables.

Error al conectar:
[pegar error completo]

¿Qué debo verificar?
```

**IA sugerirá:**
1. Ver DATABASE_URL exacta (typo en nombre de variable?)
2. Verificar formato: `postgresql://user:pass@host:port/db`
3. Check de networking (firewall, VPC)

**Checklist:**
- [ ] `echo $DATABASE_URL` muestra la URL completa
- [ ] URL tiene formato correcto (no `postgres://`, sino `postgresql://`)
- [ ] Host y port son accesibles desde el container
- [ ] Credenciales son correctas

**Solución común:**
```python
# En Railway, la variable puede llamarse DATABASE_URL
# pero SQLAlchemy puede necesitar postgresql:// en lugar de postgres://

# api/database.py
import os

database_url = os.getenv("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(database_url)
```

---

### Problema 3: "Migrations not applied"

**Síntomas:**
```
App starts
API endpoints return 500
Logs: sqlalchemy.exc.ProgrammingError: relation "tareas" does not exist
```

**Prompt para IA:**
```
Desplegué en Railway pero las tablas no existen.

Mi railway.toml:
startCommand = "alembic upgrade head && uvicorn api.api:app"

Logs:
[pegar logs de alembic upgrade]

¿Por qué no se aplican las migraciones?
```

**IA identificará:**
- Alembic no encuentra `alembic.ini`
- `env.py` no lee DATABASE_URL correctamente
- Migrations folder no está en la imagen Docker

**Solución:**
```dockerfile
# Dockerfile - asegurar que alembic está incluido
COPY ./alembic ./alembic
COPY alembic.ini .

# Verificar que env.py lee DATABASE_URL
# alembic/env.py
from api.config import settings

def get_url():
    return settings.database_url  # Lee de variable de entorno
```

**Debug local:**
```bash
# Verificar que migrations funcionan localmente
export DATABASE_URL="postgresql://..."
alembic upgrade head
```

---

## 💾 Problemas de Base de Datos

### Problema 1: "N+1 Query Problem"

**Síntomas:**
```
Endpoint /tareas muy lento
PostgreSQL logs muestran 100+ queries para listar 10 tareas
```

**Prompt para IA:**
```
Este endpoint tarda 5 segundos:

@app.get("/tareas")
def listar_tareas(...):
    tareas = db.query(TareaModel).all()
    return [
        {
            "id": t.id,
            "titulo": t.titulo,
            "usuario": t.usuario.nombre  # ⚠️ Aquí hace query por cada tarea
        }
        for t in tareas
    ]

¿Cómo optimizo esto?
```

**IA sugerirá:**
```python
# ✅ Eager loading con joinedload
from sqlalchemy.orm import joinedload

tareas = db.query(TareaModel).options(
    joinedload(TareaModel.usuario)
).all()

# Ahora solo 1 query (JOIN)
```

**Verificar con SQL logging:**
```python
# api/database.py
engine = create_engine(
    settings.database_url,
    echo=True  # ⬅ Ver todas las queries
)
```

---

### Problema 2: "Foreign key constraint violation"

**Síntomas:**
```
IntegrityError: FOREIGN KEY constraint failed
Al intentar crear tarea
```

**Prompt para IA:**
```
Error al crear tarea:

[pegar stack trace]

Modelo:
usuario_id: Mapped[int] = mapped_column(
    ForeignKey("usuarios.id", ondelete="CASCADE")
)

¿Qué estoy haciendo mal?
```

**IA preguntará:**
- ¿El usuario_id existe en la tabla usuarios?
- ¿Estás creando la tarea con un usuario_id válido?

**Solución:**
```python
# ❌ MAL - usar ID hardcoded
tarea = TareaModel(titulo="Test", usuario_id=1)

# ✅ BIEN - verificar que usuario existe
usuario = obtener_usuario_actual(...)  # De JWT
tarea = TareaModel(titulo="Test", usuario_id=usuario.id)
```

---

## 🔐 Errores de Autenticación

### Problema 1: "Invalid token"

**Síntomas:**
```
POST /auth/login → 200 OK (devuelve token)
GET /tareas con Bearer token → 401 Unauthorized
```

**Prompt para IA:**
```
Mi JWT token no funciona:

Genero token:
[pegar código de crear_access_token]

Valido token:
[pegar código de obtener_usuario_actual]

Error: "Could not validate credentials"

¿Qué puede estar mal?
```

**IA sugerirá verificar:**
1. **JWT_SECRET** igual en generación y validación
2. **Algorithm** coincide
3. **Token no expiró**

**Debug:**
```python
# Decodificar token manualmente para ver payload
import jwt

token = "eyJhbGciOiJIUzI1NiIs..."
decoded = jwt.decode(token, verify=False)  # ⚠️ Solo para debug
print(decoded)
# Verifica: sub, user_id, exp
```

**Solución común:**
```python
# ❌ MAL - secrets diferentes
# dev: JWT_SECRET=dev-secret
# prod: JWT_SECRET=prod-secret  # ⚠️ Token de dev no funciona en prod

# ✅ BIEN - regenerar token en cada ambiente
# O usar el mismo secret (no recomendado en prod)
```

---

### Problema 2: "Password verification fails"

**Síntomas:**
```
POST /auth/register → 201 Created
POST /auth/login con misma password → 401 Unauthorized
```

**Prompt para IA:**
```
Registro usuario con password "test123"
Login con "test123" falla

Código de registro:
password_hash = hash_password(request.password)
usuario = Usuario(password_hash=password_hash)

Código de login:
if verificar_password(password, usuario.password_hash):
    # Nunca entra aquí

¿Qué estoy haciendo mal?
```

**IA verificará:**
- ¿Usas bcrypt correctamente?
- ¿El hash se guarda completo en BD? (no truncado)

**Debug:**
```python
# Verificar que hash se guarda completo
password = "test123"
hash1 = hash_password(password)
print(f"Hash generado: {hash1}")

# Guardar en BD
usuario = Usuario(password_hash=hash1)
db.commit()

# Leer de BD
usuario_db = db.query(Usuario).first()
print(f"Hash en BD: {usuario_db.password_hash}")

# Si son diferentes → problema de BD (columna muy corta?)
```

**Solución:**
```python
# Asegurar que columna es lo suficientemente grande
password_hash: Mapped[str] = mapped_column(String(255))  # ✅ Suficiente para bcrypt
```

---

## ⚡ Performance Issues

### Problema 1: "Slow API response"

**Síntomas:**
```
GET /tareas tarda 3+ segundos
Solo 100 tareas en BD
```

**Prompt para IA:**
```
Mi API es muy lenta:

Endpoint:
[pegar código]

¿Qué puede estar causando la lentitud?
¿Hay problema de N+1?
¿Faltan índices?
```

**IA sugerirá:**
1. Ver queries con `echo=True`
2. Check de índices
3. EXPLAIN ANALYZE en PostgreSQL

**Debug con EXPLAIN:**
```sql
-- En PostgreSQL
EXPLAIN ANALYZE
SELECT * FROM tareas WHERE usuario_id = 1 AND completada = false;

-- Si ves "Seq Scan" → Falta índice
-- Si ves "Index Scan" → Índice se está usando
```

**Solución:**
```python
# Agregar índice compuesto
__table_args__ = (
    Index("idx_usuario_completada", "usuario_id", "completada"),
)

# Regenerar migración
alembic revision --autogenerate -m "Add index"
alembic upgrade head
```

---

## 🐳 Errores de Docker

### Problema 1: "Permission denied"

**Síntomas:**
```
docker run → Container starts
Logs: PermissionError: [Errno 13] Permission denied: '/app/tareas.db'
```

**Prompt para IA:**
```
Mi container Docker falla con permission denied:

Dockerfile:
[pegar Dockerfile]

¿Por qué no puede escribir en /app?
```

**IA identificará:**
- Usuario non-root no tiene permisos en `/app`
- Archivos copiados pertenecen a root

**Solución:**
```dockerfile
# ❌ MAL
COPY ./api ./api
USER appuser  # No tiene permisos en archivos copiados

# ✅ BIEN
COPY ./api ./api
RUN chown -R appuser:appuser /app  # Cambiar owner
USER appuser
```

---

### Problema 2: "Module not found en container"

**Síntomas:**
```
docker build → OK
docker run → ModuleNotFoundError: No module named 'pydantic'
```

**Prompt para IA:**
```
Dockerfile:
[pegar Dockerfile]

Build funciona pero runtime falla.
¿Por qué no encuentra pydantic?
```

**IA verificará:**
- Multi-stage build: ¿copiaste las dependencias al runtime stage?

**Solución:**
```dockerfile
# Stage 1: Builder
RUN pip install --user -r requirements.txt

# Stage 2: Runtime
COPY --from=builder /root/.local /root/.local  # ✅ Copiar deps
ENV PATH=/root/.local/bin:$PATH
```

---

## 🧪 Problemas de Tests

### Problema 1: "Tests pass locally, fail in CI"

**Síntomas:**
```
pytest local → All tests pass
GitHub Actions → 5 tests fail
Error: "database is locked"
```

**Prompt para IA:**
```
Tests fallan en CI pero pasan local:

conftest.py:
[pegar fixture de test_db]

GitHub Actions usa Ubuntu.
¿Por qué SQLite se bloquea en CI?
```

**IA sugerirá:**
- SQLite in-memory es single-threaded
- CI puede usar threading/multiprocessing

**Solución:**
```python
# conftest.py
@pytest.fixture(scope="function")
def test_db():
    # ✅ Usar :memory: con check_same_thread=False
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    # ...
```

---

### Problema 2: "Fixtures not cleaning up"

**Síntomas:**
```
Test 1 → Pass
Test 2 → Fail (depends on state from test 1)
```

**Prompt para IA:**
```
Mis tests fallan cuando se ejecutan juntos pero pasan individualmente:

[pegar código de tests]

¿Hay estado compartido entre tests?
```

**IA verificará:**
- Fixtures con scope="session" o "module"
- BD no se limpia entre tests

**Solución:**
```python
# ❌ MAL
@pytest.fixture(scope="module")  # Comparte entre tests
def test_db():
    ...

# ✅ BIEN
@pytest.fixture(scope="function")  # Nueva BD por test
def test_db():
    ...
    yield db
    db.close()
    Base.metadata.drop_all(engine)  # Limpiar
```

---

## 📊 Workflow de Troubleshooting con IA

### 1. Reproduce el error localmente

```bash
# ❌ No debuguear directamente en producción

# ✅ Reproducir local:
export DATABASE_URL="postgresql://..."
export JWT_SECRET="..."
python -m uvicorn api.api:app --reload

# O con Docker:
docker build -t test .
docker run -p 8000:8000 test
```

### 2. Recolecta información completa

```
Para pedirle ayuda a IA, necesitas:
- Stack trace COMPLETO (no solo última línea)
- Código relevante (función donde falla)
- Configuración (Dockerfile, .env, alembic.ini)
- Logs completos (no solo el error)
- Qué has intentado ya
```

### 3. Pregunta específicamente

```
❌ "Mi app no funciona"

✅ "Mi endpoint POST /tareas devuelve 500.
   Error: IntegrityError foreign key constraint.
   Código: [pegar código]
   ¿Qué puede estar mal?"
```

### 4. Verifica cada sugerencia

```
IA sugiere 3 causas posibles:
1. [verificas] → No es esto
2. [verificas] → Tampoco
3. [verificas] → ¡Este era! → Arreglas

No asumas que la primera sugerencia es correcta.
```

### 5. Aprende del proceso

```
Después de arreglar:
- ¿Por qué falló?
- ¿Cómo lo detecté?
- ¿Cómo evito que vuelva a pasar?
- ¿Qué test falta para detectar esto?
```

---

## ✅ Checklist de Troubleshooting

Antes de pedir ayuda a IA:

- [ ] Leí el error completo (no solo última línea)
- [ ] Reproduje el error localmente
- [ ] Verifiqué variables de entorno
- [ ] Revisé logs completos (no solo snippet)
- [ ] Intenté Google/StackOverflow primero
- [ ] Tengo el stack trace completo
- [ ] Identifiqué la función/línea donde falla
- [ ] Puedo describir qué esperaba vs qué pasó

Para pedir ayuda a IA:

- [ ] Contexto claro (qué estoy haciendo)
- [ ] Error completo (stack trace, logs)
- [ ] Código relevante (no todo el proyecto)
- [ ] Qué he intentado ya
- [ ] Entorno (local, Docker, Railway, etc.)

---

## 🎓 Aprendizajes Clave

**1. La IA no tiene acceso a tu entorno**
- Debes copiar logs, variables, código
- No puede "ver" tu pantalla o BD

**2. Garbage in, garbage out**
- Prompt vago → Respuesta genérica
- Prompt específico → Solución concreta

**3. Verifica, no confíes ciegamente**
- IA puede equivocarse
- Tú conoces tu contexto mejor

**4. Aprende de cada error**
- Documenta la solución
- Agrega test para detectar el error
- Comparte con el equipo

---

**Regla final**: La IA es tu **asistente de debug**, no tu **debugger automático**. Tú sigues siendo el desarrollador que debe entender y arreglar el problema.
