"""Tests for Player routes."""

import pytest
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_player.db"
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


def test_create_player():
    """Test creating a new player."""
    response = client.post(
        "/api/player/",
        json={"username": "testuser", "avatar": "avatar1.png"}
    )

    assert response.status_code == 201
    data = response.json()

    assert data["username"] == "testuser"
    assert data["avatar"] == "avatar1.png"
    assert data["level"] == 1
    assert data["xp"] == 0
    assert "id" in data
    assert "created_at" in data


def test_create_player_duplicate_username():
    """Test creating player with duplicate username returns 409."""
    # Create first player
    client.post(
        "/api/player/",
        json={"username": "duplicate", "avatar": "avatar1.png"}
    )

    # Try to create duplicate
    response = client.post(
        "/api/player/",
        json={"username": "duplicate", "avatar": "avatar2.png"}
    )

    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_create_player_invalid_username():
    """Test creating player with invalid username."""
    # Empty username
    response = client.post(
        "/api/player/",
        json={"username": "", "avatar": "avatar1.png"}
    )
    assert response.status_code == 422

    # Username too long (>50 chars)
    response = client.post(
        "/api/player/",
        json={"username": "a" * 51, "avatar": "avatar1.png"}
    )
    assert response.status_code == 422


def test_get_player():
    """Test retrieving a player by ID."""
    # Create player
    create_response = client.post(
        "/api/player/",
        json={"username": "gettest", "avatar": "avatar1.png"}
    )
    player_id = create_response.json()["id"]

    # Get player
    response = client.get(f"/api/player/{player_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == player_id
    assert data["username"] == "gettest"


def test_get_player_not_found():
    """Test getting non-existent player returns 404."""
    response = client.get("/api/player/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_list_players():
    """Test listing all players."""
    # Create multiple players
    client.post("/api/player/", json={"username": "user1", "avatar": "avatar1.png"})
    client.post("/api/player/", json={"username": "user2", "avatar": "avatar2.png"})
    client.post("/api/player/", json={"username": "user3", "avatar": "avatar3.png"})

    # List players
    response = client.get("/api/player/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert all("username" in player for player in data)


def test_list_players_pagination():
    """Test listing players with pagination."""
    # Create 5 players
    for i in range(5):
        client.post("/api/player/", json={"username": f"user{i}", "avatar": "avatar.png"})

    # Get first page (limit 2)
    response = client.get("/api/player/?skip=0&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2

    # Get second page
    response = client.get("/api/player/?skip=2&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_player():
    """Test updating a player."""
    # Create player
    create_response = client.post(
        "/api/player/",
        json={"username": "original", "avatar": "avatar1.png"}
    )
    player_id = create_response.json()["id"]

    # Update player
    response = client.patch(
        f"/api/player/{player_id}",
        json={"username": "updated", "avatar": "avatar2.png"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updated"
    assert data["avatar"] == "avatar2.png"


def test_update_player_partial():
    """Test partial update (only username)."""
    # Create player
    create_response = client.post(
        "/api/player/",
        json={"username": "original", "avatar": "avatar1.png"}
    )
    player_id = create_response.json()["id"]

    # Update only username
    response = client.patch(
        f"/api/player/{player_id}",
        json={"username": "newusername"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newusername"
    assert data["avatar"] == "avatar1.png"  # Avatar unchanged


def test_update_player_duplicate_username():
    """Test updating to duplicate username returns 409."""
    # Create two players
    client.post("/api/player/", json={"username": "user1", "avatar": "avatar1.png"})
    create_response = client.post(
        "/api/player/",
        json={"username": "user2", "avatar": "avatar2.png"}
    )
    player2_id = create_response.json()["id"]

    # Try to update user2 to user1's username
    response = client.patch(
        f"/api/player/{player2_id}",
        json={"username": "user1"}
    )

    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_update_player_not_found():
    """Test updating non-existent player returns 404."""
    response = client.patch(
        "/api/player/99999",
        json={"username": "ghost"}
    )
    assert response.status_code == 404


def test_get_player_stats():
    """Test retrieving player stats."""
    # Create player
    create_response = client.post(
        "/api/player/",
        json={"username": "statstest", "avatar": "avatar1.png"}
    )
    player_id = create_response.json()["id"]

    # Get stats
    response = client.get(f"/api/player/{player_id}/stats")

    assert response.status_code == 200
    data = response.json()

    # Verify stats structure
    assert "player_id" in data
    assert data["player_id"] == player_id
    assert "classes_completed" in data
    assert "exercises_completed" in data
    assert "bug_hunt_wins" in data
    assert "bug_hunt_games_played" in data
    assert "current_streak" in data
    assert "longest_streak" in data

    # Verify initial values
    assert data["classes_completed"] == 0
    assert data["exercises_completed"] == 0
    assert data["bug_hunt_wins"] == 0


def test_get_player_stats_not_found():
    """Test getting stats for non-existent player returns 404."""
    response = client.get("/api/player/99999/stats")
    assert response.status_code == 404


def test_delete_player():
    """Test deleting a player."""
    # Create player
    create_response = client.post(
        "/api/player/",
        json={"username": "deleteme", "avatar": "avatar1.png"}
    )
    player_id = create_response.json()["id"]

    # Delete player
    response = client.delete(f"/api/player/{player_id}")
    assert response.status_code == 204

    # Verify player is deleted
    get_response = client.get(f"/api/player/{player_id}")
    assert get_response.status_code == 404


def test_delete_player_not_found():
    """Test deleting non-existent player returns 404."""
    response = client.delete("/api/player/99999")
    assert response.status_code == 404


def test_player_xp_and_level():
    """Test that XP and level are tracked correctly."""
    # Create player
    create_response = client.post(
        "/api/player/",
        json={"username": "xptest", "avatar": "avatar1.png"}
    )
    player_id = create_response.json()["id"]

    # Initial state
    response = client.get(f"/api/player/{player_id}")
    assert response.json()["xp"] == 0
    assert response.json()["level"] == 1

    # XP and level will be updated through progress/achievements
    # (tested in those test files)
