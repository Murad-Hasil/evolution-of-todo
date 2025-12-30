import pytest
from todo.logic.storage import TaskStorage
from todo.models.task import Task

def test_add_task():
    storage = TaskStorage()
    task = storage.add_task("Test Task", "Test Description")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.status == "Pending"
    assert len(storage.get_all_tasks()) == 1

def test_get_all_tasks():
    storage = TaskStorage()
    storage.add_task("Task 1")
    storage.add_task("Task 2")
    tasks = storage.get_all_tasks()
    assert len(tasks) == 2
    assert tasks[0].id == 1
    assert tasks[1].id == 2
