from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from django.db import transaction

from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.logistics.infrastructure.persistence.models import TravelSegment


class TravelSegmentService:
    @staticmethod
    @transaction.atomic
    def create(*, actor, **data) -> TravelSegment:
        TravelSegmentService._validate(data)
        segment = TravelSegment.objects.create(created_by=actor, **data)
        AuditEvent.objects.create(
            actor=actor,
            action="travel_segment.created",
            resource_type="TravelSegment",
            resource_id=str(segment.id),
            changes={"status": segment.status, "cost": str(segment.cost)},
        )
        return segment

    @staticmethod
    @transaction.atomic
    def update(*, segment: TravelSegment, actor, **data) -> TravelSegment:
        locked = TravelSegment.objects.select_for_update().get(pk=segment.pk)
        values = {
            field: data.get(field, getattr(locked, field))
            for field in [
                "guest",
                "departs_at",
                "arrives_at",
                "origin_timezone",
                "destination_timezone",
                "currency",
            ]
        }
        TravelSegmentService._validate(values)
        changed = {}
        for field, value in data.items():
            previous = getattr(locked, field)
            if previous != value:
                changed[field] = {"from": str(previous), "to": str(value)}
                setattr(locked, field, value)
        locked.save()
        AuditEvent.objects.create(
            actor=actor,
            action="travel_segment.updated",
            resource_type="TravelSegment",
            resource_id=str(locked.id),
            changes=changed,
        )
        return locked

    @staticmethod
    def _validate(data) -> None:
        if data["arrives_at"] <= data["departs_at"]:
            raise ValueError("The arrival time must be after the departure time.")
        if data["currency"] != data["guest"].currency:
            raise ValueError("The travel currency must match the Guest currency.")
        try:
            ZoneInfo(data["origin_timezone"])
            ZoneInfo(data["destination_timezone"])
        except ZoneInfoNotFoundError as error:
            raise ValueError("A valid IANA timezone is required.") from error
