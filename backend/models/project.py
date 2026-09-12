from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Sequence
from sqlalchemy.orm import relationship

from backend.database import Base


class Project(Base):
    """
    SQLAlchemy model representing an Onboarding Project linked to a Client.
    Compatible with Oracle Database using Sequence for primary key autoincrement.
    """

    __tablename__ = "projects"

    id = Column(Integer, Sequence("projects_id_seq"), primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="Pending", nullable=False)
    progress = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    client = relationship("Client", back_populates="projects")

    def __repr__(self) -> str:
        return (
            f"<Project(id={self.id}, client_id={self.client_id}, name='{self.name}', "
            f"status='{self.status}', progress={self.progress}%)>"
        )
