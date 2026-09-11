import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class GuestGoal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guest = models.OneToOneField("guests.Guest", on_delete=models.CASCADE, related_name="goal")
    occupancy_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    revenue_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = "guests_goal"

    def __str__(self) -> str:
        return str(self.guest_id)
