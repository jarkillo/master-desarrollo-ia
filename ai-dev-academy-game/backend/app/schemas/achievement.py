"""Achievement schemas - Pydantic models for achievements."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class AchievementCategory(str, Enum):
    """Achievement categories."""
    LEARNING = "learning"
    MINIGAME = "minigame"
    STREAK = "streak"
    MASTERY = "mastery"
    SPECIAL = "special"


class AchievementRarity(str, Enum):
    """Achievement rarity levels."""
    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class AchievementDefinition(BaseModel):
    """Definition of an available achievement."""
    achievement_id: str = Field(..., description="Unique achievement ID (e.g., 'first_class')")
    title: str = Field(..., description="Achievement title")
    description: str = Field(..., description="How to unlock this achievement")
    icon: str = Field(..., description="Icon filename or emoji")
    category: AchievementCategory
    rarity: AchievementRarity
    xp_reward: int = Field(..., ge=0, description="XP awarded when unlocked")


class UnlockAchievementRequest(BaseModel):
    """Request to unlock an achievement."""
    player_id: int = Field(..., gt=0, description="Player ID")
    achievement_id: str = Field(..., description="Achievement ID to unlock")


class AchievementResponse(BaseModel):
    """Schema for achievement response."""
    id: int
    player_id: int
    achievement_id: str
    unlocked_at: datetime

    class Config:
        from_attributes = True


class AchievementWithDetails(BaseModel):
    """Achievement response with full details."""
    id: int
    player_id: int
    achievement_id: str
    title: str
    description: str
    icon: str
    category: AchievementCategory
    rarity: AchievementRarity
    xp_reward: int
    unlocked_at: datetime


class PlayerAchievementsResponse(BaseModel):
    """Response with all player achievements."""
    player_id: int
    total_achievements: int
    achievements: list[AchievementWithDetails]


class AvailableAchievementsResponse(BaseModel):
    """Response with all available achievements."""
    total_achievements: int
    achievements: list[AchievementDefinition]


class CheckAchievementsRequest(BaseModel):
    """Request to check and unlock achievements after an action."""
    player_id: int = Field(..., gt=0, description="Player ID")
    action_type: str = Field(..., description="Type of action (e.g., 'complete_class', 'bug_hunt_win')")
    action_data: dict | None = Field(
        None,
        description="Additional data for the action"
    )


class CheckAchievementsResponse(BaseModel):
    """Response after checking achievements."""
    achievements_unlocked: list[AchievementWithDetails]
    xp_earned: int
