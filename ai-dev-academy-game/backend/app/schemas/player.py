"""Pydantic schemas for Player endpoints."""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class PlayerCreate(BaseModel):
    """Schema for creating a new player."""
    username: str = Field(..., min_length=3, max_length=20, description="Username (3-20 characters)")
    avatar: str = Field(default="default.png", description="Avatar filename")


class PlayerResponse(BaseModel):
    """Schema for player response."""
    id: int
    username: str
    avatar: str
    level: int
    xp: int
    created_at: datetime
    last_login: datetime

    class Config:
        from_attributes = True  # Allows converting from SQLAlchemy model


class PlayerUpdate(BaseModel):
    """Schema for updating player info."""
    avatar: Optional[str] = None


class PlayerStatsResponse(BaseModel):
    """Schema for player statistics."""
    total_classes_completed: int
    total_exercises_done: int
    total_minigames_played: int
    total_code_lines: int
    streak_days: int
    last_activity_date: datetime

    class Config:
        from_attributes = True
