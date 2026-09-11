import uuid

from django.conf import settings
from django.db import models

from modules.studios.domain.enums import BookingStatus


class StudioBookingRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guest = models.ForeignKey(
        "guests.Guest",
        on_delete=models.PROTECT,
        related_name="studio_booking_requests",
    )
    studio = models.ForeignKey(
        "studios.Studio",
        on_delete=models.PROTECT,
        related_name="booking_requests",
    )
    artist = models.ForeignKey("artists.ArtistProfile", on_delete=models.PROTECT)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    timezone = models.CharField(max_length=64)
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.REQUESTED,
    )
    response_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "studios_booking_request"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.studio}:{self.starts_at.isoformat()}"
