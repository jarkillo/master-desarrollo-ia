# conftest.py (colócalo DENTRO de la carpeta tests de cada clase)
import sys
from pathlib import Path

# Raíz de la clase (la carpeta que contiene 'api/')
CLASE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CLASE_ROOT))
