
from app.core.auth import get_current_user
from app.core.models import Condition, Medication, Observation, Patient
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.schemas import PatientCreate

router = APIRouter(
    prefix="/v1/patients",
    tags=["Patients"]
)


@router.get("/{patient_id}/dashboard")
def get_dashboard(
    patient_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    patient = (
        db.query(Patient)
        .filter(
            Patient.patient_id == patient_id,
            Patient.tenant_id == user["tenant_id"],
        )
        .first()
    )
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    observations = (
        db.query(Observation)
        .filter(
            Observation.patient_id == patient_id
        )
        .all()
    )

    conditions = (
        db.query(Condition)
        .filter(
            Condition.patient_id == patient_id
        )
        .all()
    )

    medications = (
        db.query(Medication)
        .filter(
            Medication.patient_id == patient_id
        )
        .all()
    )

    return {
        "patient": patient,
        "observations": observations,
        "conditions": conditions,
        "medications": medications
    }

@router.post("")
def create_patient(
    request: PatientCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    patient = Patient(
        patient_id=request.patient_id,
        first_name=request.first_name,
        last_name=request.last_name,
        dob=request.dob,
        gender=request.gender,
        tenant_id=user["tenant_id"]
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient

@router.get("")
def get_patients(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return (
        db.query(Patient)
        .filter(Patient.tenant_id == user["tenant_id"])
        .all()
    )