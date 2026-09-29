from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.task import Task
from backend.schemas.task import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

# In-memory fallback task store for offline / mock testing
_MOCK_TASKS = [
    {
        "id": 1,
        "project_id": 1,
        "title": "Configure SSO and SAML 2.0 Auth",
        "description": "Establish Okta SSO integration and configure RBAC roles.",
        "status": "Done",
        "priority": "High",
        "due_date": datetime(2026, 10, 5, 18, 0, 0),
        "created_at": datetime(2026, 9, 10, 9, 0, 0),
        "updated_at": datetime(2026, 9, 15, 11, 30, 0),
    },
    {
        "id": 2,
        "project_id": 1,
        "title": "Schema Migration & Database Seed",
        "description": "Migrate customer legacy customer records into Oracle DB schema.",
        "status": "In Progress",
        "priority": "Critical",
        "due_date": datetime(2026, 10, 12, 17, 0, 0),
        "created_at": datetime(2026, 9, 12, 10, 0, 0),
        "updated_at": datetime(2026, 9, 20, 14, 0, 0),
    },
    {
        "id": 3,
        "project_id": 1,
        "title": "Webhook & Event Subscriptions Setup",
        "description": "Configure real-time event notifications for onboarding milestones.",
        "status": "To Do",
        "priority": "Medium",
        "due_date": datetime(2026, 10, 20, 17, 0, 0),
        "created_at": datetime(2026, 9, 14, 11, 0, 0),
        "updated_at": datetime(2026, 9, 14, 11, 0, 0),
    },
    {
        "id": 4,
        "project_id": 2,
        "title": "HIPAA Compliance Review & Signoff",
        "description": "Verify encryption in transit and at rest with security compliance officers.",
        "status": "In Progress",
        "priority": "High",
        "due_date": datetime(2026, 10, 18, 12, 0, 0),
        "created_at": datetime(2026, 9, 15, 14, 0, 0),
        "updated_at": datetime(2026, 9, 22, 16, 0, 0),
    },
    {
        "id": 5,
        "project_id": 2,
        "title": "Production Cutover Strategy Plan",
        "description": "Finalize go-live cutover runbook and stakeholder notification matrix.",
        "status": "To Do",
        "priority": "Low",
        "due_date": datetime(2026, 11, 1, 9, 0, 0),
        "created_at": datetime(2026, 9, 18, 8, 30, 0),
        "updated_at": datetime(2026, 9, 18, 8, 30, 0),
    },
]


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task associated with a project or standalone."""
    try:
        new_task = Task(
            project_id=payload.project_id,
            title=payload.title,
            description=payload.description,
            status=payload.status or "To Do",
            priority=payload.priority or "Medium",
            due_date=payload.due_date,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    except Exception:
        db.rollback()
        # Fallback to mock store
        new_id = max((t["id"] for t in _MOCK_TASKS), default=0) + 1
        mock_task = {
            "id": new_id,
            "project_id": payload.project_id,
            "title": payload.title,
            "description": payload.description,
            "status": payload.status or "To Do",
            "priority": payload.priority or "Medium",
            "due_date": payload.due_date,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        _MOCK_TASKS.append(mock_task)
        return mock_task
