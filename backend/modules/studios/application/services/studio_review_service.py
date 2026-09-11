from django.db import transaction

from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.studios.domain.enums import StudioStatus
from modules.studios.infrastructure.persistence.models import Studio


class StudioReviewService:
    @staticmethod
    @transaction.atomic
    def submit(studio: Studio) -> Studio:
        if studio.status != StudioStatus.DRAFT:
            raise ValueError("Only draft Studios can be submitted.")
        studio.status = StudioStatus.UNDER_REVIEW
        studio.save(update_fields=["status", "updated_at"])
        return studio

    @staticmethod
    @transaction.atomic
    def review(studio: Studio, reviewer, approved: bool, reason: str) -> Studio:
        if studio.status != StudioStatus.UNDER_REVIEW:
            raise ValueError("The Studio is not under review.")
        if not approved and not reason.strip():
            raise ValueError("Rejection requires a reason.")
        previous = studio.status
        studio.status = StudioStatus.APPROVED if approved else StudioStatus.REJECTED
        studio.reviewed_by = reviewer
        studio.review_reason = reason.strip()
        studio.save()
        AuditEvent.objects.create(
            actor=reviewer,
            action="studio.reviewed",
            resource_type="Studio",
            resource_id=str(studio.id),
            reason=reason.strip(),
            changes={"status": {"from": previous, "to": studio.status}},
        )
        return studio
