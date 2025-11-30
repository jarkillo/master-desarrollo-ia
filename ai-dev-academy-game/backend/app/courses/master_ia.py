"""Master IA Course adapter - Wraps existing Master IA content."""

from typing import Any
from app.services.content_service import get_all_modules


class MasterIACourse:
    """
    Adapter for Master en Desarrollo con IA course.

    Wraps the existing content_service to provide a course interface.
    This maintains backward compatibility with the existing system.
    """

    @property
    def id(self) -> str:
        """Unique identifier for the course."""
        return "master-ia"

    @property
    def name(self) -> str:
        """Display name of the course."""
        return "Master en Desarrollo con IA"

    @property
    def description(self) -> str:
        """Short description of the course."""
        return "Aprende desarrollo moderno con IA como tu asistente. FastAPI, React, Docker, y más."

    @property
    def status(self) -> str:
        """Course status."""
        return "available"

    @property
    def modules(self) -> int:
        """Number of modules in the course."""
        return len(get_all_modules())

    @property
    def icon(self) -> str:
        """Icon representing the course."""
        return "🤖"

    def get_modules(self) -> list[dict[str, Any]]:
        """
        Get all modules for Master IA course.

        Uses the existing get_all_modules function to maintain backward compatibility.

        Returns:
            List of module dictionaries
        """
        modules = []
        for module_info in get_all_modules():
            module_dict = {
                "id": module_info.module_number,
                "name": module_info.title,
                "description": module_info.description,
                "classes": [
                    {
                        "id": cls.class_number,
                        "title": cls.title,
                        "description": cls.description,
                        "xp_reward": cls.xp_reward,
                        "exercises_count": cls.exercises_count,
                        "difficulty": cls.difficulty,
                        "estimated_time_minutes": cls.estimated_time_minutes,
                    }
                    for cls in module_info.classes
                ]
            }
            modules.append(module_dict)
        return modules

    def get_achievements(self) -> list[dict[str, Any]]:
        """
        Get achievements for Master IA course.

        Returns empty list for now (achievements are global in current system).
        This will be implemented in NFLOW-7.

        Returns:
            Empty list
        """
        return []
