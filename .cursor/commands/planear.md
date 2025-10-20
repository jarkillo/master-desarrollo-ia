**Propósito**: Analizar la issue de Linear y crear un plan de implementación detallado.

**Proceso:**
1. **Leer la issue de Linear** (usar el código JAR-XX proporcionado)
2. **Consultar documentación relevante**:
   - `docs/API_SPECIFICATION.md` para endpoints
   - `docs/DATABASE_SCHEMA.md` para modelos
   - `docs/ARQUITECTURA.md` para estructura
   - `docs/SECURITY_CHECKLIST.md` para validaciones
3. **Analizar dependencias**:
   - ¿Qué issues deben completarse antes?
   - ¿Qué modelos/servicios/endpoints existen ya?
4. **Crear plan detallado** con:
   - **Tests a escribir** (PRIMERO, según TDD)
   - **Modelos** a crear/modificar (SQLAlchemy)
   - **Schemas** Pydantic necesarios
   - **Servicios** (lógica de negocio)
   - **Endpoints** API (FastAPI)
   - **Migraciones** Alembic si hay cambios en BD
   - **Validaciones de seguridad** a aplicar
   - **Tiempo estimado** vs tiempo de la issue

**Output esperado:**
```markdown
## 📋 Plan de Implementación: [JAR-XX] Título

### 🔍 Análisis
- **Descripción**: [breve resumen]
- **Dependencias**: [JAR-YY debe estar completo]
- **Archivos a modificar/crear**: [lista]

### 🧪 Tests (TDD - Escribir PRIMERO)
1. `tests/test_[modulo].py`:
   - `test_[funcion]_caso_exitoso()`
   - `test_[funcion]_caso_error_[tipo]()`
   - ...

### 📦 Implementación
1. **Modelo** (`app/models/[nombre].py`):
   - Campos: [lista con tipos]
   - Relaciones: [lista]
   
2. **Schema** (`app/schemas/[nombre].py`):
   - [Nombre]Create
   - [Nombre]Update
   - [Nombre]Response

3. **Servicio** (`app/services/[nombre]_service.py`):
   - Funciones: [lista con firma]

4. **Endpoint** (`app/api/v1/[nombre].py`):
   - POST/GET/PUT/DELETE [ruta]

5. **Migración Alembic**:
   - `alembic revision -m "Add [tabla]"`

### 🔒 Validaciones de Seguridad
- [ ] Validar inputs con Pydantic
- [ ] Rate limiting en endpoint
- [ ] Verificar permisos de usuario
- [ ] ...

### ⏱️ Estimación
- **Tiempo issue**: [X] horas
- **Tiempo real estimado**: [Y] horas
- **Complejidad**: Baja/Media/Alta