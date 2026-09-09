import logging
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from backend.config import settings
from backend.database import get_db
from backend.models.user import User
from backend.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse,
)
from backend.utils.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_active_user,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
    description="Validates user payload, hashes the password using bcrypt, and creates a new user record in the Oracle database.",
)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user:
    - Verifies that email is not already taken
    - Hashes password using bcrypt
    - Persists user to database
    - Returns newly created user details (excluding password hash)
    """
    # Check if user already exists
    try:
        existing_user = db.query(User).filter(User.email == payload.email.lower()).first()
    except SQLAlchemyError as err:
        logger.error(f"Database query error during registration: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error while checking existing user.",
        )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email address already exists.",
        )

    # Hash the password
    hashed_pwd = get_password_hash(payload.password)

    # Instantiate User model
    new_user = User(
        name=payload.name.strip(),
        email=payload.email.lower().strip(),
        hashed_password=hashed_pwd,
        is_active=True,
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except SQLAlchemyError as err:
        db.rollback()
        logger.error(f"Database error during user registration commit: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save user account to database.",
        )

    return new_user
