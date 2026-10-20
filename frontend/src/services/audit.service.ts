import api from "../api/axios";

export interface AuditLog {
  id: number;
  document_id: number;
  action: string;
  performed_by: string;
  details: string;
  created_at: string;
  tenant_id?: string;
}

class AuditService {
  async getAuditLogs(): Promise<AuditLog[]> {
    const response = await api.get<AuditLog[]>(
      "/v1/audit"
    );

    return response.data;
  }

  async getDocumentAuditLogs(
    documentId: number
  ): Promise<AuditLog[]> {

    const response = await api.get<AuditLog[]>(
      `/v1/audit/document/${documentId}`
    );

    return response.data;
  }
}

export default new AuditService();