import uuid

from django.core.validators import MinValueValidator
from django.db import models

from modules.studios.domain.enums import PricingType


class StudioPrice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    studio = models.ForeignKey("studios.Studio", on_delete=models.CASCADE, related_name="prices")
    pricing_type = models.CharField(max_length=20, choices=PricingType.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3)
    conditions = models.TextField(blank=True)
    valid_from = models.DateField()
    valid_until = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "studios_price"

    def __str__(self) -> str:
        return f"{self.studio}:{self.pricing_type}:{self.amount}"
