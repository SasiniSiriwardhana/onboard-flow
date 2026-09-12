from datetime import datetime
from typing import Any, Dict, List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.config import settings
from backend.database import check_db_connection, get_db, Base, engine
from backend.schemas import ProjectCreate, ProjectResponse, DBHealthResponse
from backend.routers import auth_router, client_router
import backend.models  # Ensures all ORM models (User, Customer, OnboardingProject, Client, Project) are registered


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context for startup and shutdown events."""
    # Attempt to create tables if database is reachable
    try:
        if engine is not None:
            Base.metadata.create_all(bind=engine)
    except Exception:
        pass
    yield


# Initialize FastAPI Application
app = FastAPI(
    title=settings.APP_NAME,
    description="FastAPI Backend with Oracle DB for Customer Onboarding & Implementation SaaS Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(auth_router)
app.include_router(client_router)

# Sample In-Memory Fallback Projects
_PROJECTS_STORE: List[Dict[str, Any]] = [
    {
        "id": 1,
        "title": "Global FinTech Onboarding",
        "customer_name": "Nexus Bank International",
        "tier": "Enterprise VIP",
        "description": "Multi-region core banking integration and security sign-off.",
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
        "description": "HIPAA-compliant patient data migration and webhook setup.",
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
        "description": "POS synchronization and multi-warehouse inventory feed.",
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
        "description": "Real-time dispatch API and telemetry stream integration.",
        "status": "Completed",
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
    """System health check endpoint with database status summary."""
    db_status = check_db_connection()
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "timestamp": datetime.utcnow().isoformat(),
        "database": {
            "status": db_status.get("status"),
            "host": db_status.get("host"),
            "port": db_status.get("port"),
            "service_name": db_status.get("service_name"),
            "latency_ms": db_status.get("latency_ms"),
        },
    }


@app.get("/api/db/health", response_model=DBHealthResponse, tags=["Database"])
def database_health():
    """Diagnostic check for Oracle Database connectivity via SQLAlchemy."""
    return check_db_connection()


@app.get("/api/v1/onboarding/stats", tags=["Onboarding"])
def get_onboarding_stats():
    """Returns aggregated high-level onboarding KPIs."""
    total = len(_PROJECTS_STORE)
    completed = sum(1 for p in _PROJECTS_STORE if p["progress"] == 100)
    in_progress = sum(1 for p in _PROJECTS_STORE if 0 < p["progress"] < 100)
    kickoff = sum(1 for p in _PROJECTS_STORE if p["progress"] <= 15)

    return {
        "total_projects": total,
        "active_onboardings": in_progress,
        "completed": completed,
        "kickoff_stage": kickoff,
        "average_progress": round(sum(p["progress"] for p in _PROJECTS_STORE) / total if total else 0, 1),
    }


@app.get("/api/v1/onboarding/projects", response_model=List[ProjectResponse], tags=["Onboarding"])
def list_onboarding_projects():
    """List customer implementation and onboarding projects."""
    return _PROJECTS_STORE


@app.post(
    "/api/v1/onboarding/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Onboarding"],
)
def create_onboarding_project(payload: ProjectCreate):
    """Create a new customer onboarding project."""
    new_id = max((p["id"] for p in _PROJECTS_STORE), default=0) + 1
    new_project = {
        "id": new_id,
        "title": payload.title,
        "customer_name": payload.customer_name or "New Client",
        "tier": payload.tier or "Enterprise",
        "description": payload.description or "",
        "status": payload.status or "Kickoff",
        "progress": payload.progress or 5,
        "target_go_live": payload.target_go_live,
        "created_at": datetime.utcnow().isoformat(),
    }
    _PROJECTS_STORE.append(new_project)
    return new_project


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.server:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG,
    )
