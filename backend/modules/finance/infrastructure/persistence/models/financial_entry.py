import uuid

from django.core.validators import MinValueValidator
from django.db import models

from modules.finance.domain.enums import FinancialEntryStatus, FinancialEntryType


class FinancialEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guest = models.ForeignKey(
        "guests.Guest",
        on_delete=models.PROTECT,
        related_name="financial_entries",
    )
    closing = models.ForeignKey(
        "sales.Closing",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="financial_entries",
    )
    entry_type = models.CharField(max_length=24, choices=FinancialEntryType.choices)
    status = models.CharField(max_length=16, choices=FinancialEntryStatus.choices)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    currency = models.CharField(max_length=3)
    source_reference = models.CharField(max_length=160)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "finance_financial_entry"
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["entry_type", "source_reference"],
                name="uq_financial_entry_type_source",
            )
        ]

    def __str__(self) -> str:
        return f"{self.entry_type}:{self.amount} {self.currency}"
