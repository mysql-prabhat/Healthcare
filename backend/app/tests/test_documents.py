from types import SimpleNamespace

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from redis.exceptions import RedisError

from app.api.v1 import documents
from app.core.auth import get_current_user
from app.core.db import get_db
from app.core.models import Document, Patient


class FakeQuery:
    def __init__(self, session, model, patient, document, documents):
        self.session = session
        self.model = model
        self.patient = patient
        self.document = document
        self.documents = documents

    def filter(self, *criteria):
        self.session.filters.append(criteria)
        return self

    def join(self, *args):
        return self

    def first(self):
        if self.model is Patient:
            return self.patient
        return self.document

    def all(self):
        return self.documents


class FakeSession:
    def __init__(
        self,
        *,
        patient=None,
        document=None,
        documents=None,
    ):
        self.patient = patient
        self.document = document
        self.documents = documents or []
        self.added = []
        self.commit_count = 0
        self.next_id = 101
        self.filters = []

    def query(self, model):
        return FakeQuery(
            self,
            model,
            self.patient,
            self.document,
            self.documents,
        )

    def add(self, instance):
        self.added.append(instance)

    def commit(self):
        self.commit_count += 1

    def refresh(self, instance):
        instance.id = self.next_id
        self.next_id += 1


@pytest.fixture
def patient():
    return Patient(
        id=7,
        patient_id="patient-123",
        tenant_id="tenant-1",
    )


@pytest.fixture
def client(monkeypatch, tmp_path):
    monkeypatch.setattr(documents, "UPLOAD_DIR", str(tmp_path))
    session = FakeSession()
    app = FastAPI()
    app.include_router(documents.router)
    app.dependency_overrides[get_db] = lambda: session
    app.dependency_overrides[get_current_user] = lambda: {
        "tenant_id": "tenant-1",
    }

    with TestClient(app) as test_client:
        yield test_client, session

    app.dependency_overrides.clear()


def test_create_document_persists_document_fields(client):
    test_client, session = client

    response = test_client.post(
        "/v1/documents/documents",
        json={
            "title": "Visit notes",
            "file_name": "visit.txt",
            "file_type": "text/plain",
            "file_path": "uploads/visit.txt",
        },
    )

    assert response.status_code == 200
    document = session.added[0]
    assert isinstance(document, Document)
    assert document.id == 101
    assert document.title == "Visit notes"
    assert document.file_name == "visit.txt"
    assert document.file_type == "text/plain"
    assert document.file_path == "uploads/visit.txt"
    assert document.tenant_id == "tenant-1"
    assert document.status == "PENDING"
    assert session.commit_count == 1


def test_create_document_allows_optional_file_fields_to_be_omitted(client):
    test_client, session = client

    response = test_client.post(
        "/v1/documents/documents",
        json={"title": "Visit notes"},
    )

    assert response.status_code == 200
    document = session.added[0]
    assert document.title == "Visit notes"
    assert document.file_name is None
    assert document.file_type is None
    assert document.file_path is None


def test_create_document_requires_title(client):
    test_client, session = client

    response = test_client.post(
        "/v1/documents/documents",
        json={"file_name": "visit.txt"},
    )

    assert response.status_code == 422
    assert session.added == []


def test_get_documents_returns_tenant_documents(client):
    test_client, session = client
    session.documents = [
        Document(
            id=4,
            title="Visit notes",
            status="PENDING_REVIEW",
            file_name="visit.txt",
            file_type="text/plain",
            file_path="uploads/visit.txt",
        )
    ]

    response = test_client.get("/v1/documents/documents")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 4,
            "title": "Visit notes",
            "patient_name": None,
            "summary": None,
            "status": "PENDING_REVIEW",
            "file_name": "visit.txt",
            "file_type": "text/plain",
            "file_path": "uploads/visit.txt",
            "created_at": None,
        }
    ]


def test_get_documents_returns_empty_list_when_no_documents_exist(client):
    test_client, _ = client

    response = test_client.get("/v1/documents/documents")

    assert response.status_code == 200
    assert response.json() == []


def test_upload_saves_document_and_enqueues_processing(
    client,
    patient,
    monkeypatch,
):
    test_client, session = client
    session.patient = patient
    job = SimpleNamespace(id="job-123")
    enqueue_calls = []

    def enqueue(*args):
        enqueue_calls.append(args)
        return job

    monkeypatch.setattr(documents.document_queue, "enqueue", enqueue)

    response = test_client.post(
        "/v1/documents/upload",
        data={
            "title": "Visit notes",
            "patient_id": "patient-123",
        },
        files={
            "file": ("visit notes.txt", b"Clinical notes", "text/plain"),
        },
    )

    assert response.status_code == 200
    body = response.json()
    document = session.added[0]
    assert body == {
        "id": 101,
        "title": "Visit notes",
        "file_name": "visit notes.txt",
        "file_type": "text/plain",
        "status": "PROCESSING",
        "tenant_id": "tenant-1",
        "job_id": "job-123",
    }
    assert document.patient_id == patient.id
    assert document.file_path.endswith("_visit_notes.txt")
    assert document.retry_count == 0
    assert session.commit_count == 1
    assert enqueue_calls == [
        ("app.workers.document_worker.process_document", 101)
    ]
    patient_filter = session.filters[0]
    assert [
        (criterion.left.key, criterion.right.value)
        for criterion in patient_filter
    ] == [
        ("patient_id", "patient-123"),
        ("tenant_id", "tenant-1"),
    ]
    with open(document.file_path, "rb") as uploaded_file:
        assert uploaded_file.read() == b"Clinical notes"


@pytest.mark.parametrize(
    "content_type",
    [
        "application/pdf",
        "application/json",
        (
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        ),
    ],
)
def test_upload_accepts_other_allowed_content_types(
    client,
    patient,
    monkeypatch,
    content_type,
):
    test_client, session = client
    session.patient = patient

    def enqueue(*args):
        return SimpleNamespace(id="job-allowed")

    monkeypatch.setattr(documents.document_queue, "enqueue", enqueue)

    response = test_client.post(
        "/v1/documents/upload",
        data={
            "title": "Clinical document",
            "patient_id": "patient-123",
        },
        files={
            "file": ("document", b"content", content_type),
        },
    )

    assert response.status_code == 200
    assert response.json()["file_type"] == content_type
    assert session.added[0].file_type == content_type


@pytest.mark.parametrize(
    "form_data,files",
    [
        (
            {"patient_id": "patient-123"},
            {"file": ("visit.txt", b"notes", "text/plain")},
        ),
        (
            {"title": "Visit notes"},
            {"file": ("visit.txt", b"notes", "text/plain")},
        ),
        (
            {"title": "Visit notes", "patient_id": "patient-123"},
            {},
        ),
    ],
)
def test_upload_requires_all_form_fields(client, form_data, files):
    test_client, session = client

    response = test_client.post(
        "/v1/documents/upload",
        data=form_data,
        files=files,
    )

    assert response.status_code == 422
    assert session.added == []


def test_upload_rejects_unsupported_file_type(client):
    test_client, session = client

    response = test_client.post(
        "/v1/documents/upload",
        data={
            "title": "Executable",
            "patient_id": "patient-123",
        },
        files={
            "file": ("malware.exe", b"content", "application/octet-stream"),
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid file type"
    assert session.added == []
    assert session.commit_count == 0


def test_upload_returns_404_when_patient_is_not_found(client):
    test_client, session = client

    response = test_client.post(
        "/v1/documents/upload",
        data={
            "title": "Visit notes",
            "patient_id": "missing-patient",
        },
        files={
            "file": ("visit.txt", b"Clinical notes", "text/plain"),
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Patient not found"
    assert session.added == []
    assert session.commit_count == 0


def test_upload_marks_document_failed_when_queue_is_unavailable(
    client,
    patient,
    monkeypatch,
):
    test_client, session = client
    session.patient = patient

    def fail_enqueue(*args):
        raise RedisError("Redis unavailable")

    monkeypatch.setattr(
        documents.document_queue,
        "enqueue",
        fail_enqueue,
    )

    response = test_client.post(
        "/v1/documents/upload",
        data={
            "title": "Visit notes",
            "patient_id": "patient-123",
        },
        files={
            "file": ("visit.txt", b"Clinical notes", "text/plain"),
        },
    )

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Document processing queue is unavailable"
    )
    assert session.added[0].status == "FAILED"
    assert session.added[0].processing_error == "Redis unavailable"
    assert session.commit_count == 2


def test_download_returns_file_contents(client, tmp_path):
    test_client, session = client
    file_path = tmp_path / "visit.txt"
    file_path.write_bytes(b"Clinical notes")
    session.document = Document(
        id=23,
        title="Visit notes",
        file_name="visit.txt",
        file_path=str(file_path),
    )

    response = test_client.get("/v1/documents/23/download")

    assert response.status_code == 200
    assert response.content == b"Clinical notes"
    assert response.headers["content-disposition"] == (
        'attachment; filename="visit.txt"'
    )


def test_download_returns_404_for_unknown_document(client):
    test_client, _ = client

    response = test_client.get("/v1/documents/999/download")

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"
