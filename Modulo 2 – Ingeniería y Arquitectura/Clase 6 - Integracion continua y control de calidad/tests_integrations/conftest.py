# integration_tests/conftest.py
import sys
from pathlib import Path

# Subimos dos niveles desde esta carpeta hasta la raíz del proyecto
raiz_proyecto = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(raiz_proyecto))
