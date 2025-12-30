"""Unit tests for sort functionality in TaskStorage."""
import pytest
from todo.models.task import Task, Priority
from todo.logic.storage import TaskStorage


def test_sort_by_title_alphabetical():
    """Test sorting by title A-Z."""
    storage = TaskStorage()
    storage.add_task("Zebra task")
    storage.add_task("Alpha task")
    storage.add_task("Beta task")

    tasks = storage.sort_tasks(sort_by="title")
    assert len(tasks) == 3
    assert tasks[0].title == "Alpha task"
    assert tasks[1].title == "Beta task"
    assert tasks[2].title == "Zebra task"


def test_sort_by_title_case_insensitive():
    """Test that title sorting is case-insensitive."""
    storage = TaskStorage()
    storage.add_task("zebra")
    storage.add_task("Alpha")
    storage.add_task("beta")

    tasks = storage.sort_tasks(sort_by="title")
    assert len(tasks) == 3
    assert tasks[0].title == "Alpha"
    assert tasks[1].title == "beta"
    assert tasks[2].title == "zebra"


def test_sort_by_priority_high_to_low():
    """Test sorting by priority (High → Medium → Low)."""
    storage = TaskStorage()
    storage.add_task("Low priority task", priority=Priority.LOW)
    storage.add_task("High priority task", priority=Priority.HIGH)
    storage.add_task("Medium priority task", priority=Priority.MEDIUM)

    tasks = storage.sort_tasks(sort_by="priority")
    assert len(tasks) == 3
    assert tasks[0].priority == Priority.HIGH
    assert tasks[1].priority == Priority.MEDIUM
    assert tasks[2].priority == Priority.LOW


def test_sort_priority_tie_breaker_by_id():
    """Test that ID breaks ties when sorting by priority."""
    storage = TaskStorage()
    storage.add_task("Task 1", priority=Priority.HIGH)
    storage.add_task("Task 2", priority=Priority.HIGH)

    tasks = storage.sort_tasks(sort_by="priority")
    assert len(tasks) == 2
    assert tasks[0].id == 1
    assert tasks[1].id == 2


def test_sort_title_tie_breaker_by_id():
    """Test that ID breaks ties when sorting by title."""
    storage = TaskStorage()
    storage.add_task("Same")
    storage.add_task("Same")

    tasks = storage.sort_tasks(sort_by="title")
    assert len(tasks) == 2
    assert tasks[0].id == 1
    assert tasks[1].id == 2


def test_sort_by_default_is_title():
    """Test that default sort is by title."""
    storage = TaskStorage()
    storage.add_task("Zebra")
    storage.add_task("Alpha")

    tasks = storage.sort_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == "Alpha"
    assert tasks[1].title == "Zebra"
