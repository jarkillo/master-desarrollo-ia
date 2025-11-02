"""Tests for backend services (content_service, xp_service)."""

import pytest
from app.database import Base
from app.models.player import Player
from app.services import content_service, xp_service
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_services.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Create fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# Content Service Tests

def test_get_module_info():
    """Test getting module information."""
    module = content_service.get_module_info(0)

    assert module is not None
    assert module.module_number == 0
    assert module.title == "IA Development Foundations"
    assert len(module.classes) == 6


def test_get_module_info_invalid():
    """Test getting invalid module returns None."""
    module = content_service.get_module_info(99)
    assert module is None


def test_get_class_info():
    """Test getting class information."""
    class_info = content_service.get_class_info(0, 0)

    assert class_info is not None
    assert class_info.class_number == 0
    assert class_info.title == "Intro al Desarrollo con IA"
    assert class_info.xp_reward == 100


def test_get_class_info_invalid():
    """Test getting invalid class returns None."""
    class_info = content_service.get_class_info(99, 99)
    assert class_info is None


def test_get_all_modules():
    """Test getting all modules."""
    modules = content_service.get_all_modules()

    assert len(modules) == 6
    assert modules[0].module_number == 0
    assert modules[5].module_number == 5


def test_get_total_classes():
    """Test getting total classes count."""
    total = content_service.get_total_classes()
    assert total > 0
    assert total == sum(len(m.classes) for m in content_service.get_all_modules())


def test_get_total_xp():
    """Test getting total XP available."""
    total_xp = content_service.get_total_xp()
    assert total_xp > 0


def test_is_class_unlockable_first_class():
    """Test that Module 0 Class 0 is always unlockable."""
    unlockable = content_service.is_class_unlockable(0, 0, [])
    assert unlockable is True


def test_is_class_unlockable_second_class():
    """Test that second class requires first class completed."""
    # Without first class completed
    unlockable = content_service.is_class_unlockable(0, 1, [])
    assert unlockable is False

    # With first class completed
    unlockable = content_service.is_class_unlockable(0, 1, [(0, 0)])
    assert unlockable is True


def test_is_class_unlockable_new_module():
    """Test that new module requires previous module completion."""
    # Without Module 0 completed
    unlockable = content_service.is_class_unlockable(1, 0, [(0, 0)])
    assert unlockable is False

    # With Module 0 completed (all 6 classes)
    completed = [
        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)
    ]
    unlockable = content_service.is_class_unlockable(1, 0, completed)
    assert unlockable is True


def test_get_next_unlockable_class():
    """Test getting next unlockable class."""
    # With no progress, should return Module 0 Class 0
    next_class = content_service.get_next_unlockable_class([])
    assert next_class == (0, 0)

    # With Module 0 Class 0 completed, should return Module 0 Class 1
    next_class = content_service.get_next_unlockable_class([(0, 0)])
    assert next_class == (0, 1)


def test_get_next_unlockable_class_curriculum_complete():
    """Test getting next unlockable when curriculum is complete."""
    # Complete all classes (simplified - just enough to test)
    all_completed = []
    for module in content_service.get_all_modules():
        for class_info in module.classes:
            all_completed.append((module.module_number, class_info.class_number))

    next_class = content_service.get_next_unlockable_class(all_completed)
    assert next_class is None


def test_calculate_progress_percentage():
    """Test progress percentage calculation."""
    percentage = content_service.calculate_progress_percentage(10, 40)
    assert percentage == 25.0

    percentage = content_service.calculate_progress_percentage(0, 40)
    assert percentage == 0.0

    percentage = content_service.calculate_progress_percentage(40, 40)
    assert percentage == 100.0


def test_calculate_progress_percentage_zero_total():
    """Test progress percentage with zero total."""
    percentage = content_service.calculate_progress_percentage(0, 0)
    assert percentage == 0.0


def test_get_module_progress():
    """Test module progress calculation."""
    percentage = content_service.get_module_progress(0, 3)
    # Module 0 has 6 classes, 3 completed = 50%
    assert percentage == 50.0


# XP Service Tests

def test_calculate_level_from_xp():
    """Test level calculation from XP."""
    assert xp_service.calculate_level_from_xp(0) == 1
    assert xp_service.calculate_level_from_xp(100) == 2
    assert xp_service.calculate_level_from_xp(400) == 3
    assert xp_service.calculate_level_from_xp(900) == 4
    assert xp_service.calculate_level_from_xp(10000) == 11


def test_calculate_level_from_negative_xp():
    """Test level calculation with negative XP."""
    level = xp_service.calculate_level_from_xp(-100)
    assert level == 1


def test_calculate_xp_for_level():
    """Test XP required for level."""
    assert xp_service.calculate_xp_for_level(1) == 0
    assert xp_service.calculate_xp_for_level(2) == 100
    assert xp_service.calculate_xp_for_level(3) == 400
    assert xp_service.calculate_xp_for_level(4) == 900
    assert xp_service.calculate_xp_for_level(10) == 8100


def test_get_xp_progress_to_next_level():
    """Test XP progress calculation."""
    # Player with 150 XP (Level 2, halfway to Level 3)
    progress = xp_service.get_xp_progress_to_next_level(150)

    assert progress["current_level"] == 2
    assert progress["next_level"] == 3
    assert progress["xp_for_current_level"] == 100
    assert progress["xp_for_next_level"] == 400
    assert progress["xp_progress"] == 50
    assert progress["xp_needed"] == 250
    assert progress["progress_percentage"] > 0


def test_award_xp():
    """Test awarding XP to player."""
    db = TestingSessionLocal()

    # Create player
    player = Player(username="xptest", avatar="avatar.png")
    db.add(player)
    db.commit()
    db.refresh(player)

    # Award XP
    result = xp_service.award_xp(
        player_id=player.id,
        xp_amount=100,
        db=db,
        reason="Test award"
    )

    assert result["previous_xp"] == 0
    assert result["new_xp"] == 100
    assert result["xp_gained"] == 100
    assert result["previous_level"] == 1
    assert result["new_level"] == 2
    assert result["leveled_up"] is True
    assert result["reason"] == "Test award"

    db.close()


def test_award_xp_no_level_up():
    """Test awarding XP that doesn't cause level up."""
    db = TestingSessionLocal()

    # Create player
    player = Player(username="xptest2", avatar="avatar.png")
    db.add(player)
    db.commit()
    db.refresh(player)

    # Award small XP
    result = xp_service.award_xp(
        player_id=player.id,
        xp_amount=50,
        db=db,
        reason="Small award"
    )

    assert result["new_xp"] == 50
    assert result["new_level"] == 1
    assert result["leveled_up"] is False

    db.close()


def test_award_xp_invalid_player():
    """Test awarding XP to non-existent player raises error."""
    db = TestingSessionLocal()

    with pytest.raises(ValueError, match="not found"):
        xp_service.award_xp(
            player_id=99999,
            xp_amount=100,
            db=db,
            reason="Test"
        )

    db.close()


def test_award_negative_xp():
    """Test awarding negative XP (penalty)."""
    db = TestingSessionLocal()

    # Create player with some XP
    player = Player(username="penaltytest", avatar="avatar.png", xp=200, level=2)
    db.add(player)
    db.commit()
    db.refresh(player)

    # Award negative XP
    result = xp_service.award_xp(
        player_id=player.id,
        xp_amount=-50,
        db=db,
        reason="Penalty"
    )

    assert result["new_xp"] == 150
    assert result["xp_gained"] == -50

    db.close()


def test_get_level_title():
    """Test getting level titles."""
    assert xp_service.get_level_title(1) == "Junior Developer"
    assert xp_service.get_level_title(5) == "Junior Developer"
    assert xp_service.get_level_title(6) == "Mid Developer"
    assert xp_service.get_level_title(10) == "Mid Developer"
    assert xp_service.get_level_title(11) == "Senior Developer"
    assert xp_service.get_level_title(15) == "Senior Developer"
    assert xp_service.get_level_title(16) == "Tech Lead"
    assert xp_service.get_level_title(20) == "Tech Lead"
    assert xp_service.get_level_title(21) == "Architect"
    assert xp_service.get_level_title(25) == "Architect"
    assert xp_service.get_level_title(26) == "CTO"
    assert xp_service.get_level_title(30) == "CTO"
    assert xp_service.get_level_title(31) == "Legend"


def test_get_player_rank_info():
    """Test getting complete rank information."""
    db = TestingSessionLocal()

    # Create player with XP
    player = Player(username="ranktest", avatar="avatar.png", xp=250, level=2)
    db.add(player)
    db.commit()
    db.refresh(player)

    # Get rank info
    rank_info = xp_service.get_player_rank_info(player.id, db)

    assert rank_info["level"] == 2
    assert rank_info["title"] == "Junior Developer"
    assert rank_info["xp"] == 250
    assert "xp_progress" in rank_info

    db.close()


def test_get_player_rank_info_invalid_player():
    """Test getting rank info for non-existent player raises error."""
    db = TestingSessionLocal()

    with pytest.raises(ValueError, match="not found"):
        xp_service.get_player_rank_info(99999, db)

    db.close()
