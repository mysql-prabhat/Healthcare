from app.core.db import SessionLocal
from app.core.models import (
    Document,
    DeadLetterQueue
)

from app.services.text_extractor import (
    extract_text
)

from app.services.ai_service import (
    generate_summary
)

MAX_RETRY = 3

def process_document(
    document_id: int
):
    db = SessionLocal()

    try:
        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )
        if document is None:
            raise LookupError(
                f"Document {document_id} was not found"
            )

        try:
            text = extract_text(document.file_path)
            ai_result = generate_summary(text)

            document.extracted_text = text
            document.summary = ai_result["summary"]
            document.recommendations = str(
                ai_result["recommendations"]
            )
            document.confidence_score = ai_result["confidence"]
            document.status = "PENDING_REVIEW"
            document.processing_error = None
            db.commit()

        except Exception as ex:
            db.rollback()
            handle_retry(db, document, str(ex))
    finally:
        db.close()

def handle_retry(
    db,
    document,
    error_message
):

    document.retry_count = (document.retry_count or 0) + 1

    document.processing_error = (
        error_message
    )

    if (
        document.retry_count
        < MAX_RETRY
    ):

        document.status = (
            "RETRYING"
        )

        db.commit()

        from app.core.redis import (
            document_queue
        )

        document_queue.enqueue(
            process_document,
            document.id
        )

    else:

        move_to_dlq(
            db,
            document,
            error_message
        )

def move_to_dlq(
    db,
    document,
    error_message
):

    dead_record = (
        DeadLetterQueue(
            document_id=document.id,
            error_message=error_message,
            retry_attempts=
                document.retry_count,
            payload=document.file_name
        )
    )

    db.add(dead_record)

    document.status = "FAILED"

    db.commit()