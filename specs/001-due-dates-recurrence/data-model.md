# Data Model: Due Dates & Recurrence

**Feature**: Due Dates & Recurrence | **Date**: 2025-12-30

## Entities

### Task (Extended)

Extends existing Task dataclass in `src/todo/models/task.py`

| Field | Type | Required | Default | Validation |
|-------|------|----------|---------|------------|
| id | int | Yes | Auto-increment | Positive integer |
| title | str | Yes | - | 1-100 chars |
| description | str | No | "" | Max 500 chars |
| status | str | No | "Pending" | "Pending" or "Completed" |
| priority | Priority | No | MEDIUM | Priority enum |
| tags | List[str] | No | [] | Max 20 tags, 30 chars each |
| **due_date** | Optional[datetime] | No | None | YYYY-MM-DD HH:MM format |
| **recurrence_type** | RecurrenceType | No | NONE | RecurrenceType enum |

### Enums

#### RecurrenceType

```python
class RecurrenceType(str, Enum):
    """Task recurrence options."""
    NONE = "None"
    DAILY = "Daily"
    WEEKLY = "Weekly"
```

#### TaskStatus (Derived)

Computed property, not stored:

```python
class TaskStatus(Enum):
    """Computed task status based on due date."""
    OVERDUE = "Overdue"           # due_date < now
    DUE_SOON = "Due Soon"         # due_date within 24h, not overdue
    ON_TRACK = "On Track"         # due_date > 24h from now
    NO_DEADLINE = "No Deadline"   # due_date is None
```

## Validation Rules

### Date Format

- Must match: `YYYY-MM-DD HH:MM` (24-hour format)
- Example: "2025-12-31 23:59"
- Invalid: "12/31/2025 11:59 PM", "2025-12-31", "2025-12-31 25:00"

### Recurrence Type

- Must be one of: "None", "Daily", "Weekly"
- Case-insensitive input accepted
- Stored as uppercase enum value

### Task Completion with Recurrence

1. Mark task as "Completed"
2. If `recurrence_type == DAILY`:
   - Create new Task with same title, description, priority, tags
   - Set `due_date = original.due_date + timedelta(days=1)` if due_date exists
   - Set `recurrence_type = original.recurrence_type`
3. If `recurrence_type == WEEKLY`:
   - Create new Task with same title, description, priority, tags
   - Set `due_date = original.due_date + timedelta(weeks=1)` if due_date exists
   - Set `recurrence_type = original.recurrence_type`
4. If `recurrence_type == NONE`:
   - No new task created

## Relationships

```
Task (1) ---- completes ----> (0 or 1) Task (recurrence)
```

- Each completed recurring task creates at most one new task
- Chain continues until user disables recurrence
- Original task remains in history (completed)
