"""
Automated Test Suite for Phase 5: Client Onboarding Frontend & Proxy Routes.
Tests Flask templates, HTMX form submissions, validation responses, and success redirection.
"""

import pytest
from unittest.mock import patch, MagicMock
from frontend.app import app


@pytest.fixture
def client():
    """Create Flask test client configured for testing."""
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        yield client


class TestOnboardingFrontend:
    """Test suite covering Client Onboarding frontend interface and proxy routes."""

    def test_01_get_onboarding_form_page(self, client):
        """Verify GET /onboarding renders the registration form with required fields."""
        response = client.get("/onboarding")
        assert response.status_code == 200
        html = response.data.decode("utf-8")
        assert "New Client Onboarding Registration" in html
        assert 'name="company_name"' in html
        assert 'name="contact_person"' in html
        assert 'name="email"' in html
        assert 'name="phone"' in html
        assert 'name="address"' in html
        assert 'hx-post="/onboarding/submit"' in html

    def test_02_submit_onboarding_missing_required_fields(self, client):
        """Verify POST /onboarding/submit rejects submission when required fields are missing."""
        response = client.post(
            "/onboarding/submit",
            data={"company_name": "", "contact_person": "", "email": ""},
        )
        assert response.status_code == 400
        html = response.data.decode("utf-8")
        assert "Please complete all required fields" in html

    def test_03_submit_onboarding_invalid_email_format(self, client):
        """Verify POST /onboarding/submit rejects submission with malformed email."""
        response = client.post(
            "/onboarding/submit",
            data={
                "company_name": "Acme Corp",
                "contact_person": "Jane Doe",
                "email": "invalid-email-address",
            },
        )
        assert response.status_code == 400
        html = response.data.decode("utf-8")
        assert "valid corporate email" in html

    @patch("requests.post")
    def test_04_submit_onboarding_success_with_hx_redirect(self, mock_post, client):
        """Verify successful onboarding proxy submission returns HX-Redirect header."""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": 101,
            "company_name": "Apex Global Solutions",
            "contact_person": "Alex Hunter",
            "email": "alex@apex.com",
            "status": "Active",
            "projects": [{"id": 501, "name": "Apex Global Solutions - Onboarding Implementation"}],
        }
        mock_post.return_value = mock_response

        response = client.post(
            "/onboarding/submit",
            data={
                "company_name": "Apex Global Solutions",
                "contact_person": "Alex Hunter",
                "email": "alex@apex.com",
                "phone": "+1 (555) 345-6789",
                "address": "123 Tech Boulevard",
            },
        )
        assert response.status_code == 200
        assert "HX-Redirect" in response.headers
        assert "/onboarding/success" in response.headers["HX-Redirect"]
        assert "client_id=101" in response.headers["HX-Redirect"]

    @patch("requests.post")
    def test_05_submit_onboarding_duplicate_email_conflict(self, mock_post, client):
        """Verify 409 conflict when client email is already registered."""
        mock_response = MagicMock()
        mock_response.status_code = 409
        mock_response.json.return_value = {
            "detail": "A client with email 'alex@apex.com' already exists."
        }
        mock_post.return_value = mock_response

        response = client.post(
            "/onboarding/submit",
            data={
                "company_name": "Apex Global Duplicate",
                "contact_person": "Alex Hunter",
                "email": "alex@apex.com",
            },
        )
        assert response.status_code == 409
        html = response.data.decode("utf-8")
        assert "already registered" in html

    @patch("requests.post")
    def test_06_submit_onboarding_backend_unreachable(self, mock_post, client):
        """Verify graceful 503 error handling when backend is unreachable."""
        import requests
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")

        response = client.post(
            "/onboarding/submit",
            data={
                "company_name": "Apex Global Offline",
                "contact_person": "Alex Hunter",
                "email": "offline@apex.com",
            },
        )
        assert response.status_code == 503
        html = response.data.decode("utf-8")
        assert "Unable to reach backend service" in html

    def test_07_get_onboarding_success_page(self, client):
        """Verify GET /onboarding/success renders confirmation details and dashboard link."""
        response = client.get(
            "/onboarding/success?client_id=101&company_name=Apex+Global+Solutions&contact_person=Alex+Hunter&email=alex@apex.com"
        )
        assert response.status_code == 200
        html = response.data.decode("utf-8")
        assert "Client Successfully Registered!" in html
        assert "Apex Global Solutions" in html
        assert "Alex Hunter" in html
        assert "alex@apex.com" in html
        assert "Return to Dashboard" in html

    def test_08_get_onboarding_list_page(self, client):
        """Verify GET /onboarding/list renders the clients directory page."""
        response = client.get("/onboarding/list")
        assert response.status_code == 200
        html = response.data.decode("utf-8")
        assert "Registered Onboarding Clients" in html

    @patch("requests.get")
    def test_09_get_onboarding_list_json_format(self, mock_get, client):
        """Verify GET /onboarding/list?format=json returns JSON response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "id": 1,
                "company_name": "Apex Global Solutions",
                "contact_person": "Alex Hunter",
                "email": "alex@apex.com",
                "status": "Active",
                "projects": [],
            }
        ]
        mock_get.return_value = mock_response

        response = client.get("/onboarding/list?format=json")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert data[0]["company_name"] == "Apex Global Solutions"

    def test_10_onboarding_form_has_daisyui_select_fields(self, client):
        """Verify onboarding form renders DaisyUI select components for tier and status."""
        response = client.get("/onboarding")
        assert response.status_code == 200
        html = response.data.decode("utf-8")
        assert 'name="tier"' in html
        assert 'name="status"' in html
        assert "Enterprise VIP" in html
        assert "Enterprise Commercial" in html
        assert "DaisyUI Select" in html
        assert "<select" in html

    @patch("requests.post")
    def test_11_submit_onboarding_with_tier_and_status(self, mock_post, client):
        """Verify POST /onboarding/submit sends tier and status to backend payload."""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": 202,
            "company_name": "Tier Test Corp",
            "contact_person": "Jordan Lee",
            "email": "jordan@tier.com",
            "status": "Active",
            "projects": [],
        }
        mock_post.return_value = mock_response

        response = client.post(
            "/onboarding/submit",
            data={
                "company_name": "Tier Test Corp",
                "contact_person": "Jordan Lee",
                "email": "jordan@tier.com",
                "tier": "Enterprise VIP",
                "status": "Active",
            },
        )
        assert response.status_code == 200
        assert "HX-Redirect" in response.headers
        # Verify the payload was sent with the tier in project name
        call_kwargs = mock_post.call_args
        sent_payload = call_kwargs[1]["json"] if "json" in call_kwargs[1] else call_kwargs[0][1]
        assert "Enterprise VIP" in sent_payload.get("initial_project_name", "")

    def test_12_check_company_name_validation(self, client):
        """Verify POST /onboarding/check-company returns valid/invalid feedback."""
        # Test valid company name
        resp_valid = client.post("/onboarding/check-company", data={"company_name": "Acme Corp"})
        assert resp_valid.status_code == 200
        assert "Valid company name" in resp_valid.data.decode("utf-8")

        # Test short invalid company name
        resp_invalid = client.post("/onboarding/check-company", data={"company_name": "A"})
        assert resp_invalid.status_code == 200
        assert "at least 2 characters" in resp_invalid.data.decode("utf-8")

    def test_13_onboarding_form_renders_wizard_steps(self, client):
        """Verify onboarding form renders multi-step visual wizard progress bar."""
        response = client.get("/onboarding")
        assert response.status_code == 200
        html = response.data.decode("utf-8")
        assert "1. Corporate Profile" in html
        assert "2. Service Tier &amp; SLAs" in html or "2. Service Tier & SLAs" in html
        assert "3. Auto Project Setup" in html
