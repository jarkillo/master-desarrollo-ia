# api/sentry_config.py
"""Configuración avanzada de Sentry para observabilidad segura.

Este módulo implementa las mejores prácticas de seguridad para Sentry:
- Scrubbing automático de datos sensibles (passwords, tokens, PII)
- Sample rate adaptativo según ambiente
- Filtrado de eventos para reducir ruido
- Environment-aware configuration
"""
import os
import re

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

# Lista de campos sensibles que NUNCA deben enviarse a Sentry
SENSITIVE_FIELDS = [
    'password', 'secret', 'token', 'api_key', 'authorization',
    'credit_card', 'ssn', 'dni', 'access_token', 'refresh_token',
    'jwt_secret', 'database_url', 'private_key', 'cookie'
]


def scrub_sensitive_data(data: dict) -> dict:
    """Elimina campos sensibles de un diccionario antes de enviar a Sentry.

    Usa un enfoque de blocklist: cualquier clave que contenga patrones
    de SENSITIVE_FIELDS (case-insensitive, match parcial) se reemplaza
    con [REDACTED].

    Args:
        data: Diccionario que puede contener datos sensibles

    Returns:
        Diccionario con campos sensibles redactados

    Example:
        >>> data = {"username": "demo", "password": "secret123"}
        >>> scrubbed = scrub_sensitive_data(data)
        >>> scrubbed["password"]
        '[REDACTED]'
    """
    if not isinstance(data, dict):
        return data

    scrubbed = {}
    for key, value in data.items():
        key_lower = key.lower()

        # Verificar si la clave contiene algún patrón sensible
        is_sensitive = any(pattern in key_lower for pattern in SENSITIVE_FIELDS)

        if is_sensitive:
            scrubbed[key] = "[REDACTED]"
        elif isinstance(value, dict):
            scrubbed[key] = scrub_sensitive_data(value)  # Recursivo
        elif isinstance(value, list):
            scrubbed[key] = [
                scrub_sensitive_data(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            scrubbed[key] = value

    return scrubbed


def before_send(event: dict, hint: dict) -> dict | None:
    """Hook que procesa eventos antes de enviarlos a Sentry.

    Implementa múltiples capas de seguridad:
    1. Filtra headers sensibles (Authorization, API keys)
    2. Scrubbing del request body
    3. Previene envío de variables de entorno
    4. Redacta URL parameters sensibles
    5. Limita contexto de usuario a campos no-PII

    Args:
        event: Evento de Sentry a procesar
        hint: Información adicional del contexto

    Returns:
        El evento procesado (o None para descartarlo)

    Example:
        >>> event = {"request": {"headers": {"Authorization": "Bearer token"}}}
        >>> processed = before_send(event, {})
        >>> "Authorization" in processed["request"]["headers"]
        False
    """
    if 'request' in event:
        # ✅ HEADERS: Eliminar Authorization y headers sensibles
        if 'headers' in event['request']:
            headers = dict(event['request']['headers'])

            # Eliminar headers sensibles completamente
            sensitive_headers = ['authorization', 'x-api-key', 'cookie', 'x-csrf-token']
            for header in sensitive_headers:
                headers.pop(header, None)
                headers.pop(header.upper(), None)
                headers.pop(header.title(), None)

            event['request']['headers'] = headers

        # ✅ BODY: Scrubbing de campos sensibles en request data
        if 'data' in event['request']:
            event['request']['data'] = scrub_sensitive_data(event['request']['data'])

        # ✅ URL: Redactar query parameters sensibles
        if 'query_string' in event['request']:
            query = event['request']['query_string']
            # Ejemplo: ?token=abc123 -> ?token=[REDACTED]
            for field in SENSITIVE_FIELDS:
                query = re.sub(
                    f"{field}=[^&]*",
                    f"{field}=[REDACTED]",
                    query,
                    flags=re.IGNORECASE
                )
            event['request']['query_string'] = query

    # ✅ USER CONTEXT: Solo incluir información no-sensible
    if 'user' in event:
        # Mantener: user ID, username
        # Eliminar: email (PII), IP address (PII en EU)
        allowed_fields = {'id', 'username'}
        event['user'] = {k: v for k, v in event['user'].items() if k in allowed_fields}

    # ✅ CONTEXTS: Nunca enviar variables de entorno
    if 'contexts' in event:
        event['contexts'].pop('environment', None)

    return event


def configurar_sentry() -> None:
    """Inicializa Sentry con configuración adaptada al entorno.

    Características de seguridad:
    - Environment-aware sampling (100% dev, 10% prod)
    - Scrubbing automático de datos sensibles
    - Filtrado de PII por defecto
    - Release tracking para correlacionar errores con despliegues
    - Integración específica con FastAPI/Starlette

    Raises:
        No lanza excepciones si SENTRY_DSN no está configurado (degrada gracefully)

    Example:
        >>> # En tu api.py
        >>> from api.sentry_config import configurar_sentry
        >>> configurar_sentry()
        ✅ Sentry inicializado (environment=dev, sampling=1.0)
    """
    environment = os.getenv("MODE", "development")
    dsn = os.getenv("SENTRY_DSN")

    if not dsn:
        print("[WARNING] SENTRY_DSN no configurado, observabilidad deshabilitada")
        return

    # Sampling adaptativo por ambiente
    # Dev: 100% de traces (ver todo durante desarrollo)
    # Prod: 10% de traces (balance costo/visibilidad)
    traces_sample_rate = 1.0 if environment == "development" else 0.1

    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        release=os.getenv("VERSION", "dev"),

        # Integraciones específicas de FastAPI
        integrations=[
            FastApiIntegration(
                transaction_style="endpoint"  # Agrupar por endpoint, no por path completo
            ),
            StarletteIntegration(),
        ],

        # Sampling de trazas (performance monitoring)
        traces_sample_rate=traces_sample_rate,

        # Hook personalizado para scrubbing
        before_send=before_send,

        # Scrubbing de PII integrado (fallback, pero siempre implementar custom)
        send_default_pii=False,

        # Limitar breadcrumbs para reducir uso de memoria
        max_breadcrumbs=50,

        # Attach stack locals (útil para debugging, deshabilitar si hay info sensible)
        attach_stacktrace=True,

        # Server name (ayuda a identificar qué instancia falló)
        server_name=os.getenv("HOSTNAME", "unknown"),
    )

    print(f"[OK] Sentry inicializado (environment={environment}, sampling={traces_sample_rate})")
