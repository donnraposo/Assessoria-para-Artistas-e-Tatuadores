from django.db import transaction

from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.guests.infrastructure.persistence.models import Guest, GuestStudio
from modules.studios.domain.enums import StudioStatus
from modules.studios.infrastructure.persistence.models import Studio


class GuestStudioService:
    @staticmethod
    @transaction.atomic
    def add(*, guest: Guest, studio: Studio, actor, starts_at, ends_at) -> GuestStudio:
        if ends_at <= starts_at:
            raise ValueError("The end date must be after the start date.")
        if studio.status != StudioStatus.APPROVED:
            raise ValueError("The Studio must be approved.")
        overlap = GuestStudio.objects.filter(
            guest=guest,
            starts_at__lt=ends_at,
            ends_at__gt=starts_at,
        )
        if overlap.exists():
            raise ValueError("The period overlaps another Studio already assigned to this Guest.")
        guest_studio = GuestStudio.objects.create(
            guest=guest,
            studio=studio,
            starts_at=starts_at,
            ends_at=ends_at,
        )
        AuditEvent.objects.create(
            actor=actor,
            action="guest_studio.added",
            resource_type="GuestStudio",
            resource_id=str(guest_studio.id),
            changes={
                "guest_id": str(guest.id),
                "studio_id": str(studio.id),
                "starts_at": starts_at.isoformat(),
                "ends_at": ends_at.isoformat(),
            },
        )
        return guest_studio
