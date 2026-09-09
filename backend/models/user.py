from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Sequence
from backend.database import Base


class User(Base):
    """SQLAlchemy User model for authentication and system access."""

    __tablename__ = "users"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', is_active={self.is_active})>"
