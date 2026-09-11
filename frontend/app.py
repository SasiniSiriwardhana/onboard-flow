import os
from pathlib import Path
from flask import Flask, render_template, redirect, url_for, request
from dotenv import load_dotenv

# Base paths and environment setup
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

# Initialize Flask application
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-onboardflow-2026")

# Backend Service Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "5000"))
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")


@app.context_processor
def inject_globals():
    """Inject global template variables."""
    return {
        "app_name": "OnboardFlow",
        "backend_url": BACKEND_URL,
    }


@app.route("/")
def index():
    """Root route redirecting to login or dashboard."""
    return redirect(url_for("dashboard"))


@app.route("/login")
def login_page():
    """Render User Login Page."""
    return render_template("auth/login.html")


@app.route("/auth/login", methods=["POST"])
def auth_login():
    """Proxy login submission from HTMX to FastAPI backend."""
    import json
    import requests

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        return (
            """<div class="alert alert-warning text-sm shadow-md py-2.5 px-4 mb-4">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
                <span>Please enter both email address and password.</span>
            </div>""",
            400,
        )

    try:
        backend_resp = requests.post(
            f"{BACKEND_URL}/api/auth/login",
            json={"email": email, "password": password},
            timeout=4.0,
        )
    except requests.exceptions.RequestException:
        return (
            """<div class="alert alert-error text-sm shadow-md py-2.5 px-4 mb-4">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                <span>Unable to reach authentication server. Please check backend service.</span>
            </div>""",
            503,
        )

    if backend_resp.status_code == 200:
        data = backend_resp.json()
        token = data.get("access_token")
        user = data.get("user", {})
        trigger_data = json.dumps({"loginSuccess": {"token": token, "user": user}})

        response = app.response_class(
            response="""<div class="alert alert-success text-sm shadow-md py-2.5 px-4 mb-4">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                <span>Authentication successful! Redirecting to dashboard...</span>
            </div>""",
            status=200,
            mimetype="text/html",
        )
        response.headers["HX-Trigger"] = trigger_data
        return response

    # Handle error responses from backend
    error_msg = "Invalid email or password. Please try again."
    try:
        err_json = backend_resp.json()
        if "detail" in err_json:
            error_msg = err_json["detail"]
    except Exception:
        pass

    return (
        f"""<div class="alert alert-error text-sm shadow-md py-2.5 px-4 mb-4">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            <span>{error_msg}</span>
        </div>""",
        backend_resp.status_code,
    )



@app.route("/register")
def register_page():
    """Render User Registration Page."""
    return render_template("auth/register.html")


@app.route("/auth/register", methods=["POST"])
def auth_register():
    """Proxy registration submission from HTMX to FastAPI backend."""
    import json
    import requests

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not name or not email or not password:
        return (
            """<div class="alert alert-warning text-sm shadow-md py-2.5 px-4 mb-4">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
                <span>Please fill in all required fields.</span>
            </div>""",
            400,
        )

    if len(password) < 6:
        return (
            """<div class="alert alert-warning text-sm shadow-md py-2.5 px-4 mb-4">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
                <span>Password must be at least 6 characters long.</span>
            </div>""",
            400,
        )

    if confirm_password and password != confirm_password:
        return (
            """<div class="alert alert-warning text-sm shadow-md py-2.5 px-4 mb-4">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
                <span>Passwords do not match. Please verify both fields.</span>
            </div>""",
            400,
        )

    try:
        backend_resp = requests.post(
            f"{BACKEND_URL}/api/auth/register",
            json={"name": name, "email": email, "password": password},
            timeout=4.0,
        )
    except requests.exceptions.RequestException:
        return (
            """<div class="alert alert-error text-sm shadow-md py-2.5 px-4 mb-4">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                <span>Unable to connect to backend server. Please verify FastAPI is running.</span>
            </div>""",
            503,
        )

    if backend_resp.status_code == 201:
        trigger_data = json.dumps({"registerSuccess": {"email": email, "name": name}})
        response = app.response_class(
            response="""<div class="alert alert-success text-sm shadow-md py-2.5 px-4 mb-4">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                <span>Account created successfully! Redirecting to login page...</span>
            </div>""",
            status=201,
            mimetype="text/html",
        )
        response.headers["HX-Trigger"] = trigger_data
        return response

    error_msg = "Registration failed. Please check the provided information."
    try:
        err_json = backend_resp.json()
        if "detail" in err_json:
            error_msg = err_json["detail"]
    except Exception:
        pass

    return (
        f"""<div class="alert alert-error text-sm shadow-md py-2.5 px-4 mb-4">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            <span>{error_msg}</span>
        </div>""",
        backend_resp.status_code,
    )


@app.route("/auth/validate-email", methods=["POST"])
def validate_email_endpoint():
    """Live HTMX endpoint to validate email format in real-time."""
    import re
    email = request.form.get("email", "").strip().lower()
    if not email:
        return ""

    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, email):
        return """<span class="text-xs text-rose-500 font-medium flex items-center gap-1 mt-1">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            Please enter a valid email address (e.g. user@domain.com)
        </span>"""

    return """<span class="text-xs text-emerald-600 font-medium flex items-center gap-1 mt-1">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
        Valid email format
    </span>"""




@app.route("/dashboard")
def dashboard():
    """Render Protected Customer Onboarding Dashboard."""
    return render_template("dashboard.html")


if __name__ == "__main__":
    print(f"Starting OnboardFlow Frontend on http://localhost:{FRONTEND_PORT}")
    app.run(host="0.0.0.0", port=FRONTEND_PORT, debug=DEBUG)
