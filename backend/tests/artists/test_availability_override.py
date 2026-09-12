from datetime import timedelta
from decimal import Decimal

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from modules.artists.infrastructure.persistence.models import ArtistAvailability, ArtistProfile
from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.identity.domain.enums import RoleType
from modules.identity.infrastructure.persistence.models import Role, User, UserRole


def build_availability(suffix: str) -> ArtistAvailability:
    user = User.objects.create_user(email=f"artist-{suffix}@example.com", full_name="Ana Ink")
    role, _ = Role.objects.get_or_create(code=RoleType.ARTIST, defaults={"name": "Artist"})
    UserRole.objects.create(user=user, role=role)
    artist = ArtistProfile.objects.create(
        user=user,
        professional_name="Ana Ink",
        styles=["blackwork"],
        minimum_tattoo_value=Decimal("500"),
        expected_ticket=Decimal("900"),
    )
    starts_at = timezone.now() + timedelta(days=10)
    return ArtistAvailability.objects.create(
        artist=artist,
        starts_at=starts_at,
        ends_at=starts_at + timedelta(hours=6),
        timezone="Europe/Lisbon",
    )


def build_advisory(suffix: str) -> User:
    user = User.objects.create_user(email=f"advisory-{suffix}@example.com", full_name="Ops Lead")
    role, _ = Role.objects.get_or_create(code=RoleType.ADVISORY, defaults={"name": "Advisory"})
    UserRole.objects.create(user=user, role=role)
    return user


@pytest.mark.django_db
def test_advisory_override_records_before_after_actor_and_reason() -> None:
    availability = build_availability("override")
    advisory = build_advisory("override")
    previous_start = availability.starts_at
    new_start = availability.starts_at + timedelta(hours=2)
    client = APIClient()
    client.force_authenticate(advisory)

    response = client.post(
        f"/api/v1/artists/availability/{availability.id}/override/",
        {
            "starts_at": new_start.isoformat(),
            "ends_at": (new_start + timedelta(hours=4)).isoformat(),
            "reason": "Studio changed the operating hours.",
        },
        format="json",
    )

    assert response.status_code == 200
    availability.refresh_from_db()
    assert availability.changed_by_advisory is True
    assert availability.change_reason == "Studio changed the operating hours."
    event = AuditEvent.objects.get(
        resource_id=str(availability.id),
        action="artist_availability.overridden",
    )
    assert event.actor_id == advisory.id
    assert event.reason == "Studio changed the operating hours."
    assert event.changes["starts_at"]["from"] == previous_start.isoformat()
    assert event.changes["starts_at"]["to"] == availability.starts_at.isoformat()


@pytest.mark.django_db
def test_override_without_reason_is_refused_at_the_contract() -> None:
    availability = build_availability("no-reason")
    advisory = build_advisory("no-reason")
    client = APIClient()
    client.force_authenticate(advisory)

    response = client.post(
        f"/api/v1/artists/availability/{availability.id}/override/",
        {
            "starts_at": availability.starts_at.isoformat(),
            "ends_at": availability.ends_at.isoformat(),
            "reason": "   ",
        },
        format="json",
    )

    assert response.status_code == 400
    availability.refresh_from_db()
    assert availability.changed_by_advisory is False


@pytest.mark.django_db
def test_override_cannot_create_an_overlapping_window() -> None:
    availability = build_availability("overlap")
    advisory = build_advisory("overlap")
    neighbour_start = availability.ends_at + timedelta(hours=1)
    ArtistAvailability.objects.create(
        artist=availability.artist,
        starts_at=neighbour_start,
        ends_at=neighbour_start + timedelta(hours=3),
        timezone="Europe/Lisbon",
    )
    client = APIClient()
    client.force_authenticate(advisory)

    response = client.post(
        f"/api/v1/artists/availability/{availability.id}/override/",
        {
            "starts_at": availability.starts_at.isoformat(),
            "ends_at": (neighbour_start + timedelta(hours=1)).isoformat(),
            "reason": "Extending the window.",
        },
        format="json",
    )

    assert response.status_code == 409


@pytest.mark.django_db
def test_artist_cannot_use_the_advisory_override() -> None:
    availability = build_availability("forbidden")
    client = APIClient()
    client.force_authenticate(availability.artist.user)

    response = client.post(
        f"/api/v1/artists/availability/{availability.id}/override/",
        {
            "starts_at": availability.starts_at.isoformat(),
            "ends_at": availability.ends_at.isoformat(),
            "reason": "Trying to self-serve.",
        },
        format="json",
    )

    assert response.status_code == 403
