"""
Tests para la API de Tareas - Clase 2
Cubre todos los endpoints CRUD: POST, GET, PUT, DELETE
"""
from api import api as api_mod
from fastapi.testclient import TestClient


def test_crear_tarea_minima_devuelve_201_y_cuerpo_esperado():
    """Test para POST /tareas - caso exitoso."""
    # Resetear estado (evitar interferencia entre tests)
    api_mod._tareas.clear()
    api_mod._contador_id = 0

    cliente = TestClient(api_mod.app)

    cuerpo_peticion = {"nombre": "Estudiar SOLID"}
    respuesta = cliente.post("/tareas", json=cuerpo_peticion)

    assert respuesta.status_code == 201
    cuerpo_respuesta = respuesta.json()
    assert cuerpo_respuesta["id"] == 1
    assert cuerpo_respuesta["nombre"] == "Estudiar SOLID"
    assert cuerpo_respuesta["completada"] is False


def test_crear_tarea_con_nombre_vacio_devuelve_422():
    """Test para POST /tareas - validación de nombre vacío."""
    api_mod._tareas.clear()
    api_mod._contador_id = 0

    cliente = TestClient(api_mod.app)

    respuesta = cliente.post("/tareas", json={"nombre": ""})
    assert respuesta.status_code == 422


# === Tests para GET /tareas (listar) ===

def test_listar_tareas_vacia_devuelve_lista_vacia():
    """Test para GET /tareas - lista vacía inicial."""
    api_mod._tareas.clear()
    api_mod._contador_id = 0

    cliente = TestClient(api_mod.app)

    respuesta = cliente.get("/tareas")
    assert respuesta.status_code == 200
    assert respuesta.json() == []


def test_listar_tareas_devuelve_tareas_creadas():
    """Test para GET /tareas - lista con tareas."""
    api_mod._tareas.clear()
    api_mod._contador_id = 0

    cliente = TestClient(api_mod.app)

    # Crear 2 tareas
    cliente.post("/tareas", json={"nombre": "Tarea 1"})
    cliente.post("/tareas", json={"nombre": "Tarea 2"})

    # Listar
    respuesta = cliente.get("/tareas")
    assert respuesta.status_code == 200

    tareas = respuesta.json()
    assert len(tareas) == 2
    assert tareas[0]["nombre"] == "Tarea 1"
    assert tareas[1]["nombre"] == "Tarea 2"


# === Tests para GET /tareas/{id} (obtener una) ===

def test_obtener_tarea_existente_devuelve_200():
    """Test para GET /tareas/{id} - tarea existe."""
    api_mod._tareas.clear()
    api_mod._contador_id = 0

    cliente = TestClient(api_mod.app)

    # Crear tarea
    crear_respuesta = cliente.post("/tareas", json={"nombre": "Tarea de prueba"})
    tarea_creada = crear_respuesta.json()
    tarea_id = tarea_creada["id"]

    # Obtener por ID
    respuesta = cliente.get(f"/tareas/{tarea_id}")
    assert respuesta.status_code == 200

    tarea = respuesta.json()
    assert tarea["id"] == tarea_id
    assert tarea["nombre"] == "Tarea de prueba"
    assert tarea["completada"] is False


def test_obtener_tarea_inexistente_devuelve_404():
    """Test para GET /tareas/{id} - tarea no existe."""
    api_mod._tareas.clear()
    api_mod._contador_id = 0

    cliente = TestClient(api_mod.app)

    respuesta = cliente.get("/tareas/999")
    assert respuesta.status_code == 404
    assert "no encontrada" in respuesta.json()["detail"].lower()


# === Tests para PUT /tareas/{id}/completar ===

def test_completar_tarea_existente_devuelve_200():
    """Test para PUT /tareas/{id}/completar - tarea existe."""
    api_mod._tareas.clear()
    api_mod._contador_id = 0

    cliente = TestClient(api_mod.app)

    # Crear tarea
    crear_respuesta = cliente.post("/tareas", json={"nombre": "Tarea a completar"})
    tarea_id = crear_respuesta.json()["id"]

    # Completar
    respuesta = cliente.put(f"/tareas/{tarea_id}/completar")
    assert respuesta.status_code == 200

    tarea_completada = respuesta.json()
    assert tarea_completada["id"] == tarea_id
    assert tarea_completada["completada"] is True


def test_completar_tarea_inexistente_devuelve_404():
    """Test para PUT /tareas/{id}/completar - tarea no existe."""
    api_mod._tareas.clear()
    api_mod._contador_id = 0

    cliente = TestClient(api_mod.app)

    respuesta = cliente.put("/tareas/999/completar")
    assert respuesta.status_code == 404


def test_completar_tarea_mantiene_nombre():
    """Test para PUT /tareas/{id}/completar - solo cambia completada, no otros campos."""
    api_mod._tareas.clear()
    api_mod._contador_id = 0

    cliente = TestClient(api_mod.app)

    # Crear
    crear_respuesta = cliente.post("/tareas", json={"nombre": "Tarea original"})
    tarea_id = crear_respuesta.json()["id"]

    # Completar
    respuesta = cliente.put(f"/tareas/{tarea_id}/completar")
    tarea_completada = respuesta.json()

    # Verificar que el nombre no cambió
    assert tarea_completada["nombre"] == "Tarea original"
    assert tarea_completada["completada"] is True


# === Tests para DELETE /tareas/{id} ===

def test_eliminar_tarea_existente_devuelve_204():
    """Test para DELETE /tareas/{id} - tarea existe."""
    api_mod._tareas.clear()
    api_mod._contador_id = 0

    cliente = TestClient(api_mod.app)

    # Crear tarea
    crear_respuesta = cliente.post("/tareas", json={"nombre": "Tarea a eliminar"})
    tarea_id = crear_respuesta.json()["id"]

    # Eliminar
    respuesta = cliente.delete(f"/tareas/{tarea_id}")
    assert respuesta.status_code == 204

    # Verificar que ya no existe
    respuesta_get = cliente.get(f"/tareas/{tarea_id}")
    assert respuesta_get.status_code == 404


def test_eliminar_tarea_inexistente_devuelve_404():
    """Test para DELETE /tareas/{id} - tarea no existe."""
    api_mod._tareas.clear()
    api_mod._contador_id = 0

    cliente = TestClient(api_mod.app)

    respuesta = cliente.delete("/tareas/999")
    assert respuesta.status_code == 404


def test_eliminar_tarea_reduce_cantidad():
    """Test para DELETE /tareas/{id} - verifica que lista se reduce."""
    api_mod._tareas.clear()
    api_mod._contador_id = 0

    cliente = TestClient(api_mod.app)

    # Crear 3 tareas
    cliente.post("/tareas", json={"nombre": "Tarea 1"})
    crear_respuesta = cliente.post("/tareas", json={"nombre": "Tarea 2"})
    cliente.post("/tareas", json={"nombre": "Tarea 3"})

    tarea_2_id = crear_respuesta.json()["id"]

    # Eliminar la segunda
    cliente.delete(f"/tareas/{tarea_2_id}")

    # Verificar que quedan 2
    respuesta_listar = cliente.get("/tareas")
    tareas = respuesta_listar.json()
    assert len(tareas) == 2
    assert all(t["id"] != tarea_2_id for t in tareas)
