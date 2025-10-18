"""Player model - represents a game player."""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Player(Base):
    """Player table - stores player information."""

    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    avatar = Column(String, default="default.png")
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    progress = relationship("Progress", back_populates="player", cascade="all, delete-orphan")
    achievements = relationship("Achievement", back_populates="player", cascade="all, delete-orphan")
    stats = relationship("PlayerStats", back_populates="player", uselist=False, cascade="all, delete-orphan")
    unlocked_tools = relationship("UnlockedTool", back_populates="player", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Player(id={self.id}, username='{self.username}', level={self.level}, xp={self.xp})>"
