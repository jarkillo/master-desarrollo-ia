"""Tests for Course Catalog routes (NFLOW-1)."""

import pytest
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_catalog.db"
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


def test_get_courses_catalog():
    """Test GET /api/courses returns list of available courses."""
    response = client.get("/api/courses")

    assert response.status_code == 200
    data = response.json()

    # Should return a list of courses
    assert isinstance(data, list)
    assert len(data) >= 2  # At least Master IA and Data Engineering

    # Check Master IA course
    master_ia = next((c for c in data if c["id"] == "master-ia"), None)
    assert master_ia is not None
    assert master_ia["name"] == "Master en Desarrollo con IA"
    assert master_ia["description"] is not None
    assert master_ia["status"] == "available"
    assert master_ia["modules"] > 0

    # Check Data Engineering course
    data_eng = next((c for c in data if c["id"] == "data-engineering"), None)
    assert data_eng is not None
    assert data_eng["name"] == "Data Engineering"
    assert data_eng["status"] in ["coming_soon", "available"]


def test_get_courses_structure():
    """Test course objects have required fields."""
    response = client.get("/api/courses")
    data = response.json()

    for course in data:
        # Required fields
        assert "id" in course
        assert "name" in course
        assert "description" in course
        assert "status" in course
        assert "modules" in course
        assert "icon" in course

        # Valid status values
        assert course["status"] in ["available", "coming_soon", "draft"]

        # Types
        assert isinstance(course["id"], str)
        assert isinstance(course["name"], str)
        assert isinstance(course["modules"], int)
        assert course["modules"] >= 0


def test_backward_compatibility_modules_without_course_id():
    """Test GET /api/progress/modules still works without course_id (backward compatibility)."""
    # Create a player first
    player_response = client.post(
        "/api/player/",
        json={"username": "testuser", "avatar": "avatar1.png"}
    )
    assert player_response.status_code == 201

    # Get modules without course_id (should default to "master-ia")
    response = client.get("/api/progress/modules")

    assert response.status_code == 200
    data = response.json()

    # Should return Master IA modules
    assert isinstance(data, list)
    assert len(data) > 0  # Master IA has modules


def test_backward_compatibility_modules_with_default_course_id():
    """Test GET /api/progress/modules?course_id=master-ia returns same as no param."""
    # Create a player first
    player_response = client.post(
        "/api/player/",
        json={"username": "testuser", "avatar": "avatar1.png"}
    )
    assert player_response.status_code == 201

    # Get modules without course_id
    response_default = client.get("/api/progress/modules")
    data_default = response_default.json()

    # Get modules with explicit master-ia
    response_explicit = client.get("/api/progress/modules?course_id=master-ia")
    data_explicit = response_explicit.json()

    # Should be identical
    assert response_default.status_code == 200
    assert response_explicit.status_code == 200
    assert data_default == data_explicit


def test_get_modules_with_different_course_id():
    """Test GET /api/progress/modules?course_id=data-engineering (when ready)."""
    # Create a player first
    player_response = client.post(
        "/api/player/",
        json={"username": "testuser", "avatar": "avatar1.png"}
    )
    assert player_response.status_code == 201

    # Get modules for Data Engineering
    response = client.get("/api/progress/modules?course_id=data-engineering")

    # This might return 200 with empty list (coming soon) or 404
    # We accept both for now until NFLOW-4 is implemented
    assert response.status_code in [200, 404]

    if response.status_code == 200:
        data = response.json()
        # If coming soon, might have 0 modules
        assert isinstance(data, list)
