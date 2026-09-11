import uuid

from django.conf import settings
from django.db import models

from modules.scheduling.domain.enums import CancellationResponsibility, CancellationStatus


class CancellationRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appointment = models.ForeignKey(
        "scheduling.Appointment",
        on_delete=models.PROTECT,
        related_name="cancellation_requests",
    )
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="cancellation_requests_created",
    )
    responsibility = models.CharField(
        max_length=16,
        choices=CancellationResponsibility.choices,
        default=CancellationResponsibility.ARTIST,
    )
    reason = models.TextField()
    status = models.CharField(
        max_length=16,
        choices=CancellationStatus.choices,
        default=CancellationStatus.PENDING,
    )
    decided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="cancellation_requests_decided",
    )
    decision_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    decided_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "scheduling_cancellation_request"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.appointment_id}:{self.status}"
