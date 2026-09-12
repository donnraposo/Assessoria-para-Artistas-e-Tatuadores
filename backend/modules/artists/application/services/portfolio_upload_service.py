from datetime import timedelta
from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from modules.artists.infrastructure.persistence.models import PendingPortfolioUpload, PortfolioItem
from modules.artists.infrastructure.storage import PortfolioStorage
from modules.audit.infrastructure.persistence.models import AuditEvent


class PortfolioUploadService:
    MIME_SIGNATURES = {
        "image/jpeg": (b"\xff\xd8\xff",),
        "image/png": (b"\x89PNG\r\n\x1a\n",),
        "image/webp": (b"RIFF",),
    }
    EXTENSIONS = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}

    @staticmethod
    def request(*, artist, **data) -> tuple[PendingPortfolioUpload, str]:
        content_type = data["content_type"]
        extension = PortfolioUploadService.EXTENSIONS[content_type]
        allowed_extensions = {extension, ".jpeg" if extension == ".jpg" else extension}
        if Path(data["original_name"]).suffix.lower() not in allowed_extensions:
            raise ValueError("The file extension does not match its image format.")
        upload = PendingPortfolioUpload.objects.create(
            artist=artist,
            object_key=f"portfolio/{artist.id}/{uuid4()}{extension}",
            expires_at=timezone.now() + timedelta(seconds=settings.S3_UPLOAD_EXPIRATION_SECONDS),
            **data,
        )
        url = PortfolioStorage().create_upload_url(upload.object_key, upload.content_type)
        return upload, url

    @staticmethod
    @transaction.atomic
    def confirm(*, upload: PendingPortfolioUpload, actor) -> PortfolioItem:
        locked = PendingPortfolioUpload.objects.select_for_update().get(pk=upload.pk)
        existing = PortfolioItem.objects.filter(object_key=locked.object_key).first()
        if existing:
            return existing
        if locked.expires_at <= timezone.now():
            raise ValueError("The upload request has expired.")
        size, content_type, prefix = PortfolioStorage().inspect(locked.object_key)
        if size != locked.size_bytes or content_type != locked.content_type:
            raise ValueError("The uploaded file metadata does not match the request.")
        signatures = PortfolioUploadService.MIME_SIGNATURES[locked.content_type]
        signature_matches = any(prefix.startswith(signature) for signature in signatures)
        if locked.content_type == "image/webp":
            signature_matches = prefix.startswith(b"RIFF") and prefix[8:12] == b"WEBP"
        if not signature_matches:
            raise ValueError("The uploaded content is not a supported image.")
        item = PortfolioItem.objects.create(
            artist=locked.artist,
            object_key=locked.object_key,
            original_name=locked.original_name,
            content_type=locked.content_type,
            size_bytes=locked.size_bytes,
            caption=locked.caption,
            style=locked.style,
            position=locked.position,
        )
        locked.confirmed_at = timezone.now()
        locked.save(update_fields=["confirmed_at"])
        AuditEvent.objects.create(
            actor=actor,
            action="portfolio.uploaded",
            resource_type="PortfolioItem",
            resource_id=str(item.id),
            changes={"content_type": item.content_type, "size_bytes": item.size_bytes},
        )
        return item

    @staticmethod
    @transaction.atomic
    def delete(*, item: PortfolioItem, actor) -> None:
        PortfolioStorage().delete(item.object_key)
        resource_id = str(item.id)
        item.delete()
        AuditEvent.objects.create(
            actor=actor,
            action="portfolio.deleted",
            resource_type="PortfolioItem",
            resource_id=resource_id,
            changes={},
        )
