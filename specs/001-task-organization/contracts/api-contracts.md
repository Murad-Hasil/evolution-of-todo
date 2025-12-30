# API Contracts: Task Organization

**Feature**: 001-task-organization
**Date**: 2025-12-30

## Overview

This document defines the API contracts for task organization features. Since this is a CLI application, "contracts" refer to the public interfaces of the `TaskStorage` class and Pydantic validation schemas.

## Storage API Contract

### TaskStorage

**Purpose**: In-memory task storage with CRUD and organizational operations.

**Public Methods**:

#### `add_task(title: str, description: str = "", priority: Priority = Priority.MEDIUM, tags: List[str] = None) -> Task`

Create a new task.

**Parameters**:
- `title` (str, required): Task title, 1-100 characters
- `description` (str, optional): Task description, max 500 characters, default ""
- `priority` (Priority, optional): Task priority, default Priority.MEDIUM
- `tags` (List[str], optional): Task tags, max 20 items, default []

**Returns**: Created `Task` object with auto-generated `id`

**Raises**: `ValueError` (via Pydantic validation) if input constraints violated

**Example**:
```python
task = storage.add_task(
    title="Fix bug",
    description="Urgent fix needed",
    priority=Priority.HIGH,
    tags=["bugfix", "urgent"]
)
# Returns: Task(id=1, title="Fix bug", description="Urgent fix needed", status="Pending", priority=Priority.HIGH, tags=["bugfix", "urgent"])
```

#### `get_all_tasks() -> List[Task]`

Return all tasks in insertion order.

**Returns**: List of all `Task` objects

**Example**:
```python
tasks = storage.get_all_tasks()
# Returns: [Task(...), Task(...), ...]
```

#### `get_task_by_id(task_id: int) -> Optional[Task]`

Retrieve a single task by ID.

**Parameters**:
- `task_id` (int, required): Task identifier

**Returns**: `Task` object if found, `None` otherwise

**Example**:
```python
task = storage.get_task_by_id(5)
# Returns: Task(...) or None
```

#### `update_task(task_id: int, title: Optional[str] = None, description: Optional[str] = None, status: Optional[str] = None, priority: Optional[Priority] = None, tags: Optional[List[str]] = None) -> Optional[Task]`

Update an existing task. Only provided fields are updated.

**Parameters**:
- `task_id` (int, required): Task identifier
- `title` (str, optional): New title
- `description` (str, optional): New description
- `status` (str, optional): New status ("Pending" or "Completed")
- `priority` (Priority, optional): New priority
- `tags` (List[str], optional): New tag list (replaces existing tags)

**Returns**: Updated `Task` object if found, `None` otherwise

**Raises**: `ValueError` if validation fails

**Example**:
```python
task = storage.update_task(
    task_id=5,
    priority=Priority.LOW,
    tags=["bugfix"]  # Replaces existing tags
)
# Returns: Task(id=5, ..., priority=Priority.LOW, tags=["bugfix"])
```

#### `delete_task(task_id: int) -> bool`

Delete a task by ID.

**Parameters**:
- `task_id` (int, required): Task identifier

**Returns**: `True` if deleted, `False` if not found

**Example**:
```python
deleted = storage.delete_task(5)
# Returns: True (task existed) or False (task not found)
```

#### `search_tasks(keyword: str) -> List[Task]`

Search tasks by keyword in title or description.

**Parameters**:
- `keyword` (str, required): Search query (case-insensitive)

**Returns**: List of matching `Task` objects, or all tasks if keyword is empty

**Example**:
```python
tasks = storage.search_tasks("urgent")
# Returns: Tasks containing "urgent" (case-insensitive) in title or description
```

#### `filter_tasks(status: Optional[str] = None, priority: Optional[Priority] = None, tag: Optional[str] = None) -> List[Task]`

Filter tasks by criteria. All specified filters are combined with AND logic.

**Parameters**:
- `status` (str, optional): Filter by "Pending" or "Completed"
- `priority` (Priority, optional): Filter by priority level
- `tag` (str, optional): Filter by exact tag name (case-sensitive)

**Returns**: List of matching `Task` objects, or all tasks if no filters specified

**Example**:
```python
tasks = storage.filter_tasks(status="Pending", priority=Priority.HIGH)
# Returns: Tasks that are both Pending AND High priority
```

#### `sort_tasks(sort_by: str = "title") -> List[Task]`

Sort tasks by specified field with tie-breaking by task ID.

**Parameters**:
- `sort_by` (str, required): Sort field ("title" or "priority")

**Returns**: Sorted list of `Task` objects

**Example**:
```python
tasks = storage.sort_tasks(sort_by="priority")
# Returns: Tasks ordered High → Medium → Low, with ID tie-breaker
```

## Validation Schemas

### TaskCreateSchema

**Purpose**: Validate task creation input.

**Fields**:
```python
class TaskCreateSchema(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default="", max_length=500)
    priority: Priority = Field(default=Priority.MEDIUM)
    tags: List[str] = Field(default_factory=list, max_length=20)

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @field_validator("tags")
    @classmethod
    def tags_unique(cls, v: List[str]) -> List[str]:
        seen = set()
        unique_tags = []
        for tag in v:
            tag = tag.strip()
            if not tag:
                continue  # Skip empty tags
            if tag not in seen:
                seen.add(tag)
                unique_tags.append(tag)
        return unique_tags
```

**Validation Rules**:
- Title: 1-100 characters, not empty after stripping
- Description: 0-500 characters
- Priority: Must be valid Priority enum value
- Tags: 0-20 items, non-empty after stripping, duplicates removed

### TaskUpdateSchema

**Purpose**: Validate task update input. All fields optional.

**Fields**:
```python
class TaskUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[str] = Field(None)
    priority: Optional[Priority] = Field(None)
    tags: Optional[List[str]] = Field(None, max_length=20)

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ["Pending", "Completed"]:
            raise ValueError("Status must be 'Pending' or 'Completed'")
        return v

    @field_validator("tags")
    @classmethod
    def tags_unique(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        if v is None:
            return None
        seen = set()
        unique_tags = []
        for tag in v:
            tag = tag.strip()
            if not tag:
                continue
            if tag not in seen:
                seen.add(tag)
                unique_tags.append(tag)
        return unique_tags
```

**Validation Rules**:
- Title (if provided): 1-100 characters
- Description (if provided): 0-500 characters
- Status (if provided): "Pending" or "Completed"
- Priority (if provided): Must be valid Priority enum value
- Tags (if provided): 0-20 items, non-empty after stripping, duplicates removed

## Error Contract

### Validation Errors

All schema validation raises `pydantic.ValidationError` with human-readable messages.

**Common Error Messages**:

| Field | Error | Message |
|-------|--------|---------|
| Title | Empty | "Title cannot be empty" |
| Title | Too long | "String should have at most 100 characters" |
| Description | Too long | "String should have at most 500 characters" |
| Priority | Invalid value | "Input should be 'High', 'Medium', or 'Low'" |
| Status | Invalid value | "Status must be 'Pending' or 'Completed'" |
| Tags | Too many | "List should have at most 20 items" |

## CLI Integration Contract

The `menu.py` module provides user-facing functions that interact with the above APIs:

### Menu Functions

| Function | Purpose | Storage Method Called |
|----------|---------|---------------------|
| `render_task_table(tasks)` | Display tasks in Rich table | `get_all_tasks()`, `search_tasks()`, `filter_tasks()`, `sort_tasks()` |
| `get_filter_criteria()` | Collect filter inputs from user | N/A (user input) |
| `get_sort_option()` | Collect sort option from user | N/A (user input) |

### Display Contract

**Task Table Columns**:
1. ID (right-aligned, cyan)
2. Title (white)
3. Description (dim)
4. Priority (colored: red=High, yellow=Medium, green=Low)
5. Tags (comma-separated, cyan)
6. Status (green=Completed, yellow=Pending)

**Empty State**:
- When no tasks match search/filter: Display "[yellow]No tasks found.[/yellow]"
