"""Course schemas for API responses."""

from pydantic import BaseModel, Field


class CourseResponse(BaseModel):
    """Response model for course information in catalog."""

    id: str = Field(..., description="Unique identifier for the course")
    name: str = Field(..., description="Display name of the course")
    description: str = Field(..., description="Short description of the course")
    status: str = Field(..., description="Course status: available, coming_soon, or draft")
    modules: int = Field(..., description="Number of modules in the course", ge=0)
    icon: str = Field(..., description="Icon/emoji representing the course")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "master-ia",
                    "name": "Master en Desarrollo con IA",
                    "description": "Aprende desarrollo moderno con IA como tu asistente",
                    "status": "available",
                    "modules": 6,
                    "icon": "🤖"
                }
            ]
        }
    }
