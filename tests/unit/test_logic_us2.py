import pytest
from todo.logic.storage import TaskStorage

def test_update_task():
    storage = TaskStorage()
    storage.add_task("Original Title", "Original Desc")
    updated_task = storage.update_task(1, title="New Title", status="Completed")
    assert updated_task.title == "New Title"
    assert updated_task.status == "Completed"
    assert updated_task.description == "Original Desc"

def test_delete_task():
    storage = TaskStorage()
    storage.add_task("Task to delete")
    assert len(storage.get_all_tasks()) == 1
    assert storage.delete_task(1) is True
    assert len(storage.get_all_tasks()) == 0
    assert storage.delete_task(1) is False
