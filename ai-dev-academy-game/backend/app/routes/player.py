"""Player routes - CRUD operations for game players."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.player import Player
from app.models.progress import PlayerStats
from app.schemas.player import (
    PlayerCreate,
    PlayerResponse,
    PlayerUpdate,
    PlayerStatsResponse
)

router = APIRouter()


@router.post("/", response_model=PlayerResponse, status_code=status.HTTP_201_CREATED)
async def create_player(
    player_data: PlayerCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new player.

    - **username**: Unique username (3-20 chars)
    - **avatar**: Optional avatar filename (default: default.png)

    Returns the created player with initial stats (level 1, 0 XP).
    """
    # Check if username already exists
    existing_player = db.query(Player).filter(
        Player.username == player_data.username
    ).first()

    if existing_player:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username '{player_data.username}' is already taken"
        )

    # Create new player
    new_player = Player(
        username=player_data.username,
        avatar=player_data.avatar or "default.png",
        level=1,
        xp=0
    )

    db.add(new_player)
    db.flush()  # Get player.id without committing

    # Create initial player stats
    player_stats = PlayerStats(
        player_id=new_player.id,
        classes_completed=0,
        exercises_completed=0,
        minigames_played=0,
        current_streak=0,
        longest_streak=0
    )

    db.add(player_stats)
    db.commit()
    db.refresh(new_player)

    return new_player


@router.get("/{player_id}", response_model=PlayerResponse)
async def get_player(
    player_id: int,
    db: Session = Depends(get_db)
):
    """
    Get player profile by ID.

    Returns player information including level, XP, and avatar.
    """
    player = db.query(Player).filter(Player.id == player_id).first()

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found"
        )

    return player


@router.get("/", response_model=List[PlayerResponse])
async def list_players(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all players with pagination.

    - **skip**: Number of players to skip (default: 0)
    - **limit**: Maximum players to return (default: 100, max: 100)
    """
    if limit > 100:
        limit = 100

    players = db.query(Player).offset(skip).limit(limit).all()
    return players


@router.patch("/{player_id}", response_model=PlayerResponse)
async def update_player(
    player_id: int,
    player_data: PlayerUpdate,
    db: Session = Depends(get_db)
):
    """
    Update player profile (avatar or username).

    Only non-null fields in the request will be updated.
    """
    player = db.query(Player).filter(Player.id == player_id).first()

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found"
        )

    # Check if new username is taken (if provided)
    if player_data.username and player_data.username != player.username:
        existing = db.query(Player).filter(
            Player.username == player_data.username
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Username '{player_data.username}' is already taken"
            )

        player.username = player_data.username

    # Update avatar if provided
    if player_data.avatar:
        player.avatar = player_data.avatar

    db.commit()
    db.refresh(player)

    return player


@router.get("/{player_id}/stats", response_model=PlayerStatsResponse)
async def get_player_stats(
    player_id: int,
    db: Session = Depends(get_db)
):
    """
    Get comprehensive player statistics.

    Returns stats including:
    - Classes completed
    - Exercises completed
    - Minigames played
    - Current and longest streak
    """
    player = db.query(Player).filter(Player.id == player_id).first()

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found"
        )

    # Get or create stats
    stats = db.query(PlayerStats).filter(
        PlayerStats.player_id == player_id
    ).first()

    if not stats:
        # Create default stats if they don't exist
        stats = PlayerStats(
            player_id=player_id,
            classes_completed=0,
            exercises_completed=0,
            minigames_played=0,
            current_streak=0,
            longest_streak=0
        )
        db.add(stats)
        db.commit()
        db.refresh(stats)

    return stats


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_player(
    player_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a player and all associated data.

    This will cascade delete:
    - Player stats
    - Progress records
    - Achievements
    - Unlocked tools
    - Bug Hunt games
    """
    player = db.query(Player).filter(Player.id == player_id).first()

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found"
        )

    db.delete(player)
    db.commit()

    return None
