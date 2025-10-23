# api/api.py
"""
API REST con autenticación JWT completa.

Endpoints:
- POST /auth/register: Registro de nuevos usuarios
- POST /auth/login: Login y obtención de token JWT
- GET /auth/me: Obtener datos del usuario autenticado (protegido)
- GET /health: Health check para monitoring
"""
import os
import logging
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.modelos import RegisterRequest, LoginRequest, AuthResponse, UserResponse
from api.servicio_usuarios import ServicioUsuarios
from api.dependencias import obtener_servicio_usuarios
from api.seguridad_jwt import verificar_jwt

# Configurar logging para producción
logging.basicConfig(
    level=logging.INFO if os.getenv("MODE") == "production" else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def validate_environment():
    """Valida que todas las environment variables requeridas estén presentes."""
    required_vars = ["JWT_SECRET"]
    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        error_msg = (
            f"❌ Missing required environment variables: {', '.join(missing)}\n"
            "Check your Railway/Render dashboard for environment configuration."
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.info("✅ All required environment variables are set")


# Validar environment al startup
validate_environment()

app = FastAPI(
    title="API con Autenticación JWT",
    description="API REST Full-Stack con autenticación JWT, registro, login y rutas protegidas",
    version="1.0.0",
)

# CORS configurado dinámicamente para producción
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
ALLOWED_ORIGINS = [FRONTEND_URL]

# En desarrollo, agregar localhost alternativas
if os.getenv("MODE") != "production":
    ALLOWED_ORIGINS.extend(["http://localhost:5173", "http://127.0.0.1:5173"])

logger.info(f"CORS configured for origins: {ALLOWED_ORIGINS}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """
    Health check endpoint para Railway/Render monitoring.

    Returns:
        Status, timestamp y versión de la API
    """
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "environment": os.getenv("MODE", "development")
    }


@app.post("/auth/register", response_model=AuthResponse, status_code=201)
async def registrar(
    request: RegisterRequest, servicio: ServicioUsuarios = Depends(obtener_servicio_usuarios)
):
    """
    Registra un nuevo usuario y devuelve un token JWT.

    - **email**: Email único del usuario
    - **password**: Contraseña (mínimo 8 caracteres)
    - **nombre**: Nombre del usuario

    Returns:
        AuthResponse con token JWT y datos del usuario
    """
    try:
        return servicio.registrar(request)
    except ValueError as e:
        # Email ya registrado
        raise HTTPException(status_code=409, detail=str(e))


@app.post("/auth/login", response_model=AuthResponse)
async def login(request: LoginRequest, servicio: ServicioUsuarios = Depends(obtener_servicio_usuarios)):
    """
    Autentica un usuario existente y devuelve un token JWT.

    - **email**: Email del usuario
    - **password**: Contraseña

    Returns:
        AuthResponse con token JWT y datos del usuario
    """
    try:
        return servicio.login(request)
    except ValueError as e:
        # Credenciales inválidas
        raise HTTPException(status_code=401, detail=str(e))


@app.get("/auth/me", response_model=UserResponse)
async def obtener_usuario_actual(
    payload: dict = Depends(verificar_jwt), servicio: ServicioUsuarios = Depends(obtener_servicio_usuarios)
):
    """
    Obtiene los datos del usuario autenticado.

    **Requiere autenticación**: Header `Authorization: Bearer <token>`

    Returns:
        UserResponse con los datos del usuario
    """
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario = servicio.obtener_usuario_actual(user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario


# Ejemplo de endpoint protegido adicional
@app.get("/protected/dashboard")
async def dashboard_protegido(payload: dict = Depends(verificar_jwt)):
    """
    Endpoint protegido de ejemplo.

    **Requiere autenticación**: Header `Authorization: Bearer <token>`

    Returns:
        Datos del dashboard personalizados por usuario
    """
    return {
        "message": f"Bienvenido {payload.get('nombre')}!",
        "user_id": payload.get("sub"),
        "email": payload.get("email"),
        "dashboard_data": {"tasks_count": 5, "pending_tasks": 3, "completed_tasks": 2},
    }
