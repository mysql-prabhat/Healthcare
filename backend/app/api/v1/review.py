from app.core.models import Document
from fastapi import APIRouter, Depends, HTTPException
from app.core.rbac import require_reviewer, require_roles
from app.core.schemas import ReviewRequest
from app.core.db import get_db
from sqlalchemy.orm import Session
from app.services.review_service import ReviewService


router = APIRouter(
    prefix="/v1/review",
    tags=["Review"]
)
review_service = ReviewService()

@router.get("/queue")
def review_queue(
    db: Session = Depends(get_db),
    user=Depends(require_roles(
        ["reviewer", "admin"]
    ))
):

    return (
        db.query(Document)
        .filter(
            Document.status ==
            "PENDING_REVIEW"
        )
        .all()
    )

@router.post("/{document_id}")
def approve_document(
    document_id: int,
    request: ReviewRequest,
    db: Session = Depends(get_db),
    user=Depends(require_reviewer())
):

    document = review_service.approve(
        db=db,
        document_id=document_id,
        approved=request.approved,
        reviewer=user["sub"],
        comments=request.comments,
    )
    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )
    return document

@router.post("/{document_id}/approve")
def approve_document_status(
    document_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_reviewer()),
):
    document = review_service.approve(
        db=db,
        document_id=document_id,
        approved=True,
        reviewer=user["sub"],
    )
    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )
    return document

@router.post("/{document_id}/reject")
def reject_document(
    document_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_reviewer()),
):
    document = review_service.approve(
        db=db,
        document_id=document_id,
        approved=False,
        reviewer=user["sub"],
    )
    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )
    return document