"""Pydantic schemas for Player endpoints."""

from datetime import datetime

from pydantic import BaseModel, Field


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
    username: str | None = Field(default=None, min_length=3, max_length=50)
    avatar: str | None = Field(default=None)


class PlayerStatsResponse(BaseModel):
    """Schema for player statistics."""
    player_id: int
    classes_completed: int
    exercises_completed: int
    bug_hunt_wins: int
    bug_hunt_games_played: int
    current_streak: int
    longest_streak: int
    last_activity_date: datetime

    class Config:
        from_attributes = True
