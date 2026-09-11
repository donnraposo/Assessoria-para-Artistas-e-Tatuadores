import uuid

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from modules.scheduling.domain.enums import AppointmentStatus


class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guest = models.ForeignKey("guests.Guest", on_delete=models.PROTECT, related_name="appointments")
    artist = models.ForeignKey("artists.ArtistProfile", on_delete=models.PROTECT)
    studio = models.ForeignKey("studios.Studio", on_delete=models.PROTECT)
    client_name = models.CharField(max_length=160)
    client_email = models.EmailField(blank=True)
    client_phone = models.CharField(max_length=40, blank=True)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    timezone = models.CharField(max_length=64)
    final_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    currency = models.CharField(max_length=3)
    status = models.CharField(
        max_length=24,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.PENDING_PAYMENT,
    )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "scheduling_appointment"
        ordering = ["starts_at"]
        indexes = [models.Index(fields=["artist", "starts_at", "ends_at"])]

    def __str__(self) -> str:
        return f"{self.client_name}:{self.starts_at.isoformat()}"
