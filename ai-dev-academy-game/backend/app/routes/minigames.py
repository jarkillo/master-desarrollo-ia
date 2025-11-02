"""Minigames API routes - Bug Hunt and other mini-games."""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.database import get_db
from app.models import BugHuntGame, Player, PlayerStats
from app.schemas.minigame import (
    BugHuntStartRequest,
    BugHuntStartResponse,
    BugHuntSubmitRequest,
    BugHuntSubmitResponse,
    BugResult,
    LeaderboardResponse,
    LeaderboardEntry,
    PlayerBugHuntStatsResponse
)
from app.content.bug_templates import get_random_template, get_template_by_id, BugTemplate


router = APIRouter()


# Bug Hunt Endpoints

@router.post("/bug-hunt/start", response_model=BugHuntStartResponse)
async def start_bug_hunt(
    request: BugHuntStartRequest,
    db: Session = Depends(get_db)
):
    """
    Start a new Bug Hunt game session.

    - **player_id**: ID of the player starting the game
    - **difficulty**: Optional difficulty level (easy, medium, hard)

    Returns a code snippet with bugs and a session ID for submission.
    """
    # Verify player exists
    player = db.query(Player).filter(Player.id == request.player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Get random template based on difficulty
    try:
        template: BugTemplate = get_random_template(difficulty=request.difficulty)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Create game session
    started_at = datetime.utcnow()
    game_session = BugHuntGame(
        player_id=request.player_id,
        template_id=template.id,
        difficulty=template.difficulty,
        bugs_total=len(template.bugs),
        bugs_found=0,
        time_seconds=0,
        score=0,
        xp_earned=0,
        started_at=started_at
    )

    db.add(game_session)
    db.commit()
    db.refresh(game_session)

    return BugHuntStartResponse(
        session_id=game_session.id,
        template_id=template.id,
        title=template.title,
        description=template.description,
        difficulty=template.difficulty,
        code=template.code,
        bugs_count=len(template.bugs),
        max_xp=template.xp_reward,
        started_at=started_at
    )


def calculate_bug_hunt_score(
    bugs_found: int,
    bugs_total: int,
    time_seconds: float,
    false_positives: int,
    difficulty: str
) -> tuple[int, int]:
    """
    Calculate score and XP for Bug Hunt game.

    Returns: (score, xp_earned)
    """
    # Base score from bugs found
    base_score = (bugs_found / bugs_total) * 1000 if bugs_total > 0 else 0

    # Accuracy penalty for false positives
    if false_positives > 0:
        base_score -= false_positives * 100

    # Time bonus (faster = better, max 200 bonus points)
    # Perfect time thresholds by difficulty
    time_thresholds = {
        "easy": 60,    # 1 minute
        "medium": 120,  # 2 minutes
        "hard": 180     # 3 minutes
    }
    threshold = time_thresholds.get(difficulty, 120)
    time_bonus = max(0, int(200 * (1 - min(time_seconds / threshold, 1))))

    # Calculate final score
    score = max(0, int(base_score + time_bonus))

    # XP calculation
    xp_multipliers = {
        "easy": 50,
        "medium": 75,
        "hard": 100
    }
    base_xp = xp_multipliers.get(difficulty, 50)

    # Perfect game bonus
    perfect_bonus = 0
    if bugs_found == bugs_total and false_positives == 0:
        perfect_bonus = 50

    # Speed bonus
    speed_bonus = min(25, time_bonus // 4)

    xp_earned = base_xp + perfect_bonus + speed_bonus

    return score, xp_earned


@router.post("/bug-hunt/submit", response_model=BugHuntSubmitResponse)
async def submit_bug_hunt(
    request: BugHuntSubmitRequest,
    db: Session = Depends(get_db)
):
    """
    Submit Bug Hunt answers and get results.

    - **session_id**: Game session ID from start response
    - **player_id**: Player ID
    - **found_bug_lines**: List of line numbers identified as bugs
    - **time_seconds**: Time taken to complete

    Returns score, XP earned, and detailed results.
    """
    # Get game session
    game_session = db.query(BugHuntGame).filter(BugHuntGame.id == request.session_id).first()
    if not game_session:
        raise HTTPException(status_code=404, detail="Game session not found")

    # Verify player
    if game_session.player_id != request.player_id:
        raise HTTPException(status_code=403, detail="This session belongs to another player")

    # Get template to validate answers
    try:
        template = get_template_by_id(game_session.template_id)
    except ValueError:
        raise HTTPException(status_code=500, detail="Template not found")

    # Extract correct bug lines from template
    correct_bug_lines = {bug["line"] for bug in template.bugs}
    submitted_lines = set(request.found_bug_lines)

    # Calculate results
    found_correct = submitted_lines & correct_bug_lines
    missed_bugs = correct_bug_lines - submitted_lines
    false_positives_set = submitted_lines - correct_bug_lines

    bugs_found = len(found_correct)
    bugs_missed = len(missed_bugs)
    false_positives_count = len(false_positives_set)

    # Calculate score and XP
    score, xp_earned = calculate_bug_hunt_score(
        bugs_found=bugs_found,
        bugs_total=len(correct_bug_lines),
        time_seconds=request.time_seconds,
        false_positives=false_positives_count,
        difficulty=template.difficulty
    )

    # Build detailed results
    results = []
    for bug in template.bugs:
        line = bug["line"]
        was_found = line in submitted_lines
        results.append(BugResult(
            line=line,
            found=was_found,
            is_correct=True,
            bug_type=bug["type"],
            description=bug["description"]
        ))

    # Add false positives to results
    for line in false_positives_set:
        results.append(BugResult(
            line=line,
            found=True,
            is_correct=False,
            bug_type=None,
            description="No bug on this line"
        ))

    # Calculate accuracy
    accuracy = (bugs_found / len(correct_bug_lines)) * 100 if correct_bug_lines else 0

    # Check if perfect game
    is_perfect = bugs_found == len(correct_bug_lines) and false_positives_count == 0

    # Update game session
    game_session.bugs_found = bugs_found
    game_session.time_seconds = request.time_seconds
    game_session.score = score
    game_session.xp_earned = xp_earned
    game_session.found_bugs = list(found_correct)
    game_session.missed_bugs = list(missed_bugs)
    game_session.false_positives = list(false_positives_set)
    game_session.completed_at = datetime.utcnow()

    # Update player XP
    player = db.query(Player).filter(Player.id == request.player_id).first()
    if player:
        player.xp += xp_earned
        # Update level based on XP (Level = floor(sqrt(XP / 100)) + 1)
        import math
        player.level = math.floor(math.sqrt(player.xp / 100)) + 1

    # Update player stats
    stats = db.query(PlayerStats).filter(PlayerStats.player_id == request.player_id).first()
    if not stats:
        stats = PlayerStats(
            player_id=request.player_id,
            bug_hunt_games_played=1,
            bug_hunt_wins=1 if is_perfect else 0,
            last_activity_date=datetime.utcnow()
        )
        db.add(stats)
    else:
        stats.bug_hunt_games_played += 1
        if is_perfect:
            stats.bug_hunt_wins += 1
        stats.last_activity_date = datetime.utcnow()

    db.commit()

    # Check for achievements (simplified - could be more sophisticated)
    achievements_unlocked = []
    if is_perfect:
        achievements_unlocked.append("bug_hunter")

    return BugHuntSubmitResponse(
        success=True,
        score=score,
        xp_earned=xp_earned,
        bugs_found=bugs_found,
        bugs_total=len(correct_bug_lines),
        bugs_missed=bugs_missed,
        false_positives=false_positives_count,
        accuracy=accuracy,
        time_seconds=request.time_seconds,
        is_perfect=is_perfect,
        results=results,
        performance_bonus=xp_earned - template.xp_reward if xp_earned > template.xp_reward else 0,
        achievements_unlocked=achievements_unlocked
    )


@router.get("/bug-hunt/leaderboard", response_model=LeaderboardResponse)
async def get_bug_hunt_leaderboard(
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    limit: int = Query(10, ge=1, le=100, description="Number of entries to return"),
    db: Session = Depends(get_db)
):
    """
    Get Bug Hunt leaderboard.

    - **difficulty**: Optional filter by difficulty (easy, medium, hard)
    - **limit**: Number of entries to return (1-100)

    Returns top scores globally or filtered by difficulty.
    """
    # Build query
    query = db.query(
        BugHuntGame,
        Player.username
    ).join(Player, BugHuntGame.player_id == Player.id)

    # Apply difficulty filter if specified
    if difficulty:
        if difficulty not in ["easy", "medium", "hard"]:
            raise HTTPException(status_code=400, detail="Invalid difficulty. Must be: easy, medium, or hard")
        query = query.filter(BugHuntGame.difficulty == difficulty)

    # Order by score descending and limit
    query = query.order_by(desc(BugHuntGame.score)).limit(limit)

    results = query.all()

    # Build leaderboard entries
    entries = []
    for rank, (game, username) in enumerate(results, start=1):
        entries.append(LeaderboardEntry(
            rank=rank,
            player_id=game.player_id,
            username=username,
            score=game.score,
            bugs_found=game.bugs_found,
            bugs_total=game.bugs_total,
            time_seconds=game.time_seconds,
            accuracy=game.accuracy,
            difficulty=game.difficulty,
            completed_at=game.completed_at
        ))

    total_count = db.query(func.count(BugHuntGame.id))
    if difficulty:
        total_count = total_count.filter(BugHuntGame.difficulty == difficulty)
    total_count = total_count.scalar()

    return LeaderboardResponse(
        total_entries=total_count or 0,
        entries=entries,
        difficulty_filter=difficulty
    )


@router.get("/bug-hunt/stats/{player_id}", response_model=PlayerBugHuntStatsResponse)
async def get_player_bug_hunt_stats(
    player_id: int,
    db: Session = Depends(get_db)
):
    """
    Get Bug Hunt statistics for a specific player.

    - **player_id**: Player ID

    Returns aggregated statistics for the player's Bug Hunt games.
    """
    # Verify player exists
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Get all games for player
    games = db.query(BugHuntGame).filter(BugHuntGame.player_id == player_id).all()

    if not games:
        return PlayerBugHuntStatsResponse(
            total_games_played=0,
            total_bugs_found=0,
            total_perfect_games=0,
            best_score=0,
            average_score=0.0,
            average_accuracy=0.0,
            favorite_difficulty=None,
            total_xp_earned=0
        )

    # Calculate stats
    total_games = len(games)
    total_bugs_found = sum(g.bugs_found for g in games)
    total_perfect_games = sum(1 for g in games if g.is_perfect)
    best_score = max(g.score for g in games)
    average_score = sum(g.score for g in games) / total_games
    average_accuracy = sum(g.accuracy for g in games) / total_games
    total_xp_earned = sum(g.xp_earned for g in games)

    # Find favorite difficulty (most played)
    difficulty_counts = {}
    for game in games:
        difficulty_counts[game.difficulty] = difficulty_counts.get(game.difficulty, 0) + 1

    favorite_difficulty = max(difficulty_counts, key=difficulty_counts.get) if difficulty_counts else None

    return PlayerBugHuntStatsResponse(
        total_games_played=total_games,
        total_bugs_found=total_bugs_found,
        total_perfect_games=total_perfect_games,
        best_score=best_score,
        average_score=average_score,
        average_accuracy=average_accuracy,
        favorite_difficulty=favorite_difficulty,
        total_xp_earned=total_xp_earned
    )
