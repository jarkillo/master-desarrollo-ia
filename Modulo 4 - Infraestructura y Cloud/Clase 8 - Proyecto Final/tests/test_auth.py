"""
Tests de autenticación (registro, login, obtener usuario actual).
"""

from fastapi import status


def test_registrar_usuario_exitoso(client):
    """Test de registro exitoso de un nuevo usuario."""
    response = client.post(
        "/auth/register",
        json={
            "email": "nuevo@example.com",
            "nombre": "Nuevo Usuario",
            "password": "password123"
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "nuevo@example.com"
    assert data["nombre"] == "Nuevo Usuario"
    assert "password" not in data
    assert "password_hash" not in data
    assert "id" in data


def test_registrar_usuario_email_duplicado(client, usuario_test):
    """Test que falla al intentar registrar un email ya existente."""
    response = client.post(
        "/auth/register",
        json={
            "email": usuario_test.email,  # Email ya existe
            "nombre": "Otro Usuario",
            "password": "password123"
        }
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "ya está registrado" in response.json()["detail"]


def test_registrar_usuario_password_corto(client):
    """Test de validación de contraseña corta."""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "nombre": "Test User",
            "password": "123"  # Muy corto
        }
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_login_exitoso(client, usuario_test):
    """Test de login exitoso con credenciales correctas."""
    response = client.post(
        "/auth/login",
        json={
            "email": usuario_test.email,
            "password": "password123"
        }
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0


def test_login_password_incorrecta(client, usuario_test):
    """Test de login con contraseña incorrecta."""
    response = client.post(
        "/auth/login",
        json={
            "email": usuario_test.email,
            "password": "password_incorrecta"
        }
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Credenciales incorrectas" in response.json()["detail"]


def test_login_email_no_existe(client):
    """Test de login con email que no existe."""
    response = client.post(
        "/auth/login",
        json={
            "email": "noexiste@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_obtener_usuario_actual_exitoso(client, auth_headers, usuario_test):
    """Test de obtener datos del usuario autenticado."""
    response = client.get("/auth/me", headers=auth_headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == usuario_test.email
    assert data["nombre"] == usuario_test.nombre
    assert data["id"] == usuario_test.id


def test_obtener_usuario_actual_sin_token(client):
    """Test que falla al intentar acceder sin token."""
    response = client.get("/auth/me")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_obtener_usuario_actual_token_invalido(client):
    """Test que falla con token inválido."""
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer token_invalido"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
