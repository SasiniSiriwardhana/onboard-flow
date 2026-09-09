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


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate user and issue JWT token",
    description="Verifies user credentials (email & password) and returns a signed JWT access token with the user profile.",
)
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user:
    - Finds user by email
    - Verifies password against bcrypt hash
    - Checks if account is active
    - Issues JWT access token
    - Returns token and user profile
    """
    try:
        user = db.query(User).filter(User.email == payload.email.lower().strip()).first()
    except SQLAlchemyError as err:
        logger.error(f"Database error during user login query: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error during authentication.",
        )

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated. Please contact an administrator.",
        )

    # Generate JWT token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user,
    )


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current authenticated user profile",
    description="Protected endpoint that decodes the Bearer JWT token and returns the current user profile.",
)
def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """
    Return currently authenticated user from Bearer token.
    """
    return current_user
