---
name: skill-validation-guardianship
description: Global validation logic for inputs and data models.
---
# Validation Guardianship
## Instructions
- Use Pydantic for all data validation.
- Implement custom error handlers to catch 'Task Not Found' or 'Invalid Date'.
- Sanitize all string inputs to prevent injection.
## Examples
User: "Add a task with no title."
Output: Return a clear validation error: "Title cannot be empty."
