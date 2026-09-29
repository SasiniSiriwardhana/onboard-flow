from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=2000, description="Task detailed description")
    status: str = Field(default="To Do", description="Task status: To Do, In Progress, Done")
    priority: str = Field(default="Medium", description="Task priority: Low, Medium, High, Critical")
    due_date: Optional[datetime] = Field(None, description="Due date and time")
    project_id: Optional[int] = Field(None, description="Associated project ID")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[str] = Field(None, description="Status: To Do, In Progress, Done")
    priority: Optional[str] = Field(None, description="Priority: Low, Medium, High, Critical")
    due_date: Optional[datetime] = None
    project_id: Optional[int] = None


class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
