"""Tests for Achievement routes."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models.player import Player
from app.models.achievement import PlayerStats


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_achievements.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Create fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_player():
    """Create a test player with stats."""
    db = TestingSessionLocal()
    player = Player(username="achievementtest", avatar="avatar.png")
    db.add(player)
    db.commit()
    db.refresh(player)

    # Create player stats
    stats = PlayerStats(player_id=player.id)
    db.add(stats)
    db.commit()

    player_id = player.id
    db.close()
    return player_id


def test_get_all_achievements():
    """Test getting all available achievements."""
    response = client.get("/api/achievements/")

    assert response.status_code == 200
    data = response.json()

    assert "total_achievements" in data
    assert "achievements" in data
    assert data["total_achievements"] > 0
    assert len(data["achievements"]) == data["total_achievements"]

    # Verify achievement structure
    first_achievement = data["achievements"][0]
    assert "achievement_id" in first_achievement
    assert "title" in first_achievement
    assert "description" in first_achievement
    assert "icon" in first_achievement
    assert "category" in first_achievement
    assert "rarity" in first_achievement
    assert "xp_reward" in first_achievement


def test_get_player_achievements_empty(test_player):
    """Test getting achievements for player with none unlocked."""
    response = client.get(f"/api/achievements/player/{test_player}")

    assert response.status_code == 200
    data = response.json()

    assert data["player_id"] == test_player
    assert data["total_achievements"] == 0
    assert data["achievements"] == []


def test_get_player_achievements_not_found():
    """Test getting achievements for non-existent player returns 404."""
    response = client.get("/api/achievements/player/99999")
    assert response.status_code == 404


def test_unlock_achievement_manually(test_player):
    """Test manually unlocking an achievement."""
    # Get initial XP
    player_response = client.get(f"/api/player/{test_player}")
    initial_xp = player_response.json()["xp"]

    # Unlock achievement
    response = client.post(
        "/api/achievements/unlock",
        json={
            "player_id": test_player,
            "achievement_id": "first_class"
        }
    )

    assert response.status_code == 201
    data = response.json()

    assert data["achievement_id"] == "first_class"
    assert data["player_id"] == test_player
    assert data["title"] == "First Steps"
    assert "unlocked_at" in data
    assert data["xp_reward"] > 0

    # Verify XP was awarded
    player_response = client.get(f"/api/player/{test_player}")
    new_xp = player_response.json()["xp"]
    assert new_xp == initial_xp + data["xp_reward"]


def test_unlock_achievement_duplicate(test_player):
    """Test unlocking same achievement twice returns 409."""
    # Unlock first time
    client.post(
        "/api/achievements/unlock",
        json={
            "player_id": test_player,
            "achievement_id": "first_class"
        }
    )

    # Try to unlock again
    response = client.post(
        "/api/achievements/unlock",
        json={
            "player_id": test_player,
            "achievement_id": "first_class"
        }
    )

    assert response.status_code == 409
    assert "already unlocked" in response.json()["detail"]


def test_unlock_achievement_invalid_id(test_player):
    """Test unlocking non-existent achievement returns 404."""
    response = client.post(
        "/api/achievements/unlock",
        json={
            "player_id": test_player,
            "achievement_id": "nonexistent_achievement"
        }
    )

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_unlock_achievement_invalid_player():
    """Test unlocking achievement for non-existent player returns 404."""
    response = client.post(
        "/api/achievements/unlock",
        json={
            "player_id": 99999,
            "achievement_id": "first_class"
        }
    )

    assert response.status_code == 404
    assert "Player" in response.json()["detail"]


def test_check_achievements_complete_class(test_player):
    """Test auto-checking achievements after completing a class."""
    # Update player stats to have 1 completed class
    db = TestingSessionLocal()
    stats = db.query(PlayerStats).filter(PlayerStats.player_id == test_player).first()
    stats.classes_completed = 1
    db.commit()
    db.close()

    # Check achievements
    response = client.post(
        "/api/achievements/check",
        json={
            "player_id": test_player,
            "action_type": "complete_class",
            "action_data": {"module_number": 0, "class_number": 0}
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert "achievements_unlocked" in data
    assert "xp_earned" in data

    # Should have unlocked "first_class" achievement
    if len(data["achievements_unlocked"]) > 0:
        assert any(
            a["achievement_id"] == "first_class"
            for a in data["achievements_unlocked"]
        )
        assert data["xp_earned"] > 0


def test_check_achievements_bug_hunt_win(test_player):
    """Test auto-checking achievements after Bug Hunt win."""
    # Update player stats to have 1 Bug Hunt win
    db = TestingSessionLocal()
    stats = db.query(PlayerStats).filter(PlayerStats.player_id == test_player).first()
    stats.bug_hunt_wins = 1
    db.commit()
    db.close()

    # Check achievements
    response = client.post(
        "/api/achievements/check",
        json={
            "player_id": test_player,
            "action_type": "bug_hunt_win",
            "action_data": {"accuracy": 100, "time_seconds": 45}
        }
    )

    assert response.status_code == 200
    data = response.json()

    # Should unlock achievements for first Bug Hunt win and possibly perfect/speed
    achievements = data["achievements_unlocked"]
    achievement_ids = [a["achievement_id"] for a in achievements]

    assert "first_bug_hunt" in achievement_ids
    # Should also unlock perfect game (100% accuracy)
    assert "bug_hunt_perfect" in achievement_ids


def test_check_achievements_no_unlocks(test_player):
    """Test checking achievements when none should unlock."""
    # Player with 0 stats, check for 10 classes achievement
    response = client.post(
        "/api/achievements/check",
        json={
            "player_id": test_player,
            "action_type": "complete_class",
            "action_data": {}
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["achievements_unlocked"] == []
    assert data["xp_earned"] == 0


def test_delete_achievement(test_player):
    """Test deleting an achievement."""
    # Unlock achievement
    unlock_response = client.post(
        "/api/achievements/unlock",
        json={
            "player_id": test_player,
            "achievement_id": "first_class"
        }
    )
    achievement_id = unlock_response.json()["id"]

    # Delete achievement
    response = client.delete(f"/api/achievements/{achievement_id}")
    assert response.status_code == 204

    # Verify it's deleted
    player_achievements = client.get(f"/api/achievements/player/{test_player}")
    assert len(player_achievements.json()["achievements"]) == 0


def test_delete_achievement_not_found():
    """Test deleting non-existent achievement returns 404."""
    response = client.delete("/api/achievements/99999")
    assert response.status_code == 404


def test_achievement_categories():
    """Test that achievements have valid categories."""
    response = client.get("/api/achievements/")
    achievements = response.json()["achievements"]

    valid_categories = ["learning", "minigame", "streak", "mastery", "special"]

    for achievement in achievements:
        assert achievement["category"] in valid_categories


def test_achievement_rarities():
    """Test that achievements have valid rarities."""
    response = client.get("/api/achievements/")
    achievements = response.json()["achievements"]

    valid_rarities = ["common", "rare", "epic", "legendary"]

    for achievement in achievements:
        assert achievement["rarity"] in valid_rarities


def test_achievement_xp_rewards():
    """Test that achievement XP rewards are positive."""
    response = client.get("/api/achievements/")
    achievements = response.json()["achievements"]

    for achievement in achievements:
        assert achievement["xp_reward"] > 0


def test_multiple_achievements_unlock():
    """Test multiple achievements can be unlocked at once."""
    # Set player stats to trigger multiple achievements
    db = TestingSessionLocal()
    stats = db.query(PlayerStats).filter(PlayerStats.player_id == test_player).first()
    stats.classes_completed = 10
    db.commit()
    db.close()

    # Check achievements
    response = client.post(
        "/api/achievements/check",
        json={
            "player_id": test_player,
            "action_type": "complete_class",
            "action_data": {}
        }
    )

    data = response.json()
    achievements = data["achievements_unlocked"]

    # Should unlock both "first_class" and "ten_classes"
    achievement_ids = [a["achievement_id"] for a in achievements]
    assert "first_class" in achievement_ids
    assert "ten_classes" in achievement_ids

    # XP should be sum of both achievements
    assert data["xp_earned"] > 0


def test_player_achievements_with_details(test_player):
    """Test that player achievements include full details."""
    # Unlock an achievement
    client.post(
        "/api/achievements/unlock",
        json={
            "player_id": test_player,
            "achievement_id": "first_class"
        }
    )

    # Get player achievements
    response = client.get(f"/api/achievements/player/{test_player}")
    data = response.json()

    assert data["total_achievements"] == 1
    achievement = data["achievements"][0]

    # Verify full details are included
    assert achievement["achievement_id"] == "first_class"
    assert achievement["title"] == "First Steps"
    assert "description" in achievement
    assert "icon" in achievement
    assert "category" in achievement
    assert "rarity" in achievement
    assert "xp_reward" in achievement
    assert "unlocked_at" in achievement
