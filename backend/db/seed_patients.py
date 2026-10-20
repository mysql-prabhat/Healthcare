import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from app.core.db import SessionLocal
from app.core.models import Patient

db = SessionLocal()

patients = [
    Patient(
        patient_id="P001",
        first_name="John",
        last_name="Doe",
        dob="1985-05-10",
        gender="Male",
        tenant_id="tenant-001"
    ),
    Patient(
        patient_id="P002",
        first_name="Jane",
        last_name="Smith",
        dob="1990-08-20",
        gender="Female",
        tenant_id="tenant-001"
    ),
    Patient(
        patient_id="P003",
        first_name="Michael",
        last_name="Wilson",
        dob="1975-03-18",
        gender="Male",
        tenant_id="tenant-001"
    ),
    Patient(
        patient_id="P004",
        first_name="Sarah",
        last_name="Johnson",
        dob="1988-12-05",
        gender="Female",
        tenant_id="tenant-001"
    ),
    Patient(
        patient_id="P005",
        first_name="David",
        last_name="Brown",
        dob="1995-07-15",
        gender="Male",
        tenant_id="tenant-001"
    )
]

db.add_all(patients)
db.commit()

print("Patients seeded")