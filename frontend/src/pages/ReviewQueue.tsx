import { useEffect, useState } from "react";
import api from "../api/axios";

interface ReviewDocument {
  id: number;
  title: string;
  file_name: string;
  summary: string;
  recommendations: string;
  confidence_score: number;
  status: string;
}

function ReviewQueue() {
  const [documents, setDocuments] = useState<
    ReviewDocument[]
  >([]);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    loadQueue();
  }, []);

  const loadQueue = async () => {
    try {
      const response = await api.get(
        "/review/queue"
      );

      setDocuments(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const approveDocument = async (
    documentId: number
  ) => {
    try {
      await api.post(
        `/review/${documentId}/approve`
      );

      loadQueue();
    } catch (error) {
      console.error(error);
    }
  };

  const rejectDocument = async (
    documentId: number
  ) => {
    try {
      await api.post(
        `/review/${documentId}/reject`
      );

      loadQueue();
    } catch (error) {
      console.error(error);
    }
  };

  if (loading) {
    return <h2>Loading...</h2>;
  }

  return (
    <div
      style={{
        padding: "20px",
        maxWidth: "1200px",
        margin: "0 auto",
      }}
    >
      <h1>
        Human Review Queue
      </h1>

      {documents.length === 0 && (
        <h3>
          No Documents Awaiting Review
        </h3>
      )}

      {documents.map((doc) => (
        <div
          key={doc.id}
          style={{
            border: "1px solid #ddd",
            borderRadius: "8px",
            padding: "20px",
            marginBottom: "20px",
            boxShadow:
              "0px 2px 8px rgba(0,0,0,0.1)",
          }}
        >
          <h3>{doc.title}</h3>

          <p>
            <strong>File:</strong>{" "}
            {doc.file_name}
          </p>

          <p>
            <strong>Status:</strong>{" "}
            <span
              style={{
                color: "orange",
                fontWeight: "bold",
              }}
            >
              {doc.status}
            </span>
          </p>

          <div>
            <strong>AI Summary</strong>

            <div
              style={{
                marginTop: "10px",
                padding: "15px",
                background: "#f4f4f4",
              }}
            >
              {doc.summary}
            </div>
          </div>

          <div
            style={{
              marginTop: "15px",
            }}
          >
            <strong>
              Recommendations
            </strong>

            <div
              style={{
                marginTop: "10px",
                padding: "15px",
                background: "#f4f4f4",
              }}
            >
              {doc.recommendations}
            </div>
          </div>

          <div
            style={{
              marginTop: "15px",
            }}
          >
            <strong>
              Confidence Score:
            </strong>{" "}
            {(doc.confidence_score * 100)
              .toFixed(0)}
            %
          </div>

          <div
            style={{
              marginTop: "20px",
              display: "flex",
              gap: "10px",
            }}
          >
            <button
              style={{
                background: "#28a745",
                color: "#fff",
                border: "none",
                padding:
                  "10px 20px",
                cursor: "pointer",
              }}
              onClick={() =>
                approveDocument(doc.id)
              }
            >
              Approve
            </button>

            <button
              style={{
                background: "#dc3545",
                color: "#fff",
                border: "none",
                padding:
                  "10px 20px",
                cursor: "pointer",
              }}
              onClick={() =>
                rejectDocument(doc.id)
              }
            >
              Reject
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default ReviewQueue;