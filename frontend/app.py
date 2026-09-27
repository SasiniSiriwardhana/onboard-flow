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


@app.route("/onboarding")
def onboarding_page():
    """Render Client Onboarding Registration Form (Phase 5)."""
    return render_template("onboarding/form.html")


@app.route("/onboarding/check-company", methods=["POST"])
def check_company_name():
    """Live HTMX endpoint to validate company name input and check length/syntax in real-time."""
    company_name = request.form.get("company_name", "").strip()
    if not company_name:
        return ""

    if len(company_name) < 2:
        return """<span class="text-xs text-rose-500 font-medium flex items-center gap-1 mt-1">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            Company name must be at least 2 characters
        </span>"""

    return """<span class="text-xs text-emerald-600 font-medium flex items-center gap-1 mt-1">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
        Valid company name
    </span>"""


@app.route("/onboarding/submit", methods=["POST"])
def onboarding_submit():
    """Proxy onboarding form submission from HTMX to FastAPI backend /api/clients."""
    import re
    import urllib.parse
    import requests

    company_name = request.form.get("company_name", "").strip()
    contact_person = request.form.get("contact_person", "").strip()
    email = request.form.get("email", "").strip().lower()
    phone = request.form.get("phone", "").strip()
    address = request.form.get("address", "").strip()
    client_status = request.form.get("status", "Active").strip()
    tier = request.form.get("tier", "Enterprise").strip()

    # 1. Field Validation
    if not company_name or not contact_person or not email:
        return (
            """<div class="alert alert-warning text-sm shadow-md py-3 px-4 mb-4">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
                <span>Please complete all required fields (Company Name, Contact Person, and Email).</span>
            </div>""",
            400,
        )

    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, email):
        return (
            """<div class="alert alert-warning text-sm shadow-md py-3 px-4 mb-4">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
                <span>Please enter a valid corporate email address.</span>
            </div>""",
            400,
        )

    # 2. Prepare payload for FastAPI backend
    payload = {
        "company_name": company_name,
        "contact_person": contact_person,
        "email": email,
        "phone": phone if phone else None,
        "address": address if address else None,
        "status": client_status if client_status else "Active",
        "initial_project_name": f"{company_name} - {tier} Onboarding Implementation",
    }

    # Extract optional auth header
    headers = {}
    auth_header = request.headers.get("Authorization")
    if auth_header:
        headers["Authorization"] = auth_header

    try:
        backend_resp = requests.post(
            f"{BACKEND_URL}/api/clients",
            json=payload,
            headers=headers,
            timeout=5.0,
        )
    except requests.exceptions.RequestException:
        return (
            """<div class="alert alert-error text-sm shadow-md py-3 px-4 mb-4">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                <span>Unable to reach backend service (FastAPI :8000). Please verify the server is running.</span>
            </div>""",
            503,
        )

    # 3. Handle Successful Creation
    if backend_resp.status_code == 201:
        created_client = backend_resp.json()
        client_id = created_client.get("id", "")
        params = {
            "client_id": str(client_id),
            "company_name": company_name,
            "contact_person": contact_person,
            "email": email,
            "phone": phone,
            "address": address,
        }
        query_str = urllib.parse.urlencode(params)
        redirect_url = f"/onboarding/success?{query_str}"

        # Respond with HX-Redirect header for smooth HTMX client-side redirection
        response = app.response_class(
            response=f"""<div class="alert alert-success text-sm shadow-md py-3 px-4 mb-4">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                <span>Onboarding registered successfully! Redirecting to confirmation...</span>
            </div>""",
            status=200,
            mimetype="text/html",
        )
        response.headers["HX-Redirect"] = redirect_url
        return response

    # 4. Handle Conflict (e.g. Duplicate Email)
    if backend_resp.status_code == 409:
        return (
            f"""<div class="alert alert-warning text-sm shadow-md py-3 px-4 mb-4">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
                <span>A client with corporate email <strong>{email}</strong> is already registered in the system.</span>
            </div>""",
            409,
        )

    # 5. Handle General Errors
    error_msg = "Failed to register client onboarding. Please review details."
    try:
        err_data = backend_resp.json()
        if "detail" in err_data:
            error_msg = err_data["detail"]
    except Exception:
        pass

    return (
        f"""<div class="alert alert-error text-sm shadow-md py-3 px-4 mb-4">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            <span>{error_msg}</span>
        </div>""",
        backend_resp.status_code,
    )


@app.route("/onboarding/success")
def onboarding_success():
    """Render Client Onboarding Success Confirmation Page."""
    import requests

    client_id = request.args.get("client_id")
    company_name = request.args.get("company_name", "Valued Client")
    contact_person = request.args.get("contact_person", "")
    email = request.args.get("email", "")
    phone = request.args.get("phone", "")
    address = request.args.get("address", "")

    client_obj = {
        "id": client_id,
        "company_name": company_name,
        "contact_person": contact_person,
        "email": email,
        "phone": phone,
        "address": address,
    }

    # Optionally fetch freshest client record from backend if client_id is available
    if client_id:
        try:
            resp = requests.get(f"{BACKEND_URL}/api/clients/{client_id}", timeout=2.0)
            if resp.status_code == 200:
                client_obj = resp.json()
        except Exception:
            pass

    return render_template(
        "onboarding/success.html",
        client=client_obj,
        company_name=company_name,
        contact_person=contact_person,
        email=email,
        phone=phone,
        address=address,
    )


@app.route("/onboarding/list", methods=["GET"])
def onboarding_list():
    """List all registered clients, supporting full page, HTMX partials, and JSON."""
    import requests
    from flask import jsonify

    status_filter = request.args.get("status")
    search_query = request.args.get("search")

    params = {}
    if status_filter:
        params["status"] = status_filter
    if search_query:
        params["search"] = search_query

    clients = []
    backend_error = None
    try:
        resp = requests.get(f"{BACKEND_URL}/api/clients", params=params, timeout=3.0)
        if resp.status_code == 200:
            clients = resp.json()
        else:
            backend_error = f"Backend returned HTTP {resp.status_code}"
    except requests.exceptions.RequestException:
        backend_error = "Unable to connect to backend service (:8000)."

    # Support JSON response format
    if (
        request.is_json
        or request.headers.get("Accept") == "application/json"
        or request.args.get("format") == "json"
    ):
        return jsonify(clients)

    # HTMX partial table rows render
    if request.headers.get("HX-Request"):
        return render_template(
            "onboarding/list_partial.html",
            clients=clients,
            backend_error=backend_error,
        )

    # Standard browser full page render
    return render_template(
        "onboarding/list.html",
        clients=clients,
        backend_error=backend_error,
    )


if __name__ == "__main__":
    print(f"Starting OnboardFlow Frontend on http://localhost:{FRONTEND_PORT}")
    app.run(host="0.0.0.0", port=FRONTEND_PORT, debug=DEBUG)
