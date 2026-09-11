from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from modules.artists.infrastructure.persistence.models import ArtistProfile
from modules.guests.infrastructure.persistence.models import Guest, GuestProposal
from modules.identity.infrastructure.persistence.models import User
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
