"""Achievement routes - Manage player achievements and unlocking."""


from app.database import get_db
from app.models.achievement import Achievement
from app.models.player import Player
from app.schemas.achievement import (
    AchievementWithDetails,
    AvailableAchievementsResponse,
    CheckAchievementsRequest,
    CheckAchievementsResponse,
    PlayerAchievementsResponse,
    UnlockAchievementRequest,
)
from app.services import achievement_service, xp_service
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=AvailableAchievementsResponse)
async def get_all_achievements():
    """
    Get all available achievements in the game.

    Returns all achievement definitions with their requirements,
    icons, rarity, and XP rewards.
    """
    definitions = achievement_service.get_all_achievement_definitions()

    return AvailableAchievementsResponse(
        total_achievements=len(definitions),
        achievements=definitions
    )


@router.get("/player/{player_id}", response_model=PlayerAchievementsResponse)
async def get_player_achievements(
    player_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all achievements unlocked by a player.

    Returns achievement records with full details including unlock timestamps.
    """
    # Validate player exists
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found"
        )

    # Get all unlocked achievements
    unlocked = db.query(Achievement).filter(
        Achievement.player_id == player_id
    ).all()

    # Build response with full details
    achievements_with_details = []
    for achievement in unlocked:
        definition = achievement_service.get_achievement_definition(achievement.achievement_id)
        if definition:
            achievements_with_details.append(
                AchievementWithDetails(
                    id=achievement.id,
                    player_id=achievement.player_id,
                    achievement_id=achievement.achievement_id,
                    title=definition.title,
                    description=definition.description,
                    icon=definition.icon,
                    category=definition.category,
                    rarity=definition.rarity,
                    xp_reward=definition.xp_reward,
                    unlocked_at=achievement.unlocked_at
                )
            )

    return PlayerAchievementsResponse(
        player_id=player_id,
        total_achievements=len(achievements_with_details),
        achievements=achievements_with_details
    )


@router.post("/unlock", response_model=AchievementWithDetails, status_code=status.HTTP_201_CREATED)
async def unlock_achievement(
    request: UnlockAchievementRequest,
    db: Session = Depends(get_db)
):
    """
    Manually unlock an achievement for a player.

    Validates that:
    - Player exists
    - Achievement definition exists
    - Achievement not already unlocked
    - Awards XP to player
    """
    # Validate player exists
    player = db.query(Player).filter(Player.id == request.player_id).first()
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {request.player_id} not found"
        )

    # Validate achievement definition exists
    definition = achievement_service.get_achievement_definition(request.achievement_id)
    if not definition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Achievement '{request.achievement_id}' not found"
        )

    # Check if already unlocked
    existing = db.query(Achievement).filter(
        Achievement.player_id == request.player_id,
        Achievement.achievement_id == request.achievement_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Achievement '{request.achievement_id}' already unlocked for this player"
        )

    # Create achievement record
    new_achievement = Achievement(
        player_id=request.player_id,
        achievement_id=request.achievement_id
    )

    db.add(new_achievement)
    db.flush()

    # Award XP using centralized service
    xp_service.award_xp(
        player_id=request.player_id,
        xp_amount=definition.xp_reward,
        db=db,
        reason=f"Unlocked achievement: {definition.title}"
    )

    db.commit()
    db.refresh(new_achievement)

    # Return with full details
    return AchievementWithDetails(
        id=new_achievement.id,
        player_id=new_achievement.player_id,
        achievement_id=new_achievement.achievement_id,
        title=definition.title,
        description=definition.description,
        icon=definition.icon,
        category=definition.category,
        rarity=definition.rarity,
        xp_reward=definition.xp_reward,
        unlocked_at=new_achievement.unlocked_at
    )


@router.post("/check", response_model=CheckAchievementsResponse)
async def check_achievements(
    request: CheckAchievementsRequest,
    db: Session = Depends(get_db)
):
    """
    Check and automatically unlock achievements after an action.

    Common action types:
    - 'complete_class' (action_data: {module_number, class_number})
    - 'bug_hunt_win' (action_data: {accuracy, time_seconds})
    - 'complete_exercise'

    Returns list of newly unlocked achievements and total XP earned.
    """
    # Validate player exists
    player = db.query(Player).filter(Player.id == request.player_id).first()
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {request.player_id} not found"
        )

    # Check and unlock achievements
    unlocked_achievements = achievement_service.check_and_unlock_achievements(
        player_id=request.player_id,
        action_type=request.action_type,
        action_data=request.action_data,
        db=db
    )

    # Calculate total XP earned
    total_xp = sum(a.xp_reward for a in unlocked_achievements)

    return CheckAchievementsResponse(
        achievements_unlocked=unlocked_achievements,
        xp_earned=total_xp
    )


@router.delete("/{achievement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_achievement(
    achievement_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an unlocked achievement (admin/debug only).

    Note: Does NOT refund XP.
    """
    achievement = db.query(Achievement).filter(Achievement.id == achievement_id).first()

    if not achievement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Achievement with ID {achievement_id} not found"
        )

    db.delete(achievement)
    db.commit()

    return None
