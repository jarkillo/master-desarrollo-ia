"""Tests for Bug Hunt mini-game."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models import Player


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_bug_hunt.db"
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
    """Create a test player."""
    db = TestingSessionLocal()
    player = Player(username="test_player", avatar="test.png")
    db.add(player)
    db.commit()
    db.refresh(player)
    player_id = player.id
    db.close()
    return player_id


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_start_bug_hunt_without_difficulty(test_player):
    """Test starting Bug Hunt game without specifying difficulty."""
    response = client.post(
        "/api/minigames/bug-hunt/start",
        json={"player_id": test_player}
    )

    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "session_id" in data
    assert "template_id" in data
    assert "title" in data
    assert "description" in data
    assert "difficulty" in data
    assert "code" in data
    assert "bugs_count" in data
    assert "max_xp" in data
    assert "started_at" in data

    # Verify difficulty is valid
    assert data["difficulty"] in ["easy", "medium", "hard"]

    # Verify bugs_count is positive
    assert data["bugs_count"] > 0


def test_start_bug_hunt_with_difficulty(test_player):
    """Test starting Bug Hunt game with specific difficulty."""
    response = client.post(
        "/api/minigames/bug-hunt/start",
        json={"player_id": test_player, "difficulty": "easy"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["difficulty"] == "easy"


def test_start_bug_hunt_invalid_player():
    """Test starting Bug Hunt with non-existent player."""
    response = client.post(
        "/api/minigames/bug-hunt/start",
        json={"player_id": 99999}
    )

    assert response.status_code == 404
    assert "Player not found" in response.json()["detail"]


def test_start_bug_hunt_invalid_difficulty(test_player):
    """Test starting Bug Hunt with invalid difficulty."""
    response = client.post(
        "/api/minigames/bug-hunt/start",
        json={"player_id": test_player, "difficulty": "impossible"}
    )

    assert response.status_code == 400


def test_submit_bug_hunt_perfect_score(test_player):
    """Test submitting Bug Hunt with perfect score."""
    # Start game
    start_response = client.post(
        "/api/minigames/bug-hunt/start",
        json={"player_id": test_player, "difficulty": "easy"}
    )
    assert start_response.status_code == 200
    start_data = start_response.json()

    # Get correct bug lines from template
    from app.content.bug_templates import get_template_by_id
    template = get_template_by_id(start_data["template_id"])
    correct_lines = [bug["line"] for bug in template.bugs]

    # Submit perfect answer
    submit_response = client.post(
        "/api/minigames/bug-hunt/submit",
        json={
            "session_id": start_data["session_id"],
            "player_id": test_player,
            "found_bug_lines": correct_lines,
            "time_seconds": 30.0
        }
    )

    assert submit_response.status_code == 200
    submit_data = submit_response.json()

    # Verify perfect score
    assert submit_data["success"] is True
    assert submit_data["bugs_found"] == submit_data["bugs_total"]
    assert submit_data["bugs_missed"] == 0
    assert submit_data["false_positives"] == 0
    assert submit_data["is_perfect"] is True
    assert submit_data["accuracy"] == 100.0
    assert submit_data["xp_earned"] > 0


def test_submit_bug_hunt_partial_score(test_player):
    """Test submitting Bug Hunt with partial score."""
    # Start game with hard difficulty to ensure multiple bugs
    start_response = client.post(
        "/api/minigames/bug-hunt/start",
        json={"player_id": test_player, "difficulty": "hard"}
    )
    assert start_response.status_code == 200
    start_data = start_response.json()

    # Get correct bug lines and submit only first bug (partial answer)
    from app.content.bug_templates import get_template_by_id
    template = get_template_by_id(start_data["template_id"])
    correct_lines = [bug["line"] for bug in template.bugs]

    # If template has multiple bugs, submit only first one; otherwise submit none
    if len(correct_lines) > 1:
        partial_lines = [correct_lines[0]]
        expected_accuracy_range = (0, 100)  # Between 0 and 100 (not inclusive)
    else:
        # For single bug template, submit empty to test 0% accuracy
        partial_lines = []
        expected_accuracy_range = (0, 0)  # Exactly 0%

    # Submit partial answer
    submit_response = client.post(
        "/api/minigames/bug-hunt/submit",
        json={
            "session_id": start_data["session_id"],
            "player_id": test_player,
            "found_bug_lines": partial_lines,
            "time_seconds": 60.0
        }
    )

    assert submit_response.status_code == 200
    submit_data = submit_response.json()

    # Verify partial score
    assert submit_data["success"] is True
    assert submit_data["bugs_missed"] > 0
    assert submit_data["is_perfect"] is False

    # Check accuracy based on what we submitted
    if len(correct_lines) > 1:
        assert 0 < submit_data["accuracy"] < 100.0
    else:
        assert submit_data["accuracy"] == 0.0


def test_submit_bug_hunt_with_false_positives(test_player):
    """Test submitting Bug Hunt with false positives."""
    # Start game
    start_response = client.post(
        "/api/minigames/bug-hunt/start",
        json={"player_id": test_player}
    )
    assert start_response.status_code == 200
    start_data = start_response.json()

    # Get correct bug lines and add false positives
    from app.content.bug_templates import get_template_by_id
    template = get_template_by_id(start_data["template_id"])
    correct_lines = [bug["line"] for bug in template.bugs]

    # Add lines that are NOT bugs
    max_line = max(bug["line"] for bug in template.bugs)
    false_positive_lines = [max_line + 1, max_line + 2]
    all_lines = correct_lines + false_positive_lines

    # Submit with false positives
    submit_response = client.post(
        "/api/minigames/bug-hunt/submit",
        json={
            "session_id": start_data["session_id"],
            "player_id": test_player,
            "found_bug_lines": all_lines,
            "time_seconds": 45.0
        }
    )

    assert submit_response.status_code == 200
    submit_data = submit_response.json()

    # Verify false positives are counted
    assert submit_data["success"] is True
    assert submit_data["false_positives"] == len(false_positive_lines)
    assert submit_data["is_perfect"] is False


def test_leaderboard_empty():
    """Test leaderboard when no games have been played."""
    response = client.get("/api/minigames/bug-hunt/leaderboard")

    assert response.status_code == 200
    data = response.json()
    assert data["total_entries"] == 0
    assert len(data["entries"]) == 0


def test_leaderboard_with_games(test_player):
    """Test leaderboard after playing games."""
    # Play a game
    start_response = client.post(
        "/api/minigames/bug-hunt/start",
        json={"player_id": test_player}
    )
    start_data = start_response.json()

    from app.content.bug_templates import get_template_by_id
    template = get_template_by_id(start_data["template_id"])
    correct_lines = [bug["line"] for bug in template.bugs]

    client.post(
        "/api/minigames/bug-hunt/submit",
        json={
            "session_id": start_data["session_id"],
            "player_id": test_player,
            "found_bug_lines": correct_lines,
            "time_seconds": 30.0
        }
    )

    # Get leaderboard
    response = client.get("/api/minigames/bug-hunt/leaderboard")

    assert response.status_code == 200
    data = response.json()
    assert data["total_entries"] == 1
    assert len(data["entries"]) == 1
    assert data["entries"][0]["player_id"] == test_player
    assert data["entries"][0]["rank"] == 1


def test_player_stats_no_games(test_player):
    """Test player stats when no games have been played."""
    response = client.get(f"/api/minigames/bug-hunt/stats/{test_player}")

    assert response.status_code == 200
    data = response.json()
    assert data["total_games_played"] == 0
    assert data["total_bugs_found"] == 0
    assert data["best_score"] == 0


def test_player_stats_with_games(test_player):
    """Test player stats after playing games."""
    # Play 2 games
    for _ in range(2):
        start_response = client.post(
            "/api/minigames/bug-hunt/start",
            json={"player_id": test_player}
        )
        start_data = start_response.json()

        from app.content.bug_templates import get_template_by_id
        template = get_template_by_id(start_data["template_id"])
        correct_lines = [bug["line"] for bug in template.bugs]

        client.post(
            "/api/minigames/bug-hunt/submit",
            json={
                "session_id": start_data["session_id"],
                "player_id": test_player,
                "found_bug_lines": correct_lines,
                "time_seconds": 30.0
            }
        )

    # Get stats
    response = client.get(f"/api/minigames/bug-hunt/stats/{test_player}")

    assert response.status_code == 200
    data = response.json()
    assert data["total_games_played"] == 2
    assert data["total_bugs_found"] > 0
    assert data["best_score"] > 0
    assert data["average_score"] > 0
    assert data["favorite_difficulty"] is not None
