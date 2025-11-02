"""Minigame models - tracks minigame sessions and scores."""

from app.database import Base
from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class BugHuntGame(Base):
    """Bug Hunt game session - tracks individual plays."""

    __tablename__ = "bug_hunt_games"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    template_id = Column(String, nullable=False)  # e.g., "bug_001"
    difficulty = Column(String, nullable=False)  # "easy", "medium", "hard"

    # Game results
    bugs_found = Column(Integer, default=0)  # Number of bugs correctly identified
    bugs_total = Column(Integer, nullable=False)  # Total bugs in template
    time_seconds = Column(Float, nullable=False)  # Time taken in seconds
    score = Column(Integer, nullable=False)  # Calculated score
    xp_earned = Column(Integer, nullable=False)  # XP awarded

    # Detailed results
    found_bugs = Column(JSON, nullable=True)  # List of bug lines found
    missed_bugs = Column(JSON, nullable=True)  # List of bug lines missed
    false_positives = Column(JSON, nullable=True)  # List of incorrect identifications

    # Timestamps
    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    player = relationship("Player", backref="bug_hunt_games")

    def __repr__(self):
        return f"<BugHuntGame(id={self.id}, player_id={self.player_id}, score={self.score})>"

    @property
    def accuracy(self) -> float:
        """Calculate accuracy percentage."""
        if self.bugs_total == 0:
            return 0.0
        return (self.bugs_found / self.bugs_total) * 100

    @property
    def is_perfect(self) -> bool:
        """Check if player found all bugs with no false positives."""
        return (
            self.bugs_found == self.bugs_total and
            (not self.false_positives or len(self.false_positives) == 0)
        )
