"""
Ejemplo 2: FastAPI con Endpoints Async
Demuestra async vs sync en FastAPI y uso de asyncio.gather()
"""

from fastapi import FastAPI
import asyncio
from typing import List, Dict
import time

app = FastAPI(title="Ejemplo Async FastAPI")


# Simulación de servicios externos
async def consultar_servicio_usuarios() -> List[Dict]:
    """Simula consulta a servicio de usuarios (0.5s)"""
    await asyncio.sleep(0.5)
    return [
        {"id": 1, "nombre": "Ana"},
        {"id": 2, "nombre": "Luis"},
    ]


async def consultar_servicio_productos() -> List[Dict]:
    """Simula consulta a servicio de productos (0.8s)"""
    await asyncio.sleep(0.8)
    return [
        {"id": 101, "nombre": "Laptop", "precio": 1200},
        {"id": 102, "nombre": "Mouse", "precio": 25},
    ]


async def consultar_servicio_pedidos() -> List[Dict]:
    """Simula consulta a servicio de pedidos (0.3s)"""
    await asyncio.sleep(0.3)
    return [
        {"id": 1001, "usuario_id": 1, "producto_id": 101},
        {"id": 1002, "usuario_id": 2, "producto_id": 102},
    ]


# ❌ ENDPOINT LENTO: Consultas secuenciales
@app.get("/dashboard-lento")
async def dashboard_lento():
    """
    Consulta servicios secuencialmente.
    Tiempo total: 0.5s + 0.8s + 0.3s = 1.6s
    """
    inicio = time.time()

    usuarios = await consultar_servicio_usuarios()    # 0.5s
    productos = await consultar_servicio_productos()  # 0.8s
    pedidos = await consultar_servicio_pedidos()      # 0.3s

    tiempo = time.time() - inicio

    return {
        "usuarios": usuarios,
        "productos": productos,
        "pedidos": pedidos,
        "tiempo_ms": round(tiempo * 1000, 2),
        "metodo": "secuencial"
    }


# ✅ ENDPOINT RÁPIDO: Consultas paralelas
@app.get("/dashboard-rapido")
async def dashboard_rapido():
    """
    Consulta servicios en paralelo con asyncio.gather().
    Tiempo total: max(0.5s, 0.8s, 0.3s) = 0.8s
    """
    inicio = time.time()

    # Ejecutar las 3 consultas en paralelo
    usuarios, productos, pedidos = await asyncio.gather(
        consultar_servicio_usuarios(),
        consultar_servicio_productos(),
        consultar_servicio_pedidos()
    )

    tiempo = time.time() - inicio

    return {
        "usuarios": usuarios,
        "productos": productos,
        "pedidos": pedidos,
        "tiempo_ms": round(tiempo * 1000, 2),
        "metodo": "paralelo",
        "mejora": "50% más rápido"
    }


# Ejemplo con manejo de errores
async def consultar_servicio_con_error():
    """Simula servicio que falla aleatoriamente"""
    await asyncio.sleep(0.3)
    import random
    if random.random() < 0.3:  # 30% de probabilidad de fallo
        raise ValueError("Servicio no disponible")
    return {"status": "ok"}


@app.get("/dashboard-robusto")
async def dashboard_robusto():
    """
    Consulta servicios en paralelo con manejo de errores.
    Usa return_exceptions=True para no detener todo si uno falla.
    """
    inicio = time.time()

    # gather() con return_exceptions=True captura errores
    resultados = await asyncio.gather(
        consultar_servicio_usuarios(),
        consultar_servicio_productos(),
        consultar_servicio_con_error(),
        return_exceptions=True  # No detiene si uno falla
    )

    tiempo = time.time() - inicio

    # Procesar resultados
    usuarios = resultados[0] if not isinstance(resultados[0], Exception) else []
    productos = resultados[1] if not isinstance(resultados[1], Exception) else []
    servicio_extra = (
        resultados[2]
        if not isinstance(resultados[2], Exception)
        else {"error": str(resultados[2])}
    )

    return {
        "usuarios": usuarios,
        "productos": productos,
        "servicio_extra": servicio_extra,
        "tiempo_ms": round(tiempo * 1000, 2)
    }


# Ejemplo con timeout
@app.get("/dashboard-con-timeout")
async def dashboard_con_timeout():
    """
    Aplica timeout de 1 segundo a todo el dashboard.
    Si tarda más, lanza TimeoutError.
    """
    try:
        resultado = await asyncio.wait_for(
            dashboard_rapido(),
            timeout=1.0  # Máximo 1 segundo
        )
        return resultado
    except asyncio.TimeoutError:
        return {
            "error": "Timeout: Dashboard tardó más de 1 segundo",
            "status_code": 408
        }


# ✅ Async cuando haces I/O
@app.get("/async-io")
async def async_io():
    """Usa async cuando haces I/O (DB, API, archivos)"""
    await asyncio.sleep(0.1)  # Simula I/O
    return {"mensaje": "Async apropiado para I/O"}


# ✅ Sync cuando solo calculas
@app.get("/sync-cpu")
def sync_cpu():
    """Usa sync para cálculos sin I/O"""
    resultado = sum(range(1000))  # Solo cálculo
    return {"resultado": resultado, "mensaje": "Sync apropiado para CPU"}


if __name__ == "__main__":
    import uvicorn
    print("🚀 Inicia servidor con: uvicorn examples.fastapi_async:app --reload")
    print("📖 Visita http://localhost:8000/docs para probar endpoints")
    uvicorn.run(app, host="0.0.0.0", port=8000)
