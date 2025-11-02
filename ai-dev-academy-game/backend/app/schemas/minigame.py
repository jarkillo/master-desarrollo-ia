"""Pydantic schemas for minigame endpoints."""

from datetime import datetime

from pydantic import BaseModel, Field

# Bug Hunt Schemas

class BugHuntStartRequest(BaseModel):
    """Request to start a Bug Hunt game."""
    player_id: int = Field(..., description="Player ID")
    difficulty: str | None = Field(None, description="Difficulty: easy, medium, or hard (random if not specified)")


class BugInfo(BaseModel):
    """Information about a bug in the code."""
    line: int = Field(..., description="Line number where the bug is located")
    type: str = Field(..., description="Type of bug")
    description: str = Field(..., description="Description of the bug")
    hint: str = Field(..., description="Hint to help find the bug")


class BugHuntStartResponse(BaseModel):
    """Response when starting a Bug Hunt game."""
    session_id: int = Field(..., description="Unique session ID for this game")
    template_id: str = Field(..., description="Template ID")
    title: str = Field(..., description="Challenge title")
    description: str = Field(..., description="Challenge description")
    difficulty: str = Field(..., description="Difficulty level")
    code: str = Field(..., description="Code snippet with bugs")
    bugs_count: int = Field(..., description="Total number of bugs to find")
    max_xp: int = Field(..., description="Maximum XP for perfect score")
    started_at: datetime = Field(..., description="Game start timestamp")


class BugHuntSubmitRequest(BaseModel):
    """Request to submit Bug Hunt answers."""
    session_id: int = Field(..., description="Session ID from start response")
    player_id: int = Field(..., description="Player ID")
    found_bug_lines: list[int] = Field(..., description="List of line numbers identified as bugs")
    time_seconds: float = Field(..., description="Time taken in seconds", ge=0)


class BugResult(BaseModel):
    """Detailed result for a single bug."""
    line: int
    found: bool
    is_correct: bool
    bug_type: str | None = None
    description: str | None = None


class BugHuntSubmitResponse(BaseModel):
    """Response after submitting Bug Hunt answers."""
    success: bool
    score: int = Field(..., description="Score earned")
    xp_earned: int = Field(..., description="XP awarded")
    bugs_found: int = Field(..., description="Number of bugs correctly identified")
    bugs_total: int = Field(..., description="Total bugs in the challenge")
    bugs_missed: int = Field(..., description="Number of bugs missed")
    false_positives: int = Field(..., description="Number of incorrect identifications")
    accuracy: float = Field(..., description="Accuracy percentage")
    time_seconds: float = Field(..., description="Time taken")
    is_perfect: bool = Field(..., description="Whether all bugs were found with no false positives")

    # Detailed results
    results: list[BugResult] = Field(..., description="Detailed results per bug")
    performance_bonus: int = Field(default=0, description="Bonus XP for speed/accuracy")

    # Achievements unlocked
    achievements_unlocked: list[str] = Field(default_factory=list, description="Achievement keys unlocked")


class LeaderboardEntry(BaseModel):
    """Single entry in the leaderboard."""
    rank: int
    player_id: int
    username: str
    score: int
    bugs_found: int
    bugs_total: int
    time_seconds: float
    accuracy: float
    difficulty: str
    completed_at: datetime

    class Config:
        from_attributes = True


class LeaderboardResponse(BaseModel):
    """Leaderboard response."""
    total_entries: int
    entries: list[LeaderboardEntry]
    difficulty_filter: str | None = None


class PlayerBugHuntStatsResponse(BaseModel):
    """Player's Bug Hunt statistics."""
    total_games_played: int
    total_bugs_found: int
    total_perfect_games: int
    best_score: int
    average_score: float
    average_accuracy: float
    favorite_difficulty: str | None = None
    total_xp_earned: int
