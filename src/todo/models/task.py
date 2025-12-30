from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List

class Priority(str, Enum):
    """Task priority levels."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class RecurrenceType(str, Enum):
    """Task recurrence options."""
    NONE = "None"
    DAILY = "Daily"
    WEEKLY = "Weekly"

@dataclass
class Task:
    """Represents a single todo item."""
    id: int
    title: str
    description: str = ""
    status: str = "Pending"
    priority: Priority = Priority.MEDIUM
    tags: List[str] = field(default_factory=list)
    due_date: Optional[datetime] = None
    recurrence_type: RecurrenceType = RecurrenceType.NONE
