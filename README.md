# 🚀 OnboardFlow - Customer Onboarding & Implementation SaaS Platform

[![CI/CD Pipeline](https://github.com/SasiniSiriwardhana/onboard-flow/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/SasiniSiriwardhana/onboard-flow/actions/workflows/ci-cd.yml)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg?logo=python)](https://python.org)
[![Oracle Database](https://img.shields.io/badge/Database-Oracle%20XE%20Thin%20Mode-F80000.svg?logo=oracle)](https://www.oracle.com/database/)
[![Flask](https://img.shields.io/badge/Frontend-Flask%20Templates-000000.svg?logo=flask)](https://flask.palletsprojects.com/)
[![Tailwind CSS + DaisyUI](https://img.shields.io/badge/Styling-Tailwind%20%2B%20DaisyUI-38B2AC.svg?logo=tailwind-css)](https://daisyui.com/)
[![HTMX + Alpine.js](https://img.shields.io/badge/Reactive-HTMX%20%2B%20Alpine.js-336699.svg)](https://htmx.org/)

OnboardFlow is an enterprise-grade Customer Onboarding & SaaS Implementation Management System designed to accelerate customer time-to-value, automate milestone tracking, streamline multi-party compliance signoffs, and provide real-time executive visibility into project velocity.

---

## 🏛️ System Architecture

```
                                    +-----------------------------------------+
                                    |         User Browser / Client           |
                                    |  (Tailwind CSS + DaisyUI + Alpine.js)   |
                                    +--------------------+--------------------+
                                                         |
                                                  HTMX / Fetch
                                                         |
                                                         v
                                    +-----------------------------------------+
                                    |         Flask Frontend Layer            |
                                    |        (Port 5000 - Jinja SSR)          |
                                    +--------------------+--------------------+
                                                         |
                                                  Async REST API
                                                         |
                                                         v
                                    +-----------------------------------------+
                                    |         FastAPI Backend Engine          |
                                    |       (Port 8000 - Python 3.11)         |
                                    +--------------------+--------------------+
                                                         |
                                               SQLAlchemy ORM + Thin
                                                         |
                                                         v
                                    +-----------------------------------------+
                                    |         Oracle Database (XE)            |
                                    |     (Port 1521 - Relational Engine)     |
                                    +-----------------------------------------+
```

---

## 🌟 Modules & Features Summary

| Phase | Module | Key Features & Endpoints |
|---|---|---|
| **Phase 1-5** | Core Setup & Client Registration | Project scaffold, JWT Auth, Client Onboarding Form (`/api/clients`) |
| **Phase 6** | Task & Milestone Management | Kanban Board, Task CRUD (`/api/tasks`), Live Drag/Status Filters |
| **Phase 7** | Executive Admin Dashboard | Global KPI Stats (`/api/admin/stats`), Chart.js Velocity, Client Directory |
| **Phase 8** | Cloud Documents & Reports | Drag & Drop Cloud Storage (`/api/documents`), SLA Analytics, Email Notifications |
| **Phase 9** | Testing & Deployment CI/CD | Pytest Test Suites, GitHub Actions CI/CD, Render/Vercel/Docker Support |

---

## 💻 Local Setup & Quickstart

### 1. Prerequisites
- Python 3.11+
- Git
- Oracle Database XE (or thin mode in-memory fallback enabled)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/SasiniSiriwardhana/onboard-flow.git
cd onboard-flow

# Create and activate Python virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your Oracle DB, Cloudinary, and JWT secrets
```

### 4. Run the Backend (FastAPI)
```bash
uvicorn backend.server:app --host 0.0.0.0 --port 8000 --reload
# Interactive API Docs: http://localhost:8000/docs
```

### 5. Run the Frontend (Flask)
```bash
python frontend/app.py
# Web Application UI: http://localhost:5000
```

---

## 🧪 Running Automated Tests

```bash
# Run all backend unit & integration tests
pytest backend/tests/ -v

# Run frontend route & template tests
pytest frontend/tests/ -v
```

---

## 🔀 Git Branching & Manual Merge Instructions

To merge completed feature branches into `main` sequentially without conflicts:

```bash
# 1. Update main branch
git checkout main
git pull origin main

# 2. Merge Phase 6 (Task Management)
git merge feature/task-management -m "Merge branch 'feature/task-management' into main"
git push origin main

# 3. Merge Phase 7 (Admin Dashboard)
git merge feature/admin-dashboard -m "Merge branch 'feature/admin-dashboard' into main"
git push origin main

# 4. Merge Phase 8 (Documents & Reports)
git merge feature/documents-reports -m "Merge branch 'feature/documents-reports' into main"
git push origin main

# 5. Merge Phase 9 (Testing & Deployment)
git merge feature/testing-deployment -m "Merge branch 'feature/testing-deployment' into main"
git push origin main
```

---

## 🛡️ License & Credits
Developed for Enterprise Customer Onboarding Systems. Powered by FastAPI, Oracle Database, and DaisyUI.
