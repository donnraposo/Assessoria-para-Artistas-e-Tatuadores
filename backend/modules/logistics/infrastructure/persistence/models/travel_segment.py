import uuid

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from modules.logistics.domain.enums import LogisticsStatus, TravelSegmentType


class TravelSegment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guest = models.ForeignKey(
        "guests.Guest",
        on_delete=models.PROTECT,
        related_name="travel_segments",
    )
    segment_type = models.CharField(max_length=12, choices=TravelSegmentType.choices)
    origin = models.CharField(max_length=160)
    destination = models.CharField(max_length=160)
    departs_at = models.DateTimeField()
    arrives_at = models.DateTimeField()
    origin_timezone = models.CharField(max_length=64)
    destination_timezone = models.CharField(max_length=64)
    provider = models.CharField(max_length=120, blank=True)
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
        db_table = "logistics_travel_segment"
        ordering = ["departs_at"]

    def __str__(self) -> str:
        return f"{self.origin}:{self.destination}:{self.departs_at.isoformat()}"
