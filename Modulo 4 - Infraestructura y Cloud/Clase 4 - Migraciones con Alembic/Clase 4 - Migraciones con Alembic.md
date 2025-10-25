# Clase 4 - Migraciones con Alembic: cambios de schema sin perder datos

## 🎬 El problema

En la Clase 3 usaste `Base.metadata.create_all()` para crear tablas:

```python
def crear_tablas():
    Base.metadata.create_all(bind=engine)
```

Pero este enfoque tiene problemas **graves en producción**:

> "¡Agregué un campo al modelo pero la BD no se actualizó!"
> "¡Perdí todos los datos al recrear las tablas!"
> "¿Cómo revierto este cambio de schema que rompió todo?"

¿Por qué ocurre?

Porque `create_all()` solo funciona para **desarrollo**:
- **No actualiza** tablas existentes (solo crea las que faltan)
- **No migra datos** cuando cambias el schema
- **No hay rollback** si algo sale mal
- **No hay historial** de cambios

Para solucionar esto existe **Alembic**: el sistema de migraciones de base de datos para SQLAlchemy.

---

## 🧠 Concepto

Piensa en Alembic como un **sistema de control de versiones para tu base de datos**:

- **Git versiona tu código** (commit, checkout, revert)
- **Alembic versiona tu schema** (upgrade, downgrade, history)

Por eso:
- Cada cambio de schema es una "migration" (como un commit)
- Puedes avanzar (upgrade) o retroceder (downgrade)
- Tienes un historial completo de cambios
- Puedes aplicar cambios en cualquier entorno (dev, staging, producción)

### Analogía: El arquitecto y las reformas

Imagina que tu BD es un **edificio en construcción**:

- **Schema inicial** = Plano original del edificio
- **Migration** = Orden de reforma ("agregar balcón al piso 3")
- **upgrade** = Aplicar la reforma
- **downgrade** = Deshacer la reforma (quitar el balcón)
- **Alembic history** = Historial de todas las reformas

Cuando haces una reforma:
1. El **arquitecto** (Alembic) genera un **plano de cambios** (migration file)
2. El **constructor** (alembic upgrade) aplica los cambios
3. Si algo sale mal, puedes **revertir** (alembic downgrade)
4. El historial registra **quién**, **cuándo** y **qué** se cambió

---

## 📚 Fundamentos de Alembic

### ¿Qué es Alembic?

Alembic es una herramienta de **migración de bases de datos** para SQLAlchemy. Permite:

✅ **Generar migrations automáticamente** desde tus modelos
✅ **Aplicar cambios incrementales** sin perder datos
✅ **Revertir cambios** si algo sale mal
✅ **Mantener historial** de cambios de schema
✅ **Trabajar en equipo** (migrations en control de versiones)

### Componentes clave

**1. `alembic.ini`**
- Configuración de Alembic
- URL de la base de datos
- Hooks de formateo (ruff, black)

**2. `alembic/env.py`**
- Script de entorno
- Conecta Alembic con tus modelos SQLAlchemy
- Configura el contexto de ejecución

**3. `alembic/versions/`**
- Carpeta con archivos de migraciones
- Cada archivo es un cambio de schema
- Nombrados con timestamp y descripción

**4. Migration file**
- Define funciones `upgrade()` y `downgrade()`
- SQL generado automáticamente o escrito manualmente
- Cadena de dependencias entre migrations

### Workflow básico

```
┌─────────────┐
│  Modificar  │
│   Modelo    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│ alembic revision        │
│   --autogenerate        │
│   -m "descripcion"      │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Revisar migration      │
│  generada (IMPORTANTE)  │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  alembic upgrade head   │
└─────────────────────────┘
```

---

## 🛠️ Aplicación manual

### Paso 1: Instalar Alembic

```bash
# Activar entorno virtual (SIEMPRE)
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Instalar Alembic
pip install alembic
```

### Paso 2: Inicializar Alembic

```bash
# Desde el directorio de tu proyecto
alembic init alembic
```

Esto crea:
```
tu_proyecto/
├── alembic/
│   ├── versions/          # Carpeta de migraciones
│   ├── env.py             # Script de entorno
│   ├── README
│   └── script.py.mako     # Template para migrations
└── alembic.ini            # Configuración
```

### Paso 3: Configurar `alembic.ini`

Edita `alembic.ini` y cambia la URL de la base de datos:

```ini
# Línea 87
sqlalchemy.url = sqlite:///./tareas.db

# O para PostgreSQL en producción:
# sqlalchemy.url = postgresql://user:password@localhost/dbname
```

**Tip**: Habilita el hook de ruff para formatear migrations automáticamente:

```ini
# Líneas 102-105 (descomentar)
hooks = ruff
ruff.type = module
ruff.module = ruff
ruff.options = check --fix REVISION_SCRIPT_FILENAME
```

### Paso 4: Configurar `alembic/env.py`

Edita `alembic/env.py` para importar tus modelos:

```python
# Línea 19 (reemplazar)
from api.models import Base
target_metadata = Base.metadata
```

**Explicación**:
- `target_metadata`: Le dice a Alembic qué modelos usar
- Alembic compara `Base.metadata` (modelos) con la BD actual
- Genera migrations automáticamente basadas en las diferencias

### Paso 5: Crear la primera migration

```bash
# Generar migration automáticamente
alembic revision --autogenerate -m "crear tabla tareas"
```

Output:
```
Generating alembic/versions/58cbce442bf6_crear_tabla_tareas.py ...  done
Running post write hook 'ruff' ... All checks passed!
INFO  [alembic.autogenerate.compare] Detected added table 'tareas'
```

Alembic generó un archivo como este:

```python
# alembic/versions/58cbce442bf6_crear_tabla_tareas.py
"""crear tabla tareas

Revision ID: 58cbce442bf6
Revises:
Create Date: 2025-10-19 01:22:14.276126
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '58cbce442bf6'
down_revision: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Aplicar cambios al schema"""
    op.create_table('tareas',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('completada', sa.Boolean(), nullable=False),
        sa.Column('creado_en', sa.DateTime(timezone=True),
                  server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('actualizado_en', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Revertir cambios (rollback)"""
    op.drop_table('tareas')
```

**Explicación**:
- `revision`: ID único de esta migration
- `down_revision`: Migration anterior (None = primera)
- `upgrade()`: Crea la tabla
- `downgrade()`: Elimina la tabla (rollback)

### Paso 6: Aplicar la migration

```bash
# Aplicar todas las migrations pendientes
alembic upgrade head
```

Output:
```
INFO  [alembic.runtime.migration] Running upgrade  -> 58cbce442bf6, crear tabla tareas
```

Verificar que la tabla se creó:

```bash
# SQLite
sqlite3 tareas.db ".schema tareas"

# PostgreSQL
psql -d tu_bd -c "\d tareas"
```

### Paso 7: Modificar el schema (segunda migration)

Ahora vamos a agregar un campo `prioridad` al modelo:

```python
# api/models.py
class TareaModel(Base):
    __tablename__ = "tareas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    completada: Mapped[bool] = mapped_column(default=False)

    # NUEVO CAMPO
    prioridad: Mapped[int] = mapped_column(default=2)  # 1=baja, 2=media, 3=alta

    creado_en: Mapped[datetime] = mapped_column(...)
    actualizado_en: Mapped[Optional[datetime]] = mapped_column(...)
```

Generar migration:

```bash
alembic revision --autogenerate -m "agregar campo prioridad"
```

Output:
```
Generating alembic/versions/05702ef4b618_agregar_campo_prioridad.py ...  done
INFO  [alembic.autogenerate.compare] Detected added column 'tareas.prioridad'
```

Migration generada:

```python
# alembic/versions/05702ef4b618_agregar_campo_prioridad.py
revision: str = '05702ef4b618'
down_revision: Union[str, Sequence[str], None] = '58cbce442bf6'  # ← Apunta a la anterior


def upgrade() -> None:
    op.add_column('tareas', sa.Column('prioridad', sa.Integer(), nullable=False))


def downgrade() -> None:
    op.drop_column('tareas', 'prioridad')
```

**Nota importante**: `down_revision` crea una **cadena de migraciones**:

```
None → 58cbce442bf6 → 05702ef4b618 → (siguientes migrations...)
```

Aplicar migration:

```bash
alembic upgrade head
```

### Paso 8: Rollback (deshacer cambios)

Si algo sale mal, puedes revertir:

```bash
# Retroceder 1 migration
alembic downgrade -1

# Retroceder a una revisión específica
alembic downgrade 58cbce442bf6

# Retroceder TODO (⚠️ peligroso en producción)
alembic downgrade base
```

Verificar rollback:

```bash
sqlite3 tareas.db ".schema tareas"
# La columna 'prioridad' desapareció
```

Volver a aplicar:

```bash
alembic upgrade head
# La columna 'prioridad' vuelve
```

### Paso 9: Ver historial de migrations

```bash
# Ver historial completo
alembic history

# Ver migración actual
alembic current

# Ver migrations pendientes
alembic show head
```

---

## 🤖 Aplicación con IA (40%)

**Ver workflow completo**: `AI_WORKFLOW.md` incluye:
- **Generación automática** de migrations con validación de seguridad
- **Detección de migraciones peligrosas** (NOT NULL en tablas con datos)
- **Estrategias multi-paso** para zero-downtime deployments
- **Data migrations seguras** con validación inline
- **Troubleshooting** de conflictos (multiple heads, branches)
- **Production rollback strategies** con backups
- **5 ejercicios prácticos** guiados con IA (120 min total)

### Agentes Educativos Integrados

**Database ORM Specialist** (`.claude/agents/educational/database-orm-specialist.md`):
- Valida migraciones antes de aplicar en producción
- Detecta pérdida potencial de datos
- Verifica backward compatibility
- Revisa que downgrade funciona correctamente

**Python Best Practices Coach** (`.claude/agents/educational/python-best-practices-coach.md`):
- Revisa código de migrations (type hints, docstrings)
- Valida nombres descriptivos de columnas
- Verifica manejo de errores en data migrations

### Prompt para generar migrations

```
Rol: Database migration specialist especializado en Alembic.

Contexto: Tengo una tabla 'tareas' con (id, nombre, completada, creado_en, actualizado_en).
Necesito agregar un campo 'etiquetas' que sea un JSON array de strings.

Objetivo: Genera una migration de Alembic que:
- Agregue la columna 'etiquetas' como JSON (PostgreSQL) o TEXT (SQLite)
- Incluya un valor por defecto (array vacío)
- Sea reversible (downgrade debe funcionar)
- Sea compatible con PostgreSQL y SQLite

Restricciones:
- Usar Alembic operations (op.add_column, op.drop_column)
- Type hints completos
- Comentarios explicando cada decisión

Entrega:
- Código de la migration
- Explicación de por qué usaste JSON vs TEXT
- Estrategia para migrar datos existentes
```

**Qué puede generar la IA**:
- ✅ Migrations complejas (agregar índices, foreign keys, constraints)
- ✅ Data migrations (transformar datos durante la migración)
- ✅ Migrations multi-BD (SQLite, PostgreSQL, MySQL)
- ✅ Rollback strategies para cambios complejos

**Qué DEBES validar tú**:
- ⚠️ Las migrations generadas (NUNCA las apliques sin revisarlas)
- ⚠️ El impacto en datos existentes (¿se perderán datos?)
- ⚠️ La reversibilidad (¿el downgrade funciona?)
- ⚠️ El rendimiento (¿agregar un índice va a tardar horas en millones de filas?)

### Prompt para validar migrations

```
Soy un estudiante aprendiendo Alembic. Acabo de generar esta migration:

[pegar código de la migration]

¿Podrías revisarla y decirme:
1. ¿Hay algún problema de seguridad? (ej: perder datos, locks, downtime)
2. ¿El downgrade funciona correctamente?
3. ¿Falta algún índice o constraint?
4. ¿Cómo afecta esto a datos existentes en producción?
5. ¿Hay una forma más segura de hacer este cambio?

No quiero la solución completa, solo hints de qué buscar y por qué.
```

### Prompt para migrations complejas

```
Rol: Senior database engineer especializado en zero-downtime deployments.

Contexto: Necesito renombrar una columna 'nombre' a 'titulo' en la tabla 'tareas'.
Esta tabla tiene 1 millón de filas en producción.

Objetivo: Genera una estrategia de migration que:
- NO cause downtime
- NO bloquee la tabla (o lo mínimo posible)
- Sea reversible
- Funcione con aplicaciones desplegadas gradualmente (blue-green)

Restricciones:
- PostgreSQL 14
- Aplicación FastAPI con múltiples instancias
- No podemos detener la app durante la migración

Entrega:
- Estrategia paso a paso (puede ser multi-migration)
- Código de las migrations
- Explicación de por qué esta estrategia minimiza downtime
```

**Respuesta esperada de la IA**:

```
Estrategia: Migración en 3 pasos (zero-downtime)

Paso 1: Agregar columna 'titulo', mantener 'nombre'
- Migration 1: ADD COLUMN titulo
- Código actualizado: Escribir en ambos campos (nombre, titulo)
- Deploy gradual

Paso 2: Migrar datos
- Migration 2: UPDATE tareas SET titulo = nombre WHERE titulo IS NULL
- Crear trigger para sincronizar (PostgreSQL)

Paso 3: Eliminar columna 'nombre'
- Migration 3: DROP COLUMN nombre
- Código actualizado: Solo usa 'titulo'
- Deploy gradual

Por qué funciona:
- Sin bloqueos largos (cada paso es rápido)
- Aplicaciones viejas y nuevas funcionan simultáneamente
- Rollback posible en cada paso
```

### Prompt para data migrations

```
Rol: Data migration specialist.

Contexto: Tengo una columna 'prioridad' (integer: 1, 2, 3) que quiero migrar a
'prioridad_texto' (string: "baja", "media", "alta").

Objetivo: Genera una migration que:
- Agregue la nueva columna
- Transforme los datos existentes (1→"baja", 2→"media", 3→"alta")
- Valide que no queden valores NULL
- Sea reversible

Entrega:
- Código de la migration
- Explicación de cómo manejar datos inconsistentes (ej: prioridad=99)
```

### IA como validador de migrations

Después de generar una migration, usa este prompt:

```
Acabo de generar esta migration para [describir el cambio]:

[pegar migration]

Revisa:
1. ¿Puede causar pérdida de datos?
2. ¿El downgrade funciona?
3. ¿Hay problemas de rendimiento en tablas grandes?
4. ¿Qué pasa con datos existentes?
5. ¿Debería hacer esto en múltiples migrations?

Dame un checklist de validación para producción.
```

---

## 🔍 Conceptos avanzados

### 1. Data Migrations (migrar datos)

A veces necesitas **transformar datos**, no solo modificar el schema:

**Ejemplo**: Migrar de un campo `nombre_completo` a `nombre` + `apellido`

```python
# alembic/versions/xxx_split_nombre.py
def upgrade() -> None:
    # 1. Agregar columnas nuevas
    op.add_column('usuarios', sa.Column('nombre', sa.String(50)))
    op.add_column('usuarios', sa.Column('apellido', sa.String(50)))

    # 2. Migrar datos (requiere conexión a la BD)
    connection = op.get_bind()
    connection.execute(sa.text("""
        UPDATE usuarios
        SET
            nombre = SUBSTRING_INDEX(nombre_completo, ' ', 1),
            apellido = SUBSTRING_INDEX(nombre_completo, ' ', -1)
    """))

    # 3. Eliminar columna vieja
    op.drop_column('usuarios', 'nombre_completo')


def downgrade() -> None:
    # Reversible: Reconstruir nombre_completo
    op.add_column('usuarios', sa.Column('nombre_completo', sa.String(100)))

    connection = op.get_bind()
    connection.execute(sa.text("""
        UPDATE usuarios
        SET nombre_completo = CONCAT(nombre, ' ', apellido)
    """))

    op.drop_column('usuarios', 'nombre')
    op.drop_column('usuarios', 'apellido')
```

**⚠️ Advertencia**: Data migrations pueden ser **lentas** en tablas grandes.

### 2. Migrations en producción (zero-downtime)

**Problema**: Agregar una columna NOT NULL rompe aplicaciones viejas.

**Solución**: Multi-step migration

```python
# Migration 1: Agregar columna como NULLABLE
def upgrade():
    op.add_column('tareas', sa.Column('prioridad', sa.Integer(), nullable=True))

# Deploy código que usa 'prioridad' (con default)

# Migration 2: Rellenar valores NULL
def upgrade():
    connection = op.get_bind()
    connection.execute(sa.text("UPDATE tareas SET prioridad = 2 WHERE prioridad IS NULL"))

# Migration 3: Hacer columna NOT NULL
def upgrade():
    op.alter_column('tareas', 'prioridad', nullable=False)
```

**Por qué funciona**:
- Aplicaciones viejas siguen funcionando (columna nullable)
- Aplicaciones nuevas usan la columna
- Deploy gradual sin downtime

### 3. Branching y merging de migrations

**Problema**: Dos desarrolladores crean migrations al mismo tiempo.

```
main: ... → migration_A
              ↓
           migration_B (dev1)
              ↓
           migration_C (dev2)  ← Ambas apuntan a migration_A
```

**Solución**: Merge con `alembic merge`

```bash
# Detectar branches
alembic branches

# Crear migration de merge
alembic merge -m "merge branches" migration_B migration_C
```

Genera:

```python
revision = 'xxx'
down_revision = ('migration_B', 'migration_C')  # ← Tuple de múltiples padres
```

### 4. Rollback Strategies

**Pregunta clave**: ¿Cómo revertir cambios sin perder datos?

**Estrategia 1**: Soft rollback (agregar columna `deleted_at`)

```python
# En lugar de DROP TABLE, soft delete
def downgrade():
    op.add_column('tareas', sa.Column('deleted_at', sa.DateTime()))
    connection = op.get_bind()
    connection.execute(sa.text("UPDATE tareas SET deleted_at = NOW()"))
```

**Estrategia 2**: Backup antes de migration

```bash
# PostgreSQL
pg_dump -Fc mi_bd > backup_antes_de_migration.dump

# Aplicar migration
alembic upgrade head

# Si algo sale mal:
pg_restore -d mi_bd backup_antes_de_migration.dump
```

**Estrategia 3**: Blue-Green Deployment

1. Crear nueva BD (green) con migrations aplicadas
2. Migrar datos de BD vieja (blue) a nueva
3. Switch de aplicación a nueva BD
4. Si algo sale mal, switch de vuelta a BD vieja

### 5. Migrations y CI/CD

**En GitHub Actions**:

```yaml
# .github/workflows/ci.yml
- name: Run migrations en CI
  run: |
    alembic upgrade head

- name: Run tests
  run: pytest

- name: Rollback después de tests
  run: alembic downgrade base
```

**En producción** (con verificación):

```bash
# 1. Backup
pg_dump -Fc mi_bd > backup.dump

# 2. Aplicar en staging primero
alembic -c alembic_staging.ini upgrade head

# 3. Validar
pytest tests_integrations/

# 4. Aplicar en producción
alembic -c alembic_prod.ini upgrade head

# 5. Monitorear
# (Si algo falla, rollback)
alembic -c alembic_prod.ini downgrade -1
```

### 6. Índices y Performance

**¿Cuándo agregar índices en migrations?**

Los índices mejoran la velocidad de las queries, pero tienen trade-offs:

✅ **Casos para indexar**:
- **Foreign keys**: Casi siempre (mejora JOIN performance)
- **Campos en WHERE frecuentes**: `WHERE user_id = 5`, `WHERE status = 'active'`
- **Campos en ORDER BY**: `ORDER BY created_at DESC`
- **Campos únicos**: `UNIQUE(email)` automáticamente crea índice

❌ **Casos para NO indexar**:
- **Baja cardinalidad**: Boolean (solo 2 valores), `prioridad` con 3 valores
- **Tablas pequeñas**: <1000 rows no necesitan índices
- **Campos que nunca se filtran**: Campos solo de display
- **Write-heavy tables**: Cada índice ralentiza INSERT/UPDATE

**Ejemplo**: Agregar índice en un campo de fecha

```python
# alembic/versions/xxx_add_index_created_at.py
def upgrade() -> None:
    """Agregar índice en created_at para ordenamiento rápido."""
    op.create_index(
        'ix_tareas_creado_en',
        'tareas',
        ['creado_en'],
        unique=False
    )


def downgrade() -> None:
    """Remover índice."""
    op.drop_index('ix_tareas_creado_en', table_name='tareas')
```

**Medir impacto** (PostgreSQL):

```sql
-- Sin índice
EXPLAIN ANALYZE SELECT * FROM tareas ORDER BY creado_en DESC LIMIT 10;
-- Resultado: Seq Scan + Sort (SLOW en tablas grandes)

-- Con índice
EXPLAIN ANALYZE SELECT * FROM tareas ORDER BY creado_en DESC LIMIT 10;
-- Resultado: Index Scan using ix_tareas_creado_en (FAST)
```

**Índices compuestos** (múltiples columnas):

```python
# Útil si filtras por usuario Y estado frecuentemente
op.create_index(
    'ix_tareas_usuario_estado',
    'tareas',
    ['usuario_id', 'completada']
)

# Query optimizada:
# SELECT * FROM tareas WHERE usuario_id = 5 AND completada = False
```

**Trade-offs de índices**:

| Aspecto | Sin Índice | Con Índice |
|---------|------------|------------|
| SELECT (WHERE, ORDER BY) | 🐌 Lento (Full Table Scan) | ⚡ Rápido (Index Scan) |
| INSERT | ⚡ Rápido | 🐌 Más lento (actualizar índice) |
| UPDATE | ⚡ Rápido | 🐌 Más lento (si se modifica columna indexada) |
| Espacio en disco | ✅ Poco | ⚠️ Más (índice ocupa espacio) |

**Regla general**: Indexa cuando las queries de lectura son **10x más frecuentes** que writes.

---

## 🧪 Ejercicios prácticos

### Ejercicio 1: Agregar índice para búsquedas

**Objetivo**: Optimizar búsquedas por nombre agregando un índice.

**Pasos**:
1. Crear migration: `alembic revision -m "agregar indice en nombre"`
2. Editar migration:
   ```python
   def upgrade():
       op.create_index('idx_tareas_nombre', 'tareas', ['nombre'])

   def downgrade():
       op.drop_index('idx_tareas_nombre', 'tareas')
   ```
3. Aplicar: `alembic upgrade head`
4. Verificar: `sqlite3 tareas.db ".indexes tareas"`

**Prompt IA para ayuda**:
```
¿Cuándo debería agregar índices en una tabla?
¿Qué campos de 'tareas' (id, nombre, completada, prioridad) deberían tener índice?
¿Hay algún costo de rendimiento en los índices?
```

### Ejercicio 2: Agregar columna con valor por defecto

**Objetivo**: Agregar campo `descripcion` con valor por defecto.

**Pasos**:
1. Modificar modelo:
   ```python
   descripcion: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
   ```
2. Generar migration: `alembic revision --autogenerate -m "agregar descripcion"`
3. Editar migration para agregar default:
   ```python
   def upgrade():
       op.add_column('tareas',
           sa.Column('descripcion', sa.String(500),
                     server_default='Sin descripción', nullable=True))
   ```
4. Aplicar
5. Verificar que tareas existentes tienen "Sin descripción"

**Prompt IA**:
```
¿Cuál es la diferencia entre `default` y `server_default` en SQLAlchemy?
¿Cuándo debería usar cada uno?
```

### Ejercicio 3: Renombrar columna

**Objetivo**: Renombrar `completada` a `finalizada`.

**Pasos**:
1. Crear migration manual (no usar autogenerate):
   ```python
   def upgrade():
       op.alter_column('tareas', 'completada', new_column_name='finalizada')

   def downgrade():
       op.alter_column('tareas', 'finalizada', new_column_name='completada')
   ```
2. Aplicar
3. Actualizar modelo y código

**⚠️ Advertencia**: Renombrar columnas puede romper aplicaciones en producción.

**Prompt IA**:
```
¿Cómo renombrar una columna sin downtime en producción?
¿Debería hacerlo en una sola migration o varias?
```

### Ejercicio 4: Data migration (transformar datos)

**Objetivo**: Convertir `prioridad` (int) a `prioridad_texto` (string).

**Pasos**:
1. Crear migration:
   ```python
   def upgrade():
       # 1. Agregar columna nueva
       op.add_column('tareas', sa.Column('prioridad_texto', sa.String(10)))

       # 2. Migrar datos
       connection = op.get_bind()
       connection.execute(sa.text("""
           UPDATE tareas SET prioridad_texto =
               CASE prioridad
                   WHEN 1 THEN 'baja'
                   WHEN 2 THEN 'media'
                   WHEN 3 THEN 'alta'
                   ELSE 'media'
               END
       """))

       # 3. Eliminar columna vieja
       op.drop_column('tareas', 'prioridad')
   ```
2. Aplicar
3. Verificar

**Prompt IA**:
```
¿Cómo validar que la data migration no perdió datos?
¿Qué pasa si hay valores de prioridad inesperados (ej: 99)?
```

### Ejercicio 5: Rollback completo

**Objetivo**: Practicar rollback de múltiples migrations.

**Pasos**:
1. Ver historial: `alembic history`
2. Retroceder 3 migrations: `alembic downgrade -3`
3. Verificar que el schema volvió al estado anterior
4. Volver a aplicar: `alembic upgrade head`

**Prompt IA**:
```
¿En qué situaciones debería hacer rollback en producción?
¿Cuáles son los riesgos de un rollback?
```

### Ejercicio 6: Migración Peligrosa (Avanzado)

**Objetivo**: Aprender a migrar datos existentes de forma segura en producción.

**Escenario**:
Tienes 1000 tareas en producción. Necesitas añadir un campo `categoria` (NOT NULL, no puede ser vacío).

**Pasos**:

**Parte 1: Reproducir el problema**

1. Crear 100 tareas usando la API o directamente en la BD:
   ```python
   # Script para generar datos de prueba
   from api.models import TareaModel
   from api.database import SessionLocal

   db = SessionLocal()
   for i in range(100):
       tarea = TareaModel(nombre=f"Tarea {i}", completada=False, prioridad=2)
       db.add(tarea)
   db.commit()
   ```

2. Genera una migración INCORRECTA (automática):
   ```bash
   # Modificar models.py primero
   categoria: Mapped[str] = mapped_column(String(50), nullable=False)

   # Generar migration
   alembic revision --autogenerate -m "agregar categoria NOT NULL"
   ```

3. Intenta aplicarla:
   ```bash
   alembic upgrade head
   ```

4. **Observa el error**:
   ```
   sqlalchemy.exc.IntegrityError: NOT NULL constraint failed: tareas.categoria
   ```

**Parte 2: Solución correcta (2 migrations)**

**Migration 1**: Agregar columna NULLABLE con default

```python
# alembic/versions/xxx_agregar_categoria_step1.py
def upgrade() -> None:
    """Paso 1: Agregar columna nullable con default."""
    op.add_column(
        'tareas',
        sa.Column('categoria', sa.String(50), nullable=True, server_default='General')
    )

    # Poblar datos existentes (redundante con server_default, pero educativo)
    op.execute("UPDATE tareas SET categoria = 'General' WHERE categoria IS NULL")


def downgrade() -> None:
    """Paso 1 rollback: Eliminar columna."""
    op.drop_column('tareas', 'categoria')
```

**Migration 2**: Hacer NOT NULL (ahora es seguro)

```python
# alembic/versions/yyy_agregar_categoria_step2.py
def upgrade() -> None:
    """Paso 2: Hacer columna NOT NULL (datos ya poblados)."""
    # Quitar default server-side (opcional)
    op.alter_column('tareas', 'categoria', server_default=None)

    # Hacer NOT NULL (seguro porque todos los rows tienen valor)
    op.alter_column('tareas', 'categoria', nullable=False)


def downgrade() -> None:
    """Paso 2 rollback: Volver a nullable."""
    op.alter_column('tareas', 'categoria', nullable=True)
    op.alter_column('tareas', 'categoria', server_default='General')
```

5. Aplicar ambas migrations:
   ```bash
   alembic upgrade head
   ```

6. Verificar que las tareas existentes tienen `categoria = 'General'`:
   ```python
   from api.database import SessionLocal
   from api.models import TareaModel

   db = SessionLocal()
   tareas = db.query(TareaModel).limit(10).all()
   for t in tareas:
       print(f"{t.id}: {t.nombre} - {t.categoria}")
   ```

**Parte 3: Validación**

7. Crear una tarea nueva (debe tener categoria por defecto en el modelo):
   ```python
   nueva = TareaModel(nombre="Tarea nueva", completada=False, prioridad=1)
   db.add(nueva)
   db.commit()
   # Verificar que categoria NO es NULL
   ```

8. Hacer rollback de ambas migrations y verificar que los datos no se perdieron:
   ```bash
   alembic downgrade -2
   alembic upgrade head
   ```

**Prompt IA para ayuda**:
```
Tengo una tabla 'tareas' con 10,000 rows en producción.
Necesito agregar un campo 'categoria' (NOT NULL, string).

¿Cuál es la estrategia más segura?
¿Debería hacerlo en 1, 2 o 3 migrations?
¿Qué pasa si la aplicación está corriendo mientras hago la migration?
```

**Aprendizajes clave**:
- ✅ Nunca añadas columnas NOT NULL directamente en tablas con datos
- ✅ Usa estrategia de 2 pasos: nullable → poblar → not null
- ✅ `server_default` asegura que rows nuevos tengan valor
- ✅ Siempre prueba la migration con datos de prueba primero

---

## 📦 Proyecto final: Migrar de Clase 3 a Clase 4

### Objetivo

Migrar la aplicación de Clase 3 (que usa `create_all()`) a Clase 4 (con Alembic).

### Requisitos

1. **Sin pérdida de datos**: Los datos de `tareas.db` deben preservarse
2. **Sin cambios en la API**: Los endpoints funcionan igual
3. **Migrations aplicadas**: Todo el schema debe estar en migrations
4. **Tests deben pasar**: Todos los tests existentes deben seguir funcionando
5. **Documentación**: Documenta el proceso de migración

### Pasos sugeridos

**Paso 1: Setup de Alembic (ya lo hiciste)**

**Paso 2: Generar migration inicial desde BD existente**

```bash
# 1. Backup de la BD actual
cp ../Clase\ 3\ -\ Base\ de\ Datos\ con\ SQLAlchemy/tareas.db ./tareas_backup.db

# 2. Copiar BD a tu proyecto
cp ../Clase\ 3\ -\ Base\ de\ Datos\ con\ SQLAlchemy/tareas.db ./tareas.db

# 3. Generar migration que refleje el estado actual
alembic revision --autogenerate -m "estado inicial desde Clase 3"

# 4. Marcar como aplicada (porque la tabla ya existe)
alembic stamp head
```

**Explicación de `alembic stamp head`**:
- Le dice a Alembic que la BD ya está en el estado "head"
- No aplica ninguna migration
- Solo actualiza la tabla `alembic_version`

**Paso 3: Eliminar `crear_tablas()` de `database.py`**

```python
# api/database.py
# ANTES:
def crear_tablas():
    Base.metadata.create_all(bind=engine)

# DESPUÉS:
# ¡Esta función ya no es necesaria!
# Usa: alembic upgrade head
```

**Paso 4: Actualizar `api.py` (lifespan events)**

```python
# api/api.py
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    print("🚀 Iniciando aplicación...")
    # Ya NO llamamos a crear_tablas()
    # En producción, Alembic se ejecuta ANTES del deploy
    yield
    # SHUTDOWN
    print("🛑 Cerrando aplicación...")


app = FastAPI(lifespan=lifespan)
```

**Paso 5: Validar**

```bash
# 1. Correr tests
pytest tests/ -v

# 2. Probar API
uvicorn api.api:app --reload
curl http://localhost:8000/tareas

# 3. Verificar migrations
alembic history
alembic current
```

**Paso 6: Agregar una nueva feature con migration**

Ahora, agrega un campo nuevo (ej: `descripcion`) usando el workflow de Alembic:

```bash
# 1. Modificar modelo
# api/models.py: agregar campo descripcion

# 2. Generar migration
alembic revision --autogenerate -m "agregar descripcion"

# 3. Revisar migration generada
cat alembic/versions/xxx_agregar_descripcion.py

# 4. Aplicar
alembic upgrade head

# 5. Actualizar código y tests
```

### Prompt IA para el proyecto

```
Tengo una aplicación FastAPI con SQLAlchemy que usa `create_all()` para crear tablas.
Quiero migrar a Alembic sin perder datos existentes.

Mi situación:
- BD SQLite con datos en producción
- Tabla 'tareas' con 1000 filas
- No puedo tener downtime

¿Cuál es el proceso seguro paso a paso?
¿Cómo genero la migration inicial sin que intente crear la tabla de nuevo?
¿Qué hago con `create_all()` en el código existente?
```

---

## 🔧 Troubleshooting: Errores Comunes

### Error 1: "Target database is not up to date"

**Mensaje completo**:
```
alembic.util.exc.CommandError: Target database is not up to date.
```

**Causa**: Hay migrations pendientes de aplicar.

**Solución**:
```bash
# Ver migration actual
alembic current

# Ver migrations pendientes
alembic history

# Aplicar todas las migrations
alembic upgrade head
```

---

### Error 2: "Can't locate revision identified by 'xxxxx'"

**Mensaje completo**:
```
alembic.util.exc.CommandError: Can't locate revision identified by '58cbce442bf6'
```

**Causa**:
- La BD tiene una versión que no existe en tus archivos de migration
- Alguien más creó migrations que no has descargado

**Solución 1** (trabajando en equipo):
```bash
# Descargar migrations nuevas
git pull origin dev

# Aplicar
alembic upgrade head
```

**Solución 2** (BD corrupta o migration eliminada):
```bash
# Ver versión actual en la BD
alembic current

# Si la migration no existe, hacer stamp manual (¡CUIDADO!)
alembic stamp head

# O stamp a una versión específica que SÍ exista
alembic stamp 58cbce442bf6
```

⚠️ **Advertencia**: `alembic stamp` no aplica ni revierte migrations, solo actualiza el registro. Úsalo con cuidado.

---

### Error 3: "FAILED: Multiple head revisions are present"

**Mensaje completo**:
```
alembic.util.exc.CommandError: Multiple head revisions are present for given argument 'head'; please specify a specific target revision, <branchname>@head, or pass --resolve-dependencies
```

**Causa**: Dos migrations apuntan al mismo `down_revision` (branches en el historial).

**Ejemplo**:
```
main: ... → migration_A
              ↓
           migration_B (dev1)
              ↓
           migration_C (dev2)  ← Ambas apuntan a migration_A
```

**Solución**: Merge de branches con `alembic merge`

```bash
# Ver branches
alembic branches

# Output:
# 05702ef4b618 (dev1) -> migration_B
# 1234567890ab (dev2) -> migration_C

# Crear migration de merge
alembic merge -m "merge branches" 05702ef4b618 1234567890ab

# Aplicar
alembic upgrade head
```

La migration de merge generada:
```python
revision = 'abc123'
down_revision = ('05702ef4b618', '1234567890ab')  # ← Tuple de múltiples padres
```

---

### Error 4: "Column 'x' cannot be null" (IntegrityError)

**Mensaje completo**:
```
sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: tareas.prioridad
```

**Causa**: Migration añade columna NOT NULL en una tabla con datos existentes.

**Solución**: Ver **Ejercicio 6: Migración Peligrosa** (arriba).

Estrategia correcta:
1. Migration 1: ADD COLUMN nullable con default
2. Migration 2: Poblar datos existentes
3. Migration 3: ALTER COLUMN a NOT NULL

---

### Error 5: "Table 'tareas' already exists"

**Mensaje completo**:
```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) table tareas already exists
```

**Causa**:
- Ejecutaste `alembic upgrade head` pero la tabla ya existía (creada con `create_all()`)
- La BD está out-of-sync con Alembic

**Solución 1** (BD creada con create_all, quieres usar Alembic):
```bash
# Marcar la BD como si estuviera en la última migration (sin ejecutarla)
alembic stamp head

# Ahora Alembic sabe que la BD está actualizada
```

**Solución 2** (empezar desde cero):
```bash
# Eliminar BD
rm tareas.db

# Aplicar migrations desde cero
alembic upgrade head
```

---

### Error 6: "No module named 'api.models'"

**Mensaje completo**:
```
ModuleNotFoundError: No module named 'api.models'
```

**Causa**: Alembic no puede importar tus modelos porque el `PYTHONPATH` no está configurado.

**Solución**: En `alembic.ini`, asegúrate de tener:
```ini
prepend_sys_path = .
```

Y en `alembic/env.py`:
```python
# Al inicio del archivo
import sys
from pathlib import Path

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Ahora sí importar
from api.models import Base
```

---

### Error 7: "Downgrade doesn't work" (rollback falla)

**Causa**: La función `downgrade()` no revierte correctamente el `upgrade()`.

**Ejemplo de migration incorrecta**:
```python
def upgrade():
    op.add_column('tareas', sa.Column('nueva', sa.String(50)))
    op.execute("UPDATE tareas SET nueva = 'valor'")

def downgrade():
    op.drop_column('tareas', 'nueva')
    # ⚠️ FALTA: No revierte el UPDATE
```

**Solución**: Asegúrate de que `downgrade()` deshace **TODO** lo que hace `upgrade()`:
```python
def upgrade():
    op.add_column('tareas', sa.Column('nueva', sa.String(50)))
    op.execute("UPDATE tareas SET nueva = nombre")  # Copiar desde otro campo

def downgrade():
    # Revertir el UPDATE copiando de vuelta (si es posible)
    op.execute("UPDATE tareas SET nombre = nueva WHERE nueva IS NOT NULL")
    # Eliminar columna
    op.drop_column('tareas', 'nueva')
```

---

### Tips Generales de Troubleshooting

1. **Ver estado actual**:
   ```bash
   alembic current          # Versión actual
   alembic history          # Historial completo
   alembic show head        # Última migration disponible
   ```

2. **Generar SQL sin ejecutar** (modo offline):
   ```bash
   alembic upgrade head --sql > migration.sql
   # Revisar SQL antes de aplicar
   ```

3. **Logs detallados**:
   ```bash
   # En alembic.ini, cambiar log level
   [logger_alembic]
   level = DEBUG  # En lugar de INFO
   ```

4. **Validar migration antes de aplicar**:
   ```bash
   # Hacer upgrade y downgrade en BD de prueba
   alembic upgrade +1
   alembic downgrade -1
   alembic upgrade head
   ```

5. **Backup SIEMPRE antes de migrations en producción**:
   ```bash
   # SQLite
   cp tareas.db tareas.db.backup

   # PostgreSQL
   pg_dump -Fc mi_bd > backup_$(date +%Y%m%d_%H%M%S).dump
   ```

---

## ✅ Checklist de la Clase 4

### Fundamentos (obligatorio)

- [ ] Entiendes por qué `create_all()` no funciona en producción
- [ ] Instalaste y configuraste Alembic
- [ ] Generaste migrations automáticamente con `--autogenerate`
- [ ] Aplicaste migrations con `upgrade` y `downgrade`
- [ ] Entiendes la cadena de migrations (`down_revision`)
- [ ] Revisaste manualmente las migrations generadas
- [ ] Todos los tests pasan

### Conceptos avanzados (opcional)

- [ ] Creaste una data migration (transformar datos)
- [ ] Implementaste una migration en múltiples pasos (zero-downtime)
- [ ] Agregaste índices con migrations
- [ ] Practicaste rollback de múltiples migrations
- [ ] Usaste `alembic stamp` para marcar BD existente

### Integración con IA (40% del contenido)

- [ ] Usaste IA para generar migrations complejas
- [ ] Validaste migrations con IA (revisión de seguridad)
- [ ] IA te ayudó con data migrations
- [ ] Generaste rollback strategies con IA
- [ ] Documentaste qué prompts funcionaron mejor

### Validación con Agentes Educativos

**Database ORM Specialist**:
- [ ] Validaste migraciones antes de aplicar en producción
- [ ] Agent detectó migraciones peligrosas (NOT NULL en tablas con datos)
- [ ] Verificaste backward compatibility de migrations
- [ ] Revisaste que downgrade funciona correctamente
- [ ] Agent validó data migrations sin pérdida de datos

**Python Best Practices Coach**:
- [ ] Código de migrations tiene type hints completos
- [ ] Migrations tienen docstrings descriptivos
- [ ] Nombres de columnas son descriptivos y consistentes
- [ ] Manejo de errores en data migrations con RuntimeError

---

## 🎯 Conceptos clave para recordar

1. **Alembic es Git para tu base de datos**: Versiona schema, no código
2. **Siempre revisa migrations autogeneradas**: IA puede equivocarse
3. **Migrations son código**: Van en control de versiones (Git)
4. **Downgrade debe funcionar**: Practica rollback antes de producción
5. **Zero-downtime requiere multi-step**: No hagas cambios destructivos en un solo paso
6. **Data migrations son peligrosas**: Valida con datos de prueba primero

---

## 📖 Recursos adicionales

**Documentación oficial**:
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Alembic + FastAPI](https://fastapi.tiangolo.com/tutorial/sql-databases/#alembic-note)

**Tutoriales recomendados**:
- Alembic Autogenerate Explained
- Zero-Downtime Database Migrations
- Data Migrations Best Practices

**Herramientas útiles**:
- Alembic + Docker (migrations en CI/CD)
- pgAdmin (visualizar migrations en PostgreSQL)
- Alembic Branches and Merging

---

## 🚀 Próxima clase

**Clase 5: Deployment en la nube**

En la próxima clase aprenderás:
- Deployar tu API a un servicio cloud (Railway, Render, Heroku)
- Configurar base de datos PostgreSQL en producción
- Ejecutar migrations en producción de forma segura
- Monitoreo y logs en producción
- CI/CD completo con GitHub Actions

---

**¡Felicitaciones!** Ahora dominas migraciones de base de datos con Alembic. Tu aplicación está lista para producción 🚀
