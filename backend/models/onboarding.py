from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Sequence,
)
from sqlalchemy.orm import relationship

from backend.database import Base


class Customer(Base):
    """Customer account undergoing onboarding/implementation."""

    __tablename__ = "customers"

    id = Column(Integer, Sequence("customer_id_seq"), primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    company = Column(String(150), nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    tier = Column(String(50), default="Enterprise")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    projects = relationship("OnboardingProject", back_populates="customer", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Customer(id={self.id}, company='{self.company}', tier='{self.tier}')>"


class OnboardingProject(Base):
    """Customer Onboarding Project implementation tracker."""

    __tablename__ = "onboarding_projects"

    id = Column(Integer, Sequence("project_id_seq"), primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="Kickoff")  # Kickoff, Data Migration, Testing, Go-Live, Completed
    progress = Column(Integer, default=0)           # 0 to 100 percentage
    target_go_live = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="projects")

    def __repr__(self) -> str:
        return f"<OnboardingProject(id={self.id}, title='{self.title}', status='{self.status}')>"
