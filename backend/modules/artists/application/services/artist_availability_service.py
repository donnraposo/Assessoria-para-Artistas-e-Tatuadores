from datetime import datetime

from django.db import transaction

from modules.artists.infrastructure.persistence.models import ArtistAvailability, ArtistProfile
from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.identity.infrastructure.persistence.models import User


class ArtistAvailabilityService:
    @staticmethod
    @transaction.atomic
    def override_by_advisory(
        artist: ArtistProfile,
        actor: User,
        starts_at: datetime,
        ends_at: datetime,
        timezone: str,
        reason: str,
    ) -> ArtistAvailability:
        reason = reason.strip()
        if not reason:
            raise ValueError("An advisory override requires a reason.")
        if ends_at <= starts_at:
            raise ValueError("The end time must be after the start time.")
        overlap = ArtistAvailability.objects.filter(
            artist=artist,
            starts_at__lt=ends_at,
            ends_at__gt=starts_at,
        )
        if overlap.exists():
            raise ValueError("The time range overlaps another availability window.")
        availability = ArtistAvailability.objects.create(
            artist=artist,
            starts_at=starts_at,
            ends_at=ends_at,
            timezone=timezone,
            changed_by_advisory=True,
            change_reason=reason,
        )
        AuditEvent.objects.create(
            actor=actor,
            action="artist_availability.overridden_by_advisory",
            resource_type="ArtistAvailability",
            resource_id=str(availability.id),
            reason=reason,
            changes={
                "artist_id": str(artist.id),
                "starts_at": starts_at.isoformat(),
                "ends_at": ends_at.isoformat(),
            },
        )
        return availability
