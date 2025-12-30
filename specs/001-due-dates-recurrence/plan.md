# Implementation Plan: Due Dates & Recurrence

**Branch**: `001-due-dates-recurrence` | **Date**: 2025-12-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-due-dates-recurrence/spec.md`

**Note**: This template is filled in by `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Add optional due date fields and recurrence automation to the Task model. Tasks will display "Overdue" (red bold) or "Due Soon" status based on date comparisons. Daily/Weekly recurrence creates next instance upon completion. User strategy specifies: data model updates (datetime due_date, Enum recurrence_type), RecurrenceManager for task generation, Rich table enhancements with dynamic colors, and startup summary of overdue tasks.

## Technical Context

**Language/Version**: Python 3.13+ (per constitution)
**Primary Dependencies**: pydantic (validation), rich (CLI), pytest (testing)
**Storage**: In-memory dictionary (per FR-012 maintain in-memory constraint)
**Testing**: pytest (existing framework)
**Target Platform**: Linux console application (single project)
**Project Type**: Single console application
**Performance Goals**: <100ms task list display, instant recurrence generation
**Constraints**: No external storage, no database migration, in-memory only
**Scale/Scope**: ~1000 tasks max per session (in-memory limitation)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Logic-First Architecture (PASS)
- RecurrenceManager will handle business logic for task generation (independent of UI)
- Time comparison logic encapsulated in dedicated service module
- All date calculations isolated from display concerns

### UX-Driven Interactions (PASS)
- Rich table updates with dynamic colors handled by UI module
- Startup summary message (overdue count) in UI layer
- Display logic decoupled from business logic

### Input Validation Guardianship (PASS)
- Date format validation (YYYY-MM-DD HH:MM) via pydantic schemas
- Recurrence type validation via Enum
- Clear error messages for invalid dates (FR-011)

### Modular Code Architecture (PASS)
- New fields (due_date, recurrence_type) extend existing Task dataclass
- RecurrenceManager is separate module, easy to migrate to Phase II
- No tight coupling between logic and UI layers

### Code Quality Standards (PASS)
- Adherence to PEP 8 in all new code
- Meaningful names (RecurrenceManager, TaskStatus enum)
- Existing patterns (dataclass + pydantic) maintained

### Feature Completeness (PASS)
- Extending existing feature set (Add/View/Update/Delete/Complete)
- New capabilities (due dates, recurrence) integrate with existing CRUD
- No new core operations beyond spec requirements

**Result**: ALL GATES PASS. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-due-dates-recurrence/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── models/
│   ├── task.py            # Updated: Add due_date, recurrence_type fields
│   └── __init__.py
├── logic/
│   ├── storage.py         # Updated: Complete method to call RecurrenceManager
│   ├── recurrence.py      # NEW: RecurrenceManager class
│   └── __init__.py
├── ui/
│   ├── menu.py            # Updated: Rich table with Status/Deadline column, startup summary
│   └── __init__.py
├── validation/
│   ├── schemas.py         # Updated: Date format validators, recurrence validators
│   └── __init__.py
└── controller.py         # Updated: Wire RecurrenceManager into completion flow

tests/
├── contract/              # Contracts from Phase 1
├── integration/
│   └── test_recurrence_integration.py  # NEW: End-to-end recurrence tests
└── unit/
    ├── test_recurrence_logic.py       # NEW: RecurrenceManager unit tests
    ├── test_task_model.py            # Updated: New fields tests
    └── test_schemas.py              # Updated: Date validation tests
```

**Structure Decision**: Single project structure maintained (Option 1). All new modules follow existing pattern: models/ for data structures, logic/ for business rules, validation/ for input guards, ui/ for presentation. No new directories added to maintain consistency with existing codebase.

## Complexity Tracking

> **No violations to document** - All constitution gates passed.
