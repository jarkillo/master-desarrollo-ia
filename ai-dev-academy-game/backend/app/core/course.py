"""Course adapter protocol - Base interface for all courses in NeuralFlow."""

from typing import Protocol, Any


class Course(Protocol):
    """
    Protocol defining the interface that all courses must implement.

    This allows the CourseManager to work with any course implementation
    without knowing the specific details of each course.
    """

    @property
    def id(self) -> str:
        """Unique identifier for the course (e.g., 'master-ia', 'data-engineering')."""
        ...

    @property
    def name(self) -> str:
        """Display name of the course."""
        ...

    @property
    def description(self) -> str:
        """Short description of the course."""
        ...

    @property
    def status(self) -> str:
        """Course status: 'available', 'coming_soon', or 'draft'."""
        ...

    @property
    def modules(self) -> int:
        """Number of modules in the course."""
        ...

    @property
    def icon(self) -> str:
        """Icon/emoji representing the course."""
        ...

    def get_modules(self) -> list[dict[str, Any]]:
        """
        Get all modules for this course.

        Returns:
            List of module dictionaries with structure:
            {
                "id": int,
                "name": str,
                "description": str,
                "classes": list[dict]
            }
        """
        ...

    def get_achievements(self) -> list[dict[str, Any]]:
        """
        Get all achievements specific to this course.

        Returns:
            List of achievement dictionaries (can be empty for now).
        """
        ...
