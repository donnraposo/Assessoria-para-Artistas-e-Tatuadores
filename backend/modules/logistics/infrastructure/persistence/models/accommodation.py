import uuid

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from modules.logistics.domain.enums import LogisticsStatus


class Accommodation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guest = models.ForeignKey(
        "guests.Guest",
        on_delete=models.PROTECT,
        related_name="accommodations",
    )
    studio = models.ForeignKey(
        "studios.Studio",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="guest_accommodations",
    )
    name = models.CharField(max_length=160)
    address = models.CharField(max_length=300)
    check_in_at = models.DateTimeField()
    check_out_at = models.DateTimeField()
    timezone = models.CharField(max_length=64)
    booking_reference = models.CharField(max_length=160, blank=True)
    private_document_key = models.CharField(max_length=300, blank=True)
    status = models.CharField(
        max_length=16,
        choices=LogisticsStatus.choices,
        default=LogisticsStatus.PENDING,
    )
    cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    currency = models.CharField(max_length=3)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "logistics_accommodation"
        ordering = ["check_in_at"]

    def __str__(self) -> str:
        return f"{self.name}:{self.check_in_at.isoformat()}"
