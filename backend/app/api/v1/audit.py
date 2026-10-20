from app.core.models import AuditLog
from app.core.auth import get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db

router = APIRouter(
    prefix="/v1",
    tags=["Audit"]
)


@router.get("/audit")
def get_audit_logs(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    return (
        db.query(AuditLog)
        .filter(
            AuditLog.tenant_id ==
            user["tenant_id"]
        )
        .order_by(
            AuditLog.created_at.desc()
        )
        .all()
    )

async def create_audit_log(
    db: Session,
    document_id: int,
    action: str,
    user: dict
):
    audit =  AuditLog(
        document_id=document_id,
        action=action,
        performed_by=user
    )

    db.add(audit)
    db.commit()