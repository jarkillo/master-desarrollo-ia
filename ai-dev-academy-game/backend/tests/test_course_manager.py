"""Tests for CourseManager (NFLOW-1)."""

import pytest


def test_course_manager_import():
    """Test that CourseManager can be imported."""
    from app.core.course_manager import CourseManager

    assert CourseManager is not None


def test_course_manager_get_master_ia():
    """Test CourseManager.get_course('master-ia') returns configuration."""
    from app.core.course_manager import course_manager

    course = course_manager.get_course("master-ia")

    assert course is not None
    assert course.id == "master-ia"
    assert course.name == "Master en Desarrollo con IA"
    assert course.status == "available"
    assert course.modules > 0


def test_course_manager_get_data_engineering():
    """Test CourseManager.get_course('data-engineering') returns stub."""
    from app.core.course_manager import course_manager

    course = course_manager.get_course("data-engineering")

    assert course is not None
    assert course.id == "data-engineering"
    assert course.name == "Data Engineering"
    # Status can be "coming_soon" or "available" depending on NFLOW-4
    assert course.status in ["coming_soon", "available"]


def test_course_manager_get_all_courses():
    """Test CourseManager.get_all_courses() returns all registered courses."""
    from app.core.course_manager import course_manager

    courses = course_manager.get_all_courses()

    assert len(courses) >= 2  # At least Master IA and Data Engineering

    course_ids = [c.id for c in courses]
    assert "master-ia" in course_ids
    assert "data-engineering" in course_ids


def test_course_manager_get_invalid_course():
    """Test CourseManager.get_course('invalid') raises error or returns None."""
    from app.core.course_manager import course_manager

    course = course_manager.get_course("invalid-course-id")

    # Should return None for invalid course
    assert course is None


def test_course_manager_register_course():
    """Test CourseManager can register new courses."""
    from app.core.course_manager import CourseManager
    from app.courses.master_ia import MasterIACourse

    manager = CourseManager()
    course = MasterIACourse()

    manager.register_course(course)

    retrieved = manager.get_course("master-ia")
    assert retrieved is not None
    assert retrieved.id == "master-ia"


def test_course_provides_modules():
    """Test that courses provide modules list."""
    from app.core.course_manager import course_manager

    master_ia = course_manager.get_course("master-ia")

    # Should have a get_modules method
    assert hasattr(master_ia, 'get_modules')

    modules = master_ia.get_modules()
    assert isinstance(modules, list)
    assert len(modules) > 0  # Master IA has modules

    # Check first module structure
    first_module = modules[0]
    assert "id" in first_module
    assert "name" in first_module
    assert "classes" in first_module


def test_course_provides_achievements():
    """Test that courses provide achievements list."""
    from app.core.course_manager import course_manager

    master_ia = course_manager.get_course("master-ia")

    # Should have a get_achievements method
    assert hasattr(master_ia, 'get_achievements')

    achievements = master_ia.get_achievements()
    assert isinstance(achievements, list)
    # Master IA might have achievements or empty list (OK for now)


def test_course_adapter_interface():
    """Test that Course adapter implements required interface."""
    from app.core.course_manager import course_manager

    master_ia = course_manager.get_course("master-ia")

    # Required attributes
    assert hasattr(master_ia, 'id')
    assert hasattr(master_ia, 'name')
    assert hasattr(master_ia, 'description')
    assert hasattr(master_ia, 'status')
    assert hasattr(master_ia, 'modules')
    assert hasattr(master_ia, 'icon')

    # Required methods
    assert hasattr(master_ia, 'get_modules')
    assert hasattr(master_ia, 'get_achievements')
    assert callable(master_ia.get_modules)
    assert callable(master_ia.get_achievements)
