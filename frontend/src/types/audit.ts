export interface AuditLog {
  id: number;
  document_id: number;
  action: string;
  performed_by: string;
  details: string;
  created_at: string;
  tenant_id?: string;
}