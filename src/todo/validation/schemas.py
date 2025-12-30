from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List
from todo.models.task import Priority, RecurrenceType

class TaskCreateSchema(BaseModel):
    """Schema for validating task creation."""
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default="", max_length=500)
    priority: Priority = Field(default=Priority.MEDIUM)
    tags: List[str] = Field(default_factory=list, max_length=20)
    due_date: Optional[str] = Field(default=None)
    recurrence_type: RecurrenceType = Field(default=RecurrenceType.NONE)

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @field_validator("tags")
    @classmethod
    def tags_unique(cls, v: List[str]) -> List[str]:
        seen = set()
        unique_tags = []
        for tag in v:
            tag = tag.strip()
            if not tag:
                continue
            if len(tag) > 30:
                raise ValueError(f"Tag '{tag}' exceeds 30 characters")
            if tag not in seen:
                seen.add(tag)
                unique_tags.append(tag)
        return unique_tags

    @field_validator("due_date", mode="before")
    @classmethod
    def validate_due_date(cls, v: Optional[str]) -> Optional[str]:
        """Validate due date format as YYYY-MM-DD HH:MM."""
        if v is None:
            return None
        if not v.strip():
            return None
        try:
            datetime.strptime(v.strip(), "%Y-%m-%d %H:%M")
            return v.strip()
        except ValueError:
            raise ValueError("Invalid due_date format. Use YYYY-MM-DD HH:MM")

class TaskUpdateSchema(BaseModel):
    """Schema for validating task updates."""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[str] = Field(None)
    priority: Optional[Priority] = Field(None)
    tags: Optional[List[str]] = Field(None, max_length=20)
    due_date: Optional[str] = Field(None)
    recurrence_type: Optional[RecurrenceType] = Field(None)

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ["Pending", "Completed"]:
            raise ValueError("Status must be 'Pending' or 'Completed'")
        return v

    @field_validator("tags")
    @classmethod
    def tags_unique(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        if v is None:
            return None
        seen = set()
        unique_tags = []
        for tag in v:
            tag = tag.strip()
            if not tag:
                continue
            if len(tag) > 30:
                raise ValueError(f"Tag '{tag}' exceeds 30 characters")
            if tag not in seen:
                seen.add(tag)
                unique_tags.append(tag)
        return unique_tags

    @field_validator("due_date", mode="before")
    @classmethod
    def validate_due_date_update(cls, v: Optional[str]) -> Optional[str]:
        """Validate due date format as YYYY-MM-DD HH:MM."""
        if v is None or not v.strip():
            return None
        try:
            datetime.strptime(v.strip(), "%Y-%m-%d %H:%M")
            return v.strip()
        except ValueError:
            raise ValueError("Invalid due_date format. Use YYYY-MM-DD HH:MM")
