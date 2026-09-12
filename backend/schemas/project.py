from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class ProjectBase(BaseModel):
    """Base schema containing core project attributes."""
    name: str = Field(..., min_length=2, max_length=200, description="Name of the onboarding project")
    description: Optional[str] = Field(None, description="Detailed project description or scope")
    status: Optional[str] = Field("Pending", description="Current project status (e.g., Pending, In Progress, Completed)")
    progress: Optional[int] = Field(0, ge=0, le=100, description="Project progress percentage (0-100)")


class ProjectCreate(ProjectBase):
    """Schema for creating an onboarding project."""
    client_id: int = Field(..., description="ID of the client this project belongs to")
    tasks: Optional[List[str]] = Field(default=None, description="List of onboarding tasks or milestones")


class ProjectUpdate(BaseModel):
    """Schema for updating an existing project."""
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = None
    progress: Optional[int] = Field(None, ge=0, le=100)


class ProjectResponse(ProjectBase):
    """Public schema for returning project details."""
    id: int
    client_id: int
    created_at: datetime
    tasks: Optional[List[str]] = Field(default=None, description="Associated onboarding tasks")

    model_config = ConfigDict(from_attributes=True)
