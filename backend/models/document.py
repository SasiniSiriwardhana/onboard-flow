from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Sequence
from sqlalchemy.orm import relationship

from backend.database import Base


class Document(Base):
    """
    SQLAlchemy model representing an Onboarding Document / Attachment.
    Compatible with Oracle Database using Sequence for primary key autoincrement.
    """

    __tablename__ = "documents"

    id = Column(Integer, Sequence("documents_id_seq"), primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True, index=True)
    file_name = Column(String(255), nullable=False)
    file_url = Column(String(500), nullable=False)
    file_type = Column(String(100), nullable=False)
    file_size_bytes = Column(Integer, default=0, nullable=False)
    uploaded_by = Column(String(120), default="System User", nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    project = relationship("Project", backref="documents", lazy="joined")

    def __repr__(self) -> str:
        return (
            f"<Document(id={self.id}, file_name='{self.file_name}', "
            f"file_type='{self.file_type}', uploaded_at='{self.uploaded_at}')>"
        )
