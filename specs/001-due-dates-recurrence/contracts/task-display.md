# Contract: Task Display with Status Indicators

**Feature**: Due Dates & Recurrence | **Date**: 2025-12-30

## Task List Display

### Output Schema (Rich Table)

```yaml
columns:
  - id: integer
  - title: string
  - status: string  # "Pending" or "Completed"
  - priority: string
  - due_date: string | "-"  # Formatted or placeholder
  - status_deadline: string  # Computed status
```

### Status/Deadline Column Values

| Computed Status | Condition | Display Style |
|-----------------|-----------|---------------|
| OVERDUE | `due_date < now` | Red Bold text |
| DUE SOON | `now <= due_date <= now + 24h` | Yellow text |
| ON TRACK | `due_date > now + 24h` | Normal (white/gray) |
| NO DEADLINE | `due_date is None` | "-" (gray) |

### Visual Examples

```text
# Overdue task (Red Bold)
ID | Title           | Status   | Due Date       | Status/Deadline
---|-----------------|----------|----------------|----------------
1  | Pay bills       | Pending  | 2025-12-29 09:00 | [OVERDUE] ⚠️

# Due Soon task (Yellow)
ID | Title           | Status   | Due Date       | Status/Deadline
---|-----------------|----------|----------------|----------------
2  | Team meeting    | Pending  | 2025-12-30 10:00 | [DUE SOON] ⏰

# On Track task (Normal)
ID | Title           | Status   | Due Date       | Status/Deadline
---|-----------------|----------|----------------|----------------
3  | Submit report   | Pending  | 2025-12-31 17:00 | On Track

# No deadline (Gray dash)
ID | Title           | Status   | Due Date       | Status/Deadline
---|-----------------|----------|----------------|----------------
4  | Read book       | Pending  | -              | No Deadline
```

---

## Startup Summary

### Console Output

```text
========================================
     TODO LIST - Due Dates Active
========================================

You have X overdue task(s). ⚠️
```

Where `X` is the count of tasks with:
- `status == "Pending"`
- `due_date is not None`
- `due_date < now`

### Examples

- 0 overdue: "You have 0 overdue tasks. ✅"
- 1 overdue: "You have 1 overdue task. ⚠️"
- 3 overdue: "You have 3 overdue tasks. ⚠️"

---

## Date Formatting

### Input Format (User)

```
YYYY-MM-DD HH:MM
```

Examples:
- "2025-12-31 23:59"
- "2025-01-01 00:00"
- "2025-06-15 14:30"

### Display Format (Output)

```
MMM DD, HH:MM
```

Examples:
- "Dec 31, 23:59"
- "Jan 01, 00:00"
- "Jun 15, 14:30"
