from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from modules.artists.infrastructure.persistence.models import ArtistAvailability, ArtistProfile
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
