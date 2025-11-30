"""Course catalog routes - NeuralFlow multi-course catalog (NFLOW-1)."""

from fastapi import APIRouter
from app.core.course_manager import course_manager
from app.schemas.course import CourseResponse

router = APIRouter(prefix="/api", tags=["catalog"])


@router.get("/courses", response_model=list[CourseResponse])
async def get_courses():
    """
    Get catalog of all available courses in NeuralFlow.

    Returns a list of courses with their basic information including:
    - id: Unique identifier
    - name: Display name
    - description: Short description
    - status: 'available', 'coming_soon', or 'draft'
    - modules: Number of modules
    - icon: Course icon/emoji

    This endpoint is part of NFLOW-1 (Backend multi-curso con adapter pattern).
    """
    courses = course_manager.get_all_courses()

    return [
        CourseResponse(
            id=course.id,
            name=course.name,
            description=course.description,
            status=course.status,
            modules=course.modules,
            icon=course.icon
        )
        for course in courses
    ]
