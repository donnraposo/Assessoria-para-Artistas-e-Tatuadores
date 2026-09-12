from datetime import datetime

from django.db import models, transaction

from modules.artists.infrastructure.persistence.models import ArtistAvailability, ArtistProfile
from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.identity.infrastructure.persistence.models import User
from modules.scheduling.domain.enums import AppointmentStatus
from modules.scheduling.infrastructure.persistence.models import Appointment

ACTIVE_APPOINTMENT_STATUSES = [
    AppointmentStatus.CONFIRMED,
    AppointmentStatus.CANCELLATION_REQUESTED,
]


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

    @staticmethod
    @transaction.atomic
    def update(
        availability: ArtistAvailability,
        starts_at: datetime,
        ends_at: datetime,
        timezone: str,
    ) -> ArtistAvailability:
        if availability.changed_by_advisory:
            raise ValueError("Only the Advisory can change an advisory-managed window.")
        if ends_at <= starts_at:
            raise ValueError("The end time must be after the start time.")
        overlap = ArtistAvailability.objects.filter(
            artist=availability.artist,
            starts_at__lt=ends_at,
            ends_at__gt=starts_at,
        ).exclude(pk=availability.pk)
        if overlap.exists():
            raise ValueError("The time range overlaps another availability window.")
        if not ArtistAvailabilityService._appointments_still_fit(
            availability.artist, availability.starts_at, availability.ends_at, starts_at, ends_at
        ):
            raise ValueError(
                "Cannot change availability while a confirmed appointment falls outside "
                "the new range."
            )
        availability.starts_at = starts_at
        availability.ends_at = ends_at
        availability.timezone = timezone
        availability.save(update_fields=["starts_at", "ends_at", "timezone", "updated_at"])
        return availability

    @staticmethod
    @transaction.atomic
    def delete(availability: ArtistAvailability) -> None:
        if availability.changed_by_advisory:
            raise ValueError("Only the Advisory can remove an advisory-managed window.")
        conflict = Appointment.objects.filter(
            artist=availability.artist,
            starts_at__lt=availability.ends_at,
            ends_at__gt=availability.starts_at,
            status__in=ACTIVE_APPOINTMENT_STATUSES,
        ).exists()
        if conflict:
            raise ValueError(
                "Cannot remove availability with a confirmed appointment in this window."
            )
        availability.delete()

    @staticmethod
    def _appointments_still_fit(
        artist, old_starts_at, old_ends_at, new_starts_at, new_ends_at
    ) -> bool:
        affected = Appointment.objects.filter(
            artist=artist,
            starts_at__lt=old_ends_at,
            ends_at__gt=old_starts_at,
            status__in=ACTIVE_APPOINTMENT_STATUSES,
        )
        return not affected.filter(
            models.Q(starts_at__lt=new_starts_at) | models.Q(ends_at__gt=new_ends_at)
        ).exists()
