# Feature Specification: Due Dates & Recurrence

**Feature Branch**: `001-due-dates-recurrence`
**Created**: 2025-12-30
**Status**: Draft
**Input**: User description: "Feature: Phase I - Advanced Level (Due Dates & Recurrence)
Description: Add intelligent time-based tracking and recurring task logic to the existing in-memory Todo app.

Requirements:
1. Due Dates: Add an optional 'due_date' field to tasks (Format: YYYY-MM-DD HH:MM).
2. Time Reminders: Implement logic to flag tasks that are "Overdue" or "Due Soon" (within 24 hours).
3. Recurring Tasks: Add a 'recurrence' field (Options: None, Daily, Weekly).
   - Logic: When a 'Daily' task is marked complete, automatically create a new instance of it for the next day.
4. Overdue Indicators: Use 'ux-specialist' to highlight overdue tasks in Red Bold in the task list.

Constraints:
- Use Python's 'datetime' library for all calculations.
- Maintain in-memory storage.
- Ensure 'skill-validation-guardianship' validates date formats to prevent crashes."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add Due Date to Task (Priority: P1)

As a user managing tasks, I want to add an optional due date to any task so that I know when it needs to be completed.

**Why this priority**: This is the foundation for all time-based functionality and provides immediate value to users who need to track deadlines.

**Independent Test**: Can be fully tested by creating tasks with and without due dates, verifying that tasks are stored and displayed correctly with their due date information.

**Acceptance Scenarios**:

1. **Given** no tasks exist, **When** I create a new task without a due date, **Then** the task is created successfully with no due date displayed
2. **Given** a task exists without a due date, **When** I update the task with a valid due date (YYYY-MM-DD HH:MM), **Then** the due date is saved and displayed
3. **Given** I am creating a new task, **When** I provide a valid due date during task creation, **Then** the task is created with the due date displayed

---

### User Story 2 - Identify Overdue and Upcoming Tasks (Priority: P1)

As a user reviewing my task list, I want to see which tasks are overdue or due soon so I can prioritize my work effectively.

**Why this priority**: This provides immediate value by helping users identify critical tasks that need attention, improving time management and task completion rates.

**Independent Test**: Can be fully tested by creating tasks with various due dates (past, present, future, within 24 hours) and verifying the correct indicators appear.

**Acceptance Scenarios**:

1. **Given** a task with a due date in the past, **When** I view the task list, **Then** the task is marked as "Overdue" with red bold styling
2. **Given** a task due within the next 24 hours, **When** I view the task list, **Then** the task is marked as "Due Soon"
3. **Given** a task due more than 24 hours in the future, **When** I view the task list, **Then** no overdue or due soon indicators are displayed
4. **Given** a task without a due date, **When** I view the task list, **Then** no time-based indicators are displayed

---

### User Story 3 - Create Recurring Daily Tasks (Priority: P2)

As a user managing routine work, I want to mark a task as "Daily" recurring so that a new task for the next day is automatically created when I complete the current one.

**Why this priority**: This reduces repetitive data entry for daily recurring tasks, improving efficiency for users with daily routines.

**Independent Test**: Can be fully tested by creating a daily recurring task, completing it, and verifying a new task is created for the next day.

**Acceptance Scenarios**:

1. **Given** a task marked as "Daily" recurrence with a due date, **When** I mark the task as complete, **Then** a new task is created with the same description but due date moved forward by one day
2. **Given** a task marked as "Daily" recurrence without a due date, **When** I mark the task as complete, **Then** a new task is created with the same description but without a due date
3. **Given** a task marked as "None" recurrence, **When** I mark the task as complete, **Then** no new task is created

---

### User Story 4 - Create Recurring Weekly Tasks (Priority: P3)

As a user managing weekly commitments, I want to mark a task as "Weekly" recurring so that a new task for the next week is automatically created when I complete the current one.

**Why this priority**: Weekly recurrence provides value for tasks that repeat on a weekly cadence but is less critical than daily recurrence.

**Independent Test**: Can be fully tested by creating a weekly recurring task, completing it, and verifying a new task is created for the next week.

**Acceptance Scenarios**:

1. **Given** a task marked as "Weekly" recurrence with a due date, **When** I mark the task as complete, **Then** a new task is created with the same description but due date moved forward by 7 days
2. **Given** a task marked as "Weekly" recurrence without a due date, **When** I mark the task as complete, **Then** a new task is created with the same description but without a due date

---

### Edge Cases

- What happens when a user provides an invalid date format for the due date field?
- What happens when a task is marked complete that was already overdue, and recurrence is enabled?
- How does the system handle timezone considerations for due dates and time calculations?
- What happens when a recurring task is deleted instead of completed?
- What happens when the user attempts to set a due date in the distant past?
- How does the system handle tasks with recurrence but no due date when calculating the next due date?
- What happens when multiple tasks are marked complete in quick succession with recurrence enabled?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to add an optional due date field to any task using the format YYYY-MM-DD HH:MM
- **FR-002**: System MUST validate that all due dates follow the YYYY-MM-DD HH:MM format before accepting them
- **FR-003**: System MUST identify tasks as "Overdue" when the current time is past the task's due date
- **FR-004**: System MUST identify tasks as "Due Soon" when the due date is within 24 hours of the current time but not yet overdue
- **FR-005**: System MUST display overdue tasks with red bold styling in the task list
- **FR-006**: System MUST allow users to set a recurrence field for each task with options: None, Daily, or Weekly
- **FR-007**: System MUST automatically create a new task when a "Daily" recurring task is marked complete, incrementing the due date by one day if a due date exists
- **FR-008**: System MUST automatically create a new task when a "Weekly" recurring task is marked complete, incrementing the due date by 7 days if a due date exists
- **FR-009**: System MUST NOT create a new task when a task marked with "None" recurrence is completed
- **FR-010**: System MUST preserve the original task description and recurrence setting when creating the next instance of a recurring task
- **FR-011**: System MUST display user-friendly error messages when invalid date formats are provided
- **FR-012**: System MUST handle tasks without due dates correctly without displaying time-based indicators

### Key Entities

- **Task**: Represents a user's todo item, with attributes including title, description, completion status, optional due date (YYYY-MM-DD HH:MM format), and recurrence setting (None, Daily, or Weekly)
- **Task List**: The collection of all tasks managed by the user, displayed with appropriate time-based indicators (Overdue, Due Soon) based on due dates

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a valid due date to any task in less than 10 seconds
- **SC-002**: Tasks with due dates are correctly categorized as Overdue, Due Soon, or Normal 100% of the time
- **SC-003**: Overdue tasks are visually distinct (red bold styling) and immediately recognizable in the task list
- **SC-004**: Recurring daily and weekly tasks automatically create the next instance upon completion 100% of the time
- **SC-005**: Invalid date formats are rejected with clear error messages 100% of the time
- **SC-006**: Users report that time-based indicators help them prioritize tasks effectively (measured through feedback)

## Assumptions

- Users operate in a single timezone and do not require timezone conversion functionality
- The current time is determined from the system clock when calculating overdue and due soon status
- Recurring tasks create the next instance immediately upon completion, not at a scheduled time
- Tasks without due dates are valid and should not trigger any time-based indicators
- Date and time calculations use 24-hour format (HH:MM)
