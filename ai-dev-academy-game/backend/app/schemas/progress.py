"""Progress schemas - Pydantic models for player progress."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ProgressStatus(str, Enum):
    """Progress status for a class."""
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class ProgressCreate(BaseModel):
    """Schema for creating/unlocking a class."""
    player_id: int = Field(..., gt=0, description="Player ID")
    module_number: int = Field(..., ge=0, le=5, description="Module number (0-5)")
    class_number: int = Field(..., ge=0, description="Class number within module")
    status: ProgressStatus = Field(
        default=ProgressStatus.UNLOCKED,
        description="Initial status (usually 'unlocked')"
    )


class ProgressUpdate(BaseModel):
    """Schema for updating progress (mark as completed, add exercises)."""
    status: ProgressStatus | None = Field(
        None,
        description="New status (e.g., 'in_progress', 'completed')"
    )
    exercises_completed: int | None = Field(
        None,
        ge=0,
        description="Number of exercises completed"
    )


class ProgressResponse(BaseModel):
    """Schema for progress response."""
    id: int
    player_id: int
    module_number: int
    class_number: int
    status: ProgressStatus
    exercises_completed: int
    started_at: datetime | None
    completed_at: datetime | None

    class Config:
        from_attributes = True


class ClassProgress(BaseModel):
    """Schema for a single class progress summary."""
    class_number: int
    status: ProgressStatus
    exercises_completed: int = 0
    completed_at: datetime | None = None


class ModuleProgressResponse(BaseModel):
    """Schema for module-level progress summary."""
    module_number: int
    module_name: str
    total_classes: int
    completed_classes: int
    progress_percentage: float
    classes: list[ClassProgress]


class FullProgressResponse(BaseModel):
    """Schema for complete player progress across all modules."""
    player_id: int
    total_classes_completed: int
    total_exercises_completed: int
    overall_progress_percentage: float
    modules: list[ModuleProgressResponse]


class ClassInfoResponse(BaseModel):
    """Schema for class metadata from curriculum."""
    class_number: int
    title: str
    description: str
    exercises_count: int
    xp_reward: int
    difficulty: str = "intermediate"
    estimated_time_minutes: int = 60
    prerequisites: list[str] = []
    learning_objectives: list[str] = []


class ModuleInfoResponse(BaseModel):
    """Schema for module metadata from curriculum."""
    module_number: int
    title: str
    description: str
    total_classes: int
    classes: list[ClassInfoResponse]
