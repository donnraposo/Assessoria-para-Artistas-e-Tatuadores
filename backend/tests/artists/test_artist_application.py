from decimal import Decimal

import pytest

from modules.artists.application.services import ArtistApplicationService
from modules.artists.domain.enums import ApplicationStatus
from modules.artists.infrastructure.persistence.models import ArtistApplication, ArtistProfile
from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.identity.infrastructure.persistence.models import User


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
