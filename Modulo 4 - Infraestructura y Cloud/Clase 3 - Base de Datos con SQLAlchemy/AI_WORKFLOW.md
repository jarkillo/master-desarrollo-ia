# AI Workflow - Clase 3: SQLAlchemy con IA

## 🎯 Objetivos de Aprendizaje con IA

En esta clase aprenderás a usar IA como asistente para:

1. **Generar modelos SQLAlchemy** desde esquemas de base de datos
2. **Optimizar queries** detectando N+1 queries y problemas de performance
3. **Validar relaciones ORM** (one-to-many, many-to-many)
4. **Troubleshooting de SQLAlchemy** con asistencia de IA
5. **Validar código** con Database ORM Specialist agent

---

## 🔄 Workflow Completo: De Esquema a Modelos Optimizados

### Fase 1: Generación de Modelos ORM con IA

**Contexto**: Necesitas crear modelos SQLAlchemy 2.0 para tu aplicación de tareas.

#### Prompt 1: Generar modelos desde esquema conceptual

```
Rol: Database architect experto en SQLAlchemy 2.0
Contexto: Necesito crear modelos ORM para una aplicación de gestión de tareas
Objetivo: Generar modelos SQLAlchemy 2.0 con best practices

Esquema conceptual:
- Tabla "users": id, username, email, created_at
- Tabla "tasks": id, title, description, completed, user_id (FK a users)
- Relación: Un usuario tiene muchas tareas

Requisitos:
- SQLAlchemy 2.0 syntax (Mapped[], mapped_column())
- Type hints completos
- Relationships configuradas correctamente
- Timestamps automáticos (created_at, updated_at)
- Constraints apropiados (unique, nullable)

Entrega: Archivo models.py completo con ambos modelos
```

**Resultado esperado**:

```python
# api/models.py
from datetime import datetime
from typing import List
from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    # Relationship
    tasks: Mapped[List["Task"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationship
    user: Mapped["User"] = relationship(back_populates="tasks")
```

#### Validación con Database ORM Specialist

Después de generar los modelos, usa el agente educativo:

```bash
# Invocar Database ORM Specialist agent
# El agente revisará:
# ✓ SQLAlchemy 2.0 patterns (Mapped[], mapped_column())
# ✓ Relationships correctamente configuradas
# ✓ Cascade delete apropiado
# ✓ Indexes en columnas frecuentemente consultadas
# ✓ Nullable vs non-nullable correcto
```

---

### Fase 2: Detección de N+1 Queries con IA

**Problema**: El N+1 query problem es uno de los errores más comunes en ORMs.

#### ¿Qué es un N+1 query?

```python
# ❌ ANTI-PATTERN: N+1 Query
users = session.execute(select(User)).scalars().all()
for user in users:  # 1 query
    print(user.tasks)  # +N queries (uno por cada usuario)
# Total: 1 + N queries
```

#### Prompt 2: Detectar N+1 queries en código existente

```
Rol: Performance analyst especializado en SQLAlchemy
Contexto: Tengo código que puede tener N+1 queries
Objetivo: Identificar y solucionar N+1 query problems

Código a analizar:
```python
def obtener_usuarios_con_tareas():
    session = get_session()
    users = session.execute(select(User)).scalars().all()
    result = []
    for user in users:
        result.append({
            "username": user.username,
            "tasks": [task.title for task in user.tasks]
        })
    return result
```

Tareas:
1. Identificar si existe N+1 query problem
2. Explicar por qué ocurre
3. Proveer solución con eager loading
4. Mostrar la diferencia en número de queries

Entrega: Código optimizado + explicación técnica
```

**Solución optimizada**:

```python
from sqlalchemy.orm import selectinload

def obtener_usuarios_con_tareas_optimizado():
    session = get_session()
    # Eager loading: carga users y tasks en 2 queries (no N+1)
    stmt = select(User).options(selectinload(User.tasks))
    users = session.execute(stmt).scalars().all()

    result = []
    for user in users:
        result.append({
            "username": user.username,
            "tasks": [task.title for task in user.tasks]
        })
    return result

# Performance:
# Antes: 1 + N queries (11 queries para 10 usuarios)
# Después: 2 queries (1 para users, 1 para todas las tasks)
```

---

### Fase 3: Optimización de Queries con IA

#### Prompt 3: Optimizar consultas complejas

```
Rol: Database performance expert
Contexto: Tengo una consulta SQLAlchemy que tarda mucho
Objetivo: Optimizar la query para mejor performance

Query actual:
```python
def obtener_tareas_completadas_por_usuario(user_id: int):
    session = get_session()
    tasks = session.execute(
        select(Task).where(Task.user_id == user_id, Task.completed == True)
    ).scalars().all()
    return tasks
```

Información adicional:
- Tabla tasks tiene 100,000 registros
- 50% de tasks están completadas
- user_id es foreign key
- completed es boolean sin index

Tareas:
1. Identificar cuellos de botella
2. Sugerir indexes necesarios
3. Optimizar la consulta
4. Mostrar EXPLAIN ANALYZE (si es necesario)

Entrega: Query optimizada + migrations para indexes
```

**Solución optimizada**:

```python
# 1. Añadir index compuesto en migration
"""
alembic revision --autogenerate -m "add index on user_id and completed"

# En el archivo de migración:
def upgrade():
    op.create_index(
        'ix_tasks_user_completed',
        'tasks',
        ['user_id', 'completed']
    )
"""

# 2. Query optimizada (sin cambios en código, pero usa el index)
def obtener_tareas_completadas_por_usuario(user_id: int):
    session = get_session()
    stmt = (
        select(Task)
        .where(Task.user_id == user_id)
        .where(Task.completed == True)
        .order_by(Task.created_at.desc())  # Ordenar por recientes
    )
    tasks = session.execute(stmt).scalars().all()
    return tasks

# Performance:
# Antes: Full table scan (100k rows)
# Después: Index scan (~50 rows) - 2000x más rápido
```

---

### Fase 4: Validación de Relaciones con IA

#### Prompt 4: Validar relaciones many-to-many

```
Rol: SQLAlchemy relationship expert
Contexto: Necesito implementar relación many-to-many
Objetivo: Crear relación entre Tasks y Tags con best practices

Requisitos:
- Tabla tasks (ya existe)
- Tabla tags: id, name
- Relación: Una tarea puede tener múltiples tags, un tag puede estar en múltiples tareas
- Usar association table
- SQLAlchemy 2.0 syntax

Entrega: Modelos completos con association table
```

**Resultado esperado**:

```python
# api/models.py
from sqlalchemy import Table, Column, Integer, ForeignKey

# Association table para many-to-many
task_tags = Table(
    "task_tags",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    # Relationship
    tasks: Mapped[List["Task"]] = relationship(
        secondary=task_tags,
        back_populates="tags"
    )

# Modificar Task para añadir relación
class Task(Base):
    # ... (campos existentes)

    # Nueva relación many-to-many
    tags: Mapped[List["Tag"]] = relationship(
        secondary=task_tags,
        back_populates="tasks"
    )
```

---

### Fase 5: Troubleshooting con IA

#### Escenario 1: DetachedInstanceError

**Síntoma**:
```python
task = session.get(Task, 1)
session.close()
print(task.user.username)  # DetachedInstanceError!
```

**Debugging con IA**:

```
Rol: SQLAlchemy troubleshooting specialist
Contexto: Obtengo DetachedInstanceError al acceder a relaciones
Error:
```
DetachedInstanceError: Parent instance <Task> is not bound to a Session
```

Código que causa el error:
```python
def obtener_tarea(task_id: int):
    session = get_session()
    task = session.get(Task, task_id)
    session.close()
    return task

# En otro lugar:
task = obtener_tarea(1)
print(task.user.username)  # Error!
```

Tareas:
1. Explicar por qué ocurre el error
2. Mostrar 3 soluciones diferentes
3. Recomendar la mejor según el caso de uso
4. Explicar trade-offs de cada solución

Entrega: Soluciones comentadas + best practices
```

**Soluciones**:

```python
# Solución 1: Eager loading (RECOMENDADA)
def obtener_tarea_con_usuario(task_id: int):
    session = get_session()
    stmt = select(Task).options(selectinload(Task.user))
    task = session.execute(stmt).where(Task.id == task_id).scalar_one()
    session.close()
    return task
# ✅ Mejor para APIs: carga todo de una vez

# Solución 2: Expunge (copiar objeto)
def obtener_tarea_expunged(task_id: int):
    session = get_session()
    task = session.get(Task, task_id)
    session.expunge(task)  # Desvincula del session
    session.close()
    return task
# ⚠️ Acceder a relaciones lazy causará error

# Solución 3: Session scope más amplio
def obtener_tarea_con_session_abierto(task_id: int):
    session = get_session()
    task = session.get(Task, task_id)
    # NO cerrar session aquí
    return task
# ❌ Evitar: puede causar memory leaks
```

#### Escenario 2: PendingRollbackError

**Debugging con IA**:

```
Rol: Database transaction expert
Contexto: Obtengo PendingRollbackError en transacción
Error:
```
PendingRollbackError: This Session's transaction has been rolled back
```

Código:
```python
try:
    session.add(task)
    session.commit()  # Falla por unique constraint
except Exception:
    pass  # Ignorar error (❌ MAL)

# Siguiente operación
session.add(another_task)  # PendingRollbackError!
```

Tareas:
1. Explicar el ciclo de vida de transactions en SQLAlchemy
2. Mostrar cómo manejar rollback correctamente
3. Pattern de context manager para auto-rollback
4. Best practices para error handling

Entrega: Código corregido + explicación
```

**Solución**:

```python
from contextlib import contextmanager

@contextmanager
def get_db_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()  # ✅ Rollback automático
        raise  # Re-raise para que el caller maneje
    finally:
        session.close()

# Uso:
try:
    with get_db_session() as session:
        session.add(task)
        # Si falla, auto-rollback
except IntegrityError as e:
    return {"error": "Task ya existe"}
```

---

## 🎓 Ejercicios Prácticos con IA

### Ejercicio 1: Generar Modelos desde ERD (30 min)

**Objetivo**: Crear modelos SQLAlchemy desde un diagrama entidad-relación.

**Esquema**:
```
Users (1) ----< (N) Posts (1) ----< (N) Comments
              |
              < (N) Tags (M-to-M)
```

**Tareas**:
1. Usa IA para generar los 4 modelos (User, Post, Comment, Tag)
2. Incluye association table para Post-Tag
3. Configura relaciones bidireccionales
4. Añade timestamps automáticos

**Prompt sugerido**:
```
Rol: Database architect
Objetivo: Crear modelos SQLAlchemy 2.0 desde ERD

ERD:
- Users: id, username, email
- Posts: id, title, content, user_id
- Comments: id, text, user_id, post_id
- Tags: id, name
- Relaciones:
  * User 1:N Posts
  * User 1:N Comments
  * Post 1:N Comments
  * Post M:N Tags

Requisitos: SQLAlchemy 2.0, type hints, timestamps, cascades

Entrega: models.py completo
```

**Validación**:
- [ ] Modelos generados correctamente
- [ ] Relaciones bidireccionales configuradas
- [ ] Cascade delete apropiado
- [ ] Validado con Database ORM Specialist

---

### Ejercicio 2: Detectar y Solucionar N+1 Queries (40 min)

**Objetivo**: Identificar N+1 queries en código real y optimizarlo.

**Código base**:
```python
def obtener_reporte_usuarios():
    """Genera reporte de usuarios con sus posts y comments"""
    users = session.execute(select(User)).scalars().all()
    reporte = []

    for user in users:
        user_data = {
            "username": user.username,
            "posts_count": len(user.posts),  # N+1!
            "posts": []
        }

        for post in user.posts:  # Ya cargado (N+1)
            post_data = {
                "title": post.title,
                "comments_count": len(post.comments)  # Otro N+1!
            }
            user_data["posts"].append(post_data)

        reporte.append(user_data)

    return reporte
```

**Tareas**:
1. Identifica TODOS los N+1 queries (hay múltiples)
2. Usa IA para generar versión optimizada
3. Compara número de queries:
   - Versión original con 10 usuarios, 5 posts cada uno, 3 comments por post
   - Versión optimizada
4. Mide performance con `time`

**Criterios de aceptación**:
- [ ] N+1 queries identificados correctamente
- [ ] Versión optimizada usa joinedload/selectinload
- [ ] Reducción de queries >90%
- [ ] Documentado el before/after

---

### Ejercicio 3: Crear Relación Many-to-Many con Atributos Adicionales (45 min)

**Objetivo**: Implementar association table con columnas adicionales.

**Contexto**: En una app de recetas, queremos relacionar Recipes con Ingredients, pero también guardar la cantidad de cada ingrediente.

**Esquema**:
```
Recipes ----< RecipeIngredients >---- Ingredients
                (quantity, unit)
```

**Tareas**:
1. Usa IA para generar association object (no table)
2. Incluye columnas `quantity` y `unit` en la relación
3. Configura relationships apropiados
4. Crea query para obtener receta con ingredientes y cantidades

**Prompt sugerido**:
```
Rol: SQLAlchemy expert
Objetivo: Crear many-to-many con association object (no table)

Modelos:
- Recipe: id, name, description
- Ingredient: id, name
- RecipeIngredient (association): recipe_id, ingredient_id, quantity, unit

La relación debe permitir:
recipe.ingredients -> Lista de Ingredient
ingredient.recipes -> Lista de Recipe
recipe.recipe_ingredients -> Lista de RecipeIngredient (con quantity, unit)

Entrega: Modelos completos con relationships
```

**Criterios de aceptación**:
- [ ] Association object (no table) creado
- [ ] Atributos adicionales incluidos
- [ ] Relationships bidireccionales funcionales
- [ ] Query para obtener recipe con cantidades

---

### Ejercicio 4: Troubleshooting Session Scope (35 min)

**Objetivo**: Diagnosticar y solucionar problemas de session scope en FastAPI.

**Código problemático**:
```python
# api/dependencias.py
def get_db():
    db = SessionLocal()
    return db  # ❌ No cierra session

# api/api.py
@app.get("/tasks/{task_id}")
def obtener_tarea(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    return task

# Error: memory leak, sessions no se cierran
```

**Tareas**:
1. Usa IA para diagnosticar el problema
2. Implementa context manager correcto
3. Añade error handling con rollback
4. Testea con múltiples requests

**Criterios de aceptación**:
- [ ] Session se cierra correctamente
- [ ] No hay memory leaks
- [ ] Rollback automático en errores
- [ ] Testado con 100+ requests

---

## 📚 Prompts Reutilizables

### Prompt: Generar modelo ORM desde esquema SQL

```
Rol: Database migration specialist
Contexto: Tengo un schema SQL existente y necesito modelos SQLAlchemy
Objetivo: Convertir SQL DDL a modelos SQLAlchemy 2.0

SQL Schema:
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INTEGER DEFAULT 0,
    category_id INTEGER REFERENCES categories(id)
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);
```

Tareas:
1. Convertir a SQLAlchemy 2.0 models
2. Configurar relationship entre Product y Category
3. Usar type hints apropiados (Decimal, int, str)
4. Preservar constraints (unique, nullable, default)

Entrega: models.py con ambos modelos
```

### Prompt: Optimizar query lenta

```
Rol: Database performance analyst
Contexto: Tengo una query SQLAlchemy que tarda >2 segundos
Objetivo: Optimizar para <100ms

Query lenta:
```python
[Pegar código de la query aquí]
```

Información del sistema:
- Tabla tiene [N] registros
- Índices actuales: [listar]
- Database: PostgreSQL/MySQL/SQLite
- Uso típico: [describir patrón de acceso]

Tareas:
1. Analizar query plan (EXPLAIN)
2. Identificar cuellos de botella
3. Sugerir indexes necesarios
4. Optimizar query
5. Estimar mejora de performance

Entrega: Query optimizada + migration para indexes + análisis de impacto
```

### Prompt: Debuggear error de SQLAlchemy

```
Rol: SQLAlchemy troubleshooting expert
Contexto: Obtengo error al ejecutar operación con SQLAlchemy
Error completo:
```
[Pegar stack trace completo]
```

Código que causa el error:
```python
[Pegar código relevante]
```

Modelos involucrados:
```python
[Pegar definiciones de modelos]
```

Tareas:
1. Identificar causa raíz del error
2. Explicar por qué ocurre (lifecycle, sessions, transactions)
3. Proveer 2-3 soluciones con trade-offs
4. Recomendar best practice para prevenir en futuro

Entrega: Fix con explicación técnica + patrón preventivo
```

---

## 🔍 Validación Final con Database ORM Specialist

Antes de dar por completada la clase, ejecuta este checklist:

### Checklist de Validación

```markdown
**Modelos ORM**:
- [ ] SQLAlchemy 2.0 syntax (Mapped[], mapped_column())
- [ ] Type hints completos y correctos
- [ ] Timestamps automáticos (created_at, updated_at)
- [ ] Nullable vs non-nullable correctamente definido
- [ ] Indexes en columnas frecuentemente consultadas
- [ ] Unique constraints donde corresponde

**Relationships**:
- [ ] Relationships bidireccionales configuradas
- [ ] back_populates correcto en ambos lados
- [ ] Cascade delete apropiado (cascade="all, delete-orphan")
- [ ] Lazy loading vs eager loading apropiado
- [ ] Association tables para many-to-many

**Queries**:
- [ ] No hay N+1 queries
- [ ] Eager loading cuando se necesita (selectinload, joinedload)
- [ ] Indexes usados eficientemente
- [ ] Paginación implementada en queries grandes
- [ ] Filters apropiados (indexed columns)

**Sessions & Transactions**:
- [ ] Sessions se cierran correctamente
- [ ] Context managers usados para auto-close
- [ ] Rollback automático en errores
- [ ] No hay memory leaks de sessions
- [ ] Transacciones manejadas apropiadamente

**Performance**:
- [ ] No full table scans en queries frecuentes
- [ ] Indexes compuestos donde son útiles
- [ ] Bulk operations para inserts múltiples
- [ ] Query count optimizado (<5 queries por request típico)
```

---

## 🎯 Resultado Esperado

Al finalizar esta clase, deberías tener:

1. **Modelos ORM** generados con IA y validados
2. **Queries optimizadas** sin N+1 problems
3. **Relaciones correctas** entre modelos
4. **Error handling robusto** con sessions
5. **Skills de troubleshooting** con IA como asistente

**Performance típica**:
- Modelos generados: ~5 min (vs ~30 min manual)
- N+1 detection: ~2 min (vs ~20 min debugging)
- Query optimization: ~10 min (vs ~1h+ profiling)

**Total time saved: ~50-60% usando IA como asistente**

---

## 📖 Recursos Adicionales

**Documentación oficial**:
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html)
- [Type Annotations for Mapped](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#using-annotated-declarative-table)

**Agentes educativos**:
- Database ORM Specialist: `.claude/agents/educational/database-orm-specialist.md`
- Python Best Practices Coach: `.claude/agents/educational/python-best-practices-coach.md`

**Performance profiling**:
- [SQLAlchemy Query Profiling](https://docs.sqlalchemy.org/en/20/faq/performance.html)
- [N+1 Query Problem](https://stackoverflow.com/questions/97197/what-is-the-n1-selects-problem-in-orm-object-relational-mapping)
