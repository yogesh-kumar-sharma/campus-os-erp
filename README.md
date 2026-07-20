<div align="center">

# CampusOS ERP

### The open-source operating system for universities.

A production-grade, async ERP backend — with a modern web frontend on the roadmap — for managing the full academic lifecycle: authentication, students, faculty, academics, attendance, examinations, results, fees, and administration.

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-15-000000?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=flat-square&logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

[![Build](https://img.shields.io/badge/build-passing-brightgreen?style=flat-square)](#-cicd)
[![Coverage](https://img.shields.io/badge/coverage-tracked_in_CI-blue?style=flat-square)](#-testing)
[![Last Commit](https://img.shields.io/github/last-commit/your-org/campusos-erp?style=flat-square)](https://github.com/your-org/campusos-erp/commits)
[![Stars](https://img.shields.io/github/stars/your-org/campusos-erp?style=flat-square)](https://github.com/your-org/campusos-erp/stargazers)
[![Forks](https://img.shields.io/github/forks/your-org/campusos-erp?style=flat-square)](https://github.com/your-org/campusos-erp/network/members)

[Quick Start](#-quick-start) · [Architecture](#-system-architecture) · [API Reference](#-api-overview) · [Roadmap](#-roadmap) · [Contributing](#-contributing)

</div>

> [!NOTE]
> **Repository status:** the **FastAPI backend is implemented and functional** — 12 domain modules, 20 database tables, 60+ REST endpoints, and an automated test suite. The **Next.js frontend, NGINX edge layer, and CI/CD pipeline described below are the target architecture** for this monorepo and are tracked in the [Roadmap](#-roadmap). Badges and diagrams are marked accordingly so this README never overstates what exists today.

---

## 🖼️ Project Preview

<div align="center">

| Swagger / OpenAPI (live today) | Architecture Diagram (live today) |
|:---:|:---:|
| `docs/screenshots/swagger-ui.png` | `docs/screenshots/architecture.png` |
| *Interactive API docs at `/docs`* | *See [System Architecture](#-system-architecture)* |

| Login Screen | Student Dashboard | Faculty Dashboard | Admin Dashboard |
|:---:|:---:|:---:|:---:|
| `docs/screenshots/login.png` | `docs/screenshots/student-dashboard.png` | `docs/screenshots/faculty-dashboard.png` | `docs/screenshots/admin-dashboard.png` |
| 🧩 *planned — frontend* | 🧩 *planned — frontend* | 🧩 *planned — frontend* | 🧩 *planned — frontend* |

</div>

> Screenshot assets are placeholders — drop real captures into `docs/screenshots/` as the frontend lands and update the paths above.

---

## 💡 Why CampusOS ERP?

Most universities run academics, attendance, examinations, and fees across a patchwork of spreadsheets, legacy desktop tools, and disconnected vendor portals. The result: duplicated data entry, no single source of truth, and IT teams locked into closed systems they can't extend.

CampusOS ERP is built as the alternative: a **self-hostable, API-first ERP core** that any institution can own, extend, and integrate — architected the way a modern SaaS product is, not a semester project.

- 🏛️ **Real domain modeling** — students, faculty, departments, sessions, exams, and fees as first-class, related entities, not flat spreadsheets.
- ⚡ **Built for concurrency** — fully async request path, tuned for spikes like registration windows and result publishing.
- 🔐 **Security by default** — hashed credentials, short-lived access tokens, rotating refresh tokens, and route-level RBAC.
- 🧱 **Clean, testable architecture** — business logic is decoupled from FastAPI and SQLAlchemy, so it's cheap to test and safe to extend.
- 🐳 **One-command environments** — Docker Compose brings up the API, PostgreSQL, and Redis identically on every machine.
- 🌱 **Designed to grow** — the monorepo layout already reserves space for a Next.js frontend, an NGINX edge, and CI/CD, so scaling the project doesn't mean rearchitecting it.

---

## ✨ Project Highlights

<table>
<tr>
<td valign="top" width="33%">

**Backend Engineering**
- ✅ Production-ready FastAPI service
- ✅ Fully async I/O (API → DB)
- ✅ Clean Architecture, layered
- ✅ Repository Pattern
- ✅ Service Layer
- ✅ Dependency Injection

</td>
<td valign="top" width="33%">

**Security & Access**
- ✅ JWT access tokens
- ✅ Rotating refresh tokens
- ✅ Role-Based Access Control
- ✅ bcrypt password hashing
- ✅ Environment-based secrets
- ✅ Scoped, self-service endpoints

</td>
<td valign="top" width="33%">

**Platform & DX**
- ✅ Dockerized services
- ✅ Redis caching layer
- ✅ Swagger + ReDoc, auto-generated
- ✅ Alembic auto-migrations
- ✅ Pytest suite (schemas, RBAC, grading)
- ✅ Ruff linting

</td>
</tr>
</table>

---

## 🧩 Feature Overview

| Domain | Capabilities |
|---|---|
| **Authentication** | Register, login, logout, JWT access + refresh rotation, forgot/reset/change password |
| **Users** | Unified identity for Students/Faculty/Admins, profile picture, account deactivation |
| **Roles (RBAC)** | Role catalogue, per-route permission enforcement, role reassignment |
| **Students** | Profile CRUD, paginated directory, self-service `/students/me` |
| **Faculty** | Profile CRUD, paginated directory, self-service `/faculty/me` |
| **Academics** | Departments, Courses, Semesters, Subjects, Sessions, Faculty↔Subject mapping, Timetable |
| **Attendance** | Record create/update/delete, self history, aggregated summaries |
| **Examinations** | Exam scheduling, marks entry, result publishing |
| **Results** | Self-service results, automatic **CGPA calculation** |
| **Fees** | Fee categories, per-student fee assignment, payment recording, self status |
| **Notices** | Create/update/delete, self-service notice feed |
| **Documents** | Multipart upload, per-user document listing |
| **Dashboard** | Role-specific aggregate views — Admin, Faculty, Student |
| **Reports** | 🧩 *planned — analytics/export layer* |
| **Settings** | 🧩 *planned — institution-level configuration* |

---

## 🛠️ Tech Stack

<details open>
<summary><strong>Backend (implemented)</strong></summary>

| Category | Technology |
|---|---|
| Language | Python 3.12+ |
| Framework | FastAPI (async) |
| Server | Uvicorn |
| ORM | SQLAlchemy 2.0 (async) + AsyncPG |
| Migrations | Alembic |
| Validation | Pydantic v2, Pydantic Settings |
| Auth | JWT (python-jose), refresh-token rotation, RBAC |
| Password Hashing | Passlib (bcrypt) |
| File Handling | python-multipart |

</details>

<details>
<summary><strong>Frontend (planned)</strong></summary>

| Category | Technology |
|---|---|
| Framework | Next.js 15 (App Router) |
| Language | TypeScript |
| Styling | Tailwind CSS |
| Components | shadcn/ui |
| Data Fetching | React Query + Axios |
| Motion | Framer Motion |
| Charts | Chart.js / Recharts |

</details>

<details>
<summary><strong>Database & Infrastructure</strong></summary>

| Category | Technology |
|---|---|
| Database | PostgreSQL 16 |
| Cache | Redis 7 |
| Containers | Docker, Docker Compose |
| Edge / Reverse Proxy | NGINX *(planned)* |
| CI/CD | GitHub Actions *(planned)* |
| Deployment Targets | Render / Railway / VPS *(planned)* |

</details>

<details>
<summary><strong>Testing & Developer Tools</strong></summary>

| Category | Technology |
|---|---|
| Testing | Pytest, pytest-asyncio, pytest-cov, HTTPX |
| Linting | Ruff |
| API Docs | Swagger UI, ReDoc, OpenAPI schema |
| Config | Environment-based (`.env` / Pydantic Settings) |

</details>

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    Client["Client Applications<br/>Web · Mobile · Admin Console"]
    Next["Next.js Frontend<br/>(planned)"]
    Gateway["NGINX — API Gateway / Edge<br/>(planned)"]

    subgraph API["FastAPI — API Layer"]
        Routes["Routers: Auth · Users · Students · Faculty<br/>Academic · Attendance · Examinations<br/>Fees · Notices · Documents · Dashboard"]
    end

    subgraph SVC["Service Layer"]
        Services["Business Rules · RBAC Checks<br/>CGPA Calculation · Token Rotation"]
    end

    subgraph REPO["Repository Layer"]
        Repos["Data Access Abstraction"]
    end

    DB[(PostgreSQL 16<br/>SQLAlchemy 2.0 Async)]
    Cache[(Redis 7<br/>Cache · Session State)]
    Storage[["Object / Local Storage<br/>Document Uploads"]]
    External["External Services<br/>Email · SMS · Payment Gateway (planned)"]

    Client --> Next --> Gateway --> Routes
    Client -.->|direct, dev/mobile| Routes
    Routes -->|Depends| Services --> Repos -->|AsyncPG| DB
    Services -.-> Cache
    Services -.-> Storage
    Services -.-> External

    style Next fill:#00000010,stroke-dasharray: 5 5
    style Gateway fill:#00000010,stroke-dasharray: 5 5
    style External fill:#00000010,stroke-dasharray: 5 5
```

**Layering rules**

- API routes are transport-only — they parse requests and call services, nothing more.
- Services own business rules and are framework-agnostic — no FastAPI or SQLAlchemy imports.
- Repositories are the only layer allowed to talk to the database.
- Every dependency flows downward — `API → Service → Repository → Database` — never sideways or back up.

---

## 📁 Folder Structure

```
campusos-erp/
├── backend/                # FastAPI service — implemented
│   ├── app/
│   │   ├── api/            # Routers (thin HTTP layer)
│   │   ├── services/       # Business logic
│   │   ├── repositories/   # Data access
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── security/       # JWT + password hashing
│   │   └── core/           # Settings & logging
│   ├── migrations/         # Alembic
│   ├── tests/               # Pytest suite
│   ├── Dockerfile
│   └── pyproject.toml
│
├── frontend/                # Next.js app — planned
│   ├── app/  components/  lib/  hooks/  public/
│   ├── package.json
│   └── Dockerfile
│
├── nginx/                   # Edge/reverse proxy config — planned
│   └── nginx.conf
│
├── .github/workflows/       # CI/CD pipelines — planned
├── docs/                    # Module-level documentation
├── docker-compose.yml
├── README.md
└── LICENSE
```

---

## 🔌 API Overview

Base path: `/api/v1` · Interactive docs: `/docs` (Swagger) and `/redoc` (ReDoc)

| Module | Path | Sample Endpoints |
|---|---|---|
| Authentication | `/auth` | `POST /login`, `POST /refresh`, `POST /logout`, `GET /me` |
| Students | `/students` | `POST /`, `GET /me`, `GET /`, `PATCH /{id}` |
| Faculty | `/faculty` | `POST /`, `GET /me`, `GET /`, `PATCH /{id}` |
| Attendance | `/attendance` | `POST /`, `GET /me`, `GET /me/summary` |
| Examinations | `/examinations` | `POST /{exam_id}/marks`, `POST /{exam_id}/publish`, `GET /me/cgpa` |
| Fees | `/fees` | `POST /categories`, `POST /{fee_id}/payments`, `GET /me/status` |
| Dashboard | `/dashboard` | `GET /admin`, `GET /faculty`, `GET /student` |

Full endpoint-by-endpoint reference lives in [`docs/`](docs) and the live OpenAPI schema.

---

## 📨 Request / Response Examples

<details>
<summary><strong>Login → receive token pair</strong></summary>

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "student@campusos.edu",
  "password": "••••••••"
}
```

```json
{
  "access_token": "eyJhbGciOi...",
  "refresh_token": "8f14e45f-ceea-467e-...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

</details>

<details>
<summary><strong>Fetch current student's CGPA</strong></summary>

```http
GET /api/v1/examinations/me/cgpa
Authorization: Bearer <access_token>
```

```json
{
  "student_id": "3fae5c9e-9d2e-4a3a-9d7e-2c1b0e6a1c11",
  "cgpa": 8.42,
  "total_credits": 96
}
```

</details>

---

## 🔐 Authentication Flow

```mermaid
sequenceDiagram
    participant U as Client
    participant A as Auth Service
    participant D as Database
    participant R as Protected Route

    U->>A: POST /auth/login (email, password)
    A->>D: verify hashed password
    A-->>U: access_token + refresh_token

    U->>R: GET /resource (Bearer access_token)
    R->>R: validate JWT + resolve role
    alt role authorized
        R-->>U: 200 OK
    else role forbidden
        R-->>U: 403 Forbidden
    end

    U->>A: POST /auth/refresh (refresh_token)
    A->>D: rotate refresh token
    A-->>U: new access_token + new refresh_token
```

Refresh tokens **rotate on every use**; reusing a stale refresh token is treated as a compromise signal. See [`docs/authentication.md`](docs/authentication.md) and [`docs/rbac.md`](docs/rbac.md).

---

## 🗄️ Database Design

20 tables model the full academic lifecycle — identity (`users`, `roles`, `refresh_tokens`), people (`students`, `faculty`), academics (`departments`, `courses`, `semesters`, `subjects`, `academic_sessions`, `timetable`, `faculty_subject_assignments`), operations (`attendance`, `exams`, `results`, `notices`, `documents`), and finance (`fee_categories`, `fees`, `payments`).

```
docs/screenshots/er-diagram.png   ← placeholder, generate via `alembic` + a schema visualizer
```

Full schema reference: [`docs/database-schema.md`](docs/database-schema.md).

---

## 📊 Project Metrics

| Metric | Value |
|---|---|
| Domain Modules | 12 |
| REST Endpoints | 60+ |
| Database Tables | 20 |
| Architecture Pattern | Clean Architecture (Repository + Service layers) |
| Auth Model | JWT + Rotating Refresh Tokens + RBAC |
| Test Suite | Pytest — schemas, config, security, RBAC, grading |
| Docker Services | API · PostgreSQL · Redis |
| API Version | `v1` |

---

## ⚡ Performance Features

- Fully **async** request path — FastAPI → SQLAlchemy async → AsyncPG, no blocking I/O on the hot path
- **Connection pooling** tuned via `DATABASE_POOL_SIZE` / `DATABASE_MAX_OVERFLOW`
- **Redis** available for caching hot reads and reducing database load
- **Pagination** on all list endpoints (students, faculty, etc.) to bound response size
- Indexed, UUID-keyed models designed for efficient lookups and joins

---

## 🔒 Security Features

- JWT access tokens with short expiry + rotating refresh tokens
- Passwords hashed with **bcrypt** — never stored or logged in plaintext
- **RBAC** enforced at the route dependency layer, not in application logic
- Strict Pydantic input validation on every request body
- All secrets and connection strings sourced from environment variables — nothing hardcoded
- CORS configured via `CORS_ORIGINS`
- Rate limiting and audit logging — see [Roadmap](#-roadmap)

---

## 🧑‍💻 Developer Experience

- `uvicorn --reload` hot reload for local development
- One-command environment via `docker compose up`
- Auto-generated **Swagger UI** and **ReDoc** — no hand-written API docs to keep in sync
- **Alembic autogenerate** turns model changes into migrations
- Pytest suite runs in seconds; `ruff check` keeps style consistent
- Fully typed request/response contracts via Pydantic v2

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/your-org/campusos-erp.git
cd campusos-erp/backend

# 2. Install
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# 3. Configure
cp .env.example .env   # set DATABASE_URL, REDIS_URL, JWT_SECRET_KEY

# 4. Migrate
alembic upgrade head

# 5. Run
uvicorn app.main:app --reload
```

API → `http://localhost:8000` · Docs → `http://localhost:8000/docs` · Health → `http://localhost:8000/health`

---

## ⚙️ Environment Variables

| Variable | Description | Example |
|---|---|---|
| `APP_NAME` | Service display name | `CampusOS ERP` |
| `APP_ENV` | Environment name | `development` / `production` |
| `API_V1_PREFIX` | Versioned API base path | `/api/v1` |
| `CORS_ORIGINS` | Allowed origins (comma-separated) | `http://localhost:3000` |
| `DATABASE_URL` | Async PostgreSQL DSN | `postgresql+asyncpg://user:pass@host:5432/db` |
| `DATABASE_POOL_SIZE` / `DATABASE_MAX_OVERFLOW` | Pool tuning | `5` / `10` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `JWT_SECRET_KEY` | JWT signing secret | *generate a strong random value* |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token TTL | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token TTL | `7` |
| `STORAGE_PATH` | Upload storage directory | `storage` |
| `MAX_UPLOAD_SIZE_MB` | Upload size limit | `10` |

> [!WARNING]
> Never commit a real `.env`. `JWT_SECRET_KEY` must be unique per environment.

Full list: [`backend/.env.example`](backend/.env.example) · [`docs/configuration.md`](docs/configuration.md)

---

## 🐳 Docker Setup

```bash
cp backend/.env.example backend/.env
docker compose up --build
```

| Service | Purpose | Port |
|---|---|---|
| `api` | FastAPI backend | 8000 |
| `postgres` | PostgreSQL 16 | 5432 |
| `redis` | Redis 7 | 6379 |
| `frontend` | Next.js app *(planned)* | 3000 |
| `nginx` | Edge / reverse proxy *(planned)* | 80/443 |

Migrations run automatically on container start. See [`docs/docker.md`](docs/docker.md).

---

## 🧪 Testing

```bash
pytest                                  # full suite
pytest --cov=app --cov-report=term-missing   # with coverage
pytest tests/test_rbac.py -v            # a single module
```

Coverage includes config, schemas (student/faculty/academic/attendance/user), security (`test_tokens`), RBAC, and grading logic. See [`docs/testing.md`](docs/testing.md).

---

## 🔁 CI/CD

> 🧩 **Planned.** `.github/workflows/` will host:

- **`ci.yml`** — lint (Ruff) + test (Pytest + coverage) on every PR
- **`build.yml`** — build & push backend/frontend Docker images
- **`deploy.yml`** — deploy to Render / Railway / VPS on merge to `main`

```mermaid
flowchart LR
    PR["Pull Request"] --> Lint["Ruff Lint"] --> Test["Pytest + Coverage"] --> Build["Docker Build"] --> Deploy["Deploy<br/>(Render / Railway / VPS)"]
```

---

## 🗺️ Roadmap

**Backend**
- [x] Auth, RBAC, and core domain modules
- [x] Dockerized API + PostgreSQL + Redis
- [ ] Rate limiting on auth endpoints
- [ ] Redis-backed response caching for dashboards
- [ ] Structured audit logging
- [ ] Bulk CSV import/export for students & faculty

**Platform**
- [ ] Next.js frontend (App Router, TypeScript, Tailwind, shadcn/ui)
- [ ] NGINX reverse proxy in front of API + frontend
- [ ] GitHub Actions CI/CD pipeline
- [ ] OpenAPI-generated TypeScript client
- [ ] Reports/analytics module
- [ ] Institution-level settings module

---

## 🤝 Contributing

1. Fork the repo and create a branch: `git checkout -b feature/my-feature`
2. Respect the layering — routes stay thin, logic lives in `services/`, persistence in `repositories/`
3. Before opening a PR:
   ```bash
   ruff check .
   pytest --cov=app
   ```
4. Update relevant docs in `docs/` when behavior changes
5. Open a PR describing the change, motivation, and how it was tested

Large or breaking changes → please open an issue first to discuss.

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE).

## 🙏 Acknowledgements

Built on the shoulders of [FastAPI](https://fastapi.tiangolo.com/), [SQLAlchemy](https://www.sqlalchemy.org/), [Pydantic](https://docs.pydantic.dev/), and the wider Python async ecosystem.

---

<div align="center">

**Built with ❤️ using FastAPI, PostgreSQL, and Redis — with Next.js on the way.**

</div>
