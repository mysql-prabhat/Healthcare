import {
  useEffect,
  useState
} from "react";
import { useNavigate } from "react-router-dom";
import DocumentService from "../services/document.service";
import PatientService from "../services/patient.service";

function DocumentUpload() {
  const navigate = useNavigate();

  const [title, setTitle] = useState("");
  const [file, setFile] =  useState<File | null>(null);
  const [patients, setPatients] = useState<any[]>([]);
  const [patientId, setPatientId] = useState("");

  useEffect(() => {
    loadPatients();
  }, []);

  const loadPatients = async () => {
    const data =
      await PatientService.getPatients();
      setPatients(data);
  };
  const upload = async () => {
    console.log("Uploading document:", title, file);
    if (!file) {
      alert("Choose file");
      return;
    }

    try {
      await DocumentService.uploadDocument(
        title,
        patientId,
        file
      );

      alert("Uploaded");

      setTitle("");
      navigate("/documents");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>

      <h2>
        Upload Document
      </h2>

      <input
        type="text"
        placeholder="Title"
        value={title}
        onChange={(e) =>
          setTitle(
            e.target.value
          )
        }
      />

      <br />

      <input
        type="file"
        onChange={(e) =>
          setFile(
            e.target.files?.[0] ?? null
          )
        }
      />
      <select  value={patientId} onChange={(e) =>setPatientId(e.target.value)}>
        <option value="">
          Select Patient
        </option>

        {patients.map((patient) => (
          <option
            key={patient.patient_id}
            value={patient.patient_id}
          >
            {patient.first_name}
            {" "}
            {patient.last_name}
          </option>
        ))}
      </select>
      <br />
      <br />

      <button onClick={upload}>
        Upload
      </button>

    </div>
  );
}

export default DocumentUpload;