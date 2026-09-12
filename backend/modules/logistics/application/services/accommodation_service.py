from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from django.db import transaction

from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.guests.infrastructure.persistence.models import GuestStudio
from modules.logistics.infrastructure.persistence.models import Accommodation


class AccommodationService:
    @staticmethod
    @transaction.atomic
    def create(*, actor, **data) -> Accommodation:
        AccommodationService._validate(data)
        accommodation = Accommodation.objects.create(created_by=actor, **data)
        AuditEvent.objects.create(
            actor=actor,
            action="accommodation.created",
            resource_type="Accommodation",
            resource_id=str(accommodation.id),
            changes={"status": accommodation.status, "cost": str(accommodation.cost)},
        )
        return accommodation

    @staticmethod
    @transaction.atomic
    def update(*, accommodation: Accommodation, actor, **data) -> Accommodation:
        locked = Accommodation.objects.select_for_update().get(pk=accommodation.pk)
        values = {
            field: data.get(field, getattr(locked, field))
            for field in [
                "guest",
                "studio",
                "check_in_at",
                "check_out_at",
                "timezone",
                "currency",
            ]
        }
        AccommodationService._validate(values)
        changed = {}
        for field, value in data.items():
            previous = getattr(locked, field)
            if previous != value:
                changed[field] = {"from": str(previous), "to": str(value)}
                setattr(locked, field, value)
        locked.save()
        AuditEvent.objects.create(
            actor=actor,
            action="accommodation.updated",
            resource_type="Accommodation",
            resource_id=str(locked.id),
            changes=changed,
        )
        return locked

    @staticmethod
    def _validate(data) -> None:
        if data["check_out_at"] <= data["check_in_at"]:
            raise ValueError("The check-out time must be after the check-in time.")
        if data["currency"] != data["guest"].currency:
            raise ValueError("The accommodation currency must match the Guest currency.")
        try:
            ZoneInfo(data["timezone"])
        except ZoneInfoNotFoundError as error:
            raise ValueError("A valid IANA timezone is required.") from error
        studio = data.get("studio")
        if studio:
            if not studio.offers_accommodation:
                raise ValueError("The selected Studio does not offer accommodation.")
            if not GuestStudio.objects.filter(guest=data["guest"], studio=studio).exists():
                raise ValueError("The selected Studio is not assigned to this Guest.")
