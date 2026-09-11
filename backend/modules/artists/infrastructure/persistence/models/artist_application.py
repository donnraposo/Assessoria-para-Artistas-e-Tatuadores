import uuid

from django.conf import settings
from django.db import models

from modules.artists.domain.enums import ApplicationStatus


class ArtistApplication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artist = models.OneToOneField("artists.ArtistProfile", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=24,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.DRAFT,
    )
    review_reason = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reviewed_artist_applications",
    )
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "artists_application"

    def __str__(self) -> str:
        return f"{self.artist}:{self.status}"
