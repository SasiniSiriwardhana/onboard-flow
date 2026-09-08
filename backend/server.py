from datetime import datetime
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.config import settings

# Initialize FastAPI Application
app = FastAPI(
    title=settings.APP_NAME,
    description="FastAPI Backend for Customer Onboarding & Implementation SaaS Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Schemas for Day 1 API structure
class ProjectCreate(BaseModel):
    title: str = Field(..., example="Enterprise ERP Cloud Migration")
    customer_name: str = Field(..., example="Acme Corporation")
    tier: str = Field("Enterprise", example="Enterprise")
    target_go_live: Optional[str] = Field(None, example="2026-10-15")
    description: Optional[str] = Field(None, example="Phased rollout of customer data pipeline")


class ProjectResponse(BaseModel):
    id: int
    title: str
    customer_name: str
    tier: str
    status: str
    progress: int
    target_go_live: Optional[str]
    created_at: str


# Sample Day 1 Mock In-Memory Store
_MOCK_PROJECTS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "title": "Global FinTech Onboarding",
        "customer_name": "Nexus Bank International",
        "tier": "Enterprise VIP",
        "status": "In Progress",
        "progress": 68,
        "target_go_live": "2026-10-01",
        "created_at": "2026-09-01T10:00:00",
    },
    {
        "id": 2,
        "title": "Healthcare EHR Cloud Integration",
        "customer_name": "MedLife Health Systems",
        "tier": "Enterprise",
        "status": "Data Migration",
        "progress": 42,
        "target_go_live": "2026-10-20",
        "created_at": "2026-09-03T14:30:00",
    },
    {
        "id": 3,
        "title": "Retail Omnichannel Implementation",
        "customer_name": "Nordic Retail Group",
        "tier": "Growth",
        "status": "Kickoff",
        "progress": 15,
        "target_go_live": "2026-11-15",
        "created_at": "2026-09-06T09:15:00",
    },
    {
        "id": 4,
        "title": "Logistics Freight Hub Rollout",
        "customer_name": "Pacific Freight Logistics",
        "tier": "Enterprise",
        "status": "Live / Completed",
        "progress": 100,
        "target_go_live": "2026-09-05",
        "created_at": "2026-08-15T11:00:00",
    },
]


@app.get("/", tags=["General"])
def root():
    """Root endpoint providing system status and documentation links."""
    return {
        "system": settings.APP_NAME,
        "version": "1.0.0",
        "status": "online",
        "documentation": "/docs",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/api/health", tags=["Health"])
def health_check():
    """System health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "timestamp": datetime.utcnow().isoformat(),
        "backend": {
            "host": settings.BACKEND_HOST,
            "port": settings.BACKEND_PORT,
        },
    }


@app.get("/api/v1/onboarding/stats", tags=["Onboarding"])
def get_onboarding_stats():
    """Returns aggregated high-level onboarding KPIs."""
    total = len(_MOCK_PROJECTS)
    completed = sum(1 for p in _MOCK_PROJECTS if p["progress"] == 100)
    in_progress = sum(1 for p in _MOCK_PROJECTS if 0 < p["progress"] < 100)
    kickoff = sum(1 for p in _MOCK_PROJECTS if p["progress"] <= 15)

    return {
        "total_projects": total,
        "active_onboardings": in_progress,
        "completed": completed,
        "kickoff_stage": kickoff,
        "average_progress": round(sum(p["progress"] for p in _MOCK_PROJECTS) / total if total else 0, 1),
    }


@app.get("/api/v1/onboarding/projects", response_model=List[ProjectResponse], tags=["Onboarding"])
def list_onboarding_projects():
    """List customer implementation and onboarding projects."""
    return _MOCK_PROJECTS


@app.post("/api/v1/onboarding/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED, tags=["Onboarding"])
def create_onboarding_project(payload: ProjectCreate):
    """Create a new customer onboarding project."""
    new_id = max((p["id"] for p in _MOCK_PROJECTS), default=0) + 1
    new_project = {
        "id": new_id,
        "title": payload.title,
        "customer_name": payload.customer_name,
        "tier": payload.tier,
        "status": "Kickoff",
        "progress": 5,
        "target_go_live": payload.target_go_live,
        "created_at": datetime.utcnow().isoformat(),
    }
    _MOCK_PROJECTS.append(new_project)
    return new_project


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.server:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG,
    )
