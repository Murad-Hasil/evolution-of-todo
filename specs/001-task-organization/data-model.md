# Data Model: Task Organization

**Feature**: 001-task-organization
**Date**: 2025-12-30

## Overview

The data model for task organization extends the existing `Task` entity with priority enumeration and tag collection. The design maintains backward compatibility with existing fields while adding organizational capabilities.

## Entities

### Task

Represents a single todo item with extended organizational attributes.

**Fields**:

| Field | Type | Default | Description | Validation |
|-------|------|---------|-------------|------------|
| `id` | `int` | Auto-generated | Unique task identifier | > 0 |
| `title` | `str` | Required | Task title | 1-100 chars, not empty |
| `description` | `str` | `""` | Optional description | Max 500 chars |
| `status` | `str` | `"Pending"` | Task completion state | "Pending" or "Completed" |
| `priority` | `Priority` | `Priority.MEDIUM` | Task importance level | High, Medium, or Low |
| `tags` | `List[str]` | `[]` | Categorization labels | Max 20 tags per task, max 30 chars each |

**State Transitions**:

- `status`: `"Pending"` ↔ `"Completed"` (bidirectional)
- `priority`: `"High"` ↔ `"Medium"` ↔ `"Low"` (any transition allowed)
- `tags`: Add/remove at any time; no state machine

**Relationships**: None (independent entity)

### Priority (Enumeration)

Type-safe enumeration for task priority levels.

**Values**:

| Value | String Representation | Display Color | Description |
|-------|-------------------|---------------|-------------|
| `Priority.HIGH` | `"High"` | Red | Urgent tasks requiring immediate attention |
| `Priority.MEDIUM` | `"Medium"` | Yellow | Normal priority, default for new tasks |
| `Priority.LOW` | `"Low"` | Green | Tasks that can be deferred |

**Type Definition**:
```python
class Priority(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
```

### Tag

Simple string label for categorization. Not a separate entity due to in-memory scope.

**Properties**:

| Property | Constraint | Rationale |
|----------|------------|-----------|
| Length | Max 30 characters | Prevents excessively long tags |
| Characters | No restriction | Users may use any text including spaces |
| Uniqueness | Duplicates removed per task | Prevents `[tag, tag]` on same task |
| Case-sensitivity | Case-sensitive | "Work" ≠ "work" (per spec assumption) |

## Validation Rules

### Task Creation

**Required Fields**: `title`, `priority` (defaults to Medium), `status` (defaults to Pending)

**Validation Rules**:

1. Title must be non-empty after stripping whitespace
2. Title length: 1-100 characters
3. Description length: 0-500 characters (optional)
4. Priority must be one of: "High", "Medium", "Low"
5. Status must be one of: "Pending", "Completed"
6. Tags list: 0-20 items maximum
7. Individual tag length: 1-30 characters (non-empty)
8. Tags must be unique within a single task

### Task Update

**Partial Updates**: All fields except `id` are optional

**Validation Rules**:

1. If provided, follow same validation as Task Creation
2. Missing fields retain existing values
3. Empty `tags` list removes all tags from task
4. Empty string for tag triggers validation error

### Search Query

**Validation Rules**:

1. Keyword length: 0-100 characters
2. Empty string or `None`: Return all tasks (no filter)
3. Case-insensitive matching against title and description

### Filter Criteria

**Validation Rules**:

1. `status`: Must be "Pending", "Completed", or `None` (no filter)
2. `priority`: Must be "High", "Medium", "Low", or `None` (no filter)
3. `tag`: String matching exact tag name (case-sensitive), or `None` (no filter)
4. Filters combined with AND logic (all must match)

### Sort Options

**Validation Rules**:

1. `sort_by`: Must be "title" or "priority"
2. Invalid value defaults to "title"
3. Tie-breaking: Uses task `id` (insertion order)

## Data Integrity

### In-Memory Storage Constraints

- Task IDs are monotonically increasing integers starting from 1
- Deleted task IDs are **not** reused
- Tags are stored as lists (no reference integrity to other tasks)
- No cascading operations (delete task → tags removed with it)

### Concurrent Access

**Out of Scope**: No locking or concurrency control implemented (single-user per spec assumption).

## Migration Considerations

### Backward Compatibility

The data model is **backward compatible** with existing code:

- New fields (`priority`, `tags`) have sensible defaults
- Existing fields (`id`, `title`, `description`, `status`) unchanged
- Old tasks created before feature will receive `priority=Medium`, `tags=[]`

### Phase II Migration (FastAPI/SQLModel)

| Current | Phase II | Notes |
|---------|----------|-------|
| `@dataclass Task` | `class Task(BaseModel)` | Pydantic model maps to SQLModel |
| `Priority(str, Enum)` | `Priority(str, Enum)` | Same enum, SQLAlchemy compatible |
| `List[str] tags` | `List[str] tags` | SQLModel supports list types via JSON or join tables |
| In-memory dict | PostgreSQL table | Database persistence replaces in-memory storage |

The validation rules defined here translate directly to Pydantic field validators in Phase II, ensuring schema consistency across phases.
