# api/config.py
"""
Configuración de la aplicación usando Pydantic Settings.

Gestiona environment variables para diferentes entornos:
- dev: SQLite local, debug mode
- staging: PostgreSQL en cloud, logs moderados
- prod: PostgreSQL en cloud, optimizado para producción

Ventajas de Pydantic Settings:
- Validación automática de tipos
- Valores por defecto seguros
- Fácil overriding con .env files
- Type hints nativos
"""
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuración de la aplicación.

    Las variables se leen desde:
    1. Environment variables del sistema/cloud
    2. Archivo .env (si existe)
    3. Valores por defecto (definidos aquí)

    Ejemplo de uso:
        from api.config import settings

        if settings.environment == "prod":
            print("Running in production!")
    """

    # Environment (dev, staging, prod)
    environment: Literal["dev", "staging", "prod"] = "dev"

    # Database
    database_url: str = "sqlite:///./tareas.db"

    # API
    api_title: str = "API de Tareas - Cloud Ready"
    api_version: str = "1.0.0"
    api_description: str = "API REST con FastAPI + SQLAlchemy + PostgreSQL en Cloud"

    # CORS (Cross-Origin Resource Sharing)
    # En producción, especifica los dominios permitidos
    # Se parsea desde string separado por comas si viene de env var
    _cors_origins: str = "*"

    # Security
    # IMPORTANTE: En producción, genera con: openssl rand -hex 32
    # Si estás en dev, puedes dejar el default, pero NUNCA en prod
    secret_key: str = "dev-secret-only-change-in-production"

    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    # Server (usado por Uvicorn)
    host: str = "0.0.0.0"  # Permite conexiones externas (necesario en cloud)
    port: int = 8000

    # Database connection pool (importante para producción)
    db_pool_size: int = 5  # Conexiones simultáneas
    db_max_overflow: int = 10  # Conexiones adicionales si se necesitan

    model_config = SettingsConfigDict(
        env_file=".env",  # Lee del archivo .env si existe
        env_file_encoding="utf-8",
        case_sensitive=False,  # DATABASE_URL = database_url
        extra="ignore"  # Ignora variables extra (no falla si hay más en .env)
    )

    @property
    def is_production(self) -> bool:
        """Helper para saber si estamos en producción"""
        return self.environment == "prod"

    @property
    def is_development(self) -> bool:
        """Helper para saber si estamos en desarrollo"""
        return self.environment == "dev"

    @property
    def database_echo(self) -> bool:
        """
        Controla si SQLAlchemy muestra SQL en logs.
        Solo en desarrollo para debugging.
        """
        return self.environment == "dev"

    @property
    def cors_origins(self) -> list[str]:
        """
        Retorna lista de CORS origins según el entorno.

        En desarrollo: permite todo ["*"]
        En producción: lista específica de dominios permitidos
        """
        if self.is_development:
            return ["*"]

        # En producción, parsea desde environment variable
        # Formato: "https://app.com,https://www.app.com"
        if self._cors_origins == "*":
            # ⚠️ WARNING: CORS abierto en producción es inseguro
            return ["*"]

        return [origin.strip() for origin in self._cors_origins.split(",")]


# Instancia global de settings (singleton)
# Úsala así: from api.config import settings
settings = Settings()
