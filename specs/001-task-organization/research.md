# Research: Task Organization - Priorities, Categories, and Search

**Feature**: 001-task-organization
**Date**: 2025-12-30

## Overview

This document captures research findings for implementing task organization features. No NEEDS CLARIFICATION items were identified during planning, as the technical approach is clear based on the existing codebase architecture and feature requirements.

## Research Findings

### 1. Priority Implementation

**Question**: How to implement priority levels in Python dataclass with Pydantic validation?

**Decision**: Use Python's `enum.Enum` for type safety, integrated with Pydantic's validator for schema validation.

**Rationale**:
- Python enums provide compile-time type safety and IDE autocomplete
- Pydantic can validate enum values and provide helpful error messages
- Enum values are serializable and work well with dataclasses
- Matches best practices for bounded value sets in Python

**Alternatives Considered**:
- String literals with validation: Less type-safe, easier to introduce typos
- Integer constants (1, 2, 3): Less self-documenting than named enums

**Implementation**:
```python
from enum import Enum

class Priority(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
```

### 2. Tags Storage

**Question**: How to store and manage multiple tags per task?

**Decision**: Use `List[str]` in dataclass with Pydantic validation for uniqueness and sanitization.

**Rationale**:
- Lists are native to Python and work well with dataclasses
- Pydantic can validate tag format (length, allowed characters)
- Duplicate tag prevention can be handled in validators
- No need for complex data structures given scope

**Alternatives Considered**:
- Set: Automatically prevents duplicates but loses order; JSON serialization more complex
- Comma-separated string: No native list operations, requires parsing

**Implementation**:
```python
tags: List[str] = Field(default_factory=list, max_items=20)
```

### 3. Search Algorithm

**Question**: How to implement keyword search with partial matching?

**Decision**: Case-insensitive substring search across title and description fields using Python's `in` operator.

**Rationale**:
- Simple, fast for in-memory storage (O(n) complexity is acceptable for <10k tasks)
- Case-insensitive search improves user experience
- Substring matching covers "partial word" requirement naturally
- No external dependencies needed

**Alternatives Considered**:
- Regular expressions: More powerful but adds complexity and potential security issues
- External search libraries (Whoosh, Elasticsearch): Overkill for in-memory CLI app

**Implementation**:
```python
def search_tasks(self, keyword: str) -> List[Task]:
    if not keyword:
        return self.get_all_tasks()
    kw_lower = keyword.lower()
    return [
        task for task in self._tasks.values()
        if kw_lower in task.title.lower() or kw_lower in task.description.lower()
    ]
```

### 4. Filtering Strategy

**Question**: How to implement multiple simultaneous filters?

**Decision**: Apply filters sequentially with AND logic, each reducing the candidate list.

**Rationale**:
- Simple to understand and maintain
- Performance is acceptable for in-memory storage
- Allows flexible combination of filter criteria
- Easy to test each filter independently

**Alternatives Considered**:
- Single complex SQL-like WHERE clause: More complex to implement and maintain
- Filter objects with operator overloading: Over-engineering for this use case

**Implementation**:
```python
def filter_tasks(self, status=None, priority=None, tag=None) -> List[Task]:
    tasks = self.get_all_tasks()
    if status:
        tasks = [t for t in tasks if t.status == status]
    if priority:
        tasks = [t for t in tasks if t.priority == priority]
    if tag:
        tasks = [t for t in tasks if tag in t.tags]
    return tasks
```

### 5. Sorting Implementation

**Question**: How to implement multi-field sorting with tie-breaking?

**Decision**: Use Python's `sorted()` with custom key function returning tuple of sort fields.

**Rationale**:
- Python's sort is stable and efficient (Timsort algorithm)
- Tuple keys enable natural multi-field sorting
- Existing task ID can serve as tie-breaker (implies insertion order)

**Alternatives Considered**:
- Multiple sort passes (sort by secondary, then primary): Less efficient
- Custom comparator classes: More verbose and less Pythonic

**Implementation**:
```python
def sort_tasks(self, sort_by="title") -> List[Task]:
    if sort_by == "priority":
        order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        return sorted(self._tasks.values(), key=lambda t: (order[t.priority], t.id))
    else:  # title (default)
        return sorted(self._tasks.values(), key=lambda t: (t.title.lower(), t.id))
```

### 6. CLI Display with Rich

**Question**: How to display priorities and tags in Rich table with color coding?

**Decision**: Map priority values to Rich color constants; join tags with comma separators in table cells.

**Rationale**:
- Rich's table formatting handles cell wrapping and alignment automatically
- Color coding provides immediate visual distinction (Red for High, Yellow for Medium, Green for Low)
- Simple string joining for tags is readable and sufficient

**Alternatives Considered**:
- Custom render functions: More complex, but allows richer tag formatting
- Tags as separate columns: Doesn't scale well with variable tag counts

**Implementation**:
```python
PRIORITY_COLORS = {
    Priority.HIGH: "red",
    Priority.MEDIUM: "yellow",
    Priority.LOW: "green"
}

priority_color = PRIORITY_COLORS.get(task.priority, "white")
tags_display = ", ".join(task.tags) if task.tags else ""
```

## Performance Considerations

Based on success criteria (SC-003: search under 1 second, SC-004: filter under 2 seconds for 100+ tasks):

| Operation | Complexity | Estimated Time (10k tasks) | Notes |
|-----------|-------------|----------------------------|-------|
| Search (keyword) | O(n) | <100ms | Linear scan of all tasks |
| Filter (status+priority+tag) | O(n) | <100ms | Sequential filter application |
| Sort (priority/title) | O(n log n) | <200ms | Timsort algorithm |

**Conclusion**: All operations will comfortably meet performance targets for the specified scale (up to 10,000 tasks).

## Dependencies

No new external dependencies are required. The feature uses:
- Python 3.13+ (standard library: `enum`, `typing`, `dataclasses`)
- pydantic (existing dependency: validation)
- rich (existing dependency: CLI display)
- pytest (existing dependency: testing)

## Migration Path to Phase II

The design supports seamless migration to FastAPI/SQLModel:

| Current (In-Memory) | Phase II (FastAPI/SQLModel) |
|---------------------|-------------------------------|
| `Priority` enum | Same enum, can be SQLAlchemy enum |
| `List[str]` tags | Same (SQLModel supports list types) |
| In-memory filter/sort | Database WHERE/ORDER BY clauses |
| Rich table display | Frontend table component |
| Pydantic schemas | Same schemas (request/response models) |

The modular separation of Logic, Validation, and UI ensures minimal refactoring when transitioning to web-based architecture.
