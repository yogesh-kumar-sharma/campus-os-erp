"""Tests for stable role definitions."""

from app.models.role import RoleName


def test_system_roles_match_the_access_policy() -> None:
    """The initial policy must expose administrator, faculty, and student roles."""
    assert {role.value for role in RoleName} == {"admin", "faculty", "student"}
