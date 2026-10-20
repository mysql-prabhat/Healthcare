import api from "../api/axios";
import type { Document } from "../types/document";


class DocumentService {
  async getDocuments(): Promise<Document[]> {
    const response = await api.get<Document[]>(
      "/documents/documents"
    );

    return response.data;
  }

  async uploadDocument(title: string,  patientId: string, file: File): Promise<Document> {
    const formData = new FormData();

    formData.append(
      "title",
      title
    );
    formData.append(
      "patient_id",
      patientId
    );
    formData.append(
      "file",
      file
    );
    const response = await api.post(
      "/documents/upload",
      formData
    );

    return response.data;
  }
}

export default new DocumentService();