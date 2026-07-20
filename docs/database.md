# Database Setup

The API uses SQLAlchemy 2.0's asynchronous engine with the `asyncpg`
PostgreSQL driver. A request receives an `AsyncSession` through the
`get_db_session` dependency; services explicitly commit successful business
transactions, while database errors trigger a rollback.

## Migrations

Alembic is configured for async models. Once a model is added, generate a
migration from the project root:

```bash
alembic revision --autogenerate -m "describe schema change"
alembic upgrade head
```

Use `DATABASE_URL` from `.env`; do not hard-code credentials in migration files.
The shared `Base`, `UUIDPrimaryKeyMixin`, and `TimestampMixin` are in
`app/database/base.py` and should be used for all persistent entities.

