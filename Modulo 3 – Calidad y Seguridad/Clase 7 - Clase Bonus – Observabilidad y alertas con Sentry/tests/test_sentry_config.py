# tests/test_sentry_config.py
"""Tests para el módulo sentry_config.py

Estos tests verifican:
- Scrubbing de datos sensibles
- Procesamiento de eventos antes de enviar a Sentry
- Configuración de Sentry con diferentes ambientes
- Protección de PII y datos sensibles
"""
import os
import pytest
from unittest.mock import patch, MagicMock
from api.sentry_config import (
    scrub_sensitive_data,
    before_send,
    configurar_sentry,
    SENSITIVE_FIELDS
)


class TestScrubSensitiveData:
    """Tests para la función scrub_sensitive_data"""

    def test_scrub_simple_password(self):
        """Debería redactar campos de password"""
        data = {"username": "demo", "password": "secret123"}
        result = scrub_sensitive_data(data)

        assert result["username"] == "demo"
        assert result["password"] == "[REDACTED]"

    def test_scrub_multiple_sensitive_fields(self):
        """Debería redactar múltiples campos sensibles"""
        data = {
            "username": "demo",
            "password": "secret123",
            "api_key": "xyz789",
            "token": "abc456"
        }
        result = scrub_sensitive_data(data)

        assert result["username"] == "demo"
        assert result["password"] == "[REDACTED]"
        assert result["api_key"] == "[REDACTED]"
        assert result["token"] == "[REDACTED]"

    def test_scrub_case_insensitive(self):
        """Debería ser case-insensitive en la detección"""
        data = {
            "PASSWORD": "secret123",
            "Secret": "hidden",
            "API_KEY": "xyz789"
        }
        result = scrub_sensitive_data(data)

        assert result["PASSWORD"] == "[REDACTED]"
        assert result["Secret"] == "[REDACTED]"
        assert result["API_KEY"] == "[REDACTED]"

    def test_scrub_partial_match(self):
        """Debería detectar patrones dentro del nombre de la clave"""
        data = {
            "user_password": "secret123",
            "auth_token": "abc456",
            "jwt_secret_key": "xyz789"
        }
        result = scrub_sensitive_data(data)

        assert result["user_password"] == "[REDACTED]"
        assert result["auth_token"] == "[REDACTED]"
        assert result["jwt_secret_key"] == "[REDACTED]"

    def test_scrub_nested_dict(self):
        """Debería procesar diccionarios anidados recursivamente"""
        data = {
            "user": {
                "username": "demo",
                "password": "secret123",
                "profile": {
                    "name": "Demo User",
                    "credit_card": "1234-5678"
                }
            }
        }
        result = scrub_sensitive_data(data)

        assert result["user"]["username"] == "demo"
        assert result["user"]["password"] == "[REDACTED]"
        assert result["user"]["profile"]["name"] == "Demo User"
        assert result["user"]["profile"]["credit_card"] == "[REDACTED]"

    def test_scrub_list_of_dicts(self):
        """Debería procesar listas de diccionarios"""
        data = {
            "users": [
                {"username": "user1", "password": "pass1"},
                {"username": "user2", "password": "pass2"}
            ]
        }
        result = scrub_sensitive_data(data)

        assert result["users"][0]["username"] == "user1"
        assert result["users"][0]["password"] == "[REDACTED]"
        assert result["users"][1]["username"] == "user2"
        assert result["users"][1]["password"] == "[REDACTED]"

    def test_scrub_list_of_primitives(self):
        """Debería mantener listas de primitivos sin cambios"""
        data = {
            "tags": ["python", "security", "testing"],
            "scores": [1, 2, 3, 4, 5]
        }
        result = scrub_sensitive_data(data)

        assert result["tags"] == ["python", "security", "testing"]
        assert result["scores"] == [1, 2, 3, 4, 5]

    def test_scrub_non_dict_returns_unchanged(self):
        """Debería devolver datos no-dict sin cambios"""
        assert scrub_sensitive_data("string") == "string"
        assert scrub_sensitive_data(123) == 123
        assert scrub_sensitive_data([1, 2, 3]) == [1, 2, 3]
        assert scrub_sensitive_data(None) is None


class TestBeforeSend:
    """Tests para la función before_send"""

    def test_before_send_removes_authorization_header(self):
        """Debería eliminar headers de Authorization"""
        event = {
            "request": {
                "headers": {
                    "authorization": "Bearer token123",
                    "content-type": "application/json"
                }
            }
        }
        result = before_send(event, {})

        assert "authorization" not in result["request"]["headers"]
        assert result["request"]["headers"]["content-type"] == "application/json"

    def test_before_send_removes_sensitive_headers_case_variants(self):
        """Debería eliminar headers sensibles en todas las variantes de case"""
        event = {
            "request": {
                "headers": {
                    "Authorization": "Bearer token123",
                    "AUTHORIZATION": "Bearer token456",
                    "x-api-key": "xyz789",
                    "X-Api-Key": "abc123",
                    "Cookie": "session=abc"
                }
            }
        }
        result = before_send(event, {})

        headers = result["request"]["headers"]
        assert "authorization" not in headers
        assert "Authorization" not in headers
        assert "AUTHORIZATION" not in headers
        assert "x-api-key" not in headers
        assert "X-Api-Key" not in headers
        assert "cookie" not in headers
        assert "Cookie" not in headers

    def test_before_send_scrubs_request_data(self):
        """Debería aplicar scrubbing al request body"""
        event = {
            "request": {
                "data": {
                    "username": "demo",
                    "password": "secret123"
                }
            }
        }
        result = before_send(event, {})

        assert result["request"]["data"]["username"] == "demo"
        assert result["request"]["data"]["password"] == "[REDACTED]"

    def test_before_send_redacts_query_params(self):
        """Debería redactar query parameters sensibles"""
        event = {
            "request": {
                "query_string": "user=demo&token=abc123&api_key=xyz789"
            }
        }
        result = before_send(event, {})

        query = result["request"]["query_string"]
        assert "token=[REDACTED]" in query
        assert "api_key=[REDACTED]" in query
        assert "user=demo" in query

    def test_before_send_filters_user_context(self):
        """Debería filtrar campos sensibles del contexto de usuario"""
        event = {
            "user": {
                "id": "123",
                "username": "demo",
                "email": "demo@example.com",
                "ip_address": "192.168.1.1"
            }
        }
        result = before_send(event, {})

        user = result["user"]
        assert "id" in user
        assert "username" in user
        assert "email" not in user
        assert "ip_address" not in user

    def test_before_send_removes_environment_context(self):
        """Debería eliminar variables de entorno del contexto"""
        event = {
            "contexts": {
                "environment": {
                    "DATABASE_URL": "postgres://...",
                    "SECRET_KEY": "xyz"
                },
                "runtime": {
                    "version": "3.12"
                }
            }
        }
        result = before_send(event, {})

        assert "environment" not in result["contexts"]
        assert "runtime" in result["contexts"]

    def test_before_send_handles_event_without_request(self):
        """Debería manejar eventos sin sección request"""
        event = {
            "message": "Error occurred",
            "level": "error"
        }
        result = before_send(event, {})

        assert result["message"] == "Error occurred"
        assert result["level"] == "error"

    def test_before_send_handles_partial_request_data(self):
        """Debería manejar request con datos parciales"""
        event = {
            "request": {
                "method": "POST"
                # Sin headers, data, query_string
            }
        }
        result = before_send(event, {})

        assert result["request"]["method"] == "POST"


class TestConfigurarSentry:
    """Tests para la función configurar_sentry"""

    @patch.dict(os.environ, {}, clear=True)
    @patch('builtins.print')
    def test_configurar_sentry_without_dsn(self, mock_print):
        """Debería degradar gracefully si no hay SENTRY_DSN"""
        configurar_sentry()

        mock_print.assert_called_once()
        call_args = str(mock_print.call_args)
        assert "SENTRY_DSN no configurado" in call_args

    @patch.dict(os.environ, {
        "SENTRY_DSN": "https://test@sentry.io/123",
        "MODE": "development"
    })
    @patch('api.sentry_config.sentry_sdk')
    @patch('builtins.print')
    def test_configurar_sentry_development(self, mock_print, mock_sentry):
        """Debería usar sampling 100% en development"""
        configurar_sentry()

        mock_sentry.init.assert_called_once()
        call_kwargs = mock_sentry.init.call_args[1]

        assert call_kwargs["dsn"] == "https://test@sentry.io/123"
        assert call_kwargs["environment"] == "development"
        assert call_kwargs["traces_sample_rate"] == 1.0
        assert call_kwargs["send_default_pii"] is False

        mock_print.assert_called_once()
        call_args = str(mock_print.call_args)
        assert "environment=development" in call_args
        assert "sampling=1.0" in call_args

    @patch.dict(os.environ, {
        "SENTRY_DSN": "https://test@sentry.io/123",
        "MODE": "production",
        "VERSION": "v1.2.3",
        "HOSTNAME": "server-01"
    })
    @patch('api.sentry_config.sentry_sdk')
    @patch('builtins.print')
    def test_configurar_sentry_production(self, mock_print, mock_sentry):
        """Debería usar sampling 10% en production"""
        configurar_sentry()

        mock_sentry.init.assert_called_once()
        call_kwargs = mock_sentry.init.call_args[1]

        assert call_kwargs["dsn"] == "https://test@sentry.io/123"
        assert call_kwargs["environment"] == "production"
        assert call_kwargs["traces_sample_rate"] == 0.1
        assert call_kwargs["release"] == "v1.2.3"
        assert call_kwargs["server_name"] == "server-01"
        assert call_kwargs["max_breadcrumbs"] == 50
        assert call_kwargs["attach_stacktrace"] is True

        mock_print.assert_called_once()
        call_args = str(mock_print.call_args)
        assert "environment=production" in call_args
        assert "sampling=0.1" in call_args

    @patch.dict(os.environ, {
        "SENTRY_DSN": "https://test@sentry.io/123"
    }, clear=False)
    @patch('api.sentry_config.sentry_sdk')
    def test_configurar_sentry_default_values(self, mock_sentry):
        """Debería usar valores por defecto cuando no hay env vars"""
        # Limpiar las env vars que queremos testear
        for key in ["MODE", "VERSION", "HOSTNAME"]:
            os.environ.pop(key, None)

        configurar_sentry()

        call_kwargs = mock_sentry.init.call_args[1]

        # MODE no definido -> "development" por defecto
        assert call_kwargs["environment"] == "development"
        # VERSION no definido -> "dev" por defecto
        assert call_kwargs["release"] == "dev"
        # HOSTNAME no definido -> usa os.getenv("HOSTNAME", "unknown")
        # que puede ser el hostname del sistema o "unknown"
        assert "server_name" in call_kwargs

    @patch.dict(os.environ, {
        "SENTRY_DSN": "https://test@sentry.io/123"
    })
    @patch('api.sentry_config.sentry_sdk')
    def test_configurar_sentry_uses_before_send(self, mock_sentry):
        """Debería configurar el hook before_send"""
        configurar_sentry()

        call_kwargs = mock_sentry.init.call_args[1]
        assert call_kwargs["before_send"] == before_send

    @patch.dict(os.environ, {
        "SENTRY_DSN": "https://test@sentry.io/123"
    })
    @patch('api.sentry_config.sentry_sdk')
    def test_configurar_sentry_has_integrations(self, mock_sentry):
        """Debería incluir integraciones de FastAPI y Starlette"""
        configurar_sentry()

        call_kwargs = mock_sentry.init.call_args[1]
        integrations = call_kwargs["integrations"]

        assert len(integrations) == 2
        # Verificar que hay FastApiIntegration y StarletteIntegration
        integration_types = [type(i).__name__ for i in integrations]
        assert "FastApiIntegration" in integration_types
        assert "StarletteIntegration" in integration_types
