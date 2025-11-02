# conftest.py (colócalo DENTRO de la carpeta tests de cada clase)
import os
import sys
from pathlib import Path

import pytest

# Raíz de la clase (la carpeta que contiene 'api/')
CLASE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CLASE_ROOT))


@pytest.fixture(autouse=True)
def reset_jwt_env():
    """Fixture que resetea las variables JWT antes y después de cada test.

    Esto previene contaminación entre tests cuando un test modifica
    JWT_SECRET o JWT_MINUTOS.
    """
    # Guardar valores originales
    original_secret = os.environ.get("JWT_SECRET")
    original_minutos = os.environ.get("JWT_MINUTOS")

    # Establecer valores por defecto para tests
    os.environ["JWT_SECRET"] = "secret-test"
    if "JWT_MINUTOS" in os.environ:
        del os.environ["JWT_MINUTOS"]  # Usar default (30 min)

    yield  # Ejecutar el test

    # Restaurar valores originales después del test
    if original_secret is not None:
        os.environ["JWT_SECRET"] = original_secret
    elif "JWT_SECRET" in os.environ:
        del os.environ["JWT_SECRET"]

    if original_minutos is not None:
        os.environ["JWT_MINUTOS"] = original_minutos
    elif "JWT_MINUTOS" in os.environ:
        del os.environ["JWT_MINUTOS"]
