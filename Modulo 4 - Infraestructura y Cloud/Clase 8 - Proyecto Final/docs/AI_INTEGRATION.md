# 🤖 AI Integration - Desarrollo Asistido por IA

Este documento enseña cómo usar IA efectivamente durante el desarrollo del Proyecto Final.

**Filosofía**: La IA es tu **pair programmer junior** - puede generar código rápido, pero TÚ debes entender, revisar y decidir.

---

## 📋 Tabla de Contenidos

1. [Principios de Desarrollo con IA](#-principios-de-desarrollo-con-ia)
2. [Prompts por Fase del Proyecto](#-prompts-por-fase-del-proyecto)
3. [Mejores Prácticas](#-mejores-prácticas)
4. [Anti-Patterns](#-anti-patterns-qué-no-hacer)
5. [Troubleshooting con IA](#-troubleshooting-con-ia)
6. [Ejemplos Reales](#-ejemplos-reales)

---

## 🎯 Principios de Desarrollo con IA

### 1. **La IA no reemplaza tu cerebro**

```
❌ MAL: "Crea una API completa de tareas"
✅ BIEN: "Diseña el modelo ORM para Usuario con estos campos..."
```

**Por qué**: Requests muy amplios producen código genérico que no entiendes.

### 2. **Itera, no generes todo de una**

```
Fase 1: Diseño → Pide arquitectura general
Fase 2: Modelo  → Genera modelos ORM
Fase 3: Review  → Pide revisión de modelos
Fase 4: Repo    → Genera repositorio
Fase 5: Tests   → Genera tests del repositorio
```

**Por qué**: Iteraciones pequeñas te permiten entender cada pieza.

### 3. **Siempre revisa y modifica el código generado**

```python
# IA genera:
def crear_tarea(titulo: str):
    tarea = Tarea(titulo=titulo)
    db.add(tarea)
    db.commit()
    return tarea

# TÚ mejoras:
def crear_tarea(titulo: str, usuario_id: int) -> TareaModel:
    """Crea una tarea asignada al usuario."""
    if not titulo.strip():
        raise ValueError("Título no puede estar vacío")

    tarea = TareaModel(titulo=titulo, usuario_id=usuario_id)
    self._session.add(tarea)
    self._session.commit()
    self._session.refresh(tarea)
    return tarea
```

**Por qué**: La IA no conoce tu contexto específico (validaciones, reglas de negocio).

### 4. **La IA es excelente para boilerplate, pero tú defines la lógica**

**IA es buena para:**
- ✅ Generar esqueletos de clases
- ✅ Escribir tests repetitivos
- ✅ Sugerir nombres de variables
- ✅ Explicar errores complejos
- ✅ Generar documentación

**TÚ eres mejor para:**
- ✅ Diseñar arquitectura
- ✅ Tomar decisiones de negocio
- ✅ Optimizar para tu caso de uso
- ✅ Entender trade-offs

---

## 📝 Prompts por Fase del Proyecto

### Fase 1: Diseño de Arquitectura

**Prompt:**

```
Rol: Software architect especializado en Python y FastAPI.

Contexto: Voy a crear una API de gestión de tareas con:
- Usuarios autenticados (JWT)
- Tareas asignadas a usuarios (relación 1:N)
- Autenticación, CRUD, filtros, paginación
- PostgreSQL en producción, SQLite en desarrollo

Objetivo: Diseña la arquitectura en capas siguiendo Clean Architecture:
- API Layer (FastAPI endpoints)
- Service Layer (lógica de negocio)
- Repository Layer (abstracción de BD)
- Database Layer (SQLAlchemy ORM)

Restricciones:
- Dependency Injection con FastAPI Depends()
- Repository Pattern con Protocols
- Configuración multi-entorno (Pydantic Settings)

Entrega:
1. Diagrama de capas (texto)
2. Estructura de directorios
3. Explicación de cada capa (responsabilidades)
4. Flujo de un request típico (desde endpoint hasta BD)
```

**Qué esperar:**
- Estructura de directorios clara
- Explicación de separación de responsabilidades
- Ejemplos de cómo fluye la información

**Qué validar:**
- ⚠️ Que la arquitectura se adapte a tu escala (no over-engineering)
- ⚠️ Que uses Patterns que conoces (no inventes)

---

### Fase 2: Diseño de Modelos de Datos

**Prompt:**

```
Rol: Database designer especializado en SQLAlchemy 2.0.

Contexto: Necesito diseñar 2 modelos: Usuario y Tarea.

Especificaciones:
**Usuario:**
- email (único, indexado)
- nombre
- password_hash (nunca password en claro)
- activo (para soft delete)
- creado_en, actualizado_en (automáticos)

**Tarea:**
- titulo (max 200 caracteres)
- descripcion (opcional, max 1000)
- completada (boolean)
- prioridad (1=Baja, 2=Media, 3=Alta)
- eliminada (soft delete)
- usuario_id (FK a usuarios)
- creado_en, actualizado_en

Relación: Un usuario tiene muchas tareas (1:N)

Objetivo: Genera los modelos con:
- SQLAlchemy 2.0 syntax (Mapped[], mapped_column)
- Type hints completos
- Relaciones bidireccionales con back_populates
- Cascade rules correctas
- Índices para queries frecuentes:
  * usuario_id + completada
  * usuario_id + eliminada
  * prioridad

Restricciones:
- Compatible con PostgreSQL y SQLite
- Timestamps con server_default=func.now()
- Snake_case para nombres de tabla

Entrega:
- Código Python completo
- Explicación de cada índice (por qué optimiza)
- Ejemplo de query que usa cada índice
```

**Qué esperar:**
- Modelos con todas las columnas
- Índices bien justificados
- Explicación de cascade rules

**Qué validar:**
- ⚠️ Tipos de columnas (String(100) vs Text)
- ⚠️ Índices realmente necesarios (no todos lo son)
- ⚠️ Cascade rules no borran datos importantes

---

### Fase 3: Implementación de Repositorio

**Prompt:**

```
Rol: Backend developer especializado en Repository Pattern.

Contexto: Tengo estos modelos ORM:
[pegar modelos UsuarioModel y TareaModel]

Objetivo: Implementa RepositorioTareasDB con:

Métodos requeridos:
1. crear(titulo, usuario_id, descripcion=None, prioridad=2) -> TareaModel
2. listar(usuario_id, completada=None, prioridad=None, limite=10, offset=0) -> List[TareaModel]
3. obtener_por_id(tarea_id, usuario_id) -> Optional[TareaModel]
4. actualizar(tarea: TareaModel) -> TareaModel
5. eliminar(tarea_id, usuario_id) -> bool  # Soft delete
6. restaurar(tarea_id, usuario_id) -> bool
7. contar(usuario_id, ...) -> int  # Para paginación

Restricciones:
- Session injection en __init__
- No devolver tareas eliminadas (excepto en restaurar)
- Verificar que tarea pertenece al usuario (seguridad)
- Ordenar por prioridad desc, creado_en desc
- Soft delete (marcar eliminada=True, no DELETE)

Entrega:
- Código completo del repositorio
- Docstrings en cada método
- Comentarios en queries complejas
```

**Qué esperar:**
- Repositorio funcional con todos los métodos
- Queries optimizadas
- Seguridad (verificar usuario_id)

**Qué validar:**
- ⚠️ Soft delete implementado correctamente
- ⚠️ Queries no hacen N+1
- ⚠️ Validación de permisos (usuario solo ve sus tareas)

---

### Fase 4: Implementación de Endpoints

**Prompt:**

```
Rol: FastAPI expert especializado en REST APIs.

Contexto: Tengo ServicioTareas con estos métodos:
[listar métodos del servicio]

Objetivo: Implementa el endpoint GET /tareas con:

Funcionalidades:
- Listar tareas del usuario autenticado
- Query params opcionales:
  * page (int, default=1, >=1)
  * page_size (int, default=10, entre 1 y 100)
  * completada (bool, opcional)
  * prioridad (int, entre 1 y 3, opcional)
  * q (string, búsqueda en título, max 200 chars)

Response:
{
  "items": [TareaResponse],
  "total": int,
  "page": int,
  "page_size": int,
  "total_pages": int
}

Restricciones:
- Proteger con Depends(obtener_usuario_actual)
- Inyectar servicio con Depends(get_servicio_tareas)
- Validaciones automáticas con Query()
- response_model=TareaListResponse
- Docstring explicativo

Entrega:
- Código del endpoint
- Schema de TareaListResponse (Pydantic)
- Ejemplos de uso con curl
```

**Qué esperar:**
- Endpoint con todas las validaciones
- Schema de response bien definido
- Documentación clara

**Qué validar:**
- ⚠️ Autenticación correcta (JWT)
- ⚠️ Validaciones de Query params
- ⚠️ Response model coincide con lo prometido

---

### Fase 5: Tests

**Prompt:**

```
Rol: QA engineer especializado en pytest y FastAPI testing.

Contexto: Tengo este endpoint:
[pegar código del endpoint]

Objetivo: Genera tests que cubran:

1. **Happy path**: Request válido devuelve 200 con datos correctos
2. **Validación**: Parámetros inválidos devuelven 422
3. **Autenticación**: Sin JWT devuelve 401
4. **Autorización**: Usuario solo ve sus tareas (no de otros)
5. **Paginación**: Verificar total, total_pages
6. **Filtros**: Cada filtro funciona (completada, prioridad, q)
7. **Edge cases**: Lista vacía, página fuera de rango

Restricciones:
- Usar fixtures de conftest.py (test_db, auth_headers, tarea_test)
- Assertions claras con mensajes
- Nombres descriptivos (test_listar_tareas_filtro_completada)
- Agrupar tests relacionados

Entrega:
- Código de tests completo
- Comentarios explicando qué valida cada test
- Al menos 8 tests diferentes
```

**Qué esperar:**
- Tests completos y bien nombrados
- Coverage de casos happy path y edge cases
- Uso correcto de fixtures

**Qué validar:**
- ⚠️ Tests realmente validan lo correcto (no false positives)
- ⚠️ No hay tests redundantes
- ⚠️ Coverage de error handling

---

### Fase 6: Docker Optimization

**Prompt:**

```
Tengo este Dockerfile:
[pegar Dockerfile actual]

Problemas:
- Imagen muy grande (600MB)
- Build lento (3+ minutos)
- Incluye dependencias de desarrollo

Objetivo: Optimiza usando:
- Multi-stage build (builder + runtime)
- Alpine Linux (si es compatible con psycopg2)
- Cache de layers
- Non-root user para seguridad

Restricciones:
- Debe incluir psycopg2 (necesita libpq-dev en build)
- Mantener health check
- Port 8000 expuesto

Entrega:
- Dockerfile optimizado
- Comparativa de tamaños (antes/después)
- Explicación de cada optimización
```

**Qué esperar:**
- Dockerfile multi-stage
- Imagen más pequeña (50%+ reducción)
- Explicación de optimizaciones

**Qué validar:**
- ⚠️ Imagen funciona igual (no rompió nada)
- ⚠️ Build sigue siendo reproducible
- ⚠️ Seguridad mejorada (non-root)

---

### Fase 7: Migraciones

**Prompt:**

```
Contexto: Tengo modelos SQLAlchemy y Alembic configurado.

Problema: Necesito agregar un campo "fecha_limite" (opcional) a TareaModel.

Objetivo: Guíame paso a paso:
1. Modificar el modelo ORM
2. Generar migración con Alembic
3. Revisar el SQL generado
4. Aplicar migración
5. Rollback si algo falla

Restricciones:
- Campo debe ser opcional (nullable=True)
- Debe tener default=None
- Compatible con SQLite y PostgreSQL

Entrega:
- Código modificado del modelo
- Comandos de Alembic a ejecutar
- Qué verificar en el archivo de migración generado
- Cómo testear que funciona
```

**Qué esperar:**
- Pasos claros y ordenados
- Comandos exactos de Alembic
- Qué revisar en la migración generada

**Qué validar:**
- ⚠️ SQL generado es correcto (no DROP TABLE accidentalmente)
- ⚠️ Migración es reversible (downgrade funciona)
- ⚠️ No pierde datos existentes

---

## ✅ Mejores Prácticas

### 1. **Da contexto específico**

```
❌ "Haz un endpoint de login"

✅ "Crea endpoint POST /auth/login que:
   - Recibe email y password
   - Valida credenciales con bcrypt
   - Devuelve JWT token con expiración de 60min
   - 401 si credenciales incorrectas
   - Usa el UsuarioModel de models.py"
```

### 2. **Pide explicaciones, no solo código**

```
✅ "Explica por qué usas cascade='all, delete-orphan'"
✅ "¿Cuál es el trade-off entre SQLite y PostgreSQL aquí?"
✅ "¿Por qué índice compuesto en lugar de dos índices separados?"
```

### 3. **Itera sobre el código generado**

```
Tú: Genera el repositorio de tareas
IA: [genera código]

Tú: El método listar() no filtra por usuario_id, arréglalo
IA: [corrige]

Tú: Ahora agrega paginación con limit y offset
IA: [agrega]

Tú: Falta validar que el usuario existe antes de crear tarea
IA: [agrega validación]
```

### 4. **Usa IA para review de tu código**

```
He escrito este endpoint:
[pegar código]

¿Hay algún problema de seguridad?
¿Falta alguna validación?
¿El error handling es correcto?
¿Hay mejor forma de escribir esto?
```

### 5. **Aprende de las sugerencias**

```
IA sugiere: "Usa .ilike() en lugar de .like() para búsqueda case-insensitive"

Tú investigas: ¿Qué es ilike()? ¿Funciona en PostgreSQL y SQLite?
Resultado: Entiendes y aplicas correctamente
```

---

## ❌ Anti-Patterns (Qué NO hacer)

### 1. **Copy-paste sin entender**

```python
# IA genera:
@app.get("/tareas")
async def listar_tareas(db: Session = Depends(get_db)):
    tareas = db.query(TareaModel).all()
    return tareas

# TÚ haces copy-paste sin notar:
# ❌ No hay autenticación (cualquiera ve TODAS las tareas)
# ❌ No hay filtro por usuario
# ❌ No hay paginación (puede devolver 100,000 tareas)
# ❌ Devuelve password_hash si hay join con usuario
```

**Solución**: Lee, entiende, modifica.

### 2. **Pedir "haz toda la API"**

```
❌ "Crea una API completa de gestión de tareas con FastAPI, SQLAlchemy,
   JWT, Docker, tests y deployment en Railway"

Resultado: Código genérico de 2000 líneas que no compile ni entiendas.
```

**Solución**: Pide componentes específicos uno por uno.

### 3. **No verificar código de seguridad**

```python
# IA genera (PELIGROSO):
password = request.password  # ❌ Nunca validado
user = User(password=password)  # ❌ Password en claro

# TÚ DEBES cambiar a:
password_hash = hash_password(request.password)
user = User(password_hash=password_hash)
```

**Regla**: Siempre revisa autenticación, autorización, validación.

### 4. **Asumir que el código generado es óptimo**

```python
# IA genera:
for tarea in tareas:
    tarea.usuario = db.query(Usuario).get(tarea.usuario_id)  # ❌ N+1

# TÚ optimizas:
tareas = db.query(Tarea).options(joinedload(Tarea.usuario)).all()  # ✅ 1 query
```

**Regla**: Siempre considera performance.

### 5. **No testear el código generado**

```
IA genera endpoint → TÚ haces commit → En producción falla

Correcto:
IA genera endpoint → TÚ escribes test → Test falla → Corriges → Commit
```

---

## 🐛 Troubleshooting con IA

### Tipo 1: Errores de código

**Prompt efectivo:**

```
Tengo este error al ejecutar pytest:

[pegar stack trace COMPLETO]

Mi código:
[pegar código relevante, no todo el proyecto]

¿Cuál es la causa?
¿Cómo lo arreglo?
¿Cómo evito que vuelva a pasar?
```

**La IA es excelente para:**
- ✅ Interpretar stack traces complejos
- ✅ Identificar la línea exacta del problema
- ✅ Sugerir 2-3 causas probables

**Tú debes:**
- ⚠️ Leer el error completo primero (no solo la última línea)
- ⚠️ Verificar cada sugerencia (no asumir que la primera es correcta)

---

### Tipo 2: Errores de deployment

**Prompt efectivo:**

```
Mi API falla al desplegar en Railway con este error:

[pegar logs de Railway]

Setup:
- Dockerfile multi-stage
- PostgreSQL addon conectado
- Variables: DATABASE_URL, JWT_SECRET, ENVIRONMENT=prod
- Build termina exitoso, pero al iniciar falla

¿Qué puede estar causando el error?
¿Qué debo verificar primero?
¿Cómo reproduzco localmente?
```

**La IA sugerirá:**
1. Verificar variables de entorno
2. Check de migraciones (Alembic)
3. Logs de la aplicación

**Tú debes:**
- ⚠️ Verificar TODAS las variables (typos comunes)
- ⚠️ Ejecutar migrations localmente primero
- ⚠️ Revisar logs completos (no solo el error)

---

### Tipo 3: Tests que fallan

**Prompt efectivo:**

```
Este test falla pero no entiendo por qué:

[pegar código del test]

Error:
[pegar assertion error]

Mi fixture:
[pegar fixture relevante]

¿Qué estoy haciendo mal?
```

**La IA identificará:**
- Fixtures mal configuradas
- Assertions incorrectas
- Estado compartido entre tests

**Tú debes:**
- ⚠️ Ejecutar el test aislado (`pytest test_file.py::test_name`)
- ⚠️ Verificar fixtures con `--fixtures`
- ⚠️ Leer el error de assertion completo

---

### Tipo 4: Performance issues

**Prompt efectivo:**

```
Mi endpoint /tareas es muy lento (5+ segundos).

Código:
[pegar endpoint y queries]

¿Qué está causando la lentitud?
¿Hay problema de N+1 queries?
¿Qué índices faltan?
```

**La IA detectará:**
- N+1 queries (loop haciendo queries)
- Missing indexes
- Queries sin limit

**Tú debes:**
- ⚠️ Usar SQL logging (echo=True) para ver queries
- ⚠️ Verificar con `EXPLAIN` en PostgreSQL
- ⚠️ Testear con datos reales (no 10 tareas, 10,000)

---

## 💡 Ejemplos Reales

### Ejemplo 1: Agregar búsqueda de texto

**Conversación con IA:**

```
Yo: Necesito agregar búsqueda por texto en el endpoint GET /tareas.
    Query param: ?q=comprar
    Debe buscar case-insensitive en el campo titulo.

IA: Puedes usar .ilike() de SQLAlchemy:
    query.filter(TareaModel.titulo.ilike(f"%{q}%"))

Yo: ¿Funciona en SQLite y PostgreSQL?

IA: Sí, ambos soportan ILIKE.

Yo: ¿Necesito índice para esto?

IA: Para búsquedas LIKE no hay índice eficiente en texto.
    Considera full-text search si tienes miles de tareas.

Yo: OK, por ahora me alcanza con ILIKE. ¿Cómo limito resultados?

IA: Agrega .limit(50) al query para evitar devolver todo.

[Implemento, testeo, funciona]
```

**Lecciones:**
- ✅ Pregunté sobre compatibilidad (SQLite vs PostgreSQL)
- ✅ Pregunté sobre performance (índices)
- ✅ Consideré límites (no devolver todo)

---

### Ejemplo 2: Debugging de migración fallida

**Conversación con IA:**

```
Yo: Alembic falla con este error:
    "Target database is not up to date"

IA: Ejecuta `alembic current` para ver el estado actual.

Yo: [ejecuto] Muestra: (head)

IA: Ejecuta `alembic history` para ver migraciones pendientes.

Yo: [ejecuto] Hay una migración que no está aplicada.

IA: Ejecuta `alembic upgrade head` para aplicarla.

Yo: [ejecuto] Falla con: "column fecha_limite already exists"

IA: La migración ya se aplicó parcialmente. Necesitas:
    1. Verificar manualmente qué columnas existen
    2. Marcar la migración como aplicada: alembic stamp head
    O
    3. Hacer rollback y volver a aplicar

Yo: [verifico BD] La columna existe. Hago stamp head.
    [funciona]
```

**Lecciones:**
- ✅ IA me guió paso a paso
- ✅ Yo ejecuté cada comando y reporté resultado
- ✅ Verificamos estado de BD antes de decidir

---

### Ejemplo 3: Optimizar Dockerfile

**Conversación con IA:**

```
Yo: Mi imagen Docker es 800MB. ¿Cómo la reduzco?

    Dockerfile:
    [pego Dockerfile single-stage]

IA: Usa multi-stage build:
    Stage 1: Instala dependencias (gcc, build-tools)
    Stage 2: Copia solo lo necesario para runtime

    [genera Dockerfile multi-stage]

Yo: ¿Por qué funciona esto?

IA: El stage 1 (builder) queda descartado.
    Solo se incluye en la imagen final el stage 2 (runtime).

Yo: [buildo nueva imagen] ¡Ahora es 280MB! (65% reducción)

IA: Puedes reducir más usando python:3.12-alpine en lugar de python:3.12-slim.

Yo: [pruebo alpine] Falla al instalar psycopg2.

IA: Alpine usa musl en lugar de glibc. Instala psycopg2-binary en requirements.

Yo: [cambio a psycopg2-binary] Funciona. Imagen: 180MB (78% reducción).
```

**Lecciones:**
- ✅ IA explicó el concepto (multi-stage)
- ✅ Yo probé cada sugerencia
- ✅ Cuando falló, debugueamos juntos

---

## 📚 Recursos Adicionales

**Prompting para desarrollo:**
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Library](https://docs.anthropic.com/claude/prompt-library)

**AI Pair Programming:**
- [GitHub Copilot Best Practices](https://github.blog/2023-06-20-how-to-write-better-prompts-for-github-copilot/)
- [Cursor AI Tips](https://cursor.sh/docs)

**Testing AI-Generated Code:**
- [How to review AI code](https://stackoverflow.blog/2023/04/03/how-to-review-ai-generated-code-effectively/)

---

## ✅ Checklist de AI Integration

Antes de usar código generado por IA:

- [ ] Entiendo QUÉ hace el código
- [ ] Entiendo POR QUÉ está escrito así
- [ ] He verificado casos edge (qué pasa si...?)
- [ ] He revisado seguridad (autenticación, validación)
- [ ] He escrito tests para el código
- [ ] He ejecutado los tests y pasan
- [ ] He considerado performance
- [ ] He agregado type hints si faltan
- [ ] He documentado con docstrings si falta
- [ ] Puedo explicar este código a otra persona

---

**Regla de oro**: Si no entiendes el código que generó la IA, NO LO USES. Pide que te explique, iteración por iteración, hasta que lo entiendas.

La IA es una herramienta poderosa, pero TÚ eres el desarrollador.
