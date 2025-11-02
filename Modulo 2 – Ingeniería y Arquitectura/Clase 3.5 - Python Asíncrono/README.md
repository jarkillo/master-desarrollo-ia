# Clase 3.5 - Python Asíncrono

Clase intermedia entre **Clase 3 (Arquitectura Limpia)** y **Clase 4 (SOLID en FastAPI)** que enseña programación asíncrona en Python con async/await.

## 🎯 ¿Por Qué Esta Clase?

**Problema identificado**: FastAPI es fundamentalmente async, pero el programa no enseñaba async/await antes de usarlo. Esto causaba que estudiantes usaran endpoints async sin entender por qué o cómo optimizarlos.

**Solución**: Esta clase llena el gap crítico enseñando:
- Event loop y cómo funciona
- Coroutines y async/await
- Cuándo usar async vs sync
- Patrones async en FastAPI
- Performance optimization con paralelización

## 📂 Estructura

```
Clase 3.5 - Python Asíncrono/
├── Clase 3.5 - Python Asíncrono.md  # Contenido teórico principal (~4h)
├── EJERCICIOS.md                     # 5+ ejercicios prácticos progresivos
├── AI_WORKFLOW.md                    # 40% integración con IA
├── Glosario.md                       # Términos clave async/await
├── README.md                         # Este archivo
├── examples/
│   ├── basic_async.py               # Async básico: secuencial vs paralelo
│   └── fastapi_async.py             # Endpoints FastAPI async
├── tests/
│   ├── conftest.py                  # Configuración pytest
│   ├── test_basic_async.py          # Tests para 01_basic_async.py
│   └── test_fastapi_async.py        # Tests para 02_fastapi_async.py
└── api/                              # (Vacío - para ejercicios del estudiante)
```

## 🚀 Quick Start

### 1. Leer Contenido Teórico

```bash
# Leer el contenido principal (4 horas de material)
cat "Clase 3.5 - Python Asíncrono.md"
```

### 2. Ejecutar Ejemplos

```bash
# Ejemplo 1: Async básico
python examples/basic_async.py

# Ejemplo 2: FastAPI async
uvicorn examples.fastapi_async:app --reload
# Visita http://localhost:8000/docs
```

### 3. Ejecutar Tests

```bash
# Todos los tests
pytest tests/ -v

# Solo tests de async básico
pytest tests/test_basic_async.py -v

# Solo tests de FastAPI
pytest tests/test_fastapi_async.py -v

# Con coverage
pytest tests/ --cov=examples --cov-report=term-missing
```

### 4. Hacer Ejercicios

```bash
# Ver ejercicios prácticos
cat EJERCICIOS.md

# Los ejercicios van de ⭐ (principiante) a ⭐⭐⭐⭐ (experto)
# Empieza por el Ejercicio 1 y avanza progresivamente
```

### 5. Usar IA para Aprender

```bash
# Ver workflow de IA (40% del contenido)
cat AI_WORKFLOW.md

# Incluye prompts específicos para:
# - Generar código async
# - Debugging
# - Refactoring sync→async
# - Testing
```

## 📖 Contenido Destacado

### 1. Event Loop Explicado Claramente

Analogía del "director de orquesta" para entender cómo asyncio coordina tareas:

```python
# Event loop coordina múltiples tareas sin bloquear
async def tarea1():
    await asyncio.sleep(1)  # Pausa tarea1, loop ejecuta tarea2

async def tarea2():
    await asyncio.sleep(1)  # Pausa tarea2, loop retoma tarea1
```

### 2. Comparación Sync vs Async

Ejemplos lado a lado mostrando mejoras de performance:

```python
# ❌ Sync: 3 segundos total
def sync_version():
    requests.get(url1)  # 1s
    requests.get(url2)  # 1s
    requests.get(url3)  # 1s

# ✅ Async: 1 segundo total (en paralelo)
async def async_version():
    await asyncio.gather(
        client.get(url1),
        client.get(url2),
        client.get(url3)
    )
```

### 3. FastAPI Async Patterns

Endpoints optimizados con paralelización:

```python
@app.get("/dashboard")
async def dashboard():
    # Consultar 3 servicios en paralelo
    usuarios, productos, pedidos = await asyncio.gather(
        get_usuarios(),
        get_productos(),
        get_pedidos()
    )
    return {"usuarios": usuarios, ...}
```

### 4. Debugging Async Code

Errores comunes y cómo solucionarlos:

- `RuntimeWarning: coroutine was never awaited`
- `RuntimeError: asyncio.run() cannot be called from running event loop`
- Blocking calls en async functions

### 5. Testing Async

Usando pytest-asyncio:

```python
@pytest.mark.asyncio
async def test_mi_funcion_async():
    resultado = await mi_funcion_async()
    assert resultado == "esperado"
```

## 🎯 Objetivos de Aprendizaje

Después de esta clase, podrás:

- ✅ Explicar qué es el event loop y cómo funciona
- ✅ Escribir coroutines con `async`/`await`
- ✅ Decidir cuándo usar async vs sync
- ✅ Optimizar código con `asyncio.gather()`
- ✅ Aplicar patrones async en FastAPI
- ✅ Debuggear errores async comunes
- ✅ Testear código asíncrono con pytest-asyncio

## 📊 Ejercicios Progresivos

| Ejercicio | Dificultad | Tiempo | Conceptos |
|-----------|------------|--------|-----------|
| 1. Primera Coroutine | ⭐ | 15 min | async/await, gather() |
| 2. API de Clima | ⭐⭐ | 30 min | FastAPI async, timeout |
| 3. Procesador de Imágenes | ⭐⭐ | 45 min | Semaphore, progreso |
| 4. Rate Limiter | ⭐⭐⭐ | 60 min | Lock, thread-safety |
| 5. Notificaciones | ⭐⭐⭐ | 90 min | Reintentos, logging |
| Bonus. Web Scraper | ⭐⭐⭐⭐ | 120 min | Queue, workers, httpx |

## 🤖 Integración con IA (40%)

Esta clase incluye **40% de contenido con IA**:

- **Prompts específicos** para cada concepto
- **Agentes educativos** para review de código
- **Workflow completo** de desarrollo con IA
- **Ejercicios guiados** con IA como par de programación

Ver `AI_WORKFLOW.md` para detalles.

## 🔗 Conexión con Otras Clases

### Prerequisito: Clase 3 - Arquitectura Limpia

Necesitas entender:
- Separación de capas (API, Servicio, Repositorio)
- Dependency Inversion Principle
- FastAPI básico

### Siguiente: Clase 4 - SOLID en FastAPI

Con conocimiento de async, ahora podrás:
- Implementar repositorios async (conexiones DB)
- Optimizar servicios con paralelización
- Diseñar endpoints FastAPI eficientemente

## 📚 Recursos Adicionales

### Documentación Oficial

- [asyncio — Asynchronous I/O](https://docs.python.org/3/library/asyncio.html)
- [FastAPI Async Guide](https://fastapi.tiangolo.com/async/)
- [PEP 492 – Coroutines with async and await](https://peps.python.org/pep-0492/)

### Librerías Async Recomendadas

- **HTTP**: `httpx` (async requests)
- **Files**: `aiofiles` (async file I/O)
- **PostgreSQL**: `asyncpg` (async database)
- **MongoDB**: `motor` (async motor driver)
- **Redis**: `aioredis` (async Redis client)

### Herramientas

- **pytest-asyncio**: Testing async code
- **httpx**: Async HTTP client
- **uvicorn**: ASGI server para FastAPI

## ⚙️ Instalación de Dependencias

```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Instalar dependencias
pip install fastapi uvicorn pytest pytest-asyncio httpx aiofiles
```

**Nota sobre tests**: Los tests requieren `pytest-asyncio` que puede no estar en el `requirements.txt` global del proyecto. Si los tests fallan, instala: `pip install pytest-asyncio`

## 🎓 Tips de Estudio

1. **Empieza con teoría**: Lee `Clase 3.5 - Python Asíncrono.md` primero
2. **Practica con ejemplos**: Ejecuta `01_basic_async.py` y `02_fastapi_async.py`
3. **Haz ejercicios**: Resuelve en orden (1 → 2 → 3 → 4 → 5)
4. **Usa IA**: Consulta `AI_WORKFLOW.md` para prompts efectivos
5. **Consulta glosario**: `Glosario.md` cuando veas términos nuevos
6. **Ejecuta tests**: Verifica tu comprensión con pytest

## 🐛 Troubleshooting

### Error: "RuntimeWarning: coroutine was never awaited"

**Solución**: Agregaste `await` antes de la coroutine:

```python
# ❌ Error
resultado = mi_funcion_async()

# ✅ Correcto
resultado = await mi_funcion_async()
```

### Error: "pytest: command not found"

**Solución**: Instala pytest-asyncio:

```bash
pip install pytest pytest-asyncio
```

### Error: "No module named 'httpx'"

**Solución**: Instala httpx:

```bash
pip install httpx
```

## 📝 Notas Importantes

- **Async NO es más rápido para CPU-bound**: Solo ayuda con I/O-bound
- **No bloquees el event loop**: Usa `await asyncio.sleep()`, no `time.sleep()`
- **FastAPI maneja async automáticamente**: Solo escribe `async def` y FastAPI se encarga
- **Testing async requiere pytest-asyncio**: Marca tests con `@pytest.mark.asyncio`

## 🎯 Evaluación

Para aprobar esta clase, debes:

- ✅ Completar al menos 3 de 5 ejercicios
- ✅ Pasar todos los tests (`pytest tests/ -v`)
- ✅ Demostrar comprensión de event loop
- ✅ Usar `asyncio.gather()` correctamente
- ✅ Aplicar async en al menos 1 endpoint FastAPI

## 🤝 Contribuciones

Esta clase fue creada para llenar un gap crítico en el programa. Si encuentras errores o mejoras:

1. Reporta issues en Linear
2. Sugiere mejoras en ejercicios
3. Comparte prompts efectivos de IA

---

**Duración estimada**: 4 horas de contenido teórico + 3-5 horas de ejercicios prácticos

**Siguiente clase**: [Clase 4 - SOLID en FastAPI](../Clase%204%20-%20SOLID%20en%20FastAPI/)
