---
id: 0002
title: Create Due Dates Recurrence Plan
stage: plan
date: 2025-12-30
surface: agent
model: claude-sonnet-4.5
feature: 001-due-dates-recurrence
branch: 001-due-dates-recurrence
user: Murad Hasil (mbmuradhasil@gmail.com)
command: /sp.plan
labels: ["planning","due-dates","recurrence","architecture"]
links:
  spec: ../../specs/001-due-dates-recurrence/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-due-dates-recurrence/plan.md
  - specs/001-due-dates-recurrence/research.md
  - specs/001-due-dates-recurrence/data-model.md
  - specs/001-due-dates-recurrence/contracts/task-creation.md
  - specs/001-due-dates-recurrence/contracts/task-completion.md
  - specs/001-due-dates-recurrence/contracts/task-display.md
  - specs/001-due-dates-recurrence/quickstart.md
tests:
  - Constitution gates: All 6 gates PASS (Logic-First, UX-Driven, Validation, Modular, Code Quality, Feature Completeness)

## Prompt

Strategy for Advanced Features:
1. Data Model Update: 'logic-specialist' will update the 'Task' model to include 'due_date' (datetime object) and 'recurrence_type' (Enum).
2. Business Logic:
   - Create a 'RecurrenceManager' to handle auto-generation of daily/weekly tasks.
   - Implement a status check that compares 'current_time' with 'due_date'.
3. UI Enhancements: 'ux-specialist' will update the 'Rich' table to include a "Status/Deadline" column with dynamic colors.
4. Notifications: Add a summary at the start of the app showing: "You have X overdue tasks."

## Response snapshot

Implementation plan created successfully for Due Dates & Recurrence feature.

**Constitution Check**: All 6 gates passed (Logic-First, UX-Driven, Input Validation, Modular Code, Code Quality, Feature Completeness).

**Phase 0 (Research)**: No unknowns to resolve. Confirmed approach using Python datetime, RecurrenceType enum, RecurrenceManager pattern, and Rich styling.

**Phase 1 (Design & Contracts)**: Created complete artifacts:
- data-model.md: Task model extension with due_date and recurrence_type fields
- contracts/task-creation.md: Schema for task creation/update with date validation
- contracts/task-completion.md: Recurrence logic flow (Daily/Weekly generation)
- contracts/task-display.md: Visual contracts for status indicators and Rich table styling
- quickstart.md: Developer and user guide with examples

**Structure**: Single project maintained, new modules follow existing patterns (logic/recurrence.py, updated validation schemas, Rich table enhancements).

**Agent Context**: Updated CLAUDE.md with new technologies.

## Outcome

- ✅ Impact: Complete implementation plan for due dates and recurrence with all contracts and design artifacts
- 🧪 Tests: Constitution gates validated (6/6 PASS)
- 📁 Files: Created plan.md, research.md, data-model.md, 3 contract files, quickstart.md
- 🔁 Next prompts: Ready for /sp.tasks to generate implementation tasks
- 🧠 Reflection: Plan follows constitution principles, uses existing patterns (pydantic, Rich), and maintains modular architecture. No architectural violations.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution Check (6/6 PASS)
- Prompt variant: N/A
- Next experiment: N/A - plan is complete and ready for task generation
