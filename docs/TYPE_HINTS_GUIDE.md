# Guía de Type Hints - Python 3.12

Esta guía documenta las mejores prácticas de type hints para el proyecto master-ia-manu usando Python 3.12.

## 🎯 Objetivo

Usar type hints estrictos para:
- Detectar errores en tiempo de desarrollo (no en producción)
- Mejorar autocompletado en IDEs
- Documentar contratos de funciones
- Facilitar refactoring seguro

## 📚 Sintaxis Moderna de Python 3.12

### 1. Type Aliases con `type` keyword

```python
# ❌ Antiguo (Python < 3.12)
from typing import List, Dict
UserDict = Dict[str, str]
UserList = List[UserDict]

# ✅ Nuevo (Python 3.12+)
type UserId = int
type UserName = str
type UserDict = dict[str, str]
type UserList = list[UserDict]
```

### 2. Union Types con `|` (desde Python 3.10)

```python
# ❌ Antiguo
from typing import Optional, Union
def get_user(id: int) -> Optional[dict]:
    ...

# ✅ Nuevo
def get_user(id: int) -> dict | None:
    ...

def process(value: str | int | float) -> str:
    ...
```

### 3. Colecciones Genéricas Built-in

```python
# ❌ Antiguo (Python < 3.9)
from typing import List, Dict, Set, Tuple

def foo(items: List[str]) -> Dict[str, int]:
    ...

# ✅ Nuevo (Python 3.12)
def foo(items: list[str]) -> dict[str, int]:
    ...

# También:
def bar() -> set[int]: ...
def baz() -> tuple[str, int, bool]: ...
```

### 4. Protocols para Duck Typing

```python
from typing import Protocol

class RepositorioTareas(Protocol):
    """Define el contrato sin implementación"""

    def crear(self, tarea: dict[str, str]) -> dict[str, str | int]:
        ...

    def obtener(self, id: int) -> dict[str, str | int] | None:
        ...

# Cualquier clase que implemente estos métodos
# será compatible automáticamente
class RepositorioMemoria:
    def crear(self, tarea: dict[str, str]) -> dict[str, str | int]:
        # implementación
        return {"id": 1, **tarea}

    def obtener(self, id: int) -> dict[str, str | int] | None:
        # implementación
        return None
```

### 5. Literal Types para Valores Específicos

```python
from typing import Literal

type EstadoTarea = Literal["pendiente", "en_progreso", "completada"]
type Prioridad = Literal["baja", "media", "alta", "urgente"]

def cambiar_estado(
    tarea_id: int,
    estado: EstadoTarea  # Solo acepta estos 3 valores
) -> None:
    ...

# Mypy validará en tiempo de desarrollo:
cambiar_estado(1, "pendiente")  # ✅ OK
cambiar_estado(1, "cancelada")  # ❌ Error de mypy
```

## 🔧 Uso en FastAPI

### Pydantic Models

```python
from pydantic import BaseModel, Field

class TareaCreate(BaseModel):
    """Schema para crear tareas - Pydantic valida en runtime"""
    titulo: str = Field(..., min_length=1, max_length=200)
    descripcion: str = Field(..., min_length=1)
    prioridad: Literal["baja", "media", "alta"] = "media"

class TareaResponse(BaseModel):
    """Schema para respuestas"""
    id: int
    titulo: str
    descripcion: str
    completada: bool = False
    prioridad: Literal["baja", "media", "alta"]
```

### Endpoints con Type Hints

```python
from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()

@app.post("/tareas", response_model=TareaResponse, status_code=201)
async def crear_tarea(
    tarea: TareaCreate,  # Validación automática de Pydantic
    repo: RepositorioTareas = Depends(get_repositorio)
) -> TareaResponse:
    """
    Crea una nueva tarea

    - **titulo**: Título de la tarea (1-200 chars)
    - **descripcion**: Descripción detallada
    - **prioridad**: Nivel de prioridad
    """
    resultado = repo.crear(tarea.model_dump())
    return TareaResponse(**resultado)

@app.get("/tareas/{tarea_id}", response_model=TareaResponse)
async def obtener_tarea(
    tarea_id: int,
    repo: RepositorioTareas = Depends(get_repositorio)
) -> TareaResponse:
    tarea = repo.obtener(tarea_id)
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return TareaResponse(**tarea)
```

## 🧪 Type Hints en Tests

```python
from typing import Generator
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Fixture que retorna un TestClient"""
    from api.api import app
    with TestClient(app) as c:
        yield c

def test_crear_tarea(client: TestClient) -> None:
    """Test con type hints claros"""
    response = client.post(
        "/tareas",
        json={"titulo": "Test", "descripcion": "Test desc"}
    )
    assert response.status_code == 201

    data: dict[str, str | int] = response.json()
    assert "id" in data
```

## 📝 Funciones con Type Hints Completos

```python
from collections.abc import Sequence, Callable

def procesar_tareas(
    tareas: Sequence[dict[str, str | int]],  # Acepta list, tuple, etc.
    filtro: Callable[[dict[str, str | int]], bool],
    max_resultados: int | None = None
) -> list[dict[str, str | int]]:
    """
    Procesa tareas aplicando un filtro

    Args:
        tareas: Secuencia de tareas a procesar
        filtro: Función que retorna True para tareas a incluir
        max_resultados: Límite de resultados (None = sin límite)

    Returns:
        Lista de tareas filtradas

    Raises:
        ValueError: Si tareas está vacía

    Example:
        >>> tareas = [{"id": 1, "titulo": "Tarea 1"}]
        >>> filtradas = procesar_tareas(tareas, lambda t: t["id"] > 0)
    """
    if not tareas:
        raise ValueError("La lista de tareas no puede estar vacía")

    resultado = [t for t in tareas if filtro(t)]

    if max_resultados is not None:
        resultado = resultado[:max_resultados]

    return resultado
```

## 🛠️ Herramientas

### Mypy (Type Checking Estático)

```bash
# Verificar un archivo
mypy api/api.py

# Verificar un directorio
mypy api/

# Con configuración personalizada
mypy --config-file pyproject.toml api/

# Usar script del proyecto
bash scripts/check_types.sh
```

### Ruff (Linter Moderno)

```bash
# Verificar código
ruff check api/

# Auto-fix
ruff check --fix api/

# Formatear
ruff format api/
```

## 📊 Configuración de Mypy (pyproject.toml)

```toml
[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true  # Requiere types en todas las funciones
no_implicit_optional = true
warn_redundant_casts = true
strict_equality = true
show_error_codes = true
```

## ✅ Checklist de Type Hints

Antes de hacer commit:

- [ ] Todas las funciones públicas tienen type hints
- [ ] Parámetros y return types especificados
- [ ] Usada sintaxis moderna (`dict` en vez de `Dict`, `|` en vez de `Union`)
- [ ] Protocols usados para interfaces
- [ ] Literales usados para valores específicos
- [ ] `mypy` pasa sin errores
- [ ] `ruff check` pasa sin errores
- [ ] Tests tienen type hints básicos

## 🚀 Comandos Útiles

```bash
# Activar entorno virtual
source .venv/bin/activate

# Verificar types
bash scripts/check_types.sh

# Linting
ruff check api/

# Tests con coverage
pytest --cov=api --cov-report=term-missing

# Todo junto (pre-commit check)
ruff check api/ && mypy api/ && pytest
```

## 📚 Referencias

- [Python Type Hints - PEP 484](https://peps.python.org/pep-0484/)
- [Type Aliases - PEP 613](https://peps.python.org/pep-0613/)
- [Union Types with | - PEP 604](https://peps.python.org/pep-0604/)
- [Mypy Documentation](https://mypy.readthedocs.io/)
- [FastAPI Type Hints](https://fastapi.tiangolo.com/python-types/)
- [Pydantic Models](https://docs.pydantic.dev/)
