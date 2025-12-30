from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from typing import List, Optional
from todo.models.task import Task, Priority, RecurrenceType
from datetime import datetime
from todo.logic.recurrence import RecurrenceManager, TaskStatus

console = Console()
recurrence_manager = RecurrenceManager()

PRIORITY_COLORS = {
    Priority.HIGH: "red",
    Priority.MEDIUM: "yellow",
    Priority.LOW: "green"
}

def get_due_date_input() -> Optional[datetime]:
    """Collect due date input from user (YYYY-MM-DD HH:MM format)."""
    due_date_str = Prompt.ask("Due date (YYYY-MM-DD HH:MM, or Enter to skip)", default="")
    if not due_date_str.strip():
        return None
    try:
        return datetime.strptime(due_date_str.strip(), "%Y-%m-%d %H:%M")
    except ValueError:
        show_error("Invalid date format. Use YYYY-MM-DD HH:MM")
        return None

def get_recurrence_type_input(default: str = "None") -> RecurrenceType:
    """Collect recurrence type input from user."""
    recurrence = Prompt.ask(f"Recurrence (None/Daily/Weekly)", default=default)
    recurrence_map = {
        "none": RecurrenceType.NONE,
        "daily": RecurrenceType.DAILY,
        "weekly": RecurrenceType.WEEKLY
    }
    return recurrence_map.get(recurrence.lower(), RecurrenceType.NONE)

def display_welcome():
    """Display welcome message."""
    console.print(Panel("[bold blue]Evolution of Todo - Phase I[/bold blue]",
                        subtitle="[italic]In-Memory CLI Edition[/italic]"))

def display_menu():
    """Display available commands."""
    table = Table(show_header=False, box=None)
    table.add_row("[bold cyan]add[/bold cyan]", "Add a new task")
    table.add_row("[bold cyan]list[/bold cyan]", "View all tasks")
    table.add_row("[bold cyan]update[/bold cyan]", "Modify a task")
    table.add_row("[bold cyan]complete[/bold cyan]", "Mark task as complete")
    table.add_row("[bold cyan]delete[/bold cyan]", "Delete a task")
    table.add_row("[bold cyan]exit[/bold cyan]", "Quit application")

    console.print(Panel(table, title="Commands", border_style="dim"))

def render_task_table(tasks: List[Task]):
    """Render tasks in a Rich table."""
    if not tasks:
        console.print("[yellow]No tasks found.[/yellow]")
        return

    # Count overdue tasks for startup summary
    overdue_count = sum(1 for t in tasks if t.status == "Pending" and
                        t.due_date is not None and t.due_date < datetime.now())

    if overdue_count > 0:
        console.print(f"[bold red]You have {overdue_count} overdue task(s).[/bold red]")

    table = Table(title="Task List", header_style="bold magenta")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Priority", justify="center")
    table.add_column("Due Date", justify="center")
    table.add_column("Status", justify="center")
    table.add_column("Recurrence", justify="center")

    for task in tasks:
        status_style = "green" if task.status == "Completed" else "yellow"
        priority_color = PRIORITY_COLORS.get(task.priority, "white")

        # Format due date
        if task.due_date:
            due_display = task.due_date.strftime("%b %d, %H:%M")
        else:
            due_display = "-"

        # Determine deadline status and styling
        due_status = recurrence_manager.check_due_status(task)
        if task.due_date is None:
            deadline_style = "dim"
            deadline_display = "No Deadline"
        elif due_status == TaskStatus.OVERDUE:
            deadline_style = "bold red"
            deadline_display = "[OVERDUE]"
        elif due_status == TaskStatus.DUE_SOON:
            deadline_style = "yellow"
            deadline_display = "[DUE SOON]"
        else:
            deadline_style = "green"
            deadline_display = "On Track"

        # Recurrence display
        recurrence_display = task.recurrence_type.value if task.recurrence_type != RecurrenceType.NONE else "-"

        table.add_row(
            str(task.id),
            task.title,
            f"[{priority_color}]{task.priority.value}[/{priority_color}]",
            f"[{deadline_style}]{due_display}[/{deadline_style}]",
            f"[{status_style}]{task.status}[/{status_style}]",
            f"[cyan]{recurrence_display}[/cyan]" if task.recurrence_type != RecurrenceType.NONE else "-"
        )

    console.print(table)

def get_search_keyword() -> Optional[str]:
    """Collect search keyword from user."""
    keyword = Prompt.ask("Search keyword (press Enter to skip)", default="")
    return keyword or None

def get_filter_criteria() -> dict:
    """Collect filter criteria from user."""
    filters = {}

    status = Prompt.ask("Filter by status (Pending/Completed/any)", default="any")
    if status.lower() not in ("any", ""):
        filters["status"] = "Pending" if status.lower() == "pending" else "Completed"

    priority = Prompt.ask("Filter by priority (High/Medium/Low/any)", default="any")
    if priority.lower() not in ("any", ""):
        priority_map = {"high": Priority.HIGH, "medium": Priority.MEDIUM, "low": Priority.LOW}
        filters["priority"] = priority_map.get(priority.lower())

    tag = Prompt.ask("Filter by tag (any tag name)", default="")
    if tag:
        filters["tag"] = tag

    return filters

def get_sort_option() -> str:
    """Collect sort option from user."""
    sort_by = Prompt.ask("Sort by (title/priority)", default="title")
    if sort_by.lower() not in ("title", "priority"):
        return "title"
    return sort_by.lower()

def get_priority_input(default: str = "Medium") -> Priority:
    """Collect priority input from user."""
    priority = Prompt.ask(f"Priority (High/Medium/Low)", default=default)
    priority_map = {"high": Priority.HIGH, "medium": Priority.MEDIUM, "low": Priority.LOW}
    return priority_map.get(priority.lower(), Priority.MEDIUM)

def get_tags_input() -> List[str]:
    """Collect tags input from user (comma-separated)."""
    tags_str = Prompt.ask("Tags (comma-separated)", default="")
    if not tags_str:
        return []
    tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]
    return tags

def show_message(message: str, style: str = "green"):
    """Display a styled message."""
    console.print(f"[{style}]{message}[/{style}]")

def show_error(message: str):
    """Display an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")
