from datetime import date, timedelta

import pytest
from api.api import CrearTareaRequest
from pydantic import ValidationError

# === Tests de campo 'nombre' ===

def test_nombre_solo_espacios_falla():
    """Nombre con solo espacios debe fallar."""
    with pytest.raises(ValueError, match="no puede estar vacío"):
        CrearTareaRequest(nombre="   ")


def test_nombre_se_capitaliza():
    """Primera letra debe capitalizarse."""
    tarea = CrearTareaRequest(nombre="estudiar python")
    assert tarea.nombre == "Estudiar python"


def test_nombre_con_espacios_al_inicio_y_final_se_limpia():
    """Espacios al inicio/final deben eliminarse."""
    tarea = CrearTareaRequest(nombre="  tarea importante  ")
    assert tarea.nombre == "Tarea importante"


# === Tests de campo 'prioridad' ===

def test_prioridad_menor_que_1_falla():
    """Prioridad < 1 debe fallar."""
    with pytest.raises(ValidationError):
        CrearTareaRequest(nombre="Test", prioridad=0)


def test_prioridad_mayor_que_5_falla():
    """Prioridad > 5 debe fallar."""
    with pytest.raises(ValidationError):
        CrearTareaRequest(nombre="Test", prioridad=6)


def test_prioridad_por_defecto_es_3():
    """Si no se especifica prioridad, debe ser 3."""
    tarea = CrearTareaRequest(nombre="Test")
    assert tarea.prioridad == 3


def test_prioridad_1_es_valida():
    """Prioridad 1 debe ser válida (con fecha límite requerida)."""
    mañana = date.today() + timedelta(days=1)
    tarea = CrearTareaRequest(nombre="Test", prioridad=1, fecha_limite=mañana)
    assert tarea.prioridad == 1
    assert tarea.fecha_limite == mañana


def test_prioridad_5_es_valida():
    """Prioridad 5 debe ser válida."""
    tarea = CrearTareaRequest(nombre="Test", prioridad=5)
    assert tarea.prioridad == 5


# === Tests de campo 'fecha_limite' ===

def test_fecha_pasada_falla():
    """Fecha en el pasado debe fallar."""
    ayer = date.today() - timedelta(days=1)
    with pytest.raises(ValueError, match="no puede estar en el pasado"):
        CrearTareaRequest(nombre="Test", fecha_limite=ayer)


def test_fecha_none_es_valida():
    """Fecha None debe ser permitida."""
    tarea = CrearTareaRequest(nombre="Test", fecha_limite=None)
    assert tarea.fecha_limite is None


def test_fecha_hoy_es_valida():
    """Fecha de hoy debe ser válida."""
    hoy = date.today()
    tarea = CrearTareaRequest(nombre="Test", fecha_limite=hoy)
    assert tarea.fecha_limite == hoy


def test_fecha_futura_es_valida():
    """Fecha futura debe ser válida."""
    mañana = date.today() + timedelta(days=1)
    tarea = CrearTareaRequest(nombre="Test", fecha_limite=mañana)
    assert tarea.fecha_limite == mañana


# === Tests de campo 'etiquetas' ===

def test_etiquetas_se_convierten_a_minusculas():
    """Etiquetas deben ser lowercase."""
    tarea = CrearTareaRequest(nombre="Test", etiquetas=["PYTHON", "Django"])
    assert tarea.etiquetas == ["python", "django"]


def test_etiquetas_duplicadas_se_eliminan():
    """Duplicados deben ser removidos."""
    tarea = CrearTareaRequest(nombre="Test", etiquetas=["python", "PYTHON", "Python"])
    assert tarea.etiquetas == ["python"]


def test_etiquetas_con_espacios_se_limpian():
    """Espacios al inicio/final de etiquetas deben eliminarse."""
    tarea = CrearTareaRequest(nombre="Test", etiquetas=["  python  ", " django "])
    assert tarea.etiquetas == ["python", "django"]


def test_etiquetas_vacias_por_defecto():
    """Si no se especifican etiquetas, debe ser lista vacía."""
    tarea = CrearTareaRequest(nombre="Test")
    assert tarea.etiquetas == []


def test_etiquetas_mantienen_orden_al_eliminar_duplicados():
    """Al eliminar duplicados, debe mantenerse el orden de primera aparición."""
    tarea = CrearTareaRequest(nombre="Test", etiquetas=["python", "django", "fastapi", "PYTHON"])
    assert tarea.etiquetas == ["python", "django", "fastapi"]


# === Tests de @model_validator ===

def test_tarea_urgente_sin_fecha_falla():
    """Prioridad 1-2 requiere fecha límite."""
    with pytest.raises(ValueError, match="requieren una fecha límite"):
        CrearTareaRequest(nombre="Test", prioridad=1, fecha_limite=None)


def test_tarea_muy_urgente_sin_fecha_falla():
    """Prioridad 2 también requiere fecha límite."""
    with pytest.raises(ValueError, match="requieren una fecha límite"):
        CrearTareaRequest(nombre="Test", prioridad=2, fecha_limite=None)


def test_tarea_urgente_con_fecha_es_valida():
    """Prioridad 1 con fecha debe ser válida."""
    mañana = date.today() + timedelta(days=1)
    tarea = CrearTareaRequest(
        nombre="Test",
        prioridad=1,
        fecha_limite=mañana
    )
    assert tarea.prioridad == 1
    assert tarea.fecha_limite == mañana


def test_tarea_normal_sin_fecha_es_valida():
    """Prioridad 3 (normal) sin fecha debe ser válida."""
    tarea = CrearTareaRequest(nombre="Test", prioridad=3, fecha_limite=None)
    assert tarea.prioridad == 3
    assert tarea.fecha_limite is None


def test_tarea_baja_sin_fecha_es_valida():
    """Prioridad 5 (baja) sin fecha debe ser válida."""
    tarea = CrearTareaRequest(nombre="Test", prioridad=5, fecha_limite=None)
    assert tarea.prioridad == 5
    assert tarea.fecha_limite is None


# === Tests de integración (múltiples validadores) ===

def test_tarea_completa_con_todos_los_campos():
    """Tarea con todos los campos debe ser válida."""
    mañana = date.today() + timedelta(days=1)
    tarea = CrearTareaRequest(
        nombre="  estudiar pydantic  ",
        prioridad=1,
        fecha_limite=mañana,
        etiquetas=["PYTHON", "  FastAPI  ", "Python"]
    )
    assert tarea.nombre == "Estudiar pydantic"
    assert tarea.prioridad == 1
    assert tarea.fecha_limite == mañana
    assert tarea.etiquetas == ["python", "fastapi"]


def test_tarea_minima_solo_con_nombre():
    """Tarea mínima con solo nombre debe usar defaults."""
    tarea = CrearTareaRequest(nombre="Tarea simple")
    assert tarea.nombre == "Tarea simple"
    assert tarea.prioridad == 3
    assert tarea.fecha_limite is None
    assert tarea.etiquetas == []
