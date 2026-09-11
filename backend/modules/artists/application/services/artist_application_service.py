from django.db import transaction
from django.utils import timezone

from modules.artists.domain.enums import ApplicationStatus
from modules.artists.infrastructure.persistence.models import ArtistApplication
from modules.audit.infrastructure.persistence.models import AuditEvent


class ArtistApplicationService:
    @staticmethod
    @transaction.atomic
    def submit(application: ArtistApplication) -> ArtistApplication:
        if application.status != ApplicationStatus.DRAFT:
            raise ValueError("Only draft applications can be submitted.")
        if not application.artist.styles:
            raise ValueError("Add at least one tattoo style.")
        application.status = ApplicationStatus.UNDER_REVIEW
        application.submitted_at = timezone.now()
        application.save(update_fields=["status", "submitted_at", "updated_at"])
        return application

    @staticmethod
    @transaction.atomic
    def review(
        application: ArtistApplication,
        reviewer,
        approved: bool,
        reason: str,
    ) -> ArtistApplication:
        if application.status != ApplicationStatus.UNDER_REVIEW:
            raise ValueError("The application is not under review.")
        if not approved and not reason.strip():
            raise ValueError("Rejection requires a reason.")
        previous = application.status
        application.status = ApplicationStatus.APPROVED if approved else ApplicationStatus.REJECTED
        application.reviewed_by = reviewer
        application.review_reason = reason.strip()
        application.reviewed_at = timezone.now()
        application.save()
        AuditEvent.objects.create(
            actor=reviewer,
            action="artist_application.reviewed",
            resource_type="ArtistApplication",
            resource_id=str(application.id),
            reason=reason.strip(),
            changes={"status": {"from": previous, "to": application.status}},
        )
        return application
