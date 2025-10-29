# Workflow AI - Clase 1: El Código que se Defiende Solo (Pydantic Validation)

## 🎯 Objetivo

Usar IA para **diseñar validaciones robustas con Pydantic** que prevengan errores antes de que lleguen a producción. Aprende a hacer que tu código rechace datos inválidos automáticamente.

---

## 🤖 Agentes Recomendados

### 1. FastAPI Design Coach
- **Cuándo**: Al diseñar modelos Pydantic
- **Qué valida**: Validaciones completas, Field() constraints, custom validators

### 2. Security Hardening Mentor
- **Cuándo**: Al validar inputs de usuario
- **Qué detecta**: SQL injection, XSS, path traversal

---

## 🚀 Workflow: Validación con IA

### Paso 1: Identificar Vectores de Ataque

**Prompt**:
```
Tengo este modelo Pydantic básico:

class TareaCreate(BaseModel):
    nombre: str

¿Qué inputs maliciosos podría recibir?
Lista 10 casos edge que debería validar.
```

### Paso 2: Diseñar Validaciones

**Prompt con Security Hardening Mentor**:
```
Diseña validaciones Pydantic para:

1. nombre:
   - Min 3, max 100 caracteres
   - No HTML tags
   - No SQL keywords (', --, ;)
   - No path traversal (../, ..\)

2. descripcion (opcional):
   - Max 500 caracteres
   - Permitir markdown seguro
   - No scripts

Muestra el modelo con Field() y validators.
```

**Código generado**:
```python
from pydantic import BaseModel, Field, validator
import re

class TareaCreate(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    descripcion: str | None = Field(None, max_length=500)

    @validator('nombre')
    def validar_nombre_seguro(cls, v):
        # No HTML tags
        if re.search(r'<[^>]+>', v):
            raise ValueError("HTML tags no permitido")
        # No SQL injection básico
        if any(kw in v.lower() for kw in ["'", "--", ";", "union", "select"]):
            raise ValueError("Caracteres sospechosos detectados")
        return v.strip()
```

### Paso 3: Testing de Validaciones

**Prompt**:
```
Genera tests para intentar romper estas validaciones:

[PEGA EL MODELO]

Tests necesarios:
1. Inputs válidos (deben pasar)
2. Inputs inválidos (deben fallar con 422)
3. Casos edge (longitudes límite, caracteres especiales)
4. Ataques comunes (SQL injection, XSS)

Usa TestClient de FastAPI.
```

---

## ✅ Checklist de Validación

```markdown
- [ ] Todos los campos tienen min/max length
- [ ] Strings validan caracteres peligrosos
- [ ] Emails usan EmailStr de Pydantic
- [ ] URLs usan HttpUrl
- [ ] Números tienen range constraints
- [ ] Custom validators para lógica compleja
- [ ] Tests cubren casos maliciosos
```

---

**Tiempo**: 1.5 horas | **Agentes**: FastAPI Design Coach, Security Hardening Mentor
