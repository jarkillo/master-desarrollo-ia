# Workflow AI - Clase 2: Seguridad Básica en tu API

## 🎯 Objetivo

Usar IA para **detectar y corregir vulnerabilidades OWASP Top 10** en tu API FastAPI.

---

## 🤖 Agentes Recomendados

### 1. Security Hardening Mentor
- **Qué detecta**: Injection, broken auth, sensitive data exposure, XSS, SSRF
- **Cuándo usar**: Antes de cada commit, después de Bandit scan

### 2. API Design Reviewer
- **Qué valida**: Endpoints seguros, rate limiting, CORS correcto

---

## 🚀 Workflow: Auditoría de Seguridad con IA

### Paso 1: Escaneo Automático

```bash
# Ejecutar Bandit
bandit -r api/ -ll -o bandit_report.json -f json
```

**Prompt con Security Hardening Mentor**:
```
Bandit detectó estos issues:

[PEGA bandit_report.json]

Para cada issue:
1. ¿Es falso positivo o riesgo real?
2. ¿Cuál es el ataque posible?
3. Dame el código corregido
4. ¿Cómo prevenirlo en el futuro?
```

---

### Paso 2: Checklist Manual con IA

**Prompt**:
```
Revisa mi API contra OWASP Top 10:

[PEGA api.py]

Verifica:
1. A01:2021 – Broken Access Control
   - ¿Endpoints públicos sin auth?
   - ¿IDs expuestos sin autorización?

2. A02:2021 – Cryptographic Failures
   - ¿Passwords en plaintext?
   - ¿Secrets hardcodeados?

3. A03:2021 – Injection
   - ¿SQL injection posible?
   - ¿Command injection?

4. A04:2021 – Insecure Design
   - ¿Rate limiting?
   - ¿CORS demasiado permisivo?

5. A05:2021 – Security Misconfiguration
   - ¿Debug=True en producción?
   - ¿Errores exponen stack traces?

Dame reporte detallado con severidad (Critical/High/Medium/Low).
```

---

### Paso 3: Implementar Correcciones

**Ejemplo: Secrets Management**

```python
# ❌ ANTES (inseguro)
JWT_SECRET = "mysecretkey123"

# ✅ DESPUÉS (seguro)
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwt_secret: str

    class Config:
        env_file = ".env"

settings = Settings()
```

---

## ✅ Checklist de Seguridad Básica

```markdown
- [ ] Sin secrets hardcodeados
- [ ] Variables de entorno con python-dotenv
- [ ] CORS configurado correctamente
- [ ] Rate limiting en endpoints públicos
- [ ] Validación de inputs con Pydantic
- [ ] HTTPException con mensajes seguros (no stack traces)
- [ ] Bandit scan sin issues high/critical
```

---

**Tiempo**: 2 horas | **Agentes**: Security Hardening Mentor, API Design Reviewer
