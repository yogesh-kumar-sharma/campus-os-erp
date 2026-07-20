"""Local upload storage designed for later replacement by object storage."""

from pathlib import Path
from uuid import UUID, uuid4

from fastapi import UploadFile

from app.core.config import get_settings


class UnsupportedUploadError(Exception):
    """Raised when an uploaded file is too large or not an accepted image."""


class LocalFileStorage:
    """Store profile images under a configurable, non-public local directory."""

    _image_extensions = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}

    async def store_profile_picture(self, user_id: UUID, upload: UploadFile) -> str:
        """Validate and save a profile image, returning a relative storage path."""
        extension = self._image_extensions.get(upload.content_type or "")
        if extension is None:
            raise UnsupportedUploadError("Only JPEG, PNG, and WebP profile images are accepted")
        settings = get_settings()
        maximum_bytes = settings.max_upload_size_mb * 1024 * 1024
        content = await upload.read(maximum_bytes + 1)
        if not content or len(content) > maximum_bytes:
            raise UnsupportedUploadError(
                "Profile image is empty or exceeds the configured size limit"
            )
        relative_path = (
            Path("profile_pictures") / str(user_id) / f"{uuid4()}{extension}"
        )
        destination = settings.storage_path / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
        return relative_path.as_posix()
