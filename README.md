# CampusOS ERP

**Enterprise University Management Platform**

A scalable, async, production-oriented backend for automating university operations — authentication, users, students, faculty, academics, attendance, examinations, results, fees, and administration — built on FastAPI, PostgreSQL, and Redis.

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/lint-ruff-261230)](https://github.com/astral-sh/ruff)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Setup (without Docker)](#local-setup-without-docker)
  - [Setup with Docker Compose](#setup-with-docker-compose)
- [Environment Variables](#environment-variables)
- [Database Migrations](#database-migrations)
- [API Reference](#api-reference)
- [Authentication & RBAC](#authentication--rbac)
- [Testing](#testing)
- [Documentation](#documentation)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Universities typically run academics, attendance, examinations, fees, and administration on a patchwork of spreadsheets, legacy desktop software, and disconnected portals. This creates duplicated data entry, inconsistent records, and no single source of truth for a student's academic lifecycle.

**CampusOS ERP** solves this by providing a single, well-architected backend API that models the full academic lifecycle — from admission and enrollment through attendance, examinations, results, and fee payments — behind a secure, role-aware REST interface that any frontend (web, mobile, or admin console) can consume.

**Target users**

- **University IT teams** who need a self-hosted, extensible ERP core instead of a closed vendor product.
- **Frontend / product teams** building student, faculty, or admin portals that need a stable API contract.
- **Students & Faculty**, indirectly, through the client applications built on top of this API.

**Key benefits**

- 🏗️ Clean, layered architecture that keeps business logic testable and independent of transport/framework details.
- ⚡ Fully asynchronous request handling for high-concurrency workloads (registration windows, result publishing, exam periods).
- 🔐 Security-first design — hashed credentials, short-lived access tokens, rotating refresh tokens, and granular RBAC.
- 🐳 One-command local environment via Docker Compose (API + PostgreSQL + Redis).
- 🧪 A real automated test suite covering schemas, config, security, and business rules — not just happy-path smoke tests.

---

## Features

### 🔑 Authentication Module
- User registration & login with hashed passwords (bcrypt via Passlib)
- JWT **access tokens** + **rotating refresh tokens**
- Token refresh, logout, forgot-password, reset-password, and change-password flows
- `GET /auth/me` for current-session identity resolution

### 👥 User & Role Management
- Central `User` identity shared across Students, Faculty, and Admins
- Role catalogue with **Role-Based Access Control (RBAC)**
- Admin endpoints to list roles and reassign a user's role
- Profile management, profile picture upload, and account deactivation

### 🎓 Student Management
- Student profile creation and paginated listing/search
- Self-service `GET/PATCH /students/me`
- Academic metadata (department, session, enrollment info)
- Linked document management for student records

### 🧑‍🏫 Faculty Management
- Faculty profile creation, self-service view, and paginated directory
- Department-linked faculty records
- Faculty-to-subject assignment for teaching workloads

### 📚 Academic Management
- Departments, Courses, Semesters, and Subjects
- Academic Sessions (e.g. term/year cycles)
- Faculty ↔ Subject mapping
- Timetable creation and retrieval

### 🗓️ Attendance Management
- Attendance record creation, update, and deletion
- Self-service attendance history (`/attendance/me`)
- Aggregated attendance summaries per subject/session

### 📝 Examination & Result Management
- Examination scheduling
- Marks entry per examination
- Result publishing workflow
- Self-service results and **automatic CGPA calculation**

### 💰 Fees & Payment Management
- Fee category configuration
- Fee assignment per student
- Payment recording against a fee
- Self-service fee/payment status

### 📢 Notice Management
- Notice creation, update, and deletion (admin/faculty)
- Self-service notice feed (`/notices/me`)

### 📁 Document Management
- Multipart file upload for student/faculty documents
- Document listing per user

### 📊 Dashboard APIs
- Role-specific aggregate dashboards: **Admin**, **Faculty**, and **Student**

---

## Technology Stack

| Category | Technology |
|---|---|
| Language | Python 3.12+ |
| Web Framework | FastAPI (async) |
| ASGI Server | Uvicorn |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy 2.0 (async) |
| DB Driver | AsyncPG |
| Migrations | Alembic |
| Caching | Redis 7 |
| Auth | JWT (python-jose), Access + Refresh Token Rotation, RBAC |
| Password Hashing | Passlib (bcrypt) |
| Validation | Pydantic v2, Pydantic Settings, email-validator |
| File Handling | python-multipart (multipart uploads, document storage) |
| Testing | Pytest, pytest-asyncio, pytest-cov, HTTPX |
| Linting | Ruff |
| Containerization | Docker, Docker Compose |
| Config | Environment-based (`.env` / Pydantic Settings) |

---

## System Architecture

CampusOS ERP follows **Clean Architecture** with a strict, one-directional dependency flow: API routes never touch the database directly, and business rules never depend on FastAPI or SQLAlchemy internals.

```mermaid
flowchart TD
    Client[Client Applications<br/>Web / Mobile / Admin Console]

    subgraph API["API Layer (app/api)"]
        Routes["FastAPI Routers<br/>Auth · Users · Students · Faculty<br/>Academic · Attendance · Examinations<br/>Fees · Notices · Documents · Dashboard"]
    end

    subgraph SVC["Service Layer (app/services)"]
        Services["Business Logic & Orchestration<br/>Validation Rules · CGPA Calc · RBAC Checks"]
    end

    subgraph REPO["Repository Layer (app/repositories)"]
        Repos["Data Access Abstraction<br/>Query Building · Persistence"]
    end

    subgraph INFRA["Infrastructure"]
        DB[(PostgreSQL<br/>SQLAlchemy 2.0 Async ORM)]
        Cache[(Redis<br/>Caching / Token State)]
        Storage[[Local / Mounted Storage<br/>Document Uploads]]
    end

    Client -->|HTTPS / JSON| Routes
    Routes -->|Dependency Injection| Services
    Services --> Repos
    Repos -->|AsyncPG| DB
    Services -.->|cache reads/writes| Cache
    Services -.->|file I/O| Storage

    Middleware["Middleware<br/>Auth Guard · CORS · Logging"] -.-> Routes
    Security["Security Layer<br/>JWT · Password Hashing"] -.-> Services
```

**Design principles applied**

- **Repository Pattern** — all persistence access is abstracted behind repository classes; services never write raw queries.
- **Service Layer** — business rules (RBAC checks, CGPA math, token rotation) live in `app/services`, independent of the HTTP layer.
- **Dependency Injection** — FastAPI's `Depends()` wires repositories, services, and the authenticated user into each route.
- **Separation of Concerns** — models, schemas, routing, business logic, and persistence each live in their own package.
- **Async end-to-end** — from the ASGI server down to the database driver, no blocking I/O sits on the request path.

---

## Project Structure

```
CampusOS-ERP/
├── app/
│   ├── main.py               # FastAPI app factory, lifespan, health check
│   ├── api/                  # Route definitions (thin HTTP layer)
│   │   ├── auth.py           # /auth  – login, refresh, logout, password flows
│   │   ├── users.py          # /users – profile, avatar, deactivation
│   │   ├── roles.py          # /roles – RBAC role assignment
│   │   ├── students.py       # /students
│   │   ├── faculty.py        # /faculty
│   │   ├── academic.py       # /academic – departments, courses, subjects...
│   │   ├── attendance.py     # /attendance
│   │   ├── examinations.py   # /examinations – marks, publish, CGPA
│   │   ├── fees.py           # /fees – categories, payments
│   │   ├── notices.py        # /notices
│   │   ├── documents.py      # /documents – uploads
│   │   ├── dashboard.py      # /dashboard – admin/faculty/student summaries
│   │   └── router.py         # Aggregates all routers into api_router
│   ├── services/              # Business logic (one service per domain)
│   ├── repositories/          # Data-access layer (one repository per aggregate)
│   ├── models/                 # SQLAlchemy ORM models
│   ├── schemas/                # Pydantic request/response schemas
│   ├── security/               # Password hashing & JWT token utilities
│   ├── middleware/             # Auth guard, CORS, logging middleware
│   ├── dependencies/            # FastAPI dependency providers
│   ├── database/                # Async session/engine management
│   ├── core/                    # Settings (Pydantic Settings) & logging config
│   └── utils/                    # Shared helpers
├── migrations/                 # Alembic migration environment & versions
├── tests/                      # Pytest suite (schemas, config, security, RBAC, grading)
├── docs/                       # Module-level documentation
├── docker-compose.yml          # API + PostgreSQL + Redis stack
├── Dockerfile                  # Production container image
├── alembic.ini
├── pyproject.toml
└── .env.example
```

---

## Getting Started

### Prerequisites

- Python **3.12+**
- PostgreSQL **16+** (or use the provided Docker service)
- Redis **7+** (or use the provided Docker service)
- Docker & Docker Compose *(optional but recommended)*

### Local Setup (without Docker)

```bash
# 1. Clone the repository
git clone https://github.com/<your-org>/campusos-erp.git
cd campusos-erp

# 2. Create and activate a virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies (runtime + dev/test extras)
pip install -e ".[dev]"

# 4. Configure environment variables
cp .env.example .env
# edit .env with your local DATABASE_URL, REDIS_URL, and JWT_SECRET_KEY

# 5. Apply database migrations
alembic upgrade head

# 6. Run the development server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`, with interactive docs at:

- Swagger UI → `http://localhost:8000/docs`
- ReDoc → `http://localhost:8000/redoc`
- Health check → `http://localhost:8000/health`

### Setup with Docker Compose

This spins up the API, PostgreSQL, and Redis together, and automatically runs migrations on startup.

```bash
cp .env.example .env
docker compose up --build
```

| Service | Container Port | Host Port |
|---|---|---|
| `api` | 8000 | 8000 |
| `postgres` | 5432 | 5432 |
| `redis` | 6379 | 6379 |

Stop the stack:

```bash
docker compose down          # keep volumes
docker compose down -v       # also remove postgres/redis volumes
```

---

## Environment Variables

Configuration is fully environment-driven via **Pydantic Settings** (`app/core/config.py`). See [`.env.example`](.env.example) for the complete list. Key variables:

| Variable | Description | Example |
|---|---|---|
| `APP_NAME` | Display name of the service | `College ERP Management System` |
| `APP_ENV` | Environment name | `development` / `production` |
| `DEBUG` | Enable debug mode | `true` / `false` |
| `API_V1_PREFIX` | Base path for versioned routes | `/api/v1` |
| `CORS_ORIGINS` | Comma-separated allowed origins | `http://localhost:3000` |
| `DATABASE_URL` | Async PostgreSQL DSN | `postgresql+asyncpg://user:pass@host:5432/db` |
| `DATABASE_POOL_SIZE` / `DATABASE_MAX_OVERFLOW` | SQLAlchemy pool tuning | `5` / `10` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `JWT_SECRET_KEY` | Secret used to sign JWTs | *(generate a strong random value)* |
| `JWT_ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token lifetime | `7` |
| `PASSWORD_RESET_TOKEN_EXPIRE_MINUTES` | Reset-token lifetime | `15` |
| `STORAGE_PATH` | Directory for uploaded documents | `storage` |
| `MAX_UPLOAD_SIZE_MB` | Upload size limit | `10` |

> ⚠️ Never commit a real `.env` file. `JWT_SECRET_KEY` in particular must be replaced with a strong, unique secret in every environment.

---

## Database Migrations

Schema changes are managed with **Alembic**.

```bash
# Generate a new migration from model changes
alembic revision --autogenerate -m "add fee_category table"

# Apply all pending migrations
alembic upgrade head

# Roll back one revision
alembic downgrade -1
```

See [`docs/database.md`](docs/database.md) and [`docs/database-schema.md`](docs/database-schema.md) for schema details.

---

## API Reference

All endpoints are versioned under `API_V1_PREFIX` (default `/api/v1`). Full interactive documentation is served at `/docs` (Swagger) and `/redoc`.

| Module | Base Path | Highlights |
|---|---|---|
| Authentication | `/api/v1/auth` | `register`, `login`, `refresh`, `logout`, `forgot-password`, `reset-password`, `change-password`, `me` |
| Roles | `/api/v1/roles` | List roles, assign role to user |
| Users | `/api/v1/users` | Profile, profile picture upload, deactivate, admin listing |
| Students | `/api/v1/students` | Create, self-profile, paginated list, get/update by ID |
| Faculty | `/api/v1/faculty` | Create, self-profile, paginated list, get/update by ID |
| Academic | `/api/v1/academic` | Departments, Courses, Semesters, Subjects, Sessions, Faculty-Subjects, Timetable |
| Attendance | `/api/v1/attendance` | Create/update/delete records, self history, self summary |
| Examinations | `/api/v1/examinations` | Create exam, enter marks, publish results, self results, self CGPA |
| Fees | `/api/v1/fees` | Fee categories, assign fees, record payments, self status |
| Notices | `/api/v1/notices` | Create/update/delete, self feed |
| Documents | `/api/v1/documents` | Upload, list |
| Dashboard | `/api/v1/dashboard` | Admin, Faculty, and Student summary views |

---

## Authentication & RBAC

1. **Register / Login** → receive a short-lived **access token** and a long-lived **refresh token**.
2. Every protected route requires `Authorization: Bearer <access_token>`.
3. When the access token expires, call `POST /auth/refresh` with the refresh token to obtain a new token pair — refresh tokens **rotate** on every use, and reuse of an old token is treated as a compromise signal.
4. Each `User` is linked to a **Role** (e.g. Admin, Faculty, Student). Route-level dependencies enforce **RBAC**, so a Student cannot access Faculty- or Admin-only endpoints (e.g. publishing results, managing fee categories).

See [`docs/authentication.md`](docs/authentication.md) and [`docs/rbac.md`](docs/rbac.md) for the full flow and permission matrix.

---

## Testing

The project ships with a Pytest suite covering configuration, schemas, security primitives, RBAC rules, and grading logic.

```bash
# Run the full test suite
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run a specific test file
pytest tests/test_rbac.py -v
```

Test coverage includes: `test_health`, `test_config`, `test_database_base`, `test_tokens`, `test_rbac`, `test_grade_calculation`, `test_user_schemas`, `test_student_schemas`, `test_faculty_schemas`, `test_academic_schemas`, and `test_attendance_schema`. See [`docs/testing.md`](docs/testing.md) for conventions and how to add new tests.

---

## Documentation

In-depth, module-level documentation lives under [`docs/`](docs):

| Doc | Covers |
|---|---|
| [`architecture.md`](docs/architecture.md) | Layering, request flow, design decisions |
| [`authentication.md`](docs/authentication.md) | Auth & token lifecycle |
| [`rbac.md`](docs/rbac.md) | Roles & permissions |
| [`users.md`](docs/users.md) | User profile management |
| [`students.md`](docs/students.md) | Student domain |
| [`faculty.md`](docs/faculty.md) | Faculty domain |
| [`academic.md`](docs/academic.md) | Departments, courses, subjects, timetable |
| [`attendance.md`](docs/attendance.md) | Attendance records & summaries |
| [`notices.md`](docs/notices.md) | Notice board |
| [`database.md`](docs/database.md) / [`database-schema.md`](docs/database-schema.md) | Data model & schema |
| [`docker.md`](docs/docker.md) | Container image & compose stack |
| [`deployment.md`](docs/deployment.md) | Deployment guidance |
| [`testing.md`](docs/testing.md) | Test suite conventions |
| [`configuration.md`](docs/configuration.md) | Settings & environment variables |

---

## Roadmap

- [ ] Rate limiting on authentication endpoints
- [ ] Redis-backed caching for read-heavy dashboard/report endpoints
- [ ] Structured audit logging for administrative actions
- [ ] Bulk import/export (CSV) for students and faculty
- [ ] Webhook/notification integration for fee and result publishing events
- [ ] OpenAPI-generated TypeScript client for frontend consumption

Have an idea? Open an issue or start a discussion.

---

## Contributing

Contributions are welcome!

1. Fork the repository and create a feature branch (`git checkout -b feature/my-feature`).
2. Follow the existing layering — routes stay thin, business logic goes in `services/`, persistence goes in `repositories/`.
3. Run linting and tests before opening a PR:
   ```bash
   ruff check .
   pytest --cov=app
   ```
4. Write clear commit messages and update relevant docs in `docs/` when behavior changes.
5. Open a pull request describing the change, motivation, and testing performed.

Please open an issue first for large or breaking changes so they can be discussed.

---

## License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

<p align="center">Built for universities that deserve better software.</p>
