# AI Workflow - Clase 5: Pipelines Seguros con DevSecOps + IA

## 🎯 Objetivos de Aprendizaje con IA

En esta clase aprenderás a usar IA como asistente para:

1. **Generar pipelines CI/CD seguros** automáticamente
2. **Configurar escaneo de secretos** (gitleaks) con reglas personalizadas
3. **Detectar vulnerabilidades** en dependencias con safety + dependabot
4. **Implementar branch protection** y deployment strategies
5. **Troubleshooting** de pipelines con asistencia de IA

---

## 🔄 Workflow Completo: De Pipeline Básico a DevSecOps

### Fase 1: Generación de GitHub Actions Workflow Seguro

**Contexto**: Ya tienes tests y coverage funcionando (Clase 3-4). Ahora necesitas añadir escaneo de seguridad al pipeline.

#### Prompt 1: Generar workflow CI/CD completo con seguridad

```
Rol: DevSecOps engineer especializado en GitHub Actions
Contexto: API FastAPI con tests, coverage (80%), Bandit, y JWT
Objetivo: Crear GitHub Actions workflow que incluya seguridad completa
Restricciones:
- Escaneo de dependencias (safety)
- Detección de secretos (gitleaks)
- Coverage mínimo 80%
- Auditoría de código (Bandit)
- Falla rápido si hay vulnerabilidades críticas

Entrega:
- Archivo .github/workflows/ci_security.yml completo
- Comentarios explicando cada step
- Estrategia de caching para acelerar pipeline
```

**Resultado esperado**:

```yaml
name: CI/CD con Seguridad

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]

jobs:
  security-and-tests:
    runs-on: ubuntu-latest

    steps:
      # 1. Checkout con historial completo (necesario para gitleaks)
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      # 2. Setup Python con cache de dependencias
      - name: Set up Python 3.12
        uses: actions/setup-python@v4
        with:
          python-version: 3.12
          cache: 'pip'

      # 3. Instalar dependencias
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # 4. Secret scanning (PRIMERO - falla rápido)
      - name: Secret scanning with Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      # 5. Dependency vulnerability scanning
      - name: Security audit with Safety
        run: |
          pip install safety
          safety check --json > safety-report.json || true
          safety check --continue-on-error

      # 6. Code security audit (Bandit)
      - name: Security linting with Bandit
        run: |
          pip install bandit
          bandit -r api/ -ll -f json -o bandit-report.json

      # 7. Linting (Ruff)
      - name: Lint with Ruff
        run: |
          pip install ruff
          ruff check api/

      # 8. Run tests with coverage
      - name: Test with pytest and coverage
        run: |
          pytest --cov=api --cov-report=term-missing --cov-fail-under=80

      # 9. Upload security reports as artifacts
      - name: Upload security reports
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: |
            safety-report.json
            bandit-report.json
```

**Por qué este orden**:
- ✅ **Gitleaks primero**: Falla rápido si hay secretos (no pierdas tiempo en tests)
- ✅ **Safety después**: Detecta vulnerabilidades de dependencias antes de instalarlas
- ✅ **Bandit + tests al final**: Si llegaste aquí, el código es seguro en términos de secrets/deps
- ✅ **Artifacts**: Reportes se guardan aunque el pipeline falle

#### Validación con Python Best Practices Coach

Después de generar el workflow, usa el agente educativo:

```bash
# Invocar Python Best Practices Coach agent
# El agente revisará:
# ✓ Nombres de jobs son descriptivos
# ✓ Steps tienen comentarios claros
# ✓ Usa cache para acelerar
# ✓ Fail-fast strategy aplicada
# ✓ Artifacts se suben correctamente
```

---

### Fase 2: Configuración Avanzada de Gitleaks

**Problema**: Gitleaks detecta falsos positivos (ej: "password" en comentarios, URLs con "token" en el nombre).

#### Prompt 2: Crear configuración personalizada de gitleaks

```
Rol: Security engineer especializado en secret scanning
Contexto: API FastAPI con gitleaks configurado, pero detecta falsos positivos
Objetivo: Crear .gitleaks.toml que ignore falsos positivos comunes
Restricciones:
- Ignorar comentarios con "password" (no son claves reales)
- Ignorar URLs de ejemplo (ej: https://api.example.com/token)
- Mantener detección de claves reales (AWS, JWT secrets, API keys)
- Documentar cada regla personalizada

Entrega:
- Archivo .gitleaks.toml completo
- .gitleaksignore para paths específicos (docs/, examples/)
- Explicación de cada custom rule
```

**Resultado esperado**:

```toml
# .gitleaks.toml - Configuración personalizada de Gitleaks

title = "Gitleaks Config - API Tareas"

# Reglas por defecto de Gitleaks
[extend]
useDefault = true

# Paths a ignorar completamente
[allowlist]
paths = [
    '''docs/''',
    '''examples/''',
    '''tests/fixtures/'''
]

# Regexes específicas a ignorar
regexes = [
    # Ignorar "password" en comentarios de Python
    '''# .*(password|secret).*''',

    # Ignorar URLs de ejemplo
    '''https?://.*example\.(com|org).*''',

    # Ignorar constantes de test
    '''TEST_.*SECRET.*'''
]

# Custom rules (además de las default)
[[rules]]
id = "custom-jwt-secret"
description = "JWT secret real (no de test)"
regex = '''JWT_SECRET\s*=\s*['"][^'"]{32,}['"]'''
tags = ["key", "JWT"]

[[rules]]
id = "custom-api-key"
description = "API Key real (formato específico)"
regex = '''API_KEY\s*=\s*['"]sk-[a-zA-Z0-9]{40,}['"]'''
tags = ["key", "API"]
```

**Archivo .gitleaksignore**:

```
# Paths específicos a ignorar
docs/ejemplos_vulnerables/
tests/fixtures/fake_secrets.py

# Líneas específicas (por hash de commit)
# Usa: gitleaks detect --log-level=debug para obtener hashes
```

**Validación**:

```bash
# Probar configuración localmente
gitleaks detect --config .gitleaks.toml -v

# Resultado esperado:
# - No detecta "password" en comentarios ✅
# - No detecta URLs de ejemplo ✅
# - SÍ detecta JWT_SECRET real ✅
# - SÍ detecta API keys reales ✅
```

---

### Fase 3: Detección Automática de Vulnerabilidades en Dependencias

**Problema**: Safety solo escanea al hacer CI. Necesitas detección continua + auto-fixes.

#### Prompt 3: Configurar dependabot + safety policies

```
Rol: Dependency security specialist
Contexto: API FastAPI en producción con 20+ dependencias
Objetivo: Configurar dependabot para auto-updates seguros + safety policies
Restricciones:
- Solo auto-update patches de seguridad (no breaking changes)
- Crear PRs automáticos con changelog
- Agrupar updates por tipo (security, dependencies, dev-dependencies)
- Configurar límite de PRs abiertas (max 5 simultáneas)

Entrega:
- Archivo .github/dependabot.yml
- Configuración de safety policies
- Estrategia de revisión de auto-PRs
```

**Resultado esperado (.github/dependabot.yml)**:

```yaml
version: 2
updates:
  # Security updates (máxima prioridad)
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "daily"  # Revisar diario para security
      time: "06:00"
    open-pull-requests-limit: 5

    # Agrupar updates de seguridad
    groups:
      security-updates:
        patterns:
          - "*"
        update-types:
          - "patch"

    # Labels automáticos
    labels:
      - "dependencies"
      - "security"

    # Commit message format
    commit-message:
      prefix: "chore(deps)"
      include: "scope"

    # Reviewers automáticos
    reviewers:
      - "tu-usuario"

    # Solo security patches (no features ni breaking)
    versioning-strategy: increase-if-necessary

  # Dev dependencies (menos frecuente)
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 3

    groups:
      dev-dependencies:
        patterns:
          - "pytest*"
          - "ruff"
          - "bandit"
        update-types:
          - "patch"
          - "minor"

    labels:
      - "dependencies"
      - "dev-dependencies"
```

**Safety Policy (.safety-policy.yml)**:

```yaml
# Política de seguridad para safety CLI
security:
  # Nivel mínimo de severidad para fallar CI
  fail-on-severity: medium

  # Ignorar vulnerabilidades específicas (con justificación)
  ignore-vulnerabilities:
    # Ejemplo: CVE viejo que no aplica a nuestro uso
    # - id: "51668"
    #   reason: "No usamos la funcionalidad vulnerable"
    #   expires: "2025-12-31"

  # Configuración de reportes
  output:
    format: json
    file: safety-report.json

# Auto-apply patches de seguridad
auto-apply:
  patch-updates: true
  minor-updates: false  # Requiere revisión manual
  major-updates: false  # Requiere revisión manual
```

**Workflow de revisión de auto-PRs**:

```markdown
Checklist para PRs de Dependabot:

1. ✅ Ver changelog del PR (Dependabot lo incluye automáticamente)
2. ✅ Verificar que CI pasa (tests + coverage + security)
3. ✅ Revisar breaking changes en CHANGELOG.md de la librería
4. ✅ Si es patch de seguridad → merge automático
5. ✅ Si es minor/major → revisar manualmente
```

---

### Fase 4: Branch Protection y Deployment Strategies

**Problema**: Cualquiera puede hacer push a main sin revisión ni CI.

#### Prompt 4: Configurar branch protection + deployment strategy

```
Rol: DevOps engineer especializado en Git workflows
Contexto: API FastAPI con CI/CD completo (tests, coverage, security)
Objetivo: Configurar branch protection rules para main + dev
Restricciones:
- Requiere PR + revisión antes de merge
- Requiere CI green (todos los checks pasan)
- Requiere coverage >= 80%
- No permite force push ni delete
- Deployment solo desde main (con aprobación manual)

Entrega:
- Lista de branch protection rules a configurar
- Deployment workflow con aprobación manual
- Rollback strategy si deployment falla
```

**Branch Protection Rules (configurar en GitHub UI)**:

```markdown
## Rules para branch: main

**Require a pull request before merging**:
- ✅ Require approvals: 1
- ✅ Dismiss stale pull request approvals when new commits are pushed
- ✅ Require review from Code Owners (si usas CODEOWNERS)

**Require status checks to pass before merging**:
- ✅ Require branches to be up to date before merging
- ✅ Status checks required:
  * security-and-tests (job del CI)
  * gitleaks
  * coverage-80

**Require conversation resolution before merging**:
- ✅ All conversations must be resolved

**Require signed commits** (opcional pero recomendado):
- ✅ Require signed commits

**Do not allow bypassing the above settings**:
- ✅ Do not allow bypassing the above settings
- ✅ Restrict who can push to matching branches (solo admins)

**Rules applied to everyone including administrators**:
- ✅ Include administrators
```

**Deployment Workflow con Aprobación Manual**:

```yaml
# .github/workflows/deploy_production.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://api-tareas.tudominio.com

    steps:
      # 1. Esperar aprobación manual
      - name: Wait for manual approval
        uses: trstringer/manual-approval@v1
        with:
          approvers: tu-usuario,otro-reviewer
          minimum-approvals: 1
          issue-title: "Deploy to Production - Review Required"
          issue-body: |
            **Deployment Details**:
            - Branch: ${{ github.ref }}
            - Commit: ${{ github.sha }}
            - Author: ${{ github.actor }}

            Please review and approve deployment to production.

      # 2. Checkout code
      - uses: actions/checkout@v4

      # 3. Run final security check
      - name: Final security scan
        run: |
          pip install safety bandit
          safety check
          bandit -r api/ -ll

      # 4. Deploy (ejemplo con Railway)
      - name: Deploy to Railway
        run: |
          # Tu comando de deploy aquí
          echo "Deploying to production..."
          # railway up --service api-tareas

      # 5. Health check post-deployment
      - name: Health check
        run: |
          sleep 10
          curl -f https://api-tareas.tudominio.com/health || exit 1

      # 6. Rollback automático si falla
      - name: Rollback on failure
        if: failure()
        run: |
          echo "Deployment failed - rolling back"
          # railway rollback --service api-tareas
```

**Rollback Strategy**:

```bash
# Rollback manual si algo falla después del deploy

# 1. Ver últimos deployments
railway deployments list --service api-tareas

# 2. Rollback a la versión anterior
railway rollback <deployment-id>

# 3. Verificar que el rollback funcionó
curl https://api-tareas.tudominio.com/health

# 4. Investigar qué falló
railway logs --service api-tareas --tail 100
```

---

## 🧪 Ejercicios Prácticos con IA

### Ejercicio 1: Generar GitHub Actions Workflow Completo (25 min)

**Objetivo**: Usar IA para generar un pipeline CI/CD con seguridad completa.

**Pasos**:

1. **Usa el Prompt 1** (arriba) para generar el workflow

2. **Crea el archivo**:
   ```bash
   mkdir -p .github/workflows
   # Pega el código generado en .github/workflows/ci_security.yml
   ```

3. **Valida el workflow**:
   ```bash
   # Instala act para probar workflows localmente (opcional)
   # brew install act  # macOS
   # choco install act  # Windows

   # O simplemente commit y push para ver si funciona
   git add .github/workflows/ci_security.yml
   git commit -m "feat: añadir CI/CD con seguridad completa"
   git push
   ```

4. **Revisa el resultado en GitHub Actions**:
   - Ve a tu repo → Actions
   - Verifica que el workflow corre correctamente
   - Revisa los security reports artifacts

**Criterios de aceptación**:
- [ ] Workflow corre sin errores
- [ ] Gitleaks detecta (o no detecta) secretos correctamente
- [ ] Safety reporta vulnerabilidades (si hay)
- [ ] Coverage cumple 80%+
- [ ] Artifacts de seguridad se generan

---

### Ejercicio 2: Configurar Gitleaks con Reglas Personalizadas (20 min)

**Objetivo**: Eliminar falsos positivos de gitleaks usando configuración custom.

**Pasos**:

1. **Crea falsos positivos intencionalmente**:
   ```python
   # api/test_falsos_positivos.py
   # Este archivo tiene "secretos" que NO son reales

   # Comentario con password (falso positivo)
   def test_login():
       """
       Test de login con password verificado.
       """
       pass

   # URL de ejemplo (falso positivo)
   DOCS_URL = "https://api.example.com/docs?token=example"
   ```

2. **Ejecuta gitleaks sin configuración**:
   ```bash
   gitleaks detect --source . --no-git
   # Debería detectar falsos positivos
   ```

3. **Usa el Prompt 2** para generar `.gitleaks.toml`

4. **Prueba la configuración**:
   ```bash
   gitleaks detect --config .gitleaks.toml -v
   # Los falsos positivos deberían desaparecer
   ```

5. **Crea un secreto REAL de prueba**:
   ```python
   # api/test_secreto_real.py
   JWT_SECRET = "sk-1234567890abcdef1234567890abcdef12345678"
   ```

6. **Verifica que SÍ lo detecta**:
   ```bash
   gitleaks detect --config .gitleaks.toml
   # Debería detectar el secreto real
   ```

**Criterios de aceptación**:
- [ ] `.gitleaks.toml` creado y documentado
- [ ] Falsos positivos ignorados correctamente
- [ ] Secretos reales SÍ se detectan
- [ ] Configuración validada localmente

---

### Ejercicio 3: Setup Safety + Dependabot (20 min)

**Objetivo**: Configurar detección automática de vulnerabilidades con auto-updates.

**Pasos**:

1. **Registra una cuenta en Safety CLI** (gratis):
   ```bash
   pip install safety
   safety auth login
   ```

2. **Escanea tu proyecto**:
   ```bash
   safety check
   # Anota cuántas vulnerabilidades detecta
   ```

3. **Usa el Prompt 3** para generar `.github/dependabot.yml`

4. **Crea el archivo de configuración**:
   ```bash
   # Pega el contenido generado
   ```

5. **Haz commit y espera 24h** (Dependabot corre diario):
   ```bash
   git add .github/dependabot.yml
   git commit -m "feat: configurar dependabot para auto-updates"
   git push
   ```

6. **Valida la configuración**:
   - Ve a tu repo → Insights → Dependency graph → Dependabot
   - Verifica que esté activo
   - Espera a que genere PRs automáticos

**Criterios de aceptación**:
- [ ] Dependabot configurado correctamente
- [ ] Safety detecta vulnerabilidades (si hay)
- [ ] Configuración agrupa updates por tipo
- [ ] Límite de PRs configurado (max 5)

---

### Ejercicio 4: Implementar Branch Protection (15 min)

**Objetivo**: Proteger branch main para requerir CI + revisión.

**Pasos**:

1. **Ve a tu repo en GitHub** → Settings → Branches

2. **Crea Branch Protection Rule para `main`**:
   - Branch name pattern: `main`
   - Activa todas las opciones del Prompt 4

3. **Prueba la protección**:
   ```bash
   # Intenta hacer push directo a main (debería fallar)
   git checkout main
   echo "test" >> README.md
   git commit -m "test: intentar push directo"
   git push origin main
   # Error: protected branch
   ```

4. **Flujo correcto con PR**:
   ```bash
   git checkout -b feature/test-branch-protection
   echo "test" >> README.md
   git commit -m "test: validar branch protection"
   git push origin feature/test-branch-protection

   # Crea PR en GitHub UI
   # Verifica que CI debe pasar antes de merge
   ```

**Criterios de aceptación**:
- [ ] Push directo a main bloqueado
- [ ] PR requiere aprobación
- [ ] PR requiere CI green
- [ ] Coverage 80% requerido

---

### Ejercicio 5: Troubleshooting de Pipeline Failures (25 min)

**Objetivo**: Usar IA para diagnosticar y resolver errores de CI/CD.

**Escenarios preparados**:

#### Escenario A: Gitleaks falla por secreto accidental

**Simular error**:
```python
# api/config.py
JWT_SECRET = "supersecretkey123456789"  # ❌ Hardcoded
```

```bash
git add api/config.py
git commit -m "feat: añadir config"
git push
# CI falla en gitleaks step
```

**Prompt para troubleshooting**:
```
Rol: DevSecOps troubleshooter
Error: Gitleaks detectó secreto en api/config.py
Logs:
[pegar logs de gitleaks del CI]

Tareas:
1. Identificar el secreto detectado
2. Sugerir cómo moverlo a .env
3. Actualizar .gitleaksignore si es necesario
4. Verificar que el fix funciona
```

**Solución esperada**:
1. Mover secreto a `.env.template`
2. Usar `os.getenv("JWT_SECRET")` en código
3. Actualizar `.gitleaksignore` para ignorar `.env.template`
4. Re-ejecutar CI

---

#### Escenario B: Safety detecta vulnerabilidad

**Simular error**:
```bash
# Instala una versión vieja con vulnerabilidades conocidas
pip install requests==2.25.0  # Versión con CVE
pip freeze > requirements.txt
git commit -m "feat: actualizar deps"
git push
# CI falla en safety step
```

**Prompt para troubleshooting**:
```
Safety detectó vulnerabilidad en requirements.txt:

[pegar output de safety check]

¿Cómo soluciono esto sin romper compatibilidad?
```

**Solución esperada**:
1. Actualizar a versión segura: `pip install requests==2.31.0`
2. Verificar que no rompe tests
3. Actualizar `requirements.txt`

---

#### Escenario C: Coverage cae debajo de 80%

**Simular error**:
```python
# api/nueva_funcion.py (sin tests)
def procesar_datos(datos):
    # Código sin testear
    return datos.upper()
```

**Prompt para troubleshooting**:
```
CI falla porque coverage bajó a 75% (mínimo 80%)
Nuevo código en api/nueva_funcion.py sin tests

¿Cómo genero tests rápidamente con IA?
```

**Solución esperada**:
1. Usar IA para generar tests básicos
2. Ejecutar `pytest --cov` localmente
3. Iterar hasta alcanzar 80%+

---

## 📋 Prompts Reutilizables

### Prompt: Generar workflow CI/CD desde cero

```
Rol: DevSecOps automation specialist
Contexto: [Describir tu stack: FastAPI/Django/Flask, testing framework, etc.]
Objetivo: Crear GitHub Actions workflow completo con DevSecOps
Restricciones:
- Incluir: linting, testing, coverage, security scanning
- Estrategia fail-fast
- Caching de dependencias
- Artifacts de reportes

Stack técnico:
- Lenguaje: Python 3.12
- Framework: [tu framework]
- Testing: pytest
- Linter: ruff
- Security: safety, bandit, gitleaks

Entrega: Archivo .github/workflows/ci.yml completo con comentarios
```

### Prompt: Troubleshooting de CI failures

```
Rol: CI/CD troubleshooting expert
Error: [Descripción del error]
Logs:
```
[Pegar logs completos del CI]
```

Contexto:
- Workflow file: [pegar YAML]
- Último commit: [hash y mensaje]
- Branch: [nombre]

Tareas:
1. Identificar causa raíz
2. Sugerir 3 soluciones ordenadas por probabilidad
3. Comandos específicos para validar fix
4. Prevención para el futuro

Entrega: Diagnóstico + fix paso a paso
```

### Prompt: Optimizar pipeline lento

```
Rol: CI/CD performance optimizer
Contexto: Mi pipeline tarda 8 minutos, quiero reducirlo a <3 min
Workflow actual:
```
[Pegar YAML]
```

Objetivos:
- Reducir tiempo total a < 3 min
- Mantener todos los checks de seguridad
- No sacrificar coverage

Entrega:
- Análisis de bottlenecks
- Estrategias de caching
- Paralelización de jobs
- YAML optimizado
```

---

## 🔍 Validación Final con Agents

Antes de dar por completada la clase, ejecuta este checklist:

### Python Best Practices Coach Validation

```markdown
**GitHub Actions Workflow**:
- [ ] Jobs tienen nombres descriptivos
- [ ] Steps están comentados claramente
- [ ] Usa caching para dependencias
- [ ] Fail-fast strategy aplicada
- [ ] Secrets se manejan correctamente (no hardcoded)

**Python Scripts en CI**:
- [ ] Scripts usan type hints
- [ ] Manejo de errores apropiado
- [ ] Logging configurado correctamente
```

### Docker Infrastructure Guide Validation (si usas Docker)

```markdown
**Deployment Configuration**:
- [ ] Dockerfile usa multi-stage builds
- [ ] Usuario no-root configurado
- [ ] Health checks implementados
- [ ] Secrets via environment variables
```

---

## 🎯 Resultado Esperado

Al finalizar esta clase, deberías tener:

1. **GitHub Actions workflow** completo con:
   - Gitleaks (secret scanning)
   - Safety (dependency scanning)
   - Bandit (code security)
   - Tests + coverage (80%+)

2. **Configuración de seguridad**:
   - `.gitleaks.toml` personalizado
   - `.github/dependabot.yml` activo
   - Branch protection rules en main

3. **Troubleshooting skills**:
   - Diagnosticar failures con IA
   - Resolver vulnerabilidades detectadas
   - Optimizar pipelines lentos

4. **Documentación**:
   - Proceso de DevSecOps en notes.md
   - Estrategias de rollback documentadas

**Impacto de IA en DevSecOps**:
- ⚡ **70% más rápido**: Generar workflows desde cero
- 🛡️ **90% menos errores**: Validación automática de configuraciones
- ✅ **100% reproducible**: Pipelines documentados y versionados

---

## 📖 Recursos Adicionales

**Documentación oficial**:
- [GitHub Actions Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [Gitleaks Configuration](https://github.com/gitleaks/gitleaks#configuration)
- [Dependabot Configuration](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file)

**Herramientas de validación**:
- `act`: Ejecuta GitHub Actions localmente
- `gitleaks detect`: Escaneo local de secretos
- `safety check`: Auditoría de dependencias

**Agentes educativos**:
- Python Best Practices Coach: `.claude/agents/educational/python-best-practices-coach.md`
- Docker Infrastructure Guide: `.claude/agents/educational/docker-infrastructure-guide.md`
