# Workflow AI - Clase 4: Seguridad Avanzada y Autenticación con JWT

## 🎯 Objetivo

Usar IA para **implementar autenticación JWT segura** y **evitar errores comunes** (secrets débiles, tokens sin expiración, etc.).

---

## 🤖 Agentes Recomendados

### 1. Security Hardening Mentor
- **JWT best practices**: Algoritmos seguros, claims correctos, revocación
- **Password hashing**: bcrypt, argon2

### 2. FastAPI Design Coach
- **Dependency injection**: `Depends(get_current_user)`
- **Auth flows**: Login, refresh tokens, logout

---

## 🚀 Workflow: Implementar JWT con IA

### Paso 1: Diseño de Autenticación

**Prompt**:
```
Diseña sistema de autenticación JWT para FastAPI.

Requisitos:
1. Registro: email + password (hasheado)
2. Login: retorna access token (exp: 30min) + refresh token (exp: 7d)
3. Endpoints protegidos: require valid token
4. Refresh: renovar access token con refresh token
5. Logout: invalidar tokens (blacklist)

Seguridad:
- Algoritmo: RS256 (no HS256 si es multi-service)
- Password hashing: bcrypt con salt
- Secrets en variables de entorno
- Rate limiting en /login y /register

Muestra arquitectura y flujo de autenticación.
```

---

### Paso 2: Implementación Segura

**Prompt con Security Hardening Mentor**:
```
Implementa módulo seguridad_jwt.py con:

1. generate_token(user_id: int) -> str
   - Claims: sub, exp, iat, jti (unique id)
   - Exp: 30 minutos

2. verify_token(token: str) -> dict
   - Validar firma
   - Verificar expiración
   - Raise HTTPException 401 si inválido

3. hash_password(password: str) -> str
   - bcrypt con rounds=12

4. verify_password(plain: str, hashed: str) -> bool

Configuración segura:
- JWT_SECRET desde os.getenv()
- JWT_ALGORITHM = "HS256"  # o RS256 si multi-service
- ACCESS_TOKEN_EXPIRE_MINUTES = 30

Muestra código completo con manejo de errores.
```

---

### Paso 3: Dependency de Autorización

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency para proteger endpoints."""
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        # Obtener usuario de DB
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# Uso en endpoints
@app.get("/tareas", response_model=List[TareaResponse])
async def listar_tareas(current_user: int = Depends(get_current_user)):
    """Endpoint protegido - requiere autenticación."""
    return obtener_tareas_del_usuario(current_user)
```

---

### Paso 4: Testing de Seguridad JWT

**Prompt**:
```
Genera tests de seguridad para JWT:

1. test_login_con_credenciales_validas
   - POST /login
   - Assert 200 + access_token

2. test_login_con_password_incorrecto
   - Assert 401

3. test_endpoint_protegido_sin_token
   - GET /tareas sin Authorization header
   - Assert 401

4. test_endpoint_protegido_con_token_invalido
   - Token manipulado
   - Assert 401

5. test_token_expirado
   - Token viejo
   - Assert 401

6. test_refresh_token_funciona
   - POST /refresh con refresh_token válido
   - Assert 200 + nuevo access_token
```

---

## ✅ Checklist JWT Seguro

```markdown
- [ ] Secrets en variables de entorno (NO hardcoded)
- [ ] Tokens con expiración (access: 30min, refresh: 7d)
- [ ] Passwords hasheados con bcrypt (rounds≥12)
- [ ] Algoritmo seguro (HS256 o RS256)
- [ ] Claims estándar (sub, exp, iat, jti)
- [ ] Manejo de errores sin exponer detalles
- [ ] Rate limiting en /login y /register
- [ ] Tests de seguridad completos
```

---

**Tiempo**: 3 horas | **Agentes**: Security Hardening Mentor, FastAPI Design Coach
