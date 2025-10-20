"""Achievement model - tracks unlocked achievements."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Achievement(Base):
    """Achievement table - stores unlocked achievements per player."""

    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    achievement_key = Column(String, nullable=False)  # 'first_steps', 'bug_hunter', etc.
    unlocked_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    player = relationship("Player", back_populates="achievements")

    # Unique constraint: player can only unlock each achievement once
    __table_args__ = (
        UniqueConstraint('player_id', 'achievement_key', name='_player_achievement_uc'),
    )

    def __repr__(self):
        return f"<Achievement(player_id={self.player_id}, key='{self.achievement_key}')>"


class PlayerStats(Base):
    """Player stats table - aggregated statistics."""

    __tablename__ = "player_stats"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False, unique=True)
    total_classes_completed = Column(Integer, default=0)
    total_exercises_done = Column(Integer, default=0)
    total_minigames_played = Column(Integer, default=0)
    total_code_lines = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)
    last_activity_date = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    player = relationship("Player", back_populates="stats")

    def __repr__(self):
        return f"<PlayerStats(player_id={self.player_id}, classes={self.total_classes_completed}, streak={self.streak_days})>"


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
