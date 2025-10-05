import sys
from pathlib import Path

raiz_proyecto = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(raiz_proyecto))
