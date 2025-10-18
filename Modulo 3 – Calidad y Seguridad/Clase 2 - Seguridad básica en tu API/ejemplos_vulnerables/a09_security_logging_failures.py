# ejemplos_vulnerables/a09_security_logging_failures.py
"""
CÓDIGO VULNERABLE - A09: Security Logging and Monitoring Failures

Este código fue generado por IA sin contexto de seguridad.
Demuestra vulnerabilidades de logging y monitoreo.

VULNERABILIDADES:
1. No registra eventos de seguridad (autenticación, autorización)
2. No usa logging estructurado
3. Logs no van a sistema centralizado (Sentry, ELK)
4. No registra cambios críticos (CRUD)
5. Sin alertas automáticas ante actividad sospechosa
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

app = FastAPI()

# Base de datos simulada
tareas_db = {}
usuarios_db = {"user1": "api_key_123"}


class Tarea(BaseModel):
    id: int
    nombre: str
    user_id: int


def obtener_usuario_actual() -> int:
    """Simula autenticación"""
    return 1


# ========================================
# VULNERABLE 1: No registra autenticación fallida
# ========================================

def verificar_api_key(api_key: str) -> int:
    """
    VULNERABILIDAD: No registra intentos fallidos de autenticación.

    PROBLEMA:
    - Atacante puede hacer 1,000,000 de intentos
    - No hay registro de ataques de fuerza bruta ❌
    - Imposible detectar intentos de intrusión ❌
    - No se puede investigar incidentes de seguridad ❌
    """
    for user_id, key in usuarios_db.items():
        if api_key == key:
            return int(user_id.replace("user", ""))

    # ❌ NO REGISTRA intento fallido
    raise HTTPException(status_code=401, detail="API Key inválida")


# ========================================
# VULNERABLE 2: No registra accesos no autorizados (403)
# ========================================

@app.get("/tareas/{tarea_id}")
def obtener_tarea(tarea_id: int, usuario_actual: int = Depends(obtener_usuario_actual)):
    """
    VULNERABILIDAD: No registra intentos de acceso no autorizados.

    ESCENARIO:
    - Usuario 2 intenta acceder a tarea de Usuario 1
    - Sistema retorna 403
    - NO SE REGISTRA el intento ❌
    - Imposible detectar enumeración de recursos ❌
    """
    tarea = tareas_db.get(tarea_id)

    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    if tarea.user_id != usuario_actual:
        # ❌ NO REGISTRA intento no autorizado
        raise HTTPException(status_code=403, detail="Acceso denegado")

    return tarea


# ========================================
# VULNERABLE 3: No registra eventos críticos (CRUD)
# ========================================

@app.post("/tareas")
def crear_tarea(nombre: str, usuario_actual: int = Depends(obtener_usuario_actual)):
    """
    VULNERABILIDAD: No registra creación de recursos.

    PROBLEMA:
    - No hay audit trail ❌
    - Imposible saber quién creó qué ❌
    - Sin evidencia forense ante incidentes ❌
    """
    tarea_id = len(tareas_db) + 1
    tarea = Tarea(id=tarea_id, nombre=nombre, user_id=usuario_actual)
    tareas_db[tarea_id] = tarea

    # ❌ NO REGISTRA creación de tarea
    return tarea


@app.delete("/tareas/{tarea_id}")
def eliminar_tarea(tarea_id: int, usuario_actual: int = Depends(obtener_usuario_actual)):
    """
    VULNERABILIDAD CRÍTICA: No registra eliminaciones.

    PROBLEMA:
    - Usuario elimina datos importantes
    - NO HAY REGISTRO de quién, cuándo, qué ❌
    - Imposible investigar eliminaciones accidentales/maliciosas ❌
    - Violación de compliance (GDPR, SOX, HIPAA) ❌
    """
    tarea = tareas_db.get(tarea_id)

    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    if tarea.user_id != usuario_actual:
        raise HTTPException(status_code=403, detail="Acceso denegado")

    # ❌ NO REGISTRA eliminación (evento crítico)
    del tareas_db[tarea_id]
    return {"message": "Tarea eliminada"}


# ========================================
# VULNERABLE 4: Logging no estructurado
# ========================================

def endpoint_vulnerable_con_print():
    """
    VULNERABILIDAD: Usa print() en vez de logging module.

    PROBLEMA:
    - print() va a stdout, no a logs centralizados ❌
    - Sin niveles de severidad (INFO, WARNING, ERROR) ❌
    - Sin contexto estructurado ❌
    - Imposible filtrar/buscar logs ❌
    """
    print("Usuario accedió al endpoint")  # ❌ NO estructurado


# ========================================
# VULNERABLE 5: Sin integración con Sentry/ELK
# ========================================

@app.get("/endpoint-que-falla")
def endpoint_sin_monitoreo():
    """
    VULNERABILIDAD: Excepciones no se reportan a Sentry.

    PROBLEMA:
    - Errores en producción pasan desapercibidos ❌
    - No se recopilan stack traces ❌
    - Imposible detectar problemas proactivamente ❌
    """
    try:
        resultado = 1 / 0  # Error intencional
    except ZeroDivisionError:
        # ❌ NO reporta a Sentry
        raise HTTPException(status_code=500, detail="Error interno")


# ========================================
# CÓDIGO CORREGIDO (para comparación)
# ========================================

"""
CORRECCIÓN 1: Logging de autenticación fallida

import logging

logger = logging.getLogger(__name__)

def verificar_api_key_seguro(api_key: str) -> int:
    for user_id, key in usuarios_db.items():
        if api_key == key:
            # ✅ Registrar autenticación exitosa
            logger.info(
                f"Autenticación exitosa para usuario {user_id}",
                extra={"event": "auth_success", "user_id": user_id}
            )
            return int(user_id.replace("user", ""))

    # ✅ Registrar intento fallido
    logger.warning(
        "Intento de autenticación fallido",
        extra={
            "event": "auth_failed",
            "api_key_prefix": api_key[:4],  # Solo primeros 4 caracteres
            "ip": "192.168.1.1"  # En producción, obtener IP real
        }
    )

    raise HTTPException(status_code=401, detail="API Key inválida")


CORRECCIÓN 2: Logging de accesos no autorizados (403)

@app.get("/tareas/{tarea_id}")
def obtener_tarea_seguro(tarea_id: int, usuario_actual: int = Depends(obtener_usuario_actual)):
    tarea = tareas_db.get(tarea_id)

    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    if tarea.user_id != usuario_actual:
        # ✅ Registrar intento no autorizado
        logger.warning(
            f"Intento no autorizado de acceder a tarea {tarea_id} por usuario {usuario_actual}",
            extra={
                "event": "unauthorized_access",
                "tarea_id": tarea_id,
                "user_id": usuario_actual,
                "resource_owner": tarea.user_id
            }
        )
        raise HTTPException(status_code=403, detail="Acceso denegado")

    return tarea


CORRECCIÓN 3: Logging de eventos críticos (CRUD)

@app.post("/tareas")
def crear_tarea_seguro(nombre: str, usuario_actual: int = Depends(obtener_usuario_actual)):
    tarea_id = len(tareas_db) + 1
    tarea = Tarea(id=tarea_id, nombre=nombre, user_id=usuario_actual)
    tareas_db[tarea_id] = tarea

    # ✅ Audit log de creación
    logger.info(
        f"Tarea {tarea_id} creada por usuario {usuario_actual}",
        extra={
            "event": "tarea_creada",
            "tarea_id": tarea_id,
            "user_id": usuario_actual,
            "tarea_nombre": nombre
        }
    )

    return tarea


@app.delete("/tareas/{tarea_id}")
def eliminar_tarea_seguro(tarea_id: int, usuario_actual: int = Depends(obtener_usuario_actual)):
    tarea = tareas_db.get(tarea_id)

    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    if tarea.user_id != usuario_actual:
        raise HTTPException(status_code=403, detail="Acceso denegado")

    # ✅ Audit log CRÍTICO de eliminación
    logger.warning(
        f"Tarea {tarea_id} eliminada por usuario {usuario_actual}",
        extra={
            "event": "tarea_eliminada",
            "tarea_id": tarea_id,
            "user_id": usuario_actual,
            "tarea_nombre": tarea.nombre,
            "timestamp": datetime.now().isoformat()
        }
    )

    del tareas_db[tarea_id]
    return {"message": "Tarea eliminada"}


CORRECCIÓN 4: Logging estructurado

import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }

        # Agregar campos extra
        if hasattr(record, "event"):
            log_data["event"] = record.event
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id

        return json.dumps(log_data)


# Configurar logger
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)


CORRECCIÓN 5: Integración con Sentry

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastAPIIntegration

# ✅ Configurar Sentry
sentry_sdk.init(
    dsn="https://tu_dsn@sentry.io/proyecto",
    integrations=[FastAPIIntegration()],
    traces_sample_rate=0.1,  # 10% de transacciones
    environment="production"
)

@app.get("/endpoint-con-monitoreo")
def endpoint_monitoreado():
    try:
        resultado = 1 / 0
    except ZeroDivisionError as e:
        # ✅ Sentry captura automáticamente la excepción
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail="Error interno")


CORRECCIÓN 6: Middleware de logging

from fastapi import Request
import time

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # ✅ Registrar request
    logger.info(
        f"{request.method} {request.url.path}",
        extra={
            "event": "http_request",
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host
        }
    )

    response = await call_next(request)

    # ✅ Registrar response con tiempo de procesamiento
    duration = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} - {response.status_code}",
        extra={
            "event": "http_response",
            "status_code": response.status_code,
            "duration_ms": round(duration * 1000, 2)
        }
    )

    return response
"""

# ========================================
# EJERCICIO
# ========================================

"""
1. Identifica las 5 vulnerabilidades de logging en este código
2. Explica por qué es crítico registrar eliminaciones y cambios
3. Implementa logging estructurado con Python logging
4. Configura Sentry para capturar errores en producción
5. Crea middleware para registrar todos los requests HTTP
6. Implementa alertas: si >10 intentos fallidos en 1 min, notificar
7. Escribe tests:
   - test_auth_fallida_se_registra()
   - test_acceso_no_autorizado_se_registra()
   - test_eliminacion_se_registra_en_audit_log()
   - test_sentry_captura_excepciones()
"""
