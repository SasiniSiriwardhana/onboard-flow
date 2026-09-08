from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr


class CustomerBase(BaseModel):
    name: str = Field(..., example="Jane Doe")
    company: str = Field(..., example="Acme Corp")
    email: str = Field(..., example="jane.doe@acme.com")
    tier: str = Field("Enterprise", example="Enterprise")


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    title: str = Field(..., example="Global ERP Migration")
    customer_name: Optional[str] = Field("Acme Corp", example="Acme Corp")
    tier: Optional[str] = Field("Enterprise", example="Enterprise")
    description: Optional[str] = Field(None, example="End-to-end customer system migration")
    status: Optional[str] = Field("Kickoff", example="Kickoff")
    progress: Optional[int] = Field(0, ge=0, le=100, example=25)
    target_go_live: Optional[str] = Field(None, example="2026-10-30")


class ProjectCreate(ProjectBase):
    customer_id: Optional[int] = None


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    progress: Optional[int] = Field(None, ge=0, le=100)
    target_go_live: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: int
    created_at: str

    class Config:
        from_attributes = True


class DBHealthResponse(BaseModel):
    status: str
    driver: Optional[str] = None
    host: str
    port: int
    service_name: str
    user: Optional[str] = None
    latency_ms: Optional[float] = None
    error: Optional[str] = None
    hint: Optional[str] = None
