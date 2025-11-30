"""Data Engineering Course stub - Coming soon."""

from typing import Any


class DataEngineeringCourse:
    """
    Stub for Data Engineering course.

    This course is coming soon. Content will be added in NFLOW-4.
    For now, it's registered in the catalog as "coming_soon".
    """

    @property
    def id(self) -> str:
        """Unique identifier for the course."""
        return "data-engineering"

    @property
    def name(self) -> str:
        """Display name of the course."""
        return "Data Engineering"

    @property
    def description(self) -> str:
        """Short description of the course."""
        return "Construye pipelines de datos a escala. ETL, Airflow, Data Warehousing, y más."

    @property
    def status(self) -> str:
        """Course status."""
        return "coming_soon"

    @property
    def modules(self) -> int:
        """Number of modules in the course."""
        return 5  # Planned: ETL Foundations, Databases at Scale, Airflow, Data Warehousing, Final Project

    @property
    def icon(self) -> str:
        """Icon representing the course."""
        return "📊"

    def get_modules(self) -> list[dict[str, Any]]:
        """
        Get all modules for Data Engineering course.

        Returns empty list for now (content not yet created - NFLOW-4).

        Returns:
            Empty list
        """
        return []

    def get_achievements(self) -> list[dict[str, Any]]:
        """
        Get achievements for Data Engineering course.

        Returns empty list for now (will be implemented in NFLOW-7).

        Returns:
            Empty list
        """
        return []
