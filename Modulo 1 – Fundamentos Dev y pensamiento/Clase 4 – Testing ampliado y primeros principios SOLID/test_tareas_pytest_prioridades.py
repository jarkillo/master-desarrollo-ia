# test_tareas_pytest_prioridades.py
# Tests con pytest para funcionalidad de prioridades
# Clase 4 - Testing ampliado y primeros principios SOLID

import os
import tempfile
import pytest
from tareas import (
    guardar_tareas,
    cargar_tareas,
    agregar_tarea,
    completar_tarea,
    listar_tareas,
)


@pytest.fixture
def archivo_temporal():
    """
    Fixture que crea un archivo temporal para tests.
    Se ejecuta antes de cada test y limpia después.
    """
    fd, tmp = tempfile.mkstemp(prefix="tareas_", suffix=".json")
    os.close(fd)
    guardar_tareas(tmp, [])
    yield tmp
    os.remove(tmp)


# ===================================================================
# Tests básicos (heredados de Clase 3)
# ===================================================================

def test_agregar_tarea(archivo_temporal):
    """Test happy path: Agregar tarea con nombre válido."""
    tarea = agregar_tarea(archivo_temporal, "Estudiar IA")

    assert tarea["nombre"] == "Estudiar IA"
    assert tarea["completada"] == False

    tareas = cargar_tareas(archivo_temporal)
    assert len(tareas) == 1


def test_completar_tarea(archivo_temporal):
    """Test: Completar una tarea existente."""
    tarea = agregar_tarea(archivo_temporal, "Repasar Git")
    ok = completar_tarea(archivo_temporal, tarea["id"])

    assert ok == True

    tareas = listar_tareas(archivo_temporal)
    assert tareas[0]["completada"] == True


# ===================================================================
# Tests de prioridades (nuevos en Clase 4)
# ===================================================================

def test_agregar_tarea_prioridad_por_defecto(archivo_temporal):
    """
    Test: Agregar tarea sin especificar prioridad.
    Debe usar prioridad por defecto "media".
    """
    tarea = agregar_tarea(archivo_temporal, "Repasar SOLID")

    assert tarea["prioridad"] == "media"


def test_agregar_tarea_con_prioridad_alta(archivo_temporal):
    """
    Test: Agregar tarea con prioridad explícita "alta".
    """
    tarea = agregar_tarea(archivo_temporal, "Estudiar IA", prioridad="alta")

    assert tarea["nombre"] == "Estudiar IA"
    assert tarea["prioridad"] == "alta"
    assert tarea["completada"] == False


@pytest.mark.parametrize("prioridad", ["alta", "media", "baja"])
def test_agregar_tarea_prioridades_validas(archivo_temporal, prioridad):
    """
    Test parametrizado: Todas las prioridades válidas se aceptan.
    Reduce duplicación usando pytest.mark.parametrize.
    """
    tarea = agregar_tarea(archivo_temporal, f"Tarea {prioridad}", prioridad=prioridad)

    assert tarea["prioridad"] == prioridad


def test_agregar_tarea_prioridad_invalida_usa_media(archivo_temporal):
    """
    Edge case: Prioridad inválida debe usar "media" como default.
    """
    tarea = agregar_tarea(archivo_temporal, "Tarea inválida", prioridad="super-urgente")

    assert tarea["prioridad"] == "media"


# ===================================================================
# Tests de filtrado por prioridad
# ===================================================================

def test_listar_solo_prioridad_alta(archivo_temporal):
    """
    Test: Filtrar tareas por prioridad "alta".
    Solo debe devolver tareas con esa prioridad.
    """
    agregar_tarea(archivo_temporal, "Urgente", prioridad="alta")
    agregar_tarea(archivo_temporal, "Normal", prioridad="media")
    agregar_tarea(archivo_temporal, "Puede esperar", prioridad="baja")

    tareas_alta = listar_tareas(archivo_temporal, prioridad="alta")

    assert len(tareas_alta) == 1
    assert tareas_alta[0]["nombre"] == "Urgente"
    assert tareas_alta[0]["prioridad"] == "alta"


def test_listar_sin_filtro_devuelve_todas(archivo_temporal):
    """
    Test: Listar sin parámetro de prioridad devuelve todas las tareas.
    """
    agregar_tarea(archivo_temporal, "Tarea 1", prioridad="alta")
    agregar_tarea(archivo_temporal, "Tarea 2", prioridad="media")
    agregar_tarea(archivo_temporal, "Tarea 3", prioridad="baja")

    todas = listar_tareas(archivo_temporal)

    assert len(todas) == 3


def test_listar_prioridad_sin_resultados(archivo_temporal):
    """
    Edge case: Filtrar por prioridad que no tiene tareas.
    Debe devolver lista vacía.
    """
    agregar_tarea(archivo_temporal, "Solo media", prioridad="media")

    tareas_alta = listar_tareas(archivo_temporal, prioridad="alta")

    assert tareas_alta == []


# ===================================================================
# Tests de edge cases adicionales (para 90%+ coverage)
# ===================================================================

def test_completar_tarea_id_inexistente(archivo_temporal):
    """
    Edge case crítico: Completar tarea que no existe.
    Debe devolver False sin crashear.
    """
    agregar_tarea(archivo_temporal, "Tarea 1")

    resultado = completar_tarea(archivo_temporal, 999)

    assert resultado == False


def test_cargar_tareas_archivo_json_corrupto(archivo_temporal):
    """
    Edge case crítico: Archivo JSON corrupto.
    cargar_tareas debe devolver lista vacía sin crashear.
    """
    # Escribir JSON inválido
    with open(archivo_temporal, 'w') as f:
        f.write("{esto no es json válido")

    tareas = cargar_tareas(archivo_temporal)

    assert tareas == []


def test_cargar_tareas_archivo_vacio(archivo_temporal):
    """
    Edge case: Archivo vacío (sin contenido).
    Debe devolver lista vacía.
    """
    # Crear archivo vacío
    with open(archivo_temporal, 'w') as f:
        f.write("")

    tareas = cargar_tareas(archivo_temporal)

    assert tareas == []


def test_backfill_prioridad_en_tareas_antiguas(archivo_temporal):
    """
    Test: Tareas guardadas sin campo 'prioridad' reciben 'media' al cargar.
    Simula migración de datos legacy.
    """
    # Simular tarea guardada sin prioridad (formato antiguo)
    tareas_legacy = [
        {"id": 1, "nombre": "Tarea antigua", "completada": False}
        # Sin campo 'prioridad'
    ]
    guardar_tareas(archivo_temporal, tareas_legacy)

    # Al cargar, debe añadir prioridad por defecto
    tareas = cargar_tareas(archivo_temporal)

    assert len(tareas) == 1
    assert tareas[0]["prioridad"] == "media"  # Backfill automático


# ===================================================================
# NOTA PEDAGÓGICA:
# ===================================================================
# Coverage alcanzado con estos tests: ~90%+
#
# Tests incluidos:
# ✅ Happy paths (agregar, completar, listar)
# ✅ Prioridades (default, explícita, inválida)
# ✅ Filtrado (con/sin parámetro, sin resultados)
# ✅ Edge cases críticos (ID inexistente, JSON corrupto, archivo vacío)
# ✅ Backfill de datos legacy
# ✅ Parametrización (reduce duplicación)
#
# Para alcanzar 95%+, añadir tests de:
# - Múltiples tareas consecutivas (IDs incrementales)
# - Nombre de tarea vacío o muy largo
# - Concurrencia (dos procesos escribiendo)
#
# Ejercicio: Usa Test Coverage Strategist para identificar gaps restantes.
# ===================================================================
