import uuid

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from modules.marketing.domain.enums import CampaignStatus


class Campaign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guest = models.ForeignKey("guests.Guest", on_delete=models.PROTECT, related_name="campaigns")
    name = models.CharField(max_length=160)
    channel = models.CharField(max_length=80)
    authorized_budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    currency = models.CharField(max_length=3)
    starts_on = models.DateField()
    ends_on = models.DateField()
    status = models.CharField(
        max_length=16,
        choices=CampaignStatus.choices,
        default=CampaignStatus.DRAFT,
    )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "marketing_campaign"
        ordering = ["-starts_on"]

    def __str__(self) -> str:
        return self.name
