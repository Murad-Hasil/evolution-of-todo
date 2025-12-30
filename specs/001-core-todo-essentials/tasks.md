# Tasks: Phase I - Core Todo Essentials

**Input**: Design documents from `/specs/001-core-todo-essentials/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included as standard practice for Python development, focusing on the logic layer.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize UV project with `uv init`
- [x] T002 Install dependencies (`rich`, `pydantic`, `pytest`) using `uv add`
- [x] T003 Create directory structure (`src/todo`, `src/todo/logic`, `src/todo/ui`, `src/todo/validation`, `src/todo/models`)
- [x] T004 [P] Configure `pyproject.toml` with project metadata and script entry point

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create base `Task` dataclass in `src/todo/models/task.py`
- [x] T006 Implement base `TaskStorage` memory structure in `src/todo/logic/storage.py`
- [x] T007 [P] Create validation schemas in `src/todo/validation/schemas.py`
- [x] T008 [P] Initialize `Console` and basic UI components in `src/todo/ui/menu.py`
- [x] T009 Create centralized `TodoController` in `src/todo/controller.py` to orchestrate flows

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Allow users to add tasks with title/description and view them in a beautified table.

**Independent Test**: Add a task via the CLI and verify it appears in the list output with ID 1 and "Pending" status.

### Tests for User Story 1
- [x] T010 [P] [US1] Unit test for `add_task` in `tests/unit/test_logic.py`
- [x] T011 [P] [US1] Unit test for `get_all_tasks` in `tests/unit/test_logic.py`

### Implementation for User Story 1
- [x] T012 [US1] Implement `add_task` logic in `src/todo/logic/storage.py`
- [x] T013 [US1] Implement `get_all_tasks` logic in `src/todo/logic/storage.py`
- [x] T014 [US1] Create `render_task_table` in `src/todo/ui/menu.py` using Rich Table
- [x] T015 [US1] Implement "add" and "list" flows in `src/todo/controller.py`
- [x] T016 [US1] Create the main REPL loop and menu in `src/todo/main.py`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently (MVP).

---

## Phase 4: User Story 2 - Task Lifecycle Management (Priority: P2)

**Goal**: Allow users to update, delete, and mark tasks as complete.

**Independent Test**: Mark an existing task as complete and verify its status changes in the list; update a task and verify changes; delete a task and verify its removal.

### Tests for User Story 2
- [x] T017 [P] [US2] Unit test for `update_task` in `tests/unit/test_logic.py`
- [x] T018 [P] [US2] Unit test for `delete_task` in `tests/unit/test_logic.py`

### Implementation for User Story 2
- [x] T019 [US2] Implement `update_task` logic in `src/todo/logic/storage.py` (mapping to complete toggle too)
- [x] T020 [US2] Implement `delete_task` logic in `src/todo/logic/storage.py`
- [x] T021 [US2] Create update and delete interaction prompt in `src/todo/ui/menu.py`
- [x] T022 [US2] Implement "update", "delete", and "complete" flows in `src/todo/controller.py`
- [x] T023 [US2] Register new commands in the main loop in `src/todo/main.py`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T024 [P] Update `CLAUDE.md` with build/run/test instructions
- [x] T025 Add error handling for non-existent IDs in `src/todo/validation/schemas.py`
- [x] T026 [P] Run final validation against `quickstart.md`
- [x] T027 Code cleanup (Refactor imports, ensure type hints)

---

## Dependencies & Execution Order

### Phase Dependencies
- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all stories.
- **User Stories (Phase 3+)**: Depend on Foundational phase.
- **Polish (Final Phase)**: Depends on all user stories.

### Parallel Opportunities
- T003, T004 (Structure and Config)
- T007, T008 (Validation and UI)
- T010, T011 (Logic tests)
- T017, T018 (Lifecycle tests)

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test CLI add/list.

### Incremental Delivery
1. Foundation Ready
2. Add/List Ready (MVP)
3. Lifecycle Ready (Full Feature)
4. Polish Applied
