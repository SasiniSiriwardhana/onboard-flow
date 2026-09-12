"""Automated unit and integration test suite for Client Onboarding backend endpoints (Phase 4)."""
import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.database import Base, get_db
from backend.server import app
from backend.routers.clients import DEFAULT_ONBOARDING_TASKS

# In-memory SQLite database engine for test suite
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Create all database tables in test database
Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


class TestClientOnboarding(unittest.TestCase):
    def test_01_register_client_success(self):
        """Verify registering a new client creates client, auto-generates project and default tasks."""
        payload = {
            "company_name": "Acme Innovations Ltd",
            "contact_person": "Sarah Connor",
            "email": "sarah@acmeinnovations.com",
            "phone": "+1-555-0199",
            "address": "100 Tech Blvd, Silicon Valley, CA",
            "status": "Active",
            "initial_project_name": "Acme Core Migration",
        }
        response = client.post("/api/clients", json=payload)
        self.assertEqual(response.status_code, 201, response.text)
        data = response.json()
        self.assertIsNotNone(data["id"])
        self.assertEqual(data["company_name"], "Acme Innovations Ltd")
        self.assertEqual(data["email"], "sarah@acmeinnovations.com")
        self.assertEqual(len(data["projects"]), 1)

        project = data["projects"][0]
        self.assertEqual(project["name"], "Acme Core Migration")
        self.assertEqual(project["status"], "Kickoff")
        self.assertEqual(project["progress"], 5)
        self.assertEqual(project["tasks"], DEFAULT_ONBOARDING_TASKS)

    def test_02_register_client_duplicate_email(self):
        """Verify duplicate client registration returns 409 Conflict."""
        payload = {
            "company_name": "Duplicate Corp",
            "contact_person": "John Doe",
            "email": "sarah@acmeinnovations.com",  # Already registered
        }
        response = client.post("/api/clients", json=payload)
        self.assertEqual(response.status_code, 409)
        self.assertIn("already exists", response.json()["detail"])

    def test_03_list_clients(self):
        """Verify listing clients returns all registered clients."""
        response = client.get("/api/clients")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) >= 1)
        self.assertTrue(any(c["company_name"] == "Acme Innovations Ltd" for c in data))

    def test_04_get_client_by_id_found(self):
        """Verify fetching client by ID returns client and associated projects."""
        list_res = client.get("/api/clients")
        first_client_id = list_res.json()[0]["id"]

        response = client.get(f"/api/clients/{first_client_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], first_client_id)
        self.assertTrue(len(data["projects"]) >= 1)

    def test_05_get_client_by_id_not_found(self):
        """Verify non-existent client ID returns 404."""
        response = client.get("/api/clients/999999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("was not found", response.json()["detail"])

    def test_06_update_client(self):
        """Verify updating client information."""
        list_res = client.get("/api/clients")
        first_client_id = list_res.json()[0]["id"]

        update_payload = {
            "phone": "+1-555-9999",
            "status": "Onboarding",
        }
        response = client.put(f"/api/clients/{first_client_id}", json=update_payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["phone"], "+1-555-9999")
        self.assertEqual(data["status"], "Onboarding")


if __name__ == "__main__":
    unittest.main()
