from decimal import Decimal

import pytest

from modules.finance.domain.enums import FinancialEntryStatus, FinancialEntryType
from modules.finance.infrastructure.persistence.models import FinancialEntry
from modules.sales.application.services import ClosingService
from modules.scheduling.application.services import CancellationService
from modules.scheduling.domain.enums import AppointmentStatus, CancellationStatus
from tests.sales.test_closing import build_scenario


@pytest.mark.django_db
def test_artist_requests_and_advisory_approves_cancellation() -> None:
    artist_user, advisory, _, lead, appointment = build_scenario("cancellation")
    ClosingService.close(
        lead=lead,
        appointment=appointment,
        actor=advisory,
        final_value=Decimal("1000.00"),
        currency="BRL",
        artist_minimum_approved=False,
        payment_reference="payment-cancel",
        idempotency_key="close-cancel",
    )
    cancellation = CancellationService.request(
        appointment=appointment,
        actor=artist_user,
        reason="I cannot travel.",
    )
    decided = CancellationService.decide(
        cancellation=cancellation,
        actor=advisory,
        approved=True,
        reason="Travel issue confirmed.",
    )

    appointment.refresh_from_db()
    refund = FinancialEntry.objects.get(entry_type=FinancialEntryType.ARTIST_REFUND_DUE)
    assert decided.status == CancellationStatus.APPROVED
    assert appointment.status == AppointmentStatus.CANCELLED
    assert refund.amount == Decimal("200.00")
    assert refund.status == FinancialEntryStatus.DUE


@pytest.mark.django_db
def test_another_artist_cannot_request_cancellation() -> None:
    _, advisory, _, lead, appointment = build_scenario("ownership")
    other_artist = type(advisory).objects.create_user(
        email="other-artist@example.com",
        full_name="Other Artist",
    )
    ClosingService.close(
        lead=lead,
        appointment=appointment,
        actor=advisory,
        final_value=Decimal("900.00"),
        currency="BRL",
        artist_minimum_approved=False,
        payment_reference="payment-owner",
        idempotency_key="close-owner",
    )
    with pytest.raises(ValueError, match="assigned Artist"):
        CancellationService.request(
            appointment=appointment,
            actor=other_artist,
            reason="Invalid owner.",
        )
