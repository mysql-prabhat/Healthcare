from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
    Float
)

from app.core.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String)
    tenant_id = Column(String)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    document_id = Column(
        Integer,
        ForeignKey("documents.id")
    )
    approved = Column(String)
    comments = Column(Text)
    reviewer = Column(String)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer)
    action = Column(String)
    performed_by = Column(String)
    details = Column(Text)



class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    tenant_id = Column(String)
    patient_id = Column(
        Integer,
        ForeignKey("patients.id")
    )
    title = Column(String)
    file_name = Column(String)
    file_path = Column(String)
    file_type = Column(String)
    extracted_text = Column(Text)
    summary = Column(Text)
    recommendations = Column(Text)
    confidence_score = Column(Float)
    retry_count = Column(
        Integer,
        default=0
    )
    processing_error = Column(Text)
    status = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    patient_id = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    dob = Column(String)
    gender = Column(String)
    tenant_id = Column(String)

class Observation(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key=True)
    patient_id = Column(String)
    observation_type = Column(String)
    value = Column(String)
    unit = Column(String)

class Condition(Base):
    __tablename__ = "conditions"

    id = Column(Integer, primary_key=True)
    patient_id = Column(String)
    diagnosis = Column(String)

class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True)
    patient_id = Column(String)
    medication_name = Column(String)
    dosage = Column(String)

class DeadLetterQueue(Base):
    __tablename__ = "dead_letter_queue"
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer)
    error_message = Column(Text)
    retry_attempts = Column(Integer)
    payload = Column(Text)
    created_at = Column(DateTime)