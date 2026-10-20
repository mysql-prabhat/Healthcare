import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import PatientService from "../services/patient.service";

import { type PatientDashboardResponse } from "../types/patient";

function PatientDashboard() {
  const { id } = useParams();

  const [dashboard, setDashboard] =
    useState<PatientDashboardResponse>();

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    if (id) {
      loadDashboard(id);
    }
  }, [id]);

  const loadDashboard = async (
    patientId: string
  ) => {
    try {
      const data =
        await PatientService.getPatientDashboard(
          patientId
        );

      setDashboard(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <h2>Loading...</h2>;
  }

  if (!dashboard) {
    return <h2>No Data Found</h2>;
  }

  return (
    <div
      style={{
        maxWidth: "1200px",
        margin: "0 auto",
        padding: "20px",
      }}
    >
      <h1>Patient Dashboard</h1>

      {/* Patient Information */}

      <div className="card">
        <h2>Patient Information</h2>

        <p>
          <strong>Name:</strong>{" "}
          {dashboard.patient.first_name}{" "}
          {dashboard.patient.last_name}
        </p>

        <p>
          <strong>Patient Id:</strong>{" "}
          {dashboard.patient.patient_id}
        </p>

        <p>
          <strong>DOB:</strong>{" "}
          {dashboard.patient.dob}
        </p>

        <p>
          <strong>Gender:</strong>{" "}
          {dashboard.patient.gender}
        </p>
      </div>

      {/* Conditions */}

      <div className="card">
        <h2>Conditions</h2>

        <ul>
          {dashboard.conditions.map(
            (condition) => (
              <li key={condition.id}>
                {condition.diagnosis}
              </li>
            )
          )}
        </ul>
      </div>

      {/* Medications */}

      <div className="card">
        <h2>Medications</h2>

        <ul>
          {dashboard.medications.map(
            (medication) => (
              <li key={medication.id}>
                {medication.medication_name}
                {" "}
                ({medication.dosage})
              </li>
            )
          )}
        </ul>
      </div>

      {/* Observations */}

      <div className="card">
        <h2>Observations</h2>

        <table>
          <thead>
            <tr>
              <th>Type</th>
              <th>Value</th>
              <th>Unit</th>
            </tr>
          </thead>

          <tbody>
            {dashboard.observations.map(
              (obs) => (
                <tr key={obs.id}>
                  <td>
                    {obs.observation_type}
                  </td>

                  <td>{obs.value}</td>

                  <td>{obs.unit}</td>
                </tr>
              )
            )}
          </tbody>
        </table>
      </div>

      {/* AI Summary */}

      <div className="card">
        <h2>AI Clinical Summary</h2>

        <p>
          {dashboard.ai_summary ??
            "Summary not generated"}
        </p>
      </div>

      {/* Risk */}

      <div className="card">
        <h2>Risk Assessment</h2>

        <span
          style={{
            background:
              dashboard.risk_level ===
              "HIGH"
                ? "#dc3545"
                : "#198754",
            color: "white",
            padding: "8px 12px",
            borderRadius: "5px",
          }}
        >
          {dashboard.risk_level ??
            "Unknown"}
        </span>
      </div>

      {/* Recommendations */}

      <div className="card">
        <h2>Recommendations</h2>

        <ul>
          {dashboard.recommendations?.map(
            (item, index) => (
              <li key={index}>
                {item}
              </li>
            )
          )}
        </ul>
      </div>
    </div>
  );
}

export default PatientDashboard;