# Ejercicios Prácticos: Repository Pattern y Clean Architecture con IA

## 🎯 Objetivo

Dominar el uso de IA para **diseñar, implementar y validar arquitectura limpia** aplicando Repository Pattern, Open/Closed Principle y Dependency Inversion.

Al completar estos ejercicios, sabrás:
- ✅ Generar Protocols con IA que cumplen SOLID
- ✅ Implementar repositorios concretos (SQLite, Redis)
- ✅ Validar arquitectura con agentes educacionales
- ✅ Detectar y corregir violaciones de DIP
- ✅ Refactorizar código legacy a Clean Architecture

---

## Ejercicio 1: Implementar RepositorioSQLite con IA

### 📋 Contexto

Tienes `RepositorioMemoria` y `RepositorioJSON` funcionando. Ahora necesitas persistencia real en base de datos SQLite para escalar a producción.

**Requisitos**:
- Debe cumplir el mismo Protocol (`RepositorioTareas`)
- Usar `sqlite3` del stdlib (sin ORMs externos)
- Manejo robusto de errores (tabla no existe, BD corrupta)
- IDs autoincrementales (AUTOINCREMENT en SQLite)

---

### 🤖 Paso 1: Diseñar el prompt

**Tu tarea**: Escribe un prompt estructurado para que IA genere `RepositorioSQLite`.

**Plantilla sugerida**:

```
Rol: [¿Qué expertise necesitas?]

Contexto:
[Describe el Protocol, el esquema de la tabla, requisitos de la BD]

Objetivo:
[Qué clase quieres generar]

Requisitos:
[Lista completa de funcionalidades]

Restricciones:
[Límites técnicos: solo sqlite3, no ORMs, etc.]

Formato:
```python
# api/repositorio_sqlite.py
# Código aquí
```

Explica:
[Qué decisiones de diseño quieres que justifique]
```

**Criterios de éxito**:
- [ ] Prompt incluye el Protocol completo como referencia
- [ ] Especifica el esquema de la tabla (CREATE TABLE)
- [ ] Pide manejo de conexiones con context managers
- [ ] Requiere type hints completos
- [ ] Pide docstrings que expliquen manejo de errores

---

### 🔨 Paso 2: Generar el código con IA

Ejecuta tu prompt con Claude/ChatGPT/Copilot.

**Validación rápida**:
```python
# ¿El código tiene estas características?
- [ ] def __init__(self, ruta_bd: str = "tareas.db"): ...
- [ ] _crear_tabla_si_no_existe() en __init__
- [ ] with sqlite3.connect(...) as conn: (context manager)
- [ ] try/except para manejar errores de BD
- [ ] Implementa los 5 métodos del Protocol
```

---

### ✅ Paso 3: Validar con Python Best Practices Coach

**Prompt de validación**:

```
Rol: Python Best Practices Coach

Revisa este código de RepositorioSQLite y valida:

1. ¿Usa context managers para conexiones? (with conn:)
2. ¿Maneja excepciones de BD? (sqlite3.Error)
3. ¿Usa SQL parametrizado? (? placeholders, NO f-strings)
4. ¿Cierra conexiones correctamente?
5. ¿Los type hints son correctos?

Código:
[Pegar RepositorioSQLite completo]

Formato:
✅ Validaciones correctas
❌ Problemas encontrados (con línea y corrección)
```

**Red flags comunes**:

```python
# ❌ SQL Injection vulnerable
cursor.execute(f"SELECT * FROM tareas WHERE id = {id}")  # MAL

# ✅ SQL parametrizado (seguro)
cursor.execute("SELECT * FROM tareas WHERE id = ?", (id,))  # BIEN


# ❌ Conexión no se cierra
conn = sqlite3.connect("tareas.db")
cursor = conn.cursor()  # MAL: si hay excepción, no se cierra

# ✅ Context manager cierra automáticamente
with sqlite3.connect("tareas.db") as conn:
    cursor = conn.cursor()  # BIEN: se cierra incluso con excepciones
```

---

### 🧪 Paso 4: Agregar a los tests parametrizados

**Tu tarea**: Modifica `test_repositorios_integracion.py` para incluir SQLite.

**Cambio necesario**:

```python
# tests_integrations/test_repositorios_integracion.py

from api.repositorio_sqlite import RepositorioSQLite  # NUEVO

@pytest.fixture(params=["memoria", "json", "sqlite"])  # Agregar "sqlite"
def repositorio(request, tmp_path):
    if request.param == "memoria":
        return RepositorioMemoria()
    elif request.param == "json":
        archivo = tmp_path / f"tareas_{request.node.name}.json"
        return RepositorioJSON(str(archivo))
    elif request.param == "sqlite":  # NUEVO
        bd = tmp_path / f"tareas_{request.node.name}.db"
        return RepositorioSQLite(str(bd))
```

**Ejecutar tests**:

```bash
cd "Modulo 2 – Ingeniería y Arquitectura/Clase 4 - Open_Closed y Dependency Inversion"
pytest tests_integrations/ -v
```

**Criterios de éxito**:
- [ ] Los 15 tests pasan para los **3 repositorios** (45 tests totales)
- [ ] Si algún test falla solo para SQLite, hay un bug de implementación
- [ ] Todos los repositorios son **perfectamente intercambiables**

---

### 💾 Entregable

**Archivo a crear**: `api/repositorio_sqlite.py` (aproximadamente 150 líneas)

**Incluir en el código**:
- Docstring de clase con características y limitaciones
- Método `_crear_tabla_si_no_existe()` privado
- Context managers en todos los métodos
- Try/except con sqlite3.Error
- Type hints completos
- Comentarios que expliquen SQL no obvio

**Extra (opcional)**:
- Índice en la columna `id` para búsquedas rápidas
- Manejo de concurrent access (BEGIN TRANSACTION)
- Logging de errores con `logging` module

---

## Ejercicio 2: Code Review de Arquitectura con Agentes Educacionales

### 📋 Contexto

Te uniste a un proyecto donde el código viola principios SOLID. Tu tarea: usar agentes de IA para identificar violaciones y proponer refactorizaciones.

---

### 🔍 Paso 1: Analizar código legacy

**Código problemático** (simula un proyecto real):

```python
# api/api_legacy.py (CÓDIGO MALO - NO USAR)
from fastapi import FastAPI
import json

app = FastAPI()

@app.post("/tareas")
def crear_tarea(nombre: str):
    # PROBLEMA 1: Lógica de persistencia en la API
    with open("tareas.json", "r") as f:
        tareas = json.load(f)

    # PROBLEMA 2: Generación de ID en la API
    nuevo_id = max([t["id"] for t in tareas], default=0) + 1

    # PROBLEMA 3: Lógica de negocio mezclada
    nueva_tarea = {
        "id": nuevo_id,
        "nombre": nombre,
        "completada": False
    }
    tareas.append(nueva_tarea)

    # PROBLEMA 4: Escritura en disco directamente
    with open("tareas.json", "w") as f:
        json.dump(tareas, f)

    return nueva_tarea


@app.get("/tareas")
def listar_tareas():
    # PROBLEMA 5: Código duplicado (lectura de archivo)
    with open("tareas.json", "r") as f:
        return json.load(f)
```

**Tu tarea**: Usa agentes de IA para identificar TODAS las violaciones de SOLID.

---

### 🤖 Paso 2: Validar con FastAPI Design Coach

**Prompt**:

```
Rol: FastAPI Design Coach experto en Clean Architecture

Contexto:
Analiza este código de una API FastAPI

Código:
[Pegar api_legacy.py completo]

Objetivo:
Identifica TODAS las violaciones de:
1. Single Responsibility Principle (SRP)
2. Open/Closed Principle (OCP)
3. Dependency Inversion Principle (DIP)
4. Separation of Concerns (API vs Servicio vs Repositorio)

Para cada violación:
- Indica la línea exacta
- Explica QUÉ principio se viola y POR QUÉ
- Propón la refactorización correcta
- Muestra código antes/después

Formato:
## ❌ Violaciones encontradas
### Violación 1: [Nombre del principio]
**Línea**: X
**Problema**: [Explicación]
**Refactorización**: [Código correcto]
```

**Resultado esperado** (parcial):

```markdown
## ❌ Violaciones encontradas

### Violación 1: Dependency Inversion Principle (DIP)
**Línea**: 8-10
**Problema**: La API depende directamente del detalle de implementación (archivo JSON).
Cambiar de JSON a SQLite requiere modificar TODOS los endpoints.

**Refactorización**:
```python
# ✅ CORRECTO: Inyectar repositorio abstracto
from api.repositorio_base import RepositorioTareas

def crear_tarea(
    nombre: str,
    servicio: ServicioTareas = Depends(obtener_servicio)  # Inyección
):
    tarea = servicio.crear(nombre)
    return tarea.model_dump()
```

### Violación 2: Single Responsibility Principle (SRP)
**Línea**: Toda la función `crear_tarea`
**Problema**: El endpoint hace 4 cosas:
1. Lee archivo (persistencia)
2. Genera ID (lógica de dominio)
3. Crea tarea (lógica de negocio)
4. Escribe archivo (persistencia)

**Refactorización**: Separar en capas (API → Servicio → Repositorio)
```

---

### 🔧 Paso 3: Refactorizar a Clean Architecture

**Tu tarea**: Usando las recomendaciones de IA, refactoriza el código legacy en 3 capas:

1. **Crear `repositorio_base.py`** (Protocol)
2. **Crear `servicio_tareas.py`** (Lógica de negocio)
3. **Refactorizar `api.py`** (Solo endpoints)

**Criterios de validación**:

```python
# Pregunta clave 1: ¿Puedes cambiar de JSON a SQLite cambiando 1 sola línea?
# Si NO → arquitectura incorrecta

# Pregunta clave 2: ¿El servicio importa RepositorioJSON o RepositorioSQLite?
# Si SÍ → violación de DIP

# Pregunta clave 3: ¿La API tiene lógica de negocio (if, cálculos, validaciones)?
# Si SÍ → violación de SRP
```

---

### 💾 Entregable

**Archivos a entregar**:
1. `repositorio_base.py` - Protocol con contrato
2. `repositorio_json_refactorizado.py` - Implementación concreta
3. `servicio_tareas_refactorizado.py` - Lógica de negocio
4. `api_refactorizado.py` - Solo endpoints

**Documento de refactorización**:

Crea `REFACTORING_NOTES.md` con:
- Lista de violaciones encontradas (con agente usado)
- Decisiones de diseño tomadas
- Antes/después de cada cambio clave
- Lecciones aprendidas

**Validación final**:

Ejecuta este prompt para confirmar que la refactorización es correcta:

```
Rol: Clean Architecture Enforcer

Valida que esta arquitectura refactorizada cumple SOLID:

Archivos:
[Pegar los 4 archivos]

Checklist:
1. ¿Hay un Protocol abstracto?
2. ¿El servicio depende solo del Protocol?
3. ¿La API solo llama al servicio?
4. ¿Cada capa tiene una sola responsabilidad?
5. ¿Se puede cambiar de repositorio con 1 línea?

Responde SÍ/NO para cada punto y justifica.
```

---

## Ejercicio 3: Implementar Caching con Decorator Pattern

### 📋 Contexto

Tu `RepositorioJSON` funciona, pero es lento (lee el archivo completo en cada operación). Quieres agregar cache **sin modificar** la implementación original.

**Objetivo**: Implementar un `RepositorioCache` que envuelve otro repositorio y cachea resultados.

---

### 🏗️ Paso 1: Diseñar el Decorator Pattern con IA

**Prompt**:

```
Rol: Arquitecto Python experto en patrones de diseño

Contexto:
Tengo un RepositorioTareas (Protocol con métodos: guardar, listar, obtener_por_id, eliminar, completar).
Quiero agregar cache en memoria para mejorar performance SIN modificar las implementaciones existentes.

Objetivo:
Diseña un RepositorioCache que:
- Implementa el mismo Protocol (es transparente)
- Envuelve otro repositorio (Decorator Pattern)
- Cachea resultados de listar() y obtener_por_id()
- Invalida cache cuando se modifica (guardar, eliminar, completar)

Requisitos:
- Debe cumplir el Protocol RepositorioTareas
- Constructor: __init__(self, repositorio_interno: RepositorioTareas)
- Cache simple: dict de Python (no Redis para este ejercicio)
- Docstrings que expliquen la estrategia de invalidación

Restricciones:
- NO modificar RepositorioMemoria, RepositorioJSON, RepositorioSQLite
- El servicio NO debe saber que hay cache (transparencia)

Formato:
```python
# api/repositorio_cache.py
# Código con explicación de cada decisión
```

Explica:
- Por qué Decorator Pattern es apropiado aquí
- Cuándo invalidar el cache (qué métodos)
- Limitaciones del cache simple (vs Redis)
```

---

### 🔨 Paso 2: Implementar y validar

**Código esperado** (esqueleto):

```python
# api/repositorio_cache.py
from typing import List, Optional, Dict
from api.repositorio_base import RepositorioTareas
from api.servicio_tareas import Tarea


class RepositorioCache:
    """Decorador que agrega cache a cualquier repositorio.

    Estrategia de cache:
    - listar(): cachea la lista completa
    - obtener_por_id(): cachea cada tarea por ID
    - guardar/eliminar/completar: invalidan cache completo

    Limitaciones:
    - Cache en memoria (se pierde al reiniciar)
    - No es thread-safe (solo para single-threaded apps)
    - Invalida TODO el cache en modificaciones (puede optimizarse)
    """

    def __init__(self, repositorio_interno: RepositorioTareas):
        self._repo = repositorio_interno
        self._cache_lista: Optional[List[Tarea]] = None
        self._cache_por_id: Dict[int, Tarea] = {}

    def _invalidar_cache(self) -> None:
        """Limpia todo el cache."""
        self._cache_lista = None
        self._cache_por_id.clear()

    def guardar(self, tarea: Tarea) -> None:
        self._repo.guardar(tarea)
        self._invalidar_cache()  # Modificación → invalidar

    def listar(self) -> List[Tarea]:
        if self._cache_lista is None:
            # Cache miss → cargar del repositorio interno
            self._cache_lista = self._repo.listar()
        return self._cache_lista.copy()  # Copia defensiva

    def obtener_por_id(self, id: int) -> Optional[Tarea]:
        if id not in self._cache_por_id:
            # Cache miss → cargar del repositorio interno
            tarea = self._repo.obtener_por_id(id)
            if tarea:
                self._cache_por_id[id] = tarea
        return self._cache_por_id.get(id)

    # TODO: Implementa eliminar y completar con invalidación
```

**Tu tarea**: Completa los métodos `eliminar` y `completar`.

---

### ✅ Paso 3: Validar transparencia (cumple Protocol)

**Test de intercambiabilidad**:

```python
# tests_integrations/test_repositorio_cache.py
import pytest
from api.repositorio_memoria import RepositorioMemoria
from api.repositorio_cache import RepositorioCache
from api.servicio_tareas import Tarea


def test_cache_es_transparente():
    """Valida que RepositorioCache cumple el mismo Protocol."""
    repo_base = RepositorioMemoria()
    repo_con_cache = RepositorioCache(repo_base)

    # Guardar a través del cache
    tarea = Tarea(id=0, nombre="Test", completada=False)
    repo_con_cache.guardar(tarea)

    # Listar desde el cache
    tareas = repo_con_cache.listar()
    assert len(tareas) == 1
    assert tareas[0].nombre == "Test"


def test_cache_mejora_performance():
    """Valida que el cache reduce accesos al repositorio interno."""
    repo_base = RepositorioMemoria()
    repo_con_cache = RepositorioCache(repo_base)

    # Guardar tarea
    tarea = Tarea(id=0, nombre="Cacheable", completada=False)
    repo_con_cache.guardar(tarea)

    # Primera llamada: cache miss
    tareas1 = repo_con_cache.listar()

    # Segunda llamada: cache hit (debería ser la misma lista cacheada)
    tareas2 = repo_con_cache.listar()

    # Verificar que el cache funciona (mismo contenido, no mismo objeto)
    assert tareas1 == tareas2
    assert tareas1 is not tareas2  # Copia defensiva
```

---

### 🚀 Paso 4: Usar el cache en la aplicación

**Modificar `api/dependencias.py`** (solo cambiar 1 línea):

```python
# ANTES (sin cache)
def obtener_servicio():
    repo = RepositorioJSON("tareas.json")
    return ServicioTareas(repo)

# DESPUÉS (con cache)
from api.repositorio_cache import RepositorioCache

def obtener_servicio():
    repo_base = RepositorioJSON("tareas.json")
    repo_con_cache = RepositorioCache(repo_base)  # Decorador
    return ServicioTareas(repo_con_cache)
```

**Pregunta clave**: ¿Tuviste que modificar `ServicioTareas` o `api.py`?

- ✅ **NO** → Decorator Pattern correcto (Open/Closed cumplido)
- ❌ **SÍ** → Violación de OCP, revisar diseño

---

### 💾 Entregable

**Archivos a crear**:
1. `api/repositorio_cache.py` (~100 líneas)
2. `tests_integrations/test_repositorio_cache.py` (~150 líneas)

**Documento de análisis**:

Crea `CACHE_DESIGN.md` con:

```markdown
# Diseño de Cache con Decorator Pattern

## Decisiones de diseño

### ¿Por qué Decorator Pattern?
[Explica por qué envolver en vez de modificar]

### Estrategia de invalidación
[Cuándo invalidar el cache y por qué]

### Limitaciones
[Qué NO hace este cache (thread-safety, TTL, LRU)]

## Performance

### Benchmark simple
```python
import time

repo_sin_cache = RepositorioJSON("tareas.json")
repo_con_cache = RepositorioCache(repo_sin_cache)

# Medir 100 lecturas sin cache
start = time.time()
for _ in range(100):
    repo_sin_cache.listar()
sin_cache_time = time.time() - start

# Medir 100 lecturas con cache
start = time.time()
for _ in range(100):
    repo_con_cache.listar()
con_cache_time = time.time() - start

print(f"Mejora: {sin_cache_time / con_cache_time:.2f}x más rápido")
```

### Mejoras futuras
- [ ] LRU cache (limitar tamaño)
- [ ] TTL (time-to-live)
- [ ] Invalidación selectiva (solo IDs modificados)
- [ ] Redis para cache distribuido
```

---

## 🏆 Criterios de Éxito General

Para considerar los 3 ejercicios completos, debes poder responder **SÍ** a todas estas preguntas:

### Ejercicio 1 (RepositorioSQLite)
- [ ] ¿Los 15 tests pasan para los 3 repositorios (Memoria, JSON, SQLite)?
- [ ] ¿Usas SQL parametrizado (no f-strings)?
- [ ] ¿Usas context managers para conexiones?
- [ ] ¿Puedes cambiar de JSON a SQLite cambiando 1 línea?

### Ejercicio 2 (Refactorización)
- [ ] ¿Identificaste al menos 5 violaciones de SOLID en el código legacy?
- [ ] ¿Tu arquitectura refactorizada cumple Clean Architecture?
- [ ] ¿El servicio depende del Protocol, NO de clases concretas?
- [ ] ¿Cada capa tiene una sola responsabilidad?

### Ejercicio 3 (Cache)
- [ ] ¿El cache es transparente (cumple el Protocol)?
- [ ] ¿NO modificaste ServicioTareas ni api.py para agregar cache?
- [ ] ¿El cache invalida correctamente en modificaciones?
- [ ] ¿Mediste la mejora de performance (ej: 10x más rápido)?

---

## 📚 Recursos Adicionales

**Agentes educacionales recomendados**:
- `.claude/agents/educational/python-best-practices-coach.md` → Valida Protocols, type hints
- `.claude/agents/educational/fastapi-design-coach.md` → Revisa separación de capas
- `.claude/agents/educational/database-orm-specialist.md` → Valida SQL y manejo de BD

**Patrones de diseño**:
- Repository Pattern: https://martinfowler.com/eaaCatalog/repository.html
- Decorator Pattern: https://refactoring.guru/design-patterns/decorator/python
- Dependency Injection: https://fastapi.tiangolo.com/tutorial/dependencies/

**Documentación Python**:
- PEP 544 (Protocols): https://peps.python.org/pep-0544/
- sqlite3 module: https://docs.python.org/3/library/sqlite3.html
- Context managers: https://docs.python.org/3/reference/datamodel.html#context-managers

---

## 💡 Tips para usar IA efectivamente

### Prompts iterativos
No esperes que IA genere código perfecto en el primer intento. Itera:

1. **Prompt inicial**: Genera estructura básica
2. **Validar con agente**: Identifica problemas
3. **Prompt de corrección**: "Corrige [problema específico]"
4. **Repetir** hasta que no haya violaciones

### Pregunta "¿Por qué?"
Siempre pide a IA que justifique sus decisiones:

```
¿Por qué usaste X en vez de Y?
¿Qué pasaría si cambio Z?
¿Qué limitaciones tiene este enfoque?
```

### Valida con múltiples agentes
Usa diferentes agentes para diferentes aspectos:

- **Python Best Practices Coach**: Sintaxis, type hints, PEP 8
- **FastAPI Design Coach**: Arquitectura, separación de capas
- **Database ORM Specialist**: SQL, manejo de BD

Cada agente detecta problemas diferentes → cobertura completa.

---

**¡Éxito con los ejercicios! 🚀**
