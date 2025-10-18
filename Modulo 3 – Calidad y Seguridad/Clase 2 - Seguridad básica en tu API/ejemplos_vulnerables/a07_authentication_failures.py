# ejemplos_vulnerables/a07_authentication_failures.py
"""
CÓDIGO VULNERABLE - A07: Authentication Failures

Este código fue generado por IA sin contexto de seguridad.
Demuestra vulnerabilidades típicas de autenticación.

VULNERABILIDADES:
1. API Keys débiles (cortas, predecibles)
2. Comparación insegura (vulnerable a timing attacks)
3. API Keys almacenadas en texto plano
4. No usa secrets module
5. Tokens sin expiración
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from typing import Optional

app = FastAPI()

# ========================================
# VULNERABLE 1: API Keys débiles
# ========================================

# ❌ API Keys demasiado cortas y predecibles
USUARIOS_DB = {
    "user1": "abc123",  # ❌ Solo 6 caracteres
    "user2": "pass456",  # ❌ Predecible
    "admin": "admin",  # ❌ Palabra común
}


def obtener_api_key_del_header(x_api_key: Optional[str] = Header(None)) -> str:
    """Extrae API Key del header"""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API Key requerida")
    return x_api_key


# ========================================
# VULNERABLE 2: Comparación insegura (Timing Attack)
# ========================================


def verificar_api_key_inseguro(api_key: str = Depends(obtener_api_key_del_header)) -> str:
    """
    VULNERABILIDAD CRÍTICA: Usa == en vez de secrets.compare_digest

    Escenario de ataque (Timing Attack):
    1. Atacante prueba "a" -> falla en 0.001ms
    2. Atacante prueba "b" -> falla en 0.001ms
    3. Atacante prueba "abc" -> falla en 0.003ms (más tiempo = primer carácter correcto!)
    4. Atacante prueba "abc1" -> falla en 0.004ms
    5. Continúa hasta descubrir "abc123"

    El operador == compara carácter por carácter y retorna inmediatamente al
    encontrar diferencia. Esto revela información sobre la clave correcta.
    """
    for usuario, clave_valida in USUARIOS_DB.items():
        # ❌ VULNERABLE a timing attacks
        if api_key == clave_valida:
            return usuario

    raise HTTPException(status_code=401, detail="API Key inválida")


# ========================================
# VULNERABLE 3: Almacenamiento inseguro
# ========================================

# ❌ API Keys almacenadas en texto plano
# Si la base de datos se filtra, todas las claves quedan expuestas

# ❌ Generación débil de API Keys


def generar_api_key_debil():
    """
    VULNERABILIDAD: Usa random en vez de secrets

    random NO es criptográficamente seguro.
    Un atacante puede predecir las claves generadas.
    """
    import random
    import string

    # ❌ random.choice NO es seguro para criptografía
    return ''.join(random.choice(string.ascii_letters) for _ in range(8))


# ========================================
# VULNERABLE 4: Sin rotación de claves
# ========================================

@app.post("/usuarios/crear")
def crear_usuario_inseguro(username: str):
    """
    VULNERABILIDAD: API Keys sin expiración ni rotación.

    - Keys nunca expiran ❌
    - No hay mecanismo de rotación ❌
    - Si se compromete, es válida para siempre ❌
    """
    api_key = generar_api_key_debil()
    USUARIOS_DB[username] = api_key

    return {
        "username": username,
        "api_key": api_key,  # ❌ Retorna clave en texto plano
        "warning": "Esta API Key nunca expira"
    }


# ========================================
# VULNERABLE 5: Sin rate limiting
# ========================================

@app.get("/datos-sensibles")
def obtener_datos(usuario: str = Depends(verificar_api_key_inseguro)):
    """
    VULNERABILIDAD: Sin rate limiting, permite brute force.

    Escenario de ataque:
    - Atacante hace 1,000,000 de intentos/segundo
    - Eventualmente descubre una API Key válida ❌
    - No hay límite de intentos ❌
    """
    return {"datos": "Información confidencial", "usuario": usuario}


# ========================================
# CÓDIGO CORREGIDO (para comparación)
# ========================================

"""
CORRECCIÓN 1: Usar secrets.token_urlsafe para generar API Keys

import secrets

def generar_api_key_seguro():
    # ✅ Genera 32 bytes aleatorios (256 bits)
    # ✅ Criptográficamente seguro
    return secrets.token_urlsafe(32)  # Genera ~43 caracteres


CORRECCIÓN 2: Almacenar API Keys hasheadas

import hashlib

USUARIOS_DB_SEGURO = {
    "user1": {
        "api_key_hash": hashlib.sha256("clave_real".encode()).hexdigest(),
        "username": "user1"
    }
}


CORRECCIÓN 3: Usar secrets.compare_digest (timing-safe)

import secrets

def verificar_api_key_seguro(api_key: str = Depends(obtener_api_key_del_header)) -> str:
    for usuario, datos in USUARIOS_DB_SEGURO.items():
        api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()

        # ✅ Timing-safe comparison
        # ✅ Siempre toma el mismo tiempo, independiente de si coincide o no
        if secrets.compare_digest(api_key_hash, datos["api_key_hash"]):
            return usuario

    raise HTTPException(status_code=401, detail="API Key inválida")


CORRECCIÓN 4: Rate limiting

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

@app.get(
    "/datos-sensibles",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))]  # ✅ 10 requests/min
)
def obtener_datos_seguro(usuario: str = Depends(verificar_api_key_seguro)):
    return {"datos": "Información confidencial", "usuario": usuario}


CORRECCIÓN 5: API Keys con expiración

from datetime import datetime, timedelta

USUARIOS_DB_CON_EXPIRACION = {
    "user1": {
        "api_key_hash": "hash_de_la_clave",
        "expires_at": datetime.now() + timedelta(days=30),  # ✅ Expira en 30 días
        "created_at": datetime.now()
    }
}

def verificar_api_key_con_expiracion(api_key: str = Depends(obtener_api_key_del_header)) -> str:
    for usuario, datos in USUARIOS_DB_CON_EXPIRACION.items():
        # ✅ Verificar expiración
        if datetime.now() > datos["expires_at"]:
            raise HTTPException(status_code=401, detail="API Key expirada")

        api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()

        if secrets.compare_digest(api_key_hash, datos["api_key_hash"]):
            return usuario

    raise HTTPException(status_code=401, detail="API Key inválida")


CORRECCIÓN 6: Logging de intentos fallidos

import logging

logger = logging.getLogger(__name__)

def verificar_con_logging(api_key: str = Depends(obtener_api_key_del_header)) -> str:
    for usuario, datos in USUARIOS_DB_SEGURO.items():
        api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()

        if secrets.compare_digest(api_key_hash, datos["api_key_hash"]):
            return usuario

    # ✅ Registrar intento fallido
    logger.warning(
        f"Intento de autenticación fallido",
        extra={"event": "auth_failed", "api_key_prefix": api_key[:4]}
    )

    raise HTTPException(status_code=401, detail="API Key inválida")
"""

# ========================================
# EJERCICIO
# ========================================

"""
1. Identifica las 6 vulnerabilidades de autenticación en este código
2. Explica por qué cada una es peligrosa y cómo se explota
3. Implementa las correcciones:
   - Generar API Keys con secrets.token_urlsafe(32)
   - Almacenar hasheadas con SHA-256
   - Comparar con secrets.compare_digest
   - Agregar expiración a las claves
   - Implementar rate limiting
   - Logging de intentos fallidos
4. Escribe tests:
   - test_api_key_debil_rechazada()
   - test_timing_attack_no_funciona()
   - test_api_key_expirada_rechazada()
   - test_rate_limiting_bloquea_brute_force()
"""
