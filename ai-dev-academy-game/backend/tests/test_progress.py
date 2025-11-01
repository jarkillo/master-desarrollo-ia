"""Tests for Progress routes."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models.player import Player
from app.models.progress import PlayerStats


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_progress.db"
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
    player = Player(username="progresstest", avatar="avatar.png")
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


def test_create_progress_first_class(test_player):
    """Test creating progress for first class (Module 0, Class 0)."""
    response = client.post(
        "/api/progress/",
        json={
            "player_id": test_player,
            "module_number": 0,
            "class_number": 0,
            "status": "unlocked"
        }
    )

    assert response.status_code == 201
    data = response.json()

    assert data["player_id"] == test_player
    assert data["module_number"] == 0
    assert data["class_number"] == 0
    assert data["status"] == "unlocked"
    assert data["exercises_completed"] == 0
    assert "id" in data


def test_create_progress_without_prerequisites():
    """Test creating progress without meeting prerequisites returns 403."""
    # Create player
    create_response = client.post(
        "/api/player/",
        json={"username": "noprerequis", "avatar": "avatar.png"}
    )
    player_id = create_response.json()["id"]

    # Try to unlock Module 0, Class 1 without completing Class 0
    response = client.post(
        "/api/progress/",
        json={
            "player_id": player_id,
            "module_number": 0,
            "class_number": 1,
            "status": "unlocked"
        }
    )

    assert response.status_code == 403
    assert "Prerequisites not met" in response.json()["detail"]


def test_create_progress_duplicate():
    """Test creating duplicate progress returns 409."""
    # Create player and unlock first class
    create_response = client.post(
        "/api/player/",
        json={"username": "duptest", "avatar": "avatar.png"}
    )
    player_id = create_response.json()["id"]

    # Create first progress
    client.post(
        "/api/progress/",
        json={
            "player_id": player_id,
            "module_number": 0,
            "class_number": 0,
            "status": "unlocked"
        }
    )

    # Try to create duplicate
    response = client.post(
        "/api/progress/",
        json={
            "player_id": player_id,
            "module_number": 0,
            "class_number": 0,
            "status": "unlocked"
        }
    )

    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_create_progress_invalid_class():
    """Test creating progress for non-existent class returns 404."""
    create_response = client.post(
        "/api/player/",
        json={"username": "invalidclass", "avatar": "avatar.png"}
    )
    player_id = create_response.json()["id"]

    response = client.post(
        "/api/progress/",
        json={
            "player_id": player_id,
            "module_number": 99,
            "class_number": 99,
            "status": "unlocked"
        }
    )

    assert response.status_code == 404
    assert "not found in curriculum" in response.json()["detail"]


def test_get_full_progress(test_player):
    """Test getting full player progress."""
    # Create some progress
    client.post(
        "/api/progress/",
        json={
            "player_id": test_player,
            "module_number": 0,
            "class_number": 0,
            "status": "completed"
        }
    )

    # Get full progress
    response = client.get(f"/api/progress/{test_player}")

    assert response.status_code == 200
    data = response.json()

    assert data["player_id"] == test_player
    assert "total_classes_completed" in data
    assert "total_exercises_completed" in data
    assert "overall_progress_percentage" in data
    assert "modules" in data
    assert len(data["modules"]) == 6  # 6 modules in curriculum


def test_get_full_progress_empty(test_player):
    """Test getting progress for player with no progress."""
    response = client.get(f"/api/progress/{test_player}")

    assert response.status_code == 200
    data = response.json()

    assert data["total_classes_completed"] == 0
    assert data["overall_progress_percentage"] == 0.0


def test_get_module_progress(test_player):
    """Test getting progress for specific module."""
    # Create progress in Module 0
    client.post(
        "/api/progress/",
        json={
            "player_id": test_player,
            "module_number": 0,
            "class_number": 0,
            "status": "completed"
        }
    )

    # Get Module 0 progress
    response = client.get(f"/api/progress/{test_player}/module/0")

    assert response.status_code == 200
    data = response.json()

    assert data["module_number"] == 0
    assert data["module_name"] == "IA Development Foundations"
    assert data["total_classes"] == 6
    assert data["completed_classes"] == 1
    assert "progress_percentage" in data
    assert "classes" in data


def test_get_module_progress_invalid_module(test_player):
    """Test getting progress for non-existent module returns 404."""
    response = client.get(f"/api/progress/{test_player}/module/99")
    assert response.status_code == 404


def test_update_progress_mark_completed(test_player):
    """Test marking progress as completed awards XP."""
    # Create progress
    create_response = client.post(
        "/api/progress/",
        json={
            "player_id": test_player,
            "module_number": 0,
            "class_number": 0,
            "status": "in_progress"
        }
    )
    progress_id = create_response.json()["id"]

    # Get initial XP
    player_response = client.get(f"/api/player/{test_player}")
    initial_xp = player_response.json()["xp"]

    # Mark as completed
    response = client.patch(
        f"/api/progress/{progress_id}",
        json={"status": "completed"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["completed_at"] is not None

    # Verify XP was awarded
    player_response = client.get(f"/api/player/{test_player}")
    new_xp = player_response.json()["xp"]
    assert new_xp > initial_xp


def test_update_progress_exercises(test_player):
    """Test updating exercises completed."""
    # Create progress
    create_response = client.post(
        "/api/progress/",
        json={
            "player_id": test_player,
            "module_number": 0,
            "class_number": 0,
            "status": "in_progress"
        }
    )
    progress_id = create_response.json()["id"]

    # Update exercises
    response = client.patch(
        f"/api/progress/{progress_id}",
        json={"exercises_completed": 5}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["exercises_completed"] == 5


def test_update_progress_not_found():
    """Test updating non-existent progress returns 404."""
    response = client.patch(
        "/api/progress/99999",
        json={"status": "completed"}
    )
    assert response.status_code == 404


def test_get_next_unlockable(test_player):
    """Test getting next unlockable class."""
    # First call should return Module 0, Class 0
    response = client.get(f"/api/progress/{test_player}/next-unlockable")

    assert response.status_code == 200
    data = response.json()

    assert data["module_number"] == 0
    assert data["class_number"] == 0
    assert "title" in data
    assert "xp_reward" in data


def test_get_next_unlockable_after_completion(test_player):
    """Test next unlockable updates after completing class."""
    # Complete Module 0, Class 0
    client.post(
        "/api/progress/",
        json={
            "player_id": test_player,
            "module_number": 0,
            "class_number": 0,
            "status": "completed"
        }
    )

    # Next unlockable should be Module 0, Class 1
    response = client.get(f"/api/progress/{test_player}/next-unlockable")

    assert response.status_code == 200
    data = response.json()

    assert data["module_number"] == 0
    assert data["class_number"] == 1


def test_sequential_class_unlock(test_player):
    """Test that classes must be unlocked sequentially."""
    # Unlock and complete first class
    client.post(
        "/api/progress/",
        json={
            "player_id": test_player,
            "module_number": 0,
            "class_number": 0,
            "status": "completed"
        }
    )

    # Should be able to unlock second class
    response = client.post(
        "/api/progress/",
        json={
            "player_id": test_player,
            "module_number": 0,
            "class_number": 1,
            "status": "unlocked"
        }
    )
    assert response.status_code == 201

    # Should NOT be able to skip to third class
    response = client.post(
        "/api/progress/",
        json={
            "player_id": test_player,
            "module_number": 0,
            "class_number": 2,
            "status": "unlocked"
        }
    )
    assert response.status_code == 403


def test_module_prerequisite():
    """Test that new module requires previous module completion."""
    # Create player
    create_response = client.post(
        "/api/player/",
        json={"username": "moduletest", "avatar": "avatar.png"}
    )
    player_id = create_response.json()["id"]

    # Try to unlock Module 1, Class 0 without completing Module 0
    response = client.post(
        "/api/progress/",
        json={
            "player_id": player_id,
            "module_number": 1,
            "class_number": 0,
            "status": "unlocked"
        }
    )

    assert response.status_code == 403
    assert "Prerequisites not met" in response.json()["detail"]


def test_player_stats_update_on_completion(test_player):
    """Test that PlayerStats updates when completing classes."""
    # Get initial stats
    stats_response = client.get(f"/api/player/{test_player}/stats")
    initial_classes = stats_response.json()["classes_completed"]

    # Complete a class
    create_response = client.post(
        "/api/progress/",
        json={
            "player_id": test_player,
            "module_number": 0,
            "class_number": 0,
            "status": "completed"
        }
    )
    progress_id = create_response.json()["id"]

    # If it was created as in_progress, mark as completed
    if create_response.json()["status"] != "completed":
        client.patch(
            f"/api/progress/{progress_id}",
            json={"status": "completed"}
        )

    # Verify stats updated
    stats_response = client.get(f"/api/player/{test_player}/stats")
    new_classes = stats_response.json()["classes_completed"]

    assert new_classes == initial_classes + 1
