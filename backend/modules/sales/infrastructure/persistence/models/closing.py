import uuid

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Closing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lead = models.OneToOneField("sales.Lead", on_delete=models.PROTECT, related_name="closing")
    appointment = models.OneToOneField(
        "scheduling.Appointment",
        on_delete=models.PROTECT,
        related_name="closing",
    )
    final_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    currency = models.CharField(max_length=3)
    artist_minimum_approved = models.BooleanField(default=False)
    closed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    closed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sales_closing"

    def __str__(self) -> str:
        return str(self.id)
