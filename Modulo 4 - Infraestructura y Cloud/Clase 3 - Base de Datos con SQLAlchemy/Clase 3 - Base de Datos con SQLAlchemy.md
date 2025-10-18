# Clase 3 - Base de Datos con SQLAlchemy: persistencia real

## 🎬 El problema

Hasta ahora, tu API usa **JSON** o **memoria** para guardar tareas.

Pero cuando reinicias el servidor o tienes múltiples usuarios concurrentes, eso falla:

> "¡Perdí todos mis datos al reiniciar!"
> "¿Por qué dos usuarios están sobrescribiendo sus tareas?"

¿Por qué ocurre?

Porque **no tienes una base de datos real** que:
- Persista datos de forma confiable
- Maneje concurrencia
- Garantice integridad de datos
- Soporte relaciones entre entidades

Para solucionar esto existe **SQLAlchemy**: el ORM (Object-Relational Mapper) más popular de Python.

---

## 🧠 Concepto

Piensa en SQLAlchemy como un **traductor universal**:

- **Tú hablas en Python** (clases, objetos)
- **La BD habla en SQL** (tablas, filas)
- **SQLAlchemy traduce** entre ambos

Por eso:
- No escribes SQL manualmente (el ORM lo genera)
- Los modelos son clases Python normales
- Las consultas son métodos de objetos

### Analogía: La biblioteca municipal

Imagina que tu app es una **biblioteca**:

- **ORM Models** = Las fichas catalográficas (esquema de cada libro)
- **Session** = El bibliotecario (intermedia entre tú y la estantería)
- **Repository** = El mostrador de préstamos (interfaz para operaciones)
- **Database** = Las estanterías reales (almacenamiento físico)

Cuando pides un libro:
1. Hablas con el **mostrador** (Repository)
2. El **bibliotecario** (Session) busca en las **estanterías** (Database)
3. Te devuelve el libro según la **ficha** (Model)

---

## 📚 Fundamentos de SQLAlchemy 2.0

### ¿Qué cambió en SQLAlchemy 2.0?

SQLAlchemy 2.0 introdujo cambios importantes:

✅ **Mejor type hints**: `Mapped[int]` en lugar de `Column(Integer)`
✅ **`mapped_column()`** reemplaza `Column()`
✅ **Declarative base moderna**: `DeclarativeBase` en lugar de `declarative_base()`
✅ **Mejor integración con mypy**: Type checking robusto

### Componentes clave

**1. Engine (Motor)**
- Gestiona conexiones a la BD
- Se configura una vez al inicio
- Ejemplo: `create_engine("sqlite:///./tareas.db")`

**2. Session (Sesión)**
- Una "conversación" con la BD
- Se crea por cada request (en FastAPI)
- Maneja transacciones (commit, rollback)

**3. Model (Modelo)**
- Representa una tabla en Python
- Define columnas, tipos, relaciones
- Hereda de `DeclarativeBase`

**4. Repository (Repositorio)**
- Capa de abstracción sobre la BD
- Implementa operaciones CRUD
- Desacopla la BD del servicio

---

## 🛠️ Aplicación manual

### Paso 1: Instalar SQLAlchemy

```bash
pip install sqlalchemy
```

### Paso 2: Crear el modelo ORM

```python
# api/models.py
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Clase base para todos los modelos"""
    pass


class TareaModel(Base):
    """Modelo ORM para la tabla 'tareas'"""
    __tablename__ = "tareas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    completada: Mapped[bool] = mapped_column(default=False)
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
```

**Explicación**:
- `Mapped[int]`: Type hint nativo de SQLAlchemy 2.0
- `mapped_column()`: Define la columna con opciones
- `server_default=func.now()`: El timestamp se crea en la BD (no en Python)
- `__tablename__`: Nombre de la tabla en la BD

### Paso 3: Configurar la base de datos

```python
# api/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.models import Base

DATABASE_URL = "sqlite:///./tareas.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Solo para SQLite
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def crear_tablas():
    """Crea todas las tablas definidas en los modelos"""
    Base.metadata.create_all(bind=engine)
```

**Explicación**:
- `engine`: Motor que gestiona conexiones
- `SessionLocal`: Fábrica de sesiones (una por request)
- `crear_tablas()`: Crea las tablas en la BD (DDL)

### Paso 4: Crear el repositorio

```python
# api/repositorio_db.py
from sqlalchemy.orm import Session
from api.models import TareaModel
from api.servicio_tareas import Tarea


class RepositorioDB:
    def __init__(self, session: Session):
        self._session = session

    def guardar(self, tarea: Tarea) -> None:
        if tarea.id == 0:
            # Nueva tarea - INSERT
            db_tarea = TareaModel(
                nombre=tarea.nombre,
                completada=tarea.completada
            )
            self._session.add(db_tarea)
            self._session.commit()
            self._session.refresh(db_tarea)
            tarea.id = db_tarea.id
        else:
            # Actualización - UPDATE
            db_tarea = self._session.get(TareaModel, tarea.id)
            if db_tarea:
                db_tarea.nombre = tarea.nombre
                db_tarea.completada = tarea.completada
                self._session.commit()

    def listar(self) -> List[Tarea]:
        db_tareas = self._session.query(TareaModel).all()
        return [
            Tarea(id=t.id, nombre=t.nombre, completada=t.completada)
            for t in db_tareas
        ]
```

**Explicación**:
- **Session injection**: La sesión se inyecta desde fuera
- **Separación ORM/Dominio**: `TareaModel` (BD) vs `Tarea` (Pydantic)
- **commit()**: Persiste los cambios en la BD
- **refresh()**: Obtiene valores generados por la BD (ej: ID)

### Paso 5: Integrar con FastAPI (Dependency Injection)

```python
# api/dependencias.py
from fastapi import Depends
from sqlalchemy.orm import Session
from api.database import get_db
from api.repositorio_db import RepositorioDB
from api.servicio_tareas import ServicioTareas


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_repositorio(db: Session = Depends(get_db)) -> RepositorioDB:
    return RepositorioDB(session=db)


def get_servicio(repo: RepositorioDB = Depends(get_repositorio)) -> ServicioTareas:
    return ServicioTareas(repositorio=repo)
```

**Explicación**:
- **Dependency chain**: `get_db → get_repositorio → get_servicio`
- **Lifecycle management**: La sesión se cierra automáticamente
- **Thread safety**: Cada request tiene su propia sesión

### Paso 6: Usar en endpoints

```python
# api/api.py
from fastapi import FastAPI, Depends
from api.dependencias import get_servicio
from api.servicio_tareas import ServicioTareas, TareaCreate


@app.post("/tareas")
def crear_tarea(
    tarea_data: TareaCreate,
    servicio: ServicioTareas = Depends(get_servicio)
):
    return servicio.crear(nombre=tarea_data.nombre)
```

### Paso 7: Inicializar BD al arrancar (Lifespan Events)

```python
# api/api.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.database import crear_tablas


@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    print("🚀 Iniciando aplicación...")
    crear_tablas()
    yield
    # SHUTDOWN
    print("🛑 Cerrando aplicación...")


app = FastAPI(lifespan=lifespan)
```

**Explicación**:
- **Lifespan events**: Reemplazan `@app.on_event("startup")`
- **Async context manager**: Maneja inicio y cierre limpiamente
- **Crear tablas**: Se ejecuta una vez al arrancar

---

## 🤖 Aplicación con IA (40%)

### Prompt para generar modelos ORM

```
Rol: Database architect especializado en SQLAlchemy 2.0.

Contexto: Tengo una API FastAPI que actualmente usa JSON.
Necesito migrar a SQLAlchemy con PostgreSQL en producción.

Objetivo: Genera un modelo ORM para la entidad "Tarea" usando:
- SQLAlchemy 2.0 syntax (Mapped[], mapped_column)
- Type hints completos
- Timestamps automáticos (creado_en, actualizado_en)
- Validaciones a nivel de BD (constraints)
- Índices para optimizar búsquedas

Restricciones:
- Usar DeclarativeBase (no declarative_base())
- Compatible con PostgreSQL y SQLite
- Seguir convenciones de naming (snake_case para tablas)

Entrega:
- Código del modelo
- Explicación de cada decisión de diseño
```

**Qué puede generar la IA**:
- ✅ Modelos ORM completos con relaciones
- ✅ Migrations iniciales (con Alembic)
- ✅ Queries optimizadas (evitar N+1)
- ✅ Índices para mejorar rendimiento

**Qué DEBES validar tú**:
- ⚠️ Los tipos de datos (Int vs BigInt, String(100) vs Text)
- ⚠️ Las relaciones (one-to-many, many-to-many)
- ⚠️ Los índices (¿realmente se necesita en esa columna?)
- ⚠️ La seguridad (¿falta validación de integridad?)

### Prompt para optimizar queries

```
Rol: Performance engineer especializado en SQLAlchemy.

Contexto: Mi endpoint `/tareas` lista todas las tareas con sus usuarios asignados.
Actualmente hace 1 + N queries (problema N+1).

Código actual:
[pegar código del endpoint]

Objetivo: Optimiza las queries usando:
- Eager loading (joinedload, selectinload)
- Paginación (offset, limit)
- Filtros eficientes

Restricciones:
- Mantener la misma interfaz pública del endpoint
- No comprometer la legibilidad del código

Entrega:
- Código optimizado
- Explicación de qué mejoró y por qué
- Comparativa de queries antes/después
```

### Prompt para generar tests de integración

```
Rol: QA engineer especializado en testing de bases de datos.

Contexto: Tengo un RepositorioDB que implementa CRUD con SQLAlchemy.

Objetivo: Genera tests de integración que verifiquen:
- CRUD completo (create, read, update, delete)
- Persistencia entre operaciones
- Manejo de errores (duplicados, FK violations)
- Casos edge (eliminar algo que no existe, actualizar con datos inválidos)

Restricciones:
- Usar SQLite in-memory para tests
- Fixtures con pytest
- Limpiar BD entre tests (autouse fixture)

Entrega:
- Código de tests completo
- Comentarios explicando qué valida cada test
```

### IA como validador de diseño

Después de crear tu modelo ORM, usa este prompt:

```
Soy un estudiante aprendiendo SQLAlchemy. Acabo de crear este modelo:

[pegar código del modelo]

¿Podrías revisarlo y decirme:
1. ¿Hay algún anti-pattern? (ej: falta de índices, tipos incorrectos)
2. ¿Las relaciones están bien definidas?
3. ¿Falta alguna validación a nivel de BD?
4. ¿Cómo podría optimizar este modelo para queries frecuentes?

No quiero la solución completa, solo hints de qué buscar y por qué.
```

---

## 🔍 Conceptos avanzados (para estudiantes que quieren más)

### 1. Relaciones en SQLAlchemy

**One-to-Many** (Un usuario tiene muchas tareas):

```python
class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))

    # Relación
    tareas: Mapped[List["Tarea"]] = relationship(back_populates="usuario")


class Tarea(Base):
    __tablename__ = "tareas"
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))

    # Relación inversa
    usuario: Mapped["Usuario"] = relationship(back_populates="tareas")
```

**Consultar con relaciones**:

```python
# Eager loading (1 query)
usuario = session.query(Usuario).options(joinedload(Usuario.tareas)).first()
print(usuario.tareas)  # No hace otra query

# Sin eager loading (N+1 queries)
usuario = session.query(Usuario).first()
print(usuario.tareas)  # Hace otra query aquí
```

### 2. Migraciones con Alembic

**¿Por qué Alembic?**
- `create_all()` solo funciona para desarrollo
- En producción necesitas **migrations** (cambios incrementales)
- Alembic genera SQL para actualizar el schema sin perder datos

**Setup básico**:

```bash
pip install alembic
alembic init alembic
```

**Generar migration**:

```bash
alembic revision --autogenerate -m "Add tareas table"
alembic upgrade head
```

### 3. Optimización de queries

**Problema: N+1 queries**

```python
# ❌ MAL: 1 query para tareas + N queries para usuarios
tareas = session.query(Tarea).all()
for tarea in tareas:
    print(tarea.usuario.nombre)  # Query por cada tarea
```

**Solución: Eager loading**

```python
# ✅ BIEN: 1 sola query con JOIN
tareas = session.query(Tarea).options(joinedload(Tarea.usuario)).all()
for tarea in tareas:
    print(tarea.usuario.nombre)  # Sin query adicional
```

### 4. Transacciones y rollback

```python
try:
    session.add(nueva_tarea)
    session.add(nuevo_usuario)
    session.commit()  # Se guardan ambos o ninguno
except Exception as e:
    session.rollback()  # Deshace TODO
    raise
```

---

## 🧪 Ejercicios prácticos

### Ejercicio 1: Agregar campo "prioridad"

**Objetivo**: Agregar un campo `prioridad` (int) a la tabla tareas.

**Pasos**:
1. Modificar `TareaModel` para incluir `prioridad: Mapped[int]`
2. Actualizar `Tarea` (Pydantic) con el campo
3. Modificar el repositorio para guardar/leer la prioridad
4. Crear un endpoint `GET /tareas?prioridad=1` que filtre por prioridad
5. Escribir tests

**Prompt IA para ayuda**:
```
Tengo un modelo Tarea con (id, nombre, completada).
Quiero agregar un campo "prioridad" (1=baja, 2=media, 3=alta).

¿Cómo modifico el modelo ORM?
¿Necesito un índice en este campo?
¿Cómo implemento el filtro en el repositorio?
```

### Ejercicio 2: Implementar búsqueda por nombre

**Objetivo**: Crear un endpoint que busque tareas por nombre (case-insensitive).

**Pasos**:
1. Agregar método `buscar_por_nombre(texto: str)` al repositorio
2. Usar `.filter()` con `.ilike()` (case-insensitive)
3. Crear endpoint `GET /tareas/buscar?q=comprar`
4. Escribir tests

**Prompt IA**:
```
¿Cómo hago una búsqueda case-insensitive en SQLAlchemy?
¿Debería usar .filter() o .where()?
¿Necesito un índice para búsquedas de texto?
```

### Ejercicio 3: Soft delete (borrado lógico)

**Objetivo**: En lugar de eliminar tareas, marcarlas como "eliminada=True".

**Pasos**:
1. Agregar campo `eliminada: Mapped[bool]` al modelo
2. Modificar `.listar()` para filtrar `eliminada=False`
3. Modificar `.eliminar()` para hacer UPDATE en lugar de DELETE
4. Crear endpoint `GET /tareas/papelera` que liste eliminadas
5. Escribir tests

**Prompt IA**:
```
¿Qué es soft delete y cuándo usarlo?
¿Cómo implemento un filtro global en SQLAlchemy para excluir "eliminadas"?
```

### Ejercicio 4: Paginación

**Objetivo**: Implementar paginación en `GET /tareas`.

**Pasos**:
1. Modificar `.listar(limit: int, offset: int)` en el repositorio
2. Usar `.limit()` y `.offset()` en la query
3. Modificar endpoint para aceptar `?page=1&page_size=10`
4. Agregar metadata (total_items, total_pages) en la respuesta
5. Escribir tests

**Prompt IA**:
```
¿Cómo implemento paginación eficiente en SQLAlchemy?
¿Debería usar limit/offset o cursor-based pagination?
¿Cómo cuento el total de items sin cargar todo en memoria?
```

### Ejercicio 5: Timestamps automáticos con eventos

**Objetivo**: Actualizar `actualizado_en` automáticamente al modificar una tarea.

**Pasos**:
1. Ya tienes `actualizado_en` con `onupdate=func.now()`
2. Verificar que funciona haciendo un UPDATE
3. Crear un test que valide que `actualizado_en` cambia al actualizar
4. (Avanzado) Usar eventos de SQLAlchemy para logging

**Prompt IA**:
```
¿Cómo valido que onupdate funciona correctamente en tests?
¿Qué son los eventos de SQLAlchemy y cuándo usarlos?
```

---

## 📦 Proyecto final: Migrar de JSON a BD

### Objetivo

Migrar la aplicación de tareas de `RepositorioJSON` a `RepositorioDB` sin romper la API.

### Requisitos

1. **Sin cambios en la API**: Los endpoints deben funcionar igual
2. **Migración de datos**: Los datos de `tareas.json` deben importarse a la BD
3. **Tests deben pasar**: Todos los tests existentes deben seguir funcionando
4. **Documentación**: Documenta el proceso de migración

### Pasos sugeridos

**Paso 1: Implementar RepositorioDB (ya lo hiciste)**

**Paso 2: Script de migración de datos**

```python
# scripts/migrar_json_a_db.py
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.models import Base, TareaModel

# Leer tareas.json
with open("tareas.json", "r") as f:
    tareas_json = json.load(f)

# Conectar a BD
engine = create_engine("sqlite:///./tareas.db")
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

# Migrar
for tarea_data in tareas_json:
    tarea = TareaModel(
        nombre=tarea_data["nombre"],
        completada=tarea_data["completada"]
    )
    session.add(tarea)

session.commit()
print(f"✅ Migradas {len(tareas_json)} tareas")
```

**Paso 3: Cambiar dependencias**

```python
# api/dependencias.py
def get_repositorio(db: Session = Depends(get_db)) -> RepositorioDB:
    # Antes: return RepositorioJSON()
    return RepositorioDB(session=db)  # Ahora
```

**Paso 4: Validar**

```bash
# 1. Correr tests
pytest tests/ -v

# 2. Probar manualmente
uvicorn api.api:app --reload
curl http://localhost:8000/tareas

# 3. Validar datos
sqlite3 tareas.db "SELECT * FROM tareas"
```

### Prompt IA para el proyecto

```
Tengo una API con RepositorioJSON que guarda tareas en JSON.
Quiero migrar a RepositorioDB (SQLAlchemy) sin romper nada.

¿Cuál es el proceso seguro?
¿Cómo valido que no perdí datos?
¿Debo hacer backup del JSON?
¿Qué tests adicionales necesito?
```

---

## ✅ Checklist de la Clase 3

### Fundamentos (obligatorio)

- [ ] Entiendes qué es un ORM y por qué usarlo
- [ ] Creaste un modelo ORM con SQLAlchemy 2.0 syntax
- [ ] Configuraste engine y session factory
- [ ] Implementaste RepositorioDB con CRUD completo
- [ ] Integraste SQLAlchemy con FastAPI (dependency injection)
- [ ] Usaste lifespan events para inicializar BD
- [ ] Todos los tests pasan (unitarios + integración)

### Conceptos avanzados (opcional)

- [ ] Entiendes la diferencia entre `joinedload` y `selectinload`
- [ ] Sabes qué es el problema N+1 y cómo evitarlo
- [ ] Implementaste soft delete
- [ ] Agregaste paginación
- [ ] Usaste Alembic para migraciones

### Integración con IA (40% del contenido)

- [ ] Usaste IA para generar el modelo inicial
- [ ] Validaste el modelo con IA (revisión de anti-patterns)
- [ ] IA te ayudó a optimizar queries
- [ ] Generaste tests con IA y los entiendes
- [ ] Documentaste qué prompts funcionaron mejor

---

## 🎯 Conceptos clave para recordar

1. **ORM traduce Python ↔ SQL**: No escribes SQL manualmente
2. **Session = conversación con BD**: Se crea por request, se cierra después
3. **Repository desacopla BD de lógica**: El servicio no conoce SQLAlchemy
4. **Dependency injection es crucial**: FastAPI maneja el ciclo de vida
5. **IA genera código, tú lo validas**: Especialmente en diseño de BD

---

## 📖 Recursos adicionales

**Documentación oficial**:
- [SQLAlchemy 2.0 Docs](https://docs.sqlalchemy.org/en/20/)
- [FastAPI + SQLAlchemy](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)

**Tutoriales recomendados**:
- SQLAlchemy 2.0 Type Annotations
- N+1 Query Problem Explained
- Database Indexing Best Practices

**Herramientas útiles**:
- SQLite Browser (visualizar BD)
- pgAdmin (para PostgreSQL)
- DBeaver (cliente universal)

---

## 🚀 Próxima clase

**Clase 4: Migraciones con Alembic**

En la próxima clase aprenderás:
- Cómo gestionar cambios de schema sin perder datos
- Migraciones automáticas vs manuales
- Rollback de migraciones
- Deployments sin downtime
