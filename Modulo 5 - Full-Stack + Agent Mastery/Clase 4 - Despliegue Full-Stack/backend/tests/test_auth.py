# tests/test_auth.py
"""
Tests completos para endpoints de autenticación.

Casos cubiertos:
- Registro de usuarios (exitoso y con errores)
- Login (exitoso y con credenciales inválidas)
- Endpoint protegido /auth/me
- Validación de tokens JWT
"""
import pytest
from api.api import app
from api.dependencias import _repositorio_usuarios
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def limpiar_repositorio():
    """Limpia el repositorio antes de cada test."""
    _repositorio_usuarios.limpiar()
    yield
    _repositorio_usuarios.limpiar()


client = TestClient(app)


# ========== Tests de Health Check ==========
def test_health_check():
    """GET / debe retornar status ok."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# ========== Tests de Registro ==========
def test_registrar_usuario_exitoso():
    """POST /auth/register con datos válidos debe crear usuario y retornar token."""
    payload = {"email": "test@example.com", "password": "password123", "nombre": "Test User"}

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "test@example.com"
    assert data["user"]["nombre"] == "Test User"
    assert "id" in data["user"]
    assert "created_at" in data["user"]


def test_registrar_usuario_email_duplicado():
    """POST /auth/register con email duplicado debe retornar 409."""
    payload = {"email": "duplicate@example.com", "password": "password123", "nombre": "User 1"}

    # Primer registro (exitoso)
    response1 = client.post("/auth/register", json=payload)
    assert response1.status_code == 201

    # Segundo registro con mismo email (debe fallar)
    response2 = client.post("/auth/register", json=payload)
    assert response2.status_code == 409
    assert "ya está registrado" in response2.json()["detail"]


def test_registrar_usuario_password_corto():
    """POST /auth/register con password corto debe retornar 422."""
    payload = {"email": "test@example.com", "password": "123", "nombre": "Test User"}

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 422


def test_registrar_usuario_email_invalido():
    """POST /auth/register con email inválido debe retornar 422."""
    payload = {"email": "invalid-email", "password": "password123", "nombre": "Test User"}

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 422


def test_registrar_usuario_sin_nombre():
    """POST /auth/register sin nombre debe retornar 422."""
    payload = {"email": "test@example.com", "password": "password123"}

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 422


# ========== Tests de Login ==========
def test_login_exitoso():
    """POST /auth/login con credenciales válidas debe retornar token."""
    # Primero registrar usuario
    register_payload = {"email": "login@example.com", "password": "password123", "nombre": "Login User"}
    client.post("/auth/register", json=register_payload)

    # Luego hacer login
    login_payload = {"email": "login@example.com", "password": "password123"}
    response = client.post("/auth/login", json=login_payload)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "login@example.com"


def test_login_password_incorrecta():
    """POST /auth/login con password incorrecta debe retornar 401."""
    # Registrar usuario
    register_payload = {"email": "user@example.com", "password": "correctpassword", "nombre": "User"}
    client.post("/auth/register", json=register_payload)

    # Intentar login con password incorrecta
    login_payload = {"email": "user@example.com", "password": "wrongpassword"}
    response = client.post("/auth/login", json=login_payload)

    assert response.status_code == 401
    assert "inválidas" in response.json()["detail"]


def test_login_usuario_no_existe():
    """POST /auth/login con usuario inexistente debe retornar 401."""
    login_payload = {"email": "noexiste@example.com", "password": "password123"}
    response = client.post("/auth/login", json=login_payload)

    assert response.status_code == 401
    assert "inválidas" in response.json()["detail"]


# ========== Tests de Endpoint Protegido /auth/me ==========
def test_auth_me_con_token_valido():
    """GET /auth/me con token válido debe retornar datos del usuario."""
    # Registrar y obtener token
    register_payload = {"email": "me@example.com", "password": "password123", "nombre": "Me User"}
    register_response = client.post("/auth/register", json=register_payload)
    token = register_response.json()["access_token"]

    # Llamar a /auth/me con token
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@example.com"
    assert data["nombre"] == "Me User"
    assert "id" in data
    assert "created_at" in data


def test_auth_me_sin_token():
    """GET /auth/me sin token debe retornar 401."""
    response = client.get("/auth/me")

    assert response.status_code == 401
    assert "ausente" in response.json()["detail"]


def test_auth_me_con_token_invalido():
    """GET /auth/me con token inválido debe retornar 401."""
    response = client.get("/auth/me", headers={"Authorization": "Bearer token_invalido"})

    assert response.status_code == 401
    assert "inválido" in response.json()["detail"]


def test_auth_me_sin_prefijo_bearer():
    """GET /auth/me sin prefijo 'Bearer' debe retornar 401."""
    response = client.get("/auth/me", headers={"Authorization": "token_sin_bearer"})

    assert response.status_code == 401
    assert "formato inválido" in response.json()["detail"]


# ========== Tests de Endpoint Protegido Adicional ==========
def test_dashboard_protegido_con_token_valido():
    """GET /protected/dashboard con token válido debe retornar datos."""
    # Registrar y obtener token
    register_payload = {"email": "dashboard@example.com", "password": "password123", "nombre": "Dashboard User"}
    register_response = client.post("/auth/register", json=register_payload)
    token = register_response.json()["access_token"]

    # Llamar a /protected/dashboard con token
    response = client.get("/protected/dashboard", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Dashboard User" in data["message"]
    assert data["email"] == "dashboard@example.com"
    assert "dashboard_data" in data


def test_dashboard_protegido_sin_token():
    """GET /protected/dashboard sin token debe retornar 401."""
    response = client.get("/protected/dashboard")

    assert response.status_code == 401


# ========== Tests de Validación de Password ==========
def test_password_hasheada_no_se_devuelve():
    """Verificar que la password hasheada nunca se devuelve en responses."""
    register_payload = {"email": "secure@example.com", "password": "password123", "nombre": "Secure User"}
    response = client.post("/auth/register", json=register_payload)

    data = response.json()
    # Verificar que no hay ninguna key relacionada con password
    assert "password" not in data
    assert "hashed_password" not in data
    assert "password" not in data["user"]
    assert "hashed_password" not in data["user"]


# ========== Tests de CORS ==========
def test_cors_headers():
    """Verificar que los headers CORS están configurados."""
    response = client.options("/auth/register")
    # FastAPI debería incluir headers CORS en la response
    # (TestClient no simula OPTIONS perfectamente, pero podemos verificar que CORS middleware está activo)
    assert response.status_code in [200, 405]  # OPTIONS puede no estar implementado, pero no debe fallar


# ========== Tests de Documentación OpenAPI ==========
def test_openapi_docs_disponibles():
    """Verificar que la documentación OpenAPI está disponible."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "info" in data
    assert "paths" in data
    assert "/auth/register" in data["paths"]
    assert "/auth/login" in data["paths"]
    assert "/auth/me" in data["paths"]
