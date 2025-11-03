# CI/CD Pipeline - Proyecto Final

Este documento explica el pipeline de CI/CD implementado con GitHub Actions.

---

## 🔄 Workflows Configurados

### 1. **CI Pipeline** (`.github/workflows/ci.yml`)

Se ejecuta automáticamente en:
- ✅ Push a `main`, `dev`, o ramas `feature/**`
- ✅ Pull Requests a `main` o `dev`
- ✅ Solo cuando hay cambios en la Clase 8

#### Jobs Ejecutados:

**1. Tests y Coverage** ✅
```bash
pytest --cov=api --cov-report=term-missing --cov-fail-under=80
```
- Ejecuta todos los tests
- Genera reporte de coverage
- **Falla si coverage < 80%**
- Sube reporte a Codecov (opcional)

**2. Linting (Ruff)** 🔍
```bash
ruff check api/
```
- Verifica estilo de código
- Detecta errores comunes
- Usa configuración de `ruff.toml`

**3. Security Audit (Bandit)** 🔒
```bash
bandit -r api/ -ll
```
- Detecta vulnerabilidades de seguridad
- Nivel: High y Medium (`-ll`)
- Genera reporte JSON

**4. Verificar Migraciones (Alembic)** 🔄
```bash
alembic upgrade head
alembic check
```
- Aplica migraciones en BD de test
- Verifica que no hay cambios pendientes
- Detecta modelos sin migración

**5. Docker Build** 🐳
```bash
docker build -t api-tareas:test .
```
- Verifica que el Dockerfile es válido
- Build completo (no push)
- Usa cache de GitHub Actions

**6. CI Summary** 📊
- Genera resumen de todos los jobs
- Muestra tabla con resultados
- Falla el workflow si algún job falló

---

## 🎯 Cómo Funciona

### Flujo de Desarrollo con CI

```
1. Crear rama feature
   ├─ git checkout -b feature/nueva-funcionalidad
   └─ Implementar código

2. Commit y Push
   ├─ git add .
   ├─ git commit -m "feat: nueva funcionalidad"
   └─ git push origin feature/nueva-funcionalidad

3. CI se ejecuta automáticamente ⚡
   ├─ Tests (debe pasar)
   ├─ Linting (debe pasar)
   ├─ Security (debe pasar)
   ├─ Migrations (debe pasar)
   └─ Docker (debe pasar)

4. Crear Pull Request
   ├─ Si CI pasa: ✅ PR listo para review
   └─ Si CI falla: ❌ Arreglar antes de merge

5. Merge a dev/main
   └─ CI vuelve a ejecutarse
```

---

## 🚀 Deploy Pipeline (`.github/workflows/deploy.yml`)

**Nota:** Este workflow es **opcional** y se ejecuta manualmente.

Railway y Render hacen deployment automático desde su dashboard:

### Railway
```bash
# Deployment automático al conectar GitHub repo
# O con Railway CLI:
npm i -g @railway/cli
railway link
railway up
```

### Render
```bash
# Deployment automático al conectar repo
# Detecta render.yaml automáticamente
# Deploy en cada push a main
```

---

## 📊 Badges para README

Agrega estos badges al README principal del proyecto:

```markdown
![CI Status](https://github.com/tu-usuario/tu-repo/actions/workflows/ci.yml/badge.svg)
![Coverage](https://codecov.io/gh/tu-usuario/tu-repo/branch/main/graph/badge.svg)
```

---

## 🔧 Configuración de Ruff

Ver `ruff.toml`:

```toml
line-length = 100
target-version = "py312"

[lint]
select = ["E", "W", "F", "I", "B", "C4", "UP"]
ignore = ["E501", "B008"]
```

**Reglas aplicadas:**
- ✅ PEP 8 (E, W)
- ✅ Pyflakes (F)
- ✅ Import sorting (I)
- ✅ Bugbear (B)
- ✅ Comprehensions (C4)
- ✅ Pyupgrade (UP)

---

## 🐛 Troubleshooting

### Tests fallan en CI pero pasan localmente

**Causa:** Variables de entorno diferentes

**Solución:**
```yaml
# En ci.yml
env:
  DATABASE_URL: sqlite:///./test.db
  JWT_SECRET: test-secret-key-for-ci
  ENVIRONMENT: dev
```

### Coverage no alcanza 80%

**Ver qué falta:**
```bash
pytest --cov=api --cov-report=html
# Abre htmlcov/index.html en navegador
```

**Agregar más tests:**
- Casos edge
- Error handling
- Validaciones

### Ruff encuentra errores

**Ejecutar localmente:**
```bash
ruff check api/ --fix
```

**Ignorar reglas específicas:**
```python
# En el archivo:
# ruff: noqa: E501

# O en ruff.toml:
ignore = ["E501"]
```

### Bandit reporta falsos positivos

**Ignorar línea específica:**
```python
password = get_password()  # nosec B106
```

**O en comando:**
```bash
bandit -r api/ -ll --skip B201,B301
```

### Docker build falla

**Verificar localmente:**
```bash
cd "Modulo 4 - Infraestructura y Cloud/Clase 8 - Proyecto Final"
docker build -t test .
```

**Errores comunes:**
- COPY rutas incorrectas
- Dependencias faltantes en requirements.txt
- Puerto no expuesto

---

## 📈 Mejoras Futuras

### 1. Integration Tests con PostgreSQL
```yaml
services:
  postgres:
    image: postgres:15
    env:
      POSTGRES_PASSWORD: postgres
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
```

### 2. E2E Tests con Playwright
```yaml
- name: E2E Tests
  run: |
    npm install -g @playwright/test
    playwright install
    pytest tests_e2e/
```

### 3. Performance Tests
```yaml
- name: Load Testing
  run: |
    pip install locust
    locust -f tests_load/locustfile.py --headless -u 100 -r 10
```

### 4. Deploy Automático a Staging
```yaml
on:
  push:
    branches: [dev]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Staging
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: railway up
```

---

## ✅ Checklist de CI/CD

Antes de hacer merge a `main`:

- [ ] Todos los tests pasan
- [ ] Coverage ≥ 80%
- [ ] Ruff no reporta errores
- [ ] Bandit no reporta vulnerabilidades críticas
- [ ] Alembic check pasa
- [ ] Docker build exitoso
- [ ] PR tiene descripción clara
- [ ] Commits siguen Conventional Commits

---

## 📚 Referencias

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Pytest Coverage](https://pytest-cov.readthedocs.io/)
- [Ruff Linter](https://docs.astral.sh/ruff/)
- [Bandit Security](https://bandit.readthedocs.io/)
- [Railway Deployment](https://docs.railway.app/)
- [Render Deployment](https://render.com/docs)
