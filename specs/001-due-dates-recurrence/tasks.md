# Tasks: Due Dates & Recurrence

**Input**: Design documents from `/specs/001-due-dates-recurrence/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: No test tasks included - tests were not explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create RecurrenceType enum in src/todo/models/task.py
- [x] T002 [P] Create RecurrenceManager class stub in src/todo/logic/recurrence.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Add due_date and recurrence_type fields to Task dataclass in src/todo/models/task.py
- [x] T004 [P] Add due_date and recurrence_type to TaskCreateSchema in src/todo/validation/schemas.py
- [x] T005 [P] Add due_date and recurrence_type to TaskUpdateSchema in src/todo/validation/schemas.py
- [x] T006 Implement date format validator (YYYY-MM-DD HH:MM) in src/todo/validation/schemas.py
- [x] T007 [P] Implement RecurrenceType validator in src/todo/validation/schemas.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Due Date to Task (Priority: P1) 🎯 MVP

**Goal**: Users can add optional due dates to any task, stored and displayed correctly.

**Independent Test**: Create tasks with and without due dates, verify storage and display of due date information.

### Implementation for User Story 1

- [x] T008 [P] [US1] Add due_date input prompt to task creation flow in src/todo/ui/menu.py
- [x] T009 [P] [US1] Add due_date input prompt to task update flow in src/todo/ui/menu.py
- [x] T010 [P] [US1] Update storage.create_task() to handle due_date in src/todo/logic/storage.py
- [x] T011 [US1] Update storage.update_task() to handle due_date in src/todo/logic/storage.py
- [x] T012 [US1] Display due_date in task list table in src/todo/ui/menu.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Identify Overdue and Upcoming Tasks (Priority: P1)

**Goal**: Tasks display "Overdue" (red bold) or "Due Soon" (yellow) status indicators based on due date.

**Independent Test**: Create tasks with various due dates (past, present, future, within 24 hours), verify correct indicators appear.

### Implementation for User Story 2

- [x] T013 [P] [US2] Implement check_due_status() method in RecurrenceManager in src/todo/logic/recurrence.py
- [x] T014 [US2] Add "Status/Deadline" column to task list table in src/todo/ui/menu.py
- [x] T015 [US2] Implement red bold styling for overdue tasks in src/todo/ui/menu.py
- [x] T016 [US2] Implement yellow styling for due soon tasks in src/todo/ui/menu.py
- [x] T017 [US2] Handle "No Deadline" display for tasks without due date in src/todo/ui/menu.py
- [x] T018 [US2] Add startup summary showing overdue task count in src/todo/ui/menu.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Create Recurring Daily Tasks (Priority: P2)

**Goal**: Mark tasks as "Daily" recurring; completing them automatically creates next instance with due_date +1 day.

**Independent Test**: Create a daily recurring task, complete it, verify a new task is created for next day.

### Implementation for User Story 3

- [x] T019 [P] [US3] Add recurrence_type input prompt to task creation flow in src/todo/ui/menu.py
- [x] T020 [P] [US3] Add recurrence_type input prompt to task update flow in src/todo/ui/menu.py
- [x] T021 [US3] Update storage.create_task() to handle recurrence_type in src/todo/logic/storage.py
- [x] T022 [US3] Update storage.update_task() to handle recurrence_type in src/todo/logic/storage.py
- [x] T023 [US3] Implement handle_recurrence() method for Daily in RecurrenceManager in src/todo/logic/recurrence.py
- [x] T024 [US3] Wire RecurrenceManager.handle_recurrence() into storage.complete_task() in src/todo/logic/storage.py
- [x] T025 [US3] Display recurrence_type in task list table in src/todo/ui/menu.py

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all be independently functional

---

## Phase 6: User Story 4 - Create Recurring Weekly Tasks (Priority: P3)

**Goal**: Mark tasks as "Weekly" recurring; completing them automatically creates next instance with due_date +7 days.

**Independent Test**: Create a weekly recurring task, complete it, verify a new task is created for next week.

### Implementation for User Story 4

- [x] T026 [US4] Implement Weekly recurrence logic in RecurrenceManager.handle_recurrence() in src/todo/logic/recurrence.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T027 [P] Apply skill-cli-beautification for professional warning messages in src/todo/ui/menu.py
- [ ] T028 [P] Update quickstart.md validation to reflect implementation
- [ ] T029 Run and validate all acceptance scenarios from spec.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in priority order: P1 (US1) → P1 (US2) → P2 (US3) → P3 (US4)
  - US1 and US2 are both P1, implement together for full MVP
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) and US1 complete - Uses due_date fields from US1
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) and US1 complete - Uses due_date fields and recurrence_type
- **User Story 4 (P3)**: Can start after Foundational (Phase 2), US1 complete, US3 complete - Extends RecurrenceManager from US3

### Within Each User Story

- Input prompts in UI before storage updates
- Storage updates before display changes
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- All UI input prompt tasks within a story marked [P] can run in parallel
- All storage update tasks within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members (after US1/US2 MVP)

---

## Parallel Example: User Story 1

```bash
# Launch all UI input prompts together:
Task: "T008 [P] [US1] Add due_date input prompt to task creation flow in src/todo/ui/menu.py"
Task: "T009 [P] [US1] Add due_date input prompt to task update flow in src/todo/ui/menu.py"

# Launch all storage updates together:
Task: "T010 [P] [US1] Update storage.create_task() to handle due_date in src/todo/logic/storage.py"
Task: "T011 [P] [US1] Update storage.update_task() to handle due_date in src/todo/logic/storage.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. Complete Phase 4: User Story 2
5. **STOP and VALIDATE**: Test User Stories 1 & 2 independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (Due Dates)
3. Add User Story 2 → Test independently → Deploy/Demo (Status Indicators - Full MVP!)
4. Add User Story 3 → Test independently → Deploy/Demo (Daily Recurrence)
5. Add User Story 4 → Test independently → Deploy/Demo (Weekly Recurrence)
6. Polish and validate
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Due Dates)
   - Developer B: User Story 2 (Status Indicators) - after US1 starts
3. Together: User Stories 1 & 2 = MVP (complete before moving on)
4. Developer C: User Story 3 (Daily Recurrence) - after MVP
5. Developer D: User Story 4 (Weekly Recurrence) - after US3
6. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- US1 and US2 form the complete MVP for due dates functionality
- US3 and US4 add recurrence automation on top of MVP
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Apply skill-cli-beautification (T027) ensures professional CLI output
- RecurrenceManager encapsulates all recurrence logic (US3 + US4)
