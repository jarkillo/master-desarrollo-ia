# Workflow AI - Clase 3: Auditoría Continua y Defensa Inteligente con IA

## 🎯 Objetivo

Automatizar auditorías de seguridad usando **IA como revisor de código** y **detectar patrones de vulnerabilidades** que los scanners tradicionales no ven.

---

## 🤖 Agentes Recomendados

### 1. Security Hardening Mentor
- **Auditoría de código completo**: Lógica de negocio vulnerable
- **Detección de patrones inseguros**: Race conditions, TOCTOU

### 2. Clean Architecture Enforcer
- **Validar capas**: ¿Lógica de seguridad en lugar correcto?
- **Detectar bypass**: ¿Validaciones saltadas?

---

## 🚀 Workflow: Auditoría Inteligente con IA

### Paso 1: Auditoría de Lógica de Negocio

**Prompt avanzado**:
```
Audita esta lógica de negocio buscando vulnerabilidades sutiles:

[PEGA servicio_tareas.py]

Busca específicamente:
1. Race conditions en operaciones concurrentes
2. IDOR (Insecure Direct Object Reference)
3. Business logic bypass
4. Time-of-check to time-of-use (TOCTOU)
5. Missing authorization checks
6. Information leakage en errores

Para cada problema encontrado:
- Línea específica
- Severidad (Critical/High/Medium/Low)
- Explotación posible
- Código corregido
```

---

### Paso 2: Revisión de Dependencias

**Prompt**:
```
Analiza mi requirements.txt:

[PEGA requirements.txt]

1. ¿Hay versiones con vulnerabilidades conocidas?
2. ¿Dependencias innecesarias (aumentan superficie de ataque)?
3. ¿Falta pinning de versiones (reproducibilidad)?
4. Sugerencias de actualización segura

Usa CVE databases y PyPI advisory.
```

---

### Paso 3: Testing de Seguridad con IA

**Prompt para generar tests de penetración**:
```
Genera tests de penetración para:

[PEGA api.py]

Tests de seguridad necesarios:
1. test_sql_injection_en_queries
2. test_xss_en_responses
3. test_idor_acceso_recursos_ajenos
4. test_rate_limiting_funciona
5. test_auth_bypass_attempts

Usa pytest con requests maliciosos reales.
```

---

### Paso 4: Configurar Auditoría Continua

```yaml
# .github/workflows/security-audit.yml
name: Security Audit

on:
  schedule:
    - cron: '0 0 * * 0'  # Semanal
  push:
    branches: [main]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Dependency check
        run: |
          pip install safety
          safety check --json > safety_report.json

      - name: Bandit scan
        run: |
          pip install bandit
          bandit -r api/ -ll -f json -o bandit_report.json

      - name: AI Security Review
        run: |
          # Enviar reportes a Claude Code API
          # Generar reporte consolidado
```

---

## ✅ Checklist Auditoría Continua

```markdown
- [ ] Auditoría semanal automatizada
- [ ] Dependency scanning (Safety)
- [ ] Code scanning (Bandit)
- [ ] IA review de lógica de negocio
- [ ] Tests de penetración en CI
- [ ] Reportes consolidados
- [ ] Alertas en Slack/email
```

---

**Tiempo**: 2 horas | **Agentes**: Security Hardening Mentor, Clean Architecture Enforcer
