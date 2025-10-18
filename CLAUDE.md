# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **Master's degree repository on AI-Assisted Development** organized into progressive modules (0-4). Each module builds upon the previous one, teaching software engineering fundamentals through cloud deployment. The same "tareas" (tasks) application is implemented multiple times across modules, each time with increased sophistication.

## Project Structure

### Module Organization
- **Modulo 0 - Preparacion**: Git workflows, documentation, foundational materials
- **Modulo 1 - Fundamentos**: CLI applications, basic Python, testing introduction
- **Modulo 2 - Ingeniería y Arquitectura**: FastAPI, SOLID principles, clean architecture
- **Modulo 3 - Calidad y Seguridad**: Security hardening, JWT, Sentry, auditing
- **Modulo 4 - Infraestructura y Cloud**: Docker, deployment, infrastructure as code

### Self-Contained Class Design
Each class folder is **completely independent** and can be run/tested in isolation. Every class from Module 2+ follows this structure:

```
Clase X/
├── api/
│   ├── api.py                    # FastAPI application with endpoints
│   ├── servicio_tareas.py        # Service layer (business logic)
│   ├── repositorio_base.py       # Protocol/Interface (Dependency Inversion)
│   ├── repositorio_memoria.py    # In-memory implementation
│   ├── repositorio_json.py       # JSON file persistence
│   ├── dependencias.py           # (Module 3+) Dependency injection
│   └── seguridad_jwt.py          # (Module 3 Class 4+) JWT auth
├── tests/
│   ├── conftest.py               # Path configuration for imports
│   └── test_*.py                 # Unit tests
├── tests_integrations/
│   └── test_integracion_*.py     # Integration tests for repositories
└── infra/                        # (Module 4) Infrastructure configs
```

## Architecture Patterns

### Clean Architecture with Dependency Inversion
The codebase demonstrates SOLID principles through a layered architecture:

1. **Repository Pattern**: Abstract interface (`RepositorioTareas` Protocol) with multiple implementations
   - `RepositorioMemoria`: In-memory storage (for tests/demos)
   - `RepositorioJSON`: File-based persistence

2. **Service Layer**: `ServicioTareas` contains business logic, depends only on the repository abstraction
   ```python
   class ServicioTareas:
       def __init__(self, repositorio: RepositorioTareas):
           self._repo = repositorio
   ```

3. **API Layer**: FastAPI endpoints use the service layer through dependency injection

### Test Strategy
- **Unit tests** (`tests/`): Test individual components in isolation
- **Integration tests** (`tests_integrations/`): Test repository implementations
- All tests use `conftest.py` to add parent directory to `sys.path` for imports
- Tests use FastAPI's `TestClient` for endpoint testing

## Common Development Commands

### Running Tests

**Test a specific class** (run from within the class directory):
```bash
cd "Modulo X/Clase Y - Topic"
pytest
```

**Test with coverage** (minimum 80% required in CI):
```bash
pytest --cov=api --cov-report=term-missing --cov-fail-under=80
```

**Test specific file**:
```bash
pytest tests/test_crear_tarea_claseX.py -v
```

**Integration tests only**:
```bash
pytest tests_integrations/ -v
```

### Running the API

**From class directory** (most modules 2+):
```bash
cd "Modulo X/Clase Y - Topic"
uvicorn api.api:app --reload
```

**With Docker** (Module 4, Class 2):
```bash
cd "Modulo 4 - Infraestructura y Cloud/Clase 2 - Tu API en un contenedor"
docker build -t api-tareas .
docker run -p 8000:8000 api-tareas
```

### Quality & Security Checks

**Linting** (Ruff - modern, fast linter):
```bash
ruff check api/
```

**Security audit** (Bandit):
```bash
bandit -r api/ -ll
```

**Dependency security** (Safety):
```bash
safety check
```

## Environment Setup

### Python Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables
Copy `.env.template` to `.env` and configure:
```
API_KEY=your_api_key_here
JWT_SECRET=your_secret_key_here
DATABASE_URL=your_database_url
MODE=dev
```

**Important**: Module 4 classes have `infra/.env.template` with validation via `python infra/check_env.py`

## CI/CD Workflows

### `.github/workflows/ci.yml`
Basic test workflow:
- Runs `pytest -q` on specified class directories
- Python 3.12, Ubuntu latest
- Cleans `__pycache__` before running

### `.github/workflows/ci_quality.yml`
Comprehensive quality pipeline:
- **Test coverage**: 80% minimum (`--cov-fail-under=80`)
- **Ruff linting**: Fast Python linter
- **Bandit**: Security audit (`-ll` flag)
- **Safety**: Dependency vulnerability scanning
- **Gitleaks**: Secret scanning
- **Environment validation**: Runs `infra/check_env.py`

**To update which classes are tested**: Edit the `matrix.class_dir` list in both workflow files.

## Technology Stack

**Core**:
- FastAPI 0.118.0 + Uvicorn 0.37.0 (web framework)
- Pydantic 2.11.10 (data validation)
- Python 3.12

**Testing**:
- Pytest 8.4.2 + pytest-cov (testing framework)
- httpx 0.27.2 (HTTP client for API tests)

**Security**:
- python-jose[cryptography] (JWT handling)
- Bandit (security linting)
- Safety (dependency scanning)

**Observability**:
- Sentry-sdk[fastapi] (error tracking - Module 3 Class 7)

**Quality**:
- Ruff (modern Python linter)

## Key Patterns to Follow

### Adding a New Endpoint
1. Define request/response models using Pydantic with validation (e.g., `Field(..., min_length=1)`)
2. Implement business logic in service layer
3. Add endpoint to `api.py` using dependency injection
4. Write tests FIRST (TDD approach emphasized throughout)

### Implementing a New Repository
1. Ensure it implements the `RepositorioTareas` Protocol
2. Add integration tests in `tests_integrations/`
3. Update dependency injection if needed

### Security Considerations (Module 3+)
- Use Pydantic validation for all inputs
- JWT secrets via environment variables (never hardcoded)
- Check `seguridad_jwt.py` for authentication patterns (Module 3 Class 4+)
- Sentry integration for production observability (Module 3 Class 7)

## Working with Different Modules

**Module 1**: Simple CLI apps, focus on fundamentals. Run directly: `python tareas.py`

**Module 2**: Introduction to FastAPI and clean architecture. Each class builds progressively on SOLID principles.

**Module 3**: Security hardened. JWT authentication introduced in Class 4, Sentry in Class 7. Always validate environment variables.

**Module 4**: Infrastructure focus. Use Docker commands, check `infra/` directories for deployment configs.

## Important Notes

- Each class is self-contained - changes in one class don't affect others
- Always run tests from the class directory (not root) due to `conftest.py` path setup
- CI/CD is configured for the latest working class (currently Module 4, Class 2)
- Coverage threshold is 80% - tests will fail below this
- Follow TDD: tests are written before implementation in most classes

## Known Issues & Gaps

⚠️ **IMPORTANT**: This repository is approximately **65% complete**. Before making changes, review:

- **`docs/reviews/REVIEW_COMPLETENESS.md`**: Missing components, inconsistencies, incomplete modules
- **`docs/reviews/REVIEW_PEDAGOGICAL.md`**: Conceptual gaps, learning progression issues
- **`docs/reviews/AGENTS_RECOMMENDED.md`**: Recommended specialist agents for educational support

### Critical Gaps to Be Aware Of

1. **Module 4 is only 25% complete** - Only Classes 1-2 exist, Classes 3-8 (database, cloud deployment) are missing
2. **Module 5 is completely absent** - DevSecOps and full-stack content not yet implemented
3. **Test naming inconsistency** - Module 3-4 tests incorrectly named `test_crear_tarea_clase7.py`
4. **CI/CD only tests one class** - Most implemented classes are not in the CI matrix
5. **Async Python not taught** - FastAPI is used synchronously, async/await patterns missing
6. **No database integration** - Promised in Module 4 but not implemented (SQLAlchemy, Alembic)
7. **Error handling patterns missing** - No custom exceptions, HTTPException handlers

### Working Around Gaps

**When adding database features**: Module 4 Classes 3-4 need to be implemented first (SQLAlchemy + Alembic)

**When fixing tests**: Module 3-4 test files need renaming from `clase7` to correct class numbers

**When updating CI**: Add all implemented classes to `.github/workflows/ci.yml` and `ci_quality.yml` matrices

**When teaching async**: This is a critical gap - consider implementing Module 2 Class 3.5 (Async Python)

### Test File Naming Convention

**Correct pattern** (Module 2):
```
tests/test_crear_tarea_clase2.py
tests/test_crear_tarea_clase3.py
```

**Incorrect pattern** (Module 3-4, needs fixing):
```
tests/test_crear_tarea_clase7.py  ❌ All files incorrectly named
```

**Recommended fix**: Rename to `test_crear_tarea_clase{X}_mod{Y}.py` for clarity

### Missing Documentation

- 3 glossaries missing: Module 3 Class 1, Module 3 Class 7, Module 4 Class 1
- 4 glossaries without `.md` extension
- Module-level READMEs absent for Modules 1-3

## Educational Context

This repository is designed for **progressive learning** where students:

1. Build the same application multiple times with increasing complexity
2. Learn by refactoring and extending previous work
3. Experience the "pain points" that motivate architectural patterns
4. Use AI as a learning assistant throughout

**Teaching Philosophy**:
- Concepts are introduced **when the pain is felt** (e.g., architecture after maintaining messy code)
- **Analogies** are used heavily (API = counter, Service = mechanic, Repository = storage)
- **Test-Driven Development** is emphasized from Module 1
- **Security** is integrated progressively, not bolted on
- **Real tools** are used (GitHub Actions, Sentry, Docker) not simplified versions

## Recommended Specialist Agents

For complex educational tasks, consider using specialized agents (see `docs/reviews/AGENTS_RECOMMENDED.md`):

**Tier 1 (Critical)**:
- **FastAPI Design Coach**: REST API design, Pydantic, async patterns
- **Test Coverage Strategist**: Test architecture, coverage optimization
- **Clean Architecture Enforcer**: SOLID principles, layering
- **Docker & Infrastructure Guide**: Containers, deployment

**Tier 2 (High Value)**:
- **Security Hardening Mentor**: Explains security findings educationally
- **CI/CD Pipeline Optimizer**: GitHub Actions, quality gates
- **Python Best Practices Coach**: Type hints, pythonic patterns
- **Database Design & ORM Specialist**: SQLAlchemy, migrations (when Module 4 DB classes exist)

These agents **teach and explain**, not just validate. They provide context and "why", not just "what's wrong".

## Module Completion Status

| Module | Status | Classes | Notes |
|--------|--------|---------|-------|
| Module 0 | ✅ Complete | - | Git, setup, documentation |
| Module 1 | ✅ Complete | 4/4 | CLI, fundamentals, basic testing |
| Module 2 | ⚠️ Mostly Complete | 5/6 | Class 1 only has notes, no code |
| Module 3 | ✅ Complete | 7/7 | All classes implemented (test naming issue) |
| Module 4 | 🔴 25% Complete | 2/8 | Missing DB, cloud deployment, LangChain |
| Module 5 | ❌ Not Started | 0/6+ | DevSecOps, full-stack completely absent |

**Overall**: ~65% complete

## Development Priorities

If you're continuing this project, prioritize:

1. **Fix critical inconsistencies** (1-2 days): Rename tests, update CI matrix, add `.md` extensions
2. **Complete Module 4** (3-4 weeks): Database integration, migrations, cloud deployment
3. **Add async/await teaching** (1 week): Critical gap in Module 2
4. **Implement error handling** (1 week): Custom exceptions, HTTPException patterns
5. **Create Module 5** (2-3 weeks): Full-stack, DevSecOps, final project

See `docs/reviews/REVIEW_COMPLETENESS.md` for detailed action items and estimates.
