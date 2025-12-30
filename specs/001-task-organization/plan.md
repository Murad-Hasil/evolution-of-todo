# Implementation Plan: Task Organization - Priorities, Categories, and Search

**Branch**: `001-task-organization` | **Date**: 2025-12-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-task-organization/spec.md`

**Note**: This template is filled in by `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Enhance the in-memory Todo CLI application with organizational features including priority levels (High/Medium/Low with default Medium), multi-tag categorization, keyword search across titles/descriptions with partial matching, filtering by status/priority/tag with simultaneous filter support, and sorting by title (A-Z) or priority (High→Low). The implementation follows the constitution's Logic-First, UX-Driven, and Validation Guardianship principles with modular code design for Phase II migration readiness.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: pydantic (validation), rich (CLI), pytest (testing)
**Storage**: In-memory dictionary (`Dict[int, Task]`)
**Testing**: pytest
**Target Platform**: Linux/WSL (CLI terminal)
**Project Type**: Single project (Python CLI app)
**Performance Goals**: Search/Filter/Sort operations < 1 second for up to 10,000 tasks
**Constraints**: Single-user, no concurrency, in-memory only (<100MB for 10k tasks)
**Scale/Scope**: Up to 10,000 tasks in memory, CLI interface

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Constitution Principle | Compliance Status | Notes |
|---------------------|-------------------|--------|
| Logic-First Architecture | ✅ PASS | Business logic (search/filter/sort) will be in TaskStorage class; UI concerns remain in menu module |
| UX-Driven Interactions | ✅ PASS | CLI display and user interaction enhancements in menu.py with Rich formatting |
| Input Validation Guardianship | ✅ PASS | Pydantic schemas will validate priority enum and tag inputs; validation module extended |
| Modular Code Architecture | ✅ PASS | Task model, storage logic, validation, and UI remain in separate modules for Phase II migration |
| Code Quality Standards | ✅ PASS | All code follows PEP 8 and clean code principles |
| Feature Completeness | ✅ PASS | Extends existing core features (Add, View, Update) with organizational capabilities |

**GATE RESULT**: ✅ PASS - No constitution violations. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-task-organization/
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
├── todo/
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py              # MODIFIED: Add Priority enum, tags field
│   ├── logic/
│   │   ├── __init__.py
│   │   └── storage.py           # MODIFIED: Add search, filter, sort methods
│   ├── validation/
│   │   ├── __init__.py
│   │   └── schemas.py           # MODIFIED: Add priority validation, tag validation
│   └── ui/
│       ├── __init__.py
│       └── menu.py               # MODIFIED: Add filter/sort options, display priority/tags
├── todo/
│   ├── __init__.py
│   ├── controller.py             # MODIFIED: Wire up filter/sort UI commands
│   └── main.py                  # MODIFIED: Add list command filter/sort subcommands
tests/
├── contract/
│   └── test_task_organization_contracts.py  # NEW: Test API contracts
├── integration/
│   └── test_task_organization_integration.py  # NEW: End-to-end tests
└── unit/
    ├── test_task_model.py          # MODIFIED: Test priority enum and tags
    ├── test_storage_search.py     # NEW: Test search functionality
    ├── test_storage_filter.py     # NEW: Test filter functionality
    ├── test_storage_sort.py      # NEW: Test sort functionality
    └── test_schemas.py           # MODIFIED: Test priority/tag validation
```

**Structure Decision**: Single project structure maintained, following existing modular architecture. Logic (`storage.py`), Validation (`schemas.py`), and UI (`menu.py`) modules are extended rather than replaced, preserving backward compatibility and Phase II migration readiness. New test files cover the new functionality while existing tests continue to validate core features.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No complexity tracking entries - all constitution gates passed.*
