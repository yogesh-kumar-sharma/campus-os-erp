"""Password hashing and verification helpers."""

from passlib.context import CryptContext

_password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plaintext password with bcrypt."""
    return _password_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Verify a plaintext password against a stored hash."""
    return _password_context.verify(plain_password, password_hash)
