# Módulo 5 - Clase 3: Autenticación Full-Stack con JWT

Esta clase implementa un **sistema de autenticación completo** con JWT (JSON Web Tokens), demostrando patrones profesionales de auth en aplicaciones full-stack: **registro, login, sesiones persistentes, rutas protegidas** y **axios interceptors** para manejo automático de tokens.

## 📋 Tabla de Contenidos

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Nuevas Tecnologías](#nuevas-tecnologías)
3. [Arquitectura](#arquitectura)
4. [Instalación y Ejecución](#instalación-y-ejecución)
5. [Conceptos Clave](#conceptos-clave)
6. [🤖 AI Integration (40% del contenido)](#-ai-integration-40-del-contenido)
7. [Diferencias con Clase 2](#diferencias-con-clase-2)
8. [Ejercicios y Mejoras](#ejercicios-y-mejoras)
9. [Recursos Adicionales](#recursos-adicionales)

---

## Descripción del Proyecto

Una aplicación full-stack con autenticación JWT completa que demuestra:

### Backend (FastAPI + JWT)

- ✅ **Registro de usuarios** con bcrypt para hashear passwords
- ✅ **Login** con verificación de credenciales
- ✅ **Generación de JWT** con claims personalizados
- ✅ **Endpoints protegidos** que requieren token válido
- ✅ **Validación automática** de tokens con dependency injection
- ✅ **Manejo de errores** (401, 409) con mensajes claros
- ✅ **Tests completos** (20+ tests cubriendo auth flow)

### Frontend (React + TypeScript + JWT)

- ✅ **Auth Context** para estado global de autenticación
- ✅ **Login/Register forms** con React Hook Form + Zod
- ✅ **Protected Routes** que redirigen si no hay auth
- ✅ **Axios Interceptor** para agregar token automáticamente
- ✅ **Persistencia de sesión** con localStorage
- ✅ **Auto-logout** si token expira (401)
- ✅ **Loading states** durante verificación de auth
- ✅ **React Router** para navegación

---

## Nuevas Tecnologías

### JWT (JSON Web Tokens)

**¿Qué es?** Estándar abierto (RFC 7519) para crear tokens de acceso que afirman claims.

**¿Por qué usarlo?**
- ✅ **Stateless**: No requiere sesiones en servidor
- ✅ **Portable**: Funciona en web, mobile, microservicios
- ✅ **Self-contained**: Token incluye toda la info (payload)
- ✅ **Verificable**: Firma criptográfica previene manipulación

**Alternativas**: Sessions (cookies), OAuth 2.0, Auth0, Firebase Auth

**Estructura JWT**:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9    ← Header (algoritmo)
.eyJzdWIiOiJ1c2VyXzEyMyIsImVtYWlsI...   ← Payload (claims)
.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV    ← Signature (HMAC)
```

### React Context API

**¿Qué es?** Mecanismo de React para compartir estado global sin prop drilling.

**¿Por qué usarlo para auth?**
- ✅ Estado de auth accesible en toda la app
- ✅ Evita pasar `user` y `login()` por props manualmente
- ✅ Centraliza lógica de autenticación
- ✅ Integración sencilla con hooks personalizados

**Alternativas**: Redux, Zustand, Recoil, Jotai

### Protected Routes

**¿Qué son?** Componentes de React Router que verifican autenticación antes de renderizar.

**¿Por qué usarlas?**
- ✅ Previenen acceso no autorizado
- ✅ Centralizan lógica de redirección
- ✅ Mejoran UX (redirigen automáticamente)

**Patrón**:
```tsx
<Route path="/dashboard" element={
  <ProtectedRoute>
    <Dashboard />
  </ProtectedRoute>
} />
```

### Axios Interceptors

**¿Qué son?** Funciones que se ejecutan antes/después de cada request HTTP.

**¿Por qué usarlos?**
- ✅ Agregan token JWT automáticamente a todas las requests
- ✅ Manejan errores 401 globalmente (auto-logout)
- ✅ Evitan código repetitivo (`Authorization: Bearer ...`)
- ✅ Centralizan lógica de refresh tokens

---

## Arquitectura

### Backend (FastAPI)

```
backend/
├── api/
│   ├── api.py                    # Endpoints: register, login, /auth/me
│   ├── seguridad_jwt.py          # Crear/verificar tokens JWT
│   ├── modelos.py                # Pydantic models (User, AuthResponse, etc.)
│   ├── servicio_usuarios.py     # Lógica de negocio (bcrypt, auth)
│   ├── repositorio_usuarios.py  # Almacenamiento in-memory de usuarios
│   └── dependencias.py           # Dependency injection
├── tests/
│   ├── conftest.py
│   └── test_auth.py              # 20+ tests de auth flow
└── requirements.txt
```

**Endpoints disponibles**:
- `POST /auth/register` - Registro (201 Created)
- `POST /auth/login` - Login (200 OK)
- `GET /auth/me` - Usuario actual (requiere JWT)
- `GET /protected/dashboard` - Ejemplo de endpoint protegido
- `GET /` - Health check

### Frontend (React + TypeScript)

```
frontend/
├── src/
│   ├── components/
│   │   ├── LoginForm.tsx         # Form con RHF + Zod
│   │   ├── RegisterForm.tsx      # Form con validación completa
│   │   ├── Dashboard.tsx         # Página protegida
│   │   └── ProtectedRoute.tsx    # HOC para rutas protegidas
│   ├── contexts/
│   │   └── AuthContext.tsx       # Estado global de auth
│   ├── services/
│   │   └── auth.service.ts       # API calls + axios interceptor
│   ├── types/
│   │   └── auth.ts               # Tipos TypeScript
│   ├── App.tsx                   # Routing con React Router
│   ├── App.css                   # Estilos
│   └── main.tsx
├── package.json
└── vite.config.ts
```

---

## Instalación y Ejecución

### Prerrequisitos

- Python 3.12+
- Node.js 18+
- npm o yarn

### 1. Backend (FastAPI)

```bash
# Navegar al directorio backend
cd backend

# Activar entorno virtual (IMPORTANTE según CLAUDE.md)
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (opcional)
# export JWT_SECRET="tu-secret-super-seguro"
# export JWT_MINUTOS="60"

# Ejecutar servidor de desarrollo
uvicorn api.api:app --reload

# El backend estará disponible en: http://localhost:8000
# Documentación automática: http://localhost:8000/docs
```

**Ejecutar tests**:
```bash
cd backend
pytest --cov=api --cov-report=term-missing -v
```

### 2. Frontend (React + Vite)

```bash
# Navegar al directorio frontend
cd frontend

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev

# El frontend estará disponible en: http://localhost:5173
```

### 3. Ejecutar ambos simultáneamente

**Terminal 1** (Backend):
```bash
cd backend
uvicorn api.api:app --reload
```

**Terminal 2** (Frontend):
```bash
cd frontend
npm run dev
```

Abrir navegador en `http://localhost:5173`.

**Flujo de uso**:
1. Ir a `/register` y crear una cuenta
2. Serás redirigido automáticamente a `/dashboard`
3. Cerrar sesión y probar `/login`
4. Intentar acceder a `/dashboard` sin auth → redirige a `/login`

---

## Conceptos Clave

### 1. Flujo de Autenticación Completo

#### Registro de Usuario

```
User Form → Frontend → POST /auth/register → Backend
                                             ↓
                                      1. Validar datos (Pydantic)
                                      2. Hash password (bcrypt)
                                      3. Guardar usuario
                                      4. Generar JWT
                                             ↓
                         JWT + User ← 201 Created
    ↓
localStorage.setItem("auth_token", jwt)
AuthContext.setUser(user)
Navigate to /dashboard
```

#### Login

```
User Form → Frontend → POST /auth/login → Backend
                                          ↓
                                   1. Buscar usuario por email
                                   2. Verificar password (bcrypt)
                                   3. Generar JWT
                                          ↓
                        JWT + User ← 200 OK
    ↓
localStorage.setItem("auth_token", jwt)
AuthContext.setUser(user)
Navigate to /dashboard
```

#### Request a Endpoint Protegido

```
GET /auth/me → Axios Interceptor agrega header
               Authorization: Bearer <token>
                      ↓
               Backend verifica JWT
                      ↓
            ¿Token válido? → Sí → Return user data
                      ↓
                     No
                      ↓
              401 Unauthorized
                      ↓
        Axios Interceptor detecta 401
                      ↓
           localStorage.removeItem("auth_token")
           Navigate to /login
```

### 2. JWT: Anatomía y Seguridad

#### Estructura de un JWT

```json
// HEADER
{
  "alg": "HS256",
  "typ": "JWT"
}

// PAYLOAD (claims)
{
  "sub": "user_123",       // Subject (ID del usuario)
  "email": "user@example.com",
  "nombre": "Juan Pérez",
  "exp": 1729757400       // Expiration (Unix timestamp)
}

// SIGNATURE
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

#### Claims comunes

- `sub` (subject): ID del usuario
- `exp` (expiration): Timestamp de expiración
- `iat` (issued at): Timestamp de creación
- `iss` (issuer): Quién emitió el token
- `aud` (audience): Para quién es el token

#### ¿Cómo se verifica un JWT?

1. **Separar las 3 partes** (header, payload, signature)
2. **Decodificar header y payload** (Base64)
3. **Recrear signature** usando secret y algoritmo del header
4. **Comparar signatures**: Si coinciden, token es válido
5. **Verificar `exp`**: Si está expirado, rechazar

**Código de verificación (backend)**:
```python
from jose import jwt, JWTError

def verificar_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        # Verifica automáticamente exp y signature
        return payload
    except JWTError:
        raise HTTPException(401, "Token inválido o expirado")
```

### 3. Axios Interceptors: Magia de Headers Automáticos

#### Request Interceptor

**Problema sin interceptor**:
```typescript
// ❌ Código repetitivo en cada request
const getUser = async () => {
  const token = localStorage.getItem("auth_token");
  const response = await axios.get("/auth/me", {
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.data;
};
```

**Solución con interceptor**:
```typescript
// ✅ Configurar una vez
axiosInstance.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Usar en todas las requests (sin repetir código)
const getUser = async () => {
  const response = await axiosInstance.get("/auth/me");
  return response.data;
};
```

#### Response Interceptor

**Problema sin interceptor**:
```typescript
// ❌ Manejar 401 en cada request
try {
  const response = await axios.get("/auth/me");
} catch (error) {
  if (error.response?.status === 401) {
    localStorage.removeItem("auth_token");
    window.location.href = "/login";
  }
}
```

**Solución con interceptor**:
```typescript
// ✅ Manejar 401 globalmente
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      removeToken();
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);
```

### 4. Auth Context: Estado Global de Autenticación

#### ¿Por qué Context API?

**Problema sin Context**:
```tsx
// ❌ Prop drilling: pasar user por 5 niveles
<App user={user} setUser={setUser}>
  <Layout user={user}>
    <Dashboard user={user}>
      <Header user={user}>
        <UserMenu user={user} />  // Finalmente lo usamos aquí
      </Header>
    </Dashboard>
  </Layout>
</App>
```

**Solución con Context**:
```tsx
// ✅ Estado accesible en cualquier componente
<AuthProvider>
  <App>
    <Layout>
      <Dashboard>
        <Header>
          <UserMenu />  // useAuth() aquí directamente
        </Header>
      </Dashboard>
    </Layout>
  </App>
</AuthProvider>
```

#### Implementación del AuthContext

```typescript
const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    // Verificar si hay sesión activa al cargar
    const checkAuth = async () => {
      if (authService.isAuthenticated()) {
        const currentUser = await authService.getCurrentUser();
        setUser(currentUser);
      }
    };
    checkAuth();
  }, []);

  const login = async (data) => {
    const response = await authService.login(data);
    setUser(response.user);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// Hook personalizado
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
}
```

### 5. Protected Routes: Guardias de Rutas

#### Implementación

```typescript
export function ProtectedRoute({ children }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <div>Cargando...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}
```

#### Uso

```typescript
<Routes>
  <Route path="/login" element={<LoginForm />} />
  <Route path="/dashboard" element={
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  } />
</Routes>
```

---

## 🤖 AI Integration (40% del contenido)

Esta sección demuestra cómo usar **IA como arquitecto de seguridad** para implementar autenticación robusta, detectar vulnerabilidades y seguir mejores prácticas.

### 1. Generación de Sistema de Autenticación Completo

#### Prompt para generar backend con JWT

```
Crea un sistema de autenticación completo en FastAPI con JWT:

Backend:
- Endpoint POST /auth/register (email, password, nombre)
- Endpoint POST /auth/login
- Endpoint GET /auth/me (protegido con JWT)
- Password hashing con bcrypt
- JWT con python-jose
- Tokens con expiración de 1 hora
- Validación con Pydantic (email válido, password mínimo 8 caracteres)
- Repositorio in-memory para usuarios
- Tests completos con pytest

JWT debe incluir claims: sub (user_id), email, nombre, exp

Usa dependency injection para verificar JWT en endpoints protegidos.
```

**La IA generará**:
1. Módulo `seguridad_jwt.py` con `crear_token()` y `verificar_jwt()`
2. Modelos Pydantic con validación completa
3. Servicio con bcrypt para hashing
4. Repositorio de usuarios
5. Endpoints con manejo de errores (401, 409)
6. Tests cubriendo registro, login, endpoints protegidos

#### Prompt para generar frontend con Auth Context

```
Crea un frontend React + TypeScript con autenticación JWT:

Componentes:
- AuthContext con estado global (user, login, register, logout)
- LoginForm con React Hook Form + Zod (email, password)
- RegisterForm con validación (email, password, confirmPassword, nombre)
- ProtectedRoute que redirige a /login si no hay auth
- Dashboard protegido que muestra info del usuario

Axios:
- Interceptor de request que agrega Authorization: Bearer <token>
- Interceptor de response que maneja 401 (auto-logout)
- Token almacenado en localStorage

React Router:
- /login (pública)
- /register (pública)
- /dashboard (protegida)
- / (redirige según estado de auth)

TypeScript:
- Tipos para User, AuthResponse, LoginRequest, RegisterRequest
- Todo completamente tipado

Incluye estilos CSS modernos con gradientes.
```

**La IA generará**:
1. AuthContext con `useEffect` para verificar sesión al cargar
2. Formularios con validación Zod completa
3. ProtectedRoute con loading states
4. Axios interceptors configurados correctamente
5. Tipos TypeScript para toda la app
6. CSS con diseño profesional

### 2. Debugging de Problemas Comunes de Auth

#### Prompt: Token no se envía en requests

```
Mi aplicación no envía el token JWT en las requests.

Código del axios interceptor:
[pegar código]

Comportamiento:
- Login funciona (token se guarda en localStorage)
- Al hacer GET /auth/me, backend dice "Token ausente"
- En Network tab no veo Authorization header

¿Qué está mal? Muestra la solución con explicación.
```

**La IA detectará**:
- Problema: Axios instance no se está usando (usando `axios` global)
- Solución: Usar `axiosInstance` en todos los servicios
- Explicación: El interceptor solo aplica a la instancia configurada

#### Prompt: Token expira y app no maneja el error

```
Mi token expira después de 1 hora pero la app se queda en loading infinito.

Síntomas:
- Login exitoso
- Después de 1 hora, requests a /auth/me fallan con 401
- Frontend no redirige a login
- No hay mensajes de error

Código del response interceptor:
[pegar código]

¿Cómo debería manejar token expirado?
```

**La IA sugerirá**:
1. Verificar que el response interceptor detecta 401
2. Implementar `removeToken()` en el interceptor
3. Agregar redirección a `/login`
4. Opcional: Implementar refresh token pattern
5. Mostrar mensaje al usuario ("Sesión expirada")

#### Prompt: Infinite loop en AuthContext

```
Mi AuthContext causa un loop infinito:

useEffect(() => {
  const checkAuth = async () => {
    const user = await authService.getCurrentUser();
    setUser(user);
  };
  checkAuth();
}, [user]);  // ← Array de dependencias

¿Por qué se ejecuta infinitamente? Cómo arreglarlo?
```

**La IA explicará**:
- Problema: `user` en array de dependencias
- Causa: `setUser(user)` cambia `user` → re-ejecuta effect → loop
- Solución: Array vacío `[]` (ejecutar solo al montar)
- Explicación detallada del ciclo de vida

### 3. Security Review con IA

#### Prompt para auditoría de seguridad

```
Audita la seguridad de este sistema de autenticación:

Backend:
[pegar código de api.py, seguridad_jwt.py, servicio_usuarios.py]

Frontend:
[pegar código de auth.service.ts, AuthContext.tsx]

Busca vulnerabilidades en:
1. Almacenamiento de tokens (XSS, CSRF)
2. Expiración de tokens
3. Hashing de passwords
4. Validación de inputs
5. CORS configuration
6. Exposición de información sensible
7. Rate limiting en login/register

Para cada vulnerabilidad:
- Severidad (Critical/High/Medium/Low)
- Explicación del riesgo
- Código vulnerable
- Solución con código corregido
```

**La IA identificará**:
1. **localStorage vs cookies**: Analizar trade-offs (XSS vs CSRF)
2. **JWT secret hardcodeado**: Debe venir de env vars
3. **Password mínimo 8 caracteres**: Poco seguro (recomendar 12+)
4. **Sin rate limiting**: Vulnerable a brute force
5. **CORS demasiado permisivo**: Especificar origins exactos
6. **Token en query params**: Nunca (siempre en headers)

#### Prompt: ¿localStorage o cookies para JWT?

```
Debato entre almacenar JWT en localStorage vs httpOnly cookies.

Mi app:
- SPA React en dominio.com
- API FastAPI en api.dominio.com
- No planeo hacer SSR

Pros/cons de cada opción:
- localStorage + Authorization header
- httpOnly cookies

¿Cuál es más seguro? ¿Qué recomiendas y por qué?
```

**La IA explicará**:
- **localStorage**: Vulnerable a XSS, pero simple para SPAs
- **httpOnly cookies**: Protege contra XSS, pero requiere configuración CORS y CSRF tokens
- Recomendación: Depende del contexto
  - **Producción crítica**: httpOnly cookies + SameSite + CSRF
  - **Apps internas**: localStorage + sanitización XSS
- Trade-offs detallados con diagramas

### 4. Testing Avanzado de Autenticación

#### Prompt para tests completos

```
Genera tests completos para esta API de autenticación:

Endpoints:
- POST /auth/register
- POST /auth/login
- GET /auth/me

Casos a cubrir:
- Registro exitoso (201)
- Registro con email duplicado (409)
- Registro con password corta (422)
- Registro con email inválido (422)
- Login exitoso (200)
- Login con credenciales incorrectas (401)
- Login con usuario inexistente (401)
- /auth/me con token válido (200)
- /auth/me sin token (401)
- /auth/me con token inválido (401)
- /auth/me con token expirado (401)
- Password hasheada nunca se devuelve en responses

Usa pytest + TestClient + fixtures.
```

**La IA generará**:
1. Fixture para limpiar repositorio entre tests
2. Tests parametrizados para validación
3. Helpers para crear usuarios de prueba
4. Assertions detalladas (status, body, headers)
5. Tests de edge cases (token sin "Bearer", header vacío)

#### Prompt para tests de frontend

```
Genera tests para el AuthContext y componentes de auth:

Componentes:
- AuthContext
- LoginForm
- RegisterForm
- ProtectedRoute

Casos:
- AuthContext verifica sesión al montar
- login() actualiza estado correctamente
- logout() limpia token y usuario
- LoginForm envía datos correctos
- LoginForm muestra errores de validación
- RegisterForm valida password confirmation
- ProtectedRoute redirige si no hay auth
- ProtectedRoute muestra loading mientras verifica

Usa React Testing Library + MSW para mock de API.
```

### 5. Implementación de Refresh Tokens

#### Prompt para agregar refresh tokens

```
Mejora este sistema de auth para usar refresh tokens:

Sistema actual:
- Access token (1 hora) en localStorage
- Sin refresh token

Sistema deseado:
- Access token (15 minutos) en memoria
- Refresh token (7 días) en httpOnly cookie
- Auto-refresh cuando access token expira
- Endpoint /auth/refresh para renovar access token
- Logout invalida refresh token

Backend: FastAPI
Frontend: React + Axios

Muestra:
1. Cambios en backend (nuevos endpoints, models)
2. Cambios en frontend (axios interceptor mejorado)
3. Cómo manejar refresh token en cookies
4. Qué pasa si refresh token también expira
5. Tests para el nuevo flujo
```

**La IA diseñará**:
1. Modelo `RefreshToken` en backend
2. Endpoint `POST /auth/refresh`
3. Interceptor de Axios que:
   - Detecta 401 en access token
   - Llama a `/auth/refresh` automáticamente
   - Reintenta request original con nuevo token
   - Si refresh falla → logout
4. Almacenamiento: Access token en memoria, refresh en cookie
5. Flujo completo con diagramas

### 6. Integración con Agentes Educacionales

Para esta clase, usa los siguientes agentes (desde `.claude/agents/educational/`):

#### 1. FastAPI Design Coach

Revisa diseño de endpoints de auth:

```bash
"Revisa backend/api/api.py con FastAPI Design Coach"
```

**Detecta**:
- Endpoints RESTful correctos (/auth/register vs /register-user)
- HTTP status codes apropiados (201 vs 200 en registro)
- Uso correcto de dependency injection
- Validación de Pydantic completa
- Error handling apropiado (HTTPException con detail)

#### 2. API Design Reviewer

Valida diseño REST y seguridad:

```bash
"Revisa el sistema de auth con API Design Reviewer"
```

**Verifica**:
- JWT en Authorization header (no en query params o body)
- Responses consistentes (siempre AuthResponse en login/register)
- Error messages no exponen info sensible
- CORS configurado correctamente
- OpenAPI docs documentan esquemas de seguridad

#### 3. React Integration Coach

Optimiza patrones de React:

```bash
"Revisa frontend con React Integration Coach"
```

**Identifica**:
- AuthContext usa useEffect correctamente (no loops)
- Forms usan React Hook Form sin re-renders innecesarios
- Estado se actualiza inmutablemente
- Tipos TypeScript correctos en Context
- Manejo de loading/error states

### 7. Mejores Prácticas de Seguridad con IA

#### Prompt: Hardening de autenticación

```
Mi sistema de auth funciona pero quiero hacerlo production-ready.

Mejoras de seguridad que quiero implementar:
1. Rate limiting en /auth/login y /auth/register
2. Email verification después de registro
3. Password strength meter en frontend
4. Logout en múltiples dispositivos
5. Logging de intentos de login fallidos
6. Two-factor authentication (2FA)

¿Cómo implementar cada una? Prioriza por impacto vs esfuerzo.
```

**La IA priorizará**:

**Alta prioridad (Quick wins)**:
1. **Rate limiting**: 5 líneas con slowapi
2. **Password strength**: Librería zxcvbn en frontend
3. **Logging**: Agregar logger a intentos fallidos

**Media prioridad**:
4. **Email verification**: Token en email + endpoint /auth/verify
5. **Logout multi-device**: Almacenar tokens activos en DB

**Baja prioridad (Complejo)**:
6. **2FA**: Requiere TOTP, QR codes, backup codes

### 8. Migración de Autenticación Básica a JWT

#### Prompt para migración

```
Tengo una app con autenticación básica (usuario/password en cada request).

Sistema actual:
- Cada request envía username + password en headers
- Backend valida en cada request (consulta a DB)
- Sin sesiones, sin tokens

Quiero migrar a JWT.

Guíame paso a paso:
1. Qué cambiar en backend (endpoints, validación)
2. Qué cambiar en frontend (axios, almacenamiento)
3. Cómo migrar usuarios existentes
4. Cómo hacer la migración sin downtime
5. Cómo testear que funciona antes de deploy

Incluye código de migración y scripts.
```

### 9. Generación de Documentación con IA

#### Prompt para documentar API de auth

```
Genera documentación completa para esta API de autenticación:

Endpoints:
[pegar código de api.py]

Incluye:
- Descripción de cada endpoint
- Request body examples (JSON)
- Response examples (success + errors)
- Status codes posibles
- Headers requeridos
- Diagramas de secuencia para flujos:
  * Registro + login + acceso a recurso protegido
  * Login fallido
  * Token expirado
- Ejemplos de cURL
- Ejemplos de uso con Axios
- Guía de troubleshooting

Formato: Markdown con bloques de código resaltados.
```

### 10. Prompts para Conceptos Avanzados

#### Entender JWT profundamente

```
Explica JWT en profundidad:

1. ¿Cómo funciona la firma HMAC?
   - ¿Qué es HMAC-SHA256?
   - ¿Por qué no se puede falsificar un JWT?
   - ¿Qué pasa si cambio el payload?

2. ¿Por qué JWT es stateless?
   - Ventajas vs sessions con cookies
   - Desventajas (no se puede invalidar)
   - ¿Cuándo usar JWT y cuándo sessions?

3. ¿Cómo manejar logout con JWT?
   - Problema: JWT no se puede invalidar
   - Soluciones: Blacklist, short expiration, refresh tokens

4. ¿Es seguro poner info sensible en payload?
   - ¿Se puede leer el payload sin secret?
   - ¿Qué es "firma" vs "encriptación"?

Usa analogías del mundo real y diagramas.
```

#### Entender Axios Interceptors

```
Explica cómo funcionan los interceptors de Axios:

1. ¿Qué es un interceptor?
   - Request interceptor vs response interceptor
   - ¿Cuándo se ejecutan?
   - ¿Se pueden encadenar múltiples?

2. ¿Qué puedo hacer en un interceptor?
   - Modificar headers
   - Transformar request/response
   - Manejar errores globalmente
   - Retry automático

3. Casos de uso comunes:
   - Agregar token JWT
   - Logging de requests
   - Refresh token automático
   - Mostrar/ocultar loading spinner global

Incluye código de ejemplo para cada caso.
```

---

## Diferencias con Clase 2

| Aspecto | Clase 2 (CRUD) | Clase 3 (Auth) |
|---------|---------------|----------------|
| **Enfoque** | Data management | User authentication |
| **Backend** | Tareas CRUD | Registro, login, JWT |
| **Frontend** | React Query | Auth Context + React Router |
| **Estado Global** | No (local state) | Sí (AuthContext) |
| **Seguridad** | Sin auth | JWT + bcrypt |
| **Routing** | Una sola página | Multi-página con protected routes |
| **Axios** | Sin interceptors | Interceptors para JWT |
| **Formularios** | RHF + Zod (tareas) | RHF + Zod (login/register) |
| **Persistencia** | Sin localStorage | Token en localStorage |

---

## Ejercicios y Mejoras

### 🎯 Ejercicios Guiados (con IA)

#### Ejercicio 1: Agregar Email Verification

**Objetivo**: Usuarios deben verificar email antes de acceder.

**Prompt sugerido**:
```
Implementa email verification en este sistema:

1. Después de registro, enviar email con token de verificación
2. Usuario hace click en link: /auth/verify?token=...
3. Backend verifica token y activa cuenta
4. Login solo permitido si cuenta está verificada

Backend: FastAPI + enviar email (usar librería python-email)
Frontend: Página /verify que muestra estado

Incluye tests para el flujo completo.
```

#### Ejercicio 2: Implementar "Remember Me"

**Objetivo**: Checkbox "Recordarme" en login que extiende sesión.

**Prompt sugerido**:
```
Agrega funcionalidad "Remember Me":

- Checkbox en LoginForm
- Si checked: Token con expiración de 30 días
- Si no checked: Token con expiración de 1 hora
- Backend ajusta exp en JWT según parámetro

¿Cómo pasar el parámetro del frontend al backend?
¿Cómo ajustar crear_token() para aceptar exp custom?
```

#### Ejercicio 3: Agregar Roles y Permisos

**Objetivo**: Admin vs User roles con endpoints específicos.

**Prompt sugerido**:
```
Implementa sistema de roles:

Roles:
- "user": Acceso básico
- "admin": Acceso completo + endpoint GET /admin/users

Backend:
- Agregar campo "role" en User model
- Incluir "role" en JWT claims
- Crear dependency verificar_admin() que rechaza si no es admin
- Endpoint GET /admin/users (solo admin)

Frontend:
- Mostrar menú Admin solo si user.role === "admin"
- Manejar 403 Forbidden si user intenta acceder a ruta admin

Tests para verificar control de acceso.
```

### 🚀 Mejoras Avanzadas

#### 1. OAuth 2.0 con Google/GitHub

**Prompt**:
```
Agrega login con Google/GitHub usando OAuth 2.0:

- Botones "Login with Google" y "Login with GitHub"
- Flujo OAuth completo (redirect, callback, exchange code)
- Backend crea usuario si no existe
- Frontend recibe JWT después de OAuth
- Integración con AuthContext existente

Usa python-oauth2 en backend y react-oauth en frontend.
Muestra código completo con manejo de errores.
```

#### 2. Refresh Tokens con Rotación

**Prompt**:
```
Implementa refresh tokens con rotación:

- Access token: 15 minutos
- Refresh token: 7 días
- Cada refresh genera NUEVO refresh token (rotación)
- Token viejo se invalida (previene replay attacks)
- Si refresh token se roba y se usa, invalidar TODOS los tokens del usuario

Backend: Almacenar refresh tokens en DB (PostgreSQL)
Frontend: Axios interceptor maneja refresh automático

¿Cómo detectar token robado?
¿Cómo forzar re-login si se detecta ataque?
```

#### 3. Two-Factor Authentication (2FA)

**Prompt**:
```
Implementa 2FA con TOTP (Google Authenticator):

Flujo:
1. Usuario activa 2FA en settings
2. Backend genera secret, muestra QR code
3. Usuario escanea con Google Authenticator
4. Login requiere password + código 6 dígitos
5. Backend verifica código TOTP

Backend: Usar pyotp
Frontend: Input para código 6 dígitos, mostrar QR

Incluye:
- Backup codes (10 códigos de un solo uso)
- Recovery si pierde teléfono
- Tests de TOTP validation
```

#### 4. Rate Limiting y Account Lockout

**Prompt**:
```
Agrega protección contra brute force:

Rate limiting:
- Máximo 5 intentos de login por IP en 15 minutos
- Máximo 3 registros por IP en 1 hora
- Response: 429 Too Many Requests

Account lockout:
- Después de 5 intentos fallidos: bloquear cuenta 30 minutos
- Email de notificación al usuario
- Opción de desbloquear con link en email

Backend: Usar slowapi + Redis para rate limiting
Frontend: Mostrar mensaje "Cuenta bloqueada, revisa tu email"
```

#### 5. Session Management (Logout de Todos los Dispositivos)

**Prompt**:
```
Implementa gestión de sesiones:

Página /settings/sessions:
- Lista de sesiones activas (IP, navegador, última actividad)
- Botón "Cerrar sesión en todos los dispositivos"
- Botón "Cerrar esta sesión" individual

Backend:
- Almacenar tokens activos en Redis (key: token, value: session info)
- Endpoint DELETE /auth/sessions (invalida todos los tokens del user)
- Endpoint DELETE /auth/sessions/:id (invalida un token específico)

Frontend:
- Componente SessionsList con tabla
- Confirmación antes de logout masivo

¿Cómo invalidar JWTs si son stateless?
→ Solución: Blacklist en Redis con TTL = exp del token
```

---

## 📚 Recursos Adicionales

### Documentación Oficial

- [JWT.io](https://jwt.io/) - Debugger y guía de JWT
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/) - OAuth2 y JWT en FastAPI
- [React Router v6](https://reactrouter.com/) - Protected routes y navigation
- [Axios Docs](https://axios-http.com/docs/interceptors) - Interceptors guide

### Tutoriales Recomendados

- **Auth0 Blog**: JWT Best Practices
- **OWASP**: Authentication Cheat Sheet
- **Web.dev**: SameSite cookies explained
- **TkDodo's Blog**: React Query + Authentication

### Herramientas de Desarrollo

- **JWT Debugger** (jwt.io) - Decodificar y verificar JWTs
- **Postman** - Probar endpoints con Authorization headers
- **React DevTools** - Inspeccionar AuthContext state
- **Axios DevTools** - Ver interceptors en acción

### Seguridad

- **Have I Been Pwned API** - Verificar si passwords están comprometidas
- **zxcvbn** - Password strength meter
- **python-jose** - Implementación JWT en Python
- **bcrypt** - Hashing de passwords seguro

---

## 🎓 Aprendizajes Clave de esta Clase

1. ✅ **JWT**: Autenticación stateless con tokens firmados
2. ✅ **Bcrypt**: Hashing seguro de passwords
3. ✅ **Auth Context**: Estado global de autenticación en React
4. ✅ **Protected Routes**: Control de acceso basado en auth
5. ✅ **Axios Interceptors**: Headers automáticos y manejo de 401
6. ✅ **React Router**: Navegación con redirecciones
7. ✅ **Persistencia**: localStorage para sesiones
8. ✅ **IA como Security Architect**: Auditorías, debugging, best practices

---

## 🤖 Conclusión: Autenticación Production-Ready con IA

Esta clase demuestra:

- **JWT** simplifica autenticación sin sesiones en servidor
- **Auth Context** centraliza estado y evita prop drilling
- **Axios Interceptors** eliminan código repetitivo
- **Protected Routes** controlan acceso de forma declarativa
- **IA** acelera implementación y detecta vulnerabilidades
- **Agentes educacionales** enseñan security best practices

### ¿Qué sigue?

**Módulo 5, Clase 4**: Integración con base de datos real (PostgreSQL), migraciones con Alembic, y persistencia de usuarios y tareas.

---

## 📊 Comparación de Código: Sin Auth vs Con Auth

### Endpoint Protegido

**Sin Auth** (inseguro):
```python
@app.get("/usuarios/{user_id}")
async def obtener_usuario(user_id: str):
    # ❌ Cualquiera puede acceder
    return servicio.obtener_usuario(user_id)
```

**Con Auth** (seguro):
```python
@app.get("/usuarios/{user_id}")
async def obtener_usuario(
    user_id: str,
    payload: dict = Depends(verificar_jwt)  # ✅ Requiere JWT válido
):
    # Solo accesible con token válido
    return servicio.obtener_usuario(user_id)
```

### Request con Token

**Sin Interceptor** (repetitivo):
```typescript
// ❌ Repetir en cada request
const response = await axios.get("/auth/me", {
  headers: { Authorization: `Bearer ${token}` }
});
```

**Con Interceptor** (automático):
```typescript
// ✅ Token se agrega automáticamente
const response = await axiosInstance.get("/auth/me");
```

**Reducción de código**: ~80% menos en requests autenticadas.

---

**¿Tienes dudas?** Usa los agentes educacionales o pregunta directamente:

```
Explica [concepto] de autenticación JWT usando analogías y ejemplos de código.
```
