# Project Onboarding System

A modern **Customer Onboarding & Implementation SaaS platform** engineered with FastAPI, Oracle DB (SQLAlchemy + oracledb), and a dynamic Flask frontend powered by Tailwind CSS, DaisyUI, HTMX, and Alpine.js.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11, FastAPI, Uvicorn, Pydantic v2
- **Database**: Oracle DB (SQLAlchemy 2.0 ORM + `python-oracledb` in Thin Mode)
- **Frontend**: Flask Templates (Jinja2) + Tailwind CSS + DaisyUI + HTMX + Alpine.js
- **Containerization**: Docker + Docker Compose

---

## 📁 Project Structure

```text
project-onboarding-system/
├── backend/                  # FastAPI Application
│   ├── models/               # SQLAlchemy ORM Models
│   ├── schemas/              # Pydantic Schemas
│   ├── config.py             # Environment & App Settings
│   ├── database.py           # Oracle DB Engine & Session Management
│   └── server.py             # FastAPI App & API Endpoints
├── frontend/                 # Flask UI & Templates
│   ├── static/               # CSS, JS, and Static Assets
│   ├── templates/            # Jinja2 HTML Templates
│   │   └── components/       # DaisyUI & HTMX Partial Components
│   └── app.py                # Flask Web Server
├── docker/                   # Dockerfiles
│   ├── Dockerfile.backend    # FastAPI Containerfile
│   └── Dockerfile.frontend   # Flask Containerfile
├── .env                      # Local Configuration (excluded from git)
├── .env.example              # Environment Configuration Template
├── .gitignore                # Git Exclusions
├── docker-compose.yml        # Multi-container Compose Spec
├── requirements.txt          # Python Dependencies
├── run.py                    # Unified Local Runner Script
└── README.md                 # Project Documentation
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.11+
- Oracle Database (local instance or Docker)
- Git

### 2. Environment Setup
```bash
# Clone the repository and copy environment config
cp .env.example .env

# Create and activate a Python virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Oracle DB Configuration
Update `.env` with your Oracle connection credentials:
```env
ORACLE_USER=system
ORACLE_PASSWORD=mypassword
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=xe
```

### 4. Running the Application Locally
Run both Backend and Frontend concurrently with the helper script:
```bash
python run.py
```
Or run individually:
- **FastAPI Backend**:
  ```bash
  uvicorn backend.server:app --host 0.0.0.0 --port 8000 --reload
  ```
  Swagger Docs available at: `http://localhost:8000/docs`
- **Flask Frontend**:
  ```bash
  python frontend/app.py
  ```
  Dashboard UI available at: `http://localhost:5000`

---

## 🐳 Docker Deployment
```bash
docker-compose up --build
```
- Frontend UI: `http://localhost:5000`
- Backend API & Docs: `http://localhost:8000/docs`
- Oracle DB Port: `1521`
