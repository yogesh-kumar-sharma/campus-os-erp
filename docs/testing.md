# Testing

Install the development dependencies, then run the suite from the project root:

```bash
pip install -e ".[dev]"
pytest -q
pytest --cov=app --cov-report=term-missing
```

The test suite covers health checks, configuration safeguards, JWT purpose
validation, schemas, roles, Student/Faculty inputs, academic date/time rules,
attendance payloads, and grade-boundary calculations. Database-backed API tests
should run against a dedicated PostgreSQL test database configured with
`APP_ENV=testing`.
