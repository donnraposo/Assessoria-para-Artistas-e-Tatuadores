from datetime import datetime, timedelta
from decimal import Decimal
from zoneinfo import ZoneInfo

import pytest

from modules.artists.infrastructure.persistence.models import ArtistAvailability, ArtistProfile
from modules.finance.domain.enums import FinancialEntryStatus, FinancialEntryType
from modules.finance.infrastructure.persistence.models import AgencyReceipt, FinancialEntry
from modules.guests.infrastructure.persistence.models import Guest, GuestProposal, GuestStudio
from modules.identity.infrastructure.persistence.models import User
from modules.sales.application.services import ClosingService
from modules.sales.infrastructure.persistence.models import Lead
from modules.scheduling.application.services import AppointmentService
from modules.scheduling.domain.enums import AppointmentStatus
from modules.studios.domain.enums import StudioStatus
from modules.studios.infrastructure.persistence.models import Studio


def build_scenario(email_suffix: str = "base"):
    artist_user = User.objects.create_user(
        email=f"artist-{email_suffix}@example.com", full_name="Artist"
    )
    studio_user = User.objects.create_user(
        email=f"studio-{email_suffix}@example.com", full_name="Studio"
    )
    advisory = User.objects.create_user(
        email=f"admin-{email_suffix}@example.com", full_name="Admin"
    )
    artist = ArtistProfile.objects.create(
        user=artist_user,
        professional_name=f"Ink {email_suffix}",
        styles=["blackwork"],
        minimum_tattoo_value=Decimal("500.00"),
        expected_ticket=Decimal("900.00"),
    )
    studio = Studio.objects.create(
        owner=studio_user,
        name=f"Black Room {email_suffix}",
        country_code="BR",
        city="Sao Paulo",
        address="Central Street, 1",
        status=StudioStatus.APPROVED,
    )
    zone = ZoneInfo("America/Sao_Paulo")
    start = (datetime.now(zone) + timedelta(days=10)).replace(
        hour=10,
        minute=0,
        second=0,
        microsecond=0,
    )
    proposal = GuestProposal.objects.create(
        artist=artist,
        primary_studio=studio,
        city="Sao Paulo",
        country_code="BR",
        starts_on=start.date(),
        ends_on=(start + timedelta(days=2)).date(),
        timezone="America/Sao_Paulo",
        currency="BRL",
        ads_budget=Decimal("1000.00"),
        minimum_tattoo_value=Decimal("500.00"),
        expected_ticket=Decimal("900.00"),
    )
    guest = Guest.objects.create(
        proposal=proposal,
        artist=artist,
        city=proposal.city,
        country_code=proposal.country_code,
        starts_on=proposal.starts_on,
        ends_on=proposal.ends_on,
        timezone=proposal.timezone,
        currency=proposal.currency,
    )
    GuestStudio.objects.create(
        guest=guest,
        studio=studio,
        starts_at=start - timedelta(hours=1),
        ends_at=start + timedelta(days=2),
    )
    ArtistAvailability.objects.create(
        artist=artist,
        starts_at=start,
        ends_at=start + timedelta(hours=8),
        timezone=guest.timezone,
    )
    lead = Lead.objects.create(
        guest=guest,
        source="Instagram",
        client_name="Taylor Client",
        created_by=advisory,
    )
    appointment = AppointmentService.create(
        guest=guest,
        studio=studio,
        client_name=lead.client_name,
        starts_at=start,
        ends_at=start + timedelta(hours=4),
        timezone=guest.timezone,
        currency=guest.currency,
        actor=advisory,
    )
    return artist_user, advisory, guest, lead, appointment


@pytest.mark.django_db
def test_closing_is_atomic_idempotent_and_splits_twenty_eighty() -> None:
    _, advisory, _, lead, appointment = build_scenario()
    closing = ClosingService.close(
        lead=lead,
        appointment=appointment,
        actor=advisory,
        final_value=Decimal("999.99"),
        currency="BRL",
        artist_minimum_approved=False,
        payment_reference="payment-001",
        idempotency_key="close-001",
    )
    repeated = ClosingService.close(
        lead=lead,
        appointment=appointment,
        actor=advisory,
        final_value=Decimal("999.99"),
        currency="BRL",
        artist_minimum_approved=False,
        payment_reference="payment-001",
        idempotency_key="close-001",
    )

    appointment.refresh_from_db()
    entries = FinancialEntry.objects.filter(closing=closing)
    assert repeated.id == closing.id
    assert appointment.status == AppointmentStatus.CONFIRMED
    assert AgencyReceipt.objects.get(closing=closing).amount == Decimal("200.00")
    assert entries.get(entry_type=FinancialEntryType.AGENCY_REVENUE).status == (
        FinancialEntryStatus.CONFIRMED
    )
    assert entries.get(entry_type=FinancialEntryType.ARTIST_RECEIVABLE).amount == Decimal("799.99")


@pytest.mark.django_db
def test_closing_respects_artist_minimum_and_approval() -> None:
    _, advisory, _, lead, appointment = build_scenario("minimum")
    with pytest.raises(ValueError, match="below"):
        ClosingService.close(
            lead=lead,
            appointment=appointment,
            actor=advisory,
            final_value=Decimal("499.99"),
            currency="BRL",
            artist_minimum_approved=False,
            payment_reference="payment-low",
            idempotency_key="close-low",
        )
    with pytest.raises(ValueError, match="approval"):
        ClosingService.close(
            lead=lead,
            appointment=appointment,
            actor=advisory,
            final_value=Decimal("500.00"),
            currency="BRL",
            artist_minimum_approved=False,
            payment_reference="payment-min",
            idempotency_key="close-min",
        )


@pytest.mark.django_db
def test_second_conflicting_appointment_cannot_be_closed() -> None:
    _, advisory, guest, first_lead, first = build_scenario("conflict")
    second_lead = Lead.objects.create(
        guest=guest,
        source="Referral",
        client_name="Second Client",
        created_by=advisory,
    )
    second = AppointmentService.create(
        guest=guest,
        studio=first.studio,
        client_name=second_lead.client_name,
        starts_at=first.starts_at + timedelta(hours=1),
        ends_at=first.ends_at + timedelta(hours=1),
        timezone=guest.timezone,
        currency=guest.currency,
        actor=advisory,
    )
    ClosingService.close(
        lead=first_lead,
        appointment=first,
        actor=advisory,
        final_value=Decimal("900.00"),
        currency="BRL",
        artist_minimum_approved=False,
        payment_reference="payment-first",
        idempotency_key="close-first",
    )
    with pytest.raises(ValueError, match="conflicting"):
        ClosingService.close(
            lead=second_lead,
            appointment=second,
            actor=advisory,
            final_value=Decimal("900.00"),
            currency="BRL",
            artist_minimum_approved=False,
            payment_reference="payment-second",
            idempotency_key="close-second",
        )
