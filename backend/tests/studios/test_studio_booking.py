from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from modules.artists.infrastructure.persistence.models import ArtistProfile
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


@pytest.mark.django_db
def test_studio_lists_only_its_own_booking_requests() -> None:
    artist_user = User.objects.create_user(email="artist-list@example.com", full_name="Artist")
    owner = User.objects.create_user(email="studio-list@example.com", full_name="Studio")
    other_owner = User.objects.create_user(email="other-studio@example.com", full_name="Other")
    advisory = User.objects.create_user(email="admin-list@example.com", full_name="Admin")
    role = Role.objects.create(code=RoleType.STUDIO, name="Studio")
    UserRole.objects.create(user=owner, role=role)
    UserRole.objects.create(user=other_owner, role=role)
    artist = ArtistProfile.objects.create(
        user=artist_user,
        professional_name="List Ink",
        styles=["blackwork"],
        minimum_tattoo_value=Decimal("500"),
        expected_ticket=Decimal("900"),
    )
    studio = Studio.objects.create(
        owner=owner,
        name="List Studio",
        country_code="BR",
        city="Sao Paulo",
        address="Main Street, 1",
        status=StudioStatus.APPROVED,
    )
    start = datetime.now(UTC) + timedelta(days=3)
    proposal = GuestProposal.objects.create(
        artist=artist,
        primary_studio=studio,
        city="Sao Paulo",
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
    StudioBookingRequest.objects.create(
        guest=guest,
        studio=studio,
        artist=artist,
        requested_by=advisory,
        starts_at=start,
        ends_at=start + timedelta(hours=4),
        timezone="America/Sao_Paulo",
    )
    client = APIClient()
    client.force_authenticate(owner)
    own_response = client.get("/api/v1/studios/me/booking-requests/")
    client.force_authenticate(other_owner)
    other_response = client.get("/api/v1/studios/me/booking-requests/")

    assert own_response.status_code == 200
    assert len(own_response.data) == 1
    assert other_response.status_code == 200
    assert other_response.data == []
