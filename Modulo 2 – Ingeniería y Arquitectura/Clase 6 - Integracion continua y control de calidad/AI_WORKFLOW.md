# Workflow de Agentes Educacionales - Clase 6 (CI/CD y Control de Calidad)

## 🎯 Objetivo

Aprender a usar agentes de IA para **configurar pipelines de CI/CD profesionales** y **automatizar controles de calidad**. Este workflow te enseña a crear GitHub Actions workflows que validen tu código automáticamente.

---

## 📊 Agentes Disponibles para Esta Clase

### 1. Test Coverage Strategist

**Ubicación**: `.claude/agents/educational/test-coverage-strategist.md`

**Cuándo usar**:
- Al analizar coverage reports (pytest --cov)
- Cuando coverage está < 80%
- Para identificar casos edge no testeados
- Al diseñar estrategia de testing

**Qué valida**:
- ✅ Coverage de líneas (line coverage)
- ✅ Coverage de ramas (branch coverage)
- ✅ Gaps críticos sin tests
- ✅ Tests redundantes
- ✅ Estrategia de pirámide de tests (unit > integration > e2e)

**Ejemplo de uso**:

```bash
# Ejecutar coverage
pytest --cov=api --cov-report=term-missing --cov-report=html

# Output
api/api.py          85%   12-15, 45-48
api/servicio.py     75%   23, 67-72
```

**Prompt para el agente**:

```
Tengo este reporte de coverage:

[PEGA EL REPORTE]

Código fuente:
[PEGA EL CÓDIGO DE LAS LÍNEAS SIN CUBRIR]

Ayúdame a:
1. Identificar qué casos edge NO están cubiertos
2. Priorizar qué tests escribir primero (más críticos)
3. Diseñar tests mínimos para llegar a 80%+ coverage
4. Detectar si hay código muerto (unreachable)

Dame tests específicos para las líneas sin cubrir.
```

---

### 2. Python Best Practices Coach

**Ubicación**: `.claude/agents/educational/python-best-practices-coach.md`

**Cuándo usar**:
- Antes de hacer commit
- Al configurar linters (ruff, flake8)
- Después de recibir warnings del linter

**Qué valida en contexto CI/CD**:
- ✅ PEP 8 compliance
- ✅ Type hints completos
- ✅ Imports organizados
- ✅ Docstrings en funciones públicas
- ✅ No variables no usadas

**Ejemplo con Ruff**:

```bash
# Ejecutar Ruff
ruff check api/

# Output
api/api.py:15:1: F401 [*] `json` imported but unused
api/servicio.py:23:5: E501 Line too long (95 > 88 characters)
```

**Prompt para corregir**:

```
Mi linter Ruff detectó estos problemas:

[PEGA LOS ERRORES]

Para cada problema:
1. Explica qué significa el código de error
2. Por qué es un problema (no solo "lo dice el linter")
3. Cómo arreglarlo correctamente
4. Si hay excepciones válidas para ignorarlo

Código actual:
[PEGA EL CÓDIGO PROBLEMÁTICO]
```

---

### 3. Security Hardening Mentor

**Ubicación**: `.claude/agents/educational/security-hardening-mentor.md`

**Cuándo usar**:
- Al configurar Bandit (security linter)
- Cuando Bandit detecta vulnerabilidades
- Antes de deploy a producción

**Qué valida**:
- ✅ Secrets hardcodeados
- ✅ SQL injection risks
- ✅ Eval/exec usage
- ✅ Weak cryptography
- ✅ Insecure deserialization

**Ejemplo con Bandit**:

```bash
# Ejecutar Bandit
bandit -r api/ -ll

# Output
[B105] hardcoded_password_string
api/api.py:12: JWT_SECRET = "mysecret123"
```

**Prompt para el agente**:

```
Bandit detectó este problema de seguridad:

Issue: [B105] hardcoded_password_string
File: api/api.py:12
Code: JWT_SECRET = "mysecret123"

Ayúdame a:
1. Entender el riesgo real (no solo teórico)
2. Implementar la solución correcta (variables de entorno)
3. Validar que no hay otros secrets hardcodeados
4. Configurar verificación en CI

Muestra código corregido y configuración de CI.
```

---

## 🚀 Workflow Completo: CI/CD Setup

### Fase 1: Tests Locales con Coverage

**Paso 1: Configurar pytest con coverage**

```bash
# Instalar dependencias
pip install pytest pytest-cov

# Ejecutar tests con coverage
pytest --cov=api --cov-report=term-missing --cov-fail-under=80
```

**Paso 2: Analizar gaps de coverage**

```
Tengo 75% de coverage. Necesito llegar a 80%.

Coverage report:
api/api.py          85%   Lines missing: 12-15, 45-48
api/servicio.py     70%   Lines missing: 23, 67-72
api/repositorio.py  90%   Lines missing: 34

Código de las líneas sin cubrir:
[PEGA EL CÓDIGO]

Usando el Test Coverage Strategist:
1. ¿Qué casos edge faltan?
2. ¿Qué tests mínimos necesito?
3. Dame los tests específicos para llegar a 80%

Restricción: Solo agregar tests realmente útiles, no tests "relleno".
```

**Paso 3: Implementar tests faltantes**

Usa el agente para generar tests específicos para las líneas críticas.

---

### Fase 2: Linting y Formateo

**Paso 4: Configurar Ruff**

```bash
# Ejecutar Ruff
ruff check api/

# Si hay errores, consultarlos con Python Best Practices Coach
```

**Prompt para configuración**:

```
Necesito configurar Ruff para mi proyecto FastAPI.

Estructura:
api/
├── api.py
├── servicio_tareas.py
├── repositorio_base.py
└── repositorio_memoria.py

Requisitos:
1. Archivo pyproject.toml con configuración Ruff
2. Reglas: PEP 8, type hints, imports organizados
3. Excluir: tests/, __pycache__
4. Line length: 100 caracteres
5. Python version: 3.12

Muestra el pyproject.toml completo.
```

---

### Fase 3: Security Scanning

**Paso 5: Ejecutar Bandit**

```bash
# Instalar Bandit
pip install bandit

# Escanear código
bandit -r api/ -ll  # -ll = solo high/medium severity
```

**Si hay issues, usa Security Hardening Mentor**:

```
Bandit encontró estos problemas:

[PEGA LOS RESULTADOS]

Para cada problema:
1. Evalúa si es un falso positivo o riesgo real
2. Dame la solución correcta (con código)
3. Explica cómo prevenirlo en el futuro

Contexto del proyecto:
- FastAPI con JWT auth
- Repositorio en memoria (no DB real aún)
- Variables de entorno en .env
```

---

### Fase 4: GitHub Actions Workflow

**Paso 6: Crear archivo de CI**

**Prompt para generar workflow**:

```
Necesito un GitHub Actions workflow para mi API FastAPI.

Requisitos del pipeline:
1. Trigger: push y PR a branches main y dev
2. Python version: 3.12
3. Jobs:
   a) Test: pytest con --cov-fail-under=80
   b) Lint: ruff check api/
   c) Security: bandit -r api/ -ll
   d) Type Check: mypy api/ (opcional)

4. Fail fast: false (ejecutar todos aunque falle uno)
5. Cache de pip para acelerar builds

Estructura de archivos:
.github/
└── workflows/
    └── ci.yml

Muestra el archivo ci.yml completo con comentarios explicativos.
```

**Ejemplo de workflow generado**:

```yaml
name: CI - Tests y Quality Checks

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov ruff bandit

      - name: Run tests with coverage
        run: |
          pytest --cov=api --cov-report=term-missing --cov-fail-under=80

      - name: Lint with Ruff
        run: |
          ruff check api/

      - name: Security scan with Bandit
        run: |
          bandit -r api/ -ll
```

---

### Fase 5: Pre-commit Hooks (Validación Local)

**Paso 7: Configurar pre-commit**

```bash
# Instalar pre-commit
pip install pre-commit

# Crear .pre-commit-config.yaml
```

**Prompt para configuración**:

```
Necesito configurar pre-commit hooks para validar localmente antes de push.

Hooks necesarios:
1. trailing-whitespace: eliminar espacios al final
2. end-of-file-fixer: nueva línea al final de archivos
3. check-yaml: validar archivos YAML
4. ruff: linting automático
5. pytest: ejecutar tests rápidos (no todos)

Python version: 3.12

Muestra .pre-commit-config.yaml completo y comandos para activar.
```

---

## 🧪 Testing del Pipeline CI/CD

**Paso 8: Probar pipeline localmente**

```bash
# Simular GitHub Actions localmente con act
# (requiere Docker)
act -j test

# O simplemente ejecutar los comandos del workflow:
pytest --cov=api --cov-fail-under=80 && \
ruff check api/ && \
bandit -r api/ -ll
```

**Paso 9: Push y verificar en GitHub**

```bash
# Crear rama de feature
git checkout -b feature/ci-setup

# Commit
git add .
git commit -m "feat: configurar CI/CD pipeline

- pytest con 80% coverage mínimo
- ruff linting
- bandit security scan
- pre-commit hooks"

# Push
git push origin feature/ci-setup

# Crear PR en GitHub y verificar que el pipeline pasa
```

---

## 📊 Entregables de Esta Clase

Al finalizar debes tener:

1. ✅ `.github/workflows/ci.yml` - Pipeline de CI completo
2. ✅ `.pre-commit-config.yaml` - Hooks de pre-commit
3. ✅ `pyproject.toml` - Configuración de Ruff
4. ✅ Coverage >80% en todos los módulos
5. ✅ Cero warnings de Ruff
6. ✅ Cero issues de Bandit (high/medium)
7. ✅ `CI_CD_SETUP.md` - Documentación del pipeline

---

## 🎯 Criterios de Éxito

Has completado esta clase exitosamente si:

1. ✅ Tu pipeline de CI ejecuta en GitHub Actions
2. ✅ Coverage es ≥ 80% y falla si baja
3. ✅ Ruff detecta problemas de estilo automáticamente
4. ✅ Bandit escanea seguridad en cada push
5. ✅ Pre-commit hooks previenen commits con errores
6. ✅ Entiendes cada paso del pipeline (no es magia)
7. ✅ Aplicaste los 3 agentes educacionales

---

## 💡 Mejores Prácticas Aprendidas

**CI/CD**:
- 🎯 Fail fast = false para ver todos los problemas
- 🎯 Cache de dependencias para builds rápidos
- 🎯 Ejecutar localmente antes de push
- 🎯 Pipeline debe ser rápido (<5 min)

**Coverage**:
- 🎯 80% es mínimo razonable (no 100%)
- 🎯 Priorizar casos edge críticos
- 🎯 No escribir tests solo por coverage

**Linting**:
- 🎯 Configurar una vez, usar siempre
- 🎯 No ignorar warnings sin razón
- 🎯 Formateo automático (ruff format)

**Security**:
- 🎯 Nunca hardcodear secrets
- 🎯 Escanear en cada PR
- 🎯 Entender el riesgo real (no solo pasar el scanner)

---

## 🔧 Troubleshooting con IA

**Pipeline falla en GitHub pero pasa localmente**:

```
Mi pipeline de CI falla en GitHub Actions pero pasa localmente.

Error en GitHub:
[PEGA EL ERROR]

Logs:
[PEGA LOS LOGS RELEVANTES]

Mi configuración local:
- Python: [VERSION]
- OS: [SISTEMA]
- Dependencies: [requirements.txt]

¿Qué puede estar causando la diferencia?
```

**Coverage cae inesperadamente**:

```
El coverage bajó de 85% a 78% después de agregar nuevas funciones.

Archivo con problemas: api/servicio.py
Líneas sin cubrir: 45-62

Código nuevo agregado:
[PEGA EL CÓDIGO]

Usando Test Coverage Strategist:
1. ¿Qué casos faltantes causan el drop?
2. Dame tests mínimos para recuperar 80%+
```

---

## 🔗 Recursos Adicionales

- 📘 **GitHub Actions Docs**: https://docs.github.com/actions
- 🎓 **Ruff Documentation**: https://docs.astral.sh/ruff/
- 📚 **Bandit Docs**: https://bandit.readthedocs.io/
- 🎯 **Coverage.py**: https://coverage.readthedocs.io/
- 🤖 **Agentes Usados**:
  - Test Coverage Strategist
  - Python Best Practices Coach
  - Security Hardening Mentor

---

## 📝 Plantilla de Documentación

Crea `CI_CD_SETUP.md` con esta información:

```markdown
# CI/CD Pipeline Documentation

## Pipeline Overview

**Trigger**: Push y PR a `main` y `dev`
**Duration**: ~X minutos
**Jobs**: Test, Lint, Security

## Jobs Description

### 1. Test Job
- Pytest con coverage ≥ 80%
- Fail si coverage baja

### 2. Lint Job
- Ruff check con configuración en pyproject.toml
- PEP 8 compliance

### 3. Security Job
- Bandit scan (high/medium severity)
- Fail si encuentra vulnerabilidades

## Local Development

```bash
# Ejecutar todos los checks localmente
./scripts/run-ci-locally.sh

# O manualmente:
pytest --cov=api --cov-fail-under=80
ruff check api/
bandit -r api/ -ll
```

## Troubleshooting

**Pipeline falla**: [Soluciones comunes]
**Coverage bajo**: [Cómo mejorar]
**Linter issues**: [Cómo resolver]
```

---

**Tiempo estimado**: 3 horas

**Siguiente módulo**: Módulo 3 - Calidad y Seguridad (seguridad avanzada con IA)
