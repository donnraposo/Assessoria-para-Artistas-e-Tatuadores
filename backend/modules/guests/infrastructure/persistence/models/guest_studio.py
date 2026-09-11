import uuid

from django.core.exceptions import ValidationError
from django.db import models


class GuestStudio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guest = models.ForeignKey("guests.Guest", on_delete=models.CASCADE, related_name="studios")
    studio = models.ForeignKey("studios.Studio", on_delete=models.PROTECT)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "guests_guest_studio"
        ordering = ["starts_at"]

    def __str__(self) -> str:
        return f"{self.guest}:{self.studio}"

    def clean(self) -> None:
        if self.ends_at <= self.starts_at:
            raise ValidationError("The end date must be after the start date.")
