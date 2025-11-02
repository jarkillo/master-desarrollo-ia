# Ejercicios Prácticos - Python Asíncrono

## Ejercicio 1: Tu Primera Coroutine ⭐

**Dificultad**: Principiante
**Tiempo estimado**: 15 minutos

### Objetivo
Crear tu primera coroutine y entender la diferencia entre sync y async.

### Instrucciones

1. Crea una función `async` llamada `preparar_cafe()` que:
   - Simule 2 segundos de preparación con `await asyncio.sleep(2)`
   - Retorne el string `"☕ Café listo"`

2. Crea otra coroutine `preparar_tostada()` que:
   - Simule 1 segundo de preparación
   - Retorne `"🍞 Tostada lista"`

3. Crea una función `main()` que:
   - Ejecute ambas tareas **secuencialmente** (una después de otra)
   - Mida el tiempo total con `time.time()`
   - Imprima el tiempo total

4. Modifica `main()` para ejecutar ambas tareas **en paralelo** con `asyncio.gather()`
   - Compara el tiempo total

### Código Base

```python
import asyncio
import time

async def preparar_cafe():
    # TODO: Implementa aquí
    pass

async def preparar_tostada():
    # TODO: Implementa aquí
    pass

async def main_secuencial():
    # TODO: Ejecuta secuencialmente y mide tiempo
    pass

async def main_paralelo():
    # TODO: Ejecuta en paralelo con asyncio.gather() y mide tiempo
    pass

if __name__ == "__main__":
    print("=== Secuencial ===")
    asyncio.run(main_secuencial())

    print("\n=== Paralelo ===")
    asyncio.run(main_paralelo())
```

### Resultado Esperado

```
=== Secuencial ===
☕ Café listo
🍞 Tostada lista
Tiempo total: 3.00s

=== Paralelo ===
☕ Café listo
🍞 Tostada lista
Tiempo total: 2.00s
```

### Preguntas de Reflexión

1. ¿Por qué la versión paralela es más rápida?
2. ¿Qué pasaría si `preparar_cafe()` tuviera un `time.sleep(2)` en vez de `await asyncio.sleep(2)`?
3. ¿Cuándo usarías ejecución secuencial en vez de paralela?

---

## Ejercicio 2: API de Clima Async ⭐⭐

**Dificultad**: Intermedio
**Tiempo estimado**: 30 minutos

### Objetivo
Crear un endpoint FastAPI que consulte múltiples APIs de clima en paralelo.

### Instrucciones

1. Crea un endpoint `/clima/{ciudad}` que:
   - Consulte 3 fuentes de clima diferentes (simuladas con `asyncio.sleep()`)
   - Ejecute las 3 consultas en paralelo con `asyncio.gather()`
   - Retorne un promedio de las temperaturas

2. Implementa timeout de 2 segundos con `asyncio.wait_for()`

3. Maneja errores si alguna fuente falla (usa `return_exceptions=True`)

### Código Base

```python
from fastapi import FastAPI, HTTPException
import asyncio
import random

app = FastAPI()

async def fuente_clima_1(ciudad: str) -> float:
    """Simula API de clima 1"""
    await asyncio.sleep(random.uniform(0.5, 1.5))
    return random.uniform(15.0, 25.0)

async def fuente_clima_2(ciudad: str) -> float:
    """Simula API de clima 2"""
    await asyncio.sleep(random.uniform(0.5, 1.5))
    # Simula error aleatorio
    if random.random() < 0.2:
        raise ValueError("API no disponible")
    return random.uniform(14.0, 26.0)

async def fuente_clima_3(ciudad: str) -> float:
    """Simula API de clima 3"""
    await asyncio.sleep(random.uniform(0.5, 1.5))
    return random.uniform(16.0, 24.0)

@app.get("/clima/{ciudad}")
async def obtener_clima(ciudad: str):
    """
    TODO: Implementa la lógica para:
    1. Ejecutar las 3 fuentes en paralelo
    2. Manejar errores (return_exceptions=True)
    3. Calcular promedio de las fuentes exitosas
    4. Aplicar timeout de 2 segundos
    """
    pass
```

### Tests

```python
# tests/test_clima.py
import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_clima_retorna_200():
    response = client.get("/clima/Madrid")
    assert response.status_code == 200
    assert "temperatura" in response.json()

def test_clima_con_timeout():
    # Este test verifica que el timeout funcione
    response = client.get("/clima/CiudadLenta")
    assert response.status_code in [200, 408]  # 408 Timeout
```

### Resultado Esperado

```json
{
  "ciudad": "Madrid",
  "temperatura": 21.3,
  "fuentes_consultadas": 3,
  "fuentes_exitosas": 2
}
```

---

## Ejercicio 3: Procesador de Imágenes Async ⭐⭐

**Dificultad**: Intermedio
**Tiempo estimado**: 45 minutos

### Objetivo
Implementar un sistema de procesamiento de imágenes asíncrono.

### Instrucciones

1. Crea un endpoint `/procesar-imagenes` que:
   - Reciba una lista de URLs de imágenes
   - Descargue las imágenes en paralelo (simulado)
   - Procese cada imagen (redimensionar, aplicar filtro)
   - Retorne URLs de imágenes procesadas

2. Implementa:
   - Límite de 5 tareas concurrentes con `asyncio.Semaphore`
   - Barra de progreso (imprime % completado)
   - Manejo de errores por imagen

### Código Base

```python
from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from typing import List

app = FastAPI()

class ImagenRequest(BaseModel):
    urls: List[str]

async def descargar_imagen(url: str, semaphore: asyncio.Semaphore) -> bytes:
    """Simula descarga async de imagen"""
    async with semaphore:
        await asyncio.sleep(0.5)  # Simula descarga
        return f"imagen_{url}".encode()

async def procesar_imagen(datos: bytes) -> str:
    """Simula procesamiento async de imagen"""
    await asyncio.sleep(0.3)  # Simula procesamiento
    return f"procesada_{datos.decode()}"

@app.post("/procesar-imagenes")
async def procesar_imagenes(request: ImagenRequest):
    """
    TODO: Implementa la lógica para:
    1. Crear Semaphore con límite de 5
    2. Descargar imágenes en paralelo
    3. Procesar imágenes descargadas
    4. Mostrar progreso
    5. Retornar resultados
    """
    pass
```

### Hints

```python
# Semaphore para limitar concurrencia
semaphore = asyncio.Semaphore(5)

# Mostrar progreso
completadas = 0
total = len(urls)
print(f"Progreso: {completadas}/{total} ({completadas/total*100:.1f}%)")
```

---

## Ejercicio 4: Rate Limiter Async ⭐⭐⭐

**Dificultad**: Avanzado
**Tiempo estimado**: 60 minutos

### Objetivo
Implementar un rate limiter asíncrono para endpoints FastAPI.

### Instrucciones

1. Crea una clase `AsyncRateLimiter` que:
   - Limite requests por usuario a X por minuto
   - Use `asyncio.Lock` para thread-safety
   - Almacene timestamps de requests en memoria

2. Implementa como dependencia de FastAPI

3. Testea con múltiples requests concurrentes

### Código Base

```python
from fastapi import FastAPI, Depends, HTTPException
import asyncio
import time
from typing import Dict, List
from collections import defaultdict

class AsyncRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        """
        max_requests: Número máximo de requests
        window_seconds: Ventana de tiempo en segundos
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: Dict[str, List[float]] = defaultdict(list)
        self._lock = asyncio.Lock()

    async def is_allowed(self, user_id: str) -> bool:
        """
        TODO: Implementa la lógica para:
        1. Usar el lock para acceso thread-safe
        2. Limpiar requests antiguos fuera de la ventana
        3. Verificar si el usuario ha excedido el límite
        4. Agregar timestamp actual si está permitido
        """
        pass

app = FastAPI()
rate_limiter = AsyncRateLimiter(max_requests=5, window_seconds=60)

async def verificar_rate_limit(user_id: str = "user1"):
    if not await rate_limiter.is_allowed(user_id):
        raise HTTPException(status_code=429, detail="Rate limit excedido")
    return user_id

@app.get("/api/datos")
async def obtener_datos(user_id: str = Depends(verificar_rate_limit)):
    return {"mensaje": "Datos obtenidos", "user_id": user_id}
```

### Tests

```python
# tests/test_rate_limiter.py
import pytest
import asyncio
from api import rate_limiter

@pytest.mark.asyncio
async def test_rate_limiter_permite_requests_validos():
    limiter = AsyncRateLimiter(max_requests=3, window_seconds=60)

    # Primeras 3 requests deben permitirse
    for i in range(3):
        assert await limiter.is_allowed("user1") is True

@pytest.mark.asyncio
async def test_rate_limiter_bloquea_exceso():
    limiter = AsyncRateLimiter(max_requests=3, window_seconds=60)

    # Hacer 3 requests permitidas
    for i in range(3):
        await limiter.is_allowed("user1")

    # La 4ta debe bloquearse
    assert await limiter.is_allowed("user1") is False

@pytest.mark.asyncio
async def test_rate_limiter_concurrente():
    limiter = AsyncRateLimiter(max_requests=10, window_seconds=60)

    # 10 requests concurrentes
    tareas = [limiter.is_allowed(f"user_{i}") for i in range(10)]
    resultados = await asyncio.gather(*tareas)

    # Todas deben permitirse (diferentes usuarios)
    assert all(resultados)
```

---

## Ejercicio 5: Sistema de Notificaciones Async ⭐⭐⭐

**Dificultad**: Avanzado
**Tiempo estimado**: 90 minutos

### Objetivo
Crear un sistema de notificaciones que envíe a múltiples canales (email, SMS, push) en paralelo.

### Instrucciones

1. Implementa 3 servicios de notificación:
   - `EnviarEmail` (tarda 1s)
   - `EnviarSMS` (tarda 0.5s)
   - `EnviarPushNotification` (tarda 0.3s)

2. Crea una clase `NotificationService` que:
   - Envíe a todos los canales en paralelo
   - Reintente automáticamente si falla (máximo 3 reintentos)
   - Registre logs de éxito/error

3. Implementa endpoint `/notificar` que use el servicio

### Código Base

```python
from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class Notificacion(BaseModel):
    usuario_id: str
    mensaje: str
    canales: List[str]  # ["email", "sms", "push"]

class NotificationService:
    def __init__(self, max_reintentos: int = 3):
        self.max_reintentos = max_reintentos

    async def enviar_email(self, usuario_id: str, mensaje: str) -> bool:
        """
        TODO: Implementa envío de email
        - Simula latencia de 1s
        - 10% de probabilidad de fallo
        """
        pass

    async def enviar_sms(self, usuario_id: str, mensaje: str) -> bool:
        """TODO: Implementa envío de SMS (0.5s latencia)"""
        pass

    async def enviar_push(self, usuario_id: str, mensaje: str) -> bool:
        """TODO: Implementa envío de push (0.3s latencia)"""
        pass

    async def enviar_con_reintentos(self, coro, nombre_canal: str):
        """
        TODO: Implementa lógica de reintentos
        1. Intenta ejecutar la coroutine
        2. Si falla, reintenta hasta max_reintentos veces
        3. Espera 1 segundo entre reintentos
        4. Registra logs
        """
        pass

    async def enviar_notificacion(
        self,
        usuario_id: str,
        mensaje: str,
        canales: List[str]
    ) -> Dict[str, bool]:
        """
        TODO: Implementa envío a múltiples canales
        1. Mapea canales a funciones de envío
        2. Ejecuta en paralelo con asyncio.gather()
        3. Retorna dict con resultado por canal
        """
        pass

notification_service = NotificationService()

@app.post("/notificar")
async def notificar(notificacion: Notificacion):
    resultados = await notification_service.enviar_notificacion(
        notificacion.usuario_id,
        notificacion.mensaje,
        notificacion.canales
    )
    return {
        "usuario_id": notificacion.usuario_id,
        "resultados": resultados
    }
```

### Tests

```python
# tests/test_notificaciones.py
import pytest
from api import NotificationService

@pytest.mark.asyncio
async def test_envio_paralelo():
    service = NotificationService()

    import time
    inicio = time.time()

    resultados = await service.enviar_notificacion(
        usuario_id="user1",
        mensaje="Hola",
        canales=["email", "sms", "push"]
    )

    tiempo = time.time() - inicio

    # Debe tardar ~1s (el más lento), no 1+0.5+0.3=1.8s
    assert tiempo < 1.5
    assert "email" in resultados
    assert "sms" in resultados
    assert "push" in resultados
```

### Resultado Esperado

```json
{
  "usuario_id": "user1",
  "resultados": {
    "email": true,
    "sms": true,
    "push": true
  }
}
```

---

## Ejercicio Bonus: Web Scraper Async ⭐⭐⭐⭐

**Dificultad**: Experto
**Tiempo estimado**: 2 horas

### Objetivo
Crear un web scraper asíncrono que descargue múltiples páginas en paralelo.

### Instrucciones

1. Usa `httpx.AsyncClient` para hacer requests HTTP async
2. Implementa queue de URLs con `asyncio.Queue`
3. Usa workers concurrentes para procesar URLs
4. Extrae títulos de páginas HTML
5. Implementa respeto a `robots.txt`

### Hints

```python
import httpx
import asyncio
from asyncio import Queue
from bs4 import BeautifulSoup

async def worker(queue: Queue, results: dict):
    """Procesa URLs de la queue"""
    async with httpx.AsyncClient() as client:
        while True:
            url = await queue.get()
            try:
                response = await client.get(url, timeout=5.0)
                soup = BeautifulSoup(response.text, 'html.parser')
                titulo = soup.find('title').text
                results[url] = titulo
            except Exception as e:
                results[url] = f"Error: {e}"
            finally:
                queue.task_done()

async def scraper(urls: list[str], num_workers: int = 5):
    queue = Queue()
    results = {}

    # Crear workers
    workers = [
        asyncio.create_task(worker(queue, results))
        for _ in range(num_workers)
    ]

    # Agregar URLs a la queue
    for url in urls:
        await queue.put(url)

    # Esperar a que se procesen todas
    await queue.join()

    # Cancelar workers
    for w in workers:
        w.cancel()

    return results
```

---

## 🎯 Criterios de Evaluación

Para cada ejercicio, verifica:

- ✅ **Funcionalidad**: El código hace lo que se pide
- ✅ **Async correctamente implementado**: Usa `async`/`await` apropiadamente
- ✅ **Manejo de errores**: Captura y maneja excepciones
- ✅ **Performance**: Ejecuta tareas en paralelo cuando es posible
- ✅ **Tests**: Los tests pasan correctamente
- ✅ **Code quality**: Código limpio y bien documentado

## 🤖 Ayuda con IA

Para resolver estos ejercicios con ayuda de IA, consulta `AI_WORKFLOW.md` para prompts específicos.

---

**💡 Tip**: Empieza por el Ejercicio 1 y avanza progresivamente. Cada ejercicio introduce conceptos nuevos basados en el anterior.
