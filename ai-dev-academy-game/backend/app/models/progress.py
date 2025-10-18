"""Progress model - tracks player progress through modules and classes."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Progress(Base):
    """Progress table - tracks completion of modules and classes."""

    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    module_number = Column(Integer, nullable=False)
    class_number = Column(Integer, nullable=False)
    status = Column(String, default="locked")  # locked, unlocked, in_progress, completed
    exercises_completed = Column(Integer, default=0)
    exercises_total = Column(Integer, default=0)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    player = relationship("Player", back_populates="progress")

    # Unique constraint: one progress record per player per module/class
    __table_args__ = (
        UniqueConstraint('player_id', 'module_number', 'class_number', name='_player_module_class_uc'),
    )

    def __repr__(self):
        return f"<Progress(player_id={self.player_id}, module={self.module_number}, class={self.class_number}, status='{self.status}')>"
