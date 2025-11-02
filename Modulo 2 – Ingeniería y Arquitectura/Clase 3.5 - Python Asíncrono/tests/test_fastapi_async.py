"""
Tests para endpoints FastAPI async
Requiere: pytest pytest-asyncio httpx
Ejecutar: pytest tests/test_fastapi_async.py -v
"""

from examples.fastapi_async import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_dashboard_lento_retorna_200():
    """Test que dashboard lento retorna 200 y datos correctos"""
    response = client.get("/dashboard-lento")
    assert response.status_code == 200

    data = response.json()
    assert "usuarios" in data
    assert "productos" in data
    assert "pedidos" in data
    assert "tiempo_ms" in data
    assert data["metodo"] == "secuencial"


def test_dashboard_rapido_retorna_200():
    """Test que dashboard rápido retorna 200 y datos correctos"""
    response = client.get("/dashboard-rapido")
    assert response.status_code == 200

    data = response.json()
    assert "usuarios" in data
    assert "productos" in data
    assert "pedidos" in data
    assert "tiempo_ms" in data
    assert data["metodo"] == "paralelo"


def test_dashboard_rapido_es_mas_rapido():
    """Test que dashboard rápido es significativamente más rápido"""
    # Dashboard lento
    response_lento = client.get("/dashboard-lento")
    tiempo_lento = response_lento.json()["tiempo_ms"]

    # Dashboard rápido
    response_rapido = client.get("/dashboard-rapido")
    tiempo_rapido = response_rapido.json()["tiempo_ms"]

    # Rápido debe ser al menos 30% más rápido
    assert tiempo_rapido < tiempo_lento * 0.7


def test_dashboard_robusto_maneja_errores():
    """Test que dashboard robusto maneja errores sin fallar"""
    response = client.get("/dashboard-robusto")
    assert response.status_code == 200

    data = response.json()
    assert "usuarios" in data
    assert "productos" in data
    assert "servicio_extra" in data

    # servicio_extra puede tener error o status ok
    servicio = data["servicio_extra"]
    assert "error" in servicio or "status" in servicio


def test_async_io_endpoint():
    """Test endpoint async para I/O"""
    response = client.get("/async-io")
    assert response.status_code == 200
    assert "mensaje" in response.json()


def test_sync_cpu_endpoint():
    """Test endpoint sync para CPU"""
    response = client.get("/sync-cpu")
    assert response.status_code == 200
    data = response.json()
    assert "resultado" in data
    assert data["resultado"] == sum(range(1000))


def test_todos_los_endpoints_retornan_json():
    """Test que todos los endpoints retornan JSON válido"""
    endpoints = [
        "/dashboard-lento",
        "/dashboard-rapido",
        "/dashboard-robusto",
        "/async-io",
        "/sync-cpu"
    ]

    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        data = response.json()  # Verifica que es JSON válido
        assert isinstance(data, dict)
