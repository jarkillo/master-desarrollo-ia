"""Course Manager - Central registry for all courses in NeuralFlow."""

from typing import Optional
from app.core.course import Course
from app.courses.master_ia import MasterIACourse
from app.courses.data_engineering import DataEngineeringCourse


class CourseManager:
    """
    Manages course registration and retrieval.

    This class maintains a registry of all available courses in the platform
    and provides methods to retrieve them by ID or get all courses.
    """

    def __init__(self):
        """Initialize the course manager with an empty registry."""
        self._courses: dict[str, Course] = {}

    def register_course(self, course: Course) -> None:
        """
        Register a new course in the manager.

        Args:
            course: Course instance to register
        """
        self._courses[course.id] = course

    def get_course(self, course_id: str) -> Optional[Course]:
        """
        Get a course by its ID.

        Args:
            course_id: Unique identifier of the course

        Returns:
            Course instance if found, None otherwise
        """
        return self._courses.get(course_id)

    def get_all_courses(self) -> list[Course]:
        """
        Get all registered courses.

        Returns:
            List of all Course instances
        """
        return list(self._courses.values())


# Global singleton instance
course_manager = CourseManager()

# Register all courses
course_manager.register_course(MasterIACourse())
course_manager.register_course(DataEngineeringCourse())
