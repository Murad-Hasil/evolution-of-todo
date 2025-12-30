"""Unit tests for filter functionality in TaskStorage."""
import pytest
from todo.models.task import Task, Priority
from todo.logic.storage import TaskStorage


def test_filter_by_status_pending():
    """Test filtering by Pending status."""
    storage = TaskStorage()
    storage.add_task("Task 1", priority=Priority.HIGH, tags=[])
    storage.add_task("Task 2", priority=Priority.LOW, tags=[])
    storage.update_task(2, status="Completed")

    tasks = storage.filter_tasks(status="Pending")
    assert len(tasks) == 1
    assert tasks[0].status == "Pending"


def test_filter_by_status_completed():
    """Test filtering by Completed status."""
    storage = TaskStorage()
    storage.add_task("Task 1", priority=Priority.HIGH, tags=[])
    storage.update_task(1, status="Completed")
    storage.add_task("Task 2", priority=Priority.LOW, tags=[])

    tasks = storage.filter_tasks(status="Completed")
    assert len(tasks) == 1
    assert tasks[0].status == "Completed"


def test_filter_by_priority_high():
    """Test filtering by High priority."""
    storage = TaskStorage()
    storage.add_task("Task 1", priority=Priority.HIGH, tags=[])
    storage.add_task("Task 2", priority=Priority.LOW, tags=[])

    tasks = storage.filter_tasks(priority=Priority.HIGH)
    assert len(tasks) == 1
    assert tasks[0].priority == Priority.HIGH


def test_filter_by_priority_medium():
    """Test filtering by Medium priority."""
    storage = TaskStorage()
    storage.add_task("Task 1", priority=Priority.MEDIUM, tags=[])
    storage.add_task("Task 2", priority=Priority.LOW, tags=[])

    tasks = storage.filter_tasks(priority=Priority.MEDIUM)
    assert len(tasks) == 1
    assert tasks[0].priority == Priority.MEDIUM


def test_filter_by_tag():
    """Test filtering by tag name."""
    storage = TaskStorage()
    storage.add_task("Task 1", priority=Priority.HIGH, tags=["work", "urgent"])
    storage.add_task("Task 2", priority=Priority.LOW, tags=["personal"])

    tasks = storage.filter_tasks(tag="work")
    assert len(tasks) == 1
    assert "work" in tasks[0].tags


def test_filter_by_tag_case_sensitive():
    """Test that tag filtering is case-sensitive."""
    storage = TaskStorage()
    storage.add_task("Task 1", priority=Priority.HIGH, tags=["Work"])
    storage.add_task("Task 2", priority=Priority.LOW, tags=["work"])

    tasks = storage.filter_tasks(tag="Work")
    assert len(tasks) == 1


def test_filter_multiple_criteria_and():
    """Test that multiple filters use AND logic."""
    storage = TaskStorage()
    storage.add_task("Task 1", priority=Priority.HIGH, tags=["work"])
    storage.update_task(1, status="Pending")
    storage.add_task("Task 2", priority=Priority.HIGH, tags=["work"])
    storage.update_task(2, status="Completed")

    tasks = storage.filter_tasks(status="Pending", priority=Priority.HIGH, tag="work")
    assert len(tasks) == 1
    assert tasks[0].id == 1


def test_filter_with_no_criteria():
    """Test that no filters returns all tasks."""
    storage = TaskStorage()
    storage.add_task("Task 1", priority=Priority.HIGH, tags=["work"])
    storage.add_task("Task 2", priority=Priority.LOW, tags=["personal"])

    tasks = storage.filter_tasks()
    assert len(tasks) == 2


def test_filter_no_matches():
    """Test that filter with no matches returns empty list."""
    storage = TaskStorage()
    storage.add_task("Task 1", priority=Priority.HIGH, tags=["work"])

    tasks = storage.filter_tasks(status="Completed")
    assert len(tasks) == 0
