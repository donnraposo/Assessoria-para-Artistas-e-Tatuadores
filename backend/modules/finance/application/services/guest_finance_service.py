from decimal import Decimal

from django.db.models import Sum

from modules.finance.domain.enums import FinancialEntryStatus, FinancialEntryType
from modules.finance.infrastructure.persistence.models import FinancialEntry


class GuestFinanceService:
    @staticmethod
    def summarize(guest) -> dict:
        entries = FinancialEntry.objects.filter(guest=guest, currency=guest.currency)

        def total(entry_type: str, status: str) -> Decimal:
            return entries.filter(entry_type=entry_type, status=status).aggregate(
                total=Sum("amount")
            )["total"] or Decimal("0")

        return {
            "currency": guest.currency,
            "agency_revenue_confirmed": total(
                FinancialEntryType.AGENCY_REVENUE, FinancialEntryStatus.CONFIRMED
            ),
            "artist_receivable_expected": total(
                FinancialEntryType.ARTIST_RECEIVABLE, FinancialEntryStatus.EXPECTED
            ),
            "artist_receivable_confirmed": total(
                FinancialEntryType.ARTIST_RECEIVABLE, FinancialEntryStatus.CONFIRMED
            ),
            "artist_refund_due": total(
                FinancialEntryType.ARTIST_REFUND_DUE, FinancialEntryStatus.DUE
            ),
            "artist_refund_confirmed": total(
                FinancialEntryType.ARTIST_REFUND_DUE, FinancialEntryStatus.CONFIRMED
            ),
            "entries": entries.order_by("created_at"),
        }
