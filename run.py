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

if __name__ == "__main__":
    start_backend()
