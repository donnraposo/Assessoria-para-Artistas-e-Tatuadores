from django.db import transaction

from modules.artists.infrastructure.persistence.models import ArtistAvailability
from modules.audit.infrastructure.persistence.models import AuditEvent


class ArtistAvailabilityService:
    """RN-008: the Advisory may change availability, keeping history and reason."""

    @staticmethod
    @transaction.atomic
    def override(
        *,
        availability: ArtistAvailability,
        actor,
        starts_at,
        ends_at,
        reason: str,
    ) -> ArtistAvailability:
        if not reason.strip():
            raise ValueError("An advisory override requires a reason.")
        locked = ArtistAvailability.objects.select_for_update().get(pk=availability.pk)
        if ends_at <= starts_at:
            raise ValueError("The end time must be after the start time.")
        overlap = ArtistAvailability.objects.filter(
            artist=locked.artist,
            starts_at__lt=ends_at,
            ends_at__gt=starts_at,
        ).exclude(pk=locked.pk)
        if overlap.exists():
            raise ValueError("The time range overlaps another availability window.")
        previous = {
            "starts_at": locked.starts_at.isoformat(),
            "ends_at": locked.ends_at.isoformat(),
        }
        locked.starts_at = starts_at
        locked.ends_at = ends_at
        locked.changed_by_advisory = True
        locked.change_reason = reason.strip()
        locked.save(
            update_fields=[
                "starts_at",
                "ends_at",
                "changed_by_advisory",
                "change_reason",
                "updated_at",
            ]
        )
        AuditEvent.objects.create(
            actor=actor,
            action="artist_availability.overridden",
            resource_type="ArtistAvailability",
            resource_id=str(locked.id),
            reason=locked.change_reason,
            changes={
                "starts_at": {"from": previous["starts_at"], "to": locked.starts_at.isoformat()},
                "ends_at": {"from": previous["ends_at"], "to": locked.ends_at.isoformat()},
            },
        )
        return locked
