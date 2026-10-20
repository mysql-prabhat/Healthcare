import { useEffect, useState } from "react";
import DocumentService from "../services/document.service";
import type { Document } from "../types/document";
import { useNavigate } from "react-router-dom";

function Documents() {
  const navigate = useNavigate();
  const [documents, setDocuments] =
    useState<Document[]>([]);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const data =
        await DocumentService.getDocuments();

      setDocuments(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <h2>Loading...</h2>;
  }

  return (
    <div style={{ padding: "20px" }}>

      <h1>Documents</h1>
      <button onClick={loadDocuments}>
        Refresh
      </button>
      <button
        onClick={() =>
          navigate("/documents/upload")
        }
      >
        Create Document
      </button>
      <table
        border={1}
        cellPadding={10}
        width="100%"
      >
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Status</th>
            <th>Summary</th>
            <th>File Name</th>
            <th>Type</th>
            <th>Patient Name</th>
            <th>Download</th>
          </tr>
        </thead>

        <tbody>

          {documents.map((document) => (
            <tr key={document.id}>

              <td>{document.id}</td>

              <td>{document.title}</td>

              <td>
                <span
                  style={{
                    color:
                      document.status === "APPROVED"
                        ? "green"
                        : document.status === "REJECTED"
                        ? "red"
                        : "orange",
                    fontWeight: "bold",
                  }}
                >
                  {document.status}
                </span>
              </td>

              <td>
                {document.summary && document.summary.length > 0
                  ? document.summary.slice(0, 100) + (document.summary.length > 100 ? "..." : "")
                  : "Not Generated"}
              </td>
              <td>
                {document.file_name && document.file_name.length > 0
                  ? document.file_name
                  : "Not Generated"}
              </td>
              <td>
                {document.file_type && document.file_type.length > 0
                  ? document.file_type
                  : "Not Generated"}
              </td>
              <td>
                {document.patient_name}
              </td>
              <td>
                <button
                  onClick={() =>
                    navigate(
                      `/documents/${document.id}/download`
                    )
                  }
                >
                  Download
                </button>
              </td>
            </tr>
          ))}

        </tbody>
      </table>

    </div>
  );
}

export default Documents;