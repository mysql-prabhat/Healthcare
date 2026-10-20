from datetime import datetime
from redis.exceptions import RedisError

from app.core.db import get_db
from app.core.models import Document, Patient
from app.api.v1.audit import create_audit_log
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException
)
from app.core.auth import get_current_user
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
import os
import shutil
from uuid import uuid4
from fastapi.responses import FileResponse
from app.core.redis import document_queue

UPLOAD_DIR = "uploads"
os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)
router = APIRouter( 
    prefix="/v1/documents",
    tags=["Documents"]
)

class DocumentCreate(BaseModel):
    title: str
    file_name: str | None = None
    file_type: str | None = None
    file_path: str | None = None    

class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    patient_name: str | None = None
    summary: str | None = None
    status: str
    file_name: str | None = None
    file_type: str | None = None
    file_path: str | None = None
    created_at: datetime | None = None

ALLOWED_TYPES = [
    "application/pdf",
    "application/json",
    "text/plain",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
]

DOCUMENT_STATUS = [
    "PENDING",
    "APPROVED",
    "REJECTED",
    "UPLOADED",
    "PROCESSING",
    "PENDING_REVIEW"
]

@router.post("/documents")
def create_document(
    request: DocumentCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    document = Document(
        title=request.title,
        file_name=request.file_name,
        file_type=request.file_type,
        file_path=request.file_path,
        tenant_id=user["tenant_id"],
        status="PENDING",
        created_at=datetime.utcnow()
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document

@router.get("/documents")
def get_documents(
    db: Session = Depends(get_db),
     user=Depends(get_current_user)
) -> list[DocumentResponse]:

    documents = (
            db.query(Document)
            .filter(
                Document.tenant_id == user["tenant_id"]
            ).join(
                Patient,
                Document.patient_id == Patient.id
            )
            .all()
        )
    return [DocumentResponse.model_validate(doc) for doc in documents]


@router.post("/upload")
def upload_document(
    title: str = Form(...),
    file: UploadFile = File(...),
    patient_id: str = Form(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type"
        )
    safe_filename = (file.filename or "upload").replace(" ", "_")
    unique_name = f"{uuid4()}_{safe_filename}"

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_name
    )
    patient = (
        db.query(Patient)
        .filter(
            Patient.patient_id == patient_id,
            Patient.tenant_id == user["tenant_id"]
        )
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    document = Document(
        title=title,
        file_name=file.filename or safe_filename,
        file_path=file_path,
        file_type=file.content_type,
        patient_id=patient.id,
        tenant_id=user["tenant_id"],
        status="PROCESSING",
        created_at=datetime.utcnow(),
        retry_count=0
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    try:
        job = document_queue.enqueue(
            "app.workers.document_worker.process_document",
            document.id
        )
    except RedisError as exc:
        document.status = "FAILED"
        document.processing_error = str(exc)
        db.commit()
        raise HTTPException(
            status_code=503,
            detail="Document processing queue is unavailable"
        ) from exc

    return {
        "id": document.id,
        "title": document.title,
        "file_name": document.file_name,
        "file_type": document.file_type,
        "status": document.status,
        "tenant_id": document.tenant_id,
        "job_id": job.id
    }

@router.get("/{document_id}/download")
def download_document(
    document_id: int,
    db: Session = Depends(get_db)
):

    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return FileResponse(
        document.file_path,
        filename=document.file_name
    )
