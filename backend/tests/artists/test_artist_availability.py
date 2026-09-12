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
    artist_user = User.objects.create_user(email="artist-ov@example.com", full_name="Artist")
    advisory_user = User.objects.create_user(email="advisory-ov@example.com", full_name="Advisory")
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
    assert AuditEvent.objects.filter(
        resource_id=str(availability.id),
        action="artist_availability.overridden_by_advisory",
        actor=advisory_user,
    ).exists()


@pytest.mark.django_db
def test_advisory_override_requires_reason() -> None:
    artist_user = User.objects.create_user(email="artist-ov2@example.com", full_name="Artist")
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
    artist_user = User.objects.create_user(email="artist-ov3@example.com", full_name="Artist")
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


def _build_artist_with_availability(email: str = "artist-crud@example.com"):
    user = User.objects.create_user(email=email, full_name="Artist")
    role, _ = Role.objects.get_or_create(code=RoleType.ARTIST, defaults={"name": "Artista"})
    UserRole.objects.create(user=user, role=role)
    profile = ArtistProfile.objects.create(
        user=user,
        professional_name="Ink",
        styles=["blackwork"],
        minimum_tattoo_value=Decimal("500"),
        expected_ticket=Decimal("900"),
    )
    start = datetime.now(UTC) + timedelta(days=1)
    availability = ArtistAvailability.objects.create(
        artist=profile,
        starts_at=start,
        ends_at=start + timedelta(hours=4),
        timezone="America/Sao_Paulo",
    )
    return user, profile, availability


@pytest.mark.django_db
def test_artist_can_edit_own_availability_window() -> None:
    user, profile, availability = _build_artist_with_availability()
    client = APIClient()
    client.force_authenticate(user)
    new_start = availability.starts_at + timedelta(hours=1)

    response = client.patch(
        f"/api/v1/artists/me/availability/{availability.id}/",
        {
            "starts_at": new_start.isoformat(),
            "ends_at": (new_start + timedelta(hours=4)).isoformat(),
            "timezone": "America/Sao_Paulo",
        },
        format="json",
    )

    assert response.status_code == 200
    availability.refresh_from_db()
    assert availability.starts_at == new_start


@pytest.mark.django_db
def test_artist_can_delete_own_availability_window() -> None:
    user, profile, availability = _build_artist_with_availability()
    client = APIClient()
    client.force_authenticate(user)

    response = client.delete(f"/api/v1/artists/me/availability/{availability.id}/")

    assert response.status_code == 204
    assert not ArtistAvailability.objects.filter(pk=availability.id).exists()


@pytest.mark.django_db
def test_artist_cannot_edit_advisory_managed_window() -> None:
    user, profile, availability = _build_artist_with_availability()
    availability.changed_by_advisory = True
    availability.change_reason = "Advisory override"
    availability.save(update_fields=["changed_by_advisory", "change_reason"])
    client = APIClient()
    client.force_authenticate(user)

    response = client.patch(
        f"/api/v1/artists/me/availability/{availability.id}/",
        {
            "starts_at": availability.starts_at.isoformat(),
            "ends_at": (availability.ends_at + timedelta(hours=1)).isoformat(),
            "timezone": "America/Sao_Paulo",
        },
        format="json",
    )

    assert response.status_code == 409


@pytest.mark.django_db
def test_artist_cannot_delete_window_with_confirmed_appointment() -> None:
    from modules.guests.infrastructure.persistence.models import Guest, GuestProposal
    from modules.scheduling.domain.enums import AppointmentStatus
    from modules.scheduling.infrastructure.persistence.models import Appointment
    from modules.studios.domain.enums import StudioStatus
    from modules.studios.infrastructure.persistence.models import Studio

    user, profile, availability = _build_artist_with_availability()
    studio_user = User.objects.create_user(email="studio-crud@example.com", full_name="Studio")
    studio = Studio.objects.create(
        owner=studio_user,
        name="Black Room",
        country_code="BR",
        city="São Paulo",
        address="Rua Central, 1",
        status=StudioStatus.APPROVED,
    )
    proposal = GuestProposal.objects.create(
        artist=profile,
        primary_studio=studio,
        city="São Paulo",
        country_code="BR",
        starts_on=availability.starts_at.date(),
        ends_on=availability.ends_at.date(),
        timezone="America/Sao_Paulo",
        currency="BRL",
        ads_budget=Decimal("1000"),
        minimum_tattoo_value=Decimal("500"),
        expected_ticket=Decimal("900"),
    )
    guest = Guest.objects.create(
        proposal=proposal,
        artist=profile,
        city=proposal.city,
        country_code=proposal.country_code,
        starts_on=proposal.starts_on,
        ends_on=proposal.ends_on,
        timezone=proposal.timezone,
        currency=proposal.currency,
    )
    Appointment.objects.create(
        guest=guest,
        artist=profile,
        studio=studio,
        client_name="Client",
        starts_at=availability.starts_at,
        ends_at=availability.starts_at + timedelta(hours=1),
        timezone="America/Sao_Paulo",
        currency="BRL",
        status=AppointmentStatus.CONFIRMED,
        created_by=user,
    )
    client = APIClient()
    client.force_authenticate(user)

    response = client.delete(f"/api/v1/artists/me/availability/{availability.id}/")

    assert response.status_code == 409
    assert ArtistAvailability.objects.filter(pk=availability.id).exists()


@pytest.mark.django_db
def test_advisory_can_list_artist_availability() -> None:
    _, profile, availability = _build_artist_with_availability()
    advisory = User.objects.create_user(email="advisory-list@example.com", full_name="Advisory")
    role, _ = Role.objects.get_or_create(code=RoleType.ADVISORY, defaults={"name": "Advisory"})
    UserRole.objects.create(user=advisory, role=role)
    client = APIClient()
    client.force_authenticate(advisory)

    response = client.get(f"/api/v1/artists/{profile.id}/availability/")

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [str(availability.id)]


@pytest.mark.django_db
def test_artist_cannot_list_another_artist_availability_via_advisory_endpoint() -> None:
    user, profile, _ = _build_artist_with_availability(email="artist-list-forbidden@example.com")
    client = APIClient()
    client.force_authenticate(user)

    response = client.get(f"/api/v1/artists/{profile.id}/availability/")

    assert response.status_code == 403
