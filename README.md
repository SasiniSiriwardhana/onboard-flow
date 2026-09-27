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
### Authentication Endpoints:
| Method | Path | Description |
| :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Register new user with bcrypt password hashing |
| `POST` | `/api/auth/login` | Authenticate user and issue JWT Bearer access token |
| `GET` | `/api/auth/me` | Protected route returning current active user profile |

---

## 🎨 Frontend Architecture (Phase 3: User Authentication)

The frontend is built using **Flask Templates (Jinja2)** styled with **Tailwind CSS + DaisyUI**, powered by **HTMX** for smooth single-page-like interactivity, and **Alpine.js** for reactive client state.

### Frontend Tech Stack:
- **Framework**: Flask 3.x
- **Styling**: Tailwind CSS & DaisyUI (modern responsive SaaS layout)
- **Dynamic Interaction**: HTMX (SPA-like form submission without full reload, real-time validations)
- **Client State**: Alpine.js (reactive user profile, badge initials, and session management)
- **JWT Storage**: Stored in `localStorage`, automatically attached as `Authorization: Bearer <token>` via HTMX request interceptor.

### Frontend Routes:
| Route | Method | Description | Phase |
| :--- | :--- | :--- | :---: |
| `/login` | `GET` | User login page with interactive DaisyUI form | Phase 3 |
| `/auth/login` | `POST` | HTMX proxy endpoint to backend `/api/auth/login` with JWT event trigger | Phase 3 |
| `/register` | `GET` | User registration page | Phase 3 |
| `/auth/register` | `POST` | HTMX proxy endpoint to backend `/api/auth/register` | Phase 3 |
| `/auth/validate-email` | `POST` | Real-time live email format check via HTMX | Phase 3 |
| `/dashboard` | `GET` | Protected Customer Onboarding Dashboard with Auth Guard & Logout | Phase 3 |
| `/onboarding` | `GET` | 3-step Client Onboarding Registration form with DaisyUI controls | Phase 5 |
| `/onboarding/check-company` | `POST` | Live debounced corporate name validator via HTMX | Phase 5 |
| `/onboarding/submit` | `POST` | HTMX proxy endpoint registering client & auto-provisioning project | Phase 5 |
| `/onboarding/list` | `GET` | Full client directory hub with summary stats and HTMX partials | Phase 5 |
| `/onboarding/success` | `GET` | Client Onboarding Success Confirmation and Project Milestone roadmap | Phase 5 |

---

## 🚀 Phase 5: Client Onboarding (Frontend & Backend Services)

Phase 5 delivers the customer-facing and administrator implementation registration engine:
- **3-Step Onboarding Form UI**: Responsive DaisyUI wizard layout with corporate credentials inputs (`company_name`, `contact_person`, `email`, `phone`, `address`, `tier`, `status`).
- **Debounced Real-Time Validation**: Instant inline validation feedback for company duplicate check, email syntax, phone formatting, and dynamic submit button state.
- **Client Directory & Metrics Hub (`/onboarding/list`)**: Full-page directory with quick stats metric cards, filter tags, click-to-copy email helpers, and HTMX dynamic table rows.
- **HTMX Form Submission**: Smooth AJAX submission via `hx-post="/onboarding/submit"` with inline loading spinner indicator and non-blocking validation alerts.
- **Auto-Project Provisioning Feedback**: Real-time integration with backend `POST /api/clients`, immediately initializing default onboarding implementation milestones.
- **Aggregated Statistics API (`GET /api/clients/stats`)**: Backend metrics endpoint returning total counts, active clients, and SLA compliance.
- **Success Confirmation Hub (`frontend/templates/onboarding/success.html`)**: Confirmation page displaying registered client profile, auto-generated project status, printable implementation summary, and one-click return to dashboard.


### Running the Application:
```bash
# Start Backend only (Port 8000)
python run.py

# Start Frontend only (Port 5000)
python run.py --frontend

# Start Both Backend and Frontend concurrently
python run.py --all
```

---

## 🐳 Docker Deployment
```bash
docker-compose up --build
```
- Frontend Portal: `http://localhost:5000`
- API & Docs: `http://localhost:8000/docs`
- Oracle DB Port: `1521`

