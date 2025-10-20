# Python Best Practices Coach - Code Review Report
## Modulo 3 – Clase 5: Defensa activa y pipelines seguros

**Review Date**: 2025-10-20
**Reviewed by**: Python Best Practices Coach (Educational Agent)
**Files Reviewed**: 7 Python files in `api/`

---

## Executive Summary

The code is **functional and demonstrates good security practices** (JWT, Pydantic validation), but has several opportunities for improvement in terms of modern Python patterns.

**Overall Grade**: **B+ (85/100)**

### Key Strengths
1. ✅ Excellent security foundation with JWT
2. ✅ Clean architecture with dependency inversion
3. ✅ Good use of Pydantic validation
4. ✅ Type hints present throughout

### Key Areas for Growth
1. ❌ Migrate to modern Python stdlib (Pathlib, built-in generics)
2. ❌ Add comprehensive logging for security events
3. ⚠️ Improve configuration validation
4. ⚠️ Add complete docstrings

---

## Priority Issues

### 🔴 CRITICAL: File Path Handling with os.path

**File**: `repositorio_json.py` (lines 13-17, 20, 34)

**Current Code** (Anti-pattern):
```python
import os

def __init__(self, ruta_archivo: str = "tareas.json"):
    self._ruta = ruta_archivo
    if not os.path.exists(self._ruta):
        with open(self._ruta, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
```

**Why This Matters**:
1. **Security risk**: `os.path` doesn't validate paths as robustly as Pathlib
2. **Platform compatibility**: Manual string paths can break on Windows/Linux differences
3. **Readability**: More verbose than modern alternatives

**Pythonic Solution** (PEP 519):
```python
from pathlib import Path

def __init__(self, ruta_archivo: str | Path = "tareas.json"):
    self._ruta = Path(ruta_archivo)
    if not self._ruta.exists():
        self._ruta.write_text("[]", encoding="utf-8")
```

**Benefits**:
- ✅ **Safer**: Pathlib validates paths automatically
- ✅ **Shorter**: `.read_text()` vs `with open() as f: f.read()`
- ✅ **Type-safe**: IDE autocomplete for path operations
- ✅ **Cross-platform**: Handles Windows/Linux paths automatically

---

### 🟡 MEDIUM: Type Hints Improvements

#### Issue 1: Using Old typing Module Generics

**Files**: `repositorio_base.py`, `seguridad_jwt.py`, `servicio_tareas.py`

**Current Code**:
```python
from typing import List, Dict, Optional

def listar(self) -> List["Tarea"]: ...
def verificar_jwt(...) -> Dict[str, Any]: ...
def crear_token(claims: Dict[str, Any], minutos: Optional[int] = None) -> str: ...
```

**Modern Solution** (Python 3.10+):
```python
def listar(self) -> list["Tarea"]: ...
def verificar_jwt(...) -> dict[str, Any]: ...
def crear_token(claims: dict[str, Any], minutos: int | None = None) -> str: ...
```

**Why This Matters**:
- ✅ **Simpler imports**: No need for `List`, `Dict`, `Optional`
- ✅ **Consistency**: Matches modern Python (3.10+ standard)
- ✅ **Future-proof**: `typing.List` is deprecated in Python 3.9+

---

#### Issue 2: Missing Type Hints on Internal Functions

**File**: `seguridad_jwt.py` (line 10-14)

**Current Code**:
```python
def _config():
    secret = os.getenv("JWT_SECRET", "dev-secret")
    minutos = int(os.getenv("JWT_MINUTOS", "30"))
    return secret, minutos
```

**Improved with NamedTuple**:
```python
from typing import NamedTuple

class JWTConfig(NamedTuple):
    """Configuración JWT inmutable."""
    secret: str
    expiration_minutes: int

def _config() -> JWTConfig:
    """Lee la configuración JWT desde variables de entorno."""
    secret = os.getenv("JWT_SECRET", "dev-secret")
    minutos = int(os.getenv("JWT_MINUTOS", "30"))
    return JWTConfig(secret=secret, expiration_minutes=minutos)
```

**Benefits**:
- ✅ **Named access**: `config.secret` instead of `config[0]`
- ✅ **Self-documenting**: Clear what each field means
- ✅ **Type-safe**: IDE knows field types

---

### 🟡 MEDIUM: Error Handling & Security

#### Issue 1: Missing Logging for Security Events

**File**: `seguridad_jwt.py` (line 34-38)

**Current Code**:
```python
try:
    payload = jwt.decode(token, secret, algorithms=["HS256"])
    return payload
except JWTError:
    raise HTTPException(status_code=401, detail="Token inválido o expirado")
```

**Production-Ready Solution**:
```python
import logging

logger = logging.getLogger(__name__)

def verificar_jwt(
    authorization: str | None = Header(None, alias="Authorization")
) -> dict[str, Any]:
    if not authorization or not authorization.lower().startswith("bearer "):
        logger.warning("Intento de acceso sin token válido")
        raise HTTPException(
            status_code=401,
            detail="Token ausente o formato inválido"
        )

    token = authorization.split(" ", 1)[1].strip()
    config = _config()

    try:
        payload = jwt.decode(token, config.secret, algorithms=["HS256"])
        logger.debug(f"Token verificado exitosamente para: {payload.get('sub')}")
        return payload
    except JWTError as e:
        logger.warning(f"Token inválido rechazado: {e}")
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado"
        )
```

**Benefits**:
- ✅ **Auditable**: Log failed authentication attempts
- ✅ **Debuggable**: Know why tokens fail in production
- ✅ **Secure**: Don't leak internal error details

---

#### Issue 2: Integer Conversion Without Validation

**File**: `seguridad_jwt.py` (line 13)

**Current Code**:
```python
minutos = int(os.getenv("JWT_MINUTOS", "30"))
```

**Problem**: If `JWT_MINUTOS="abc"`, raises `ValueError`

**Robust Solution with Pydantic Settings**:
```python
from pydantic_settings import BaseSettings

class JWTSettings(BaseSettings):
    """Configuración JWT con validación automática."""
    jwt_secret: str = "dev-secret"
    jwt_minutos: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = False

# Uso
settings = JWTSettings()  # Valida automáticamente
```

---

### 🟢 LOW: Code Style Optimizations

#### Issue: Hardcoded Credentials (Security Anti-pattern)

**File**: `api.py` (line 27)

**Current Code**:
```python
if cuerpo.usuario == "demo" and cuerpo.password == "demo":
    token = crear_token({"sub": cuerpo.usuario})
    return LoginResponse(access_token=token)
```

**Educational Note**: Acceptable for demos, but dangerous for production.

**Production-Ready Solution**:
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

USERS_DB = {
    "demo": {
        "username": "demo",
        "hashed_password": pwd_context.hash("demo"),
    }
}

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def authenticate_user(username: str, password: str) -> bool:
    user = USERS_DB.get(username)
    if not user:
        return False
    return verify_password(password, user["hashed_password"])

@app.post("/login", response_model=LoginResponse)
def login(cuerpo: LoginRequest):
    if not authenticate_user(cuerpo.usuario, cuerpo.password):
        logger.warning(f"Login fallido: {cuerpo.usuario}")
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = crear_token({"sub": cuerpo.usuario})
    return LoginResponse(access_token=token)
```

**Security Benefits**:
- ✅ **Never store plain passwords**: bcrypt hashing
- ✅ **Constant-time comparison**: Prevents timing attacks
- ✅ **Auditable**: Log authentication attempts

---

## Recommended Actions (Prioritized)

### Phase 1: Critical Security & Safety (1-2 hours)
1. ✅ **Migrate to Pathlib** in `repositorio_json.py`
2. ✅ **Add input validation** to `_config()` in `seguridad_jwt.py`
3. ✅ **Add logging** to authentication flows

### Phase 2: Modernization (2-3 hours)
4. ⚠️ **Update type hints** to Python 3.10+ syntax (`list`, `dict`, `|`)
5. ⚠️ **Add comprehensive docstrings** to all public functions
6. ⚠️ **Replace tuple return** with NamedTuple in `_config()`

### Phase 3: Production Hardening (4-6 hours)
7. 📝 **Implement Pydantic Settings** for configuration
8. 📝 **Add password hashing** to login endpoint
9. 📝 **Add comprehensive logging** throughout
10. 📝 **Add unit tests** for edge cases

---

## Example: Complete Refactored seguridad_jwt.py

```python
# api/seguridad_jwt.py (REFACTORED VERSION)
"""Módulo de seguridad JWT con validación y logging."""

from datetime import datetime, timedelta, timezone
from typing import Any
import logging

from fastapi import Header, HTTPException
from jose import jwt, JWTError
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class JWTSettings(BaseSettings):
    """Configuración JWT con validación automática."""
    jwt_secret: str = "dev-secret"
    jwt_minutos: int = 30

    class Config:
        env_prefix = ""
        case_sensitive = False


def crear_token(claims: dict[str, Any], minutos: int | None = None) -> str:
    """Crea un token JWT firmado.

    Args:
        claims: Datos del payload (ej: {"sub": "username"})
        minutos: Minutos de expiración (None usa config default)

    Returns:
        Token JWT codificado como string
    """
    settings = JWTSettings()
    exp_min = settings.jwt_minutos if minutos is None else minutos

    to_encode = claims.copy()
    to_encode["exp"] = datetime.now(tz=timezone.utc) + timedelta(minutes=exp_min)

    logger.debug(f"Creando token para: {claims.get('sub')} (exp: {exp_min}m)")
    return jwt.encode(to_encode, settings.jwt_secret, algorithm="HS256")


def verificar_jwt(
    authorization: str | None = Header(None, alias="Authorization")
) -> dict[str, Any]:
    """Verifica el token JWT del header Authorization.

    Args:
        authorization: Header 'Authorization: Bearer <token>'

    Returns:
        Payload decodificado del token

    Raises:
        HTTPException: 401 si token ausente, mal formado, inválido o expirado
    """
    if not authorization or not authorization.lower().startswith("bearer "):
        logger.warning("Intento de acceso sin token Bearer")
        raise HTTPException(
            status_code=401,
            detail="Token ausente o formato inválido"
        )

    token = authorization.split(" ", 1)[1].strip()
    settings = JWTSettings()

    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        logger.debug(f"Token verificado para: {payload.get('sub')}")
        return payload
    except JWTError as e:
        logger.warning(f"Token JWT inválido: {type(e).__name__}")
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado"
        )
```

---

## Educational Resources

### PEPs to Study
- **PEP 519**: Adding pathlib to standard library
- **PEP 604**: Union types with `|` syntax
- **PEP 484**: Type hints fundamentals

### Recommended Tools
```bash
# Type checking
mypy api/ --strict

# Modern linting
ruff check api/

# Security scanning
bandit -r api/ -ll
```

### Books & Tutorials
- "Fluent Python" (Luciano Ramalho) - Chapter 7 (Protocols)
- Real Python: "Python Type Checking Guide"
- FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/

---

## Final Assessment

**Overall Score**: **B+ (85/100)**

**Breakdown**:
- Security practices: A (90/100)
- Code organization: A- (88/100)
- Type hints: B+ (85/100)
- Modern Python patterns: B (80/100)
- Error handling: B (82/100)
- Documentation: C+ (75/100)

**Student Level**: **Intermediate → Advanced transition**

This student understands core concepts well and is ready to learn production-level patterns.

---

> **"Code that works is good. Code that's Pythonic, secure, and maintainable is excellent."**
