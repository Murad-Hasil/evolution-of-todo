"""Unit tests for search functionality in TaskStorage."""
import pytest
from todo.models.task import Task, Priority
from todo.logic.storage import TaskStorage


def test_search_empty_keyword_returns_all():
    """Test that empty search keyword returns all tasks."""
    storage = TaskStorage()
    storage.add_task("Task 1", "Description 1", Priority.HIGH, ["tag1"])
    storage.add_task("Task 2", "Description 2", Priority.LOW, ["tag2"])

    tasks = storage.search_tasks("")
    assert len(tasks) == 2


def test_search_matches_title():
    """Test that search matches task title."""
    storage = TaskStorage()
    storage.add_task("Urgent bug fix", "Low priority")
    storage.add_task("Regular task", "Description")

    tasks = storage.search_tasks("urgent")
    assert len(tasks) == 1
    assert tasks[0].title == "Urgent bug fix"


def test_search_matches_description():
    """Test that search matches task description."""
    storage = TaskStorage()
    storage.add_task("Task 1", "Urgent fix needed")
    storage.add_task("Task 2", "Normal task")

    tasks = storage.search_tasks("urgent")
    assert len(tasks) == 1
    assert "Urgent fix needed" in tasks[0].description


def test_search_case_insensitive():
    """Test that search is case-insensitive."""
    storage = TaskStorage()
    storage.add_task("URGENT Task", "Description")

    tasks = storage.search_tasks("urgent")
    assert len(tasks) == 1


def test_search_partial_match():
    """Test that search supports partial word matching."""
    storage = TaskStorage()
    storage.add_task("Project deadline", "Complete the project")

    tasks = storage.search_tasks("proj")
    assert len(tasks) == 1


def test_search_no_matches_returns_empty():
    """Test that search with no matches returns empty list."""
    storage = TaskStorage()
    storage.add_task("Task 1", "Description 1")

    tasks = storage.search_tasks("nonexistent")
    assert len(tasks) == 0


def test_search_multiple_matches():
    """Test that search matches multiple tasks."""
    storage = TaskStorage()
    storage.add_task("Urgent bug 1", "Fix bug")
    storage.add_task("Urgent bug 2", "Fix another bug")
    storage.add_task("Normal task", "Normal description")

    tasks = storage.search_tasks("urgent")
    assert len(tasks) == 2


def test_search_matches_both_title_and_description():
    """Test that search matches either title or description."""
    storage = TaskStorage()
    storage.add_task("Task with keyword", "Description without")
    storage.add_task("Task without", "Description with keyword")

    tasks = storage.search_tasks("keyword")
    assert len(tasks) == 2
