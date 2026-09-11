import uuid

from django.conf import settings
from django.db import models

from modules.studios.domain.enums import StudioStatus


class Studio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=160)
    country_code = models.CharField(max_length=2)
    city = models.CharField(max_length=120)
    address = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    amenities = models.JSONField(default=list)
    offers_accommodation = models.BooleanField(default=False)
    accommodation_details = models.TextField(blank=True)
    status = models.CharField(
        max_length=24,
        choices=StudioStatus.choices,
        default=StudioStatus.DRAFT,
    )
    review_reason = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reviewed_studios",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "studios_studio"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
