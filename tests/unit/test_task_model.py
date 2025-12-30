"""Unit tests for Task model with priority and tags."""
import pytest
from todo.models.task import Task, Priority


def test_task_creation_defaults():
    """Test that tasks have correct default values."""
    task = Task(id=1, title="Test Task")
    assert task.title == "Test Task"
    assert task.description == ""
    assert task.status == "Pending"
    assert task.priority == Priority.MEDIUM
    assert task.tags == []


def test_task_with_high_priority():
    """Test creating a task with High priority."""
    task = Task(id=1, title="Test Task", priority=Priority.HIGH)
    assert task.priority == Priority.HIGH


def test_task_with_low_priority():
    """Test creating a task with Low priority."""
    task = Task(id=1, title="Test Task", priority=Priority.LOW)
    assert task.priority == Priority.LOW


def test_task_with_tags():
    """Test creating a task with multiple tags."""
    tags = ["work", "urgent", "bugfix"]
    task = Task(id=1, title="Test Task", tags=tags)
    assert task.tags == tags


def test_task_with_empty_tags():
    """Test creating a task with empty tags list."""
    task = Task(id=1, title="Test Task", tags=[])
    assert task.tags == []


def test_all_priority_values():
    """Test that all priority enum values exist."""
    assert Priority.HIGH.value == "High"
    assert Priority.MEDIUM.value == "Medium"
    assert Priority.LOW.value == "Low"


def test_priority_enum_is_string():
    """Test that Priority enum inherits from str."""
    task = Task(id=1, title="Test Task", priority=Priority.HIGH)
    assert isinstance(task.priority, str)
    assert task.priority == "High"
