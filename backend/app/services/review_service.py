from sqlalchemy.orm import Session

from app.core.models import AuditLog, Document, Review


class ReviewService:
    def approve(
        self,
        db: Session,
        document_id: int,
        approved: bool,
        reviewer: str,
        comments: str | None = None,
    ) -> Document | None:
        document = db.query(Document).filter(
            Document.id == document_id
        ).first()
        if document is None:
            return None

        document.status = "APPROVED" if approved else "REJECTED"
        review = Review(
            document_id=document_id,
            approved=str(approved),
            reviewer=reviewer,
            comments=comments,
        )
        db.add(review)
        db.add(
            AuditLog(
                document_id=document_id,
                action="APPROVE" if approved else "REJECT",
                performed_by=reviewer,
                details=comments,
            )
        )
        db.commit()
        db.refresh(document)
        return document
