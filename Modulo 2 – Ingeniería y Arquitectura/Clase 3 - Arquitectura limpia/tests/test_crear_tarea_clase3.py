from datetime import date, timedelta

from api.api import app
from fastapi.testclient import TestClient

cliente_http = TestClient(app)


def test_crear_tarea_minima_devuelve_201_y_cuerpo_esperado():
    """Crear tarea con solo nombre debe usar valores por defecto."""
    cuerpo_peticion = {"nombre": "Estudiar SOLID"}
    respuesta = cliente_http.post("/tareas", json=cuerpo_peticion)
    assert respuesta.status_code == 201

    cuerpo_respuesta = respuesta.json()
    assert cuerpo_respuesta["id"] == 1
    assert cuerpo_respuesta["nombre"] == "Estudiar solid"  # Capitalizado por validator
    assert cuerpo_respuesta["completada"] is False
    assert cuerpo_respuesta["prioridad"] == 3  # Default
    assert cuerpo_respuesta["fecha_limite"] is None  # Default
    assert cuerpo_respuesta["etiquetas"] == []  # Default


def test_crear_tarea_con_nombre_vacio_devuelve_422():
    """Nombre vacío debe ser rechazado."""
    respuesta = cliente_http.post("/tareas", json={"nombre": ""})
    assert respuesta.status_code == 422


def test_crear_tarea_completa_con_todos_los_campos():
    """Crear tarea con todos los campos opcionales."""
    mañana = (date.today() + timedelta(days=1)).isoformat()
    cuerpo_peticion = {
        "nombre": "implementar API",
        "prioridad": 1,
        "fecha_limite": mañana,
        "etiquetas": ["python", "fastapi"]
    }
    respuesta = cliente_http.post("/tareas", json=cuerpo_peticion)
    assert respuesta.status_code == 201

    cuerpo_respuesta = respuesta.json()
    assert cuerpo_respuesta["nombre"] == "Implementar api"
    assert cuerpo_respuesta["prioridad"] == 1
    assert cuerpo_respuesta["fecha_limite"] == mañana
    assert cuerpo_respuesta["etiquetas"] == ["python", "fastapi"]


def test_crear_tarea_con_nombre_solo_espacios_devuelve_422():
    """Nombre con solo espacios debe ser rechazado."""
    respuesta = cliente_http.post("/tareas", json={"nombre": "   "})
    assert respuesta.status_code == 422


def test_crear_tarea_urgente_sin_fecha_devuelve_422():
    """Tarea urgente sin fecha límite debe ser rechazada."""
    cuerpo_peticion = {"nombre": "Tarea urgente", "prioridad": 1}
    respuesta = cliente_http.post("/tareas", json=cuerpo_peticion)
    assert respuesta.status_code == 422


def test_crear_tarea_con_fecha_pasada_devuelve_422():
    """Tarea con fecha en el pasado debe ser rechazada."""
    ayer = (date.today() - timedelta(days=1)).isoformat()
    cuerpo_peticion = {"nombre": "Tarea", "fecha_limite": ayer}
    respuesta = cliente_http.post("/tareas", json=cuerpo_peticion)
    assert respuesta.status_code == 422
