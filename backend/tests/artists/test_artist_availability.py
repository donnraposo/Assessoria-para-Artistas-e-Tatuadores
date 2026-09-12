from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from modules.artists.application.services import ArtistAvailabilityService
from modules.artists.infrastructure.persistence.models import ArtistAvailability, ArtistProfile
from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.identity.domain.enums import RoleType
from modules.identity.infrastructure.persistence.models import Role, User, UserRole


@pytest.mark.django_db
def test_overlapping_availability_is_rejected() -> None:
    user = User.objects.create_user(email="artist@example.com", full_name="Artist")
    role = Role.objects.create(code=RoleType.ARTIST, name="Artista")
    UserRole.objects.create(user=user, role=role)
    profile = ArtistProfile.objects.create(
        user=user,
        professional_name="Ink",
        styles=["blackwork"],
        minimum_tattoo_value=Decimal("500"),
        expected_ticket=Decimal("900"),
    )
    start = datetime.now(UTC) + timedelta(days=1)
    ArtistAvailability.objects.create(
        artist=profile,
        starts_at=start,
        ends_at=start + timedelta(hours=4),
        timezone="America/Sao_Paulo",
    )
    client = APIClient()
    client.force_authenticate(user)

    response = client.post(
        "/api/v1/artists/me/availability/",
        {
            "starts_at": (start + timedelta(hours=1)).isoformat(),
            "ends_at": (start + timedelta(hours=5)).isoformat(),
            "timezone": "America/Sao_Paulo",
        },
        format="json",
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_advisory_can_override_availability_with_reason() -> None:
    artist_user = User.objects.create_user(email="artist@example.com", full_name="Artist")
    advisory_user = User.objects.create_user(email="advisory@example.com", full_name="Advisory")
    Role.objects.create(code=RoleType.ARTIST, name="Artista")
    advisory_role = Role.objects.create(code=RoleType.ADVISORY, name="Advisory")
    UserRole.objects.create(user=advisory_user, role=advisory_role)
    profile = ArtistProfile.objects.create(
        user=artist_user,
        professional_name="Ink",
        styles=["blackwork"],
        minimum_tattoo_value=Decimal("500"),
        expected_ticket=Decimal("900"),
    )
    start = datetime.now(UTC) + timedelta(days=1)
    client = APIClient()
    client.force_authenticate(advisory_user)

    response = client.post(
        f"/api/v1/artists/{profile.id}/availability/override/",
        {
            "starts_at": start.isoformat(),
            "ends_at": (start + timedelta(hours=4)).isoformat(),
            "timezone": "America/Sao_Paulo",
            "reason": "Encaixe excepcional de Guest confirmado",
        },
        format="json",
    )

    assert response.status_code == 201
    availability = ArtistAvailability.objects.get(artist=profile)
    assert availability.changed_by_advisory is True
    assert availability.change_reason == "Encaixe excepcional de Guest confirmado"
    assert AuditEvent.objects.filter(
        resource_id=str(availability.id),
        action="artist_availability.overridden_by_advisory",
        actor=advisory_user,
    ).exists()


@pytest.mark.django_db
def test_advisory_override_requires_reason() -> None:
    artist_user = User.objects.create_user(email="artist@example.com", full_name="Artist")
    profile = ArtistProfile.objects.create(
        user=artist_user,
        professional_name="Ink",
        styles=["blackwork"],
        minimum_tattoo_value=Decimal("500"),
        expected_ticket=Decimal("900"),
    )
    start = datetime.now(UTC) + timedelta(days=1)

    with pytest.raises(ValueError, match="reason"):
        ArtistAvailabilityService.override_by_advisory(
            artist=profile,
            actor=artist_user,
            starts_at=start,
            ends_at=start + timedelta(hours=4),
            timezone="America/Sao_Paulo",
            reason="   ",
        )


@pytest.mark.django_db
def test_artist_cannot_call_advisory_override_endpoint() -> None:
    artist_user = User.objects.create_user(email="artist@example.com", full_name="Artist")
    Role.objects.create(code=RoleType.ARTIST, name="Artista")
    profile = ArtistProfile.objects.create(
        user=artist_user,
        professional_name="Ink",
        styles=["blackwork"],
        minimum_tattoo_value=Decimal("500"),
        expected_ticket=Decimal("900"),
    )
    start = datetime.now(UTC) + timedelta(days=1)
    client = APIClient()
    client.force_authenticate(artist_user)

    response = client.post(
        f"/api/v1/artists/{profile.id}/availability/override/",
        {
            "starts_at": start.isoformat(),
            "ends_at": (start + timedelta(hours=4)).isoformat(),
            "timezone": "America/Sao_Paulo",
            "reason": "Tentativa indevida",
        },
        format="json",
    )

    assert response.status_code == 403
