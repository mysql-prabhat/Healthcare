import api from "../api/axios";

export interface PatientDashboard {
  patient: any;
  observations: any[];
  conditions: any[];
  medications: any[];
  ai_summary?: string;
}

class PatientService {
  async getPatientDashboard(
    patientId: string
  ): Promise<PatientDashboard> {

    const response = await api.get(
      `patients/${patientId}/dashboard`
    );

    return response.data;
  }

  async getPatients() {
    const response = await api.get(
      "patients"
    );

    return response.data;
  }
}

export default new PatientService();