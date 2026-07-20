# Docker Deployment

1. Copy `.env.example` to `.env`.
2. Set a unique production `JWT_SECRET_KEY`; update `DATABASE_URL` to use
   `postgres` as its hostname and `REDIS_URL` to use `redis`.
3. Run:

```bash
docker compose up --build
```

The API runs at `http://localhost:8000`, Swagger at `/docs`, and ReDoc at
`/redoc`. Compose performs `alembic upgrade head` before starting Uvicorn.

For production, do not expose PostgreSQL or Redis ports publicly, use managed
secrets, and run the API behind TLS termination.
