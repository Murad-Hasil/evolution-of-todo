# Quickstart Guide: Task Organization

**Feature**: 001-task-organization
**Date**: 2025-12-30

## Overview

This guide provides step-by-step instructions for using the new task organization features, including priorities, tags, search, filtering, and sorting.

## Prerequisites

- Python 3.13+ installed
- Application installed via UV: `uv pip install -e .`
- Or run directly: `python -m todo.main`

## Feature Overview

| Feature | Description | Use Case |
|----------|-------------|----------|
| **Priorities** | Assign High/Medium/Low to tasks | Focus on urgent work first |
| **Tags** | Add multiple labels to tasks | Organize by project, context, or category |
| **Search** | Find tasks by keyword | Quickly locate specific tasks |
| **Filter** | Show tasks matching criteria | Focus on subset of tasks |
| **Sort** | Reorder task list | Organize view for context |

## Getting Started

### Launch Application

```bash
python -m todo.main
```

Or if installed:

```bash
todo
```

### Initial Menu

```
┌───────────────────────────────────────┐
│ Evolution of Todo - Phase I        │
│ In-Memory CLI Edition               │
└───────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Commands                           │
├─────────────────────────────────────┤
│ add        Add a new task         │
│ list       View all tasks         │
│ update     Modify a task          │
│ complete   Mark task as complete  │
│ delete     Delete a task          │
│ exit       Quit application       │
└─────────────────────────────────────┘
```

## Using Priorities

### Create Task with Priority

1. Enter command: `add`
2. Enter task title when prompted
3. Enter description (optional)
4. Enter priority level: `High`, `Medium`, or `Low`

**Example**:
```
> add
Task Title: Complete project proposal
Description (optional): Due Friday
Priority (High/Medium/Low): High
Task 'Complete project proposal' added with ID 1
```

**Default**: If no priority is specified, defaults to `Medium`.

### Update Task Priority

1. Enter command: `update`
2. Enter Task ID
3. When prompted for new priority, enter new value

**Example**:
```
> update
Enter Task ID to update: 1
New Title (current: Complete project proposal): [Enter]
New Description (current: Due Friday): [Enter]
New Priority (current: High): Medium
Task 1 updated successfully.
```

### Priority Display

Priority is shown in the task list with color coding:

| Priority | Color | Display |
|----------|-------|----------|
| High | Red | [red]High[/red] |
| Medium | Yellow | [yellow]Medium[/yellow] |
| Low | Green | [green]Low[/green] |

## Using Tags

### Create Task with Tags

1. Enter command: `add`
2. Enter task title
3. Enter description
4. Enter priority
5. Enter tags as comma-separated values

**Example**:
```
> add
Task Title: Write unit tests
Description (optional): Cover edge cases
Priority (High/Medium/Low): Medium
Tags (comma-separated): work, testing, quality-assurance
Task 'Write unit tests' added with ID 2
```

### Update Task Tags

1. Enter command: `update`
2. Enter Task ID
3. Enter new tags (replaces existing tags)

**Example**:
```
> update
Enter Task ID to update: 2
New Title (current: Write unit tests): [Enter]
New Tags (current: work, testing, quality-assurance): work, testing, bugfix
Task 2 updated successfully.
```

**Note**: Tags are case-sensitive. "Work" and "work" are different tags.

## Using Search

### Search Tasks

1. Enter command: `list` (or use search submenu if implemented)
2. Enter search keyword when prompted

**Example**:
```
> list
Search keyword (optional, press Enter to skip): urgent

┌─────────────────────────────────────────────────────────────┐
│ Task List                                              │
├─────┬──────────────────┬────────────┬────────┬──────┬─────────────┐
│ ID  │ Title             │ Description│Priority│ Tags │ Status      │
├─────┼──────────────────┼────────────┼────────┼──────┼─────────────┤
│   1 │ Urgent bug fix   │ Critical   │ High   │ bug  │ Pending     │
│   5 │ Review urgent PR  │ Security   │ High   │ review│ Pending     │
└─────┴──────────────────┴────────────┴────────┴──────┴─────────────┘
```

**Search Behavior**:
- Case-insensitive: "URGENT", "urgent", "Urgent" all match
- Partial matching: "urg" matches "urgent"
- Searches both title and description
- Empty search returns all tasks

## Using Filters

### Filter Tasks

1. Enter command: `list`
2. Enter filter criteria when prompted

**Example**:
```
> list
Search keyword (optional, press Enter to skip): [Enter]
Filter by status (Pending/Completed/any): Pending
Filter by priority (High/Medium/Low/any): High
Filter by tag (any tag name): bug

┌─────────────────────────────────────────────────────────────┐
│ Task List                                              │
├─────┬──────────────────┬────────────┬────────┬──────┬─────────────┐
│ ID  │ Title             │ Description│Priority│ Tags │ Status      │
├─────┼──────────────────┼────────────┼────────┼──────┼─────────────┤
│   1 │ Urgent bug fix   │ Critical   │ High   │ bug  │ Pending     │
└─────┴──────────────────┴────────────┴────────┴──────┴─────────────┘
```

**Filter Behavior**:
- Filters use AND logic (all criteria must match)
- Press Enter to skip a filter
- "any" option disables that filter
- Case-sensitive for tag filter

### Common Filter Patterns

| Goal | Filter Settings |
|------|----------------|
| Show only incomplete tasks | status=Pending, others=any |
| Show only high priority tasks | priority=High, others=any |
| Show work-related tasks | tag="work", others=any |
| Show urgent work tasks | status=Pending + priority=High + tag="work" |

## Using Sort

### Sort Tasks

1. Enter command: `list`
2. Choose sort option when prompted

**Example**:
```
> list
Search keyword (optional, press Enter to skip): [Enter]
Sort by (title/priority): priority

┌─────────────────────────────────────────────────────────────┐
│ Task List                                              │
├─────┬──────────────────┬────────────┬────────┬──────┬─────────────┐
│ ID  │ Title             │ Description│Priority│ Tags │ Status      │
├─────┼──────────────────┼────────────┼────────┼──────┼─────────────┤
│   3 │ Critical incident │ Security   │ High   │ ops  │ Completed   │
│   1 │ Urgent bug fix   │ Critical   │ High   │ bug  │ Pending     │
│   2 │ Weekly report    │ Monthly    │ Medium │ work │ Completed   │
└─────┴──────────────────┴────────────┴────────┴──────┴─────────────┘
```

**Sort Order**:
- **By Title**: Alphabetical (A-Z), case-insensitive
- **By Priority**: High → Medium → Low
- **Tie-breaking**: Tasks with same value sorted by ID (insertion order)

## Advanced Combinations

### Search + Filter + Sort

You can combine all features:

```
> list
Search keyword (optional, press Enter to skip): project
Filter by status (Pending/Completed/any): Pending
Filter by priority (High/Medium/Low/any): any
Filter by tag (any tag name): work
Sort by (title/priority): title

Result: Pending tasks with "project" in title/description, tagged "work", sorted alphabetically
```

## Tips & Best Practices

### Priorities
- Default to `Medium` for most tasks
- Reserve `High` for truly urgent items that need attention today
- Use `Low` for aspirational or backlog items

### Tags
- Use consistent naming (e.g., "work" not "Work" if case-sensitive)
- Keep tags short (1-2 words) for readability
- Limit to 3-5 tags per task for clarity
- Use categories: project, context, urgency, type

### Search
- Use partial words when you don't remember full term
- Empty search (press Enter) shows all tasks
- Search is great for finding tasks by description text

### Filtering
- Start with status filter to reduce list size
- Add priority/tag filters to narrow further
- Use filters with sort for organized views

### Sorting
- Sort by priority for "what to focus on today" view
- Sort by title for "scanning all tasks" view
- Remember filters apply before sorting

## Common Workflows

### Daily Planning
1. Filter by `Pending` status
2. Sort by `priority`
3. Focus on High priority tasks

### Project Focus
1. Search by project name keyword
2. Filter by `Pending` status
3. Sort by `priority`

### Review Completed
1. Filter by `Completed` status
2. Sort by `title`
3. Review work done this week

### Cleanup
1. List all tasks
2. Sort by `title`
3. Delete outdated or completed tasks

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Can't find a task | Try shorter search term (partial matching) |
| Tag filter not working | Check case sensitivity ("Work" ≠ "work") |
| Too many tasks | Use filters to narrow down before sorting |
| Tasks not matching | Check for extra spaces in keywords |
| Priority color not showing | Ensure terminal supports colors |

## Next Steps

After mastering organization features:
- Use tags consistently to build personal taxonomy
- Create daily routines using priority filters
- Combine features for powerful task management workflows

For more details on features, see:
- [Data Model](./data-model.md) - Technical specifications
- [API Contracts](./contracts/api-contracts.md) - Interface documentation
- [Research](./research.md) - Design decisions and rationale
