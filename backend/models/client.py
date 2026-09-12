from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Sequence
from sqlalchemy.orm import relationship

from backend.database import Base


class Client(Base):
    """
    SQLAlchemy model representing a Client in the Customer Onboarding System.
    Compatible with Oracle Database using Sequence for primary key autoincrement.
    """

    __tablename__ = "clients"

    id = Column(Integer, Sequence("client_id_seq"), primary_key=True, index=True)
    company_name = Column(String(150), nullable=False, index=True)
    contact_person = Column(String(120), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    phone = Column(String(50), nullable=True)
    address = Column(String(255), nullable=True)
    status = Column(String(50), default="Active", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    projects = relationship(
        "Project", back_populates="client", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Client(id={self.id}, company_name='{self.company_name}', email='{self.email}', status='{self.status}')>"
