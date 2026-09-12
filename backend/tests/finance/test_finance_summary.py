from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.finance.application.services import FinancialEntryService, GuestFinanceService
from modules.finance.domain.enums import FinancialEntryStatus, FinancialEntryType
from modules.finance.infrastructure.persistence.models import FinancialEntry
from modules.sales.application.services import ClosingService
from tests.sales.test_closing import build_scenario


@pytest.mark.django_db
def test_guest_finance_summary_reflects_expected_artist_balance() -> None:
    artist_user, advisory, guest, lead, appointment = build_scenario("finance-summary")
    ClosingService.close(
        lead=lead,
        appointment=appointment,
        actor=advisory,
        final_value=Decimal("1000.00"),
        currency="BRL",
        artist_minimum_approved=False,
        payment_reference="payment-finance-summary",
        idempotency_key="close-finance-summary",
    )

    summary = GuestFinanceService.summarize(guest)

    assert summary["agency_revenue_confirmed"] == Decimal("200.00")
    assert summary["artist_receivable_expected"] == Decimal("800.00")
    assert summary["artist_receivable_confirmed"] == Decimal("0")


@pytest.mark.django_db
def test_confirming_artist_receivable_moves_it_out_of_expected_balance() -> None:
    artist_user, advisory, guest, lead, appointment = build_scenario("finance-confirm")
    ClosingService.close(
        lead=lead,
        appointment=appointment,
        actor=advisory,
        final_value=Decimal("1000.00"),
        currency="BRL",
        artist_minimum_approved=False,
        payment_reference="payment-finance-confirm",
        idempotency_key="close-finance-confirm",
    )
    receivable = FinancialEntry.objects.get(
        guest=guest, entry_type=FinancialEntryType.ARTIST_RECEIVABLE
    )

    FinancialEntryService.confirm(receivable, advisory, "Paid via bank transfer")

    summary = GuestFinanceService.summarize(guest)
    assert summary["artist_receivable_expected"] == Decimal("0")
    assert summary["artist_receivable_confirmed"] == Decimal("800.00")
    assert AuditEvent.objects.filter(
        resource_id=str(receivable.id), action="financial_entry.confirmed"
    ).exists()


@pytest.mark.django_db
def test_confirming_an_already_confirmed_entry_is_rejected() -> None:
    artist_user, advisory, guest, lead, appointment = build_scenario("finance-double-confirm")
    ClosingService.close(
        lead=lead,
        appointment=appointment,
        actor=advisory,
        final_value=Decimal("1000.00"),
        currency="BRL",
        artist_minimum_approved=False,
        payment_reference="payment-finance-double",
        idempotency_key="close-finance-double",
    )
    revenue = FinancialEntry.objects.get(
        guest=guest,
        entry_type=FinancialEntryType.AGENCY_REVENUE,
        status=FinancialEntryStatus.CONFIRMED,
    )

    with pytest.raises(ValueError, match="already confirmed"):
        FinancialEntryService.confirm(revenue, advisory)


@pytest.mark.django_db
def test_artist_can_view_own_guest_finance_summary_via_api() -> None:
    artist_user, advisory, guest, lead, appointment = build_scenario("finance-api")
    ClosingService.close(
        lead=lead,
        appointment=appointment,
        actor=advisory,
        final_value=Decimal("1000.00"),
        currency="BRL",
        artist_minimum_approved=False,
        payment_reference="payment-finance-api",
        idempotency_key="close-finance-api",
    )
    client = APIClient()
    client.force_authenticate(artist_user)

    response = client.get(f"/api/v1/finance/guests/{guest.id}/summary/")

    assert response.status_code == 200
    assert Decimal(str(response.json()["artist_receivable_expected"])) == Decimal("800.00")


@pytest.mark.django_db
def test_other_artist_cannot_view_guest_finance_summary_via_api() -> None:
    artist_user, advisory, guest, lead, appointment = build_scenario("finance-forbidden")
    outsider = build_scenario("finance-outsider")[0]
    client = APIClient()
    client.force_authenticate(outsider)

    response = client.get(f"/api/v1/finance/guests/{guest.id}/summary/")

    assert response.status_code == 403


@pytest.mark.django_db
def test_only_advisory_can_confirm_financial_entries() -> None:
    artist_user, advisory, guest, lead, appointment = build_scenario("finance-permission")
    ClosingService.close(
        lead=lead,
        appointment=appointment,
        actor=advisory,
        final_value=Decimal("1000.00"),
        currency="BRL",
        artist_minimum_approved=False,
        payment_reference="payment-finance-permission",
        idempotency_key="close-finance-permission",
    )
    receivable = FinancialEntry.objects.get(
        guest=guest, entry_type=FinancialEntryType.ARTIST_RECEIVABLE
    )
    client = APIClient()
    client.force_authenticate(artist_user)

    response = client.post(f"/api/v1/finance/entries/{receivable.id}/confirm/")

    assert response.status_code == 403