from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class DocumentBase(BaseModel):
    file_name: str = Field(..., min_length=1, max_length=255, description="Document filename")
    file_url: str = Field(..., min_length=1, max_length=500, description="Cloudinary or storage URL")
    file_type: str = Field(..., description="MIME type or file extension")
    file_size_bytes: int = Field(default=0, description="File size in bytes")
    project_id: Optional[int] = Field(None, description="Linked project ID")
    uploaded_by: Optional[str] = Field("System User", description="Uploader name or email")


class DocumentCreate(DocumentBase):
    pass


class DocumentResponse(DocumentBase):
    id: int
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)
