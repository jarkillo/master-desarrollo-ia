"""
Tests de CRUD de tareas (crear, leer, actualizar, eliminar).
"""

from fastapi import status

# ============================================================================
# CREATE
# ============================================================================

def test_crear_tarea_exitoso(client, auth_headers):
    """Test de creación exitosa de una tarea."""
    response = client.post(
        "/tareas",
        headers=auth_headers,
        json={
            "titulo": "Nueva tarea",
            "descripcion": "Descripción de la tarea",
            "prioridad": 3,
            "completada": False
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["titulo"] == "Nueva tarea"
    assert data["descripcion"] == "Descripción de la tarea"
    assert data["prioridad"] == 3
    assert data["completada"] is False
    assert data["eliminada"] is False
    assert "id" in data
    assert "usuario_id" in data


def test_crear_tarea_sin_autenticacion(client):
    """Test que falla al crear tarea sin autenticación."""
    response = client.post(
        "/tareas",
        json={"titulo": "Tarea"}
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_crear_tarea_titulo_vacio(client, auth_headers):
    """Test de validación de título vacío."""
    response = client.post(
        "/tareas",
        headers=auth_headers,
        json={"titulo": "", "prioridad": 2}
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# ============================================================================
# READ
# ============================================================================

def test_obtener_tarea_por_id_exitoso(client, auth_headers, tarea_test):
    """Test de obtener tarea por ID."""
    response = client.get(
        f"/tareas/{tarea_test.id}",
        headers=auth_headers
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == tarea_test.id
    assert data["titulo"] == tarea_test.titulo


def test_obtener_tarea_no_existe(client, auth_headers):
    """Test de obtener tarea que no existe."""
    response = client.get(
        "/tareas/99999",
        headers=auth_headers
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_obtener_tarea_de_otro_usuario(client, auth_headers, usuario2_test, test_db):
    """Test que no permite ver tareas de otro usuario."""
    from api.models import TareaModel

    # Crear tarea del usuario2
    tarea_otro = TareaModel(
        titulo="Tarea de otro usuario",
        usuario_id=usuario2_test.id,
        prioridad=2
    )
    test_db.add(tarea_otro)
    test_db.commit()
    test_db.refresh(tarea_otro)

    # Intentar acceder con token del usuario1
    response = client.get(
        f"/tareas/{tarea_otro.id}",
        headers=auth_headers
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_listar_tareas(client, auth_headers, tareas_multiples):
    """Test de listar tareas con paginación."""
    response = client.get(
        "/tareas?page=1&page_size=10",
        headers=auth_headers
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert len(data["items"]) == 3  # 3 no eliminadas


def test_listar_tareas_filtro_completada(client, auth_headers, tareas_multiples):
    """Test de listar tareas filtradas por completada."""
    response = client.get(
        "/tareas?completada=true",
        headers=auth_headers
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(item["completada"] is True for item in data["items"])


def test_listar_tareas_filtro_prioridad(client, auth_headers, tareas_multiples):
    """Test de listar tareas filtradas por prioridad."""
    response = client.get(
        "/tareas?prioridad=3",
        headers=auth_headers
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(item["prioridad"] == 3 for item in data["items"])


def test_listar_tareas_busqueda(client, auth_headers, tareas_multiples):
    """Test de búsqueda de tareas por texto."""
    response = client.get(
        "/tareas?q=Alta",
        headers=auth_headers
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) > 0
    assert "Alta" in data["items"][0]["titulo"]


# ============================================================================
# UPDATE
# ============================================================================

def test_actualizar_tarea_exitoso(client, auth_headers, tarea_test):
    """Test de actualización exitosa de una tarea."""
    response = client.put(
        f"/tareas/{tarea_test.id}",
        headers=auth_headers,
        json={
            "titulo": "Título actualizado",
            "completada": True
        }
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["titulo"] == "Título actualizado"
    assert data["completada"] is True


def test_actualizar_tarea_parcial(client, auth_headers, tarea_test):
    """Test de actualización parcial (PATCH semántico)."""
    response = client.put(
        f"/tareas/{tarea_test.id}",
        headers=auth_headers,
        json={"prioridad": 1}  # Solo cambiar prioridad
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["prioridad"] == 1
    assert data["titulo"] == tarea_test.titulo  # No cambió


def test_actualizar_tarea_no_existe(client, auth_headers):
    """Test de actualizar tarea que no existe."""
    response = client.put(
        "/tareas/99999",
        headers=auth_headers,
        json={"titulo": "Nuevo título"}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


# ============================================================================
# DELETE
# ============================================================================

def test_eliminar_tarea_exitoso(client, auth_headers, tarea_test):
    """Test de eliminación exitosa (soft delete)."""
    response = client.delete(
        f"/tareas/{tarea_test.id}",
        headers=auth_headers
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verificar que no aparece en listado normal
    response_lista = client.get("/tareas", headers=auth_headers)
    data_lista = response_lista.json()
    assert not any(t["id"] == tarea_test.id for t in data_lista["items"])


def test_eliminar_tarea_no_existe(client, auth_headers):
    """Test de eliminar tarea que no existe."""
    response = client.delete(
        "/tareas/99999",
        headers=auth_headers
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


# ============================================================================
# PAPELERA
# ============================================================================

def test_listar_papelera(client, auth_headers, tareas_multiples):
    """Test de listar tareas eliminadas."""
    response = client.get(
        "/tareas/papelera/listar",
        headers=auth_headers
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 1  # Una tarea eliminada en fixture


def test_restaurar_tarea(client, auth_headers, tareas_multiples):
    """Test de restaurar tarea eliminada."""
    # Obtener tarea eliminada
    tarea_eliminada = next(t for t in tareas_multiples if t.eliminada)

    response = client.post(
        f"/tareas/{tarea_eliminada.id}/restaurar",
        headers=auth_headers
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["eliminada"] is False


def test_restaurar_tarea_no_eliminada(client, auth_headers, tarea_test):
    """Test que falla al restaurar tarea no eliminada."""
    response = client.post(
        f"/tareas/{tarea_test.id}/restaurar",
        headers=auth_headers
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
