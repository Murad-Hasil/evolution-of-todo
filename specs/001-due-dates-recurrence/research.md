# Research: Due Dates & Recurrence

**Date**: 2025-12-30 | **Feature**: Due Dates & Recurrence

## No Unknowns to Resolve

All technical decisions were derivable from:
1. Existing codebase patterns (pydantic dataclasses, rich CLI)
2. Feature specification requirements
3. Constitution mandates (modularity, logic-first, validation)

## Technical Approach Confirmed

### 1. Python datetime for Due Date Handling

**Decision**: Use `datetime.datetime` for due_date field in Task model

**Rationale**:
- Native Python library (no external dependency)
- Supports direct comparison with `datetime.now()`
- Easy arithmetic: `due_date + timedelta(days=1)` for daily recurrence
- String parsing via `datetime.strptime()` for user input

**Format**: YYYY-MM-DD HH:MM as specified

### 2. Enum for Recurrence Type

**Decision**: Create `RecurrenceType(str, Enum)` with values: NONE, DAILY, WEEKLY

**Rationale**:
- Type-safe values (not string literals)
- Easy validation in pydantic schemas
- Clear intent in code: `if task.recurrence == RecurrenceType.DAILY`
- Future-extensible for MONTHLY, CUSTOM patterns

### 3. RecurrenceManager Pattern

**Decision**: Dedicated `RecurrenceManager` class in logic/recurrence.py

**Rationale**:
- Follows constitution: "Logic-First Architecture"
- Encapsulates recurrence rules independently from UI
- Single responsibility: handle task generation logic
- Easy to test in isolation
- Ready for Phase II migration

### 4. Rich Table Styling

**Decision**: Use Rich `Style` and `Text` for dynamic column colors

**Rationale**:
- Existing dependency (Rich library)
- Rich `Style(color="red", bold=True)` for overdue
- Conditional formatting in table cells
- No new dependencies required

### 5. In-Memory Storage

**Decision**: Extend existing `Dict[int, Task]` storage

**Rationale**:
- Existing constraint from constitution (Phase I: in-memory)
- No changes to storage interface
- Recurrence creates new task with auto-incremented ID

## Validation Approach

**Decision**: Extend pydantic schemas with date format validation

**Implementation**:
- `TaskCreateSchema`: Optional due_date field with format validation
- `TaskUpdateSchema`: Optional due_date field with format validation
- `RecurrenceType` field in both schemas
- Custom `@field_validator` for YYYY-MM-DD HH:MM format

## Edge Cases Identified

| Edge Case | Handling |
|-----------|----------|
| Invalid date format | Reject with clear error message |
| Past due date | Accept (user may set historical due date) |
| No due date + recurrence | Create next instance without due date |
| Overdue task completed | Create next instance (not skipped) |
| Timezone confusion | Assume local system time |

## References

- Python datetime: https://docs.python.org/3/library/datetime.html
- Rich library: https://rich.readthedocs.io/
- Pydantic validators: https://docs.pydantic.dev/latest/guides/validators/
