import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import bcrypt

# Ensure compatibility between passlib 1.7.4 and bcrypt >= 4.0.0
if not hasattr(bcrypt, "__about__"):
    class _BcryptAbout:
        __version__ = getattr(bcrypt, "__version__", "4.0.0")
    bcrypt.__about__ = _BcryptAbout()

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from backend.config import settings
from backend.database import get_db
from backend.models.user import User

logger = logging.getLogger(__name__)

# Password hashing context with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for extracting Bearer token from headers
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
