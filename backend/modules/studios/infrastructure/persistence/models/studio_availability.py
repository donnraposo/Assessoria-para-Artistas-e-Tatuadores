import uuid

from django.core.exceptions import ValidationError
from django.db import models


class StudioAvailability(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    studio = models.ForeignKey(
        "studios.Studio",
        on_delete=models.CASCADE,
        related_name="availability",
    )
    workstation = models.ForeignKey(
        "studios.Workstation",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    capacity = models.PositiveSmallIntegerField(default=1)
    timezone = models.CharField(max_length=64)

    class Meta:
        db_table = "studios_availability"
        ordering = ["starts_at"]

    def __str__(self) -> str:
        return f"{self.studio}:{self.starts_at.isoformat()}"

    def clean(self) -> None:
        if self.ends_at <= self.starts_at:
            raise ValidationError("The end time must be after the start time.")
        if self.capacity < 1:
            raise ValidationError("Capacity must be positive.")
