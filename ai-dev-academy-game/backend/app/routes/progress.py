"""Progress routes - Track player progress through curriculum."""

from datetime import datetime

from app.database import get_db
from app.models.achievement import PlayerStats
from app.models.player import Player
from app.models.progress import Progress
from app.schemas.progress import (
    ClassInfoResponse,
    ClassProgress,
    FullProgressResponse,
    ModuleInfoResponse,
    ModuleProgressResponse,
    ProgressCreate,
    ProgressResponse,
    ProgressStatus,
    ProgressUpdate,
)
from app.services import content_service, xp_service
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


# IMPORTANT: Specific routes (like /modules) MUST come BEFORE path parameter routes (like /{player_id})
# Otherwise FastAPI will try to parse "modules" as a player_id integer and return 422


@router.get("/modules", response_model=list[ModuleInfoResponse])
async def get_all_modules(course_id: str = "master-ia"):
    """
    Get all modules with their class information from the curriculum.

    Args:
        course_id: Course identifier (default: "master-ia" for backward compatibility)

    Returns curriculum metadata (not player progress).

    NFLOW-1: Added course_id parameter to support multi-course platform.
    Default value maintains backward compatibility with existing frontend.
    """
    from app.core.course_manager import course_manager

    course = course_manager.get_course(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course '{course_id}' not found"
        )

    modules = course.get_modules()

    result = []
    for module in modules:
        classes = [
            ClassInfoResponse(
                class_number=c["id"],
                title=c["title"],
                description=c["description"],
                exercises_count=c["exercises_count"],
                xp_reward=c["xp_reward"]
            )
            for c in module["classes"]
        ]

        result.append(ModuleInfoResponse(
            module_number=module["id"],
            title=module["name"],
            description=module["description"],
            total_classes=len(module["classes"]),
            classes=classes
        ))

    return result


@router.get("/modules/{module_number}", response_model=ModuleInfoResponse)
async def get_module_info(module_number: int):
    """
    Get specific module information from the curriculum.

    Returns curriculum metadata (not player progress).
    """
    module = content_service.get_module_info(module_number)

    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Module {module_number} not found in curriculum"
        )

    classes = [
        ClassInfoResponse(
            class_number=c.class_number,
            title=c.title,
            description=c.description,
            exercises_count=c.exercises_count,
            xp_reward=c.xp_reward,
            difficulty=c.difficulty,
            estimated_time_minutes=c.estimated_time_minutes,
            prerequisites=c.prerequisites,
            learning_objectives=c.learning_objectives
        )
        for c in module.classes
    ]

    return ModuleInfoResponse(
        module_number=module.module_number,
        title=module.title,
        description=module.description,
        total_classes=len(module.classes),
        classes=classes
    )


@router.post("/", response_model=ProgressResponse, status_code=status.HTTP_201_CREATED)
async def create_or_unlock_class(
    progress_data: ProgressCreate,
    db: Session = Depends(get_db)
):
    """
    Create/unlock a class for a player.

    Validates that:
    - Player exists
    - Class exists in curriculum
    - Prerequisites are met (previous classes completed)
    """
    # Validate player exists
    player = db.query(Player).filter(Player.id == progress_data.player_id).first()
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {progress_data.player_id} not found"
        )

    # Validate class exists in curriculum
    class_info = content_service.get_class_info(
        progress_data.module_number,
        progress_data.class_number
    )
    if not class_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Class {progress_data.module_number}.{progress_data.class_number} not found in curriculum"
        )

    # Check if progress already exists
    existing = db.query(Progress).filter(
        Progress.player_id == progress_data.player_id,
        Progress.module_number == progress_data.module_number,
        Progress.class_number == progress_data.class_number
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Progress already exists for class {progress_data.module_number}.{progress_data.class_number}"
        )

    # Get completed classes for prerequisite check
    completed = db.query(Progress).filter(
        Progress.player_id == progress_data.player_id,
        Progress.status == ProgressStatus.COMPLETED
    ).all()

    completed_tuples = [
        (p.module_number, p.class_number) for p in completed
    ]

    # Check prerequisites
    can_unlock = content_service.is_class_unlockable(
        progress_data.module_number,
        progress_data.class_number,
        completed_tuples
    )

    if not can_unlock:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Prerequisites not met for class {progress_data.module_number}.{progress_data.class_number}"
        )

    # Create progress
    new_progress = Progress(
        player_id=progress_data.player_id,
        module_number=progress_data.module_number,
        class_number=progress_data.class_number,
        status=progress_data.status,
        exercises_completed=0
    )

    db.add(new_progress)
    db.commit()
    db.refresh(new_progress)

    return new_progress


@router.get("/{player_id}", response_model=FullProgressResponse)
async def get_full_progress(
    player_id: int,
    db: Session = Depends(get_db)
):
    """
    Get complete progress for a player across all modules.

    Returns:
    - Overall progress percentage
    - Total classes completed
    - Total exercises completed
    - Detailed progress per module
    """
    # Validate player exists
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found"
        )

    # Get all progress for player
    all_progress = db.query(Progress).filter(
        Progress.player_id == player_id
    ).all()

    # Create progress dict for quick lookup
    progress_dict = {
        (p.module_number, p.class_number): p
        for p in all_progress
    }

    # Build module progress
    modules_response = []
    total_classes_completed = 0
    total_exercises = sum(p.exercises_completed for p in all_progress)

    for module_info in content_service.get_all_modules():
        classes_progress = []
        completed_in_module = 0

        for class_info in module_info.classes:
            prog = progress_dict.get((module_info.module_number, class_info.class_number))

            if prog:
                class_progress = ClassProgress(
                    id=prog.id,  # Include progress ID for frontend
                    class_number=class_info.class_number,
                    status=prog.status,
                    exercises_completed=prog.exercises_completed,
                    completed_at=prog.completed_at
                )
                if prog.status == ProgressStatus.COMPLETED:
                    completed_in_module += 1
                    total_classes_completed += 1
            else:
                # Class not yet unlocked
                class_progress = ClassProgress(
                    id=None,  # No progress record yet
                    class_number=class_info.class_number,
                    status=ProgressStatus.LOCKED,
                    exercises_completed=0,
                    completed_at=None
                )

            classes_progress.append(class_progress)

        module_progress = ModuleProgressResponse(
            module_number=module_info.module_number,
            module_name=module_info.title,
            total_classes=len(module_info.classes),
            completed_classes=completed_in_module,
            progress_percentage=content_service.get_module_progress(
                module_info.module_number,
                completed_in_module
            ),
            classes=classes_progress
        )

        modules_response.append(module_progress)

    # Calculate overall progress
    total_classes = content_service.get_total_classes()
    overall_percentage = content_service.calculate_progress_percentage(
        total_classes_completed,
        total_classes
    )

    return FullProgressResponse(
        player_id=player_id,
        total_classes_completed=total_classes_completed,
        total_exercises_completed=total_exercises,
        overall_progress_percentage=overall_percentage,
        modules=modules_response
    )


@router.get("/{player_id}/module/{module_number}", response_model=ModuleProgressResponse)
async def get_module_progress(
    player_id: int,
    module_number: int,
    db: Session = Depends(get_db)
):
    """Get progress for a specific module."""
    # Validate player exists
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found"
        )

    # Validate module exists
    module_info = content_service.get_module_info(module_number)
    if not module_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Module {module_number} not found in curriculum"
        )

    # Get progress for this module
    module_progress = db.query(Progress).filter(
        Progress.player_id == player_id,
        Progress.module_number == module_number
    ).all()

    progress_dict = {p.class_number: p for p in module_progress}

    classes_progress = []
    completed_count = 0

    for class_info in module_info.classes:
        prog = progress_dict.get(class_info.class_number)

        if prog:
            class_progress = ClassProgress(
                id=prog.id,  # Include progress ID for frontend
                class_number=class_info.class_number,
                status=prog.status,
                exercises_completed=prog.exercises_completed,
                completed_at=prog.completed_at
            )
            if prog.status == ProgressStatus.COMPLETED:
                completed_count += 1
        else:
            class_progress = ClassProgress(
                id=None,  # No progress record yet
                class_number=class_info.class_number,
                status=ProgressStatus.LOCKED,
                exercises_completed=0,
                completed_at=None
            )

        classes_progress.append(class_progress)

    progress_percentage = content_service.get_module_progress(
        module_number,
        completed_count
    )

    return ModuleProgressResponse(
        module_number=module_number,
        module_name=module_info.title,
        total_classes=len(module_info.classes),
        completed_classes=completed_count,
        progress_percentage=progress_percentage,
        classes=classes_progress
    )


@router.patch("/{progress_id}", response_model=ProgressResponse)
async def update_progress(
    progress_id: int,
    progress_data: ProgressUpdate,
    db: Session = Depends(get_db)
):
    """
    Update progress for a class.

    Can update:
    - Status (e.g., mark as completed)
    - Exercises completed count

    When marking as completed:
    - Awards XP to player
    - Updates player stats
    - Unlocks next class if prerequisites met
    """
    progress = db.query(Progress).filter(Progress.id == progress_id).first()

    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Progress with ID {progress_id} not found"
        )

    # Get class info for XP reward
    class_info = content_service.get_class_info(
        progress.module_number,
        progress.class_number
    )

    # Update status if provided
    if progress_data.status:
        old_status = progress.status
        progress.status = progress_data.status

        # If marking as completed
        if progress_data.status == ProgressStatus.COMPLETED and old_status != ProgressStatus.COMPLETED:
            progress.completed_at = datetime.utcnow()

            # Award XP using centralized service
            if class_info:
                xp_service.award_xp(
                    player_id=progress.player_id,
                    xp_amount=class_info.xp_reward,
                    db=db,
                    reason=f"Completed class {progress.module_number}.{progress.class_number}"
                )

                # Update player stats
                stats = db.query(PlayerStats).filter(
                    PlayerStats.player_id == progress.player_id
                ).first()
                if stats:
                    stats.classes_completed += 1

        # If marking as in_progress for the first time
        elif progress_data.status == ProgressStatus.IN_PROGRESS and not progress.started_at:
            progress.started_at = datetime.utcnow()

    # Update exercises completed if provided
    if progress_data.exercises_completed is not None:
        old_count = progress.exercises_completed
        progress.exercises_completed = progress_data.exercises_completed

        # Update player stats
        if progress_data.exercises_completed > old_count:
            stats = db.query(PlayerStats).filter(
                PlayerStats.player_id == progress.player_id
            ).first()
            if stats:
                stats.exercises_completed += (progress_data.exercises_completed - old_count)

    db.commit()
    db.refresh(progress)

    return progress


@router.get("/{player_id}/next-unlockable")
async def get_next_unlockable(
    player_id: int,
    db: Session = Depends(get_db)
):
    """
    Get the next class that can be unlocked for this player.

    Returns module_number and class_number, or null if curriculum is complete.
    """
    # Validate player exists
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found"
        )

    # Get completed classes
    completed = db.query(Progress).filter(
        Progress.player_id == player_id,
        Progress.status == ProgressStatus.COMPLETED
    ).all()

    completed_tuples = [
        (p.module_number, p.class_number) for p in completed
    ]

    # Get next unlockable
    next_class = content_service.get_next_unlockable_class(completed_tuples)

    if next_class:
        module_number, class_number = next_class
        class_info = content_service.get_class_info(module_number, class_number)

        return {
            "module_number": module_number,
            "class_number": class_number,
            "title": class_info.title if class_info else "Unknown",
            "description": class_info.description if class_info else "",
            "xp_reward": class_info.xp_reward if class_info else 0
        }

    return {
        "module_number": None,
        "class_number": None,
        "message": "Curriculum complete! Congratulations!"
    }
