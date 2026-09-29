import pytest
from frontend.app import app


@pytest.fixture
def test_client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_frontend_public_routes(test_client):
    """Verify accessibility of UI pages and authentication templates."""
    # Login & Register
    res_login = test_client.get("/login")
    assert res_login.status_code == 200
    assert b"Sign In" in res_login.data or b"Login" in res_login.data

    res_reg = test_client.get("/register")
    assert res_reg.status_code == 200
    assert b"Register" in res_reg.data or b"Account" in res_reg.data

    # Dashboard & Client onboarding
    res_dash = test_client.get("/dashboard")
    assert res_dash.status_code == 200

    res_onboard = test_client.get("/onboarding")
    assert res_onboard.status_code == 200
