# Project Onboarding System

A modern **Customer Onboarding & Implementation SaaS REST API Platform** engineered with **FastAPI** (Python 3.11) and **Oracle Database** (SQLAlchemy 2.0 ORM + `python-oracledb` in Thin Mode).

> **Note**: This repository is a **100% Pure Backend REST API Platform** with zero HTML templates or markup files. All endpoints are fully documented, interactive, and testable via OpenAPI Swagger UI (`/docs`).

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11, FastAPI, Uvicorn, Pydantic v2
- **Database**: Oracle DB (SQLAlchemy 2.0 ORM + `python-oracledb` Thin Mode)
- **API Documentation**: Interactive OpenAPI Swagger UI & ReDoc
- **Containerization**: Docker + Docker Compose

---

## 📁 Project Structure

```text
project-onboarding-system/
├── backend/                  # FastAPI Application
│   ├── models/               # SQLAlchemy ORM Models (Customer, OnboardingProject)
│   ├── schemas/              # Pydantic Request/Response Schemas
│   ├── config.py             # Environment & App Settings
│   ├── database.py           # Oracle DB Engine, Connection Pool & Diagnostics
│   └── server.py             # FastAPI App & REST API Endpoints
├── docker/                   # Docker Configuration
│   └── Dockerfile.backend    # FastAPI Containerfile
├── .env                      # Local Configuration (excluded from git)
├── .env.example              # Environment Configuration Template
├── .gitignore                # Git Exclusions
├── docker-compose.yml        # Multi-container Compose Spec (Backend + Oracle DB)
├── requirements.txt          # Python Dependencies
├── run.py                    # Local Backend Runner Script
└── README.md                 # Project Documentation
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.11+
- Oracle Database (Local XE or Docker)
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

### 4. Running the Backend Service
```bash
python run.py
```
Or with Uvicorn:
```bash
uvicorn backend.server:app --host 0.0.0.0 --port 8000 --reload
```

---

## 📖 API Documentation & Testing

Once running, access the interactive API explorer:
- **Interactive Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Key Endpoints:
| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/` | API root metadata and system status |
| `GET` | `/api/health` | System health check and uptime status |
| `GET` | `/api/db/health` | Live Oracle DB connection latency check (`DUAL` test) |
| `GET` | `/api/v1/onboarding/stats` | Aggregated onboarding pipeline KPI metrics |
| `GET` | `/api/v1/onboarding/projects` | List customer onboarding implementation projects |
| `POST` | `/api/v1/onboarding/projects` | Create a new customer onboarding project |

---

## 🐳 Docker Deployment
```bash
docker-compose up --build
```
- API & Docs: `http://localhost:8000/docs`
- Oracle DB Port: `1521`
