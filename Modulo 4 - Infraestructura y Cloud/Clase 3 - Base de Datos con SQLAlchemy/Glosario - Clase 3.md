## 📘 Glosario – Clase 3

**ORM (Object-Relational Mapper):**

Herramienta que traduce entre objetos de Python (clases, instancias) y tablas de base de datos (filas, columnas).

Te permite trabajar con la BD usando código Python en lugar de escribir SQL manualmente.

SQLAlchemy es el ORM más popular de Python.

**SQLAlchemy:**

Librería Python para trabajar con bases de datos relacionales.

Proporciona un ORM completo y también permite ejecutar SQL raw cuando se necesita.

Versión 2.0 introdujo type hints nativos y mejor integración con type checkers.

**Model (Modelo ORM):**

Clase Python que representa una tabla en la base de datos.

Define las columnas, tipos de datos, relaciones y constraints.

Ejemplo: `class TareaModel(Base)` representa la tabla `tareas`.

**DeclarativeBase:**

Clase base moderna de SQLAlchemy 2.0 de la que heredan todos los modelos ORM.

Reemplaza la función `declarative_base()` de versiones anteriores.

**Mapped[T]:**

Type hint de SQLAlchemy 2.0 para columnas de modelos.

Indica el tipo Python de la columna y proporciona autocompletado en IDEs.

Ejemplo: `id: Mapped[int]` es una columna de tipo entero.

**mapped_column():**

Función de SQLAlchemy 2.0 para definir columnas en modelos ORM.

Reemplaza `Column()` de versiones anteriores con mejor soporte de tipos.

Ejemplo: `nombre: Mapped[str] = mapped_column(String(100))`

**Engine (Motor):**

Objeto que gestiona las conexiones a la base de datos.

Se configura una vez al inicio con la URL de conexión.

Todas las sesiones usan el mismo engine.

**Session (Sesión):**

Una "conversación" con la base de datos.

Maneja transacciones (begin, commit, rollback).

En FastAPI se crea una sesión por cada request HTTP.

**SessionLocal:**

Fábrica de sesiones (sessionmaker).

Produce una sesión nueva cada vez que se llama.

Configurada con `autocommit=False` para control manual de transacciones.

**Repository (Repositorio):**

Patrón de diseño que abstrae el acceso a datos.

Implementa operaciones CRUD (Create, Read, Update, Delete).

Desacopla la lógica de negocio de la tecnología de persistencia.

**CRUD:**

Siglas de Create, Read, Update, Delete.

Las cuatro operaciones básicas sobre datos en cualquier sistema.

**Dependency Injection:**

Patrón donde las dependencias se "inyectan" desde fuera en lugar de crearse dentro.

En FastAPI se usa `Depends()` para inyectar sesiones y servicios.

Facilita testing y desacoplamiento.

**Lifespan Events:**

Mecanismo de FastAPI para ejecutar código al iniciar/cerrar la aplicación.

Reemplaza `@app.on_event("startup")` y `@app.on_event("shutdown")`.

Se implementa con un async context manager.

**commit():**

Método que persiste todos los cambios pendientes en la base de datos.

Marca el final de una transacción exitosa.

Si falla, se puede hacer `rollback()` para deshacer cambios.

**rollback():**

Deshace todos los cambios no confirmados en la sesión actual.

Se usa cuando ocurre un error para mantener consistencia.

**refresh():**

Actualiza un objeto ORM con valores frescos de la base de datos.

Útil después de INSERT para obtener valores generados (ID, timestamps).

**Eager Loading:**

Técnica para cargar relaciones en una sola query (evita N+1).

Se usa `joinedload()` o `selectinload()`.

Ejemplo: `query(Tarea).options(joinedload(Tarea.usuario))`

**N+1 Problem:**

Anti-pattern donde se hacen N queries adicionales para cargar relaciones.

Ocurre cuando se carga una lista y luego se accede a relaciones una por una.

Se soluciona con eager loading.

**Migration (Migración):**

Script que modifica el schema de la BD de forma controlada.

Permite evolucionar la BD sin perder datos.

Alembic es la herramienta estándar para migraciones en SQLAlchemy.

**Alembic:**

Herramienta de migraciones para SQLAlchemy.

Genera scripts SQL para cambios de schema (agregar columna, crear tabla, etc.).

Fundamental para producción (nunca usar `create_all()` en producción).

**Foreign Key (Clave Foránea):**

Columna que referencia la primary key de otra tabla.

Establece relaciones entre tablas.

Ejemplo: `usuario_id` en `tareas` referencia `id` en `usuarios`.

**Relationship:**

Define relaciones entre modelos ORM (one-to-many, many-to-many).

Permite navegar entre objetos relacionados.

Ejemplo: `usuario.tareas` devuelve todas las tareas del usuario.

**Soft Delete:**

Técnica donde no se elimina físicamente el registro, solo se marca como "eliminado".

Se agrega una columna `eliminada: bool` en lugar de hacer DELETE.

Permite recuperar datos "eliminados" y mantener historial.

**Index (Índice):**

Estructura de datos que acelera búsquedas en la base de datos.

Se crea en columnas que se consultan frecuentemente.

Mejora rendimiento de SELECT pero ralentiza INSERT/UPDATE.

**Transaction (Transacción):**

Grupo de operaciones que se ejecutan como una unidad atómica.

Si alguna falla, todas se deshacen (rollback).

Garantiza consistencia de datos.

**SQLite:**

Base de datos relacional embebida (archivo único).

Perfecta para desarrollo y testing (no requiere servidor).

No recomendada para producción con alta concurrencia.

**PostgreSQL:**

Base de datos relacional robusta y popular.

Recomendada para producción en aplicaciones serias.

Soporta features avanzadas (JSON, full-text search, etc.).

**Connection Pool:**

Conjunto de conexiones a la BD que se reutilizan.

Evita crear/destruir conexiones constantemente (mejora rendimiento).

El Engine gestiona el pool automáticamente.
