def create_patient_summary(
    patient,
    observations,
    conditions,
    medications
):
    summary = f"""
    Patient Summary for {patient.first_name} {patient.last_name} (ID: {patient.patient_id}):

    Demographics:
    - Date of Birth: {patient.dob}
    - Gender: {patient.gender}

    Observations:
    """
    for obs in observations:
        summary += f"- {obs.observation_type}: {obs.value} {obs.unit}\n"

    summary += "\nConditions:\n"
    for cond in conditions:
        summary += f"- {cond.diagnosis}\n"

    summary += "\nMedications:\n"
    for med in medications:
        summary += f"- {med.medication_name}, Dosage: {med.dosage}\n"

    return summary