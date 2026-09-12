from decimal import ROUND_HALF_UP, Decimal

from django.db.models import Sum

from modules.finance.domain.enums import FinancialEntryStatus, FinancialEntryType
from modules.finance.infrastructure.persistence.models import FinancialEntry
from modules.marketing.infrastructure.persistence.models import AdSpend, Campaign
from modules.sales.infrastructure.persistence.models import Closing, Lead
from modules.scheduling.application.services import OccupancyService


class MetricsService:
    money_precision = Decimal("0.01")

    @classmethod
    def calculate(cls, guest) -> dict:
        leads = Lead.objects.filter(guest=guest).count()
        closings = Closing.objects.filter(lead__guest=guest, currency=guest.currency)
        closing_count = closings.count()
        gross_revenue = closings.aggregate(total=Sum("final_value"))["total"] or Decimal("0")
        agency_revenue = FinancialEntry.objects.filter(
            guest=guest,
            currency=guest.currency,
            entry_type=FinancialEntryType.AGENCY_REVENUE,
            status=FinancialEntryStatus.CONFIRMED,
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0")
        authorized_budget = Campaign.objects.filter(guest=guest, currency=guest.currency).aggregate(
            total=Sum("authorized_budget")
        )["total"] or Decimal("0")
        ad_spend = AdSpend.objects.filter(
            campaign__guest=guest,
            currency=guest.currency,
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0")
        return {
            "currency": guest.currency,
            "leads": leads,
            "closings": closing_count,
            "gross_revenue": gross_revenue,
            "agency_revenue": agency_revenue,
            "authorized_ad_budget": authorized_budget,
            "ad_spend": ad_spend,
            "conversion_percentage": cls._percentage(closing_count, leads),
            "cost_per_lead": cls._ratio(ad_spend, leads),
            "cost_per_closing": cls._ratio(ad_spend, closing_count),
            "roas": cls._ratio(gross_revenue, ad_spend),
            "occupancy": OccupancyService.calculate(guest),
        }

    @classmethod
    def _ratio(cls, numerator, denominator):
        if not denominator:
            return None
        return (Decimal(numerator) / Decimal(denominator)).quantize(
            cls.money_precision,
            rounding=ROUND_HALF_UP,
        )

    @classmethod
    def _percentage(cls, numerator, denominator):
        if not denominator:
            return None
        return (Decimal(numerator) * Decimal("100") / Decimal(denominator)).quantize(
            cls.money_precision,
            rounding=ROUND_HALF_UP,
        )
