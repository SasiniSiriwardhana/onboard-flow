import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
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


def _format_client_response(client: Client) -> ClientResponse:
    """Helper to convert a Client ORM instance to a ClientResponse schema with tasks."""
    response_projects = []
    for p in (client.projects or []):
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
        id=client.id,
        company_name=client.company_name,
        contact_person=client.contact_person,
        email=client.email,
        phone=client.phone,
        address=client.address,
        status=client.status,
        created_at=client.created_at,
        projects=response_projects,
    )


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
        project_name = (
            payload.initial_project_name
            or f"{payload.company_name.strip()} - Onboarding Implementation"
        )
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

    return _format_client_response(new_client)


@router.get(
    "",
    response_model=List[ClientResponse],
    status_code=status.HTTP_200_OK,
    summary="List all clients with onboarding status",
    description="Retrieves a list of all registered clients and their linked onboarding projects.",
)
def list_clients(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by client status"),
    search: Optional[str] = Query(None, description="Search by company name or contact person"),
    db: Session = Depends(get_db),
):
    """List all registered onboarding clients."""
    try:
        query = db.query(Client)
        if status_filter:
            query = query.filter(Client.status == status_filter)
        if search:
            search_pattern = f"%{search.strip()}%"
            query = query.filter(
                (Client.company_name.ilike(search_pattern))
                | (Client.contact_person.ilike(search_pattern))
                | (Client.email.ilike(search_pattern))
            )

        clients = query.order_by(Client.created_at.desc()).all()
        return [_format_client_response(c) for c in clients]
    except SQLAlchemyError as err:
        logger.error(f"Database error querying clients list: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve clients list from database.",
        )


@router.get(
    "/{client_id}",
    response_model=ClientResponse,
    status_code=status.HTTP_200_OK,
    summary="Get client details by ID",
    description="Fetches a specific client record and its onboarding project implementation details by ID.",
)
def get_client_by_id(client_id: int, db: Session = Depends(get_db)):
    """Fetch client by primary key ID."""
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
    except SQLAlchemyError as err:
        logger.error(f"Database error fetching client id {client_id}: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while querying client with ID {client_id}.",
        )

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with ID {client_id} was not found.",
        )

    return _format_client_response(client)


@router.put(
    "/{client_id}",
    response_model=ClientResponse,
    status_code=status.HTTP_200_OK,
    summary="Update client details",
    description="Updates existing client profile information.",
)
def update_client(client_id: int, payload: ClientUpdate, db: Session = Depends(get_db)):
    """Update existing client profile."""
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
    except SQLAlchemyError as err:
        logger.error(f"Database error finding client id {client_id} for update: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database query error for client ID {client_id}.",
        )

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with ID {client_id} was not found.",
        )

    # Check email conflict if changing email
    if payload.email and payload.email.lower().strip() != client.email:
        conflict = (
            db.query(Client)
            .filter(Client.email == payload.email.lower().strip(), Client.id != client_id)
            .first()
        )
        if conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email '{payload.email}' is already used by another client.",
            )
        client.email = payload.email.lower().strip()

    if payload.company_name is not None:
        client.company_name = payload.company_name.strip()
    if payload.contact_person is not None:
        client.contact_person = payload.contact_person.strip()
    if payload.phone is not None:
        client.phone = payload.phone.strip()
    if payload.address is not None:
        client.address = payload.address.strip()
    if payload.status is not None:
        client.status = payload.status.strip()

    try:
        db.commit()
        db.refresh(client)
    except SQLAlchemyError as err:
        db.rollback()
        logger.error(f"Database error committing update for client id {client_id}: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update client details in database.",
        )

    return _format_client_response(client)
