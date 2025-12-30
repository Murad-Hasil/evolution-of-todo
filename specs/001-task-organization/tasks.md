# Tasks: Task Organization - Priorities, Categories, and Search

**Input**: Design documents from `/specs/001-task-organization/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included as specified in the feature specification and user request includes TDD approach through agent skills.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Verify existing project structure matches plan.md (src/todo/models/task.py, src/todo/logic/storage.py, src/todo/validation/schemas.py, src/todo/ui/menu.py, src/todo/controller.py, src/todo/main.py)
- [ ] T002 Verify dependencies are installed (pydantic>=2.12.5, rich>=14.2.0, pytest>=9.0.2)
- [ ] T003 Run existing tests to ensure baseline functionality: `pytest tests/ -v`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Create Priority enumeration in src/todo/models/task.py (HIGH="High", MEDIUM="Medium", LOW="Low" as str Enum)
- [ ] T005 [P] Extend Task dataclass in src/todo/models/task.py with priority field (default=Priority.MEDIUM) and tags field (default_factory=list)
- [ ] T006 [P] Update TaskCreateSchema in src/todo/validation/schemas.py to accept priority (default=Priority.MEDIUM) and tags list with uniqueness validator
- [ ] T007 [P] Update TaskUpdateSchema in src/todo/validation/schemas.py to support optional priority and tags updates
- [ ] T008 Update TaskStorage.add_task() in src/todo/logic/storage.py signature to accept priority and tags parameters
- [ ] T009 Update TaskStorage.update_task() in src/todo/logic/storage.py to support priority and tags updates
- [ ] T010 Update render_task_table() in src/todo/ui/menu.py to display Priority column (color-coded: red=High, yellow=Medium, green=Low) and Tags column (comma-separated)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Task Prioritization (Priority: P1) 🎯 MVP

**Goal**: Users can assign priority levels (High/Medium/Low) to each task with Medium as default. Tasks display priority clearly in the list.

**Independent Test**: Create task with priority, verify default is Medium, update task priority, and confirm priority displays in task list with correct color coding.

### Tests for User Story 1 (TDD Approach) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T011 [P] [US1] Contract test for Priority enum in tests/unit/test_task_model.py - verify HIGH, MEDIUM, LOW values
- [ ] T012 [P] [US1] Unit test for Task with priority default in tests/unit/test_task_model.py - verify new tasks default to Priority.MEDIUM
- [ ] T013 [P] [US1] Unit test for TaskCreateSchema priority validation in tests/unit/test_schemas.py - verify only "High"/"Medium"/"Low" accepted
- [ ] T014 [P] [US1] Integration test for priority display in tests/integration/test_task_organization_integration.py - create task with High priority, verify red color in table output

### Implementation for User Story 1

- [ ] T015 [P] [US1] Create Priority enum (str, Enum) in src/todo/models/task.py with HIGH, MEDIUM, LOW values
- [ ] T016 [US1] Add priority field to Task dataclass in src/todo/models/task.py with type Priority and default Priority.MEDIUM
- [ ] T017 [US1] Update TaskStorage.add_task() in src/todo/logic/storage.py to accept priority parameter and pass to Task constructor
- [ ] T018 [US1] Update TaskStorage.update_task() in src/todo/logic/storage.py to support priority parameter updates
- [ ] T019 [US1] Add priority field to TaskCreateSchema in src/todo/validation/schemas.py with Field(default=Priority.MEDIUM) and enum validator
- [ ] T020 [US1] Add priority field to TaskUpdateSchema in src/todo/validation/schemas.py as Optional[Priority]
- [ ] T021 [US1] Add Priority column to task table in src/todo/ui/menu.py render_task_table() with color mapping (red/yellow/green)
- [ ] T022 [US1] Update TodoController.add_task() in src/todo/controller.py to prompt for priority using menu.Prompt.ask() with default "Medium"
- [ ] T023 [US1] Update TodoController.update_task() in src/todo/controller.py to prompt for priority update
- [ ] T024 [US1] Verify priority color coding in task table display (red=High, yellow=Medium, green=Low) in src/todo/ui/menu.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Categorization with Tags (Priority: P2)

**Goal**: Users can apply zero or more tags to each task (e.g., "Work", "Personal"). Tags display in task list and can be used for filtering.

**Independent Test**: Create task with multiple tags, update task tags, remove all tags, verify tags display in task list, and filter tasks by specific tag.

### Tests for User Story 2 (TDD Approach) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T025 [P] [US2] Unit test for Task with tags field in tests/unit/test_task_model.py - verify empty list default, multiple tags support
- [ ] T026 [P] [US2] Unit test for TaskCreateSchema tags validation in tests/unit/test_schemas.py - verify duplicate removal, max 20 tags, max 30 chars each
- [ ] T027 [P] [US2] Integration test for tag display in tests/integration/test_task_organization_integration.py - create task with tags, verify comma-separated display
- [ ] T028 [P] [US2] Unit test for TaskStorage.filter_tasks() by tag in tests/unit/test_storage_filter.py - verify tag filtering logic

### Implementation for User Story 2

- [ ] T029 [P] [US2] Add tags field to Task dataclass in src/todo/models/task.py with type List[str] and default_factory=list
- [ ] T030 [US2] Update TaskStorage.add_task() in src/todo/logic/storage.py to accept tags list parameter and pass to Task constructor
- [ ] T031 [US2] Update TaskStorage.update_task() in src/todo/logic/storage.py to support tags list updates (replaces existing tags)
- [ ] T032 [US2] Add tags field to TaskCreateSchema in src/todo/validation/schemas.py with Field(default_factory=list, max_length=20)
- [ ] T033 [US2] Add tags_unique validator to TaskCreateSchema in src/todo/validation/schemas.py - strip whitespace, remove empty tags, deduplicate within list
- [ ] T034 [US2] Add tags field to TaskUpdateSchema in src/todo/validation/schemas.py as Optional[List[str]]
- [ ] T035 [US2] Add tags_unique validator to TaskUpdateSchema in src/todo/validation/schemas.py - same logic as create schema
- [ ] T036 [US2] Add Tags column to task table in src/todo/ui/menu.py render_task_table() - display comma-separated tags or empty string
- [ ] T037 [US2] Update TodoController.add_task() in src/todo/controller.py to prompt for tags using menu.Prompt.ask() with default "" (parse comma-separated)
- [ ] T038 [US2] Update TodoController.update_task() in src/todo/controller.py to prompt for tags update
- [ ] T039 [US2] Implement TaskStorage.filter_tasks() method in src/todo/logic/storage.py with status, priority, and tag parameters using sequential AND logic

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Keyword Search (Priority: P3)

**Goal**: Users can search for tasks by keywords in title or description with case-insensitive partial matching (e.g., "proj" finds "project").

**Independent Test**: Create tasks with keywords in titles and descriptions, search with partial word, search with different case, verify matching tasks returned.

### Tests for User Story 3 (TDD Approach) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T040 [P] [US3] Unit test for search empty keyword in tests/unit/test_storage_search.py - verify returns all tasks
- [ ] T041 [P] [US3] Unit test for search case-insensitive in tests/unit/test_storage_search.py - verify "URGENT" finds "urgent"
- [ ] T042 [P] [US3] Unit test for search partial match in tests/unit/test_storage_search.py - verify "proj" finds "project"
- [ ] T043 [P] [US3] Unit test for search title vs description in tests/unit/test_storage_search.py - verify matches in either field
- [ ] T044 [P] [US3] Integration test for search UI in tests/integration/test_task_organization_integration.py - search from CLI, verify table shows matches

### Implementation for User Story 3

- [ ] T045 [US3] Implement TaskStorage.search_tasks() method in src/todo/logic/storage.py with keyword parameter - case-insensitive substring search in title and description
- [ ] T046 [US3] Add search input collection in src/todo/ui/menu.py - create get_search_keyword() function using menu.Prompt.ask()
- [ ] T047 [US3] Integrate search into TodoController.list_tasks() in src/todo/controller.py - call search if keyword provided
- [ ] T048 [US3] Update task table empty state handling in src/todo/ui/menu.py - show "No tasks found" when search returns empty

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Task Filtering (Priority: P4)

**Goal**: Users can filter tasks by completion status, priority level, or specific tag. Multiple filters can be applied simultaneously with AND logic.

**Independent Test**: Create tasks with various statuses/priorities/tags, apply single filter, apply multiple filters simultaneously, verify correct results.

### Tests for User Story 4 (TDD Approach) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T049 [P] [US4] Unit test for filter by status in tests/unit/test_storage_filter.py - verify "Pending" and "Completed" filtering
- [ ] T050 [P] [US4] Unit test for filter by priority in tests/unit/test_storage_filter.py - verify High/Medium/Low filtering
- [ ] T051 [P] [US4] Unit test for filter by tag in tests/unit/test_storage_filter.py - verify exact tag matching (case-sensitive)
- [ ] T052 [P] [US4] Unit test for filter multiple criteria in tests/unit/test_storage_filter.py - verify AND logic for status+priority+tag
- [ ] T053 [P] [US4] Integration test for filter UI in tests/integration/test_task_organization_integration.py - apply filters from CLI, verify table

### Implementation for User Story 4

- [ ] T054 [US4] Enhance TaskStorage.filter_tasks() method in src/todo/logic/storage.py to support status (Pending/Completed), priority (High/Medium/Low), and tag filtering with AND logic
- [ ] T055 [US4] Add filter input collection in src/todo/ui/menu.py - create get_filter_criteria() function with prompts for status/priority/tag
- [ ] T056 [US4] Integrate filters into TodoController.list_tasks() in src/todo/controller.py - apply filters after optional search
- [ ] T057 [US4] Add filter clear option in src/todo/ui/menu.py get_filter_criteria() - allow "any" or pressing Enter to skip

**Checkpoint**: Task filtering with multiple criteria should now work

---

## Phase 7: User Story 5 - Task Sorting (Priority: P5)

**Goal**: Users can sort tasks by title (A-Z) or priority (High→Medium→Low). Tie-breaking uses task ID.

**Independent Test**: Create tasks with different titles and priorities, sort by title (A-Z), sort by priority (High→Low), verify order and tie-breaking.

### Tests for User Story 5 (TDD Approach) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T058 [P] [US5] Unit test for sort by title in tests/unit/test_storage_sort.py - verify alphabetical A-Z order, case-insensitive
- [ ] T059 [P] [US5] Unit test for sort by priority in tests/unit/test_storage_sort.py - verify High→Medium→Low order
- [ ] T060 [P] [US5] Unit test for sort tie-breaking in tests/unit/test_storage_sort.py - verify task ID used as tie-breaker
- [ ] T061 [P] [US5] Integration test for sort UI in tests/integration/test_task_organization_integration.py - sort from CLI, verify table order

### Implementation for User Story 5

- [ ] T062 [US5] Implement TaskStorage.sort_tasks() method in src/todo/logic/storage.py with sort_by parameter ("title" or "priority") - use tuple key for priority order mapping + ID tie-breaker
- [ ] T063 [US5] Add sort input collection in src/todo/ui/menu.py - create get_sort_option() function with menu.Prompt.ask() and default "title"
- [ ] T064 [US5] Integrate sorting into TodoController.list_tasks() in src/todo/controller.py - apply sort after search and filters
- [ ] T065 [US5] Handle invalid sort_by values in src/todo/logic/storage.py - default to "title" sort

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T066 [P] Run all unit tests: `pytest tests/unit/ -v`
- [ ] T067 [P] Run all integration tests: `pytest tests/integration/ -v`
- [ ] T068 [P] Run all contract tests: `pytest tests/contract/ -v`
- [ ] T069 [P] Run full test suite: `pytest tests/ -v`
- [ ] T070 Verify code passes flake8/black/pylint in src/todo/
- [ ] T071 Update README.md with task organization feature documentation
- [ ] T072 Validate quickstart.md examples work by manual testing of all workflows
- [ ] T073 Performance test: Create 1000 tasks, measure search/filter/sort times (<1 second per success criteria)
- [ ] T074 Check all edge cases from spec.md are handled: empty tags, empty search, no matches, special characters in tags, duplicate tags prevention

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Integrates with US1 model/display but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Uses existing storage, independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Uses storage, independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Uses storage, independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before storage methods
- Storage methods before controller integration
- UI functions before controller integration
- Controller updates before final integration testing
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T001, T002, T003)
- All Foundational tasks marked [P] can run in parallel (within Phase 2: T005, T006, T007)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Tests within Polish phase marked [P] can run in parallel (T066, T067, T068, T070)
- Different user stories can be worked on in parallel by different team members (US1-5)

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (TDD approach):
Task: "Contract test for Priority enum in tests/unit/test_task_model.py"
Task: "Unit test for Task with priority default in tests/unit/test_task_model.py"
Task: "Unit test for TaskCreateSchema priority validation in tests/unit/test_schemas.py"
Task: "Integration test for priority display in tests/integration/test_task_organization_integration.py"

# Launch models and storage implementation together:
Task: "Create Priority enum (str, Enum) in src/todo/models/task.py with HIGH, MEDIUM, LOW values"
Task: "Add priority field to Task dataclass in src/todo/models/task.py"

# Launch validation and UI together:
Task: "Add priority field to TaskCreateSchema in src/todo/validation/schemas.py"
Task: "Add Priority column to task table in src/todo/ui/menu.py render_task_table()"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T010) - **CRITICAL - blocks all stories**
3. Complete Phase 3: User Story 1 (T011-T024)
4. **STOP AND VALIDATE**: Test User Story 1 independently - create tasks with priorities, verify color coding, update priorities
5. Demo priority feature to stakeholders

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Complete Polish → Final delivery

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T010)
2. Once Foundational is done:
   - Developer A: User Story 1 (Priority) - T011-T024
   - Developer B: User Story 2 (Tags) - T025-T039
   - Developer C: User Story 3 (Search) - T040-T048
3. Once US1-US3 done:
   - Developer A: User Story 4 (Filter) - T049-T057
   - Developer B: User Story 5 (Sort) - T062-T065
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD approach)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Total task count: 74 tasks across 8 phases
- User story task distribution: US1=14 tasks, US2=15 tasks, US3=9 tasks, US4=9 tasks, US5=8 tasks
- Suggested MVP scope: Phase 1-3 (Setup, Foundational, User Story 1) = 24 tasks
