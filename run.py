"""
Unified Runner Script for Project Onboarding System
Starts both FastAPI Backend (port 8000) and Flask Frontend (port 5000) concurrently.
"""

import os
import sys
import time
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

def start_services():
    print("=" * 60)
    print("  Customer Onboarding System - Launching Day 1 Stack")
    print("=" * 60)
    print("  [Backend]  FastAPI:  http://localhost:8000 (Swagger: /docs)")
    print("  [Frontend] Flask UI: http://localhost:5000")
    print("  [Database] Oracle DB: localhost:1521 / xe")
    print("=" * 60)
    print("Press Ctrl+C to terminate both servers.\n")

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

    frontend_cmd = [
        sys.executable,
        "frontend/app.py",
    ]

    backend_proc = None
    frontend_proc = None

    try:
        backend_proc = subprocess.Popen(backend_cmd, cwd=str(ROOT_DIR))
        time.sleep(1)
        frontend_proc = subprocess.Popen(frontend_cmd, cwd=str(ROOT_DIR))

        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\nGracefully shutting down services...")
        if backend_proc:
            backend_proc.terminate()
        if frontend_proc:
            frontend_proc.terminate()
        print("Done.")

if __name__ == "__main__":
    start_services()
