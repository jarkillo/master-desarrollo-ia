# Módulo 2 - Ingeniería y Arquitectura

## Overview

Este módulo introduce **arquitectura de software profesional** y **principios SOLID**, transformando aplicaciones CLI simples en APIs REST con FastAPI. Los estudiantes aprenderán a diseñar sistemas escalables, aplicar patrones arquitectónicos, y usar IA como agente especializado en revisión de arquitectura.

**Visión del módulo**: Diseñar software que crece sin romperse, aplicando principios de ingeniería de software con asistencia de agentes IA especializados.

## Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

1. **Diseñar APIs REST**: Construir endpoints profesionales con FastAPI
2. **Aplicar SOLID completo**: Implementar los 5 principios en código real
3. **Implementar arquitectura limpia**: Separar responsabilidades en capas (API, Service, Repository)
4. **Usar patrones de diseño**: Repository Pattern, Dependency Injection, Strategy Pattern
5. **Orquestar agentes IA**: Usar agentes especializados para validación, diseño y testing
6. **Implementar CI/CD**: Configurar pipelines de calidad (linting, tests, cobertura)

## Prerrequisitos

- Completar Módulo 1 (o equivalente)
- Python 3.12+
- Conocimientos de pytest
- Comprensión básica de HTTP y REST
- Git y GitHub configurados

## Estructura del Módulo

### Clase 1 - Ciclo de Vida del Software y Backlog Ágil
**Duración**: 3h | **Tipo**: Conceptual + Primera API

**Contenido**:
- Ciclo de vida del desarrollo (análisis, diseño, implementación, pruebas, despliegue)
- Metodologías ágiles: Scrum, Kanban
- Backlog de producto y gestión de tareas
- Introducción a FastAPI

**Proyecto**: Primera API REST de tareas
- `api/api.py` - Endpoints básicos (GET, POST)
- Tests unitarios con TestClient
- Almacenamiento en memoria

**Artefactos**:
- `Clase 1 - Ciclo de vida del sofware y backlog agil.md` - Material teórico
- `Glosario - Clase 1.md` - Términos de ingeniería de software
- `README.md` - Documentación de la API

### Clase 2 - Principios SOLID y Paradigmas de Programación
**Duración**: 4h | **Tipo**: Principios + Refactorización

**Contenido**:
- **S**ingle Responsibility Principle (SRP)
- **O**pen/Closed Principle (OCP) - Introducción
- **L**iskov Substitution Principle (LSP)
- **I**nterface Segregation Principle (ISP)
- **D**ependency Inversion Principle (DIP) - Introducción
- Paradigmas: POO vs Funcional

**Proyecto**: API refactorizada con SRP
- Separación de lógica de API y lógica de negocio
- Introducción a la capa de servicio

**Artefactos**:
- `Clase 2 - Principios SOLID y paradigmas de programacion.md` - Material teórico
- `Glosario - Clase 2.md` - Términos de SOLID
- `AI_WORKFLOW.md` - Workflow con IA para validación SOLID
- `EJERCICIOS_IA.md` - Ejercicios prácticos con agentes

### Clase 3 - Arquitectura Limpia
**Duración**: 4h | **Tipo**: Arquitectura + Patrones

**Contenido**:
- Clean Architecture (Uncle Bob)
- Separación en capas: API → Service → Repository (conceptual)
- Validación de datos con Pydantic
- Manejo de errores profesional

**Proyecto**: API con tres capas claramente definidas
- `api/api.py` - Capa de presentación (endpoints)
- `api/servicio_tareas.py` - Capa de lógica de negocio
- Validación avanzada con Pydantic

**Artefactos**:
- `Clase 3 - Arquitectura limpia.md` - Material teórico
- `Glosario - Clase 3.md` - Términos de arquitectura
- `AI_VALIDATION_WORKFLOW.md` - Validación de arquitectura con IA
- `test_validaciones_avanzadas_clase3.py` - Tests de validación

### Clase 4 - Open/Closed y Dependency Inversion
**Duración**: 4h | **Tipo**: Patrones Avanzados

**Contenido**:
- **Open/Closed Principle** en profundidad
- **Dependency Inversion Principle** en profundidad
- Repository Pattern (abstracción + implementaciones)
- Protocols de Python (typing)

**Proyecto**: API con Repository Pattern
- `api/repositorio_base.py` - Protocol (interfaz)
- `api/repositorio_memoria.py` - Implementación en memoria
- `api/repositorio_json.py` - Implementación con persistencia JSON
- Dependency Injection básica

**Artefactos**:
- `Clase 4 - Open_Closed y Dependency Inversion.md` - Material teórico
- `Glosario - Clase 4.md` - Términos de patrones
- `AI_REPOSITORY_WORKFLOW.md` - Diseño de repositorios con IA
- `EJERCICIOS_REPOSITORY.md` - Ejercicios de patrones
- `tests_integrations/` - Tests de integración de repositorios

### Clase 5 - Integración y Pruebas de Arquitectura
**Duración**: 4h | **Tipo**: Testing Avanzado

**Contenido**:
- Tests unitarios vs tests de integración
- Testing de arquitectura en capas
- Cobertura de código (80% mínimo)
- Mocking y fixtures avanzados

**Proyecto**: API completamente testeada
- Tests unitarios por capa
- Tests de integración de repositorios
- Cobertura 80%+

**Artefactos**:
- `Clase 5 - Integracion y pruebas de arquitectura.md` - Material teórico
- `Glosario - Clase 5.md` - Términos de testing
- `AI_TESTING_WORKFLOW.md` - Generación de tests con IA
- `EJERCICIOS_TESTING.md` - Ejercicios de testing
- `tests_integrations/test_integracion_repositorios_Clase5.py`

### Clase 6 - Integración Continua y Control de Calidad
**Duración**: 4h | **Tipo**: CI/CD + Herramientas

**Contenido**:
- CI/CD con GitHub Actions
- Linting automático (Ruff)
- Tests automáticos con cobertura
- Pre-commit hooks y pre-push hooks
- Auditoría de seguridad (Bandit)

**Proyecto**: API con pipeline completo de CI/CD
- `.github/workflows/ci.yml` - Tests automáticos
- `.github/workflows/ci_quality.yml` - Pipeline de calidad completo
- `.githooks/pre-push` - Validación local

**Artefactos**:
- `Clase 6 - Integracion continua y control de calidad.md` - Material teórico
- `Glosario - Clase 6.md` - Términos de CI/CD

## Arquitectura de Referencia

Todas las clases (a partir de Clase 3) implementan esta arquitectura:

```
api/
├── __init__.py
├── api.py                    # Capa API (endpoints FastAPI)
├── servicio_tareas.py        # Capa Service (lógica de negocio)
├── repositorio_base.py       # Protocol (abstracción)
├── repositorio_memoria.py    # Implementación en memoria
└── repositorio_json.py       # Implementación con persistencia

tests/
├── conftest.py               # Configuración de tests
├── test_crear_tarea_claseX.py
└── test_*.py

tests_integrations/
├── conftest.py
└── test_integracion_repositorios_claseX.py
```

### Flujo de Datos

```
Cliente HTTP
    ↓
API Layer (FastAPI endpoints)
    ↓
Service Layer (lógica de negocio)
    ↓
Repository Layer (persistencia)
    ↓
Storage (memoria / JSON / DB)
```

### Principios Aplicados

- **SRP**: Cada capa tiene una sola responsabilidad
- **OCP**: Nuevos repositorios sin modificar servicio
- **LSP**: Cualquier repositorio es intercambiable
- **ISP**: Protocol `RepositorioTareas` con interfaz mínima
- **DIP**: Service depende de abstracción, no de implementación

## Tecnologías Utilizadas

- **FastAPI 0.118.0**: Framework web moderno
- **Uvicorn 0.37.0**: ASGI server
- **Pydantic 2.11.10**: Validación de datos
- **pytest 8.4.2**: Testing framework
- **httpx 0.27.2**: Cliente HTTP para tests
- **Ruff**: Linting moderno
- **Bandit**: Auditoría de seguridad
- **GitHub Actions**: CI/CD

## Cómo Ejecutar los Proyectos

### Configuración inicial (una vez)

```bash
# Activar entorno virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar la API

```bash
# Navegar a una clase específica
cd "Modulo 2 – Ingeniería y Arquitectura/Clase 5 - Integracion y pruebas de arquitectura"

# Ejecutar servidor
uvicorn api.api:app --reload

# La API estará disponible en:
# http://localhost:8000
# Documentación interactiva: http://localhost:8000/docs
```

### Ejecutar tests

```bash
# Tests unitarios
pytest tests/ -v

# Tests de integración
pytest tests_integrations/ -v

# Todos los tests con cobertura
pytest --cov=api --cov-report=term-missing --cov-fail-under=80

# Test específico
pytest tests/test_crear_tarea_clase5.py -v
```

### Validación de calidad (local)

```bash
# Linting
ruff check api/

# Auditoría de seguridad
bandit -r api/ -ll

# Validación completa (pre-push hook)
bash scripts/pre-pr-check.sh
```

## Progresión del Aprendizaje

**Estrategia pedagógica: "Del dolor a la solución"**

1. **Clase 1**: API simple en un solo archivo → Sientes la necesidad de organización
2. **Clase 2**: Separas responsabilidades → Entiendes SRP por experiencia
3. **Clase 3**: Tres capas claras → Arquitectura limpia emerge naturalmente
4. **Clase 4**: Múltiples implementaciones → OCP y DIP cobran sentido
5. **Clase 5**: Tests exhaustivos → Validación de arquitectura
6. **Clase 6**: CI/CD automático → Calidad sostenible

Cada clase **refactoriza la anterior** aplicando nuevos principios, creando un aprendizaje experiencial.

## Uso de IA en Este Módulo

### Agentes Especializados Disponibles

Los siguientes agentes educativos están disponibles en `.claude/agents/educational/`:

1. **Python Best Practices Coach**: Revisión de código Pythonic
2. **FastAPI Design Coach**: Diseño profesional de APIs REST
3. **API Design Reviewer**: Validación de principios RESTful
4. **Performance Optimizer**: Optimización de rendimiento

### Workflows con IA

Cada clase incluye un documento `AI_*_WORKFLOW.md` con prompts específicos:

- **Clase 2**: `AI_WORKFLOW.md` - Validación de SOLID
- **Clase 3**: `AI_VALIDATION_WORKFLOW.md` - Revisión de arquitectura
- **Clase 4**: `AI_REPOSITORY_WORKFLOW.md` - Diseño de repositorios
- **Clase 5**: `AI_TESTING_WORKFLOW.md` - Generación de tests

**Ejemplo de uso**:

```bash
# Validar que tu API cumple SOLID
claude code "Revisa mi API en api/api.py usando los principios SOLID del AI_WORKFLOW.md"

# Generar tests de integración
claude code "Genera tests de integración para RepositorioJSON siguiendo AI_TESTING_WORKFLOW.md"
```

## Ejercicios Prácticos

Cada clase incluye ejercicios progresivos:

- **EJERCICIOS_IA.md** (Clase 2): Refactorización con agentes
- **EJERCICIOS_REPOSITORY.md** (Clase 4): Implementar nuevos repositorios
- **EJERCICIOS_TESTING.md** (Clase 5): Cobertura exhaustiva

## Próximos Pasos

Después de completar este módulo:

➡️ **Módulo 3 - Seguridad + IA con Criterio**: Aprenderás JWT, OWASP Top 10, auditoría de seguridad y revisión crítica de código generado por IA.

## Problemas Conocidos

⚠️ Según `CLAUDE.md`, hay algunas inconsistencias conocidas:

- **Clase 1 solo tiene notas** (`notes.md`), no implementación completa
- **Tests incorrectamente nombrados**: Algunos archivos se llaman `test_crear_tarea_clase7.py` en lugar del número correcto
- **CI/CD solo prueba algunas clases**: No todas las clases están en la matriz de CI

Estas inconsistencias están documentadas en `docs/reviews/REVIEW_COMPLETENESS.md` y se están corrigiendo progresivamente.

## Recursos Adicionales

- **Glosarios**: Cada clase tiene terminología técnica específica
- **AI Workflows**: Prompts optimizados para cada tarea arquitectónica
- **Documentación FastAPI**: https://fastapi.tiangolo.com/
- **SOLID en Python**: https://realpython.com/solid-principles-python/

## Contribuciones

Si encuentras errores o mejoras:

1. Abre un issue en el repositorio
2. Describe el problema con ejemplos
3. Sugiere la solución (si aplica)

---

**¿Listo para diseñar software profesional?** Comienza en [Clase 1 - Ciclo de vida del sofware y backlog agil](./Clase%201%20-%20Ciclo%20de%20vida%20del%20sofware%20y%20backlog%20agil/Clase%201%20-%20Ciclo%20de%20vida%20del%20sofware%20y%20backlog%20agil.md) 🏗️
