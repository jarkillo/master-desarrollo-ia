import sys
from pathlib import Path

raiz_proyecto = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(raiz_proyecto))
