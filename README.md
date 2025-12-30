# Evolution of Todo

A CLI todo application built using Spec-Driven Development (SDD) with Claude Code and Spec-Kit Plus.

## Agentic Dev Stack & SDD

This project demonstrates **Spec-Driven Development (SDD)** - a methodology where AI agents work from explicit specifications rather than ad-hoc instructions.

### Technology Stack

- **Python 3.13+** with UV for package management
- **Pydantic** for data validation
- **Rich** for CLI beautification
- **In-memory storage** using Python dictionary
- **Pytest** for testing

### 5 Specialized Agents

This project uses Claude Code's multi-agent system:

| Agent | Role |
|-------|------|
| `architect-prime` | High-level design, roadmaps, SDD compliance |
| `logic-specialist` | Core business logic, data models, state transitions |
| `ux-specialist` | CLI interfaces, user experience, accessibility |
| `bot-intelligence` | AI integration, MCP server integration |
| `k8s-engineer` | Containerization, infrastructure, deployment |

### 5 Configured Skills

Specialized capabilities invoked via slash commands:

| Skill | Purpose |
|-------|---------|
| `/sp.specify` | Create feature specifications from natural language |
| `/sp.plan` | Generate architectural plans with ADRs |
| `/sp.tasks` | Convert plans to testable implementation tasks |
| `/sp.git.commit_pr` | Autonomous git workflow and PR creation |
| `/sp.clarify` | Identify underspecified areas in specs |

### Spec-Driven Development Workflow

1. **Specify** → Feature requirements captured in `specs/<feature>/spec.md`
2. **Plan** → Architectural decisions documented in `specs/<feature>/plan.md`
3. **Tasks** → Implementation tasks with acceptance criteria in `specs/<feature>/tasks.md`
4. **Implement** → Code generated following SDD artifacts
5. **Verify** → Tests validate against specifications

### Prompt History Records

Every development step is recorded in `history/prompts/` proving the SDD workflow:
- Constitution decisions
- Feature specifications
- Planning sessions
- Task breakdowns
- Implementation sessions
- Refactoring records

---

## Features

### Core Todo Essentials
- Create, list, update, delete tasks
- Priority levels (high, medium, low)
- Status tracking (pending, in-progress, completed)
- Task ID generation

### Task Organization
- Categorization by context/work/Personal
- Project tagging system
- Flexible filtering and sorting

### Due Dates & Recurrence
- Due dates for tasks
- Recurring task patterns (daily, weekly, monthly)
- Overdue detection and display

## Getting Started

```bash
# Install dependencies
uv sync

# Run the CLI
python main.py --help

# Add a task
python main.py add "Complete project" --priority high

# List tasks
python main.py list

# Mark task complete
python main.py complete 1
```

## Project Structure

```
├── .claude/
│   ├── agents/           # 5 specialized agent configurations
│   └── skills/           # 5 configured skills
├── .specify/
│   ├── memory/           # Project constitution
│   └── scripts/          # SDD tooling
├── history/
│   ├── prompts/          # PHR records for every session
│   └── adr/              # Architecture Decision Records
├── specs/                # Feature specifications
│   └── <feature>/
│       ├── spec.md       # Requirements
│       ├── plan.md       # Architecture
│       └── tasks.md      # Implementation tasks
├── src/                  # Source code
└── tests/                # Test suite
```
