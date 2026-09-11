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


@app.route("/register")
def register_page():
    """Render User Registration Page."""
    return render_template("auth/register.html")


@app.route("/dashboard")
def dashboard():
    """Render Protected Customer Onboarding Dashboard."""
    return render_template("dashboard.html")


if __name__ == "__main__":
    print(f"Starting OnboardFlow Frontend on http://localhost:{FRONTEND_PORT}")
    app.run(host="0.0.0.0", port=FRONTEND_PORT, debug=DEBUG)
