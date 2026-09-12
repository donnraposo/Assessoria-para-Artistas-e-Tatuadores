from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from modules.artists.infrastructure.persistence.models import ArtistProfile
from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.guests.infrastructure.persistence.models import Guest, GuestProposal
from modules.identity.domain.enums import RoleType
from modules.identity.infrastructure.persistence.models import Role, User, UserRole
from modules.studios.application.services import StudioBookingService
from modules.studios.domain.enums import StudioStatus
from modules.studios.infrastructure.persistence.models import Studio, StudioBookingRequest


@pytest.mark.django_db
def test_overlapping_confirmed_studio_booking_is_rejected() -> None:
    artist_user = User.objects.create_user(email="artist@example.com", full_name="Artist")
    studio_user = User.objects.create_user(email="studio@example.com", full_name="Studio")
    advisory = User.objects.create_user(email="admin@example.com", full_name="Admin")
    artist = ArtistProfile.objects.create(
        user=artist_user,
        professional_name="Ink",
        styles=["blackwork"],
        minimum_tattoo_value=Decimal("500"),
        expected_ticket=Decimal("900"),
    )
    studio = Studio.objects.create(
        owner=studio_user,
        name="Black Room",
        country_code="BR",
        city="São Paulo",
        address="Rua Central, 1",
        status=StudioStatus.APPROVED,
    )
    start = datetime.now(UTC) + timedelta(days=2)
    proposal = GuestProposal.objects.create(
        artist=artist,
        primary_studio=studio,
        city="São Paulo",
        country_code="BR",
        starts_on=start.date(),
        ends_on=(start + timedelta(days=2)).date(),
        timezone="America/Sao_Paulo",
        currency="BRL",
        ads_budget=Decimal("1000"),
        minimum_tattoo_value=Decimal("500"),
        expected_ticket=Decimal("900"),
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
    first = StudioBookingRequest.objects.create(
        guest=guest,
        studio=studio,
        artist=artist,
        requested_by=advisory,
        starts_at=start,
        ends_at=start + timedelta(hours=4),
        timezone="America/Sao_Paulo",
    )
    second = StudioBookingRequest.objects.create(
        guest=guest,
        studio=studio,
        artist=artist,
        requested_by=advisory,
        starts_at=start + timedelta(hours=2),
        ends_at=start + timedelta(hours=6),
        timezone="America/Sao_Paulo",
    )
    StudioBookingService.respond(first, True)
    StudioBookingService.confirm(first, advisory)
    StudioBookingService.respond(second, True)

    with pytest.raises(ValueError, match="conflicting"):
        StudioBookingService.confirm(second, advisory)


def _build_booking_request(**overrides) -> StudioBookingRequest:
    artist_user = User.objects.create_user(
        email=overrides.pop("artist_email", "artist2@example.com"), full_name="Artist"
    )
    studio_user = User.objects.create_user(
        email=overrides.pop("studio_email", "studio2@example.com"), full_name="Studio"
    )
    advisory = (
        overrides.pop("advisory")
        if "advisory" in overrides
        else User.objects.create_user(email="admin2@example.com", full_name="Admin")
    )
    artist = ArtistProfile.objects.create(
        user=artist_user,
        professional_name="Ink",
        styles=["blackwork"],
        minimum_tattoo_value=Decimal("500"),
        expected_ticket=Decimal("900"),
    )
    studio = Studio.objects.create(
        owner=studio_user,
        name="Black Room",
        country_code="BR",
        city="São Paulo",
        address="Rua Central, 1",
        status=StudioStatus.APPROVED,
    )
    start = datetime.now(UTC) + timedelta(days=2)
    proposal = GuestProposal.objects.create(
        artist=artist,
        primary_studio=studio,
        city="São Paulo",
        country_code="BR",
        starts_on=start.date(),
        ends_on=(start + timedelta(days=2)).date(),
        timezone="America/Sao_Paulo",
        currency="BRL",
        ads_budget=Decimal("1000"),
        minimum_tattoo_value=Decimal("500"),
        expected_ticket=Decimal("900"),
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
    defaults = {
        "guest": guest,
        "studio": studio,
        "artist": artist,
        "requested_by": advisory,
        "starts_at": start,
        "ends_at": start + timedelta(hours=4),
        "timezone": "America/Sao_Paulo",
    }
    defaults.update(overrides)
    return StudioBookingRequest.objects.create(**defaults)


@pytest.mark.django_db
def test_advisory_registers_externally_negotiated_response() -> None:
    advisory = User.objects.create_user(email="admin2@example.com", full_name="Admin")
    booking_request = _build_booking_request(advisory=advisory)

    updated = StudioBookingService.register_external_response(
        booking_request, advisory, True, "Confirmed by phone with the Studio owner"
    )

    assert updated.status == "ACCEPTED"
    assert AuditEvent.objects.filter(
        resource_id=str(updated.id), action="studio_booking.external_response_registered"
    ).exists()


@pytest.mark.django_db
def test_external_response_requires_reason() -> None:
    advisory = User.objects.create_user(email="admin2@example.com", full_name="Admin")
    booking_request = _build_booking_request(advisory=advisory)

    with pytest.raises(ValueError, match="reason"):
        StudioBookingService.register_external_response(booking_request, advisory, True, "")


@pytest.mark.django_db
def test_advisory_can_mark_booking_as_paid_via_api() -> None:
    advisory_user = User.objects.create_user(email="admin2@example.com", full_name="Admin")
    advisory_role = Role.objects.create(code=RoleType.ADVISORY, name="Advisory")
    UserRole.objects.create(user=advisory_user, role=advisory_role)
    booking_request = _build_booking_request(advisory=advisory_user)
    StudioBookingService.respond(booking_request, True)
    booking = StudioBookingService.confirm(booking_request, advisory_user)
    client = APIClient()
    client.force_authenticate(advisory_user)

    response = client.patch(
        f"/api/v1/studios/bookings/{booking.id}/payment/",
        {"payment_status": "PAID"},
        format="json",
    )

    assert response.status_code == 200
    assert response.json()["payment_status"] == "PAID"
    assert AuditEvent.objects.filter(
        resource_id=str(booking.id), action="studio_booking.payment_status_changed"
    ).exists()
