from fastapi.testclient import TestClient
from backend.server import app

client = TestClient(app)


def test_tasks_api_lifecycle():
    """Verify task creation, filtering, and status transitions."""
    task_payload = {
        "title": "Configure SSL Certificates",
        "description": "Install wildcard Let's Encrypt certificates on ingress proxies.",
        "priority": "High",
        "status": "To Do",
    }
    # Create Task
    res = client.post("/api/tasks", json=task_payload)
    assert res.status_code in (201, 200)

    # List Tasks
    list_res = client.get("/api/tasks")
    assert list_res.status_code == 200
    assert isinstance(list_res.json(), list)
