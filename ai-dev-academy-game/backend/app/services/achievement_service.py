"""Achievement service - Manages achievement definitions and unlocking logic."""

from typing import Dict, List, Optional
from sqlalchemy.orm import Session

from app.models.achievement import Achievement, PlayerStats
from app.models.progress import Progress
from app.schemas.achievement import (
    AchievementDefinition,
    AchievementCategory,
    AchievementRarity,
    AchievementWithDetails
)
from app.services import xp_service


# Achievement definitions - all available achievements in the game
ACHIEVEMENT_DEFINITIONS: Dict[str, AchievementDefinition] = {
    # Learning Achievements
    "first_class": AchievementDefinition(
        achievement_id="first_class",
        title="First Steps",
        description="Complete your first class",
        icon="🎓",
        category=AchievementCategory.LEARNING,
        rarity=AchievementRarity.COMMON,
        xp_reward=50
    ),
    "module_0_complete": AchievementDefinition(
        achievement_id="module_0_complete",
        title="AI Foundations Master",
        description="Complete all classes in Module 0",
        icon="🤖",
        category=AchievementCategory.LEARNING,
        rarity=AchievementRarity.RARE,
        xp_reward=300
    ),
    "module_1_complete": AchievementDefinition(
        achievement_id="module_1_complete",
        title="Python Fundamentals",
        description="Complete all classes in Module 1",
        icon="🐍",
        category=AchievementCategory.LEARNING,
        rarity=AchievementRarity.RARE,
        xp_reward=400
    ),
    "module_2_complete": AchievementDefinition(
        achievement_id="module_2_complete",
        title="Architecture Architect",
        description="Complete all classes in Module 2",
        icon="🏗️",
        category=AchievementCategory.LEARNING,
        rarity=AchievementRarity.EPIC,
        xp_reward=500
    ),
    "module_3_complete": AchievementDefinition(
        achievement_id="module_3_complete",
        title="Security Guardian",
        description="Complete all classes in Module 3",
        icon="🛡️",
        category=AchievementCategory.LEARNING,
        rarity=AchievementRarity.EPIC,
        xp_reward=600
    ),
    "module_4_complete": AchievementDefinition(
        achievement_id="module_4_complete",
        title="Infrastructure Expert",
        description="Complete all classes in Module 4",
        icon="☁️",
        category=AchievementCategory.LEARNING,
        rarity=AchievementRarity.EPIC,
        xp_reward=700
    ),
    "module_5_complete": AchievementDefinition(
        achievement_id="module_5_complete",
        title="Full-Stack Master",
        description="Complete all classes in Module 5",
        icon="🚀",
        category=AchievementCategory.LEARNING,
        rarity=AchievementRarity.LEGENDARY,
        xp_reward=1000
    ),
    "ten_classes": AchievementDefinition(
        achievement_id="ten_classes",
        title="Dedicated Learner",
        description="Complete 10 classes",
        icon="📚",
        category=AchievementCategory.LEARNING,
        rarity=AchievementRarity.COMMON,
        xp_reward=200
    ),
    "twenty_classes": AchievementDefinition(
        achievement_id="twenty_classes",
        title="Knowledge Seeker",
        description="Complete 20 classes",
        icon="🔍",
        category=AchievementCategory.LEARNING,
        rarity=AchievementRarity.RARE,
        xp_reward=500
    ),
    "half_curriculum": AchievementDefinition(
        achievement_id="half_curriculum",
        title="Halfway There",
        description="Complete 50% of the curriculum",
        icon="🎯",
        category=AchievementCategory.LEARNING,
        rarity=AchievementRarity.EPIC,
        xp_reward=800
    ),
    "curriculum_complete": AchievementDefinition(
        achievement_id="curriculum_complete",
        title="Master Graduate",
        description="Complete the entire curriculum",
        icon="👑",
        category=AchievementCategory.MASTERY,
        rarity=AchievementRarity.LEGENDARY,
        xp_reward=2000
    ),

    # Minigame Achievements - Bug Hunt
    "first_bug_hunt": AchievementDefinition(
        achievement_id="first_bug_hunt",
        title="Bug Hunter Initiate",
        description="Win your first Bug Hunt game",
        icon="🐛",
        category=AchievementCategory.MINIGAME,
        rarity=AchievementRarity.COMMON,
        xp_reward=100
    ),
    "bug_hunt_5_wins": AchievementDefinition(
        achievement_id="bug_hunt_5_wins",
        title="Bug Slayer",
        description="Win 5 Bug Hunt games",
        icon="⚔️",
        category=AchievementCategory.MINIGAME,
        rarity=AchievementRarity.RARE,
        xp_reward=300
    ),
    "bug_hunt_10_wins": AchievementDefinition(
        achievement_id="bug_hunt_10_wins",
        title="Bug Exterminator",
        description="Win 10 Bug Hunt games",
        icon="💀",
        category=AchievementCategory.MINIGAME,
        rarity=AchievementRarity.EPIC,
        xp_reward=600
    ),
    "bug_hunt_perfect": AchievementDefinition(
        achievement_id="bug_hunt_perfect",
        title="Perfect Hunt",
        description="Win a Bug Hunt game with 100% accuracy",
        icon="💯",
        category=AchievementCategory.MINIGAME,
        rarity=AchievementRarity.EPIC,
        xp_reward=500
    ),
    "bug_hunt_speed_demon": AchievementDefinition(
        achievement_id="bug_hunt_speed_demon",
        title="Speed Demon",
        description="Win a Bug Hunt game in under 60 seconds",
        icon="⚡",
        category=AchievementCategory.MINIGAME,
        rarity=AchievementRarity.RARE,
        xp_reward=400
    ),

    # Streak Achievements
    "three_day_streak": AchievementDefinition(
        achievement_id="three_day_streak",
        title="Consistent Learner",
        description="Complete classes 3 days in a row",
        icon="🔥",
        category=AchievementCategory.STREAK,
        rarity=AchievementRarity.COMMON,
        xp_reward=150
    ),
    "seven_day_streak": AchievementDefinition(
        achievement_id="seven_day_streak",
        title="Week Warrior",
        description="Complete classes 7 days in a row",
        icon="🌟",
        category=AchievementCategory.STREAK,
        rarity=AchievementRarity.RARE,
        xp_reward=400
    ),
    "thirty_day_streak": AchievementDefinition(
        achievement_id="thirty_day_streak",
        title="Unstoppable",
        description="Complete classes 30 days in a row",
        icon="💎",
        category=AchievementCategory.STREAK,
        rarity=AchievementRarity.LEGENDARY,
        xp_reward=1500
    ),

    # Mastery Achievements
    "hundred_exercises": AchievementDefinition(
        achievement_id="hundred_exercises",
        title="Exercise Master",
        description="Complete 100 exercises",
        icon="💪",
        category=AchievementCategory.MASTERY,
        rarity=AchievementRarity.EPIC,
        xp_reward=800
    ),
    "all_modules_started": AchievementDefinition(
        achievement_id="all_modules_started",
        title="Explorer",
        description="Start at least one class in every module",
        icon="🗺️",
        category=AchievementCategory.MASTERY,
        rarity=AchievementRarity.RARE,
        xp_reward=500
    ),

    # Special Achievements
    "early_adopter": AchievementDefinition(
        achievement_id="early_adopter",
        title="Early Adopter",
        description="Created account in the first month",
        icon="🌅",
        category=AchievementCategory.SPECIAL,
        rarity=AchievementRarity.RARE,
        xp_reward=250
    ),
    "night_owl": AchievementDefinition(
        achievement_id="night_owl",
        title="Night Owl",
        description="Complete a class between midnight and 4am",
        icon="🦉",
        category=AchievementCategory.SPECIAL,
        rarity=AchievementRarity.COMMON,
        xp_reward=100
    ),
    "weekend_warrior": AchievementDefinition(
        achievement_id="weekend_warrior",
        title="Weekend Warrior",
        description="Complete 5 classes on weekends",
        icon="🏖️",
        category=AchievementCategory.SPECIAL,
        rarity=AchievementRarity.RARE,
        xp_reward=300
    ),
}


def get_all_achievement_definitions() -> List[AchievementDefinition]:
    """Get all available achievement definitions."""
    return list(ACHIEVEMENT_DEFINITIONS.values())


def get_achievement_definition(achievement_id: str) -> Optional[AchievementDefinition]:
    """Get a specific achievement definition."""
    return ACHIEVEMENT_DEFINITIONS.get(achievement_id)


def check_and_unlock_achievements(
    player_id: int,
    action_type: str,
    action_data: Optional[dict],
    db: Session
) -> List[AchievementWithDetails]:
    """
    Check if any achievements should be unlocked based on an action.

    Args:
        player_id: Player ID
        action_type: Type of action (e.g., 'complete_class', 'bug_hunt_win')
        action_data: Additional data about the action
        db: Database session

    Returns:
        List of newly unlocked achievements
    """
    newly_unlocked = []

    # Get player stats
    stats = db.query(PlayerStats).filter(PlayerStats.player_id == player_id).first()
    if not stats:
        return []

    # Get already unlocked achievements
    existing_achievements = db.query(Achievement).filter(
        Achievement.player_id == player_id
    ).all()
    existing_ids = {a.achievement_id for a in existing_achievements}

    # Check achievements based on action type
    if action_type == "complete_class":
        newly_unlocked.extend(_check_class_completion_achievements(
            player_id, stats, existing_ids, action_data, db
        ))
    elif action_type == "bug_hunt_win":
        newly_unlocked.extend(_check_bug_hunt_achievements(
            player_id, stats, existing_ids, action_data, db
        ))
    elif action_type == "complete_exercise":
        newly_unlocked.extend(_check_exercise_achievements(
            player_id, stats, existing_ids, db
        ))

    return newly_unlocked


def _check_class_completion_achievements(
    player_id: int,
    stats: PlayerStats,
    existing_ids: set,
    action_data: Optional[dict],
    db: Session
) -> List[AchievementWithDetails]:
    """Check achievements related to class completion."""
    unlocked = []

    # First class
    if "first_class" not in existing_ids and stats.classes_completed == 1:
        unlocked.append(_unlock_achievement(player_id, "first_class", db))

    # 10 classes
    if "ten_classes" not in existing_ids and stats.classes_completed >= 10:
        unlocked.append(_unlock_achievement(player_id, "ten_classes", db))

    # 20 classes
    if "twenty_classes" not in existing_ids and stats.classes_completed >= 20:
        unlocked.append(_unlock_achievement(player_id, "twenty_classes", db))

    # Module completion (check if all classes in a module are completed)
    if action_data and "module_number" in action_data:
        module_num = action_data["module_number"]
        achievement_id = f"module_{module_num}_complete"

        if achievement_id not in existing_ids and _is_module_complete(player_id, module_num, db):
            unlocked.append(_unlock_achievement(player_id, achievement_id, db))

    # 50% curriculum
    total_classes = 45  # Approximate total from content_service
    if "half_curriculum" not in existing_ids and stats.classes_completed >= total_classes / 2:
        unlocked.append(_unlock_achievement(player_id, "half_curriculum", db))

    # Full curriculum
    if "curriculum_complete" not in existing_ids and stats.classes_completed >= total_classes:
        unlocked.append(_unlock_achievement(player_id, "curriculum_complete", db))

    return [a for a in unlocked if a is not None]


def _check_bug_hunt_achievements(
    player_id: int,
    stats: PlayerStats,
    existing_ids: set,
    action_data: Optional[dict],
    db: Session
) -> List[AchievementWithDetails]:
    """Check achievements related to Bug Hunt mini-game."""
    unlocked = []

    # First win
    if "first_bug_hunt" not in existing_ids and stats.bug_hunt_wins == 1:
        unlocked.append(_unlock_achievement(player_id, "first_bug_hunt", db))

    # 5 wins
    if "bug_hunt_5_wins" not in existing_ids and stats.bug_hunt_wins >= 5:
        unlocked.append(_unlock_achievement(player_id, "bug_hunt_5_wins", db))

    # 10 wins
    if "bug_hunt_10_wins" not in existing_ids and stats.bug_hunt_wins >= 10:
        unlocked.append(_unlock_achievement(player_id, "bug_hunt_10_wins", db))

    # Perfect game (100% accuracy)
    if action_data and "accuracy" in action_data:
        if "bug_hunt_perfect" not in existing_ids and action_data["accuracy"] == 100:
            unlocked.append(_unlock_achievement(player_id, "bug_hunt_perfect", db))

    # Speed demon (under 60 seconds)
    if action_data and "time_seconds" in action_data:
        if "bug_hunt_speed_demon" not in existing_ids and action_data["time_seconds"] < 60:
            unlocked.append(_unlock_achievement(player_id, "bug_hunt_speed_demon", db))

    return [a for a in unlocked if a is not None]


def _check_exercise_achievements(
    player_id: int,
    stats: PlayerStats,
    existing_ids: set,
    db: Session
) -> List[AchievementWithDetails]:
    """Check achievements related to exercise completion."""
    unlocked = []

    # 100 exercises
    if "hundred_exercises" not in existing_ids and stats.exercises_completed >= 100:
        unlocked.append(_unlock_achievement(player_id, "hundred_exercises", db))

    return [a for a in unlocked if a is not None]


def _is_module_complete(player_id: int, module_number: int, db: Session) -> bool:
    """Check if all classes in a module are completed."""
    from app.services import content_service

    module_info = content_service.get_module_info(module_number)
    if not module_info:
        return False

    total_classes = len(module_info.classes)

    # Count completed classes in this module
    from app.schemas.progress import ProgressStatus
    completed_count = db.query(Progress).filter(
        Progress.player_id == player_id,
        Progress.module_number == module_number,
        Progress.status == ProgressStatus.COMPLETED
    ).count()

    return completed_count == total_classes


def _unlock_achievement(
    player_id: int,
    achievement_id: str,
    db: Session
) -> Optional[AchievementWithDetails]:
    """Unlock an achievement for a player."""
    # Check if already unlocked
    existing = db.query(Achievement).filter(
        Achievement.player_id == player_id,
        Achievement.achievement_id == achievement_id
    ).first()

    if existing:
        return None

    # Get achievement definition
    definition = get_achievement_definition(achievement_id)
    if not definition:
        return None

    # Create achievement record
    new_achievement = Achievement(
        player_id=player_id,
        achievement_id=achievement_id
    )

    db.add(new_achievement)
    db.flush()

    # Award XP using centralized service
    xp_service.award_xp(
        player_id=player_id,
        xp_amount=definition.xp_reward,
        db=db,
        reason=f"Unlocked achievement: {definition.title}"
    )

    db.commit()
    db.refresh(new_achievement)

    # Return achievement with details
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
