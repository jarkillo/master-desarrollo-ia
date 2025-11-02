"""XP service - Centralized XP and leveling logic."""

from app.models.player import Player
from sqlalchemy.orm import Session


def calculate_level_from_xp(xp: int) -> int:
    """
    Calculate player level based on total XP.

    Formula: level = int((xp / 100) ** 0.5) + 1

    Examples:
    - 0 XP -> Level 1
    - 100 XP -> Level 2
    - 400 XP -> Level 3
    - 900 XP -> Level 4
    - 10,000 XP -> Level 11
    """
    if xp < 0:
        xp = 0
    return int((xp / 100) ** 0.5) + 1


def calculate_xp_for_level(level: int) -> int:
    """
    Calculate XP required to reach a specific level.

    Inverse of calculate_level_from_xp.

    Examples:
    - Level 1 -> 0 XP
    - Level 2 -> 100 XP
    - Level 3 -> 400 XP
    - Level 4 -> 900 XP
    - Level 10 -> 8,100 XP
    """
    if level <= 1:
        return 0
    return ((level - 1) ** 2) * 100


def get_xp_progress_to_next_level(current_xp: int) -> dict:
    """
    Get XP progress information for current level.

    Returns:
    - current_level: Current player level
    - next_level: Next level
    - xp_for_current_level: XP required for current level
    - xp_for_next_level: XP required for next level
    - xp_progress: XP earned toward next level
    - xp_needed: XP still needed for next level
    - progress_percentage: Percentage progress to next level
    """
    current_level = calculate_level_from_xp(current_xp)
    next_level = current_level + 1

    xp_for_current = calculate_xp_for_level(current_level)
    xp_for_next = calculate_xp_for_level(next_level)

    xp_progress = current_xp - xp_for_current
    xp_needed = xp_for_next - current_xp
    xp_range = xp_for_next - xp_for_current

    progress_percentage = (xp_progress / xp_range * 100) if xp_range > 0 else 0

    return {
        "current_level": current_level,
        "next_level": next_level,
        "xp_for_current_level": xp_for_current,
        "xp_for_next_level": xp_for_next,
        "xp_progress": xp_progress,
        "xp_needed": xp_needed,
        "progress_percentage": round(progress_percentage, 2)
    }


def award_xp(
    player_id: int,
    xp_amount: int,
    db: Session,
    reason: str = ""
) -> dict:
    """
    Award XP to a player and update their level.

    Args:
        player_id: Player ID
        xp_amount: Amount of XP to award (can be negative for penalties)
        db: Database session
        reason: Optional reason for XP award (for logging)

    Returns:
        dict with:
        - previous_xp: XP before award
        - new_xp: XP after award
        - xp_gained: XP amount awarded
        - previous_level: Level before award
        - new_level: Level after award
        - leveled_up: True if player leveled up
        - reason: Reason for XP award
    """
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise ValueError(f"Player with ID {player_id} not found")

    previous_xp = player.xp
    previous_level = player.level

    # Award XP (ensure non-negative)
    player.xp = max(0, player.xp + xp_amount)

    # Recalculate level
    player.level = calculate_level_from_xp(player.xp)

    db.commit()
    db.refresh(player)

    return {
        "previous_xp": previous_xp,
        "new_xp": player.xp,
        "xp_gained": xp_amount,
        "previous_level": previous_level,
        "new_level": player.level,
        "leveled_up": player.level > previous_level,
        "reason": reason
    }


def get_level_title(level: int) -> str:
    """
    Get the title/rank for a given level.

    Level progression:
    1-5: Junior Developer
    6-10: Mid Developer
    11-15: Senior Developer
    16-20: Tech Lead
    21-25: Architect
    26-30: CTO
    31+: Legend
    """
    if level <= 5:
        return "Junior Developer"
    elif level <= 10:
        return "Mid Developer"
    elif level <= 15:
        return "Senior Developer"
    elif level <= 20:
        return "Tech Lead"
    elif level <= 25:
        return "Architect"
    elif level <= 30:
        return "CTO"
    else:
        return "Legend"


def get_player_rank_info(player_id: int, db: Session) -> dict:
    """
    Get complete rank information for a player.

    Returns:
    - level: Current level
    - title: Level title (e.g., "Senior Developer")
    - xp: Total XP
    - xp_progress: Progress info to next level
    """
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise ValueError(f"Player with ID {player_id} not found")

    return {
        "level": player.level,
        "title": get_level_title(player.level),
        "xp": player.xp,
        "xp_progress": get_xp_progress_to_next_level(player.xp)
    }
