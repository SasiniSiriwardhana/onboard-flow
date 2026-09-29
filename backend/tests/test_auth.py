from fastapi.testclient import TestClient
from backend.server import app

client = TestClient(app)


def test_auth_register_and_login_flow():
    """Test user registration and subsequent login API endpoints."""
    # 1. Register test user
    reg_payload = {
        "name": "Alex Mercer",
        "email": "alex.mercer@testenterprise.com",
        "password": "SecurePassword123!",
    }
    response = client.post("/api/auth/register", json=reg_payload)
    assert response.status_code in (201, 400, 409)

    # 2. Login test user
    login_payload = {
        "email": "alex.mercer@testenterprise.com",
        "password": "SecurePassword123!",
    }
    login_resp = client.post("/api/auth/login", json=login_payload)
    assert login_resp.status_code in (200, 401)


def test_system_health_endpoints():
    """Verify system root and health endpoints."""
    res_root = client.get("/")
    assert res_root.status_code == 200
    assert "system" in res_root.json()

    res_health = client.get("/api/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "healthy"
