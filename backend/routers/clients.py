import logging
from typing import List
from fastapi import APIRouter

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
