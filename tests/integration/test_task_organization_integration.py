"""Integration tests for task organization features."""
import pytest
from todo.models.task import Task, Priority
from todo.logic.storage import TaskStorage
from todo.ui import menu
from pydantic import ValidationError
from todo.validation.schemas import TaskCreateSchema


def test_create_task_with_priority_workflow():
    """Test creating a task with High priority."""
    storage = TaskStorage()
    schema = TaskCreateSchema(title="Urgent task", priority=Priority.HIGH, tags=["urgent", "work"])
    task = storage.add_task(schema.title, schema.description, schema.priority, schema.tags)

    assert task.title == "Urgent task"
    assert task.priority == Priority.HIGH
    assert task.tags == ["urgent", "work"]


def test_update_task_priority_workflow():
    """Test updating task priority."""
    storage = TaskStorage()
    task = storage.add_task("Task 1", priority=Priority.MEDIUM)
    updated = storage.update_task(task.id, priority=Priority.HIGH)

    assert updated.priority == Priority.HIGH


def test_search_workflow():
    """Test end-to-end search workflow."""
    storage = TaskStorage()
    storage.add_task("Urgent bug", priority=Priority.HIGH, tags=["bug"])
    storage.add_task("Regular task", priority=Priority.LOW, tags=["normal"])

    tasks = storage.search_tasks("urgent")
    assert len(tasks) == 1
    assert tasks[0].title == "Urgent bug"


def test_filter_workflow():
    """Test end-to-end filter workflow."""
    storage = TaskStorage()
    storage.add_task("Task 1", priority=Priority.HIGH, tags=["work"])
    storage.update_task(1, status="Completed")
    storage.add_task("Task 2", priority=Priority.HIGH, tags=["work"])

    tasks = storage.filter_tasks(status="Pending", tag="work")
    assert len(tasks) == 1
    assert tasks[0].id == 2


def test_sort_workflow():
    """Test end-to-end sort workflow."""
    storage = TaskStorage()
    storage.add_task("Zebra", priority=Priority.LOW)
    storage.add_task("Alpha", priority=Priority.HIGH)

    tasks = storage.sort_tasks(sort_by="title")
    assert tasks[0].title == "Alpha"
    assert tasks[1].title == "Zebra"


def test_combined_search_filter_sort_workflow():
    """Test combined search, filter, and sort workflow."""
    storage = TaskStorage()
    storage.add_task("Zebra urgent", priority=Priority.HIGH, tags=["urgent"])
    storage.add_task("Alpha urgent", priority=Priority.HIGH, tags=["urgent"])
    storage.add_task("Beta normal", priority=Priority.LOW, tags=["normal"])

    # Search
    tasks = storage.search_tasks("urgent")
    assert len(tasks) == 2

    # Filter
    tasks = storage.filter_tasks(priority=Priority.HIGH, tag="urgent")
    assert len(tasks) == 2

    # Sort
    tasks = storage.sort_tasks(tasks, sort_by="title")
    assert tasks[0].title == "Alpha urgent"
    assert tasks[1].title == "Zebra urgent"


def test_default_priority_on_create():
    """Test that new tasks default to Medium priority."""
    storage = TaskStorage()
    schema = TaskCreateSchema(title="New Task")
    task = storage.add_task(schema.title, schema.description, schema.priority, schema.tags)

    assert task.priority == Priority.MEDIUM


def test_multiple_tags_per_task():
    """Test that a task can have multiple tags."""
    storage = TaskStorage()
    tags = ["work", "urgent", "bugfix", "important"]
    schema = TaskCreateSchema(title="Multi-tag task", tags=tags)
    task = storage.add_task(schema.title, schema.description, schema.priority, schema.tags)

    assert len(task.tags) == 4
    assert "work" in task.tags
    assert "urgent" in task.tags


def test_task_without_tags():
    """Test that tasks can be created without tags."""
    storage = TaskStorage()
    schema = TaskCreateSchema(title="No tags task")
    task = storage.add_task(schema.title, schema.description, schema.priority, schema.tags)

    assert task.tags == []


def test_empty_search_returns_all():
    """Test that empty search returns all tasks."""
    storage = TaskStorage()
    storage.add_task("Task 1", priority=Priority.HIGH, tags=["work"])
    storage.add_task("Task 2", priority=Priority.LOW, tags=["personal"])

    tasks = storage.search_tasks("")
    assert len(tasks) == 2
