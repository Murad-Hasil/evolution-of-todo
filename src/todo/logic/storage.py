from typing import Dict, List, Optional
from datetime import datetime
from todo.models.task import Task, Priority, RecurrenceType

class TaskStorage:
    """In-memory storage for tasks."""
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "", priority: Priority = Priority.MEDIUM,
                 tags: Optional[List[str]] = None, due_date: Optional[datetime] = None,
                 recurrence_type: RecurrenceType = RecurrenceType.NONE) -> Task:
        """Add a new task to storage."""
        task_id = self._next_id
        task = Task(id=task_id, title=title, description=description, priority=priority,
                    tags=tags or [], due_date=due_date, recurrence_type=recurrence_type)
        self._tasks[task_id] = task
        self._next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks in insertion order."""
        return list(self._tasks.values())

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its ID."""
        return self._tasks.get(task_id)

    def update_task(self, task_id: int, title: Optional[str] = None,
                   description: Optional[str] = None, status: Optional[str] = None,
                   priority: Optional[Priority] = None, tags: Optional[List[str]] = None,
                   due_date: Optional[datetime] = None,
                   recurrence_type: Optional[RecurrenceType] = None) -> Optional[Task]:
        """Update an existing task."""
        task = self._tasks.get(task_id)
        if not task:
            return None

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        if priority is not None:
            task.priority = priority
        if tags is not None:
            task.tags = tags
        if due_date is not None:
            task.due_date = due_date
        if recurrence_type is not None:
            task.recurrence_type = recurrence_type

        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search_tasks(self, keyword: str) -> List[Task]:
        """Search tasks by keyword in title or description."""
        if not keyword:
            return self.get_all_tasks()
        kw_lower = keyword.lower()
        return [
            task for task in self._tasks.values()
            if kw_lower in task.title.lower() or kw_lower in task.description.lower()
        ]

    def filter_tasks(self, status: Optional[str] = None, priority: Optional[Priority] = None, tag: Optional[str] = None) -> List[Task]:
        """Filter tasks by status, priority, and/or tag using AND logic."""
        tasks = self.get_all_tasks()
        if status:
            tasks = [t for t in tasks if t.status == status]
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
        if tag:
            tasks = [t for t in tasks if tag in t.tags]
        return tasks

    def sort_tasks(self, tasks: List[Task] = None, sort_by: str = "title") -> List[Task]:
        """Sort tasks by title or priority with ID tie-breaking."""
        if tasks is None:
            tasks = list(self._tasks.values())
        if sort_by == "priority":
            order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
            return sorted(tasks, key=lambda t: (order[t.priority], t.id))
        else:  # title (default)
            return sorted(tasks, key=lambda t: (t.title.lower(), t.id))
