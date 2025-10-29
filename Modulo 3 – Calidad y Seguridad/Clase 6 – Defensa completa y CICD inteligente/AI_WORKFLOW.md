# Workflow AI - Clase 6: Defensa Completa y CI/CD Inteligente

## 🎯 Objetivo

Usar IA para **configurar pipelines DevSecOps** que integren seguridad en cada etapa del CI/CD (shift-left security).

---

## 🤖 Agentes Recomendados

### 1. Security Hardening Mentor
- **DevSecOps**: SAST, DAST, SCA en pipeline
- **Container security**: Docker image scanning

### 2. Docker Infrastructure Guide
- **Secure Dockerfile**: Multi-stage, non-root, minimal base
- **Image scanning**: Trivy, Snyk

---

## 🚀 Workflow: DevSecOps Pipeline con IA

### Paso 1: Diseño del Pipeline Seguro

**Prompt**:
```
Diseña pipeline DevSecOps para API FastAPI.

Stages necesarios:
1. Code Quality
   - Ruff (linting)
   - mypy (type checking)
   - pytest (coverage ≥80%)

2. Security - SAST (Static Analysis)
   - Bandit (code vulnerabilities)
   - Safety (dependency vulnerabilities)
   - Gitleaks (secret scanning)

3. Security - Container
   - Trivy (Docker image scan)
   - Dockerfile best practices

4. Security - DAST (Dynamic Analysis)
   - OWASP ZAP (running app scan)
   - Postman security tests

5. Deploy
   - Solo si todos los checks pasan

Muestra estructura GitHub Actions workflow completa.
```

---

### Paso 2: Implementar Security Gates

```yaml
# .github/workflows/devsecops.yml
name: DevSecOps Pipeline

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main]

jobs:
  sast:
    name: Static Analysis
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Bandit Security Scan
        run: |
          pip install bandit
          bandit -r api/ -ll -f json -o bandit_results.json
          # Fail si severity high/critical
          bandit -r api/ -ll

      - name: Dependency Check
        run: |
          pip install safety
          safety check --json > safety_results.json

      - name: Secret Scanning
        uses: gitleaks/gitleaks-action@v2

  container-security:
    name: Container Security
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t api-test:latest .

      - name: Trivy Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: api-test:latest
          severity: 'CRITICAL,HIGH'
          exit-code: '1'  # Fail si encuentra critical/high

  dast:
    name: Dynamic Analysis
    runs-on: ubuntu-latest
    needs: [sast, container-security]
    steps:
      - name: Start API
        run: |
          docker run -d -p 8000:8000 api-test:latest

      - name: OWASP ZAP Scan
        uses: zaproxy/action-full-scan@v0.10.0
        with:
          target: 'http://localhost:8000'
```

---

### Paso 3: AI-Powered Security Review

**Prompt para revisión pre-merge**:
```
Revisa este PR antes de merge a main:

[PEGA git diff]

Checklist de seguridad DevSecOps:
1. ¿Nuevas dependencias añadidas? → Verificar CVEs
2. ¿Código modifica autenticación/autorización? → Review exhaustivo
3. ¿Dockerfile cambiado? → Verificar best practices
4. ¿Variables de entorno nuevas? → No secrets hardcoded
5. ¿Tests de seguridad añadidos? → Coverage de casos maliciosos

Dame aprobación Go/No-Go con justificación.
```

---

### Paso 4: Security Dashboard

**Prompt**:
```
Crea script para generar dashboard de seguridad:

Inputs:
- bandit_results.json
- safety_results.json
- trivy_results.json

Output: security_dashboard.html con:
1. Security Score (0-100)
2. Vulnerabilities por severidad (Critical/High/Medium/Low)
3. Trends (comparar con builds anteriores)
4. Top 5 issues que arreglar
5. OWASP Top 10 coverage

Usar jinja2 templates + charts.js
```

---

## ✅ Checklist DevSecOps

```markdown
Pipeline CI/CD:
- [ ] SAST scan en cada PR (Bandit)
- [ ] Dependency check (Safety)
- [ ] Secret scanning (Gitleaks)
- [ ] Docker image scanning (Trivy)
- [ ] DAST tests opcionales (OWASP ZAP)

Security Gates:
- [ ] PR bloqueado si Critical/High vulnerabilities
- [ ] Auto-merge solo si todos los scans pasan
- [ ] Notificaciones a Slack en failures

Monitoring:
- [ ] Security dashboard actualizado
- [ ] Alertas de nuevas CVEs
- [ ] Compliance reports mensuales
```

---

**Tiempo**: 3 horas | **Agentes**: Security Hardening Mentor, Docker Infrastructure Guide
