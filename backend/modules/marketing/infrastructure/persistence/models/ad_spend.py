import uuid

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class AdSpend(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(
        "marketing.Campaign",
        on_delete=models.PROTECT,
        related_name="spend_entries",
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    currency = models.CharField(max_length=3)
    spent_on = models.DateField()
    external_reference = models.CharField(max_length=160, blank=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "marketing_ad_spend"
        ordering = ["spent_on", "created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["campaign", "external_reference"],
                condition=~models.Q(external_reference=""),
                name="uq_ad_spend_campaign_reference",
            )
        ]

    def __str__(self) -> str:
        return f"{self.campaign_id}:{self.amount} {self.currency}"
