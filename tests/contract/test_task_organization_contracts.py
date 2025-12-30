"""Contract tests for TaskStorage API - task organization features."""
import pytest
from todo.models.task import Task, Priority
from todo.logic.storage import TaskStorage


def test_add_task_contract_with_priority_and_tags():
    """Contract: add_task accepts priority and tags."""
    storage = TaskStorage()
    task = storage.add_task("Task title", "Description", Priority.HIGH, ["tag1", "tag2"])

    assert isinstance(task, Task)
    assert task.id == 1
    assert task.title == "Task title"
    assert task.description == "Description"
    assert task.priority == Priority.HIGH
    assert task.tags == ["tag1", "tag2"]


def test_search_tasks_contract():
    """Contract: search_tasks returns tasks matching keyword."""
    storage = TaskStorage()
    storage.add_task("Urgent task", priority=Priority.HIGH)
    storage.add_task("Normal task", priority=Priority.LOW)

    tasks = storage.search_tasks("urgent")
    assert isinstance(tasks, list)
    assert len(tasks) == 1
    assert isinstance(tasks[0], Task)


def test_filter_tasks_contract():
    """Contract: filter_tasks accepts status, priority, and tag."""
    storage = TaskStorage()
    storage.add_task("Task 1", priority=Priority.HIGH, tags=["work"])
    storage.add_task("Task 2", priority=Priority.HIGH, tags=["personal"])

    tasks = storage.filter_tasks(status="Pending", priority=Priority.HIGH, tag="work")
    assert isinstance(tasks, list)
    assert len(tasks) == 1


def test_sort_tasks_contract():
    """Contract: sort_tasks accepts sort_by parameter."""
    storage = TaskStorage()
    storage.add_task("Zebra", priority=Priority.LOW)
    storage.add_task("Alpha", priority=Priority.HIGH)

    tasks = storage.sort_tasks(sort_by="title")
    assert isinstance(tasks, list)
    assert len(tasks) == 2
    assert tasks[0].title == "Alpha"


def test_update_task_contract_with_priority_and_tags():
    """Contract: update_task accepts priority and tags."""
    storage = TaskStorage()
    task = storage.add_task("Task", priority=Priority.MEDIUM)

    updated = storage.update_task(task.id, priority=Priority.HIGH, tags=["urgent"])
    assert updated is not None
    assert updated.priority == Priority.HIGH
    assert updated.tags == ["urgent"]


def test_priority_enum_values():
    """Contract: Priority enum has HIGH, MEDIUM, LOW values."""
    assert Priority.HIGH.value == "High"
    assert Priority.MEDIUM.value == "Medium"
    assert Priority.LOW.value == "Low"


def test_task_default_values():
    """Contract: Task has default priority and tags."""
    task = Task(id=1, title="Task")

    assert task.priority == Priority.MEDIUM
    assert task.tags == []
