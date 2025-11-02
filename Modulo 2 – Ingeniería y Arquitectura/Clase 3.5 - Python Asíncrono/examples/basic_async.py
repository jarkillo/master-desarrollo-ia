"""
Ejemplo 1: Fundamentos de Async/Await
Comparación entre ejecución secuencial y paralela
"""

import asyncio
import time


async def preparar_cafe() -> str:
    """Simula preparación de café (2 segundos)"""
    print("☕ Iniciando preparación de café...")
    await asyncio.sleep(2)
    print("☕ Café listo!")
    return "Café"


async def preparar_tostada() -> str:
    """Simula preparación de tostada (1 segundo)"""
    print("🍞 Iniciando preparación de tostada...")
    await asyncio.sleep(1)
    print("🍞 Tostada lista!")
    return "Tostada"


async def preparar_jugo() -> str:
    """Simula preparación de jugo (0.5 segundos)"""
    print("🥤 Iniciando preparación de jugo...")
    await asyncio.sleep(0.5)
    print("🥤 Jugo listo!")
    return "Jugo"


async def ejemplo_secuencial():
    """❌ SECUENCIAL: Ejecuta tareas una después de otra"""
    print("=== EJECUCIÓN SECUENCIAL ===")
    inicio = time.time()

    # Cada await espera a que la anterior termine
    cafe = await preparar_cafe()       # 2s
    tostada = await preparar_tostada() # 1s
    jugo = await preparar_jugo()       # 0.5s

    tiempo_total = time.time() - inicio
    print(f"\n✅ Desayuno completo: {cafe}, {tostada}, {jugo}")
    print(f"⏱️  Tiempo total: {tiempo_total:.2f}s\n")


async def ejemplo_paralelo():
    """✅ PARALELO: Ejecuta tareas concurrentemente"""
    print("=== EJECUCIÓN PARALELA ===")
    inicio = time.time()

    # gather() ejecuta todas las tareas al mismo tiempo
    resultados = await asyncio.gather(
        preparar_cafe(),
        preparar_tostada(),
        preparar_jugo()
    )

    tiempo_total = time.time() - inicio
    print(f"\n✅ Desayuno completo: {', '.join(resultados)}")
    print(f"⏱️  Tiempo total: {tiempo_total:.2f}s\n")


async def main():
    """Ejecuta ambos ejemplos para comparar"""
    await ejemplo_secuencial()
    print("-" * 50)
    await ejemplo_paralelo()

    print("📊 RESULTADO:")
    print("   Secuencial: ~3.5 segundos (2 + 1 + 0.5)")
    print("   Paralelo:   ~2.0 segundos (máximo de las 3)")
    print("   Mejora:     ~43% más rápido!")


if __name__ == "__main__":
    asyncio.run(main())
