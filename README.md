# College ERP Management System — Backend

Production-oriented FastAPI REST API for college users, academics, attendance,
exams, fees, notices, documents, and dashboards.

## Current progress

All 18 planned modules are implemented.

## Technology stack

- Python 3.12+
- FastAPI and Pydantic v2
- PostgreSQL with SQLAlchemy 2.0 and Alembic
- Redis
- JWT authentication with refresh tokens
- Pytest and Docker (added in their respective modules)

## Features

- JWT authentication, refresh-token rotation, password reset/change, and RBAC
- User, Student, and Faculty profiles with configurable local uploads
- Departments, courses, semesters, subjects, sessions, and timetable
- Attendance reports, examinations/results/CGPA, fees/payments, and notices
- Admin, Faculty, and Student dashboards

## API modules

Swagger and ReDoc are available at `/docs` and `/redoc`. Core versioned routes:

| Module | Prefix |
| --- | --- |
| Authentication | `/api/v1/auth` |
| Users / Roles | `/api/v1/users`, `/api/v1/roles` |
| Students / Faculty | `/api/v1/students`, `/api/v1/faculty` |
| Academic / Attendance | `/api/v1/academic`, `/api/v1/attendance` |
| Exams / Fees | `/api/v1/examinations`, `/api/v1/fees` |
| Notices / Documents | `/api/v1/notices`, `/api/v1/documents` |
| Dashboards | `/api/v1/dashboard` |

## Folder structure

```text
app/
├── api/             # HTTP routes
├── core/            # Configuration and application-wide concerns
├── database/        # Engine, sessions, migrations
├── models/          # SQLAlchemy models
├── schemas/         # Pydantic request/response schemas
├── repositories/    # Persistence layer
├── services/        # Business logic
├── security/        # Authentication and authorization
├── dependencies/    # FastAPI dependency providers
├── middleware/      # Request/response middleware
└── utils/           # Reusable utilities
tests/               # Automated tests
migrations/          # Alembic migrations
docs/                # Architecture and deployment documentation
```

## Run the starter application

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Visit `/health`, `/docs`, or `/redoc` once the server is running.

## Configuration

Copy `.env.example` to `.env` before starting future modules. Never commit the
generated `.env` file or real secrets. See `docs/configuration.md` for all
available settings and production safeguards.

Database migrations are managed with Alembic; see `docs/database.md`.

Authentication endpoints and token lifecycle are documented in
`docs/authentication.md`.

Role policy and admin role-management endpoints are documented in `docs/rbac.md`.

User profile, deactivation, and profile-picture endpoints are documented in
`docs/users.md`.

Student admissions and access rules are documented in `docs/students.md`.

Faculty profiles and assignment access are documented in `docs/faculty.md`.

The normalized academic catalog and timetable are documented in `docs/academic.md`.

Testing instructions are available in `docs/testing.md`.

Docker Compose deployment instructions are in `docs/docker.md`.

## Documentation

- `docs/architecture.md` — application layers
- `docs/database-schema.md` — entity relationships
- `docs/configuration.md` — environment configuration
- `docs/testing.md` — test setup and coverage
- `docs/deployment.md` — deployment checklist

## Future improvements

- S3/MinIO storage adapter and signed download URLs
- Email provider for reset-token delivery
- Redis-backed rate limiting and cached dashboards
- CI pipeline, database integration tests, and observability export
