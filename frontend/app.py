import os
import requests
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Base directory & environment loading
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

# Initialize Flask App
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-onboarding-2026")

# Backend Service Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "5000"))
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")

# Fallback projects memory cache for seamless local UI preview
_LOCAL_PROJECTS = [
    {
        "id": 1,
        "title": "Global FinTech Onboarding",
        "customer_name": "Nexus Bank International",
        "tier": "Enterprise VIP",
        "description": "Multi-region core banking integration and security sign-off.",
        "status": "Data Migration",
        "progress": 68,
        "target_go_live": "2026-10-01",
        "created_at": "2026-09-01",
    },
    {
        "id": 2,
        "title": "Healthcare EHR Cloud Integration",
        "customer_name": "MedLife Health Systems",
        "tier": "Enterprise",
        "description": "HIPAA-compliant patient data migration and webhook setup.",
        "status": "Tech Setup",
        "progress": 42,
        "target_go_live": "2026-10-20",
        "created_at": "2026-09-03",
    },
    {
        "id": 3,
        "title": "Retail Omnichannel Implementation",
        "customer_name": "Nordic Retail Group",
        "tier": "Growth",
        "description": "POS synchronization and multi-warehouse inventory feed.",
        "status": "Kickoff",
        "progress": 15,
        "target_go_live": "2026-11-15",
        "created_at": "2026-09-06",
    },
    {
        "id": 4,
        "title": "Logistics Freight Hub Rollout",
        "customer_name": "Pacific Freight Logistics",
        "tier": "Enterprise",
        "description": "Real-time dispatch API and telemetry stream integration.",
        "status": "Go-Live / Live",
        "progress": 100,
        "target_go_live": "2026-09-05",
        "created_at": "2026-08-15",
    },
]


def fetch_backend_stats():
    """Retrieve stats from FastAPI or calculate from fallback cache."""
    try:
        resp = requests.get(f"{BACKEND_URL}/api/v1/onboarding/stats", timeout=1.5)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass

    total = len(_LOCAL_PROJECTS)
    completed = sum(1 for p in _LOCAL_PROJECTS if p["progress"] == 100)
    in_progress = sum(1 for p in _LOCAL_PROJECTS if 0 < p["progress"] < 100)
    kickoff = sum(1 for p in _LOCAL_PROJECTS if p["progress"] <= 15)
    return {
        "total_projects": total,
        "active_onboardings": in_progress,
        "completed": completed,
        "kickoff_stage": kickoff,
        "average_progress": round(sum(p["progress"] for p in _LOCAL_PROJECTS) / total if total else 0, 1),
    }


def fetch_backend_projects():
    """Retrieve projects list from FastAPI or local fallback."""
    try:
        resp = requests.get(f"{BACKEND_URL}/api/v1/onboarding/projects", timeout=1.5)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return _LOCAL_PROJECTS


def fetch_db_status():
    """Check Oracle DB status via backend health endpoint."""
    try:
        resp = requests.get(f"{BACKEND_URL}/api/db/health", timeout=1.5)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return {
        "status": "ready",
        "host": os.getenv("ORACLE_HOST", "localhost"),
        "port": 1521,
        "service_name": os.getenv("ORACLE_SERVICE_NAME", "xe"),
    }


@app.context_processor
def inject_global_vars():
    """Inject global context into all templates."""
    return {
        "backend_url": BACKEND_URL,
        "db_status": fetch_db_status(),
    }


@app.route("/")
def index():
    """SaaS Customer Onboarding Dashboard."""
    stats = fetch_backend_stats()
    projects = fetch_backend_projects()
    return render_template("index.html", stats=stats, projects=projects)


@app.route("/projects")
def projects_page():
    """All Customer Projects List page."""
    projects = fetch_backend_projects()
    return render_template("projects.html", projects=projects)


@app.route("/api/htmx/projects", methods=["GET"])
def htmx_filter_projects():
    """HTMX endpoint for filtering and searching projects."""
    query = request.args.get("q", "").strip().lower()
    all_projects = fetch_backend_projects()

    if query:
        filtered = [
            p for p in all_projects
            if query in p["title"].lower() or query in p["customer_name"].lower() or query in p.get("tier", "").lower()
        ]
    else:
        filtered = all_projects

    if not filtered:
        return '<tr><td colspan="6" class="text-center py-6 text-gray-400 text-xs">No matching onboarding projects found.</td></tr>'

    output = ""
    for project in filtered:
        output += render_template("components/project_row.html", project=project)
    return output


@app.route("/api/htmx/projects/quick-add", methods=["POST"])
def htmx_quick_add():
    """HTMX endpoint to add a new project and return rendered HTML row."""
    title = request.form.get("title", "").strip()
    customer_name = request.form.get("customer_name", "").strip()
    tier = request.form.get("tier", "Enterprise")
    target_go_live = request.form.get("target_go_live", "")
    description = request.form.get("description", "")

    new_id = max((p["id"] for p in _LOCAL_PROJECTS), default=0) + 1
    new_project = {
        "id": new_id,
        "title": title or f"Implementation #{new_id}",
        "customer_name": customer_name or "New Client",
        "tier": tier,
        "description": description,
        "status": "Kickoff",
        "progress": 10,
        "target_go_live": target_go_live or "TBD",
        "created_at": "Today",
    }
    _LOCAL_PROJECTS.insert(0, new_project)

    # Also notify FastAPI backend if reachable
    try:
        requests.post(
            f"{BACKEND_URL}/api/v1/onboarding/projects",
            json={
                "title": new_project["title"],
                "customer_name": new_project["customer_name"],
                "tier": new_project["tier"],
                "target_go_live": new_project["target_go_live"],
                "description": new_project["description"],
            },
            timeout=1.0,
        )
    except Exception:
        pass

    return render_template("components/project_row.html", project=new_project)


@app.route("/api/htmx/projects/<int:project_id>/advance", methods=["POST"])
def htmx_advance_project(project_id: int):
    """HTMX endpoint to advance a project's implementation stage and progress."""
    project = next((p for p in _LOCAL_PROJECTS if p["id"] == project_id), None)
    if not project:
        # Generate dummy project if not in list
        project = {
            "id": project_id,
            "title": f"Onboarding Project #{project_id}",
            "customer_name": "Enterprise Client",
            "tier": "Enterprise",
            "status": "Kickoff",
            "progress": 20,
            "target_go_live": "TBD",
        }
        _LOCAL_PROJECTS.append(project)

    # Stage transitions
    stages = [
        ("Kickoff", 15),
        ("Tech Setup", 40),
        ("Data Migration", 65),
        ("Customer UAT", 85),
        ("Go-Live / Live", 100),
    ]

    current_progress = project.get("progress", 0)
    for stage_name, stage_prog in stages:
        if stage_prog > current_progress:
            project["status"] = stage_name
            project["progress"] = stage_prog
            break
    else:
        project["status"] = "Completed"
        project["progress"] = 100

    return render_template("components/project_row.html", project=project)


if __name__ == "__main__":
    print(f"Starting Flask Frontend on http://localhost:{FRONTEND_PORT}")
    app.run(host="0.0.0.0", port=FRONTEND_PORT, debug=DEBUG)
