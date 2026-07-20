# Configuration

The application reads settings from environment variables. For local work, copy
`.env.example` to `.env` and replace the sample values before enabling external
services.

| Variable | Purpose | Default |
| --- | --- | --- |
| `APP_ENV` | `development`, `testing`, `staging`, or `production` | `development` |
| `DEBUG` | Enables development diagnostics | `true` |
| `DATABASE_URL` | Async PostgreSQL connection URL | Local sample URL |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` |
| `JWT_SECRET_KEY` | Secret used to sign tokens | Placeholder (invalid in production) |
| `CORS_ORIGINS` | Comma-separated permitted browser origins | `http://localhost:3000` |
| `STORAGE_PATH` | Local upload storage root | `storage` |

Production will fail fast if the placeholder JWT secret remains in use or no
CORS origins are configured. Do not commit `.env` files or deployment secrets.
