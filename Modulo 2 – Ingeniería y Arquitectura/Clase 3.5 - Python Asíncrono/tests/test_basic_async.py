"""
Tests para ejemplos básicos de async/await
Requiere: pytest pytest-asyncio
Ejecutar: pytest tests/test_basic_async.py -v
"""

import pytest
import asyncio
import time
from examples.basic_async import (
    preparar_cafe,
    preparar_tostada,
    preparar_jugo,
    ejemplo_secuencial,
    ejemplo_paralelo
)


@pytest.mark.asyncio
async def test_preparar_cafe_retorna_string():
    """Test que preparar_cafe retorna el string correcto"""
    resultado = await preparar_cafe()
    assert resultado == "Café"


@pytest.mark.asyncio
async def test_preparar_cafe_tarda_2_segundos():
    """Test que preparar_cafe tarda aproximadamente 2 segundos"""
    inicio = time.time()
    await preparar_cafe()
    tiempo = time.time() - inicio
    assert 1.9 <= tiempo <= 2.1  # Tolerancia de 0.1s


@pytest.mark.asyncio
async def test_ejecucion_secuencial_es_lenta():
    """Test que ejecución secuencial tarda suma de tiempos"""
    inicio = time.time()
    await ejemplo_secuencial()
    tiempo = time.time() - inicio

    # Secuencial: 2 + 1 + 0.5 = 3.5 segundos
    assert tiempo >= 3.4  # Al menos 3.4 segundos


@pytest.mark.asyncio
async def test_ejecucion_paralela_es_rapida():
    """Test que ejecución paralela tarda solo el máximo tiempo"""
    inicio = time.time()
    await ejemplo_paralelo()
    tiempo = time.time() - inicio

    # Paralelo: max(2, 1, 0.5) = 2 segundos
    assert tiempo <= 2.2  # Máximo 2.2 segundos


@pytest.mark.asyncio
async def test_gather_retorna_resultados_en_orden():
    """Test que asyncio.gather retorna resultados en orden correcto"""
    resultados = await asyncio.gather(
        preparar_cafe(),
        preparar_tostada(),
        preparar_jugo()
    )

    assert resultados == ["Café", "Tostada", "Jugo"]


@pytest.mark.asyncio
async def test_gather_es_mas_rapido_que_secuencial():
    """Test que gather es significativamente más rápido"""
    # Secuencial
    inicio_seq = time.time()
    await preparar_cafe()
    await preparar_tostada()
    await preparar_jugo()
    tiempo_seq = time.time() - inicio_seq

    # Paralelo
    inicio_par = time.time()
    await asyncio.gather(
        preparar_cafe(),
        preparar_tostada(),
        preparar_jugo()
    )
    tiempo_par = time.time() - inicio_par

    # Paralelo debe ser al menos 30% más rápido
    assert tiempo_par < tiempo_seq * 0.7
