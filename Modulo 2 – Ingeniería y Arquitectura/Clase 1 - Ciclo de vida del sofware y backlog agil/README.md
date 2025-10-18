# Mini API de Tareas - Clase 1 Módulo 2

API REST simple para gestión de tareas, construida con FastAPI como introducción al desarrollo backend moderno.

## Características

- CRUD completo de tareas (Crear, Listar, Obtener, Completar)
- Validación automática con Pydantic
- Documentación interactiva con Swagger UI
- Tests automatizados con pytest
- Almacenamiento en memoria (se mejorará en Clase 2)

## Requisitos

- Python 3.9+
- pip

## Instalación

### 1. Crear entorno virtual

```bash
python -m venv .venv

# Activar (Windows)
.venv\Scripts\activate

# Activar (Linux/Mac)
source .venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Uso

### Ejecutar el servidor

```bash
uvicorn api.api:app --reload
```

El servidor estará disponible en `http://127.0.0.1:8000`

### Documentación interactiva

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Endpoints

| Método | Endpoint | Descripción | Status Codes |
|--------|----------|-------------|--------------|
| GET | `/health` | Health check | 200 |
| POST | `/tareas` | Crear tarea | 201, 422 |
| GET | `/tareas` | Listar tareas | 200 |
| GET | `/tareas/{id}` | Obtener tarea por ID | 200, 404 |
| PATCH | `/tareas/{id}/completar` | Completar tarea | 200, 404 |

## Ejemplos de uso

### Crear una tarea

```bash
curl -X POST "http://127.0.0.1:8000/tareas" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Aprender FastAPI", "descripcion": "Completar Clase 1"}'
```

### Listar tareas

```bash
curl http://127.0.0.1:8000/tareas
```

### Obtener una tarea específica

```bash
curl http://127.0.0.1:8000/tareas/1
```

### Completar una tarea

```bash
curl -X PATCH "http://127.0.0.1:8000/tareas/1/completar"
```

## Testing

### Ejecutar tests

```bash
pytest -v
```

### Con cobertura

```bash
pytest --cov=api --cov-report=term-missing
```

Objetivo de cobertura: >70%

### Linting

```bash
ruff check api/
```

## Estructura del Proyecto

```
├── api/
│   ├── __init__.py
│   ├── api.py              # Endpoints de la API
│   └── notes.md            # Backlog y notas del proyecto
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # Configuración de pytest
│   ├── test_health.py
│   ├── test_crear_tarea_clase1.py
│   ├── test_obtener_tarea.py
│   └── test_completar_tarea.py
├── docs/
│   └── adr/
│       └── 001-fastapi.md  # Architecture Decision Records (pendiente)
├── ejercicios/             # Ejercicios prácticos con IA (pendiente)
├── requirements.txt
├── .gitignore
└── README.md
```

## Contenido de la Clase 1

Esta clase cubre 6 horas de contenido en 4 partes:

1. **Parte 1 (1.5h)**: Ciclo de vida del software y backlog ágil
2. **Parte 2 (2h)**: Introducción práctica a FastAPI
3. **Parte 3 (1.5h)**: 5 ejercicios con IA (Product Owner, FastAPI Coach, TDD, etc.)
4. **Parte 4 (1h)**: Proyecto final integrado

## Próximos pasos (Clase 2)

- Aplicar principios SOLID en profundidad
- Separar en capas (API, Servicio, Repositorio)
- Implementar persistencia en JSON
- Añadir inyección de dependencias
- Mejorar tests (>90% cobertura)

## Tecnologías

- **FastAPI 0.115.0**: Framework web moderno
- **Pydantic 2.10.3**: Validación de datos
- **pytest 8.4.2**: Testing framework
- **httpx 0.27.2**: Cliente HTTP para tests
- **ruff 0.8.4**: Linter moderno de Python

## Licencia

Proyecto educativo - Módulo 2 del Master en IA para Desarrollo
