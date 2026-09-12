from decimal import Decimal

import pytest

from modules.marketing.application.services import CampaignService, MetricsService
from modules.sales.application.services import ClosingService
from modules.sales.infrastructure.persistence.models import Lead
from tests.sales.test_closing import build_scenario


@pytest.mark.django_db
def test_guest_metrics_are_derived_from_operational_records() -> None:
    _, advisory, guest, lead, appointment = build_scenario("metrics")
    Lead.objects.create(
        guest=guest,
        source="Referral",
        client_name="Second Lead",
        created_by=advisory,
    )
    campaign = CampaignService.create(
        guest=guest,
        name="Lisbon launch",
        channel="Meta Ads",
        authorized_budget=Decimal("500.00"),
        currency="BRL",
        starts_on=guest.starts_on,
        ends_on=guest.ends_on,
        actor=advisory,
    )
    CampaignService.add_spend(
        campaign=campaign,
        amount=Decimal("100.00"),
        currency="BRL",
        spent_on=guest.starts_on,
        external_reference="meta-001",
        actor=advisory,
    )
    ClosingService.close(
        lead=lead,
        appointment=appointment,
        actor=advisory,
        final_value=Decimal("1000.00"),
        currency="BRL",
        artist_minimum_approved=False,
        payment_reference="payment-metrics",
        idempotency_key="close-metrics",
    )

    metrics = MetricsService.calculate(guest)

    assert metrics["leads"] == 2
    assert metrics["closings"] == 1
    assert metrics["gross_revenue"] == Decimal("1000.00")
    assert metrics["agency_revenue"] == Decimal("200.00")
    assert metrics["conversion_percentage"] == Decimal("50.00")
    assert metrics["cost_per_lead"] == Decimal("50.00")
    assert metrics["cost_per_closing"] == Decimal("100.00")
    assert metrics["roas"] == Decimal("10.00")


@pytest.mark.django_db
def test_metrics_return_null_for_undefined_denominators() -> None:
    _, _, guest, _, _ = build_scenario("zero")
    metrics = MetricsService.calculate(guest)

    assert metrics["closings"] == 0
    assert metrics["cost_per_closing"] is None
    assert metrics["roas"] is None


@pytest.mark.django_db
def test_campaign_rejects_currency_outside_guest_currency() -> None:
    _, advisory, guest, _, _ = build_scenario("currency")
    with pytest.raises(ValueError, match="currency"):
        CampaignService.create(
            guest=guest,
            name="Wrong currency",
            channel="Search",
            authorized_budget=Decimal("100.00"),
            currency="USD",
            starts_on=guest.starts_on,
            ends_on=guest.ends_on,
            actor=advisory,
        )
