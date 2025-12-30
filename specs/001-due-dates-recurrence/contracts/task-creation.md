# Contract: Task Creation with Due Date & Recurrence

**Feature**: Due Dates & Recurrence | **Date**: 2025-12-30

## Create Task Command

### Input Schema

```yaml
command: create-task
parameters:
  title:
    type: string
    required: true
    min_length: 1
    max_length: 100
  description:
    type: string
    required: false
    default: ""
    max_length: 500
  due_date:
    type: string
    required: false
    format: "YYYY-MM-DD HH:MM"
    example: "2025-12-31 23:59"
  recurrence_type:
    type: string
    required: false
    default: "None"
    enum: ["None", "Daily", "Weekly"]
  priority:
    type: string
    required: false
    default: "Medium"
    enum: ["High", "Medium", "Low"]
  tags:
    type: array
    required: false
    default: []
    max_items: 20
```

### Output Schema

```yaml
status: success | error
task:
  id: integer
  title: string
  description: string
  status: "Pending"
  priority: string
  tags: string[]
  due_date: string | null  # "YYYY-MM-DD HH:MM" or null
  recurrence_type: string  # "None", "Daily", or "Weekly"
error:
  code: VALIDATION_ERROR | INTERNAL_ERROR
  message: string
```

### Errors

| Code | Condition | Message Example |
|------|-----------|-----------------|
| VALIDATION_ERROR | Invalid date format | "Invalid due_date format. Use YYYY-MM-DD HH:MM" |
| VALIDATION_ERROR | Title empty | "Title cannot be empty" |
| VALIDATION_ERROR | Invalid recurrence type | "recurrence_type must be 'None', 'Daily', or 'Weekly'" |

---

## Update Task Command

### Input Schema

```yaml
command: update-task
parameters:
  task_id:
    type: integer
    required: true
  title:
    type: string
    required: false
    min_length: 1
    max_length: 100
  description:
    type: string
    required: false
    max_length: 500
  due_date:
    type: string | null
    required: false
    format: "YYYY-MM-DD HH:MM"
  recurrence_type:
    type: string
    required: false
    enum: ["None", "Daily", "Weekly"]
  priority:
    type: string
    required: false
    enum: ["High", "Medium", "Low"]
  tags:
    type: array | null
    required: false
    max_items: 20
```

### Output Schema

```yaml
status: success | error
task:
  # Same as create-task output
error:
  code: VALIDATION_ERROR | NOT_FOUND | INTERNAL_ERROR
  message: string
```

### Errors

| Code | Condition | Message Example |
|------|-----------|-----------------|
| NOT_FOUND | Task ID not found | "Task 42 not found" |
