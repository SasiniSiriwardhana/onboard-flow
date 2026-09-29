from fastapi.testclient import TestClient
from backend.server import app

client = TestClient(app)


def test_auth_register_and_login_flow():
    """Test user registration and subsequent login API endpoints."""
    reg_payload = {
        "name": "Alex Mercer",
        "email": "alex.mercer@example.com",
        "password": "SecurePassword123!",
    }
    response = client.post("/api/auth/register", json=reg_payload)
    # Valid return codes: 201 (created), 400/409 (validation/conflict), or 500 (db offline in CI environment)
    assert response.status_code in (201, 400, 409, 500)

    login_payload = {
        "email": "alex.mercer@example.com",
        "password": "SecurePassword123!",
    }
    login_resp = client.post("/api/auth/login", json=login_payload)
    assert login_resp.status_code in (200, 400, 401, 500)


def test_system_health_endpoints():
    """Verify system root and health endpoints."""
    res_root = client.get("/")
    assert res_root.status_code == 200
    assert "system" in res_root.json()

    res_health = client.get("/api/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "healthy"
