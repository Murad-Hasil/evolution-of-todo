---
name: skill-agentic-intent-parsing
description: Parses natural language strings into structured Todo commands.
---
# Agentic Intent Parsing
## Instructions
- Use LLM capabilities to extract 'Task Name', 'Due Date', and 'Priority' from raw text.
- Map phrases like "do it tomorrow" to actual ISO dates.
- Integrate with OpenAI Agents SDK.
## Examples
User: "Remind me to buy milk tomorrow at 5pm."
Output: { "action": "add", "task": "buy milk", "due": "2025-12-31T17:00:00" }
