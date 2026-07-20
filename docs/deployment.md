# Deployment Guide

1. Set production secrets (`JWT_SECRET_KEY`, database password, CORS origins).
2. Build and start the Compose stack: `docker compose up --build -d`.
3. Confirm `GET /health` and inspect `/docs`.
4. Create the first administrator using `python -m app.utils.create_admin`.
5. Back up PostgreSQL and persistent storage volumes before each upgrade.

Use a reverse proxy with HTTPS in production. Keep PostgreSQL and Redis private,
rotate JWT secrets deliberately, and use object storage for high-volume uploads.
