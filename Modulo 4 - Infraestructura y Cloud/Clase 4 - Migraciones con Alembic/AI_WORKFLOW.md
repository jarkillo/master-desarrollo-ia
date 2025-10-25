# AI Workflow - Clase 4: Migraciones Seguras con Alembic + IA

## 🎯 Objetivos de Aprendizaje con IA

En esta clase aprenderás a usar IA como asistente para:

1. **Generar migrations automáticamente** con contexto y validación
2. **Detectar migraciones peligrosas** antes de aplicarlas en producción
3. **Solucionar conflictos** de migrations (multiple heads, branches)
4. **Crear data migrations seguras** sin pérdida de datos
5. **Validar backward compatibility** usando agentes especializados

---

## 🔄 Workflow Completo: De Modelo a Migration Segura

### Fase 1: Generación Automática de Migrations con IA

**Contexto**: Modificaste un modelo SQLAlchemy y necesitas generar la migration de Alembic, pero quieres asegurarte de que sea segura y completa.

#### Prompt 1: Generar migration para nuevo campo

```
Rol: Database migration specialist con experiencia en Alembic y SQLAlchemy 2.0
Contexto: Tengo un modelo TareaModel con (id, nombre, completada, prioridad, creado_en, actualizado_en)
Objetivo: Agregar campo 'descripcion' (Optional[str], max 500 caracteres)
Restricciones:
- La tabla tiene 1000 filas en producción (NO puede fallar)
- Debe ser backward-compatible (aplicaciones viejas deben seguir funcionando)
- Migration debe ser reversible (downgrade completo)
- SQLite en desarrollo, PostgreSQL en producción

Entrega:
- Código de la migration con upgrade() y downgrade()
- Explicación de por qué es seguro aplicarla en producción
- Estrategia de rollback si algo sale mal
```

**Resultado esperado**:

```python
# alembic/versions/xxx_agregar_descripcion.py
"""agregar descripcion a tareas

Revision ID: abc123def456
Revises: previous_revision
Create Date: 2025-10-25 12:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'abc123def456'
down_revision: Union[str, Sequence[str], None] = 'previous_revision'


def upgrade() -> None:
    """Agregar campo descripcion (NULLABLE, seguro para producción)."""
    # ✅ NULLABLE = seguro para datos existentes
    # ✅ server_default = NULL explícito (no rompe nada)
    op.add_column(
        'tareas',
        sa.Column(
            'descripcion',
            sa.String(length=500),
            nullable=True,  # ← CRÍTICO: Permite NULL en filas existentes
            comment='Descripción detallada de la tarea'
        )
    )


def downgrade() -> None:
    """Revertir: eliminar campo descripcion (sin pérdida de datos críticos)."""
    # ⚠️ Advertencia: Eliminar columna PIERDE datos
    # En producción, considera soft-delete o backup antes
    op.drop_column('tareas', 'descripcion')
```

**Por qué es seguro**:
- ✅ `nullable=True`: Filas existentes no fallan (tienen NULL automáticamente)
- ✅ Sin `server_default`: No fuerza valores en filas viejas
- ✅ `downgrade()` funciona: Puede revertirse
- ⚠️ **Pero**: Al revertir, los datos de `descripcion` se pierden (documentar)

#### Validación con Database ORM Specialist

Después de generar la migration, usa el agente educativo:

```bash
# Invocar Database ORM Specialist agent
# El agente revisará:
# ✓ La migration es backward-compatible
# ✓ No causa pérdida de datos críticos
# ✓ El downgrade funciona correctamente
# ✓ No hay locks largos en tablas grandes
# ✓ Nombres de columnas son descriptivos
```

---

### Fase 2: Migrations Peligrosas - Detección y Prevención

**Problema**: Quieres agregar un campo NOT NULL en una tabla con datos existentes.

#### Prompt 2: Migración segura en múltiples pasos

```
Rol: Senior database engineer especializado en zero-downtime deployments
Contexto: Tabla 'tareas' con 10,000 filas en producción (PostgreSQL 14)
Objetivo: Agregar campo 'categoria' (String, NOT NULL, no puede estar vacío)
Restricciones:
- CERO downtime (aplicación corriendo durante migration)
- NO bloquear tabla (o bloqueo < 100ms)
- Aplicación tiene múltiples instancias (blue-green deployment)
- Migration debe ser reversible

Entrega:
- Estrategia de migration multi-paso (2-3 migrations)
- Código de cada migration
- Explicación de por qué evita downtime
- Plan de rollback si falla en producción
```

**Resultado esperado (IA genera estrategia de 3 pasos)**:

```
Estrategia: Migration en 3 fases (zero-downtime)

Fase 1: Agregar columna NULLABLE con default (safe)
- Migration 1: ADD COLUMN categoria (nullable=True, server_default='General')
- Código actualizado: Modelos usan categoria (con default='General')
- Deploy gradual de código nuevo
- Resultado: Apps viejas ignoran columna, apps nuevas la usan

Fase 2: Poblar datos existentes (data migration)
- Migration 2: UPDATE todas las filas con categoria=NULL → 'General'
- Sin bloqueos (UPDATE en lotes de 1000 filas)
- Resultado: Todas las filas tienen valor válido

Fase 3: Hacer NOT NULL (seguro ahora)
- Migration 3: ALTER COLUMN categoria SET NOT NULL
- Quitar server_default (ya no necesario)
- Resultado: Constraint aplicado, datos validados
```

**Implementación de las 3 migrations**:

**Migration 1: Agregar columna nullable**

```python
# alembic/versions/xxx_add_categoria_step1.py
"""agregar categoria (paso 1 de 3: nullable)

Revision ID: step1_categoria
Revises: abc123def456
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'step1_categoria'
down_revision: Union[str, Sequence[str], None] = 'abc123def456'


def upgrade() -> None:
    """Paso 1: Agregar columna nullable con default server-side."""
    op.add_column(
        'tareas',
        sa.Column(
            'categoria',
            sa.String(length=50),
            nullable=True,  # ← Seguro para filas existentes
            server_default='General',  # ← Filas NUEVAS tienen valor automático
            comment='Categoría de la tarea'
        )
    )


def downgrade() -> None:
    """Paso 1 rollback: Eliminar columna."""
    op.drop_column('tareas', 'categoria')
```

**Migration 2: Poblar datos existentes**

```python
# alembic/versions/yyy_add_categoria_step2.py
"""poblar categoria en filas existentes (paso 2 de 3)

Revision ID: step2_categoria
Revises: step1_categoria
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'step2_categoria'
down_revision: Union[str, Sequence[str], None] = 'step1_categoria'


def upgrade() -> None:
    """Paso 2: Poblar categoria en filas NULL (data migration)."""
    # Poblar filas existentes que tienen NULL
    # (Redundante con server_default, pero asegura consistencia)
    connection = op.get_bind()

    # ✅ Usar batches para evitar locks largos en tablas grandes
    connection.execute(
        sa.text("UPDATE tareas SET categoria = 'General' WHERE categoria IS NULL")
    )


def downgrade() -> None:
    """Paso 2 rollback: Volver a NULL (reversible)."""
    connection = op.get_bind()
    # Opcional: Puedes dejar los valores o ponerlos NULL de nuevo
    # connection.execute(sa.text("UPDATE tareas SET categoria = NULL"))
    pass  # No es crítico revertir esto
```

**Migration 3: Hacer NOT NULL**

```python
# alembic/versions/zzz_add_categoria_step3.py
"""hacer categoria NOT NULL (paso 3 de 3)

Revision ID: step3_categoria
Revises: step2_categoria
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'step3_categoria'
down_revision: Union[str, Sequence[str], None] = 'step2_categoria'


def upgrade() -> None:
    """Paso 3: Hacer columna NOT NULL (seguro ahora, datos poblados)."""
    # Quitar server_default (ya no necesario, modelo Python tiene default)
    op.alter_column('tareas', 'categoria', server_default=None)

    # Hacer NOT NULL (seguro porque todas las filas tienen valor)
    op.alter_column('tareas', 'categoria', nullable=False)


def downgrade() -> None:
    """Paso 3 rollback: Volver a nullable."""
    # Revertir a nullable
    op.alter_column('tareas', 'categoria', nullable=True)

    # Restaurar server_default
    op.alter_column('tareas', 'categoria', server_default='General')
```

**Por qué funciona**:
- ✅ **Paso 1**: Apps viejas no rompen (columna nullable)
- ✅ **Paso 2**: Datos consistentes antes de constraint
- ✅ **Paso 3**: Constraint aplicado cuando es seguro
- ✅ **Cada paso es reversible**: Rollback granular
- ✅ **Sin downtime**: Deploy gradual entre migrations

#### Validación de Seguridad

Usa este prompt para validar la estrategia:

```
Acabo de generar estas 3 migrations para agregar campo NOT NULL:

[Pegar código de las 3 migrations]

Valida:
1. ¿Puede causar downtime o locks largos?
2. ¿Es seguro en tablas con millones de filas?
3. ¿Qué pasa si falla en el paso 2?
4. ¿El rollback de cada paso funciona?
5. ¿Debería hacer backup antes de aplicar?

Dame un checklist pre-deploy para producción.
```

---

### Fase 3: Data Migrations - Transformar Datos Existentes

**Problema**: Necesitas transformar datos durante una migration (ej: split de columnas, conversión de tipos).

#### Prompt 3: Data migration segura

```
Rol: Data migration specialist con experiencia en PostgreSQL y SQLite
Contexto: Tengo columna 'prioridad' (integer: 1, 2, 3) en tabla 'tareas'
Objetivo: Migrar a 'prioridad_texto' (string: "baja", "media", "alta")
Restricciones:
- Preservar datos existentes (10,000 filas)
- Manejar valores inesperados (ej: prioridad=99 → default a "media")
- Migration reversible (poder volver a integers)
- Validar que no queden NULL después de migración

Entrega:
- Migration con upgrade() y downgrade()
- Código SQL de transformación
- Estrategia para valores inconsistentes
- Tests de validación post-migration
```

**Resultado esperado**:

```python
# alembic/versions/xxx_prioridad_int_to_text.py
"""migrar prioridad de int a texto

Revision ID: prioridad_text
Revises: step3_categoria
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'prioridad_text'
down_revision: Union[str, Sequence[str], None] = 'step3_categoria'


def upgrade() -> None:
    """Transformar prioridad (int) → prioridad_texto (string)."""
    # Paso 1: Agregar columna nueva (nullable temporalmente)
    op.add_column(
        'tareas',
        sa.Column('prioridad_texto', sa.String(10), nullable=True)
    )

    # Paso 2: Data migration con manejo de valores inesperados
    connection = op.get_bind()
    connection.execute(sa.text("""
        UPDATE tareas
        SET prioridad_texto = CASE prioridad
            WHEN 1 THEN 'baja'
            WHEN 2 THEN 'media'
            WHEN 3 THEN 'alta'
            ELSE 'media'  -- ← Default para valores raros (99, NULL, etc.)
        END
    """))

    # Paso 3: Validar que no hay NULL (CRÍTICO)
    result = connection.execute(
        sa.text("SELECT COUNT(*) FROM tareas WHERE prioridad_texto IS NULL")
    )
    count_null = result.scalar()
    if count_null > 0:
        raise RuntimeError(
            f"Data migration falló: {count_null} filas con prioridad_texto NULL"
        )

    # Paso 4: Eliminar columna vieja (después de validar)
    op.drop_column('tareas', 'prioridad')

    # Paso 5: Renombrar columna nueva (opcional pero limpio)
    op.alter_column('tareas', 'prioridad_texto', new_column_name='prioridad')

    # Paso 6: Hacer NOT NULL (seguro ahora)
    op.alter_column('tareas', 'prioridad', nullable=False)


def downgrade() -> None:
    """Revertir: texto → int (con pérdida de granularidad)."""
    # Paso 1: Volver a nullable temporalmente
    op.alter_column('tareas', 'prioridad', nullable=True)

    # Paso 2: Renombrar actual a temp
    op.alter_column('tareas', 'prioridad', new_column_name='prioridad_texto')

    # Paso 3: Agregar columna int de nuevo
    op.add_column('tareas', sa.Column('prioridad', sa.Integer(), nullable=True))

    # Paso 4: Convertir texto → int
    connection = op.get_bind()
    connection.execute(sa.text("""
        UPDATE tareas
        SET prioridad = CASE prioridad_texto
            WHEN 'baja' THEN 1
            WHEN 'media' THEN 2
            WHEN 'alta' THEN 3
            ELSE 2  -- Default
        END
    """))

    # Paso 5: Eliminar columna texto
    op.drop_column('tareas', 'prioridad_texto')

    # Paso 6: Hacer NOT NULL
    op.alter_column('tareas', 'prioridad', nullable=False)
```

**Puntos clave de esta migration**:
- ✅ **Validación inline**: Falla rápido si hay NULL después de transformación
- ✅ **Manejo de edge cases**: Valores inesperados → default
- ✅ **Reversible**: downgrade funciona (aunque pierde granularidad)
- ⚠️ **Bloqueo**: UPDATE puede tardar en tablas grandes (considera batching)

#### Validación con IA

```
Validación post-migration de data transformation:

1. ¿Todos los valores se transformaron correctamente?
   SELECT prioridad_texto, COUNT(*) FROM tareas GROUP BY prioridad_texto;
   -- Esperado: solo 'baja', 'media', 'alta'

2. ¿Hay NULL?
   SELECT COUNT(*) FROM tareas WHERE prioridad IS NULL;
   -- Esperado: 0

3. ¿Hay valores inesperados?
   SELECT * FROM tareas WHERE prioridad NOT IN ('baja', 'media', 'alta');
   -- Esperado: empty

4. ¿El downgrade funciona?
   alembic downgrade -1
   alembic upgrade head
   -- Validar datos nuevamente
```

---

### Fase 4: Troubleshooting - Resolución de Conflictos

**Problema**: Multiple head revisions (dos migrations apuntan al mismo padre).

#### Prompt 4: Resolver conflicto de branches

```
Rol: Alembic troubleshooting specialist
Contexto: Dos developers crearon migrations simultáneamente
Error: "Multiple head revisions are present for given argument 'head'"
Situación:
- Developer A creó: "agregar_descripcion" (revision: abc123)
- Developer B creó: "agregar_categoria" (revision: def456)
- Ambas apuntan al mismo down_revision

Objetivo: Resolver el conflicto sin perder ninguna migration
Restricciones:
- Preservar historial de ambas migrations
- No reescribir migrations ya aplicadas en otros entornos
- Mantener reversibilidad completa

Entrega:
- Comando alembic para resolver
- Código de la merge migration
- Explicación del resultado
```

**Resultado esperado**:

```bash
# 1. Detectar el problema
$ alembic heads

abc123 (head)  # agregar_descripcion
def456 (head)  # agregar_categoria

# 2. Ver el conflicto
$ alembic upgrade head

CommandError: Multiple head revisions are present...

# 3. Resolver con merge
$ alembic merge abc123 def456 -m "merge descripcion y categoria"

Generating alembic/versions/merge_abc_def_merge.py ...  done
```

**Migration de merge generada**:

```python
# alembic/versions/merge_abc_def.py
"""merge descripcion y categoria

Revision ID: merge_abc_def
Revises: abc123, def456
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'merge_abc_def'
down_revision: Union[str, Sequence[str], None] = ('abc123', 'def456')  # ← Tuple


def upgrade() -> None:
    """Merge: no hace cambios (ambas migrations ya aplicadas)."""
    pass


def downgrade() -> None:
    """Revertir merge (vuelve a los dos heads)."""
    pass
```

**Explicación**:
- ✅ Crea un nuevo "head" que une ambas ramas
- ✅ No modifica el schema (solo estructura de versiones)
- ✅ `down_revision` es una tupla de múltiples padres
- ✅ Ahora `alembic upgrade head` funciona correctamente

**Historial después del merge**:

```
Antes:
    revision_0
       ├── abc123 (head A)
       └── def456 (head B)

Después:
    revision_0
       ├── abc123 ──┐
       └── def456 ──┴── merge_abc_def (head único)
```

---

### Fase 5: Production Rollback Strategies

**Problema**: Una migration falló en producción y necesitas revertir sin pérdida de datos.

#### Prompt 5: Estrategia de rollback segura

```
Rol: Production database specialist
Contexto: Migration aplicada en producción causó error 500 en API
Situación:
- Migration: "agregar índice en nombre" (revision: xyz789)
- Error: Timeout en queries (índice está corrupto)
- Aplicación está corriendo (usuarios activos)
- Necesito revertir AHORA

Objetivo: Rollback seguro sin downtime ni pérdida de datos
Restricciones:
- NO detener aplicación
- NO perder datos de usuarios
- Validar que rollback funciona antes de aplicar
- Tener plan B si rollback falla

Entrega:
- Checklist pre-rollback
- Comando de rollback
- Validación post-rollback
- Plan B (restaurar desde backup)
```

**Resultado esperado**:

```bash
# ===== CHECKLIST PRE-ROLLBACK =====

# 1. Backup INMEDIATO de la BD
pg_dump -Fc mi_bd > backup_pre_rollback_$(date +%Y%m%d_%H%M%S).dump

# 2. Ver migration actual
alembic current

# Output: xyz789 (head)  # ← Confirmar que es la migration problemática

# 3. Ver qué hace el downgrade (DRY RUN)
alembic downgrade -1 --sql > rollback_preview.sql
cat rollback_preview.sql  # Revisar SQL antes de ejecutar

# 4. Verificar que downgrade está implementado
# Leer el código de la migration: alembic/versions/xyz789_*.py
# ⚠️ Si downgrade() está vacío o mal implementado, NO hacer rollback

# ===== EJECUTAR ROLLBACK =====

# 5. Rollback a la revisión anterior
alembic downgrade -1

# 6. Verificar que aplicó correctamente
alembic current
# Output: previous_revision (debería ser la anterior a xyz789)

# ===== VALIDACIÓN POST-ROLLBACK =====

# 7. Validar que el índice se eliminó (PostgreSQL)
\d tareas
# No debería aparecer: ix_tareas_nombre

# 8. Probar queries problemáticas
curl http://localhost:8000/tareas?nombre=test
# Debería responder correctamente (aunque sin índice, más lento)

# 9. Verificar logs de la aplicación
tail -f /var/log/api.log
# No deberían aparecer errores 500

# ===== PLAN B (si rollback falla) =====

# 10. Restaurar desde backup (ÚLTIMO RECURSO)
pg_restore -d mi_bd -c backup_pre_rollback_20251025_120000.dump

# 11. Verificar datos post-restore
SELECT COUNT(*) FROM tareas;
# Debería coincidir con el count antes del rollback

# ===== POST-MORTEM =====

# 12. Investigar por qué falló la migration
# - ¿El índice era demasiado grande?
# - ¿Timeout en PostgreSQL configurado muy bajo?
# - ¿Faltó CREATE INDEX CONCURRENTLY? (evita locks)

# 13. Corregir la migration antes de reaplicar
# Ejemplo de fix:
def upgrade():
    # ✅ CONCURRENT evita lock de tabla completa
    op.create_index(
        'ix_tareas_nombre',
        'tareas',
        ['nombre'],
        postgresql_concurrently=True  # ← CLAVE para producción
    )
```

**Estrategia avanzada: Soft rollback**

Si no puedes hacer downgrade (riesgo de pérdida de datos), considera:

```python
# En lugar de DROP COLUMN, hacer soft delete
def downgrade():
    # ❌ NO hacer esto en producción:
    # op.drop_column('tareas', 'descripcion')

    # ✅ Hacer esto (soft delete):
    op.alter_column('tareas', 'descripcion', new_column_name='descripcion_deprecated')
    # Los datos se preservan, pero el modelo Python no los usa
```

---

## 🧪 Ejercicios Prácticos con IA

### Ejercicio 1: Generar Migration Automática con Validación (25 min)

**Objetivo**: Usar IA para generar migration y validarla con el Database ORM Specialist.

**Pasos**:

1. **Modificar modelo** (agregar campo `etiquetas` como JSON):
   ```python
   # api/models.py
   from sqlalchemy.dialects.postgresql import JSONB

   etiquetas: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
   ```

2. **Usar IA para generar la migration**:

   **Prompt**:
   ```
   Genera una migration de Alembic para agregar campo 'etiquetas' (JSON) a tabla 'tareas'.
   - SQLite en desarrollo (usar TEXT para JSON)
   - PostgreSQL en producción (usar JSONB)
   - Valor por defecto: {} (objeto vacío)
   - Migration reversible
   ```

3. **Validar con Database ORM Specialist**:
   - Revisar que maneja ambos dialectos (SQLite/PostgreSQL)
   - Validar que el default no rompe filas existentes
   - Verificar que downgrade funciona

4. **Aplicar y validar**:
   ```bash
   alembic upgrade head

   # Validar
   sqlite3 tareas.db "SELECT etiquetas FROM tareas LIMIT 5;"
   ```

**Criterios de aceptación**:
- [ ] Migration generada funciona en SQLite y PostgreSQL
- [ ] Filas existentes tienen `etiquetas = NULL` (no rompe)
- [ ] Downgrade elimina la columna correctamente
- [ ] Agent validó sin errores críticos

---

### Ejercicio 2: Migration Peligrosa - Estrategia Multi-Paso (35 min)

**Objetivo**: Implementar la estrategia de 3 pasos para agregar campo NOT NULL.

**Escenario**: Agregar campo `usuario_id` (foreign key, NOT NULL) a tabla 'tareas' con datos.

**Pasos**:

1. **Generar datos de prueba** (100 tareas):
   ```python
   from api.database import SessionLocal
   from api.models import TareaModel

   db = SessionLocal()
   for i in range(100):
       tarea = TareaModel(nombre=f"Tarea {i}", completada=False, prioridad=2)
       db.add(tarea)
   db.commit()
   ```

2. **Usar IA para diseñar estrategia**:

   **Prompt**:
   ```
   Necesito agregar campo 'usuario_id' (Integer, NOT NULL, FK a usuarios) en tabla 'tareas'.
   La tabla tiene 100 filas en producción.

   ¿Cuál es la estrategia más segura? (multi-paso)
   ¿Cómo evito "NOT NULL constraint failed"?
   ```

3. **Implementar las 3 migrations** (según respuesta IA):
   - Migration 1: ADD COLUMN nullable con default=1 (usuario admin)
   - Migration 2: Poblar usuario_id en filas NULL
   - Migration 3: Hacer NOT NULL y agregar FK

4. **Validar cada paso**:
   ```bash
   # Aplicar paso 1
   alembic upgrade +1
   sqlite3 tareas.db "SELECT COUNT(*) FROM tareas WHERE usuario_id IS NULL;"
   # Esperado: 0 (todas tienen default=1)

   # Aplicar paso 2
   alembic upgrade +1

   # Aplicar paso 3
   alembic upgrade +1
   ```

5. **Practicar rollback completo**:
   ```bash
   alembic downgrade -3
   alembic upgrade head
   ```

**Criterios de aceptación**:
- [ ] 3 migrations creadas siguiendo la estrategia
- [ ] No hay error "NOT NULL constraint failed"
- [ ] Rollback de las 3 funciona correctamente
- [ ] Datos se preservan en rollback

---

### Ejercicio 3: Data Migration - Transformación Compleja (40 min)

**Objetivo**: Transformar datos existentes usando CASE statements en SQL.

**Escenario**: Migrar `completada` (Boolean) a `estado` (String: "pendiente", "completada", "cancelada").

**Pasos**:

1. **Diseñar estrategia con IA**:

   **Prompt**:
   ```
   Tengo tabla 'tareas' con campo 'completada' (Boolean).
   Quiero migrar a 'estado' (String: "pendiente" | "completada" | "cancelada").

   Conversión:
   - completada = True → "completada"
   - completada = False → "pendiente"
   - DEFAULT para nuevas tareas → "pendiente"

   ¿Cómo hago la data migration de forma segura?
   ¿Qué hago con el downgrade (string → boolean)?
   ```

2. **Implementar migration según respuesta**:
   ```python
   def upgrade():
       # ADD COLUMN
       op.add_column('tareas', sa.Column('estado', sa.String(20), nullable=True))

       # DATA MIGRATION
       connection = op.get_bind()
       connection.execute(sa.text("""
           UPDATE tareas SET estado =
               CASE completada
                   WHEN 1 THEN 'completada'
                   WHEN 0 THEN 'pendiente'
                   ELSE 'pendiente'
               END
       """))

       # VALIDATE (no NULL)
       result = connection.execute(sa.text("SELECT COUNT(*) FROM tareas WHERE estado IS NULL"))
       if result.scalar() > 0:
           raise RuntimeError("Data migration failed: NULL values found")

       # DROP old column
       op.drop_column('tareas', 'completada')
   ```

3. **Validar transformación**:
   ```bash
   alembic upgrade head

   # Verificar que solo hay estados válidos
   sqlite3 tareas.db "SELECT DISTINCT estado FROM tareas;"
   # Esperado: pendiente, completada

   # Verificar counts
   sqlite3 tareas.db "SELECT estado, COUNT(*) FROM tareas GROUP BY estado;"
   ```

4. **Implementar downgrade reversible**:
   ```python
   def downgrade():
       # ADD COLUMN boolean
       op.add_column('tareas', sa.Column('completada', sa.Boolean(), nullable=True))

       # REVERSE TRANSFORMATION (con pérdida de "cancelada" → False)
       connection = op.get_bind()
       connection.execute(sa.text("""
           UPDATE tareas SET completada =
               CASE estado
                   WHEN 'completada' THEN 1
                   ELSE 0
               END
       """))

       # DROP estado column
       op.drop_column('tareas', 'estado')
   ```

**Criterios de aceptación**:
- [ ] Data migration transforma correctamente
- [ ] No hay NULL después de transformación
- [ ] Downgrade funciona (aunque pierde "cancelada")
- [ ] Validación inline falla si hay errores

---

### Ejercicio 4: Troubleshooting - Resolver Multiple Heads (20 min)

**Objetivo**: Simular y resolver conflicto de branches en migrations.

**Pasos**:

1. **Crear el conflicto** (simular dos developers):
   ```bash
   # Developer A crea migration
   alembic revision -m "agregar indice en nombre"

   # Developer B crea migration (al mismo tiempo, mismo down_revision)
   # Editar el archivo para que apunte al mismo down_revision que la anterior
   alembic revision -m "agregar campo etiquetas"
   ```

2. **Reproducir el error**:
   ```bash
   alembic upgrade head

   # Error: Multiple head revisions are present...
   ```

3. **Usar IA para resolver**:

   **Prompt**:
   ```
   Tengo error "Multiple head revisions":
   - Revision A: abc123 (agregar indice)
   - Revision B: def456 (agregar etiquetas)

   ¿Cómo resuelvo esto sin perder ninguna migration?
   ¿Debo usar alembic merge?
   ```

4. **Aplicar solución**:
   ```bash
   # Ver heads
   alembic heads

   # Merge
   alembic merge abc123 def456 -m "merge indice y etiquetas"

   # Aplicar merge
   alembic upgrade head
   ```

5. **Validar historial**:
   ```bash
   alembic history

   # Debería mostrar:
   # abc123 -> merge_revision
   # def456 -> merge_revision
   ```

**Criterios de aceptación**:
- [ ] Conflicto de multiple heads resuelto
- [ ] Ambas migrations preservadas
- [ ] Historial muestra el merge correctamente
- [ ] `alembic upgrade head` funciona

---

### Ejercicio 5: Production Rollback Simulation (30 min)

**Objetivo**: Practicar rollback completo incluyendo backup y restore.

**Pasos**:

1. **Aplicar varias migrations** (simular producción):
   ```bash
   alembic upgrade head
   ```

2. **Crear datos de prueba** (simular usuarios activos):
   ```python
   # Crear 50 tareas con datos valiosos
   for i in range(50):
       tarea = TareaModel(
           nombre=f"Tarea producción {i}",
           descripcion="Datos críticos del usuario",
           completada=False,
           prioridad=random.choice([1, 2, 3])
       )
       db.add(tarea)
   db.commit()
   ```

3. **Backup de BD**:
   ```bash
   cp tareas.db tareas_backup_$(date +%Y%m%d_%H%M%S).db
   ```

4. **Simular migration problemática**:
   ```bash
   # Crear migration que "rompe" algo (ej: DROP COLUMN crítico)
   alembic revision -m "migration peligrosa"

   # Editar para hacer algo destructivo (solo para práctica)
   # def upgrade():
   #     op.drop_column('tareas', 'descripcion')

   alembic upgrade head
   ```

5. **Detectar problema y rollback**:
   ```bash
   # Ver que descripcion desapareció
   sqlite3 tareas.db ".schema tareas"

   # PÁNICO: Rollback inmediato
   alembic downgrade -1

   # Verificar que descripcion volvió
   sqlite3 tareas.db "SELECT descripcion FROM tareas LIMIT 5;"
   ```

6. **Validar datos post-rollback**:
   ```bash
   # Count antes vs después
   sqlite3 tareas.db "SELECT COUNT(*) FROM tareas;"
   # Debería ser el mismo (50 tareas)
   ```

7. **Plan B: Restore desde backup** (si rollback falla):
   ```bash
   # Eliminar BD corrupta
   rm tareas.db

   # Restaurar desde backup
   cp tareas_backup_20251025_120000.db tareas.db

   # Validar
   sqlite3 tareas.db "SELECT COUNT(*) FROM tareas;"
   ```

**Criterios de aceptación**:
- [ ] Backup creado antes de migration peligrosa
- [ ] Rollback funciona correctamente
- [ ] Datos se preservan en rollback
- [ ] Plan B (restore) funciona como fallback

---

## 📋 Prompts Reutilizables

### Prompt: Generar migration segura

```
Rol: Database migration specialist con experiencia en Alembic
Contexto: [Describir el cambio que necesitas]
Objetivo: Generar migration segura para producción
Restricciones:
- Tabla tiene [N] filas en producción
- [SQLite/PostgreSQL/MySQL]
- Zero-downtime required
- Migration reversible completa

Entrega:
- Código de upgrade() y downgrade()
- Explicación de por qué es seguro
- Estrategia de rollback
- Validación post-migration
```

### Prompt: Validar migration existente

```
Soy un estudiante aprendiendo Alembic. Acabo de generar esta migration:

[pegar código]

Valida:
1. ¿Es segura para producción? (pérdida de datos, locks, downtime)
2. ¿El downgrade funciona correctamente?
3. ¿Hay edge cases no manejados?
4. ¿Debería dividirla en múltiples migrations?
5. ¿Qué tests debería escribir para validarla?

No quiero la solución completa, solo hints de qué buscar y por qué.
```

### Prompt: Troubleshooting de error

```
Rol: Alembic troubleshooting expert
Error: [Pegar mensaje de error completo]
Contexto:
- Comando ejecutado: [comando]
- Migration actual: [revision]
- Stack técnico: [SQLite/PostgreSQL, FastAPI, etc.]

Tareas:
1. Identificar causa raíz del error
2. Sugerir 3 soluciones ordenadas por seguridad
3. Explicar cómo prevenir este error en el futuro
4. Comandos específicos de validación

Entrega: Diagnóstico + soluciones paso a paso
```

### Prompt: Data migration compleja

```
Rol: Data migration specialist
Contexto: Necesito transformar [campo_viejo] → [campo_nuevo]
Conversión:
- [valor_1] → [nuevo_valor_1]
- [valor_2] → [nuevo_valor_2]
- Valores inesperados → [default]

Restricciones:
- [N] filas en producción
- Sin pérdida de datos
- Reversible (aunque con pérdida de granularidad aceptable)

Entrega:
- Migration con data transformation
- Validación inline (fail fast)
- Manejo de edge cases
- Downgrade strategy
```

---

## 🔍 Validación Final con Agents

Antes de dar por completada la clase, ejecuta este checklist:

### Database ORM Specialist Validation

```markdown
**Migration Safety**:
- [ ] ¿Todas las migrations son backward-compatible?
- [ ] ¿Ninguna migration causa pérdida de datos?
- [ ] ¿Los downgrade funcionan correctamente?
- [ ] ¿No hay locks largos en tablas grandes?

**Data Integrity**:
- [ ] ¿Data migrations validan resultado (no NULL inesperados)?
- [ ] ¿Hay manejo de edge cases (valores inesperados)?
- [ ] ¿Se preservan foreign keys y constraints?

**Production Readiness**:
- [ ] ¿Hay backups antes de migrations críticas?
- [ ] ¿Multi-step strategy para cambios NOT NULL?
- [ ] ¿Índices creados con CONCURRENTLY (PostgreSQL)?
```

### Python Best Practices Coach Validation

```markdown
**Migration Code Quality**:
- [ ] ¿Migrations tienen docstrings descriptivos?
- [ ] ¿Type hints completos en funciones?
- [ ] ¿Nombres de columnas son descriptivos?
- [ ] ¿SQL statements usan parámetros (no string concat)?

**Error Handling**:
- [ ] ¿Validaciones inline con RuntimeError?
- [ ] ¿Mensajes de error son descriptivos?
```

---

## 🎯 Resultado Esperado

Al finalizar esta clase, deberías tener:

1. **Migrations generadas con IA** validadas por agentes educativos
2. **Estrategias multi-paso** para cambios peligrosos (NOT NULL)
3. **Data migrations seguras** con validación inline
4. **Troubleshooting skills** para resolver conflictos (multiple heads)
5. **Production rollback strategies** con backups

**Impacto de IA en desarrollo**:
- **60% más rápido**: IA genera migrations complejas en segundos
- **80% menos errores**: Validación con agents detecta problemas antes de producción
- **100% reversible**: IA asegura que downgrade funciona correctamente

---

## 📖 Recursos Adicionales

**Documentación oficial**:
- [Alembic Auto Generating Migrations](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)
- [Alembic Operations Reference](https://alembic.sqlalchemy.org/en/latest/ops.html)
- [PostgreSQL Index Concurrently](https://www.postgresql.org/docs/current/sql-createindex.html#SQL-CREATEINDEX-CONCURRENTLY)

**Agentes educativos**:
- Database ORM Specialist: `.claude/agents/educational/database-orm-specialist.md`
- Python Best Practices Coach: `.claude/agents/educational/python-best-practices-coach.md`

**Herramientas de validación**:
- `alembic upgrade --sql`: Preview SQL antes de ejecutar
- `alembic branches`: Detectar conflictos de merge
- `alembic history --verbose`: Ver cadena completa de migrations
