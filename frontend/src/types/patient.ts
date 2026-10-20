export interface Patient {
  id: number;
  patient_id: string;
  first_name: string;
  last_name: string;
  dob: string;
  gender: string;
}

export interface Observation {
  id: number;
  observation_type: string;
  value: string;
  unit: string;
}

export interface Condition {
  id: number;
  diagnosis: string;
}

export interface Medication {
  id: number;
  medication_name: string;
  dosage: string;
}

export interface PatientDashboardResponse {
  patient: Patient;
  conditions: Condition[];
  medications: Medication[];
  observations: Observation[];
  ai_summary?: string;
  risk_level?: string;
  recommendations?: string[];
}