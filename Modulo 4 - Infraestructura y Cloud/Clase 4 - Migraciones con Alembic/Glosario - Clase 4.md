# Glosario - Clase 4: Migraciones con Alembic

## A

**Alembic**
Sistema de migraciones de base de datos para SQLAlchemy. Permite gestionar cambios de schema de forma incremental y reversible.

**Autogenerate**
Capacidad de Alembic de generar migrations automáticamente comparando modelos SQLAlchemy con el schema actual de la BD.
```bash
alembic revision --autogenerate -m "descripción"
```

**alembic.ini**
Archivo de configuración de Alembic que contiene la URL de la BD, hooks de formateo, y otras opciones.

## D

**Data Migration**
Migration que no solo modifica el schema, sino que también transforma datos existentes. Ejemplo: convertir `prioridad` (int) a `prioridad_texto` (string).

**Down Revision**
Identificador de la migration anterior en la cadena. Conecta migrations en secuencia.
```python
down_revision = '58cbce442bf6'  # Migration padre
```

**Downgrade**
Proceso de revertir una migration, deshaciendo los cambios aplicados. Ejecuta la función `downgrade()` de la migration.
```bash
alembic downgrade -1  # Retroceder 1 migration
```

## E

**env.py**
Script de entorno de Alembic que configura cómo se conecta a la BD y qué modelos usar.
```python
from api.models import Base
target_metadata = Base.metadata
```

## H

**Head**
Última migration en la cadena. `alembic upgrade head` aplica todas las migrations pendientes.

**History**
Historial de todas las migrations creadas.
```bash
alembic history  # Ver todas las migrations
```

## M

**Migration**
Archivo Python que define cambios incrementales en el schema de la BD. Contiene funciones `upgrade()` y `downgrade()`.

**Migration Chain**
Secuencia de migrations conectadas mediante `down_revision`. Ejemplo:
```
base → migration_A → migration_B → migration_C (head)
```

## O

**Offline Mode**
Modo de ejecución de Alembic que genera SQL sin ejecutarlo. Útil para revisar cambios antes de aplicarlos.
```bash
alembic upgrade head --sql > migration.sql
```

## R

**Revision**
Identificador único de una migration. Generado automáticamente por Alembic.
```python
revision = '58cbce442bf6'
```

**Rollback**
Proceso de revertir cambios en la BD usando `downgrade`. Estrategia de recuperación ante errores.

## S

**Schema**
Estructura de la base de datos (tablas, columnas, índices, constraints). Alembic gestiona cambios de schema.

**Stamp**
Marcar la BD como si estuviera en una revisión específica sin ejecutar migrations. Útil para BD existentes.
```bash
alembic stamp head  # Marcar como actualizada
```

## T

**Target Metadata**
Objeto `Base.metadata` de SQLAlchemy que Alembic usa para comparar modelos con la BD.

## U

**Upgrade**
Proceso de aplicar una migration, ejecutando la función `upgrade()` para modificar el schema.
```bash
alembic upgrade head  # Aplicar todas las migrations pendientes
```

## V

**Versions**
Carpeta que contiene todos los archivos de migrations (`alembic/versions/`).

## Z

**Zero-Downtime Migration**
Estrategia de migration que permite actualizar la BD sin detener la aplicación. Requiere múltiples pasos y compatibilidad hacia atrás.

---

## Comandos clave

| Comando | Descripción |
|---------|-------------|
| `alembic init alembic` | Inicializar Alembic en el proyecto |
| `alembic revision --autogenerate -m "msg"` | Generar migration automáticamente |
| `alembic upgrade head` | Aplicar todas las migrations pendientes |
| `alembic downgrade -1` | Revertir última migration |
| `alembic history` | Ver historial de migrations |
| `alembic current` | Ver migration actual |
| `alembic stamp head` | Marcar BD como actualizada |
| `alembic show head` | Ver última migration |

---

## Funciones de Migration

| Función | Descripción | Ejemplo |
|---------|-------------|---------|
| `op.create_table()` | Crear tabla | `op.create_table('tareas', ...)` |
| `op.drop_table()` | Eliminar tabla | `op.drop_table('tareas')` |
| `op.add_column()` | Agregar columna | `op.add_column('tareas', sa.Column('prioridad', sa.Integer()))` |
| `op.drop_column()` | Eliminar columna | `op.drop_column('tareas', 'prioridad')` |
| `op.alter_column()` | Modificar columna | `op.alter_column('tareas', 'nombre', new_column_name='titulo')` |
| `op.create_index()` | Crear índice | `op.create_index('idx_nombre', 'tareas', ['nombre'])` |
| `op.drop_index()` | Eliminar índice | `op.drop_index('idx_nombre')` |
| `op.create_foreign_key()` | Crear foreign key | `op.create_foreign_key('fk_usuario', 'tareas', 'usuarios', ['usuario_id'], ['id'])` |
| `op.execute()` | Ejecutar SQL arbitrario | `op.execute("UPDATE tareas SET prioridad = 2")` |
| `op.get_bind()` | Obtener conexión BD | `connection = op.get_bind()` |

---

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `Target database is not up to date` | Hay migrations pendientes | `alembic upgrade head` |
| `Can't locate revision identified by 'xxx'` | Migration faltante o corrupta | Verificar `alembic/versions/` |
| `FAILED: Multiple head revisions are present` | Dos migrations apuntan al mismo padre | `alembic merge` |
| `sqlalchemy.exc.IntegrityError` | Violación de constraint en data migration | Validar datos antes de migration |
| `Table 'tareas' already exists` | Intentando crear tabla existente | Usar `alembic stamp head` |

---

## Conceptos relacionados

**DDL (Data Definition Language)**
Lenguaje SQL para definir schema (CREATE, ALTER, DROP). Alembic genera DDL automáticamente.

**DML (Data Manipulation Language)**
Lenguaje SQL para manipular datos (INSERT, UPDATE, DELETE). Usado en data migrations.

**Schema Evolution**
Proceso de evolucionar el schema de la BD a lo largo del tiempo. Alembic gestiona esta evolución.

**Idempotency**
Propiedad de que aplicar una operation múltiples veces produce el mismo resultado. Las migrations deben ser idempotentes (usar `IF NOT EXISTS`, `IF EXISTS`).

**Transactional DDL**
Capacidad de la BD de hacer rollback de cambios de schema. PostgreSQL soporta DDL transaccional, SQLite parcialmente, MySQL no.

---

## Best Practices

1. **Siempre revisar migrations autogeneradas**: Alembic puede generar código incorrecto
2. **Escribir downgrade reversible**: Cada `upgrade()` debe tener `downgrade()` funcional
3. **Probar en desarrollo primero**: Nunca aplicar migrations en producción sin probar
4. **Usar nombres descriptivos**: `"agregar_campo_prioridad"` mejor que `"cambio_1"`
5. **Commits después de migrations exitosas**: Git commit después de `alembic upgrade head`
6. **Backup antes de producción**: Siempre backup de la BD antes de aplicar migrations

---

## Recursos adicionales

- [Documentación oficial de Alembic](https://alembic.sqlalchemy.org/)
- [Tutorial de Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Alembic Cookbook](https://alembic.sqlalchemy.org/en/latest/cookbook.html)
