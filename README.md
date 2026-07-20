<div align="center">

# CampusOS ERP

### An open-source backend platform for university operations.

A production-grade, async **backend API** for managing the university academic lifecycle: authentication, students, faculty, academics, attendance, examinations, results, fees, and administration.

<!-- TODO: Replace <yogesh-kumar-sharma> and <campus-os-erp> below once the repository is published, then these badges will resolve automatically. -->

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Alembic](https://img.shields.io/badge/Alembic-Migrations-4B8BBE?style=for-the-badge)](https://alembic.sqlalchemy.org/)
[![Pytest](https://img.shields.io/badge/Pytest-Tested-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-FCC624?style=for-the-badge)](LICENSE)

<!-- TODO: Add CI badge once .github/workflows/ci.yml exists, e.g.:
[![CI](https://img.shields.io/github/actions/workflow/status/<TODO-GITHUB-USERNAME>/<TODO-REPO-NAME>/ci.yml?style=flat-square)](https://github.com/<TODO-GITHUB-USERNAME>/<TODO-REPO-NAME>/actions)
-->
<!-- TODO: Add coverage badge once test coverage is published (e.g. via Codecov), e.g.:
[![Coverage](https://img.shields.io/codecov/c/github/<TODO-GITHUB-USERNAME>/<TODO-REPO-NAME>?style=flat-square)](https://codecov.io/gh/<TODO-GITHUB-USERNAME>/<TODO-REPO-NAME>)
-->
<!-- TODO: Add these once the repo is public on GitHub — they work automatically, no CI required:
[![Last Commit](https://img.shields.io/github/last-commit/<TODO-GITHUB-USERNAME>/<TODO-REPO-NAME>?style=flat-square)](https://github.com/<TODO-GITHUB-USERNAME>/<TODO-REPO-NAME>/commits)
[![Stars](https://img.shields.io/github/stars/<TODO-GITHUB-USERNAME>/<TODO-REPO-NAME>?style=flat-square)](https://github.com/<TODO-GITHUB-USERNAME>/<TODO-REPO-NAME>/stargazers)
[![Forks](https://img.shields.io/github/forks/<TODO-GITHUB-USERNAME>/<TODO-REPO-NAME>?style=flat-square)](https://github.com/<TODO-GITHUB-USERNAME>/<TODO-REPO-NAME>/network/members)
-->

[Quick Start](#-quick-start) · [Architecture](#-system-architecture) · [API Reference](#-api-overview) · [Roadmap](#-roadmap) · [Contributing](#-contributing)

</div>

> [!NOTE]
> **Repository status:** this repository currently contains **only the backend** — a functional FastAPI service with 12 domain modules, 20 database tables, 60+ REST endpoints, and an automated test suite. There is **no frontend yet**. NGINX, GitHub Actions/CI, and hosted deployment are **planned** and tracked in the [Roadmap](#-roadmap). Every section below is explicitly labeled **Implemented** or **Planned** so this README never overstates what exists today.

---

## 🖼️ Project Preview

<div align="center">

| Swagger / OpenAPI ✅ Implemented | Architecture Diagram ✅ Implemented |
|:---:|:---:|
| `TODO: Add a screenshot of Swagger UI at /docs` | `TODO: Add an exported image of the architecture diagram below` |

| Login Screen | Student Dashboard | Faculty Dashboard | Admin Dashboard |
|:---:|:---:|:---:|:---:|
| 🧩 Planned | 🧩 Planned | 🧩 Planned | 🧩 Planned |
| `TODO: Add Login screenshot once frontend exists` | `TODO: Add Student Dashboard screenshot` | `TODO: Add Faculty Dashboard screenshot` | `TODO: Add Admin Dashboard screenshot` |

</div>

<!-- TODO: Add a short GIF demo of the API (e.g. Swagger UI walkthrough or an HTTPie/curl session) -->
<!-- TODO: Add a live deployment URL once the API is hosted -->

---

## 💡 Why CampusOS ERP?

Most universities run academics, attendance, examinations, and fees across a patchwork of spreadsheets, legacy desktop tools, and disconnected vendor portals. The result: duplicated data entry, no single source of truth, and IT teams locked into closed systems they can't extend.

CampusOS ERP is built as the alternative: a **self-hostable, API-first ERP core** that an institution can own, extend, and integrate — architected the way a production backend service is, not a tutorial project.

- 🏛️ **Real domain modeling** — students, faculty, departments, sessions, exams, and fees as first-class, related entities, not flat spreadsheets.
- ⚡ **Built for concurrency** — fully async request path, tuned for spikes like registration windows and result publishing.
- 🔐 **Security by default** — hashed credentials, short-lived access tokens, rotating refresh tokens, and route-level RBAC.
- 🧱 **Clean, testable architecture** — business logic is decoupled from FastAPI and SQLAlchemy, so it's cheap to test and safe to extend.
- 🐳 **One-command environment** — Docker Compose brings up the API, PostgreSQL, and Redis identically on every machine.
- 🌱 **Designed to grow** — a frontend, edge proxy, and CI/CD can be added on top of this backend without rearchitecting it. See [Roadmap](#-roadmap).

---

## ✨ Project Highlights

<table>
<tr>
<td valign="top" width="33%">

**Backend Engineering** ✅
- Production-oriented FastAPI service
- Fully async I/O (API → DB)
- Clean Architecture, layered
- Repository Pattern
- Service Layer
- Dependency Injection

</td>
<td valign="top" width="33%">

**Security & Access** ✅
- JWT access tokens
- Rotating refresh tokens
- Role-Based Access Control
- bcrypt password hashing
- Environment-based secrets
- Scoped, self-service endpoints

</td>
<td valign="top" width="33%">

**Platform & DX** ✅
- Dockerized services
- Redis available for caching
- Swagger + ReDoc, auto-generated
- Alembic auto-migrations
- Pytest suite (schemas, RBAC, grading)
- Ruff linting

</td>
</tr>
</table>

> All items above reflect the backend as it exists today. Frontend, CI/CD, and deployment tooling are tracked separately in the [Roadmap](#-roadmap).

---

## 🧩 Feature Overview

| Domain | Capabilities | Status |
|---|---|:---:|
| **Authentication** | Register, login, logout, JWT access + refresh rotation, forgot/reset/change password | ✅ Implemented |
| **Users** | Unified identity for Students/Faculty/Admins, profile picture, account deactivation | ✅ Implemented |
| **Roles (RBAC)** | Role catalogue, per-route permission enforcement, role reassignment | ✅ Implemented |
| **Students** | Profile CRUD, paginated directory, self-service `/students/me` | ✅ Implemented |
| **Faculty** | Profile CRUD, paginated directory, self-service `/faculty/me` | ✅ Implemented |
| **Academics** | Departments, Courses, Semesters, Subjects, Sessions, Faculty↔Subject mapping, Timetable | ✅ Implemented |
| **Attendance** | Record create/update/delete, self history, aggregated summaries | ✅ Implemented |
| **Examinations** | Exam scheduling, marks entry, result publishing | ✅ Implemented |
| **Results** | Self-service results, automatic **CGPA calculation** | ✅ Implemented |
| **Fees** | Fee categories, per-student fee assignment, payment recording, self status | ✅ Implemented |
| **Notices** | Create/update/delete, self-service notice feed | ✅ Implemented |
| **Documents** | Multipart upload, per-user document listing | ✅ Implemented |
| **Dashboard** | Role-specific aggregate views — Admin, Faculty, Student | ✅ Implemented |
| **Reports** | Analytics/export layer | 🧩 Planned |
| **Settings** | Institution-level configuration | 🧩 Planned |

---

## 🛠️ Tech Stack

<details open>
<summary><strong>Backend — ✅ Implemented</strong></summary>

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
<summary><strong>Database & Infrastructure — ✅ Implemented (Docker, Postgres, Redis) / 🧩 Planned (edge, CI, hosting)</strong></summary>

| Category | Technology | Status |
|---|---|:---:|
| Database | PostgreSQL 16 | ✅ Implemented |
| Cache | Redis 7 | ✅ Implemented |
| Containers | Docker, Docker Compose | ✅ Implemented |
| Edge / Reverse Proxy | NGINX | 🧩 Planned |
| CI/CD | GitHub Actions | 🧩 Planned |
| Deployment Targets | Render / Railway / VPS | 🧩 Planned |

</details>

<details>
<summary><strong>Frontend — 🧩 Planned (does not exist yet)</strong></summary>

| Category | Technology |
|---|---|
| Framework | Next.js (App Router) |
| Language | TypeScript |
| Styling | Tailwind CSS |
| Components | shadcn/ui |
| Data Fetching | React Query + Axios |
| Motion | Framer Motion |
| Charts | Chart.js / Recharts |

No frontend code exists in this repository yet. This table documents the intended stack for planning purposes only.

</details>

<details>
<summary><strong>Testing & Developer Tools — ✅ Implemented</strong></summary>

| Category | Technology |
|---|---|
| Testing | Pytest, pytest-asyncio, pytest-cov, HTTPX |
| Linting | Ruff |
| API Docs | Swagger UI, ReDoc, OpenAPI schema |
| Config | Environment-based (`.env` / Pydantic Settings) |

</details>

---

## 🏗️ System Architecture

The diagram below shows both the **current backend** (solid boxes) and the **target architecture** (dashed boxes, planned).

```mermaid
flowchart TD
    Client["Client Applications<br/>(current: API consumers via HTTP)"]
    Next["Next.js Frontend<br/>(planned — not built yet)"]
    Gateway["NGINX — API Gateway / Edge<br/>(planned — not built yet)"]

    subgraph API["FastAPI — API Layer (implemented)"]
        Routes["Routers: Auth · Users · Students · Faculty<br/>Academic · Attendance · Examinations<br/>Fees · Notices · Documents · Dashboard"]
    end

    subgraph SVC["Service Layer (implemented)"]
        Services["Business Rules · RBAC Checks<br/>CGPA Calculation · Token Rotation"]
    end

    subgraph REPO["Repository Layer (implemented)"]
        Repos["Data Access Abstraction"]
    end

    DB[(PostgreSQL 16<br/>SQLAlchemy 2.0 Async — implemented)]
    Cache[(Redis 7<br/>available — implemented)]
    Storage[["Local Storage<br/>Document Uploads — implemented"]]
    External["External Services<br/>Email · SMS · Payment Gateway<br/>(planned — not built yet)"]

    Client -.->|planned path| Next -.-> Gateway -.-> Routes
    Client -->|current: direct HTTP| Routes
    Routes -->|Depends| Services --> Repos -->|AsyncPG| DB
    Services -.-> Cache
    Services -.-> Storage
    Services -.-> External

    style Next fill:#00000010,stroke-dasharray: 5 5
    style Gateway fill:#00000010,stroke-dasharray: 5 5
    style External fill:#00000010,stroke-dasharray: 5 5
```

**Layering rules (implemented)**

- API routes are transport-only — they parse requests and call services, nothing more.
- Services own business rules and are framework-agnostic — no FastAPI or SQLAlchemy imports.
- Repositories are the only layer allowed to talk to the database.
- Every dependency flows downward — `API → Service → Repository → Database` — never sideways or back up.

<!-- TODO: Add an exported architecture image to docs/screenshots/architecture.png and reference it here -->

---

## 📁 Folder Structure

The structure below reflects the **actual current repository**. Planned items are marked explicitly and do not exist yet.

```
campusos-erp/
├── app/                      # FastAPI application — ✅ implemented
│   ├── api/                  # Routers (thin HTTP layer)
│   ├── services/              # Business logic
│   ├── repositories/          # Data access
│   ├── models/                 # SQLAlchemy models
│   ├── schemas/                 # Pydantic schemas
│   ├── security/                 # JWT + password hashing
│   ├── middleware/                # Auth guard, CORS, logging
│   ├── dependencies/               # DI providers
│   ├── database/                    # Async session/engine
│   └── core/                         # Settings & logging
├── migrations/                # Alembic migrations — ✅ implemented
├── tests/                      # Pytest suite — ✅ implemented
├── docs/                        # Module-level documentation — ✅ implemented
├── Dockerfile                    # ✅ implemented
├── docker-compose.yml              # ✅ implemented
├── alembic.ini
├── pyproject.toml
├── .env.example
│
├── frontend/                  # Next.js app — 🧩 planned, does not exist yet
├── nginx/                      # Reverse proxy config — 🧩 planned, does not exist yet
├── .github/workflows/            # CI/CD pipelines — 🧩 planned, does not exist yet
│
├── README.md
└── LICENSE                    # TODO: confirm LICENSE file is present at repo root
```

---

## 🔌 API Overview

Base path: `/api/v1` · Interactive docs: `/docs` (Swagger) and `/redoc` (ReDoc) — all ✅ implemented and live when the server is running.

| Module | Path | Sample Endpoints |
|---|---|---|
| Authentication | `/auth` | `POST /login`, `POST /refresh`, `POST /logout`, `GET /me` |
| Students | `/students` | `POST /`, `GET /me`, `GET /`, `PATCH /{id}` |
| Faculty | `/faculty` | `POST /`, `GET /me`, `GET /`, `PATCH /{id}` |
| Attendance | `/attendance` | `POST /`, `GET /me`, `GET /me/summary` |
| Examinations | `/examinations` | `POST /{exam_id}/marks`, `POST /{exam_id}/publish`, `GET /me/cgpa` |
| Fees | `/fees` | `POST /categories`, `POST /{fee_id}/payments`, `GET /me/status` |
| Dashboard | `/dashboard` | `GET /admin`, `GET /faculty`, `GET /student` |

Full endpoint-by-endpoint reference lives in [`docs/`](docs) and the live OpenAPI schema at `/openapi.json`.

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

> Example values above are illustrative placeholders, not real data.

---

## 🔐 Authentication Flow

✅ Implemented.

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

✅ Implemented — 20 tables model the full academic lifecycle: identity (`users`, `roles`, `refresh_tokens`), people (`students`, `faculty`), academics (`departments`, `courses`, `semesters`, `subjects`, `academic_sessions`, `timetable`, `faculty_subject_assignments`), operations (`attendance`, `exams`, `results`, `notices`, `documents`), and finance (`fee_categories`, `fees`, `payments`).

<!-- TODO: Add ER Diagram — generate via a schema visualizer (e.g. erdantic, dbdiagram.io, or `pg_dump --schema-only` + a visualizer) and save to docs/screenshots/er-diagram.png -->

Full schema reference: [`docs/database-schema.md`](docs/database-schema.md).

---

## 📊 Project Metrics

| Metric | Value | Status |
|---|---|:---:|
| Domain Modules | 12 | ✅ Implemented |
| REST Endpoints | 60+ | ✅ Implemented |
| Database Tables | 20 | ✅ Implemented |
| Architecture Pattern | Clean Architecture (Repository + Service layers) | ✅ Implemented |
| Auth Model | JWT + Rotating Refresh Tokens + RBAC | ✅ Implemented |
| Test Suite | Pytest — schemas, config, security, RBAC, grading | ✅ Implemented |
| Test Coverage % | — | <!-- TODO: run `pytest --cov=app` and record the number --> |
| Docker Services | API · PostgreSQL · Redis | ✅ Implemented |
| API Version | `v1` | ✅ Implemented |

---

## ⚡ Performance Features

✅ Implemented, unless marked otherwise.

- Fully **async** request path — FastAPI → SQLAlchemy async → AsyncPG, no blocking I/O on the hot path
- **Connection pooling** tuned via `DATABASE_POOL_SIZE` / `DATABASE_MAX_OVERFLOW`
- **Redis** available for caching hot reads and reducing database load (active caching strategies: 🧩 planned, see Roadmap)
- **Pagination** on list endpoints (students, faculty, etc.) to bound response size
- Indexed, UUID-keyed models designed for efficient lookups and joins

---

## 🔒 Security Features

✅ Implemented, unless marked otherwise.

- JWT access tokens with short expiry + rotating refresh tokens
- Passwords hashed with **bcrypt** — never stored or logged in plaintext
- **RBAC** enforced at the route dependency layer, not in application logic
- Strict Pydantic input validation on every request body
- All secrets and connection strings sourced from environment variables — nothing hardcoded
- CORS configured via `CORS_ORIGINS`
- Rate limiting — 🧩 planned
- Audit logging — 🧩 planned

---

## 🧑‍💻 Developer Experience

✅ Implemented.

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
git clone https://github.com/<TODO-GITHUB-USERNAME>/<TODO-REPO-NAME>.git
cd <TODO-REPO-NAME>

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

Full list: [`.env.example`](.env.example) · [`docs/configuration.md`](docs/configuration.md)

---

## 🐳 Docker Setup

✅ Implemented — API, PostgreSQL, and Redis. Frontend and NGINX services are 🧩 planned additions to `docker-compose.yml`.

```bash
cp .env.example .env
docker compose up --build
```

| Service | Purpose | Port | Status |
|---|---|---|:---:|
| `api` | FastAPI backend | 8000 | ✅ Implemented |
| `postgres` | PostgreSQL 16 | 5432 | ✅ Implemented |
| `redis` | Redis 7 | 6379 | ✅ Implemented |
| `frontend` | Next.js app | 3000 | 🧩 Planned |
| `nginx` | Edge / reverse proxy | 80/443 | 🧩 Planned |

Migrations run automatically on container start. See [`docs/docker.md`](docs/docker.md).

---

## 🧪 Testing

✅ Implemented.

```bash
pytest                                        # full suite
pytest --cov=app --cov-report=term-missing    # with coverage
pytest tests/test_rbac.py -v                  # a single module
```

Coverage includes config, schemas (student/faculty/academic/attendance/user), security (`test_tokens`), RBAC, and grading logic. See [`docs/testing.md`](docs/testing.md).

<!-- TODO: Publish coverage report (e.g. Codecov) and link it here once CI exists -->

---

## 🔁 CI/CD

🧩 **Planned — `.github/workflows/` does not exist yet.** Intended pipeline:

- **`ci.yml`** — lint (Ruff) + test (Pytest + coverage) on every PR
- **`build.yml`** — build & push backend (and later frontend) Docker images
- **`deploy.yml`** — deploy to a hosting target on merge to `main`

```mermaid
flowchart LR
    PR["Pull Request"] --> Lint["Ruff Lint"] --> Test["Pytest + Coverage"] --> Build["Docker Build"] --> Deploy["Deploy<br/>(target TBD)"]
```

<!-- TODO: Replace "target TBD" once a hosting provider (Render / Railway / VPS) is chosen -->
<!-- TODO: Add Live Deployment URL here once hosted -->

---

## 🗺️ Roadmap

**Backend**
- [x] Auth, RBAC, and core domain modules
- [x] Dockerized API + PostgreSQL + Redis
- [ ] Rate limiting on auth endpoints
- [ ] Redis-backed response caching for dashboards
- [ ] Structured audit logging
- [ ] Bulk CSV import/export for students & faculty

**Platform (not started)**
- [ ] Next.js frontend (App Router, TypeScript, Tailwind, shadcn/ui)
- [ ] NGINX reverse proxy in front of the API (and frontend, once it exists)
- [ ] GitHub Actions CI/CD pipeline
- [ ] OpenAPI-generated TypeScript client
- [ ] Reports/analytics module
- [ ] Institution-level settings module
- [ ] Hosted deployment (Render / Railway / VPS — TBD)

---

## 📖 Repository Philosophy

This project is written as **production software, not a tutorial**:

- **Production over tutorials** — every module models a real workflow (registration, grading, fee collection), not a toy CRUD example.
- **Clean Architecture** — routes, services, and repositories are separated on purpose, so business rules never depend on FastAPI or SQLAlchemy internals.
- **Maintainability** — one responsibility per layer makes it possible to change persistence, add caching, or swap frameworks without rewriting business logic.
- **Scalability** — an async request path and a layout that already anticipates a frontend, an edge proxy, and CI/CD, so growth doesn't require a rewrite.
- **Developer experience** — auto-generated docs, hot reload, one-command Docker environments, and a real test suite, so contributing doesn't require tribal knowledge.

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

## ⭐ Support

If this project is useful to you:

- ⭐ **Star this repository** — it helps others discover it.
- 🐛 **Report issues** you find via GitHub Issues.
- 💬 **Open a discussion** for questions, ideas, or feedback.
- 🤝 **Contributions are welcome** — see [Contributing](#-contributing) above.

<!-- TODO: Add direct links once the repository is public, e.g.:
[Issues](https://github.com/<TODO-GITHUB-USERNAME>/<TODO-REPO-NAME>/issues) · [Discussions](https://github.com/<TODO-GITHUB-USERNAME>/<TODO-REPO-NAME>/discussions)
-->

---

## 👤 Author

**Yogesh Kumar Sharma**
Python Backend Developer · MCA (Artificial Intelligence)

- GitHub: `GitHub: https://github.com/yogesh-kumar-sharma`
- LinkedIn: `https://linkedin.com/in/yogesh-kumar0`
- Portfolio: `
- Email: `ykumar0052@gmail.com`

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE).
<!-- TODO: Confirm a LICENSE file exists at the repository root; add one if missing. -->

## 🙏 Acknowledgements

Built on the shoulders of [FastAPI](https://fastapi.tiangolo.com/), [SQLAlchemy](https://www.sqlalchemy.org/), [Pydantic](https://docs.pydantic.dev/), and the wider Python async ecosystem.

---

<div align="center">

**Built with FastAPI, PostgreSQL, and Redis — and ❤️ — by Yogesh Kumar Sharma.**

</div>
