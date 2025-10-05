# 🧠 Glosario – Clase 4: Seguridad avanzada y autenticación con JWT

### 🔐 JWT (JSON Web Token)

Es un **token firmado digitalmente** que contiene información sobre la identidad del usuario.

Permite a la API verificar quién eres sin mantener sesiones en memoria.

**Estructura:**

1. **Header** – Tipo de token y algoritmo (ej. `HS256`).
2. **Payload** – Datos o *claims* (ej. `sub: "usuario"`, `exp: timestamp`).
3. **Signature** – Prueba criptográfica de que el token no fue modificado.

El servidor lo firma con una **clave secreta** (guardada en variables de entorno), y el cliente lo manda en cada petición con:

`Authorization: Bearer <token>`.

---

### 🕒 Expiración

Todo JWT debe tener una fecha de expiración (`exp`).

Pasado ese tiempo, deja de ser válido → el usuario debe volver a autenticarse.

Esto evita accesos indefinidos si el token se filtra.

---

### 🔑 Variables de entorno

Datos sensibles como `JWT_SECRET` o la duración del token (`JWT_MINUTOS`) **no se escriben en el código**.

Se guardan en el entorno o en `.env` para evitar exponer claves.

---

### ⚙️ Funciones principales

- **`crear_token(datos)`**
    
    Genera un JWT nuevo con `exp` y firma.
    
    Ejemplo:
    
    ```python
    token = crear_token({"sub": "usuario123"})
    
    ```
    
- **`verificar_jwt(authorization)`**
    
    Extrae el token del header `Authorization: Bearer ...`,
    
    lo decodifica, y lanza `HTTPException(401)` si no es válido o está expirado.
    

---

### 🧩 Endpoint `/login`

Ruta pública que recibe credenciales (usuario, contraseña) y devuelve un token firmado.

Ejemplo de respuesta:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}

```

---

### 🧰 Dependencia `Depends(verificar_jwt)`

Protege las rutas que requieren autenticación:

```python
@app.get("/tareas", dependencies=[Depends(verificar_jwt)])

```

Así, si el cliente no envía un token válido, FastAPI devuelve automáticamente `401 Unauthorized`.

---

### 🧪 Tests críticos

1. **Login válido devuelve token.**
2. **Acceso con token → 200 o 201.**
3. **Token inválido → 401.**
4. **Token expirado → 401.**

Esto garantiza que la seguridad funcione igual que cualquier otra feature.

---

### ⚖️ Diferencias clave

| Concepto | API Key | JWT |
| --- | --- | --- |
| Alcance | Global (una sola clave) | Individual (por usuario) |
| Duración | Permanente | Expira |
| Portabilidad | Simple pero insegura | Más segura y escalable |
| Ideal para | Microservicios internos | Autenticación de usuarios finales |

---

### 💡 Buenas prácticas

- No guardes la clave JWT en el repo.
- Usa HTTPS siempre (los tokens viajan por cabeceras).
- Si el token expira, devuelve 401 y pide re-login.
- Nunca reutilices un JWT viejo.

---

### 🧾 Resumen mental

> “La API Key protege la casa.
> 
> 
> El JWT da una llave única y con fecha de caducidad a cada visitante.
>