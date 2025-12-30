from todo.logic.storage import TaskStorage
from todo.logic.recurrence import RecurrenceManager
from todo.ui import menu
from todo.validation.schemas import TaskCreateSchema, TaskUpdateSchema
from pydantic import ValidationError
from datetime import datetime

class TodoController:
    """Orchestrates communication between UI and Logic."""
    def __init__(self):
        self.storage = TaskStorage()
        self.recurrence_manager = RecurrenceManager()

    def add_task(self):
        """Flow for adding a task."""
        title = menu.Prompt.ask("Task Title")
        description = menu.Prompt.ask("Description (optional)", default="")
        priority = menu.get_priority_input()
        tags = menu.get_tags_input()
        due_date = menu.get_due_date_input()
        recurrence_type = menu.get_recurrence_type_input()

        try:
            # Validate input
            schema = TaskCreateSchema(
                title=title,
                description=description,
                priority=priority,
                tags=tags,
                due_date=due_date.strftime("%Y-%m-%d %H:%M") if due_date else None,
                recurrence_type=recurrence_type
            )
            # Persist - convert due_date string back to datetime if present
            task_due_date = datetime.strptime(schema.due_date, "%Y-%m-%d %H:%M") if schema.due_date else None
            task = self.storage.add_task(
                schema.title,
                schema.description,
                schema.priority,
                schema.tags,
                task_due_date,
                schema.recurrence_type
            )
            menu.show_message(f"Task '{task.title}' added with ID {task.id}")
        except ValidationError as e:
            menu.show_error(str(e))

    def list_tasks(self):
        """Flow for listing tasks with optional search, filter, and sort."""
        # Get search keyword
        keyword = menu.get_search_keyword()
        # Get filter criteria
        filters = menu.get_filter_criteria()
        # Get sort option
        sort_by = menu.get_sort_option()

        # Apply search, filters, and sort
        tasks = self.storage.get_all_tasks()

        if keyword:
            tasks = self.storage.search_tasks(keyword)
        if filters.get("status") or filters.get("priority") or filters.get("tag"):
            tasks = self.storage.filter_tasks(
                status=filters.get("status"),
                priority=filters.get("priority"),
                tag=filters.get("tag")
            )
        tasks = self.storage.sort_tasks(tasks, sort_by=sort_by)

        menu.render_task_table(tasks)

    def update_task(self):
        """Flow for updating a task."""
        task_id = menu.IntPrompt.ask("Enter Task ID to update")
        task = self.storage.get_task_by_id(task_id)

        if not task:
            menu.show_error(f"Task with ID {task_id} not found.")
            return

        new_title = menu.Prompt.ask(f"New Title (current: {task.title})", default=task.title)
        new_desc = menu.Prompt.ask(f"New Description (current: {task.description})", default=task.description)
        new_priority = menu.Prompt.ask(f"New Priority (current: {task.priority.value})", default=task.priority.value)
        new_tags_str = menu.Prompt.ask(f"New Tags (current: {', '.join(task.tags)})", default=', '.join(task.tags))
        new_tags = [tag.strip() for tag in new_tags_str.split(',') if tag.strip()]

        # Get optional due date and recurrence
        current_due = task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else ""
        new_due_date_str = menu.Prompt.ask(f"Due date (YYYY-MM-DD HH:MM, current: {current_due})", default=current_due)
        new_due_date = None
        if new_due_date_str.strip():
            try:
                new_due_date = datetime.strptime(new_due_date_str.strip(), "%Y-%m-%d %H:%M")
            except ValueError:
                menu.show_error("Invalid date format, keeping current due date.")
                new_due_date = task.due_date

        new_recurrence = menu.get_recurrence_type_input(task.recurrence_type.value)

        try:
            schema = TaskUpdateSchema(
                title=new_title,
                description=new_desc,
                priority=task.priority if new_priority == task.priority.value else None,
                tags=new_tags,
                due_date=new_due_date.strftime("%Y-%m-%d %H:%M") if new_due_date else None,
                recurrence_type=new_recurrence
            )
            # Only update fields that changed
            task_due_date = datetime.strptime(schema.due_date, "%Y-%m-%d %H:%M") if schema.due_date else None
            self.storage.update_task(
                task_id,
                title=schema.title,
                description=schema.description,
                priority=schema.priority,
                tags=schema.tags,
                due_date=task_due_date,
                recurrence_type=schema.recurrence_type
            )
            menu.show_message(f"Task {task_id} updated successfully.")
        except ValidationError as e:
            menu.show_error(str(e))

    def complete_task(self):
        """Flow for completing a task."""
        task_id = menu.IntPrompt.ask("Enter Task ID to complete")
        task = self.storage.get_task_by_id(task_id)

        if not task:
            menu.show_error(f"Task with ID {task_id} not found.")
            return

        # Check for recurrence before marking complete
        has_recurrence = task.recurrence_type.value != "None"

        if self.storage.update_task(task_id, status="Completed"):
            menu.show_message(f"Task {task_id} marked as Completed.")

            # Handle recurrence - create next instance
            if has_recurrence:
                new_task = self.recurrence_manager.handle_recurrence(task, self.storage)
                if new_task:
                    menu.show_message(f"[cyan]Recurring task created:[/cyan] '{new_task.title}' (ID: {new_task.id})")
        else:
            menu.show_error(f"Task with ID {task_id} not found.")

    def delete_task(self):
        """Flow for deleting a task."""
        task_id = menu.IntPrompt.ask("Enter Task ID to delete")
        if menu.Confirm.ask(f"Are you sure you want to delete task {task_id}?"):
            if self.storage.delete_task(task_id):
                menu.show_message(f"Task {task_id} deleted.")
            else:
                menu.show_error(f"Task with ID {task_id} not found.")
