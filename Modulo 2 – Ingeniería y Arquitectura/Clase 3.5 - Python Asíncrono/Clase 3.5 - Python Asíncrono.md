# Clase 3.5 - Python Asíncrono: Event Loop, Coroutines y Async/Await

**Duración estimada**: 4 horas
**Nivel**: Intermedio
**Prerequisitos**: Clase 3 - Arquitectura limpia

## 🎯 Objetivos de Aprendizaje

Al finalizar esta clase serás capaz de:

1. Entender qué es la programación asíncrona y cuándo usarla
2. Comprender el event loop de Python y cómo funciona
3. Escribir y ejecutar coroutines con `async`/`await`
4. Aplicar patrones asíncronos en FastAPI
5. Decidir cuándo usar async vs sync en tu código
6. Depurar y testear código asíncrono

## 📚 Contenido

### 1. Introducción a la Programación Asíncrona

#### ¿Por qué Async?

Imagina un restaurante (tu aplicación):

**Modelo Síncrono (Sync)**:
```
Camarero → Toma orden → Espera en cocina → Sirve plato → Siguiente cliente
                         ⏰ BLOQUEADO esperando
```

**Modelo Asíncrono (Async)**:
```
Camarero → Toma orden 1 → Da orden a cocina
        ↓
        Toma orden 2 → Da orden a cocina
        ↓
        Toma orden 3 → Da orden a cocina
        ↓
        Sirve plato 1 (cuando está listo)
        Sirve plato 2 (cuando está listo)
```

**El camarero no espera. Maneja múltiples órdenes simultáneamente.**

#### Cuándo Usar Async

✅ **USA ASYNC cuando**:
- Haces llamadas a APIs externas (HTTP requests)
- Lees/escribes archivos
- Consultas a bases de datos
- Operaciones de I/O (Input/Output)
- Tienes muchas operaciones que esperan (I/O-bound)

❌ **NO USES ASYNC cuando**:
- Haces cálculos pesados (CPU-bound)
- Operaciones que no esperan nada
- Código legacy que no soporta async

**Regla de oro**: Si tu código "espera" (network, disk, database), usa async. Si "calcula" (math, algorithms), usa sync.

### 2. El Event Loop: El Corazón de Async Python

#### ¿Qué es el Event Loop?

El **event loop** es como un director de orquesta que coordina todas las tareas asíncronas.

```python
import asyncio

# El event loop es quien ejecuta tus coroutines
# Piensa en él como el "motor" de la asincronía
```

**Analogía**: El event loop es como el despachador de un call center:
- Recibe llamadas (tasks)
- Las pone en espera cuando esperan respuesta
- Atiende otras llamadas mientras tanto
- Retoma las llamadas cuando la respuesta llega

#### Cómo Funciona

```
1. Event Loop recibe Task A (coroutine)
2. Ejecuta Task A hasta que hace "await" (espera)
3. Task A se pausa → Event Loop toma Task B
4. Ejecuta Task B hasta que hace "await"
5. Task B se pausa → Event Loop toma Task C
6. Mientras, Task A recibe respuesta → Event Loop la retoma
7. Task A termina → Event Loop continúa con B, C, etc.
```

**Importante**: Solo hay UN event loop por thread. Todas las coroutines comparten el mismo loop.

### 3. Coroutines y Async/Await

#### Definir una Coroutine

```python
# Función normal (síncrona)
def saludar():
    return "Hola"

# Coroutine (asíncrona)
async def saludar_async():
    return "Hola"
```

**Diferencia clave**:
- `def` → función normal, se ejecuta inmediatamente
- `async def` → coroutine, necesita ser "awaited" o ejecutada por el event loop

#### Await: Esperando Resultados

```python
import asyncio

async def obtener_dato():
    await asyncio.sleep(1)  # Simula espera de I/O
    return "Dato obtenido"

async def main():
    # ❌ INCORRECTO: Esto NO ejecuta la coroutine
    resultado = obtener_dato()
    print(type(resultado))  # <class 'coroutine'>

    # ✅ CORRECTO: Usar await para ejecutar y obtener resultado
    resultado = await obtener_dato()
    print(resultado)  # "Dato obtenido"

# Ejecutar el event loop
asyncio.run(main())
```

**Regla de oro**:
- Si una función es `async`, debes llamarla con `await` desde otra función `async`
- `await` solo se puede usar dentro de funciones `async`

### 4. Patrones Async Comunes

#### Pattern 1: Ejecutar Múltiples Tareas en Paralelo

```python
import asyncio
import time

async def tarea_lenta(nombre: str, segundos: int):
    print(f"{nombre} iniciada...")
    await asyncio.sleep(segundos)
    print(f"{nombre} completada!")
    return f"Resultado de {nombre}"

async def ejemplo_secuencial():
    """❌ SECUENCIAL: Tarda 6 segundos"""
    inicio = time.time()

    resultado1 = await tarea_lenta("Tarea 1", 2)
    resultado2 = await tarea_lenta("Tarea 2", 2)
    resultado3 = await tarea_lenta("Tarea 3", 2)

    print(f"Tiempo total: {time.time() - inicio:.2f}s")  # ~6 segundos

async def ejemplo_paralelo():
    """✅ PARALELO: Tarda 2 segundos"""
    inicio = time.time()

    # gather() ejecuta todas las tareas en paralelo
    resultados = await asyncio.gather(
        tarea_lenta("Tarea 1", 2),
        tarea_lenta("Tarea 2", 2),
        tarea_lenta("Tarea 3", 2)
    )

    print(f"Tiempo total: {time.time() - inicio:.2f}s")  # ~2 segundos
    print(f"Resultados: {resultados}")

# asyncio.run(ejemplo_secuencial())
# asyncio.run(ejemplo_paralelo())
```

**Diferencia clave**:
- `await tarea()` → ejecuta secuencialmente (una después de otra)
- `await asyncio.gather(tarea1(), tarea2())` → ejecuta en paralelo

#### Pattern 2: Timeout en Operaciones Async

```python
import asyncio

async def operacion_lenta():
    await asyncio.sleep(10)  # Tarda 10 segundos
    return "Resultado"

async def con_timeout():
    try:
        # Espera máximo 3 segundos
        resultado = await asyncio.wait_for(
            operacion_lenta(),
            timeout=3.0
        )
        print(resultado)
    except asyncio.TimeoutError:
        print("❌ Operación cancelada por timeout")

# asyncio.run(con_timeout())
```

#### Pattern 3: Manejo de Errores en Async

```python
import asyncio

async def tarea_con_error():
    await asyncio.sleep(1)
    raise ValueError("Algo salió mal")

async def tarea_exitosa():
    await asyncio.sleep(1)
    return "OK"

async def manejar_errores():
    # gather() con return_exceptions=True captura errores
    resultados = await asyncio.gather(
        tarea_exitosa(),
        tarea_con_error(),
        tarea_exitosa(),
        return_exceptions=True  # No detiene todo si una falla
    )

    for i, resultado in enumerate(resultados):
        if isinstance(resultado, Exception):
            print(f"Tarea {i}: ❌ Error - {resultado}")
        else:
            print(f"Tarea {i}: ✅ {resultado}")

# asyncio.run(manejar_errores())
```

### 5. Async en FastAPI

#### FastAPI es Async por Defecto

FastAPI está diseñado para aprovechar async/await desde el principio:

```python
from fastapi import FastAPI

app = FastAPI()

# ✅ Endpoint async (recomendado para I/O)
@app.get("/async")
async def endpoint_async():
    # Simulamos llamada a DB o API externa
    await asyncio.sleep(0.1)
    return {"mensaje": "Respuesta async"}

# ✅ Endpoint sync (válido para cálculos rápidos)
@app.get("/sync")
def endpoint_sync():
    # Cálculos simples sin I/O
    return {"mensaje": "Respuesta sync"}
```

**Cuándo usar cada uno**:
- **`async def`**: Cuando haces I/O (DB, HTTP, archivos)
- **`def`**: Cuando haces cálculos simples sin I/O

#### Ejemplo Real: Llamadas a DB Async

```python
from fastapi import FastAPI, Depends
from typing import List
import asyncio

app = FastAPI()

# Simulación de base de datos async
async def obtener_usuarios_db() -> List[dict]:
    """Simula consulta async a DB"""
    await asyncio.sleep(0.5)  # Simula latencia de DB
    return [
        {"id": 1, "nombre": "Ana"},
        {"id": 2, "nombre": "Luis"},
    ]

async def obtener_pedidos_db(usuario_id: int) -> List[dict]:
    """Simula consulta async a DB"""
    await asyncio.sleep(0.3)
    return [
        {"id": 101, "usuario_id": usuario_id, "total": 50.0},
        {"id": 102, "usuario_id": usuario_id, "total": 75.5},
    ]

# ❌ LENTO: Consultas secuenciales
@app.get("/reporte-lento")
async def reporte_lento():
    usuarios = await obtener_usuarios_db()  # 0.5s

    reportes = []
    for usuario in usuarios:
        pedidos = await obtener_pedidos_db(usuario["id"])  # 0.3s x usuario
        reportes.append({
            "usuario": usuario["nombre"],
            "pedidos": pedidos
        })

    # Tiempo total: 0.5s + (0.3s * 2) = 1.1s
    return {"reportes": reportes}

# ✅ RÁPIDO: Consultas en paralelo
@app.get("/reporte-rapido")
async def reporte_rapido():
    usuarios = await obtener_usuarios_db()  # 0.5s

    # Ejecutar todas las consultas de pedidos en paralelo
    tareas_pedidos = [
        obtener_pedidos_db(usuario["id"])
        for usuario in usuarios
    ]
    resultados_pedidos = await asyncio.gather(*tareas_pedidos)  # 0.3s en paralelo

    reportes = [
        {"usuario": usuarios[i]["nombre"], "pedidos": resultados_pedidos[i]}
        for i in range(len(usuarios))
    ]

    # Tiempo total: 0.5s + 0.3s = 0.8s (27% más rápido)
    return {"reportes": reportes}
```

**Mejora**: De 1.1s a 0.8s (27% más rápido) usando `asyncio.gather()`

#### Async con Dependency Injection

```python
from fastapi import FastAPI, Depends

app = FastAPI()

# Dependencia async
async def obtener_session_db():
    """Simula conexión async a DB"""
    print("📂 Abriendo sesión DB...")
    await asyncio.sleep(0.1)
    yield "DB_SESSION"
    print("📂 Cerrando sesión DB...")

@app.get("/usuarios")
async def listar_usuarios(db: str = Depends(obtener_session_db)):
    """
    FastAPI ejecuta la dependencia async automáticamente
    """
    await asyncio.sleep(0.2)  # Simula query
    return {"usuarios": ["Ana", "Luis"], "db": db}
```

**Ventaja**: FastAPI maneja automáticamente el ciclo de vida de dependencias async.

### 6. Async vs Sync: Comparación Práctica

#### Ejemplo 1: Consultas a API Externa

```python
import asyncio
import httpx  # Cliente HTTP async
import requests  # Cliente HTTP sync
import time

# ❌ SYNC: Secuencial y lento
def obtener_datos_sync(urls: list[str]):
    inicio = time.time()
    resultados = []

    for url in urls:
        response = requests.get(url)
        resultados.append(response.json())

    print(f"Sync: {time.time() - inicio:.2f}s")
    return resultados

# ✅ ASYNC: Paralelo y rápido
async def obtener_datos_async(urls: list[str]):
    inicio = time.time()

    async with httpx.AsyncClient() as client:
        tareas = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tareas)
        resultados = [r.json() for r in responses]

    print(f"Async: {time.time() - inicio:.2f}s")
    return resultados

# Ejemplo de uso
urls = [
    "https://api.example.com/usuarios",
    "https://api.example.com/productos",
    "https://api.example.com/pedidos",
]

# obtener_datos_sync(urls)  # ~3 segundos (1s x 3)
# asyncio.run(obtener_datos_async(urls))  # ~1 segundo (todas en paralelo)
```

**Resultado**: Async es ~3x más rápido para I/O paralelo.

#### Ejemplo 2: Procesamiento de Archivos

```python
import asyncio
import aiofiles  # Librería para archivos async

# ❌ SYNC: Lectura secuencial
def leer_archivos_sync(archivos: list[str]):
    contenidos = []
    for archivo in archivos:
        with open(archivo, 'r') as f:
            contenidos.append(f.read())
    return contenidos

# ✅ ASYNC: Lectura paralela
async def leer_archivos_async(archivos: list[str]):
    async def leer_archivo(path: str):
        async with aiofiles.open(path, 'r') as f:
            return await f.read()

    tareas = [leer_archivo(archivo) for archivo in archivos]
    contenidos = await asyncio.gather(*tareas)
    return contenidos
```

### 7. Debugging Async Code

#### Problema Común 1: RuntimeWarning Coroutine Never Awaited

```python
# ❌ ERROR: Coroutine no ejecutada
async def mi_funcion():
    return "Hola"

def main():
    resultado = mi_funcion()  # ⚠️ RuntimeWarning: coroutine 'mi_funcion' was never awaited
    print(resultado)  # <coroutine object>

# ✅ SOLUCIÓN: Usar await o asyncio.run()
async def main_correcto():
    resultado = await mi_funcion()
    print(resultado)  # "Hola"

asyncio.run(main_correcto())
```

#### Problema Común 2: Deadlock en Async

```python
# ❌ DEADLOCK: Esperando a sí mismo
async def deadlock():
    await deadlock()  # Recursión infinita

# ✅ SOLUCIÓN: Condición de salida
async def recursion_correcta(n: int):
    if n <= 0:
        return
    await asyncio.sleep(0.1)
    await recursion_correcta(n - 1)
```

#### Herramientas de Debug

```python
import asyncio

# Activar modo debug
asyncio.run(main(), debug=True)

# Ver tareas pendientes
pending = asyncio.all_tasks()
for task in pending:
    print(task)

# Timeout global
asyncio.run(main(), timeout=5.0)
```

### 8. Testing Código Async

#### Pytest con Pytest-asyncio

```python
# tests/test_async.py
import pytest
import asyncio

# Marcar test como async
@pytest.mark.asyncio
async def test_funcion_async():
    resultado = await mi_funcion_async()
    assert resultado == "esperado"

# Fixtures async
@pytest.fixture
async def db_session():
    """Simula conexión async a DB"""
    session = await crear_session()
    yield session
    await cerrar_session(session)

@pytest.mark.asyncio
async def test_con_fixture(db_session):
    usuarios = await obtener_usuarios(db_session)
    assert len(usuarios) > 0
```

### 9. Best Practices

#### ✅ DO: Buenas Prácticas

1. **Usa async para I/O, sync para CPU**
   ```python
   # ✅ Async para I/O
   async def consultar_api():
       async with httpx.AsyncClient() as client:
           return await client.get("https://api.example.com")

   # ✅ Sync para cálculos
   def calcular_fibonacci(n: int):
       if n <= 1:
           return n
       return calcular_fibonacci(n-1) + calcular_fibonacci(n-2)
   ```

2. **Usa `asyncio.gather()` para paralelizar**
   ```python
   # ✅ Paralelo
   resultados = await asyncio.gather(
       tarea1(),
       tarea2(),
       tarea3()
   )
   ```

3. **Maneja timeouts**
   ```python
   # ✅ Con timeout
   try:
       resultado = await asyncio.wait_for(operacion_lenta(), timeout=5.0)
   except asyncio.TimeoutError:
       print("Timeout alcanzado")
   ```

4. **Usa context managers async**
   ```python
   # ✅ Async context manager
   async with aiofiles.open("archivo.txt", "r") as f:
       contenido = await f.read()
   ```

#### ❌ DON'T: Anti-Patrones

1. **No bloquees el event loop**
   ```python
   # ❌ BLOQUEA el event loop
   async def malo():
       time.sleep(5)  # Bloquea TODO el event loop

   # ✅ No bloquea
   async def bueno():
       await asyncio.sleep(5)  # Libera el event loop
   ```

2. **No uses `asyncio.run()` dentro de async**
   ```python
   # ❌ ERROR
   async def malo():
       resultado = asyncio.run(otra_coroutine())  # Crea nuevo event loop

   # ✅ CORRECTO
   async def bueno():
       resultado = await otra_coroutine()  # Usa el event loop actual
   ```

3. **No olvides await**
   ```python
   # ❌ Coroutine no ejecutada
   async def malo():
       tarea_async()  # ⚠️ No hace nada

   # ✅ CORRECTO
   async def bueno():
       await tarea_async()  # Ejecuta la coroutine
   ```

### 10. Cuándo NO Usar Async

❌ **Evita async si**:

1. **Tu código es CPU-bound**
   ```python
   # ❌ Async no ayuda aquí (CPU-bound)
   async def calcular_primos(n: int):
       # Cálculos pesados no se benefician de async
       primos = []
       for i in range(2, n):
           if es_primo(i):
               primos.append(i)
       return primos

   # ✅ Mejor usar multiprocessing para CPU-bound
   from multiprocessing import Pool
   def calcular_primos_paralelo(n: int):
       with Pool() as pool:
           return pool.map(es_primo, range(2, n))
   ```

2. **No tienes I/O**
   ```python
   # ❌ Async innecesario (sin I/O)
   async def suma(a: int, b: int):
       return a + b

   # ✅ Sync es más simple
   def suma(a: int, b: int):
       return a + b
   ```

3. **Usas librerías que no soportan async**
   ```python
   # ❌ Librería sync en función async
   async def consultar_db_sync():
       # psycopg2 es sync, bloquea el event loop
       conn = psycopg2.connect(...)
       cursor = conn.cursor()
       cursor.execute("SELECT ...")

   # ✅ Usa librería async
   async def consultar_db_async():
       # asyncpg es async
       conn = await asyncpg.connect(...)
       resultado = await conn.fetch("SELECT ...")
   ```

## 🎯 Ejercicios Prácticos

Ver `EJERCICIOS.md` para 5+ ejercicios prácticos progresivos.

## 📖 Recursos Adicionales

- [asyncio — Asynchronous I/O](https://docs.python.org/3/library/asyncio.html) (Documentación oficial)
- [FastAPI Async Guide](https://fastapi.tiangolo.com/async/)
- [Real Python: Async IO in Python](https://realpython.com/async-io-python/)

## 🔗 Siguiente Clase

**Clase 4 - SOLID en FastAPI**: Aplicaremos principios SOLID en endpoints FastAPI, ahora con conocimiento de async/await.

---

**🤖 AI Integration**: Ver `AI_WORKFLOW.md` para ejercicios con IA que refuerzan estos conceptos.
