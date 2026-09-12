from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from modules.artists.application.services import ArtistApplicationService
from modules.artists.domain.enums import ApplicationStatus
from modules.artists.infrastructure.persistence.models import ArtistApplication, ArtistProfile
from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.identity.domain.enums import RoleType
from modules.identity.infrastructure.persistence.models import Role, User, UserRole


@pytest.mark.django_db
def test_application_submission_and_approval_are_audited() -> None:
    artist_user = User.objects.create_user(email="artist@example.com", full_name="Artist")
    reviewer = User.objects.create_user(email="admin@example.com", full_name="Admin")
    profile = ArtistProfile.objects.create(
        user=artist_user,
        professional_name="Ink",
        styles=["blackwork"],
        minimum_tattoo_value=Decimal("500"),
        expected_ticket=Decimal("900"),
    )
    application = ArtistApplication.objects.create(artist=profile)

    ArtistApplicationService.submit(application)
    ArtistApplicationService.review(application, reviewer, True, "Portfólio aprovado")

    assert application.status == ApplicationStatus.APPROVED
    assert AuditEvent.objects.filter(resource_id=str(application.id)).exists()


@pytest.mark.django_db
def test_rejection_requires_reason() -> None:
    user = User.objects.create_user(email="artist@example.com", full_name="Artist")
    reviewer = User.objects.create_user(email="admin@example.com", full_name="Admin")
    profile = ArtistProfile.objects.create(
        user=user,
        professional_name="Ink",
        styles=["fine line"],
        minimum_tattoo_value=Decimal("500"),
        expected_ticket=Decimal("900"),
    )
    application = ArtistApplication.objects.create(
        artist=profile,
        status=ApplicationStatus.UNDER_REVIEW,
    )

    with pytest.raises(ValueError, match="reason"):
        ArtistApplicationService.review(application, reviewer, False, "")


@pytest.mark.django_db
def test_application_endpoint_repairs_missing_application_for_existing_profile() -> None:
    user = User.objects.create_user(email="repair-artist@example.com", full_name="Repair Artist")
    role = Role.objects.create(code=RoleType.ARTIST, name="Artist")
    UserRole.objects.create(user=user, role=role)
    ArtistProfile.objects.create(
        user=user,
        professional_name="Repair Ink",
        styles=["blackwork"],
        minimum_tattoo_value=Decimal("500.00"),
        expected_ticket=Decimal("900.00"),
    )
    client = APIClient()
    client.force_authenticate(user)

    response = client.get("/api/v1/artists/me/application/")

    assert response.status_code == 200
    assert response.data["status"] == ApplicationStatus.DRAFT
    assert ArtistApplication.objects.filter(artist__user=user).count() == 1


@pytest.mark.django_db
def test_first_profile_creation_creates_application_via_api() -> None:
    user = User.objects.create_user(email="first-profile@example.com", full_name="Artist")
    role = Role.objects.create(code=RoleType.ARTIST, name="Artista")
    UserRole.objects.create(user=user, role=role)
    client = APIClient()
    client.force_authenticate(user)

    response = client.put(
        "/api/v1/artists/me/",
        {
            "professional_name": "Ink",
            "styles": ["blackwork"],
            "minimum_tattoo_value": "500",
            "expected_ticket": "900",
        },
        format="json",
    )

    assert response.status_code == 200
    profile = ArtistProfile.objects.get(user=user)
    assert ArtistApplication.objects.filter(artist=profile).exists()
