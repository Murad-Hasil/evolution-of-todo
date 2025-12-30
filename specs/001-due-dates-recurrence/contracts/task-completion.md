# Contract: Task Completion with Recurrence

**Feature**: Due Dates & Recurrence | **Date**: 2025-12-30

## Complete Task Command

### Input Schema

```yaml
command: complete-task
parameters:
  task_id:
    type: integer
    required: true
```

### Behavior Flow

```
Start complete-task(task_id)
  Load task from storage
  If task not found -> ERROR: NOT_FOUND
  Set task.status = "Completed"
  If task.recurrence_type == "Daily":
    Create new_task with:
      - title = task.title
      - description = task.description
      - priority = task.priority
      - tags = task.tags
      - due_date = task.due_date + 1 day (if exists)
      - recurrence_type = "Daily"
      - status = "Pending"
    Add new_task to storage
  Else if task.recurrence_type == "Weekly":
    Create new_task with:
      - title = task.title
      - description = task.description
      - priority = task.priority
      - tags = task.tags
      - due_date = task.due_date + 7 days (if exists)
      - recurrence_type = "Weekly"
      - status = "Pending"
    Add new_task to storage
  Else (recurrence_type == "None"):
    No new task created
  Return updated task
End
```

### Output Schema

```yaml
status: success | error
completed_task:
  id: integer
  status: "Completed"
new_task:
  id: integer | null  # null if recurrence_type is "None"
  # All other fields as above
error:
  code: VALIDATION_ERROR | NOT_FOUND | INTERNAL_ERROR
  message: string
```

### Errors

| Code | Condition | Message Example |
|------|-----------|-----------------|
| NOT_FOUND | Task ID not found | "Task 42 not found" |
| VALIDATION_ERROR | Task already completed | "Task 42 is already completed" |

---

## Recurrence Logic Examples

### Daily Recurrence

**Input**: Task with `due_date = "2025-12-30 09:00"`, `recurrence_type = "Daily"`

**Action**: Mark task complete

**Output**: New task created with `due_date = "2025-12-31 09:00"`

### Weekly Recurrence

**Input**: Task with `due_date = "2025-12-30 09:00"`, `recurrence_type = "Weekly"`

**Action**: Mark task complete

**Output**: New task created with `due_date = "2026-01-06 09:00"`

### No Due Date + Daily Recurrence

**Input**: Task with `due_date = null`, `recurrence_type = "Daily"`

**Action**: Mark task complete

**Output**: New task created with `due_date = null` (preserved)

### No Recurrence

**Input**: Task with `recurrence_type = "None"`

**Action**: Mark task complete

**Output**: No new task created (`new_task: null`)
