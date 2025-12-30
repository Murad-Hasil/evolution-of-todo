# Implementation Research: Phase I - Core Todo Essentials

## Decision: Modular Directory Structure
**Rationale**: Enables clear separation between business logic and UI presentation, facilitating testing and future migration to FastAPI.
**Alternatives considered**: Flat structure (too messy), Framework-specific (overkill for Phase I).

## Decision: Dictionary-based In-Memory Storage
**Rationale**: O(1) lookup by ID and built-in insertion order maintenance (Python 3.7+). Using `dataclass` for Task models ensures type safety and minimal overhead.
**Alternatives considered**: List of objects (O(n) lookup), SQLite (too complex for Phase I requirements).

## Decision: Pydantic + Rich Prompt Validation
**Rationale**: Rich provides immediate UX-level validation; Pydantic ensures schema integrity; custom guards handle domain-specific rules (e.g., ID exists).
**Alternatives considered**: Custom regex (hard to maintain), Manual `if/else` checks (verbose).

## Decision: Centralized Controller Pattern
**Rationale**: Acts as the orchestrator between the CLI REPL loop and the logic layer, following the Constitution's "Logic-First" principle.
**Alternatives considered**: Direct logic calls from UI (tight coupling).

## Decision: REPL-like Main Loop
**Rationale**: Provides a continuous interactive experience using Rich's `Prompt` with choice validation.
**Alternatives considered**: Single-execution commands (poor UX for a "Todo" flow).
