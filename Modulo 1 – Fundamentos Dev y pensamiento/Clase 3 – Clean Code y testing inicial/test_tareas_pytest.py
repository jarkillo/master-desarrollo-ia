# test_tareas_pytest.py
# Tests con pytest (migrado desde unittest)
# Clase 3 - Clean Code y testing inicial

import os
import tempfile
import pytest
from tareas import guardar_tareas, cargar_tareas, agregar_tarea, completar_tarea, listar_tareas


@pytest.fixture
def archivo_temporal():
    """
    Fixture que crea un archivo temporal para tests.
    Se ejecuta antes de cada test y limpia después.
    """
    fd, tmp = tempfile.mkstemp(prefix="tareas_", suffix=".json")
    os.close(fd)
    guardar_tareas(tmp, [])  # Empezamos con archivo vacío
    yield tmp  # El test usa este archivo
    os.remove(tmp)  # Limpieza automática


def test_agregar_tarea(archivo_temporal):
    """
    Test: Agregar una tarea con nombre válido.
    Verifica que se crea correctamente con nombre y estado inicial.
    """
    agregar_tarea(archivo_temporal, "Estudiar IA")
    tareas = cargar_tareas(archivo_temporal)

    assert len(tareas) == 1
    assert tareas[0]["nombre"] == "Estudiar IA"
    assert tareas[0]["completada"] == False


def test_completar_tarea(archivo_temporal):
    """
    Test: Completar una tarea existente.
    Verifica que el estado cambia a True.
    """
    tarea = agregar_tarea(archivo_temporal, "Repasar Git")
    ok = completar_tarea(archivo_temporal, tarea["id"])

    assert ok == True

    tareas = listar_tareas(archivo_temporal)
    assert tareas[0]["completada"] == True


def test_completar_tarea_inexistente(archivo_temporal):
    """
    Test: Intentar completar tarea que no existe.
    Edge case: debe retornar False sin crashear.
    """
    guardar_tareas(archivo_temporal, [])
    ok = completar_tarea(archivo_temporal, 999)

    assert ok == False


def test_listar_vacio(archivo_temporal):
    """
    Test: Listar cuando no hay tareas.
    Edge case: debe devolver lista vacía.
    """
    guardar_tareas(archivo_temporal, [])
    tareas = listar_tareas(archivo_temporal)

    assert tareas == []


def test_listar_con_tareas(archivo_temporal):
    """
    Test: Listar con varias tareas.
    Verifica que devuelve todas en orden correcto.
    """
    agregar_tarea(archivo_temporal, "Estudiar IA")
    agregar_tarea(archivo_temporal, "Repasar Git")

    tareas = listar_tareas(archivo_temporal)

    assert len(tareas) == 2
    assert tareas[0]["nombre"] == "Estudiar IA"
    assert tareas[1]["nombre"] == "Repasar Git"
    assert tareas[0]["completada"] == False
    assert tareas[1]["completada"] == False


# ===================================================================
# NOTA PEDAGÓGICA:
# ===================================================================
# Estos tests cubren:
# - Happy path (agregar, listar, completar)
# - Edge cases (lista vacía, ID inexistente)
#
# Para alcanzar 80%+ coverage, necesitas añadir tests para:
# - Archivo JSON corrupto
# - Nombre de tarea vacío
# - ID negativo
# - Persistencia entre llamadas (leer después de escribir)
#
# Ejercicio: Usa el Test Coverage Strategist agent para identificar
# qué otros edge cases deberías testear.
# ===================================================================
