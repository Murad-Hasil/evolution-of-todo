# Quickstart: Phase I - Core Todo Essentials

## Developer Setup

### Prerequisites
- [UV](https://github.com/astral-sh/uv) installed
- Python 3.13+

### Installation
```bash
uv sync
```

### Running the App
```bash
uv run python src/todo/main.py
```

### Running Tests
```bash
uv run pytest
```

## User Guide

1. **Launch**: Run the app using `uv run`.
2. **Commands**:
   - `add`: Add a new task (Title required, Description optional).
   - `list`: Show all tasks in a table.
   - `update`: Modify an existing task by ID.
   - `complete`: Mark a task as completed.
   - `delete`: Remove a task by ID.
   - `help`: Show command list.
   - `exit`: Close the application.
3. **Storage**: Note that all data is in-memory and will be lost when the application closes.
