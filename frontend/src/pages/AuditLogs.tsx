import {
  useEffect,
  useState,
} from "react";

import AuditService from "../services/audit.service";

type AuditLog = {
  id: string | number;
  document_id: string | number;
  action: string;
  performed_by: string;
  details: string;          
  created_at: string;
};

function AuditLogs() {

  const [logs, setLogs] =
    useState<AuditLog[]>([]);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    loadLogs();
  }, []);

  const loadLogs = async () => {
    try {

      const data =
        await AuditService
          .getAuditLogs();

      setLogs(data);

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
    <div
      style={{
        padding: "20px"
      }}
    >
      <h1>Audit Logs</h1>

      <table
        style={{
          width: "100%",
          borderCollapse:
            "collapse"
        }}
      >
        <thead>
          <tr>
            <th>ID</th>
            <th>Document</th>
            <th>Action</th>
            <th>User</th>
            <th>Details</th>
            <th>Date</th>
          </tr>
        </thead>

        <tbody>

          {logs.map((log) => (

            <tr key={log.id}>

              <td>{log.id}</td>

              <td>
                {log.document_id}
              </td>

              <td>

                <span
                  style={{
                    background:
                      getColor(
                        log.action
                      ),
                    color:"white",
                    padding:
                      "4px 8px",
                    borderRadius:
                      "4px"
                  }}
                >
                  {log.action}
                </span>

              </td>

              <td>
                {log.performed_by}
              </td>

              <td>
                {log.details}
              </td>

              <td>
                {
                  new Date(
                    log.created_at
                  )
                  .toLocaleString()
                }
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}

function getColor(
  action: string
) {

  switch(action) {

    case "DOCUMENT_UPLOADED":
      return "#0d6efd";

    case "DOCUMENT_APPROVED":
      return "#198754";

    case "DOCUMENT_REJECTED":
      return "#dc3545";

    default:
      return "#6c757d";
  }
}

export default AuditLogs;