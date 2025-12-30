# Quickstart Guide: Due Dates & Recurrence

**Feature**: Due Dates & Recurrence | **Date**: 2025-12-30

## Overview

This feature extends the existing Todo application with:
- Optional due dates for tasks (format: YYYY-MM-DD HH:MM)
- Automatic status indicators: Overdue (red bold), Due Soon (yellow)
- Recurring tasks: Daily and Weekly patterns
- Startup summary showing overdue task count

## User Flow

### 1. Create Task with Due Date

```bash
$ python main.py
> create
Title: Pay electricity bill
Description: Monthly utility payment
Due date (YYYY-MM-DD HH:MM): 2025-12-31 09:00
Recurrence (None/Daily/Weekly): Monthly
Priority (High/Medium/Low): High
Tags: bills,utility

✓ Task created: [1] Pay electricity bill (Due: 2025-12-31 09:00)
```

### 2. View Task List with Status

```bash
> list

ID | Title               | Status   | Priority | Due Date       | Status/Deadline
---|---------------------|----------|----------|----------------|----------------
1  | Pay electricity bill| Pending  | High     | Dec 31, 09:00  | [OVERDUE] ⚠️
2  | Weekly report       | Pending  | Medium   | Jan 05, 14:00  | [DUE SOON] ⏰
3  | Call client          | Pending  | Low      | Jan 10, 10:00  | On Track
4  | Review docs         | Pending  | Medium   | -              | No Deadline

You have 1 overdue task(s). ⚠️
```

### 3. Complete Recurring Task

```bash
> complete 1

✓ Task completed: [1] Pay electricity bill
✓ Recurring task created: [5] Pay electricity bill (Due: 2026-01-01 09:00)
```

## Recurrence Behavior

### Daily Recurrence

When a Daily task is completed:
- New task created automatically
- Due date incremented by 1 day
- Same title, description, priority, tags
- Recurrence type preserved

**Example**:
- Completed: "Check email" (Due: 2025-12-30)
- Created: "Check email" (Due: 2025-12-31)

### Weekly Recurrence

When a Weekly task is completed:
- New task created automatically
- Due date incremented by 7 days
- Same attributes preserved

**Example**:
- Completed: "Team sync" (Due: 2025-12-30)
- Created: "Team sync" (Due: 2026-01-06)

### No Recurrence

- Task marked as complete
- No new task created

## Status Indicators

| Status | Condition | Visual |
|--------|-----------|---------|
| OVERDUE | Due date in the past | Red bold text |
| DUE SOON | Due within 24 hours | Yellow text |
| ON TRACK | Due more than 24 hours away | Normal text |
| NO DEADLINE | No due date set | Gray dash |

## Error Handling

### Invalid Date Format

```bash
> update 2
Due date: tomorrow
✗ Invalid due_date format. Use YYYY-MM-DD HH:MM
```

### Invalid Recurrence Type

```bash
> create
Title: Gym workout
Recurrence: Monthly
✗ recurrence_type must be 'None', 'Daily', or 'Weekly'
```

## Developer Notes

### Module Changes

| Module | Change |
|--------|---------|
| `src/todo/models/task.py` | Add `due_date`, `recurrence_type` fields |
| `src/todo/logic/recurrence.py` | NEW: `RecurrenceManager` class |
| `src/todo/logic/storage.py` | Wire `RecurrenceManager` in `complete_task()` |
| `src/todo/validation/schemas.py` | Add date validators |
| `src/todo/ui/menu.py` | Add status column, dynamic colors, startup summary |

### Testing

```bash
# Run all tests
pytest

# Run recurrence tests
pytest tests/unit/test_recurrence_logic.py

# Run integration tests
pytest tests/integration/test_recurrence_integration.py
```

## Next Steps

1. Implement `RecurrenceManager` in `src/todo/logic/recurrence.py`
2. Extend `Task` model with new fields
3. Update pydantic schemas with date validation
4. Add status column to Rich table with conditional formatting
5. Implement startup overdue summary
6. Write unit and integration tests
7. Run `/sp.tasks` to generate implementation tasks
