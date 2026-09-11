import pytest

from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.identity.infrastructure.persistence.models import User
from modules.studios.application.services import StudioReviewService
from modules.studios.domain.enums import StudioStatus
from modules.studios.infrastructure.persistence.models import Studio


@pytest.mark.django_db
def test_studio_can_be_submitted_and_approved() -> None:
    owner = User.objects.create_user(email="studio@example.com", full_name="Studio")
    reviewer = User.objects.create_user(email="admin@example.com", full_name="Admin")
    studio = Studio.objects.create(
        owner=owner,
        name="Black Room",
        country_code="BR",
        city="São Paulo",
        address="Rua Central, 1",
    )

    StudioReviewService.submit(studio)
    StudioReviewService.review(studio, reviewer, True, "Estrutura aprovada")

    assert studio.status == StudioStatus.APPROVED
    assert AuditEvent.objects.filter(resource_id=str(studio.id)).exists()


@pytest.mark.django_db
def test_studio_rejection_requires_reason() -> None:
    owner = User.objects.create_user(email="studio@example.com", full_name="Studio")
    reviewer = User.objects.create_user(email="admin@example.com", full_name="Admin")
    studio = Studio.objects.create(
        owner=owner,
        name="Black Room",
        country_code="BR",
        city="São Paulo",
        address="Rua Central, 1",
        status=StudioStatus.UNDER_REVIEW,
    )

    with pytest.raises(ValueError, match="reason"):
        StudioReviewService.review(studio, reviewer, False, "")
