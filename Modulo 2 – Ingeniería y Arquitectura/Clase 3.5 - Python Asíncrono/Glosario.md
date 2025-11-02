# Glosario - Python Asíncrono

## A

### Asynchronous (Asíncrono)
Modelo de programación donde las operaciones pueden ejecutarse sin bloquear el hilo principal. Permite que múltiples tareas progresen concurrentemente sin esperar a que cada una termine.

**Analogía**: Como un camarero que toma múltiples órdenes sin esperar a que la cocina termine cada plato.

### async
Palabra clave de Python que declara una función como coroutine. Funciones marcadas con `async` deben ser ejecutadas con `await` o a través del event loop.

```python
async def mi_funcion():  # Esto es una coroutine
    return "Hola"
```

### await
Palabra clave que pausa la ejecución de una coroutine hasta que otra coroutine complete. Solo puede usarse dentro de funciones `async`.

```python
async def main():
    resultado = await mi_funcion()  # Espera a que complete
```

### asyncio
Librería estándar de Python para escribir código asíncrono usando el patrón async/await. Provee el event loop y utilidades para manejar coroutines.

```python
import asyncio
asyncio.run(mi_coroutine())
```

### asyncio.gather()
Función que ejecuta múltiples coroutines en paralelo y retorna sus resultados cuando todas completan.

```python
resultados = await asyncio.gather(
    tarea1(),
    tarea2(),
    tarea3()
)
```

### asyncio.sleep()
Versión asíncrona de `time.sleep()`. Pausa la coroutine sin bloquear el event loop.

```python
await asyncio.sleep(1)  # ✅ No bloquea event loop
time.sleep(1)           # ❌ Bloquea event loop
```

### asyncio.wait_for()
Ejecuta una coroutine con un timeout máximo. Lanza `asyncio.TimeoutError` si excede el tiempo.

```python
resultado = await asyncio.wait_for(mi_tarea(), timeout=5.0)
```

## B

### Blocking Call (Llamada Bloqueante)
Operación que detiene la ejecución del hilo hasta que complete. En async Python, las llamadas bloqueantes detienen todo el event loop.

**Ejemplos de blocking calls**:
- `time.sleep()` (usa `await asyncio.sleep()` en su lugar)
- `requests.get()` (usa `httpx.AsyncClient` en su lugar)
- `open()` para archivos (usa `aiofiles` en su lugar)

## C

### Concurrency (Concurrencia)
Capacidad de manejar múltiples tareas progresando durante el mismo período, aunque no necesariamente al mismo tiempo exacto.

**Concurrencia ≠ Paralelismo**:
- **Concurrencia**: Gestionar múltiples tareas (1 camarero, N mesas)
- **Paralelismo**: Ejecutar múltiples tareas simultáneamente (N camareros, N mesas)

### Coroutine (Corrutina)
Función especial que puede pausar su ejecución y ceder control al event loop. Se define con `async def`.

```python
async def mi_coroutine():
    await asyncio.sleep(1)
    return "Completado"
```

**Características**:
- Se crea con `async def`
- Se ejecuta con `await` o `asyncio.run()`
- Puede pausarse en puntos `await`
- Retorna un objeto coroutine al ser llamada (no ejecuta inmediatamente)

### CPU-bound
Tarea limitada por el poder de cómputo del CPU. Ejemplos: cálculos matemáticos, procesamiento de imágenes, algoritmos complejos.

**Async NO ayuda con CPU-bound**: Usa `multiprocessing` en su lugar.

## D

### Deadlock
Situación donde dos o más tareas están esperándose mutuamente, causando un bloqueo permanente.

```python
# ❌ Ejemplo de deadlock
async def deadlock():
    await deadlock()  # Espera infinitamente a sí mismo
```

## E

### Event Loop (Bucle de Eventos)
Motor central de asyncio que ejecuta y coordina todas las coroutines. Maneja qué tarea ejecutar, cuándo pausarla y cuándo retomarla.

**Analogía**: Director de orquesta que coordina cuándo cada músico debe tocar.

**Funciones clave**:
- Ejecuta coroutines
- Maneja I/O asíncrono
- Programa callbacks
- Coordina tasks concurrentes

```python
# Obtener el event loop actual
loop = asyncio.get_event_loop()

# Ejecutar coroutine en el event loop
asyncio.run(mi_coroutine())  # Crea y maneja event loop automáticamente
```

## F

### Future
Objeto que representa el resultado eventual de una operación asíncrona. Similar a una Promise en JavaScript.

```python
future = asyncio.Future()
await future  # Espera hasta que future tenga resultado
```

## G

### gather()
Ver **asyncio.gather()**.

## I

### I/O-bound
Tarea limitada por operaciones de entrada/salida (Input/Output). Ejemplos: llamadas a APIs, lecturas de archivos, consultas a bases de datos.

**Async es ideal para I/O-bound**: Las tareas esperan respuestas, permitiendo que el event loop ejecute otras mientras tanto.

## N

### Non-blocking (No Bloqueante)
Operación que no detiene la ejecución del programa mientras espera. Permite que otras tareas progresen mientras espera.

```python
# ✅ Non-blocking
await asyncio.sleep(1)  # Libera event loop

# ❌ Blocking
time.sleep(1)  # Bloquea event loop
```

## P

### Parallelism (Paralelismo)
Ejecución simultánea de múltiples tareas en múltiples CPUs/cores. Diferente de concurrencia.

**En Python**:
- **Async**: Concurrencia (1 thread)
- **Threading**: Concurrencia (1 CPU, N threads - limitado por GIL)
- **Multiprocessing**: Paralelismo real (N CPUs)

## R

### Race Condition
Comportamiento impredecible cuando múltiples tareas acceden/modifican datos compartidos sin sincronización adecuada.

**Prevención**:
```python
lock = asyncio.Lock()

async with lock:
    # Acceso exclusivo a recurso compartido
    shared_data += 1
```

## S

### Semaphore (Semáforo)
Mecanismo de sincronización que limita el número de tareas concurrentes accediendo a un recurso.

```python
semaphore = asyncio.Semaphore(5)  # Máximo 5 tareas concurrentes

async with semaphore:
    # Solo 5 tareas pueden estar aquí simultáneamente
    await operacion_limitada()
```

**Uso común**: Rate limiting, control de concurrencia.

### Synchronous (Síncrono)
Modelo de programación donde las operaciones se ejecutan secuencialmente, una después de otra, bloqueando hasta completar.

```python
# Sync - cada operación espera a la anterior
resultado1 = operacion1()
resultado2 = operacion2()  # Espera a que operacion1 complete
```

## T

### Task (Tarea)
Wrapper alrededor de una coroutine que la ejecuta en el event loop. Permite mayor control y cancelación.

```python
task = asyncio.create_task(mi_coroutine())
resultado = await task

# Cancelar task
task.cancel()
```

### Timeout
Tiempo máximo permitido para que una operación complete. Útil para prevenir esperas infinitas.

```python
try:
    resultado = await asyncio.wait_for(
        operacion_lenta(),
        timeout=5.0
    )
except asyncio.TimeoutError:
    print("Operación cancelada por timeout")
```

## Conceptos Relacionados

### GIL (Global Interpreter Lock)
Mecanismo de CPython que permite que solo un thread ejecute código Python a la vez. Por esto:

- **Threading en Python**: NO da paralelismo real para CPU-bound
- **Async en Python**: Funciona bien porque usa 1 solo thread
- **Multiprocessing**: Evita GIL usando múltiples procesos

### Context Manager Async
Versión asíncrona de context managers (`with`). Usa `async with` para manejar recursos async.

```python
# Sync context manager
with open("archivo.txt") as f:
    contenido = f.read()

# Async context manager
async with aiofiles.open("archivo.txt") as f:
    contenido = await f.read()
```

### Generator vs Async Generator
- **Generator**: Usa `yield`, se consume con `for`
- **Async Generator**: Usa `yield` en función `async`, se consume con `async for`

```python
# Generator normal
def mi_gen():
    yield 1
    yield 2

# Async generator
async def mi_async_gen():
    yield 1
    await asyncio.sleep(1)
    yield 2

# Consumir
async for valor in mi_async_gen():
    print(valor)
```

## Comparaciones Útiles

### async/await vs Threading vs Multiprocessing

| Característica | async/await | Threading | Multiprocessing |
|---------------|-------------|-----------|-----------------|
| **Ideal para** | I/O-bound | I/O-bound (legacy) | CPU-bound |
| **Threads** | 1 | N | 1 por proceso |
| **Procesos** | 1 | 1 | N |
| **Overhead** | Muy bajo | Medio | Alto |
| **Complejidad** | Media | Alta | Alta |
| **GIL** | No afecta | Limitado por GIL | Sin GIL |

### Librerías Sync vs Async

| Sync | Async | Uso |
|------|-------|-----|
| `requests` | `httpx.AsyncClient` | HTTP requests |
| `open()` | `aiofiles.open()` | Archivos |
| `psycopg2` | `asyncpg` | PostgreSQL |
| `pymongo` | `motor` | MongoDB |
| `time.sleep()` | `asyncio.sleep()` | Delays |
| `sqlite3` | `aiosqlite` | SQLite |

## Errores Comunes

### "RuntimeWarning: coroutine was never awaited"
**Causa**: Llamaste una coroutine sin `await` o sin ejecutarla en event loop.

**Solución**:
```python
# ❌ Error
resultado = mi_coroutine()

# ✅ Correcto
resultado = await mi_coroutine()
```

### "RuntimeError: asyncio.run() cannot be called from a running event loop"
**Causa**: Intentaste usar `asyncio.run()` dentro de una función async.

**Solución**:
```python
# ❌ Error
async def malo():
    asyncio.run(otra_coroutine())

# ✅ Correcto
async def bueno():
    await otra_coroutine()
```

### "Task was destroyed but it is pending"
**Causa**: Task fue cancelada sin esperar su cancelación.

**Solución**:
```python
task = asyncio.create_task(mi_coroutine())
task.cancel()
try:
    await task
except asyncio.CancelledError:
    pass  # Manejado correctamente
```

## Recursos Adicionales

- [asyncio — Asynchronous I/O](https://docs.python.org/3/library/asyncio.html)
- [PEP 492 – Coroutines with async and await syntax](https://peps.python.org/pep-0492/)
- [FastAPI Async Guide](https://fastapi.tiangolo.com/async/)

---

**💡 Tip**: Marca esta página como referencia rápida. La programación asíncrona tiene terminología específica que toma tiempo dominar.
