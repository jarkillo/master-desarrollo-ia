# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **Master's degree repository on AI-Assisted Development** organized into progressive modules (0-5). Each module builds upon the previous one, teaching **software engineering fundamentals + AI as a force multiplier**. The vision: **"A solo developer with an army of agents"**.

The same "tareas" (tasks) application is implemented multiple times across modules, each time with increased sophistication, using AI assistants progressively.

## Project Structure

### Module Organization
- **Modulo 0 - IA Development Foundations**: AI tools setup, prompt engineering, first agents, Git + IA workflow
- **Modulo 1 - Fundamentos + IA Assistant**: CLI applications, Python basics, testing with AI assistance
- **Modulo 2 - Arquitectura + Agent Orchestration**: FastAPI, SOLID, clean architecture, specialized agent teams
- **Modulo 3 - Seguridad + IA con Criterio**: Security hardening, JWT, auditing AI-generated code
- **Modulo 4 - Infrastructure + AI DevOps**: Docker, databases, cloud deployment with AI agents
- **Modulo 5 - Full-Stack + Agent Mastery**: Complete projects with orchestrated agent teams

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
- **`docs/reviews/REVIEW_AI_INTEGRATION.md`**: **CRITICAL** - AI integration gaps, curriculum redesign
- **`docs/reviews/AGENTS_RECOMMENDED.md`**: Recommended specialist agents for educational support

### 🤖 The AI Integration Gap

**CRITICAL FINDING**: The program currently teaches excellent software engineering but **lacks AI dimension entirely**.

Current state:
- ✅ Clean Code, SOLID, FastAPI, Docker
- ❌ How to use Claude Code effectively
- ❌ Agent design and orchestration
- ❌ Prompt engineering for development
- ❌ Security review of AI-generated code
- ❌ Dividing projects for AI assistance

**Vision**: After this master, you should be **"a solo developer with an army of agents"** - able to build production applications alone using specialized AI agents.

**See `docs/reviews/REVIEW_AI_INTEGRATION.md`** for complete analysis and redesigned curriculum.

### Critical Gaps to Be Aware Of

**AI Integration**:
1. ~~**Module 0 needs complete redesign**~~ - ✅ **COMPLETED**: Module 0 redesigned with 6 classes (Clase 0-6) teaching AI development foundations
2. **No AI teaching in any module** - Modules 1-4 are pure software engineering (needs 40% AI integration)
3. ~~**No agent library**~~ - ✅ **COMPLETED**: 7 educational agents created in `.claude/agents/educational/`
4. **No prompt engineering** - Core skill for AI-assisted development (partially addressed in Module 0 Clase 5)

**Implementation**:
5. **Module 4 is only 25% complete** - Only Classes 1-2 exist, Classes 3-8 (database, cloud deployment) are missing
6. **Module 5 is completely absent** - Full-stack + agent orchestration content not yet implemented
7. **Test naming inconsistency** - Module 3-4 tests incorrectly named `test_crear_tarea_clase7.py`
8. **CI/CD only tests one class** - Most implemented classes are not in the CI matrix

**Technical Gaps**:
9. **Async Python not taught** - FastAPI is used synchronously, async/await patterns missing
10. **No database integration** - Promised in Module 4 but not implemented (SQLAlchemy, Alembic)
11. **Error handling patterns missing** - No custom exceptions, HTTPException handlers

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

## Educational Specialist Agents

This repository includes a library of **educational agents** designed to teach, not just validate. All agents are located in `.claude/agents/educational/` and follow a consistent teaching methodology: identify anti-patterns, explain why they're problematic, show the correct solution, and teach the underlying principle.

### Available Educational Agents

**Backend & API Development:**

1. **Python Best Practices Coach** (`.claude/agents/educational/python-best-practices-coach.md`)
   - Teaches Pythonic code patterns (list comprehensions, f-strings, pathlib)
   - Type hints and PEP 8 compliance
   - Modern Python patterns (dataclasses, context managers)
   - Detects: manual loops, missing type hints, old string formatting

2. **FastAPI Design Coach** (`.claude/agents/educational/fastapi-design-coach.md`)
   - Professional REST API design patterns
   - Pydantic validation best practices
   - Async/await usage in FastAPI
   - Dependency injection patterns
   - Detects: non-RESTful endpoints, incomplete validation, blocking I/O in async

3. **API Design Reviewer** (`.claude/agents/educational/api-design-reviewer.md`)
   - RESTful principles and HTTP semantics
   - Status code correctness (200, 201, 404, 409, etc.)
   - Response format consistency
   - API versioning strategies
   - Pagination, filtering, rate limiting
   - OpenAPI/Swagger documentation

4. **Database ORM Specialist** (`.claude/agents/educational/database-orm-specialist.md`)
   - SQLAlchemy 2.0 patterns and relationships
   - N+1 query detection and resolution
   - Index optimization
   - Alembic migrations (safe, backward-compatible)
   - When to use ORM vs raw SQL

5. **Performance Optimizer** (`.claude/agents/educational/performance-optimizer.md`)
   - Profiling Python code (cProfile, line_profiler)
   - Async/await optimization
   - Caching strategies (Redis, in-memory, HTTP)
   - Database query optimization
   - React performance (useMemo, useCallback, React.memo)
   - Load testing and monitoring

**Infrastructure & DevOps:**

6. **Docker Infrastructure Guide** (`.claude/agents/educational/docker-infrastructure-guide.md`)
   - Dockerfile optimization (multi-stage builds, layer caching)
   - docker-compose best practices
   - Security hardening (non-root users, secrets management)
   - Image size optimization
   - Health checks and restart policies

**Frontend Integration:**

7. **React Integration Coach** (`.claude/agents/educational/react-integration-coach.md`)
   - React + FastAPI integration patterns
   - State management (Context, Zustand, React Query)
   - TypeScript with React (types, interfaces, generics)
   - Forms and validation (React Hook Form, Zod)
   - API client patterns and error handling

### How to Use Educational Agents

These agents are designed for learning contexts. Invoke them when:

- **Reviewing student code**: Provide educational feedback with explanations
- **Teaching best practices**: Show anti-patterns and better alternatives
- **Code review**: Explain *why* changes are needed, not just *what* to change

**Example usage scenarios:**

```markdown
# Reviewing a FastAPI endpoint with performance issues
→ Use: performance-optimizer + fastapi-design-coach

# Student implemented database queries in a loop
→ Use: database-orm-specialist (detects N+1, teaches eager loading)

# Dockerfile is 2GB and runs as root
→ Use: docker-infrastructure-guide (teaches multi-stage, security)

# React components re-render on every keystroke
→ Use: react-integration-coach (teaches useMemo, React.memo)

# API returns 200 OK for all responses (even errors)
→ Use: api-design-reviewer (teaches HTTP status codes)
```

### Agent Design Philosophy

All educational agents follow these principles:

✅ **Teach, don't just validate**: Explain *why* something is an anti-pattern
✅ **Show before/after**: Code examples with clear comparisons
✅ **Provide context**: When to use each pattern, trade-offs
✅ **Encourage best practices**: Link to PEPs, docs, industry standards
✅ **Practical examples**: Real-world scenarios from the master curriculum

**Tone**: Encouraging, educational, never condescending. "This works, but here's a more Pythonic way..." not "This is wrong."

### Integration with Linear Issues

These agents work in conjunction with the Linear issues workflow (see `docs/LINEAR_ISSUES_MASTER_PLAN.md`):

- AI integration issues (M1-1 through M1-4, M2-2 through M2-6, etc.) can leverage these agents
- Agents help implement 40% AI content in each class
- Use agents during code review before merging feature branches

See `docs/reviews/AGENTS_RECOMMENDED.md` for detailed agent specifications and usage examples.

## Module Completion Status

| Module | Status | Classes | Notes |
|--------|--------|---------|-------|
| Module 0 | ✅ **COMPLETED** | 6/6 | AI Development Foundations (Classes 0-6) + Final Project |
| Module 1 | ⚠️ Complete (no AI) | 4/4 | CLI, fundamentals, needs AI integration |
| Module 2 | ⚠️ Mostly Complete (no AI) | 5/6 | Class 1 only has notes, needs AI agents |
| Module 3 | ⚠️ Complete (no AI) | 7/7 | Security implemented, needs AI security review |
| Module 4 | 🔴 25% Complete | 2/8 | Missing DB, cloud deployment, LangChain, AI DevOps |
| Module 5 | ❌ Not Started | 0/6+ | Agent orchestration mastery completely absent |

**Overall**: ~70% complete (was 65%, +5% with Module 0 completion and agent library)

## Development Priorities

If you're continuing this project, prioritize:

**Phase 1 - AI Integration (CRITICAL)**:
1. ~~**Redesign Module 0**~~ - ✅ **COMPLETED**: 6 classes on AI development foundations created
2. ~~**Create Agent Library**~~ - ✅ **COMPLETED**: 7 educational agents created in `.claude/agents/educational/`
3. **Add AI sections to Modules 1-3** (1-2 weeks): 40% AI integration in each class
4. **Prompt Library** (2-3 days): 50+ effective prompts for common tasks (partially addressed in Module 0 Clase 5)

**Phase 2 - Implementation Gaps**:
5. **Fix critical inconsistencies** (1-2 days): Rename tests, update CI matrix, add `.md` extensions
6. **Complete Module 4** (3-4 weeks): Database integration, migrations, cloud deployment, AI DevOps
7. **Add async/await teaching** (1 week): Critical gap in Module 2
8. **Implement error handling** (1 week): Custom exceptions, HTTPException patterns

**Phase 3 - Completion**:
9. **Create Module 5** (3-4 weeks): Full-stack, agent orchestration mastery, final project
10. **Testing & Refinement** (1-2 weeks): Validate with students, iterate

See review documents for detailed action items and estimates.
