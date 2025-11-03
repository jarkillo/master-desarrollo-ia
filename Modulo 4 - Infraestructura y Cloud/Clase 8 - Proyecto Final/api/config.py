"""
Configuración de la aplicación usando Pydantic Settings.

Este módulo gestiona todas las variables de entorno y configuración
de la aplicación de forma type-safe y con validación automática.
"""

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuración de la aplicación.

    Las variables se cargan desde:
    1. Variables de entorno del sistema
    2. Archivo .env (si existe)

    Ejemplo de uso:
        from api.config import settings
        print(settings.database_url)
    """

    # Database Configuration
    database_url: str = "sqlite:///./tareas.db"

    # Environment
    environment: Literal["dev", "staging", "prod"] = "dev"

    # JWT Configuration
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60

    # Application
    app_name: str = "API Tareas - Proyecto Final"
    debug: bool = False

    # PostgreSQL (para docker-compose)
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "tareas_db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # Las variables no son case-sensitive
        extra="ignore"  # Ignora variables extra en .env
    )

    @property
    def is_production(self) -> bool:
        """Verifica si estamos en producción."""
        return self.environment == "prod"

    @property
    def is_development(self) -> bool:
        """Verifica si estamos en desarrollo."""
        return self.environment == "dev"

    @property
    def postgres_url(self) -> str:
        """
        Construye la URL de PostgreSQL para docker-compose local.

        Returns:
            URL completa de PostgreSQL
        """
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@localhost:5432/{self.postgres_db}"
        )


# Instancia global de configuración
settings = Settings()
