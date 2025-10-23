# tests/conftest.py
import sys
from pathlib import Path

# Agregar el directorio backend al path para imports
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))
