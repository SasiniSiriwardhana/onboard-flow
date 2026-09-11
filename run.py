"""
Runner Script for Project Onboarding System
Starts the FastAPI Backend Service on port 8000 with auto-reload and OpenAPI docs.
"""

import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

def start_backend():
    print("=" * 60)
    print("  Customer Onboarding System - FastAPI Backend")
    print("=" * 60)
    print("  [API Service]    FastAPI:    http://localhost:8000")
    print("  [Interactive API] Swagger UI: http://localhost:8000/docs")
    print("  [Alternative Docs] ReDoc:     http://localhost:8000/redoc")
    print("  [Oracle Database] XE Port:    localhost:1521 / xe")
    print("=" * 60)
    print("Press Ctrl+C to terminate server.\n")

    backend_cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "backend.server:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
        "--reload",
    ]

    try:
        proc = subprocess.Popen(backend_cmd, cwd=str(ROOT_DIR))
        proc.wait()
    except KeyboardInterrupt:
        print("\nGracefully stopping backend service...")
        if proc:
            proc.terminate()
        print("Done.")

def start_frontend():
    print("=" * 60)
    print("  Customer Onboarding System - Flask Frontend")
    print("=" * 60)
    print("  [Web App]        Portal:     http://localhost:5000")
    print("  [Login Page]     Sign In:    http://localhost:5000/login")
    print("  [Register Page]  Sign Up:    http://localhost:5000/register")
    print("  [Dashboard]      Protected:  http://localhost:5000/dashboard")
    print("=" * 60)
    print("Press Ctrl+C to terminate server.\n")

    frontend_cmd = [
        sys.executable,
        "-m",
        "frontend.app",
    ]

    try:
        proc = subprocess.Popen(frontend_cmd, cwd=str(ROOT_DIR))
        proc.wait()
    except KeyboardInterrupt:
        print("\nGracefully stopping frontend service...")
        if proc:
            proc.terminate()
        print("Done.")


def start_all():
    print("=" * 60)
    print("  Customer Onboarding System - Full Stack Services")
    print("=" * 60)
    print("  [Frontend]       Portal:     http://localhost:5000")
    print("  [API Service]    FastAPI:    http://localhost:8000")
    print("  [Swagger Docs]   API Docs:   http://localhost:8000/docs")
    print("=" * 60)
    print("Press Ctrl+C to terminate both servers.\n")

    backend_cmd = [sys.executable, "-m", "uvicorn", "backend.server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    frontend_cmd = [sys.executable, "-m", "frontend.app"]

    procs = []
    try:
        procs.append(subprocess.Popen(backend_cmd, cwd=str(ROOT_DIR)))
        procs.append(subprocess.Popen(frontend_cmd, cwd=str(ROOT_DIR)))
        for p in procs:
            p.wait()
    except KeyboardInterrupt:
        print("\nShutting down all services...")
        for p in procs:
            p.terminate()
        print("All services stopped.")


if __name__ == "__main__":
    if "--frontend" in sys.argv:
        start_frontend()
    elif "--all" in sys.argv:
        start_all()
    else:
        start_backend()

