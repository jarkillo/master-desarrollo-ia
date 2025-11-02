"""Achievement model - tracks unlocked achievements."""

from app.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Achievement(Base):
    """Achievement table - stores unlocked achievements per player."""

    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    achievement_id = Column(String, nullable=False)  # 'first_class', 'bug_hunter', etc.
    unlocked_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    player = relationship("Player", back_populates="achievements")

    # Unique constraint: player can only unlock each achievement once
    __table_args__ = (
        UniqueConstraint('player_id', 'achievement_id', name='_player_achievement_uc'),
    )

    def __repr__(self):
        return f"<Achievement(player_id={self.player_id}, achievement_id='{self.achievement_id}')>"


class PlayerStats(Base):
    """Player stats table - aggregated statistics."""

    __tablename__ = "player_stats"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False, unique=True)
    classes_completed = Column(Integer, default=0)
    exercises_completed = Column(Integer, default=0)
    bug_hunt_wins = Column(Integer, default=0)
    bug_hunt_games_played = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity_date = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    player = relationship("Player", back_populates="stats")

    def __repr__(self):
        return f"<PlayerStats(player_id={self.player_id}, classes={self.classes_completed}, streak={self.current_streak})>"


class UnlockedTool(Base):
    """Unlocked tools table - tracks which tools/agents player has unlocked."""

    __tablename__ = "unlocked_tools"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    tool_key = Column(String, nullable=False)  # 'claude_code', 'cursor', 'test_strategist'
    unlocked_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    player = relationship("Player", back_populates="unlocked_tools")

    # Unique constraint: player can only unlock each tool once
    __table_args__ = (
        UniqueConstraint('player_id', 'tool_key', name='_player_tool_uc'),
    )

    def __repr__(self):
        return f"<UnlockedTool(player_id={self.player_id}, tool='{self.tool_key}')>"
