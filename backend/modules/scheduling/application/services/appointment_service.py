from zoneinfo import ZoneInfo

from django.db import transaction

from modules.artists.infrastructure.persistence.models import ArtistAvailability
from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.guests.infrastructure.persistence.models import GuestStudio
from modules.scheduling.infrastructure.persistence.models import Appointment


class AppointmentService:
    @staticmethod
    @transaction.atomic
    def create(*, actor, **data) -> Appointment:
        guest = data["guest"]
        starts_at = data["starts_at"]
        ends_at = data["ends_at"]
        studio = data["studio"]
        if ends_at <= starts_at:
            raise ValueError("The end time must be after the start time.")
        zone = ZoneInfo(guest.timezone)
        guest_start = starts_at.astimezone(zone).date()
        guest_end = ends_at.astimezone(zone).date()
        if guest_start < guest.starts_on or guest_end > guest.ends_on:
            raise ValueError("The appointment must be within the Guest period.")
        if data["currency"] != guest.currency:
            raise ValueError("The appointment currency must match the Guest currency.")
        if not ArtistAvailability.objects.filter(
            artist=guest.artist,
            starts_at__lte=starts_at,
            ends_at__gte=ends_at,
        ).exists():
            raise ValueError("The appointment is outside the Artist availability.")
        if not GuestStudio.objects.filter(
            guest=guest,
            studio=studio,
            starts_at__lte=starts_at,
            ends_at__gte=ends_at,
        ).exists():
            raise ValueError("The Studio is not assigned to this Guest for the selected period.")
        appointment = Appointment.objects.create(
            artist=guest.artist,
            created_by=actor,
            **data,
        )
        AuditEvent.objects.create(
            actor=actor,
            action="appointment.created",
            resource_type="Appointment",
            resource_id=str(appointment.id),
            changes={"status": appointment.status},
        )
        return appointment
