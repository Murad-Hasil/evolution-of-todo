---
id: 0003
title: Generate Due Dates Recurrence Tasks
stage: tasks
date: 2025-12-30
surface: agent
model: claude-sonnet-4.5
feature: 001-due-dates-recurrence
branch: 001-due-dates-recurrence
user: Murad Hasil (mbmuradhasil@gmail.com)
command: /sp.tasks
labels: ["tasks","implementation","due-dates","recurrence"]
links:
  spec: ../../specs/001-due-dates-recurrence/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-due-dates-recurrence/tasks.md
tests:
  - No test tasks generated (not explicitly requested in spec)

## Prompt

1. Update 'src/models.py': Add 'due_date' and 'recurrence' fields to the Task class.
2. Update 'src/logic.py': Implement 'check_due_status()' and 'handle_recurrence()' methods.
3. Update 'src/main.py': Add inputs for Due Date (with validation) and Recurrence options when adding/updating tasks.
4. Update 'src/main.py': Enhance the 'View' table to show a "Due In" column (e.g., "2 hours left", "Overdue").
5. Apply 'skill-cli-beautification' to ensure warnings look professional.

## Response snapshot

Generated 29 tasks organized by user story for independent implementation and testing.

**Phase Distribution**:
- Phase 1 (Setup): 2 tasks (RecurrenceType enum, RecurrenceManager stub)
- Phase 2 (Foundational): 5 tasks (model extensions, schema validators)
- Phase 3 (User Story 1): 5 tasks (due date input, storage, display)
- Phase 4 (User Story 2): 6 tasks (status logic, indicators, styling)
- Phase 5 (User Story 3): 7 tasks (daily recurrence flow)
- Phase 6 (User Story 4): 1 task (weekly recurrence logic)
- Phase 7 (Polish): 3 tasks (CLI beautification, validation)

**User Story Mapping**:
- US1 (Add Due Date): Tasks T008-T012 - independent, testable MVP slice
- US2 (Identify Overdue): Tasks T013-T018 - adds status indicators
- US3 (Daily Recurrence): Tasks T019-T025 - recurrence automation
- US4 (Weekly Recurrence): Task T026 - extends recurrence logic

**Dependencies**: Foundational phase blocks all user stories. US1 and US2 form complete MVP. US3/US4 add incremental value.

**Parallel Opportunities**: 12 tasks marked [P] can run in parallel across phases.

## Outcome

- ✅ Impact: Generated 29 actionable, dependency-ordered tasks organized by user story for independent implementation
- 🧪 Tests: No test tasks (not requested in spec)
- 📁 Files: Created tasks.md in specs/001-due-dates-recurrence/
- 🔁 Next prompts: Ready for /sp.implement to execute task generation
- 🧠 Reflection: Tasks follow user story structure enabling incremental delivery. MVP (US1+US2) delivers core due dates functionality. Each story independently testable.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All tasks follow checklist format, include file paths, story labels, and [P] markers
- Prompt variant: N/A
- Next experiment: N/A - tasks are complete and ready for execution
