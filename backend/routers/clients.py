import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from backend.database import get_db
from backend.models.client import Client
from backend.models.project import Project
from backend.schemas.client import (
    ClientCreate,
    ClientResponse,
    ClientUpdate,
)
from backend.schemas.project import ProjectResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/clients", tags=["Clients"])

# Default onboarding milestone tasks automatically provisioned for new clients
DEFAULT_ONBOARDING_TASKS: List[str] = [
    "Initial Kickoff & Requirements Gathering",
    "System Architecture & Security Configuration",
    "Data Migration & Schema Validation",
    "System Integration & API Webhook Setup",
    "User Acceptance Testing (UAT)",
    "Staff Training & Production Go-Live",
]


@router.post(
    "",
    response_model=ClientResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new client with automatic onboarding project",
    description="Registers client, verifies email uniqueness, and automatically initializes an onboarding project with default tasks.",
)
def register_client(payload: ClientCreate, db: Session = Depends(get_db)):
    """
    Register a new client in the onboarding system:
    1. Verifies that the client corporate email is not already registered.
    2. Inserts new Client record.
    3. Automatically creates an initial Onboarding Project with default implementation tasks.
    4. Persists the transaction and returns the client and project details.
    """
    clean_email = payload.email.lower().strip()

    # 1. Verify email uniqueness
    try:
        existing_client = db.query(Client).filter(Client.email == clean_email).first()
    except SQLAlchemyError as err:
        logger.error(f"Database error checking existing client: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error while checking existing client.",
        )

    if existing_client:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A client with email '{clean_email}' already exists.",
        )

    # 2. Instantiate Client entity
    new_client = Client(
        company_name=payload.company_name.strip(),
        contact_person=payload.contact_person.strip(),
        email=clean_email,
        phone=payload.phone.strip() if payload.phone else None,
        address=payload.address.strip() if payload.address else None,
        status=payload.status or "Active",
    )

    try:
        db.add(new_client)
        db.flush()  # Populates new_client.id for Oracle sequence

        # 3. Auto-generate Initial Onboarding Project with default tasks
        project_name = payload.initial_project_name or f"{payload.company_name.strip()} - Onboarding Implementation"
        tasks_summary = "\n".join([f"- {task}" for task in DEFAULT_ONBOARDING_TASKS])
        project_desc = (
            f"Auto-generated client onboarding project for {new_client.company_name}.\n"
            f"Included Default Milestones:\n{tasks_summary}"
        )

        auto_project = Project(
            client_id=new_client.id,
            name=project_name,
            description=project_desc,
            status="Kickoff",
            progress=5,
        )
        db.add(auto_project)

        db.commit()
        db.refresh(new_client)
    except SQLAlchemyError as err:
        db.rollback()
        logger.error(f"Database error during client registration commit: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register client and create onboarding project.",
        )

    # Attach default tasks to response projects
    response_projects = []
    for p in new_client.projects:
        proj_dict = {
            "id": p.id,
            "client_id": p.client_id,
            "name": p.name,
            "description": p.description,
            "status": p.status,
            "progress": p.progress,
            "created_at": p.created_at,
            "tasks": DEFAULT_ONBOARDING_TASKS,
        }
        response_projects.append(ProjectResponse(**proj_dict))

    return ClientResponse(
        id=new_client.id,
        company_name=new_client.company_name,
        contact_person=new_client.contact_person,
        email=new_client.email,
        phone=new_client.phone,
        address=new_client.address,
        status=new_client.status,
        created_at=new_client.created_at,
        projects=response_projects,
    )
