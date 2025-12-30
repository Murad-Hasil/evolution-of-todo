"""Unit tests for validation schemas with priority and tags."""
import pytest
from pydantic import ValidationError
from todo.validation.schemas import TaskCreateSchema, TaskUpdateSchema
from todo.models.task import Priority


def test_task_create_schema_default_priority():
    """Test that priority defaults to Medium."""
    schema = TaskCreateSchema(title="Test Task")
    assert schema.priority == Priority.MEDIUM


def test_task_create_schema_custom_priority():
    """Test setting custom priority."""
    schema = TaskCreateSchema(title="Test Task", priority=Priority.HIGH)
    assert schema.priority == Priority.HIGH


def test_task_create_schema_invalid_priority():
    """Test that invalid priority raises error."""
    with pytest.raises(ValidationError):
        TaskCreateSchema(title="Test Task", priority="invalid")


def test_task_create_schema_empty_tags():
    """Test that empty tags list is accepted."""
    schema = TaskCreateSchema(title="Test Task", tags=[])
    assert schema.tags == []


def test_task_create_schema_multiple_tags():
    """Test that multiple tags are accepted."""
    tags = ["work", "urgent", "bugfix"]
    schema = TaskCreateSchema(title="Test Task", tags=tags)
    assert schema.tags == tags


def test_task_create_schema_duplicate_tags_removed():
    """Test that duplicate tags are removed."""
    schema = TaskCreateSchema(title="Test Task", tags=["work", "work", "urgent"])
    assert schema.tags == ["work", "urgent"]


def test_task_create_schema_whitespace_tags_stripped():
    """Test that tag whitespace is stripped."""
    schema = TaskCreateSchema(title="Test Task", tags=[" work ", " urgent"])
    assert schema.tags == ["work", "urgent"]


def test_task_create_schema_empty_tags_removed():
    """Test that empty tags are removed."""
    schema = TaskCreateSchema(title="Test Task", tags=["work", "", "urgent"])
    assert schema.tags == ["work", "urgent"]


def test_task_create_schema_tag_too_long():
    """Test that tags over 30 characters are rejected."""
    with pytest.raises(ValidationError):
        TaskCreateSchema(title="Test Task", tags=["x" * 31])


def test_task_create_schema_too_many_tags():
    """Test that more than 20 tags are rejected."""
    with pytest.raises(ValidationError):
        TaskCreateSchema(title="Test Task", tags=["tag"] * 21)


def test_task_update_schema_optional_priority():
    """Test that priority is optional in update schema."""
    schema = TaskUpdateSchema()
    assert schema.priority is None


def test_task_update_schema_set_priority():
    """Test setting priority in update schema."""
    schema = TaskUpdateSchema(priority=Priority.LOW)
    assert schema.priority == Priority.LOW


def test_task_update_schema_tags_none():
    """Test that tags can be None in update schema."""
    schema = TaskUpdateSchema(tags=None)
    assert schema.tags is None


def test_task_update_schema_tags_list():
    """Test setting tags in update schema."""
    tags = ["work", "urgent"]
    schema = TaskUpdateSchema(tags=tags)
    assert schema.tags == tags


def test_task_update_schema_duplicate_tags_removed():
    """Test that duplicate tags are removed in update schema."""
    schema = TaskUpdateSchema(tags=["work", "work", "urgent"])
    assert schema.tags == ["work", "urgent"]
