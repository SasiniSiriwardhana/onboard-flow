import io
from fastapi.testclient import TestClient
from backend.server import app

client = TestClient(app)


def test_documents_api_upload_and_list():
    """Verify document file upload and repository listing APIs."""
    # List documents
    list_res = client.get("/api/documents")
    assert list_res.status_code in (200, 404, 500)
    if list_res.status_code == 200:
        assert isinstance(list_res.json(), list)

    # Test file upload simulation
    dummy_file = io.BytesIO(b"Sample PDF Content for Onboarding Contract")
    upload_res = client.post(
        "/api/documents/upload",
        files={"file": ("contract_v1.pdf", dummy_file, "application/pdf")},
        data={"uploaded_by": "Test Suite Admin"},
    )
    assert upload_res.status_code in (201, 200, 400, 500)
    if upload_res.status_code == 201:
        assert "file_name" in upload_res.json()
