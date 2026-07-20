# Architecture

The backend uses a layered FastAPI design:

```text
API routes → services → repositories → SQLAlchemy models → PostgreSQL
                 ↓
          security, validation, file storage, configuration
```

- Routes provide HTTP and RBAC boundaries.
- Services own business rules and transaction coordination.
- Repositories isolate query logic.
- Pydantic schemas validate external inputs and shape responses.
- SQLAlchemy async sessions access PostgreSQL; Alembic owns schema evolution.

Redis is provisioned for caching and future token/session extensions. Uploaded
files use `LocalFileStorage`, whose relative-path interface permits later S3 or
MinIO replacement without changing business APIs.
