# Service Contracts: Phase I - Core Todo Essentials

## Storage Interface (`storage.py`)

Responsible for in-memory persistence.

### `add_task(data: TaskCreate) -> Task`
- **Input**: `title`, `description` (optional)
- **Output**: Full `Task` object with generated `id`
- **Errors**: `StorageError` if memory limit exceeded (theoretical)

### `get_tasks() -> List[Task]`
- **Output**: List of all `Task` objects
- **Notes**: Maintains insertion order

### `update_task(id: int, data: TaskUpdate) -> Task`
- **Input**: `task_id`, optional `title`, `description`, `status`
- **Output**: Updated `Task` object
- **Errors**: `TaskNotFoundError` if ID doesn't exist

### `delete_task(id: int) -> bool`
- **Input**: `task_id`
- **Output**: `True` if deleted
- **Errors**: `TaskNotFoundError` if ID doesn't exist

## Validation Guard Interface (`schemas.py`)

Handles internal validation logic.

### `validate_create_task(data: dict) -> TaskCreate`
- **Uses**: Pydantic for schema checks
- **Raises**: `ValidationError` with human-readable fields

### `validate_id(task_id: int) -> int`
- **Constraint**: Must be positive integer
- **Raises**: `InvalidIDError`
