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
- ✅ Agent Library: 7 educational agents in `.claude/agents/educational/`

⚠️ **Pending AI Integration** (Modules 1-3):
- ❌ Module 1: Needs 40% AI integration in each class
- ❌ Module 2: Needs AI agent workflow sections
- ❌ Module 3: Needs AI security review integration

**Vision**: After this master, you should be **"a solo developer with an army of agents"** - able to build production applications alone using specialized AI agents.

**See `docs/reviews/REVIEW_AI_INTEGRATION.md`** for complete analysis and redesigned curriculum.

### Remaining Tasks

**AI Integration** (Priority 1):
1. ~~**Module 0 needs complete redesign**~~ - ✅ **COMPLETED**: Module 0 redesigned with 6 classes teaching AI development foundations
2. **Modules 1-3 need AI integration** - Each class needs 40% AI content (workflows, agent usage, prompts)
3. ~~**No agent library**~~ - ✅ **COMPLETED**: 7 educational agents created in `.claude/agents/educational/`
4. ~~**No prompt engineering**~~ - ✅ **COMPLETED**: Module 0 Clase 5 covers prompt engineering

**Implementation** (Priority 2):
5. ~~**Module 4 incomplete**~~ - ✅ **COMPLETED**: All 8 classes implemented (Docker, DB, Cloud, AI Agents)
6. ~~**Module 5 is completely absent**~~ - ✅ **COMPLETED**: 5 classes implemented (Full-Stack + Agent Orchestration)
7. **Test naming inconsistency** - Module 3-4 tests incorrectly named `test_crear_tarea_clase7.py`
8. **CI/CD only tests one class** - Most implemented classes are not in the CI matrix

**Documentation** (Priority 3):
9. **Missing glossaries** - 3 glossaries missing, 4 without `.md` extension
10. **Module-level READMEs** - Absent for Modules 1-3

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
- Module-level READMEs absent for Modules 1-3

**Completed**:
- ✅ Module 0 comprehensive documentation
- ✅ Module 4 & 5 class documentation
- ✅ AI Dev Academy Game documentation (README.md, SETUP.md, ARCHITECTURE.md, DEPLOY.md)
- ✅ Educational agent documentation (7 agents in `.claude/agents/educational/`)

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
| Module 2 | ⚠️ Complete (no AI) | 6/6 | FastAPI & SOLID principles, needs AI agents |
| Module 3 | ⚠️ Complete (no AI) | 7/7 | Security implemented, needs AI security review |
| Module 4 | ✅ **COMPLETED** | 8/8 | Docker, DB, SQLAlchemy, Alembic, Cloud, AI Agents, Tools |
| Module 5 | ✅ **COMPLETED** | 5/5 | Full-Stack React+FastAPI, Auth, Deploy, Agent Orchestration |

**Overall**: ~95% complete (was 70%, +25% with Module 4 & 5 completion)

## Development Priorities

If you're continuing this project, prioritize:

**Phase 1 - AI Integration (HIGHEST PRIORITY)**:
1. ~~**Redesign Module 0**~~ - ✅ **COMPLETED**: 6 classes on AI development foundations created
2. ~~**Create Agent Library**~~ - ✅ **COMPLETED**: 7 educational agents created in `.claude/agents/educational/`
3. **Add AI sections to Modules 1-3** (1-2 weeks): 40% AI integration in each class
   - Module 1: Add AI workflow sections to each class
   - Module 2: Integrate educational agents in code reviews
   - Module 3: Add AI security review workflows
4. **Prompt Library expansion** (2-3 days): 50+ effective prompts for common tasks (partially addressed in Module 0 Clase 5)

**Phase 2 - Polish & Documentation (MEDIUM PRIORITY)**:
5. **Fix critical inconsistencies** (1-2 days):
   - Rename tests from `clase7` to correct class numbers
   - Update CI matrix to test all implemented classes
   - Add `.md` extensions to 4 glossaries
6. **Complete documentation** (1-2 days):
   - Add 3 missing glossaries (Module 3 Class 1, Module 3 Class 7, Module 4 Class 1)
   - Create Module-level READMEs for Modules 1-3
   - Update CI/CD workflow configurations

**Phase 3 - Testing & Refinement (ONGOING)**:
7. ~~**Complete Module 4**~~ - ✅ **COMPLETED**: All 8 classes implemented
8. ~~**Create Module 5**~~ - ✅ **COMPLETED**: 5 classes implemented (Full-stack + Agent Orchestration)
9. **Validate with students** (ongoing): Iterate based on feedback
10. **Expand AI Dev Academy Game** (optional): Additional mini-games, more achievements

**Completed Milestones**:
- ✅ Module 0: AI Development Foundations (6 classes)
- ✅ Module 4: Complete infrastructure stack (Docker, DB, SQLAlchemy, Alembic, Cloud, AI Agents)
- ✅ Module 5: Full-Stack + Agent Orchestration (React + FastAPI)
- ✅ Educational Agent Library (7 specialized teaching agents)
- ✅ AI Dev Academy Game (Terminal + Bug Hunt mini-game)

See review documents for detailed action items and estimates.
