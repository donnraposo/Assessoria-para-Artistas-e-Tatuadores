import uuid

from django.core.validators import MinValueValidator
from django.db import models

from modules.finance.domain.enums import ReceiptStatus


class AgencyReceipt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    closing = models.OneToOneField(
        "sales.Closing",
        on_delete=models.PROTECT,
        related_name="agency_receipt",
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    currency = models.CharField(max_length=3)
    external_reference = models.CharField(max_length=160)
    idempotency_key = models.CharField(max_length=120, unique=True)
    status = models.CharField(
        max_length=16,
        choices=ReceiptStatus.choices,
        default=ReceiptStatus.CONFIRMED,
    )
    confirmed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "finance_agency_receipt"

    def __str__(self) -> str:
        return self.external_reference
