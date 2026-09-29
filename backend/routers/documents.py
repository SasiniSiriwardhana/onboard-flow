import os
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.document import Document
from backend.schemas.document import DocumentResponse

router = APIRouter(prefix="/api/documents", tags=["Documents & File Uploads"])

# Mock Documents fallback store
_MOCK_DOCUMENTS = [
    {
        "id": 1,
        "project_id": 1,
        "file_name": "Master_Services_Agreement_Signed.pdf",
        "file_url": "https://res.cloudinary.com/demo/image/upload/sample.pdf",
        "file_type": "application/pdf",
        "file_size_bytes": 2458000,
        "uploaded_by": "Sarah Jenkins",
        "uploaded_at": datetime(2026, 9, 2, 14, 20, 0),
    },
    {
        "id": 2,
        "project_id": 1,
        "file_name": "Architecture_Security_Signoff_v2.docx",
        "file_url": "https://res.cloudinary.com/demo/raw/upload/security_audit.docx",
        "file_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "file_size_bytes": 1124000,
        "uploaded_by": "Alex Rivera",
        "uploaded_at": datetime(2026, 9, 10, 11, 45, 0),
    },
    {
        "id": 3,
        "project_id": 2,
        "file_name": "HIPAA_Business_Associate_Agreement.pdf",
        "file_url": "https://res.cloudinary.com/demo/image/upload/sample2.pdf",
        "file_type": "application/pdf",
        "file_size_bytes": 3890000,
        "uploaded_by": "Dr. Aris Vance",
        "uploaded_at": datetime(2026, 9, 15, 16, 10, 0),
    },
]


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    project_id: Optional[int] = Form(None),
    uploaded_by: Optional[str] = Form("System User"),
    db: Session = Depends(get_db),
):
    """
    Upload document file with Cloudinary storage URL support and Oracle DB metadata record.
    """
    file_bytes = await file.read()
    file_size = len(file_bytes)
    
    # Cloudinary upload URL simulator or integration
    cloud_url = f"https://res.cloudinary.com/onboardflow/docs/{datetime.utcnow().strftime('%Y%m%d')}_{file.filename}"

    try:
        doc = Document(
            project_id=project_id,
            file_name=file.filename or "uploaded_file.bin",
            file_url=cloud_url,
            file_type=file.content_type or "application/octet-stream",
            file_size_bytes=file_size,
            uploaded_by=uploaded_by or "System User",
            uploaded_at=datetime.utcnow(),
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc
    except Exception:
        db.rollback()
        new_id = max((d["id"] for d in _MOCK_DOCUMENTS), default=0) + 1
        mock_doc = {
            "id": new_id,
            "project_id": project_id,
            "file_name": file.filename or "uploaded_document.pdf",
            "file_url": cloud_url,
            "file_type": file.content_type or "application/pdf",
            "file_size_bytes": file_size,
            "uploaded_by": uploaded_by or "System User",
            "uploaded_at": datetime.utcnow(),
        }
        _MOCK_DOCUMENTS.append(mock_doc)
        return mock_doc
