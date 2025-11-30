# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🚨 URGENTE: SIEMPRE trabajar en el entorno virtual

**ANTES DE HACER CUALQUIER COSA, activa el entorno virtual:**

```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

**NUNCA trabajes fuera del entorno virtual. NUNCA.**

**Razón**:
- Sin el venv, instalas dependencias globalmente (contaminas el sistema)
- Los tests pueden fallar por versiones incorrectas de librerías
- El pre-push hook puede no encontrar herramientas (ruff, pytest, etc.)
- Rompes la reproducibilidad del proyecto

**Cómo verificar que estás en el venv**:
```bash
# Deberías ver (.venv) al inicio del prompt
(.venv) E:\master-ia-manu>

# O verificar con:
python -c "import sys; print(sys.prefix)"
# Debería mostrar la ruta del .venv
```

**Si el pre-push hook dice "No estás en un entorno virtual", DETENTE y actívalo ANTES de continuar.**

---

## IMPORTANTE: Commits sin Co-Autoría de Claude

**NUNCA incluyas la línea de co-autoría de Claude en los commits:**

❌ **NO hacer esto:**
```
Co-Authored-By: Claude <noreply@anthropic.com>
```

✅ **Hacer esto:**
- Commits limpios sin referencias a Claude
- Solo el mensaje descriptivo del cambio
- Seguir Conventional Commits (feat:, fix:, docs:, etc.)

**Razón**: Este es un repositorio educativo profesional. Los commits deben reflejar únicamente el contenido del cambio, no la herramienta utilizada para crearlo.

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

## Git Workflow & Branch Protection

### Branch Protection Rules

**Protected branches**: `main` and `dev`

Both branches require Pull Requests - **direct pushes are blocked**. This ensures:
- All code passes pre-push hooks (linting, tests, coverage)
- Changes are reviewed via PR (even in solo projects for audit trail)
- CI/CD runs before merging

### Development Workflow

**1. Setup (one-time)**:
```bash
# Configure Git hooks
bash scripts/setup-hooks.sh

# Activate virtual environment
.venv/Scripts/activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

**2. Start new feature**:
```bash
# Create feature branch from dev
git checkout dev
git pull origin dev
git checkout -b feature/descripcion-corta
```

**3. Develop with validation**:
```bash
# Make changes
# ...

# Validate locally BEFORE committing
bash scripts/pre-pr-check.sh

# Commit (follow conventional commits)
git add .
git commit -m "feat: descripción del cambio"

# Push (pre-push hook validates automatically)
git push origin feature/descripcion-corta
```

**4. Create Pull Request**:
```bash
# Create PR to dev
gh pr create --base dev --title "feat: Título del PR" --body "Descripción"

# Or create PR interactively
gh pr create
```

**5. Merge PR** (after CI passes):

⚠️ **IMPORTANTE: Claude NUNCA debe hacer merge de Pull Requests**

**Razón**: El merge debe ser una decisión humana deliberada. Claude puede:
- ✅ Crear ramas
- ✅ Hacer commits
- ✅ Push de ramas
- ✅ Crear Pull Requests
- ❌ **NUNCA hacer merge** (ni `gh pr merge`, ni merge manual)

El usuario (humano) es quien decide cuándo mergear después de revisar:
- El código generado
- Los tests
- El PR completo
- La documentación

```bash
# EL USUARIO ejecuta esto (NO Claude):
gh pr merge --squash  # Squash commits
gh pr merge --merge   # Merge commit
gh pr merge --rebase  # Rebase

# Delete feature branch after merge
git branch -d feature/descripcion-corta
git push origin --delete feature/descripcion-corta
```

**6. Release to main** (from dev):
```bash
# Create PR from dev to main
git checkout dev
gh pr create --base main --title "release: v1.2.0" --body "Release notes"

# Merge after final validation
gh pr merge --merge
```

### Pre-push Hook

The `.githooks/pre-push` hook automatically runs:
- ✅ **Ruff linting**: Ensures code style compliance
- ✅ **Pytest with coverage**: Runs tests with 80% minimum coverage
- ✅ **Gitleaks**: Scans for secrets (if installed)

**Bypass hook** (NOT recommended):
```bash
git push --no-verify
```

### Pre-PR Validation Script

Before creating a PR, run the complete validation:
```bash
bash scripts/pre-pr-check.sh
```

This runs:
- Git status
- Ruff linting
- All tests with coverage
- Bandit security audit
- Gitleaks secret scanning
- Environment validation

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

**Module 4**: Infrastructure focus. Use Docker commands, check `infra/` directories for deployment configs. Includes Context Engineering (Clase 6.6) and Writing Tools for AI Agents (Clase 6.7).

**Module 5**: Full-Stack development with React + FastAPI. JWT auth, deployment strategies, and Agent Orchestration Mastery.

## AI Dev Academy Game

The repository includes an interactive game to practice concepts learned in the Master program.

### Overview

**AI Dev Academy - The Game** is a simulation where you progress from Junior Developer to CTO while learning the Master's content.

**Features**:
- 🎯 XP, levels, and skill progression
- 🏆 Achievements system
- 🤖 Hire specialized AI agents
- 🎨 Visual workspace that improves with progress
- 💾 Auto-save progress
- 🎮 Mini-games: Bug Hunt, Prompt Duel, Architecture Builder

### Quick Start

**Terminal Game** (Classic Python CLI):
```bash
cd ai-dev-academy-game
pip install -r requirements.txt
python main.py
```

**Bug Hunt Mini-Game** (Full-Stack React + FastAPI):

**Option 1: Manual Start (Development)**
```bash
# Terminal 1 - Backend
cd ai-dev-academy-game/backend
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd ai-dev-academy-game/frontend
npm install
npm run dev

# Open browser: http://localhost:3000
```

**Option 2: End-to-End Test**
```bash
python ai-dev-academy-game/test_bug_hunt_flow.py
```

### Game Structure

```
Level 1-5:   Junior Developer (Module 0)
Level 6-10:  Mid Developer (Module 1)
Level 11-15: Senior Developer (Module 2)
Level 16-20: Tech Lead (Module 3)
Level 21-25: Architect (Module 4)
Level 26-30: CTO (Module 5)
```

### Technologies

**Terminal Game**: Python 3.12, Rich (Terminal UI), JSON (save system)

**Bug Hunt Mini-Game**:
- Backend: FastAPI, SQLAlchemy, Pydantic
- Frontend: React 18, TypeScript, Vite
- 15 backend tests, 87.70% coverage

For detailed setup instructions, see `ai-dev-academy-game/SETUP.md`

## Important Notes

- Each class is self-contained - changes in one class don't affect others
- Always run tests from the class directory (not root) due to `conftest.py` path setup
- CI/CD is configured for the latest working class (currently Module 4, Class 2)
- Coverage threshold is 80% - tests will fail below this
- Follow TDD: tests are written before implementation in most classes

## Remaining Tasks & AI Integration

⚠️ **IMPORTANT**: This repository is approximately **95% complete**. The main remaining work is **AI integration** into Modules 1-3. Before making changes, review:

- **`docs/reviews/REVIEW_COMPLETENESS.md`**: Missing components, inconsistencies (mostly resolved)
- **`docs/reviews/REVIEW_PEDAGOGICAL.md`**: Conceptual gaps, learning progression issues
- **`docs/reviews/REVIEW_AI_INTEGRATION.md`**: **CRITICAL** - AI integration gaps in Modules 1-3
- **`docs/reviews/AGENTS_RECOMMENDED.md`**: Recommended specialist agents for educational support

### 🤖 The AI Integration Status

**Current State**: The program teaches excellent software engineering AND includes comprehensive AI foundations:

✅ **Completed AI Integration**:
- ✅ Module 0: Complete AI development foundations (6 classes)
- ✅ Module 4: Context Engineering & Writing Tools for AI Agents
- ✅ Module 5: Agent Orchestration Mastery
- ✅ Agent Library: 11 educational agents in `.claude/agents/educational/`

✅ **Complete AI Integration** (Modules 1-3):
- ✅ Module 1: AI exercises in all 4 classes (ejercicio_claseX_ai.md)
- ✅ Module 2: AI_WORKFLOW in all 6 classes (complete coverage)
- ✅ Module 3: AI_WORKFLOW in all 7 classes (complete security focus)

**Vision**: After this master, you should be **"a solo developer with an army of agents"** - able to build production applications alone using specialized AI agents.

**See `docs/reviews/REVIEW_AI_INTEGRATION.md`** for complete analysis and redesigned curriculum.

### Remaining Tasks

**AI Integration** (Priority 1):
1. ~~**Module 0 needs complete redesign**~~ - ✅ **COMPLETED**: Module 0 redesigned with 6 classes teaching AI development foundations
2. ~~**Modules 1-3 AI integration expansion**~~ - ✅ **COMPLETED**:
   - Module 1: 4/4 classes with AI exercises ✅
   - Module 2: 6/6 classes with AI_WORKFLOW files ✅
   - Module 3: 7/7 classes with AI_WORKFLOW ✅
3. ~~**No agent library**~~ - ✅ **COMPLETED**: 11 educational agents created in `.claude/agents/educational/`
4. ~~**No prompt engineering**~~ - ✅ **COMPLETED**: Module 0 Clase 5 covers prompt engineering

**Implementation** (Priority 2):
5. ~~**Module 4 incomplete**~~ - ✅ **COMPLETED**: All 8 classes implemented (Docker, DB, Cloud, AI Agents)
6. ~~**Module 5 is completely absent**~~ - ✅ **COMPLETED**: 5 classes implemented (Full-Stack + Agent Orchestration)
7. **Test naming inconsistency** - Module 3-4 tests incorrectly named `test_crear_tarea_clase7.py`
8. **CI/CD only tests one class** - Most implemented classes are not in the CI matrix

**Documentation** (Priority 3):
9. **Missing glossaries** - 3 glossaries missing, 4 without `.md` extension
10. ~~**Module-level READMEs**~~ - ✅ **COMPLETED**: READMEs created for Modules 0-3

### Working with Completed Features

**Database features**: ✅ Module 4 Classes 3-4 are complete (SQLAlchemy + Alembic)

**Full-Stack development**: ✅ Module 5 Classes 1-5 are complete (React + FastAPI integration)

**When fixing tests**: Module 3-4 test files still need renaming from `clase7` to correct class numbers

**When updating CI**: Add all implemented classes to `.github/workflows/ci.yml` and `ci_quality.yml` matrices

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

### Documentation Status

**Pending**:
- 3 glossaries missing: Module 3 Class 1, Module 3 Class 7, Module 4 Class 1
- 4 glossaries without `.md` extension

**Completed**:
- ✅ Module-level READMEs for all modules (Modules 0-3)
- ✅ Module 0 comprehensive documentation
- ✅ Module 4 & 5 class documentation
- ✅ AI Dev Academy Game documentation (README.md, SETUP.md, ARCHITECTURE.md, DEPLOY.md)
- ✅ Educational agent documentation (11 agents in `.claude/agents/educational/`)

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

**Architecture & Clean Code:**

6. **Clean Architecture Enforcer** (`.claude/agents/educational/clean-architecture-enforcer.md`)
   - SOLID principles enforcement
   - Dependency Inversion and layering
   - Repository pattern and abstraction
   - Service layer design
   - Detects: layer violations, concrete dependencies, business logic in controllers

**Testing & Quality:**

7. **Test Coverage Strategist** (`.claude/agents/educational/test-coverage-strategist.md`)
   - Test pyramid strategy (unit, integration, e2e)
   - Pytest fixtures and parametrization
   - Mocking and test doubles
   - Coverage analysis and gap identification
   - TDD workflow guidance

**Security:**

8. **Security Hardening Mentor** (`.claude/agents/educational/security-hardening-mentor.md`)
   - OWASP Top 10 mitigation
   - JWT authentication best practices
   - Input validation and sanitization
   - SQL injection prevention
   - Secret management and environment security

**Infrastructure & DevOps:**

9. **Docker Infrastructure Guide** (`.claude/agents/educational/docker-infrastructure-guide.md`)
   - Dockerfile optimization (multi-stage builds, layer caching)
   - docker-compose best practices
   - Security hardening (non-root users, secrets management)
   - Image size optimization
   - Health checks and restart policies

**Frontend Integration:**

10. **React Integration Coach** (`.claude/agents/educational/react-integration-coach.md`)
    - React + FastAPI integration patterns
    - State management (Context, Zustand, React Query)
    - TypeScript with React (types, interfaces, generics)
    - Forms and validation (React Hook Form, Zod)
    - API client patterns and error handling

**Git & Version Control:**

11. **Git Commit Helper** (`.claude/agents/educational/git-commit-helper.md`)
    - Conventional Commits format
    - Commit message best practices
    - Atomic commits strategy
    - Branch naming conventions
    - Git workflow guidance

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
| Module 1 | ✅ **COMPLETED** | 4/4 | CLI, fundamentals, all classes with AI exercises |
| Module 2 | ✅ **COMPLETED** | 6/6 | FastAPI & SOLID, all classes with AI_WORKFLOW |
| Module 3 | ✅ **COMPLETED** | 7/7 | Security + AI security review in all classes |
| Module 4 | ✅ **COMPLETED** | 8/8 | Docker, DB, SQLAlchemy, Alembic, Cloud, AI Agents, Tools |
| Module 5 | ✅ **COMPLETED** | 5/5 | Full-Stack React+FastAPI, Auth, Deploy, Agent Orchestration |

**Overall**: ~100% complete (was 97%, +3% with M1-M3 complete AI integration)

## Development Priorities

If you're continuing this project, prioritize:

**Phase 1 - AI Integration (COMPLETED)** ✅:
1. ~~**Redesign Module 0**~~ - ✅ **COMPLETED**: 6 classes on AI development foundations created
2. ~~**Create Agent Library**~~ - ✅ **COMPLETED**: 11 educational agents created in `.claude/agents/educational/`
3. ~~**Complete AI sections in Modules 1-3**~~ - ✅ **COMPLETED**: All classes have AI integration
   - Module 1: 4/4 classes with AI exercises ✅
   - Module 2: 6/6 classes with AI_WORKFLOW ✅
   - Module 3: 7/7 classes with AI_WORKFLOW ✅
4. **Prompt Library expansion** (2-3 days): 50+ effective prompts for common tasks (partially addressed in Module 0 Clase 5)

**Phase 2 - Polish & Documentation (IN PROGRESS)**:
5. **Fix critical inconsistencies** (partial):
   - ~~Rename tests from `clase7` to correct class numbers~~ ✅ **COMPLETED**
   - ~~Update CI matrix to test all implemented classes~~ ✅ **COMPLETED**
   - Add `.md` extensions to 4 glossaries (pending)
6. **Complete documentation** (1 day):
   - Add 3 missing glossaries (Module 3 Class 1, Module 3 Class 7, Module 4 Class 1)
   - ~~Create Module-level READMEs for Modules 1-3~~ ✅ **COMPLETED**
   - Update CI/CD workflow configurations

**Phase 3 - Testing & Refinement (ONGOING)**:
7. ~~**Complete Module 4**~~ - ✅ **COMPLETED**: All 8 classes implemented
8. ~~**Create Module 5**~~ - ✅ **COMPLETED**: 5 classes implemented (Full-stack + Agent Orchestration)
9. **Validate with students** (ongoing): Iterate based on feedback
10. **Expand AI Dev Academy Game** (optional): Additional mini-games, more achievements

**Completed Milestones**:
- ✅ Module 0: AI Development Foundations (6 classes)
- ✅ Module 1-3: Complete AI Integration (17/17 classes with AI content) 🎉
- ✅ Module 4: Complete infrastructure stack (Docker, DB, SQLAlchemy, Alembic, Cloud, AI Agents)
- ✅ Module 5: Full-Stack + Agent Orchestration (React + FastAPI)
- ✅ Educational Agent Library (11 specialized teaching agents)
- ✅ AI Dev Academy Game (Terminal + Bug Hunt mini-game)
- ✅ Module-level READMEs for all modules (0-3)
- ✅ Test naming fixes (16 files renamed)
- ✅ CI/CD matrix updated (5 new classes added)

See review documents for detailed action items and estimates.

---

## NeuralFlow - Multi-Course Educational SaaS Platform

**⚠️ IMPORTANT**: The AI Dev Academy game is being evolved into **NeuralFlow** (neuralflow.es), a multi-course educational SaaS platform. This is an active development project separate from the master's degree curriculum.

**🚨 CRITICAL WORKFLOW RULE:**
Before working on ANY NeuralFlow feature, you MUST:
1. Check Linear issues status (use `neuralflow-linear-manager` agent)
2. Verify dependency order (see execution phases below)
3. Ensure prerequisite issues are completed (status: "Done")
4. Never start dependent issues until prerequisites are merged
5. Follow the recommended execution order (5 phases)

**Execution Phases:**
```
Phase 1 (Core Infrastructure): NFLOW-1 → NFLOW-2 → NFLOW-3
Phase 2 (Testing & Deploy):    NFLOW-5 → NFLOW-8
Phase 3 (Content):              NFLOW-4 (can be parallel)
Phase 4 (Enhancements):         NFLOW-6 → NFLOW-7
Phase 5 (Documentation):        NFLOW-9
```

### Project Overview

**NeuralFlow** is a platform that hosts multiple educational courses:
- **Master IA** (existing: AI-assisted development)
- **Data Engineering** (planned: data pipelines, ETL, analytics)
- Future courses as the platform grows

**Tech Stack:**
- **Backend:** FastAPI + SQLAlchemy + SQLite (migrating to PostgreSQL)
- **Frontend:** React 18 + TypeScript + Vite + Zustand
- **Deployment:** Easypanel (Docker Compose + Traefik reverse proxy)
- **Auth:** JWT with bcrypt password hashing
- **Database:** SQLite (current), PostgreSQL (planned migration)

### Linear Project Management

All NeuralFlow development is tracked in Linear:
- **Team:** cursos-neuralflow
- **Total Issues:** 9 (covering full multi-course migration)

**Core Platform Issues (3):**
  - **NFLOW-1:** Backend multi-curso con adapter pattern (High priority, 4-6h)
  - **NFLOW-2:** Frontend catálogo de cursos (High priority, 3-5h)
  - **NFLOW-3:** Database migration - añadir course_id (Medium priority, 2-3h)

**Content & Testing (2):**
  - **NFLOW-4:** Crear contenido curricular para Data Engineering (High priority, 40-60h)
  - **NFLOW-5:** Implementar tests E2E para flujos multi-curso (High priority, 8-12h)

**Features & Analytics (2):**
  - **NFLOW-6:** Analytics y tracking multi-curso (Medium priority, 12-16h)
  - **NFLOW-7:** Sistema de achievements específicos por curso (Medium priority, 10-14h)

**Infrastructure & Documentation (2):**
  - **NFLOW-8:** Configuración de deployment y variables de entorno multi-curso (High priority, 6-8h)
  - **NFLOW-9:** Documentación completa multi-curso (Medium priority, 8-12h)

**Total Estimated Time:** 93-131 hours (~112 hours average, ~14 working days at 8h/day)

### Development Workflow for NeuralFlow

**Important Constraints:**
- ✅ Must work with Easypanel (Traefik already configured, no Nginx needed)
- ✅ Use `docker-compose.production.yml` with `expose` (not `ports`)
- ✅ All changes must be backward compatible (existing Master IA must work)
- ✅ Default `course_id` is "master-ia" for all endpoints
- ✅ Incremental migration (no big bang rewrites)
- ✅ Cannot rename `ai-dev-academy-game/` directory (breaks deployment paths)

**Architecture Principles:**
1. **Conservative over Clever** - Incremental changes, proven patterns
2. **Multi-Course from Day 1** - Every new feature supports multiple courses
3. **Fail-Safe Architecture** - Every migration has a rollback plan
4. **Developer Experience** - Clear separation of concerns (core, courses, routes)

### NeuralFlow Specialized Agents

The repository includes **12 specialized agents** for NeuralFlow development located in `.claude/agents/`:

**Development Agents (5):**
1. **neuralflow-architect.md** - Solution architect for multi-course platform decisions
2. **neuralflow-implementer.md** - Implements features following established patterns
3. **tdd-neuralflow.md** - Test-Driven Development specialist (RED-GREEN-REFACTOR)
4. **neuralflow-security-auditor.md** - Security auditing (OWASP, JWT, CORS, secrets)
5. **neuralflow-qa.md** - Quality Assurance (UAT, regression, cross-browser testing)

**Frontend & UX Agents (3):**
6. **neuralflow-frontend-expert.md** - React 18 + TypeScript + Zustand expert
7. **neuralflow-ui-expert.md** - UI design, design system, component library
8. **neuralflow-accessibility.md** - Accessibility specialist (WCAG 2.1 AA compliance)

**Product & Marketing Agents (3):**
9. **neuralflow-infoproduct-expert.md** - Educational product design, course structure
10. **neuralflow-marketing.md** - Marketing strategy, funnels, acquisition campaigns
11. **neuralflow-copywriting.md** - Conversion copywriting for developers

**Management Agent (1):**
12. **neuralflow-linear-manager.md** - Linear project management, issue tracking

### When to Use NeuralFlow Agents

**Use these agents when:**
- Working on multi-course platform features
- Implementing NFLOW-1, NFLOW-2, or NFLOW-3 issues
- Making architectural decisions for NeuralFlow
- Adding new courses or course-related features
- Designing/implementing frontend components
- Writing marketing materials or course content
- Managing Linear issues and project workflow

**Do NOT use for:**
- Master's degree curriculum development (use educational agents instead)
- Individual class implementations in Modules 1-5
- General Python/FastAPI questions (use educational agents)

### NeuralFlow Directory Structure

```
ai-dev-academy-game/
├── backend/
│   ├── app/
│   │   ├── core/              # Shared infrastructure (auth, db, config)
│   │   │   ├── auth.py
│   │   │   ├── database.py
│   │   │   ├── config.py
│   │   │   └── course_manager.py  # NFLOW-1: Course registration
│   │   ├── courses/           # Course-specific implementations
│   │   │   ├── master_ia.py   # NFLOW-1: Master IA adapter
│   │   │   └── data_engineering.py  # NFLOW-1: Data Eng stub
│   │   ├── models/            # SQLAlchemy models
│   │   ├── routes/            # FastAPI endpoints
│   │   │   ├── auth.py
│   │   │   ├── catalog.py     # NFLOW-1: GET /api/courses
│   │   │   └── ...
│   │   ├── services/          # Business logic
│   │   └── main.py
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── catalog/       # NFLOW-2: Course catalog
│   │   │   │   ├── CourseCatalog.tsx
│   │   │   │   └── CourseCard.tsx
│   │   │   ├── auth/
│   │   │   ├── game/
│   │   │   └── common/
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   ├── authApi.ts
│   │   │   ├── gameApi.ts
│   │   │   └── catalogApi.ts  # NFLOW-2: Catalog API calls
│   │   ├── stores/
│   │   │   ├── authStore.ts
│   │   │   ├── gameStore.ts
│   │   │   └── catalogStore.ts  # NFLOW-2: Catalog state
│   │   └── types/
│   │       └── course.ts      # NFLOW-2: Course TypeScript types
│   └── Dockerfile
└── docker-compose.production.yml  # Easypanel deployment config
```

### All Migration Issues (Linear)

**Phase 1: Core Infrastructure**

**NFLOW-1: Backend multi-curso con adapter pattern** (High, 4-6h)
- Create `CourseManager` to register and retrieve courses
- Add `course_id` parameter to all endpoints (default: "master-ia")
- Implement adapter pattern: `MasterIACourse`, `DataEngineeringCourse`
- Create `GET /api/courses` endpoint
- **Status:** Backlog

**NFLOW-2: Frontend catálogo de cursos** (High, 3-5h)
- Create `CourseCatalog` React component
- Implement `CourseCard` with course status badges
- Add routing: `/catalog` and `/game/:courseId`
- Backward compatibility: `/game` redirects to `/game/master-ia`
- **Depends on:** NFLOW-1
- **Status:** Backlog

**NFLOW-3: Database migration - añadir course_id** (Medium, 2-3h)
- Alembic migration to add `course_id` to `Progress` and `Achievement` tables
- Default value: "master-ia" (backward compatible)
- Backfill existing records
- **Depends on:** NFLOW-2
- **Status:** Backlog (delayed until Data Engineering ready)

**Phase 2: Testing & Deployment**

**NFLOW-5: Implementar tests E2E para flujos multi-curso** (High, 8-12h)
- Playwright/Cypress setup for end-to-end testing
- Test scenarios: new user flow, course switching, progress isolation
- Test backward compatibility (default course behavior)
- CI/CD integration for E2E tests
- **Depends on:** NFLOW-1, NFLOW-2
- **Status:** Backlog

**NFLOW-8: Configuración de deployment y variables de entorno multi-curso** (High, 6-8h)
- Update `docker-compose.production.yml` with course environment variables
- Health checks for multi-course endpoints
- Deploy scripts (Easypanel configuration)
- Backup and rollback procedures
- **Depends on:** NFLOW-3
- **Status:** Backlog

**Phase 3: Content Creation**

**NFLOW-4: Crear contenido curricular para Data Engineering** (High, 40-60h)
- 5 modules: ETL Foundations, Databases at Scale, Airflow, Data Warehousing, Final Project
- 20-25 classes with exercises
- Data Engineering final project (end-to-end pipeline)
- Integration with existing content system
- **Status:** Backlog (can be done in parallel with Phase 1-2)

**Phase 4: Enhancement Features**

**NFLOW-6: Analytics y tracking multi-curso** (Medium, 12-16h)
- Google Analytics 4 integration with course_id tracking
- Per-course metrics dashboard (admin view)
- Event tracking: course_start, class_complete, achievement_unlock
- Privacy-compliant analytics (GDPR)
- **Depends on:** NFLOW-3
- **Status:** Backlog

**NFLOW-7: Sistema de achievements específicos por curso** (Medium, 10-14h)
- 15 achievements per course (Master IA, Data Engineering)
- 5 cross-course achievements
- Achievement badges and social sharing
- Leaderboard by course
- **Depends on:** NFLOW-6
- **Status:** Backlog

**Phase 5: Documentation**

**NFLOW-9: Documentación completa multi-curso** (Medium, 8-12h)
- Update README.md with multi-course architecture
- ARCHITECTURE.md explaining adapter pattern and course system
- DEPLOY.md with Easypanel multi-course deployment guide
- API documentation (Swagger/OpenAPI) with course_id parameter examples
- **Status:** Backlog

### NeuralFlow Development Commands

**Backend (from ai-dev-academy-game/backend/):**
```bash
# Start backend development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run backend tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing
```

**Frontend (from ai-dev-academy-game/frontend/):**
```bash
# Install dependencies
npm install

# Start frontend development server
npm run dev

# Build for production
npm run build

# Run frontend tests
npm run test
```

**Docker (from ai-dev-academy-game/):**
```bash
# Build and run with docker-compose
docker-compose up --build

# Production build (Easypanel uses this)
docker-compose -f docker-compose.production.yml up -d
```

### Working with NeuralFlow

**⚠️ CRITICAL: Check Issue Dependencies Before Starting**

**Recommended execution order (5 phases):**

```
Phase 1 (Core Infrastructure):
NFLOW-1 → NFLOW-2 → NFLOW-3

Phase 2 (Testing & Deploy):
NFLOW-5 → NFLOW-8

Phase 3 (Content - Parallel):
NFLOW-4

Phase 4 (Enhancements):
NFLOW-6 → NFLOW-7

Phase 5 (Documentation):
NFLOW-9
```

**Why this order matters:**
- **Phase 1 is sequential**: NFLOW-2 needs NFLOW-1 (backend endpoints), NFLOW-3 needs NFLOW-2 (UI to test with)
- **Phase 2 validates Phase 1**: E2E tests ensure multi-course works before deployment config
- **Phase 3 can be parallel**: Content creation doesn't block infrastructure work
- **Phase 4 builds on Phase 1**: Analytics and achievements need the multi-course foundation
- **Phase 5 is last**: Documentation captures the final implemented system
- Breaking this order will cause merge conflicts, failed tests, and rework

**Before starting ANY work:**
1. ✅ **Check Linear** - Use **neuralflow-linear-manager** agent to:
   - List current issues: `mcp__linear__list_issues` with team "cursos-neuralflow"
   - Check issue status (Todo/In Progress/Done)
   - Verify which issues are already completed
2. ✅ **Verify dependencies** - Ensure prerequisite issues are DONE
   - NFLOW-1 must be Done before starting NFLOW-2
   - NFLOW-2 must be Done before starting NFLOW-3
3. ✅ **Consult architect** - Use **neuralflow-architect** agent for design decisions
4. ✅ **Create feature branch** - Use format: `feature/nflow-X-description`
5. ✅ **Review constraints** - Backward compatibility, Easypanel, no directory renames

**Example 1: Starting work on NFLOW-2 (Frontend catalog)**
```bash
# WRONG: Start without checking
git checkout -b feature/nflow-2-catalog  # ❌ May not be ready

# RIGHT: Check Linear first
# Use neuralflow-linear-manager to verify:
# - NFLOW-1 status is "Done" ✅ (prerequisite completed)
# - NFLOW-2 status is "Todo" or "Backlog" ✅
# - No blockers reported ✅
# THEN create branch
git checkout -b feature/nflow-2-catalog  # ✅ Safe to proceed
```

**Example 2: Starting work on NFLOW-6 (Analytics)**
```bash
# WRONG: Start too early
git checkout -b feature/nflow-6-analytics  # ❌ NFLOW-3 not done yet

# RIGHT: Verify entire dependency chain
# Use neuralflow-linear-manager to verify:
# - NFLOW-1 status is "Done" ✅ (Phase 1 complete)
# - NFLOW-2 status is "Done" ✅ (Phase 1 complete)
# - NFLOW-3 status is "Done" ✅ (NFLOW-6 depends on this)
# - NFLOW-6 status is "Todo" or "Backlog" ✅
# THEN create branch
git checkout -b feature/nflow-6-analytics  # ✅ Safe to proceed
```

**Example 3: Working on NFLOW-4 (Content) in parallel**
```bash
# NFLOW-4 can be done in parallel with Phase 1-2
# Use neuralflow-linear-manager to verify:
# - NFLOW-4 status is "Todo" or "Backlog" ✅
# - No dependencies blocking ✅ (content creation is independent)
git checkout -b feature/nflow-4-data-eng-content  # ✅ Can start anytime
```

**During implementation:**
1. Use **neuralflow-implementer** for code generation
2. Use **tdd-neuralflow** for writing tests first
3. Use **neuralflow-security-auditor** for auth/data changes
4. Use **neuralflow-qa** before creating PR

**After implementation:**
1. Create PR with Linear issue reference (e.g., "Closes NFLOW-1")
2. Run smoke tests
3. **DO NOT MERGE** - User (human) reviews and merges

### Recommended Agents by Issue

**NFLOW-1 (Backend multi-curso):**
- neuralflow-architect (design CourseManager pattern)
- neuralflow-implementer (implement adapters)
- tdd-neuralflow (write tests first)
- neuralflow-security-auditor (validate endpoint security)

**NFLOW-2 (Frontend catalog):**
- neuralflow-frontend-expert (React components, Zustand state)
- neuralflow-ui-expert (CourseCard design, responsive layout)
- neuralflow-accessibility (WCAG compliance)
- neuralflow-implementer (implementation)

**NFLOW-3 (Database migration):**
- neuralflow-architect (migration strategy)
- neuralflow-implementer (Alembic migration)
- neuralflow-security-auditor (data integrity checks)
- tdd-neuralflow (test migration rollback)

**NFLOW-4 (Data Engineering content):**
- neuralflow-infoproduct-expert (course structure, exercises)
- neuralflow-copywriting (course descriptions, marketing)
- neuralflow-implementer (content integration)

**NFLOW-5 (E2E tests):**
- neuralflow-qa (test strategy, Playwright/Cypress setup)
- tdd-neuralflow (test scenarios)
- neuralflow-implementer (test implementation)

**NFLOW-6 (Analytics):**
- neuralflow-architect (analytics architecture)
- neuralflow-implementer (Google Analytics integration)
- neuralflow-security-auditor (privacy compliance, GDPR)

**NFLOW-7 (Achievements):**
- neuralflow-ui-expert (badge design, social sharing UI)
- neuralflow-frontend-expert (React achievement components)
- neuralflow-implementer (achievement logic)

**NFLOW-8 (Deployment config):**
- neuralflow-architect (deployment strategy)
- neuralflow-implementer (docker-compose updates)
- neuralflow-security-auditor (environment secrets validation)

**NFLOW-9 (Documentation):**
- neuralflow-architect (architecture diagrams)
- neuralflow-copywriting (README, guides)
- neuralflow-infoproduct-expert (API documentation)

### NeuralFlow vs. Master's Curriculum

**NeuralFlow (ai-dev-academy-game/):**
- Production SaaS platform
- Multi-course support
- Real users, real data
- Deployed to neuralflow.es
- Use NeuralFlow agents

**Master's Curriculum (Modulo 0-5/):**
- Educational content
- Progressive learning modules
- Self-contained class examples
- Use educational agents

**DO NOT confuse these two projects.** They have different purposes, different agents, and different workflows.

---
