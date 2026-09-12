from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict

from backend.schemas.project import ProjectResponse


class ClientBase(BaseModel):
    """Base schema containing core Client attributes."""
    company_name: str = Field(..., min_length=2, max_length=150, description="Company or organization name")
    contact_person: str = Field(..., min_length=2, max_length=120, description="Primary contact full name")
    email: EmailStr = Field(..., description="Corporate contact email address")
    phone: Optional[str] = Field(None, max_length=50, description="Contact telephone number")
    address: Optional[str] = Field(None, max_length=255, description="Physical office or billing address")


class ClientCreate(ClientBase):
    """Schema for registering a new client."""
    status: Optional[str] = Field("Active", description="Initial client status")
    initial_project_name: Optional[str] = Field(
        None,
        description="Optional custom project name; defaults to '<Company Name> - Onboarding Implementation'",
    )


class ClientUpdate(BaseModel):
    """Schema for updating an existing client."""
    company_name: Optional[str] = Field(None, min_length=2, max_length=150)
    contact_person: Optional[str] = Field(None, min_length=2, max_length=120)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = Field(None, max_length=255)
    status: Optional[str] = None


class ClientResponse(ClientBase):
    """Public schema for returning client details."""
    id: int
    status: str
    created_at: datetime
    projects: List[ProjectResponse] = Field(default_factory=list, description="Associated onboarding projects")

    model_config = ConfigDict(from_attributes=True)
