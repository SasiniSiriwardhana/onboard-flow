from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserBase(BaseModel):
    """Base fields shared across user schemas."""
    name: str = Field(..., min_length=2, max_length=120, description="Full name of the user")
    email: EmailStr = Field(..., description="Unique email address")


class UserCreate(UserBase):
    """Schema for registering a new user."""
    password: str = Field(
        ...,
        min_length=6,
        max_length=128,
        description="Password for the user account (minimum 6 characters)",
    )


class UserLogin(BaseModel):
    """Schema for authenticating an existing user."""
    email: EmailStr = Field(..., description="Registered email address")
    password: str = Field(..., description="Account password")


class UserResponse(UserBase):
    """Public user schema returned in API responses (excludes sensitive hash)."""
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
