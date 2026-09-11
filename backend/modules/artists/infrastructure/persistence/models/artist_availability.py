import uuid

from django.core.exceptions import ValidationError
from django.db import models


class ArtistAvailability(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artist = models.ForeignKey("artists.ArtistProfile", on_delete=models.CASCADE)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    timezone = models.CharField(max_length=64)
    changed_by_advisory = models.BooleanField(default=False)
    change_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "artists_availability"
        ordering = ["starts_at"]

    def __str__(self) -> str:
        return f"{self.artist}:{self.starts_at.isoformat()}"

    def clean(self) -> None:
        if self.ends_at <= self.starts_at:
            raise ValidationError("The end time must be after the start time.")
        if self.changed_by_advisory and not self.change_reason.strip():
            raise ValidationError("An advisory override requires a reason.")
