import sys
from todo.controller import TodoController
from todo.ui import menu

def main():
    """Entry point for the application."""
    controller = TodoController()
    menu.display_welcome()

    while True:
        menu.display_menu()
        choice = menu.Prompt.ask(
            "Select a command",
            choices=["add", "list", "update", "complete", "delete", "exit"],
            show_choices=False
        ).lower()

        if choice == "add":
            controller.add_task()
        elif choice == "list":
            controller.list_tasks()
        elif choice == "update":
            controller.update_task()
        elif choice == "complete":
            controller.complete_task()
        elif choice == "delete":
            controller.delete_task()
        elif choice == "exit":
            menu.show_message("Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()
