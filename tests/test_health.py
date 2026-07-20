"""Smoke tests for the application entry point."""

from fastapi.testclient import TestClient

from app.main import app


def test_health_check_returns_service_status() -> None:
    """The health endpoint should be publicly available."""
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "college-erp-api"}

