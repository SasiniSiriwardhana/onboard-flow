from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Sequence
from sqlalchemy.orm import relationship

from backend.database import Base


class Task(Base):
    """
    SQLAlchemy model representing an Onboarding Task linked to a Project.
    Compatible with Oracle Database using Sequence for primary key autoincrement.
    """

    __tablename__ = "tasks"

    id = Column(Integer, Sequence("tasks_id_seq"), primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="To Do", nullable=False)  # "To Do", "In Progress", "Done"
    priority = Column(String(30), default="Medium", nullable=False)  # "Low", "Medium", "High", "Critical"
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    project = relationship("Project", backref="tasks", lazy="joined")

    def __repr__(self) -> str:
        return (
            f"<Task(id={self.id}, project_id={self.project_id}, title='{self.title}', "
            f"status='{self.status}', priority='{self.priority}')>"
        )
