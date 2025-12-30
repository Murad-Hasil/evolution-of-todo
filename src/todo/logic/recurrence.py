from datetime import datetime, timedelta
from typing import Optional
from enum import Enum
from todo.models.task import Task, RecurrenceType


class TaskStatus(Enum):
    """Computed task status based on due date."""
    OVERDUE = "Overdue"           # due_date < now
    DUE_SOON = "Due Soon"         # due_date within 24h, not overdue
    ON_TRACK = "On Track"         # due_date > 24h from now
    NO_DEADLINE = "No Deadline"   # due_date is None


class RecurrenceManager:
    """Manages recurring task generation and due status checking."""

    def check_due_status(self, task: Task) -> TaskStatus:
        """
        Determine the status of a task based on its due date.

        Args:
            task: The task to check

        Returns:
            TaskStatus enum value
        """
        if task.due_date is None:
            return TaskStatus.NO_DEADLINE

        now = datetime.now()

        # Compare due date with current time
        if task.due_date < now:
            return TaskStatus.OVERDUE
        elif task.due_date <= now + timedelta(hours=24):
            return TaskStatus.DUE_SOON
        else:
            return TaskStatus.ON_TRACK

    def handle_recurrence(self, completed_task: Task, storage) -> Optional[Task]:
        """
        Generate the next recurring task upon completion.

        Args:
            completed_task: The task that was just completed
            storage: TaskStorage instance to add the new task

        Returns:
            The newly created recurring task, or None if no recurrence

        Note:
            This is only triggered upon task completion to prevent infinite loops.
        """
        # Only generate new task if recurrence is set
        if completed_task.recurrence_type == RecurrenceType.NONE:
            return None

        # Calculate new due date based on recurrence type
        new_due_date = None
        if completed_task.due_date is not None:
            if completed_task.recurrence_type == RecurrenceType.DAILY:
                new_due_date = completed_task.due_date + timedelta(days=1)
            elif completed_task.recurrence_type == RecurrenceType.WEEKLY:
                new_due_date = completed_task.due_date + timedelta(weeks=1)

        # Create new task with same attributes except ID and due date
        new_task = Task(
            id=storage._next_id,  # Will be incremented by storage
            title=completed_task.title,
            description=completed_task.description,
            status="Pending",
            priority=completed_task.priority,
            tags=completed_task.tags.copy(),
            due_date=new_due_date,
            recurrence_type=completed_task.recurrence_type
        )

        # Add to storage
        storage._tasks[new_task.id] = new_task
        storage._next_id += 1

        return new_task
