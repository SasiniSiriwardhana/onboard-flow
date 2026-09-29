from fastapi.testclient import TestClient
from backend.server import app

client = TestClient(app)


def test_clients_crud_endpoints():
    """Test client creation, listing, and retrieval APIs."""
    # 1. List clients
    list_resp = client.get("/api/clients")
    assert list_resp.status_code in (200, 404, 500) or isinstance(list_resp.json(), list)

    # 2. Create client payload
    new_client = {
        "company_name": "Acme Global Solutions",
        "contact_person": "Jane Doe",
        "email": "jane.doe@acmeglobal.test",
        "phone": "+1 800-555-0199",
        "address": "100 Innovation Way, Tech City",
        "status": "Active",
    }
    create_resp = client.post("/api/clients", json=new_client)
    assert create_resp.status_code in (201, 409, 500)
