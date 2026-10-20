export interface Document {
  id: number;
  title: string;
  patient_name: string | null;
  summary: string | null;
  status: string;
  tenantId: string;
  file_name: string | null;
  file_type: string | null;
  file_path: string | null;
  created_at: string | null;
}

export interface UploadDocumentRequest {
  title: string;
}